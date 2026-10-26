#!/usr/bin/env python3
"""Price and macro feed for the FT Stock Picking Game (roadmap item 59, playbook 6.12, 21 Oct 2026).

Runs on GitHub Actions (.github/workflows/feed.yml), where the open internet is reachable. It exists because
Claude's scheduled runs can no longer rely on fetching price pages: on 20 Oct the fetch tool refused every address
it had not first seen in a search result, and nine of the evening review's rows went missing. The feed reads the
same kinds of figures straight from their sources and writes them into the repository, where the scheduled runs
read them with git:

  close mode (after the US close; the evening and weekly reviews)
    feed/latest.json  for every stock on the list, every ticker in the price store (stocks that left the list,
                      the first order's stocks, SPY, OIL through BNO, SHEL-US, BP-US, IBIT, ETHA) and any ticker
                      named in feed/request.txt: the last ten completed sessions as open, high, low, close and
                      volume, a year and a quarter of daily bars for any ticker with fewer than 260 stored rows,
                      the 52-week high and low, and a check of every overlapping row against data/history.json;
                      the US Treasury's 2, 10 and 30-year yields (the same file the playbook names); Coinbase's
                      Bitcoin, Ether, Solana and XRP prices at the US close (the same candles the playbook names);
                      the front-month Brent, WTI, natural gas and gold futures as a fallback only; and, from 1.2
                      (26 Oct 2026), the UK, German, French, Italian and Japanese 10-year government bond yields for
                      the session, each with its source, date and time (`macro.intl_yields`).
    feed/latest.md    the same, for reading.
  live mode (during the US session; the 16:45 and 19:22 UK price refreshes)
    feed/live.json    the latest price, previous close, open, high, low and volume for the same tickers, the time
                      each was read, Coinbase's live Bitcoin and Ether prices, the futures and (from 1.2) the
                      live non-US 10-year yields.

Prices are Yahoo Finance's daily bars through the yfinance library, unadjusted for dividends (adjusted for splits,
like stockanalysis.com's history pages). London prices are in pence, as in the price store. The feed never
decides anything: the pipeline's `feed` command (version 7.7) checks every row again against the stored prices
before using it, and refuses a ticker whose rows disagree.

Only the standard library and the packages in scan/requirements.txt are used.
"""

import argparse
import json
import math
import os
import sys
import time
import traceback
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

FEED_VERSION = "1.2 (26 Oct 2026)"
NY = ZoneInfo("America/New_York")
UK = ZoneInfo("Europe/London")
UTC = timezone.utc
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) ft-game-feed/1.0 (private research; github.com/timzwang/ft-game)"}

ROWS_KEPT = 10                 # completed sessions given for every ticker
LONG_IF_STORED_BELOW = 200     # tickers with fewer stored rows also get the long series (about two years): the pipeline works
                               # a stock's averages out from stored prices once it has 200 closes
PANEL_LONG_BELOW = 480         # panel stocks with fewer stored closes also get it (the panel test wants two years)
HISTORY_DAYS = 800             # calendar days of daily bars downloaded (a little over two years)
US_CLOSED = {"2026-11-26"}     # Thanksgiving
US_EARLY_CLOSE = {"2026-11-27": (13, 0)}
LONDON_CLOSED = {"2026-12-25", "2026-12-28"}
UK_TICKERS = {"SHEL", "BP.", "BA."}    # London listings in the files (data doc, part F)
# Tickers in the files that are not the Yahoo symbol of the same listing.
SPECIAL = {"OIL": "BNO", "SHEL-US": "SHEL", "BP-US": "BP"}
FUTURES = {"brent": "BZ=F", "wti": "CL=F", "natgas": "NG=F", "gold": "GC=F"}
COINS = {"btc": "BTC-USD", "eth": "ETH-USD", "sol": "SOL-USD", "xrp": "XRP-USD"}
TREASURY = ("https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/"
            "{y}/all?type=daily_treasury_yield_curve&field_tdr_date_value={y}&page&_format=csv")
COINBASE_CANDLE = ("https://api.exchange.coinbase.com/products/{pair}/candles?granularity=3600"
                   "&start={start}&end={start}")
COINBASE_TICKER = "https://api.exchange.coinbase.com/products/{pair}/ticker"

# Non-US 10-year government bond yields (feed 1.2, 26 Oct 2026, playbook 6.14.1). Until then the evening review read
# them from tradingeconomics through a search, and from 22 Oct that page came back days old, so the stored figures were
# carried (26 Oct: none for any of the five). Sources, tried in this order; the first figure dated the session is used,
# and every source's figure is kept beside it so a disagreement can be seen:
#   - Japan only: the Ministry of Finance's daily JGB file (the official close; often a day behind when the run reads it).
#   - CNBC's quote service (Tradeweb benchmark yields), dated by the time of its last trade in the bond's own market.
#     On its first run (26 Oct, 22:57 UTC) it gave UK 5.352, Germany 3.370, France 4.903, Italy 4.500; two other pages
#     gave France 4.92 to 4.93 and Germany 3.37 for that day.
#   - CNBC's previous close, when its last trade already falls on the market's next weekday (Tokyo trades while the
#     evening review runs): that close is then the session's.
# stooq's daily files were tried and refuse GitHub's servers (26 Oct). A figure not dated the session is never used.
INTL_YIELDS = {"uk10y": {"cnbc": "UK10Y-GB", "zone": "Europe/London"},
               "de10y": {"cnbc": "DE10Y-DE", "zone": "Europe/Berlin"},
               "fr10y": {"cnbc": "FR10Y-FR", "zone": "Europe/Paris"},
               "it10y": {"cnbc": "IT10Y-IT", "zone": "Europe/Rome"},
               "jp10y": {"cnbc": "JP10Y-JP", "zone": "Asia/Tokyo", "mof": True}}
CNBC_QUOTES = ("https://quote.cnbc.com/quote-html-webservice/restQuote/symbolType/symbol?symbols={syms}"
               "&requestMethod=itv&noform=1&partnerId=2&fund=1&exthrs=1&output=json&events=1")
MOF_JGB = "https://www.mof.go.jp/english/policy/jgbs/reference/interest_rate/jgbcme.csv"
YIELD_DISAGREE = 0.10   # percentage points between two sources for the same session: shown, not refused

# Agreement with the stored prices (stockanalysis.com, lse.co.uk, Cboe), checked on every overlapping session. The
# check is there to catch the wrong instrument (a ticker mapped to another listing, pence against pounds, a split),
# not the small differences between vendors: on the first run (21 Oct 2026, 984 overlapping sessions) Yahoo's close
# matched the stored close to the cent in 973, the largest gap was 0.42% (one close-only row from September), and
# 837 of 858 opens were within 0.05%. Volume is reported only, never a reason to refuse a ticker.
TOL_CLOSE = 0.5      # percent, the same limit as the pipeline's `closes` command
TOL_OHL = 1.5        # percent, open, high and low

LOG = []


def log(msg):
    line = f"{datetime.now(UTC).strftime('%H:%M:%SZ')} {msg}"
    LOG.append(line)
    print(line, flush=True)


def rnd(x, n=4):
    if x is None:
        return None
    try:
        x = float(x)
    except (TypeError, ValueError):
        return None
    if math.isnan(x) or math.isinf(x):
        return None
    return round(x, n)


# ----------------------------------------------------------------- tickers

def market_of(ticker, markets):
    if ticker in SPECIAL or ticker.endswith("-US"):
        return "US"
    if ticker in markets:
        return markets[ticker]
    if ticker.endswith(".") or ticker in UK_TICKERS:
        return "UK"
    return "US"


def yahoo_symbol(ticker, market):
    if ticker in SPECIAL:
        return SPECIAL[ticker]
    if ticker.endswith("-US"):
        return ticker[:-3]
    if market == "UK":
        return ticker.rstrip(".").replace(".", "-") + ".L"
    return ticker.replace(".", "-")


def requested_tickers(path, last=20):
    """Tickers named in feed/request.txt on lines that start with 'tickers:' (case ignored), among the file's last
    `last` lines: US tickers as in the files, London tickers ending in '.L' (for example 'tickers: HAS EFX RR.L')."""
    out = {}
    if not os.path.exists(path):
        return out
    for line in open(path, encoding="utf-8").read().splitlines()[-last:]:
        low = line.strip().lower()
        if not low.startswith("tickers:"):
            continue
        for tok in line.split(":", 1)[1].replace(",", " ").split():
            tok = tok.strip().upper()
            if not tok:
                continue
            if tok.endswith(".L"):
                out[tok[:-2]] = "UK"
            else:
                out[tok] = "US"
    return out


def build_list(repo):
    """Every ticker the runs may need: the list, the price store, the request file. Returns {ticker: market}."""
    stocks = json.load(open(os.path.join(repo, "data", "stocks.json")))
    hist = json.load(open(os.path.join(repo, "data", "history.json")))
    ledger = json.load(open(os.path.join(repo, "data", "ledger.json")))
    markets = {}
    row = next((r for r in ledger if r.get("table") == "meta" and r.get("name") == "listing_market"), None)
    if row and row.get("text"):
        try:
            markets.update(json.loads(row["text"]))
        except ValueError:
            pass
    for s in stocks:
        if s.get("ticker") and s.get("market") in ("UK", "US"):
            markets[s["ticker"]] = s["market"]
    tickers = {}
    for s in stocks:
        t = s.get("ticker")
        if t and s.get("group") != "Cash":
            tickers[t] = market_of(t, markets)
    for r in hist:
        t = r.get("ticker")
        if t and t not in tickers:
            tickers[t] = market_of(t, markets)
    for t, m in requested_tickers(os.path.join(repo, "feed", "request.txt")).items():
        tickers.setdefault(t, m)
    tickers.setdefault("SPY", "US")
    stored = {}
    for r in hist:
        stored.setdefault(r["ticker"], {})[r["date"]] = r
    # The panel test's 30 stocks (fixed 15 Oct 2026): their closes live in data/panel.json, two years each.
    panel_closes = {}
    pp = os.path.join(repo, "data", "panel.json")
    if os.path.exists(pp):
        panel = json.load(open(pp))
        for m in panel.get("members") or []:
            t = m.get("ticker")
            if t:
                tickers.setdefault(t, "US")
                panel_closes[t] = {d: {"open": c, "high": c, "low": c, "close": c, "volume": None}
                                   for d, c in (panel.get("closes") or {}).get(t, [])}
    return tickers, stored, panel_closes


def wanted_tickers(repo):
    """The stocks a run will score: the list (data/stocks.json) and the tickers on 'tickers:' request lines."""
    out = set(requested_tickers(os.path.join(repo, "feed", "request.txt")))
    try:
        for s in json.load(open(os.path.join(repo, "data", "stocks.json"))):
            if s.get("ticker") and s.get("group") != "Cash":
                out.add(s["ticker"])
    except (OSError, ValueError):
        pass
    return out


def wants_long(t, stored, panel_closes, wanted=()):
    """Whether a ticker gets the long series (about two years of full daily rows).

    - A stock in the price store with fewer than 200 rows (the pipeline works averages out from 200 stored closes).
    - A stock not in the price store that the runs score (on the list or named on a 'tickers:' line), whether or not
      it is a panel member: the panel's closes live in data/panel.json, carry no open, high, low or volume, and never
      reach history.json, so they cannot stand in for a stored history. Until 1.1 (21 Oct 2026) a panel member with a
      full panel series got only ten rows when it was requested as a candidate (Analog Devices, 21 Oct).
    - Any other ticker not in the store and not in the panel.
    - A panel member with fewer than 480 panel closes (the panel test wants two years).
    """
    n_stored = len(stored.get(t, {}))
    if t in stored and n_stored < LONG_IF_STORED_BELOW:
        return True
    if t not in stored and (t in wanted or t not in panel_closes):
        return True
    return t in panel_closes and len(panel_closes[t]) < PANEL_LONG_BELOW


# ------------------------------------------------------------------ prices

def _frames(df, symbols):
    import pandas as pd
    out = {}
    if df is None or df.empty:
        return out
    cols = ["Open", "High", "Low", "Close", "Volume"]
    if isinstance(df.columns, pd.MultiIndex):
        top = set(df.columns.get_level_values(0))
        for s in symbols:
            if s in top:
                sub = df[s][[c for c in cols if c in df[s].columns]].dropna(subset=["Close"])
                if len(sub):
                    out[s] = sub
    elif len(symbols) == 1:
        sub = df[[c for c in cols if c in df.columns]].dropna(subset=["Close"])
        if len(sub):
            out[symbols[0]] = sub
    return out


def download(symbols, period, tz):
    """Daily bars, unadjusted for dividends, dated in the exchange's own zone. `period` is a yfinance period ("5d")
    or a number of calendar days back from today."""
    import pandas as pd
    import yfinance as yf
    span = ({"start": (date.today() - timedelta(days=period)).isoformat()} if isinstance(period, int) else {"period": period})
    data = {}
    for attempt in range(3):
        try:
            df = yf.download(symbols, interval="1d", auto_adjust=False, actions=False,
                             group_by="ticker", threads=True, progress=False, **span)
            data.update(_frames(df, symbols))
            break
        except Exception as e:  # noqa: BLE001
            log(f"yahoo: attempt {attempt + 1} failed ({type(e).__name__}: {e})")
            time.sleep(15 * (attempt + 1))
    for s in [s for s in symbols if s not in data]:
        try:
            df = yf.download(s, interval="1d", auto_adjust=False, actions=False, progress=False, **span)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            data.update(_frames(df, [s]))
        except Exception:  # noqa: BLE001
            pass
        time.sleep(0.3)
    for s, df in data.items():
        idx = pd.to_datetime(df.index)
        if idx.tz is not None:
            idx = idx.tz_convert(tz).tz_localize(None)
        df.index = (idx + pd.Timedelta(hours=12)).normalize()     # zone-aware midnight or naive UTC: both land on the day
        data[s] = df[~df.index.duplicated(keep="last")].sort_index()
    return data


def us_final(now_ny, last_bar):
    """The latest US session whose daily bar is final (16:15 New York, 13:15 on the early close)."""
    h, m = US_EARLY_CLOSE.get(now_ny.date().isoformat(), (16, 0))
    if last_bar == now_ny.date() and (now_ny.hour, now_ny.minute) < (h, m + 15):
        return False
    return True


def uk_final(now_uk, last_bar):
    return not (last_bar == now_uk.date() and (now_uk.hour, now_uk.minute) < (16, 45))


def consistent_range(row):
    """Yahoo's first bar after the close sometimes has its open or close outside its own high and low (21 Oct 2026:
    Charles River open 313.83 against a low of 315.825; UnitedHealth open 421.80 against a high of 421.47, which the
    later bar corrected to 421.80). The pipeline skips such a row, so the day goes unscored. The official open and
    close are prices that traded, so the range is widened to include them. Returns True when it changed the row."""
    o, h, lo, c = row.get("open"), row.get("high"), row.get("low"), row.get("close")
    if None in (h, lo):
        return False
    pts = [x for x in (o, c) if x is not None]
    new_h, new_lo = max([h] + pts), min([lo] + pts)
    if (new_h, new_lo) == (h, lo):
        return False
    row["high"], row["low"] = new_h, new_lo
    return True


def bar_rows(df, widened=None):
    rows = []
    for d, r in df.iterrows():
        row = {"date": d.strftime("%Y-%m-%d"), "open": rnd(r.get("Open")), "high": rnd(r.get("High")),
               "low": rnd(r.get("Low")), "close": rnd(r.get("Close")),
               "volume": (int(r["Volume"]) if r.get("Volume") is not None and not math.isnan(float(r["Volume"]))
                          and float(r["Volume"]) > 0 else None)}
        if consistent_range(row) and widened is not None:
            widened.append(row["date"])
        rows.append(row)
    return rows


def close_only(s):
    """A stored row that holds only a close: marked as such from pipeline 7.2 (open_obs false), or, before that, a
    row from a closes feed with open, high and low set to the close and no volume."""
    return s.get("open_obs") is False or (s.get("volume") is None and s.get("open") == s.get("high") == s.get("low") == s.get("close"))


def compare(rows, stored):
    """Each feed row against the stored row for the same session (close-only stored rows are compared on the close
    only). Returns the check block."""
    diffs = []
    for r in rows:
        s = stored.get(r["date"])
        if not s or not s.get("close") or not r.get("close"):
            continue
        d = {"date": r["date"], "close": rnd((r["close"] / s["close"] - 1) * 100, 3)}
        if not close_only(s) and s.get("open") and r.get("open"):
            for k in ("open", "high", "low"):
                if s.get(k) and r.get(k):
                    d[k] = rnd((r[k] / s[k] - 1) * 100, 3)
        if s.get("volume") and r.get("volume"):
            d["volume"] = rnd((r["volume"] / s["volume"] - 1) * 100, 1)
        diffs.append(d)
    worst = {k: max([abs(x[k]) for x in diffs if x.get(k) is not None] or [0.0]) for k in ("close", "open", "high", "low", "volume")}
    bad = [x["date"] for x in diffs if abs(x["close"]) > TOL_CLOSE
           or any(abs(x[k]) > TOL_OHL for k in ("open", "high", "low") if x.get(k) is not None)]
    status = "no overlap" if not diffs else ("mismatch" if bad else "agrees")
    return {"status": status, "sessions_compared": len(diffs), "max_abs_pct": worst, "mismatched_sessions": bad,
            "rows": diffs}


# ------------------------------------------------------------------- macro

def treasury_rows(year, n=6):
    import requests
    r = requests.get(TREASURY.format(y=year), headers=UA, timeout=30)
    r.raise_for_status()
    lines = [x for x in r.text.splitlines() if x.strip()]
    head = [h.strip().strip('"') for h in lines[0].split(",")]
    ix = {k: head.index(k) for k in ("Date", "2 Yr", "10 Yr", "30 Yr")}
    out = []
    for ln in lines[1:]:
        p = [x.strip().strip('"') for x in ln.split(",")]
        try:
            mm, dd, yy = p[ix["Date"]].split("/")
            d = f"{int(yy):04d}-{int(mm):02d}-{int(dd):02d}"
            out.append({"date": d, "us2y": float(p[ix["2 Yr"]]), "us10y": float(p[ix["10 Yr"]]),
                        "us30y": float(p[ix["30 Yr"]])})
        except (ValueError, IndexError):
            continue
    out.sort(key=lambda x: x["date"])
    return out[-n:]


def close_hour_utc(session):
    """The UTC hour that starts one hour before the US close on `session` (data doc part F: 19 to 30 Oct, 20 from
    2 Nov, 17 on 27 Nov)."""
    h, m = US_EARLY_CLOSE.get(session, (16, 0))
    close = datetime.combine(date.fromisoformat(session), datetime.min.time()).replace(hour=h, minute=m, tzinfo=NY)
    return (close.astimezone(UTC) - timedelta(hours=1)).strftime("%Y-%m-%dT%H:00:00Z")


def coin_closes(session):
    import requests
    start = close_hour_utc(session)
    out = {}
    for k, pair in COINS.items():
        try:
            r = requests.get(COINBASE_CANDLE.format(pair=pair, start=start), headers=UA, timeout=20)
            r.raise_for_status()
            rows = r.json()
            if isinstance(rows, list) and len(rows) == 1:
                out[k] = {"price": rnd(rows[0][4], 6), "candle_start_utc": start, "pair": pair}
            else:
                out[k] = {"price": None, "candle_start_utc": start, "pair": pair, "note": f"{len(rows)} candles returned"}
        except Exception as e:  # noqa: BLE001
            out[k] = {"price": None, "candle_start_utc": start, "pair": pair, "note": f"{type(e).__name__}: {e}"[:160]}
        time.sleep(0.4)
    return out


def coin_live():
    import requests
    out = {}
    for k in ("btc", "eth"):
        try:
            r = requests.get(COINBASE_TICKER.format(pair=COINS[k]), headers=UA, timeout=20)
            r.raise_for_status()
            j = r.json()
            out[k] = {"price": rnd(j.get("price"), 6), "time_utc": j.get("time")}
        except Exception as e:  # noqa: BLE001
            out[k] = {"price": None, "note": f"{type(e).__name__}: {e}"[:160]}
    return out


def _pct(x):
    """'4.567%' or 4.567 to 4.567; anything else to None."""
    if x is None:
        return None
    try:
        v = float(str(x).replace("%", "").replace(",", "").strip())
    except ValueError:
        return None
    return v if -5 < v < 30 else None


def parse_cnbc(payload):
    """CNBC's restQuote JSON to {symbol: {value, prev_close, time_utc}}."""
    q = (payload or {}).get("FormattedQuoteResult", {}).get("FormattedQuote") or []
    if isinstance(q, dict):
        q = [q]
    out = {}
    for x in q:
        sym = x.get("symbol")
        if not sym:
            continue
        t = x.get("last_time") or ""
        try:
            t_utc = datetime.fromisoformat(t.replace("+0000", "+00:00")).astimezone(UTC).isoformat(timespec="minutes")
        except ValueError:
            t_utc = None
        out[sym] = {"value": _pct(x.get("last")), "prev_close": _pct(x.get("previous_day_closing")), "time_utc": t_utc}
    return out


def parse_mof(text):
    """The Ministry of Finance's JGB file (two title lines, then 'Date,1Y,...,10Y,...') to a list of (date, 10-year),
    oldest first. Dates are written like 2026/10/26."""
    out, ix = [], None
    for ln in (text or "").splitlines():
        p = [x.strip() for x in ln.split(",")]
        if ix is None:
            if p and p[0].lower() == "date" and "10Y" in p:
                ix = p.index("10Y")
            continue
        try:
            y, m, d = (int(x) for x in p[0].replace("-", "/").split("/"))
            v = _pct(p[ix])
        except (ValueError, IndexError):
            continue
        if v is not None:
            out.append((f"{y:04d}-{m:02d}-{d:02d}", v))
    return sorted(out)


def _local_date(t_utc, zone):
    try:
        return datetime.fromisoformat(t_utc).astimezone(ZoneInfo(zone)).date().isoformat()
    except (TypeError, ValueError):
        return None


def next_weekday(d):
    x = date.fromisoformat(d) + timedelta(days=1)
    while x.weekday() >= 5:
        x += timedelta(days=1)
    return x.isoformat()


def choose_yields(session, cnbc, mof):
    """For each yield, every source's figure and the one used for the session. A CNBC figure counts as the session's
    when its last trade fell on that day in the bond's own market; its previous close counts when the last trade fell on
    the next weekday (a holiday in that market in between makes it not count); the MoF gives dated closes."""
    values, sources = {}, {}
    for k, spec in INTL_YIELDS.items():
        cands = []
        c = cnbc.get(spec["cnbc"]) or {}
        c_day = _local_date(c.get("time_utc"), spec["zone"])
        if c.get("value") is not None:
            cands.append({"source": "cnbc", "date": c_day, "value": c["value"], "time_utc": c.get("time_utc")})
        if c.get("prev_close") is not None and c_day and c_day == next_weekday(session):
            cands.append({"source": "cnbc previous close", "date": session, "value": c["prev_close"]})
        if spec.get("mof") and mof:
            d, v = mof[-1]
            cands.append({"source": "mof", "date": d, "value": v})
        order = ["mof", "cnbc", "cnbc previous close"]
        same = sorted([x for x in cands if x["date"] == session], key=lambda x: order.index(x["source"]))
        sources[k] = cands
        if same:
            use = dict(same[0])
            spread = max(x["value"] for x in same) - min(x["value"] for x in same)
            if len(same) > 1 and spread > YIELD_DISAGREE:
                use["disagree"] = ", ".join(f"{x['source']} {x['value']:.3f}" for x in same)
            values[k] = use
        else:
            latest = max(cands, key=lambda x: x["date"] or "") if cands else None
            values[k] = {"value": None, "note": f"no figure dated {session}" + (
                f"; latest {latest['source']} {latest['value']:.3f} on {latest['date']}" if latest else "; no source answered")}
    return values, sources


def fetch_intl_yields(session=None):
    """Reads the sources; returns (values, sources, errors). With no session (live mode) it gives CNBC's latest
    figures only."""
    import requests
    errors = {}
    cnbc = {}
    try:
        syms = "%7C".join(v["cnbc"] for v in INTL_YIELDS.values())
        r = requests.get(CNBC_QUOTES.format(syms=syms), headers=UA, timeout=20)
        r.raise_for_status()
        cnbc = parse_cnbc(r.json())
    except Exception as e:  # noqa: BLE001
        errors["cnbc"] = f"{type(e).__name__}: {e}"[:160]
    if session is None:
        return {k: {**(cnbc.get(v["cnbc"]) or {"value": None}), "source": "cnbc"} for k, v in INTL_YIELDS.items()}, {}, errors
    mof = []
    try:
        r = requests.get(MOF_JGB, headers=UA, timeout=20)
        r.raise_for_status()
        mof = parse_mof(r.content.decode("utf-8", "replace"))
        if not mof:
            raise ValueError("no rows parsed")
    except Exception as e:  # noqa: BLE001
        errors["mof"] = f"{type(e).__name__}: {e}"[:160]
    values, sources = choose_yields(session, cnbc, mof)
    return values, sources, errors


# -------------------------------------------------------------------- main

def write_json(path, obj):
    tmp = path + ".part"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=1, sort_keys=False)
        f.write("\n")
    os.replace(tmp, path)


def run_close(repo, out, force=False):
    import pandas as pd
    tickers, stored, panel_closes = build_list(repo)
    sym = {t: yahoo_symbol(t, m) for t, m in tickers.items()}
    by_mk = {"US": sorted({sym[t] for t, m in tickers.items() if m == "US"}),
             "UK": sorted({sym[t] for t, m in tickers.items() if m == "UK"})}
    log(f"tickers: {len(tickers)} ({len(by_mk['US'])} US symbols, {len(by_mk['UK'])} London; {len(panel_closes)} panel stocks)")
    data = {}
    data.update(download(by_mk["US"] + list(FUTURES.values()), HISTORY_DAYS, "America/New_York"))
    if by_mk["UK"]:
        data.update(download(by_mk["UK"] + ["^FTSE"], HISTORY_DAYS, "Europe/London"))
    if "SPY" not in data:
        raise RuntimeError("no SPY bars: cannot date the session")
    now_ny, now_uk = datetime.now(NY), datetime.now(UK)
    spy = data["SPY"]
    last = spy.index[-1].date()
    session_us = (spy.index[-1] if us_final(now_ny, last) else spy.index[-2]).strftime("%Y-%m-%d")
    session_uk = None
    if "^FTSE" in data:
        f = data["^FTSE"]
        session_uk = (f.index[-1] if uk_final(now_uk, f.index[-1].date()) else f.index[-2]).strftime("%Y-%m-%d")
    log(f"session: US {session_us}, London {session_uk}")
    prev = os.path.join(out, "latest.json")
    if not force and os.path.exists(prev):
        try:
            pm = json.load(open(prev)).get("meta") or {}
            if pm.get("session_us") == session_us and pm.get("session_uk") == session_uk:
                log("this session is already in latest.json: nothing to do")
                return 0
        except ValueError:
            pass

    result, missing, mismatched, stale, short, ranges = {}, [], [], [], [], []
    wanted = wanted_tickers(repo)
    for t, m in sorted(tickers.items()):
        s = sym[t]
        df = data.get(s)
        if df is None or df.empty:
            missing.append(t)
            continue
        cut = session_uk if m == "UK" else session_us
        if cut is None:
            missing.append(t)
            continue
        df = df[df.index <= pd.Timestamp(cut)]
        if df.empty:
            missing.append(t)
            continue
        wid = []
        rows = bar_rows(df, wid)
        if wid and wid[-1] >= rows[max(0, len(rows) - ROWS_KEPT)]["date"]:
            ranges.append(f"{t} {','.join(x for x in wid if x >= rows[max(0, len(rows) - ROWS_KEPT)]['date'])}")
        last_row = rows[-1]["date"]
        st = stored.get(t) or panel_closes.get(t) or {}
        check = compare(rows[-ROWS_KEPT - 15:], st)    # the last 25 sessions against the store (or the panel's closes)
        entry = {"yahoo": s, "market": m, "session": cut, "last_bar": last_row,
                 "complete": last_row == cut, "rows": rows[-ROWS_KEPT:],
                 "week52_high": rnd(max(r["high"] for r in rows[-252:] if r["high"] is not None)),
                 "week52_low": rnd(min(r["low"] for r in rows[-252:] if r["low"] is not None)),
                 "sessions_available": len(rows), "stored_rows": len(stored.get(t, {})), "check": check}
        if t in panel_closes:
            entry["panel_closes"] = len(panel_closes[t])
        if wants_long(t, stored, panel_closes, wanted):
            entry["long"] = rows
        if t in wanted and len(stored.get(t, {})) < LONG_IF_STORED_BELOW and len(entry.get("long") or entry["rows"]) < LONG_IF_STORED_BELOW:
            short.append(t)    # a list or requested stock that will still be short of 200 closes after this feed
        if last_row != cut:
            stale.append(t)
        if check["status"] == "mismatch":
            mismatched.append(t)
        result[t] = entry

    macro = {"treasury": [], "coins": {}, "futures": {}}
    try:
        macro["treasury"] = treasury_rows(int(session_us[:4]))
        log(f"treasury: {len(macro['treasury'])} rows, last {macro['treasury'][-1]['date'] if macro['treasury'] else 'none'}")
    except Exception as e:  # noqa: BLE001
        macro["treasury_error"] = f"{type(e).__name__}: {e}"[:200]
        log(f"treasury: FAILED ({macro['treasury_error']})")
    macro["coins"] = coin_closes(session_us)
    log("coins: " + ", ".join(f"{k} {v.get('price')}" for k, v in macro["coins"].items()))
    for k, s in FUTURES.items():
        df = data.get(s)
        if df is not None and not df.empty:
            df = df[df.index <= pd.Timestamp(session_us)]
            if not df.empty:
                macro["futures"][k] = {"symbol": s, "date": df.index[-1].strftime("%Y-%m-%d"), "close": rnd(df["Close"].iloc[-1])}
    try:
        vals, srcs, errs = fetch_intl_yields(session_us)
        macro["intl_yields"] = {"session": session_us, "values": vals, "sources": srcs, "errors": errs}
        log("non-US 10-year yields: " + ", ".join(f"{k} {v.get('value')} ({v.get('source', '-')})" for k, v in vals.items())
            + (f"; source errors: {', '.join(errs)}" if errs else ""))
    except Exception as e:  # noqa: BLE001     never let the yields stop the prices
        macro["intl_yields"] = {"session": session_us, "values": {}, "sources": {}, "errors": {"all": f"{type(e).__name__}: {e}"[:200]}}
        log(f"non-US 10-year yields: FAILED ({type(e).__name__}: {e})")
    meta = {"feed_version": FEED_VERSION, "mode": "close", "generated_utc": datetime.now(UTC).isoformat(timespec="seconds"),
            "session_us": session_us, "session_uk": session_uk, "tickers": len(result), "missing": missing,
            "stale": stale, "mismatched": mismatched, "short_history": short, "ranges_widened": ranges,
            "tolerances_pct": {"close": TOL_CLOSE, "open_high_low": TOL_OHL},
            "source": "Yahoo Finance daily bars through yfinance (auto_adjust off), checked against data/history.json; "
                      "US Treasury daily par yield curve CSV; Coinbase Exchange hourly candles; non-US 10-year yields from "
                      "CNBC's quote service and the Japanese Ministry of Finance"}
    write_json(os.path.join(out, "latest.json"), {"meta": meta, "tickers": result, "macro": macro})
    write_md(os.path.join(out, "latest.md"), meta, result, macro)
    log(f"written: {len(result)} tickers; missing {missing or 'none'}; stale {stale or 'none'}; mismatched {mismatched or 'none'}; "
        f"short of {LONG_IF_STORED_BELOW} sessions {short or 'none'}; ranges widened {ranges or 'none'}")
    return 0


def run_live(repo, out):
    tickers, stored, _panel = build_list(repo)
    tickers = {t: m for t, m in tickers.items() if t in stored or t == "SPY"}    # the list and the price store; not the panel
    sym = {t: yahoo_symbol(t, m) for t, m in tickers.items()}
    data = {}
    us = sorted({sym[t] for t, m in tickers.items() if m == "US"})
    uk = sorted({sym[t] for t, m in tickers.items() if m == "UK"})
    data.update(download(us + list(FUTURES.values()), "5d", "America/New_York"))
    if uk:
        data.update(download(uk, "5d", "Europe/London"))
    read_at = datetime.now(UTC)
    today_ny, today_uk = datetime.now(NY).date().isoformat(), datetime.now(UK).date().isoformat()
    quotes = {}
    for t, m in sorted(tickers.items()):
        df = data.get(sym[t])
        if df is None or len(df) < 2:
            continue
        want = today_uk if m == "UK" else today_ny
        last_d = df.index[-1].strftime("%Y-%m-%d")
        if last_d != want:
            continue                                   # no bar for today yet (holiday, or before the open)
        r, p = df.iloc[-1], df.iloc[-2]
        quotes[t] = {"price": rnd(r["Close"]), "prev_close": rnd(p["Close"]), "open": rnd(r["Open"]),
                     "high": rnd(r["High"]), "low": rnd(r["Low"]),
                     "volume": int(r["Volume"]) if not math.isnan(float(r["Volume"])) else None,
                     "bar_date": last_d, "prev_date": df.index[-2].strftime("%Y-%m-%d"), "yahoo": sym[t]}
    fut = {}
    for k, s in FUTURES.items():
        df = data.get(s)
        if df is not None and not df.empty:
            fut[k] = {"symbol": s, "price": rnd(df["Close"].iloc[-1]), "bar_date": df.index[-1].strftime("%Y-%m-%d")}
    meta = {"feed_version": FEED_VERSION, "mode": "live", "read_utc": read_at.isoformat(timespec="seconds"),
            "read_uk": read_at.astimezone(UK).strftime("%H:%M"), "quotes": len(quotes),
            "note": "Yahoo quotes can lag the market by up to about 15 minutes; read_utc is when the feed read them."}
    try:
        yl, _s, yerr = fetch_intl_yields(None)
    except Exception as e:  # noqa: BLE001
        yl, yerr = {}, {"all": f"{type(e).__name__}: {e}"[:160]}
    write_json(os.path.join(out, "live.json"), {"meta": meta, "quotes": quotes,
                                                 "macro_now": {"coins": coin_live(), "futures": fut,
                                                               "intl_yields": yl, "intl_yields_errors": yerr}})
    log(f"live: {len(quotes)} quotes read at {meta['read_uk']} UK")
    return 0


def fmt(x, d=2):
    return "" if x is None else f"{x:,.{d}f}"


def write_md(path, meta, result, macro):
    md = [f"# Price feed: US session {meta['session_us']}, London {meta['session_uk']}", "",
          f"Generated {meta['generated_utc']} UTC (feed version {meta['feed_version']}). {meta['tickers']} tickers. "
          "Every row is checked against the stored prices; the pipeline's `feed` command checks it again before use.", "",
          f"- Missing: {', '.join(meta['missing']) or 'none'}",
          f"- Last bar not the session: {', '.join(meta['stale']) or 'none'}",
          f"- Disagree with the stored prices (close beyond {TOL_CLOSE}% or open, high, low beyond {TOL_OHL}%): "
          f"{', '.join(meta['mismatched']) or 'none'}",
          f"- List or requested stocks still short of {LONG_IF_STORED_BELOW} sessions after this feed: "
          f"{', '.join(meta.get('short_history') or []) or 'none'}",
          f"- Bars whose high and low were widened to include their own open or close (last ten sessions): "
          f"{'; '.join(meta.get('ranges_widened') or []) or 'none'}", "",
          "| Ticker | Yahoo | Session | Open | High | Low | Close | Volume | Check | Max close gap | Max open gap |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for t, e in sorted(result.items()):
        r = e["rows"][-1]
        c = e["check"]
        md.append(f"| {t} | {e['yahoo']} | {r['date']} | {fmt(r['open'])} | {fmt(r['high'])} | {fmt(r['low'])} | {fmt(r['close'])} | "
                  f"{r['volume'] if r['volume'] is not None else ''} | {c['status']} ({c['sessions_compared']}) | "
                  f"{c['max_abs_pct']['close']:.3f}% | {c['max_abs_pct']['open']:.3f}% |")
    md += ["", "## Macro", "", "| Date | US 2y | US 10y | US 30y |", "|---|---|---|---|"]
    for r in macro.get("treasury") or []:
        md.append(f"| {r['date']} | {r['us2y']:.2f} | {r['us10y']:.2f} | {r['us30y']:.2f} |")
    if macro.get("treasury_error"):
        md.append(f"\nTreasury file not read: {macro['treasury_error']}")
    md += ["", "| Coin | Price at the hour before the US close | Candle (UTC) |", "|---|---|---|"]
    for k, v in (macro.get("coins") or {}).items():
        md.append(f"| {k} | {fmt(v.get('price'), 4)} | {v.get('candle_start_utc')} {v.get('note', '')} |")
    iy = macro.get("intl_yields") or {}
    md += ["", f"Non-US 10-year yields for {iy.get('session')} (the first figure dated the session; feed 1.2):", "",
           "| Yield | Value | Source | Date | Time (UTC) | Other sources | Note |", "|---|---|---|---|---|---|---|"]
    for k in INTL_YIELDS:
        v = (iy.get("values") or {}).get(k) or {}
        others = "; ".join(f"{x['source']} {x['value']:.3f} ({x['date']})" for x in (iy.get("sources") or {}).get(k, [])
                           if x["source"] != v.get("source"))
        md.append(f"| {k} | {fmt(v.get('value'), 3)} | {v.get('source', '')} | {v.get('date', '')} | {v.get('time_utc', '')} | "
                  f"{others} | {v.get('disagree', '') and 'sources disagree: ' + v['disagree']}{v.get('note', '')} |")
    if iy.get("errors"):
        md.append("\nSources that did not answer: " + "; ".join(f"{k}: {e}" for k, e in iy["errors"].items()))
    md += ["", "Futures (fallback only; the stored series are tradingeconomics figures):", ""]
    for k, v in (macro.get("futures") or {}).items():
        md.append(f"- {k}: {v['symbol']} {fmt(v['close'])} ({v['date']})")
    open(path, "w").write("\n".join(md) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", nargs="?", default="close", choices=["close", "live"])
    ap.add_argument("--repo", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--out", default=os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument("--force", action="store_true", help="write latest.json even if its session is already there")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    try:
        rc = run_close(a.repo, a.out, a.force) if a.mode == "close" else run_live(a.repo, a.out)
    except Exception:  # noqa: BLE001
        log("ERROR\n" + traceback.format_exc())
        rc = 1
    open(os.path.join(a.out, f"log-{a.mode}.txt"), "w").write("\n".join(LOG) + "\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
