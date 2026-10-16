#!/usr/bin/env python3
"""Broad scan for the FT Stock Picking Game (roadmap item 43).

Runs on GitHub Actions (see .github/workflows/scan.yml), where the open
internet is reachable. Scans about 900 US and London stocks once per US
session and writes two lists whose rules were fixed on 16 Oct 2026, before
any result was seen:

  Leaders  above the 50-day and 200-day averages, within 10% of the 52-week
           high, turnover above the floor; ranked by the 12-month return
           excluding the latest month, less the benchmark's; top 30.
  Events   opened 3% or more above the previous close, closed at or above
           the open and in the upper half of the day's range, on volume at
           least 1.5 times the previous 20 sessions' average, turnover above
           the floor; ranked by the day's return less the benchmark's.

The scan finds stocks; it never scores them. The evening review checks
every shortlisted name from the playbook's own sources (part F).

The top 10 of each list is recorded and settled five sessions later against
the benchmark, both close to close and from the next open (the return an
order could catch), in scan/record.csv.

Outputs (in --out, default scan/): latest.csv, latest.md, latest.json,
record.csv, universe.csv, log.txt.
"""

import argparse
import io
import json
import math
import os
import sys
import time
import traceback
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

RULES_VERSION = "1 (fixed 16 Oct 2026)"
NY = ZoneInfo("America/New_York")
UK = ZoneInfo("Europe/London")
BENCH = {"US": "SPY", "UK": "^FTSE"}
TURNOVER_FLOOR = {"US": 25e6, "UK": 3e6}  # median daily turnover, USD / GBP
LEADERS_TOP = 30
EVENTS_TOP = 30
RECORD_TOP = 10
SETTLE_AFTER = 5
UNIVERSE_MAX_AGE_DAYS = 7
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) ft-game-scan/1.0 (private research; github.com/timzwang/ft-game)"}

WIKI = {
    "SP500": "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
    "NDX": "https://en.wikipedia.org/wiki/Nasdaq-100",
    "FTSE100": "https://en.wikipedia.org/wiki/FTSE_100_Index",
    "FTSE250": "https://en.wikipedia.org/wiki/FTSE_250_Index",
}

LOG = []


def log(msg):
    line = f"{datetime.now(timezone.utc).strftime('%H:%M:%SZ')} {msg}"
    LOG.append(line)
    print(line, flush=True)


# ---------------------------------------------------------------- universe

def _pick(cols, *names):
    low = {str(c).lower(): c for c in cols}
    for n in names:
        for lc, c in low.items():
            if n in lc:
                return c
    return None


def _wiki_tables(url):
    import requests
    r = requests.get(url, headers=UA, timeout=30)
    r.raise_for_status()
    return pd.read_html(io.StringIO(r.text))


def us_symbol(s):
    return str(s).strip().upper().replace(".", "-")


def uk_symbol(s):
    s = str(s).strip().upper()
    if s.endswith(".L"):
        s = s[:-2]
    s = s.rstrip(".")
    return s.replace(".", "-") + ".L"


def fetch_index(key):
    tables = _wiki_tables(WIKI[key])
    best = None
    for t in tables:
        tcol = _pick(t.columns, "symbol", "ticker", "epic")
        if tcol is None:
            continue
        if best is None or len(t) > len(best[0]):
            best = (t, tcol)
    if best is None:
        heads = "; ".join(str(list(t.columns)[:6]) for t in tables[:12])
        raise RuntimeError(f"{key}: no table with a ticker column among {len(tables)} tables: {heads}")
    t, tcol = best
    ncol = _pick(t.columns, "security", "company", "name")
    scol = _pick(t.columns, "gics sector", "sector", "industry")
    market = "UK" if key.startswith("FTSE") else "US"
    rows = []
    for _, r in t.iterrows():
        raw = r[tcol]
        if not isinstance(raw, str) or not raw.strip():
            continue
        sym = uk_symbol(raw) if market == "UK" else us_symbol(raw)
        rows.append({
            "ticker": sym,
            "name": str(r[ncol]).strip() if ncol is not None else "",
            "sector": str(r[scol]).strip() if scol is not None else "",
            "market": market,
            "index": key,
        })
    return pd.DataFrame(rows)


def build_universe(path):
    """Rebuild the universe weekly; keep the old file if a source fails."""
    old = pd.read_csv(path) if os.path.exists(path) else None
    if old is not None and "built" in old.columns:
        built = datetime.fromisoformat(str(old["built"].iloc[0]))
        if datetime.now(timezone.utc) - built < timedelta(days=UNIVERSE_MAX_AGE_DAYS):
            log(f"universe: {len(old)} stocks, built {built:%Y-%m-%d}, kept")
            return old
    parts, failed = [], []
    expect = {"SP500": 480, "NDX": 95, "FTSE100": 95, "FTSE250": 230}
    for key in WIKI:
        try:
            df = fetch_index(key)
            if len(df) < expect[key]:
                raise RuntimeError(f"only {len(df)} rows")
            parts.append(df)
            log(f"universe: {key} {len(df)} rows")
        except Exception as e:  # noqa: BLE001
            failed.append(key)
            log(f"universe: {key} FAILED ({e})")
    if failed:
        if old is not None:
            log("universe: a source failed, keeping the previous file")
            return old
        if not parts:
            raise RuntimeError("no universe source worked and there is no previous file")
    uni = pd.concat(parts, ignore_index=True)
    # A stock in both the S&P 500 and the Nasdaq-100 keeps the S&P 500 row.
    order = {"SP500": 0, "NDX": 1, "FTSE100": 2, "FTSE250": 3}
    uni["_o"] = uni["index"].map(order)
    uni = uni.sort_values("_o").drop_duplicates("ticker").drop(columns="_o")
    # A partial build (a source failed and there was no previous file) is
    # dated in the past so that the next run tries again.
    uni["built"] = ("1970-01-01T00:00:00+00:00" if failed
                    else datetime.now(timezone.utc).isoformat(timespec="seconds"))
    uni = uni.sort_values(["market", "ticker"]).reset_index(drop=True)
    uni.to_csv(path, index=False)
    log(f"universe: rebuilt, {len(uni)} stocks ({(uni.market == 'US').sum()} US, {(uni.market == 'UK').sum()} UK)")
    return uni


# ------------------------------------------------------------------ prices

def _split_download(df, tickers):
    out = {}
    if df is None or df.empty:
        return out
    if isinstance(df.columns, pd.MultiIndex):
        lvl0 = set(df.columns.get_level_values(0))
        for t in tickers:
            if t not in lvl0:
                continue
            sub = df[t].copy()
            sub = sub[[c for c in ["Open", "High", "Low", "Close", "Volume"] if c in sub.columns]]
            sub = sub.dropna(subset=["Close"])
            if len(sub):
                out[t] = sub
    elif len(tickers) == 1:
        sub = df[[c for c in ["Open", "High", "Low", "Close", "Volume"] if c in df.columns]].dropna(subset=["Close"])
        if len(sub):
            out[tickers[0]] = sub
    return out


def download_yahoo(tickers, chunk=100):
    import yfinance as yf
    data = {}
    for i in range(0, len(tickers), chunk):
        part = tickers[i:i + chunk]
        for attempt in range(3):
            try:
                df = yf.download(part, period="15mo", interval="1d", auto_adjust=True,
                                 group_by="ticker", threads=True, progress=False)
                got = _split_download(df, part)
                data.update(got)
                break
            except Exception as e:  # noqa: BLE001
                log(f"yahoo: chunk {i // chunk + 1} attempt {attempt + 1} failed ({type(e).__name__}: {e})")
                time.sleep(20 * (attempt + 1))
        time.sleep(2)
    missing = [t for t in tickers if t not in data]
    if missing:
        log(f"yahoo: retrying {len(missing)} missing one by one")
        for t in missing[:150]:
            try:
                df = yf.download(t, period="15mo", interval="1d", auto_adjust=True, progress=False)
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
                got = _split_download(df, [t])
                data.update(got)
            except Exception:  # noqa: BLE001
                pass
            time.sleep(0.3)
    return data


def _stooq_symbol(t):
    if t == "^FTSE":
        return "^ukx"
    if t.endswith(".L"):
        return t[:-2].replace("-", ".").lower() + ".uk"
    return t.lower() + ".us"


def download_stooq(tickers, limit=200):
    import requests
    data = {}
    for t in tickers[:limit]:
        url = f"https://stooq.com/q/d/l/?s={_stooq_symbol(t)}&i=d"
        try:
            r = requests.get(url, headers=UA, timeout=20)
            if r.status_code != 200 or not r.text.startswith("Date"):
                continue
            df = pd.read_csv(io.StringIO(r.text), parse_dates=["Date"], index_col="Date")
            df = df.rename(columns=str.title)
            df = df[df.index >= df.index.max() - pd.Timedelta(days=460)]
            if len(df):
                data[t] = df[[c for c in ["Open", "High", "Low", "Close", "Volume"] if c in df.columns]]
        except Exception:  # noqa: BLE001
            pass
        time.sleep(0.5)
    return data


def get_prices(tickers):
    src = {}
    data = {}
    try:
        data = download_yahoo(tickers)
        for t in data:
            src[t] = "yahoo"
        log(f"yahoo: {len(data)} of {len(tickers)}")
    except Exception as e:  # noqa: BLE001
        log(f"yahoo: FAILED ({type(e).__name__}: {e})")
    missing = [t for t in tickers if t not in data]
    if missing:
        got = download_stooq(missing)
        for t in got:
            src[t] = "stooq"
        data.update(got)
        log(f"stooq: {len(got)} of {len(missing)} missing")
    for t, df in data.items():
        df.index = pd.to_datetime(df.index).tz_localize(None).normalize()
        data[t] = df[~df.index.duplicated(keep="last")].sort_index()
    return data, src


# ---------------------------------------------------------------- measures

def measures(df, bench, market):
    """Figures for one stock on its last bar. df and bench: OHLCV frames."""
    c = df["Close"]
    n = len(c)
    if n < 60:
        return None
    last_date = c.index[-1]
    bc = bench["Close"].reindex(c.index).ffill()
    o, h, l, v = (df[k].iloc[-1] for k in ["Open", "High", "Low", "Volume"])
    prev = c.iloc[-2]
    close = c.iloc[-1]
    vol = df["Volume"].astype(float)
    avg20v = vol.iloc[-21:-1].mean()
    scale = 0.01 if market == "UK" else 1.0  # London prices are in pence
    turnover = float((c.iloc[-20:] * vol.iloc[-20:]).median() * scale)

    def rel(k):
        if n <= k or pd.isna(bc.iloc[-1 - k]):
            return np.nan
        return (close / c.iloc[-1 - k] - 1) - (bc.iloc[-1] / bc.iloc[-1 - k] - 1)

    m = {
        "session": last_date.strftime("%Y-%m-%d"),
        "close": float(close),
        "chg_1d": float(close / prev - 1),
        "rel_1d": float(rel(1)),
        "gap": float(o / prev - 1) if o and not pd.isna(o) else np.nan,
        "close_loc": float((close - l) / (h - l)) if h > l else 1.0,
        "closed_above_open": bool(close >= o) if not pd.isna(o) else False,
        "vol_ratio": float(v / avg20v) if avg20v and v and not pd.isna(v) else np.nan,
        "ma50": float(c.iloc[-50:].mean()),
        "ma200": float(c.iloc[-200:].mean()) if n >= 200 else np.nan,
        "high_52w": float(df["High"].iloc[-252:].max()),
        "rel_20d": float(rel(20)),
        "turnover_med20": turnover,
        "sessions": n,
    }
    m["above_50"] = close > m["ma50"]
    m["above_200"] = (close > m["ma200"]) if n >= 200 else False
    m["from_high"] = close / m["high_52w"] - 1
    if n >= 253 and not pd.isna(bc.iloc[-253]):
        m["mom_12_1_rel"] = float((c.iloc[-22] / c.iloc[-253] - 1) - (bc.iloc[-22] / bc.iloc[-253] - 1))
    else:
        m["mom_12_1_rel"] = np.nan
    return m


def is_leader(m, market):
    return (m["sessions"] >= 253 and m["above_50"] and m["above_200"]
            and m["from_high"] >= -0.10 and not math.isnan(m["mom_12_1_rel"])
            and m["turnover_med20"] >= TURNOVER_FLOOR[market])


def is_event(m, market):
    return (not math.isnan(m["gap"]) and m["gap"] >= 0.03 and m["closed_above_open"]
            and m["close_loc"] >= 0.5 and not math.isnan(m["vol_ratio"]) and m["vol_ratio"] >= 1.5
            and m["turnover_med20"] >= TURNOVER_FLOOR[market])


# ------------------------------------------------------------------ record

RECORD_COLS = ["session", "list", "rank", "ticker", "market", "new", "close",
               "bench", "bench_close", "settled_on", "ret_5", "bench_5", "excess_5",
               "ret_5_open", "bench_5_open", "excess_5_open"]


def settle(record, data):
    for i, r in record.iterrows():
        if isinstance(r.get("settled_on"), str) and r["settled_on"]:
            continue
        df, bdf = data.get(r["ticker"]), data.get(r["bench"])
        if df is None or bdf is None:
            continue
        d = pd.Timestamp(r["session"])
        if d not in df.index or d not in bdf.index:
            continue
        p, bp = df.index.get_loc(d), bdf.index.get_loc(d)
        if p + SETTLE_AFTER >= len(df) or bp + SETTLE_AFTER >= len(bdf):
            continue
        end = df.index[p + SETTLE_AFTER]
        if end not in bdf.index:
            continue
        be = bdf.index.get_loc(end)
        c0, c5, o1 = df["Close"].iloc[p], df["Close"].iloc[p + SETTLE_AFTER], df["Open"].iloc[p + 1]
        b0, b5, bo1 = bdf["Close"].iloc[bp], bdf["Close"].iloc[be], bdf["Open"].iloc[bp + 1]
        record.at[i, "settled_on"] = end.strftime("%Y-%m-%d")
        record.at[i, "ret_5"] = c5 / c0 - 1
        record.at[i, "bench_5"] = b5 / b0 - 1
        record.at[i, "excess_5"] = record.at[i, "ret_5"] - record.at[i, "bench_5"]
        record.at[i, "ret_5_open"] = c5 / o1 - 1
        record.at[i, "bench_5_open"] = b5 / bo1 - 1
        record.at[i, "excess_5_open"] = record.at[i, "ret_5_open"] - record.at[i, "bench_5_open"]
    return record


def record_summary(record):
    lines = []
    s = record[record["settled_on"].astype(str).str.len() > 4] if len(record) else record
    for lst in ["leaders", "events"]:
        for label, sub in [("all rows", s[s["list"] == lst]),
                           ("first appearances", s[(s["list"] == lst) & (s["new"].astype(str) == "True")])]:
            n = len(sub)
            if n == 0:
                lines.append(f"| {lst} | {label} | 0 | | | |")
                continue
            ex = sub["excess_5"].astype(float)
            exo = sub["excess_5_open"].astype(float)
            lines.append(f"| {lst} | {label} | {n} | {(ex > 0).mean():.0%} | {ex.mean() * 100:+.2f} | {exo.mean() * 100:+.2f} |")
    return lines


# -------------------------------------------------------------------- main

def us_session_final(spy):
    """The latest US session whose daily bar is final, as a date string."""
    now = datetime.now(NY)
    last = spy.index[-1].date()
    if last == now.date() and (now.hour, now.minute) < (16, 5):
        return spy.index[-2].strftime("%Y-%m-%d"), True
    return last.strftime("%Y-%m-%d"), False


def uk_session_final(ftse):
    """The latest London session whose bar is final (after 16:45 UK)."""
    now = datetime.now(UK)
    last = ftse.index[-1].date()
    if last == now.date() and (now.hour, now.minute) < (16, 45):
        return ftse.index[-2].strftime("%Y-%m-%d"), True
    return last.strftime("%Y-%m-%d"), False


def fmt_pct(x, d=1):
    return "" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x * 100:+.{d}f}%"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument("--force", action="store_true", help="scan even if this session is done")
    ap.add_argument("--offline", help="folder of <ticker>.csv files to use instead of downloading (tests)")
    a = ap.parse_args()
    out = a.out
    os.makedirs(out, exist_ok=True)
    meta_path = os.path.join(out, "latest.json")
    prev_meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {}

    skipped = False
    try:
        if a.offline:
            uni = pd.read_csv(os.path.join(a.offline, "universe.csv"))
            data, src = {}, {}
            for t in list(uni["ticker"]) + list(BENCH.values()):
                f = os.path.join(a.offline, t.replace("^", "_") + ".csv")
                if os.path.exists(f):
                    data[t] = pd.read_csv(f, parse_dates=["Date"], index_col="Date")
                    src[t] = "offline"
        else:
            uni = build_universe(os.path.join(out, "universe.csv"))
            # Cheap check first: is there a new final session to scan?
            bench_data, _ = get_prices(list(BENCH.values()))
            if "SPY" not in bench_data:
                raise RuntimeError("no SPY prices: cannot date the session")
            session, waiting = us_session_final(bench_data["SPY"])
            if not a.force and prev_meta.get("session_us") == session:
                log(f"session {session} already scanned{' (today not final yet)' if waiting else ''}: nothing to do")
                skipped = True
                return 0
            tickers = list(uni["ticker"])
            data, src = get_prices(tickers)
            data.update(bench_data)
            for t in bench_data:
                src[t] = "yahoo"

        spy = data["SPY"]
        session, waiting = us_session_final(spy) if not a.offline else (spy.index[-1].strftime("%Y-%m-%d"), False)
        # Drop an unfinished bar for today (US) so every figure is on final bars.
        if waiting:
            cut = pd.Timestamp(session)
            for t in list(data):
                if t != "^FTSE" and not str(t).endswith(".L"):
                    data[t] = data[t][data[t].index <= cut]
        session_uk = None
        if "^FTSE" in data:
            if a.offline:
                session_uk = data["^FTSE"].index[-1].strftime("%Y-%m-%d")
            else:
                session_uk, uk_waiting = uk_session_final(data["^FTSE"])
                if uk_waiting:
                    cut = pd.Timestamp(session_uk)
                    for t in list(data):
                        if t == "^FTSE" or str(t).endswith(".L"):
                            data[t] = data[t][data[t].index <= cut]

        rows, stale, missing = [], [], []
        info = uni.set_index("ticker")
        for t in uni["ticker"]:
            df = data.get(t)
            if df is None:
                missing.append(t)
                continue
            market = info.at[t, "market"]
            bt = BENCH[market]
            if bt not in data:
                continue
            want = session if market == "US" else session_uk
            if df.index[-1].strftime("%Y-%m-%d") != want:
                stale.append(t)
                continue
            try:
                m = measures(df, data[bt], market)
            except Exception as e:  # noqa: BLE001
                log(f"measure failed for {t}: {e}")
                continue
            if m is None:
                continue
            m.update({"ticker": t, "name": info.at[t, "name"], "sector": info.at[t, "sector"],
                      "market": market, "index": info.at[t, "index"], "source": src.get(t, "")})
            m["leader"] = is_leader(m, market)
            m["event"] = is_event(m, market)
            rows.append(m)
        allm = pd.DataFrame(rows)
        log(f"measured {len(allm)}; missing {len(missing)}; stale or not traded {len(stale)}")
        if len(allm) < 0.8 * len(uni):
            log(f"WARNING: only {len(allm)} of {len(uni)} stocks measured")

        leaders = allm[allm["leader"]].sort_values("mom_12_1_rel", ascending=False).head(LEADERS_TOP).copy()
        leaders["list"], leaders["rank"] = "leaders", range(1, len(leaders) + 1)
        events = allm[allm["event"]].sort_values("rel_1d", ascending=False).head(EVENTS_TOP).copy()
        events["list"], events["rank"] = "events", range(1, len(events) + 1)
        latest = pd.concat([leaders, events], ignore_index=True)

        cols = ["list", "rank", "ticker", "name", "market", "index", "sector", "session", "close",
                "chg_1d", "rel_1d", "gap", "close_loc", "vol_ratio", "above_50", "above_200",
                "from_high", "mom_12_1_rel", "rel_20d", "turnover_med20", "source"]
        latest = latest[cols] if len(latest) else pd.DataFrame(columns=cols)
        latest.to_csv(os.path.join(out, "latest.csv"), index=False, float_format="%.6g")

        # Record: top 10 of each list, once per session.
        rpath = os.path.join(out, "record.csv")
        record = pd.read_csv(rpath, dtype=str) if os.path.exists(rpath) else pd.DataFrame(columns=RECORD_COLS)
        for c in RECORD_COLS:
            if c not in record.columns:
                record[c] = ""
        record = record[RECORD_COLS].fillna("").astype(object)
        if not ((record["session"] == session).any()):
            prev_sessions = sorted(set(record["session"]))
            prev = prev_sessions[-1] if prev_sessions else None
            prev_top = {(r["list"], r["ticker"]) for _, r in record[record["session"] == prev].iterrows()} if prev else set()
            add = []
            for _, r in latest[latest["rank"].astype(int) <= RECORD_TOP].iterrows():
                bt = BENCH[r["market"]]
                add.append({"session": r["session"], "list": r["list"], "rank": r["rank"], "ticker": r["ticker"],
                            "market": r["market"], "new": (r["list"], r["ticker"]) not in prev_top,
                            "close": r["close"], "bench": bt,
                            "bench_close": float(data[bt]["Close"].loc[pd.Timestamp(r["session"])]),
                            "settled_on": ""})
            if add:
                record = pd.concat([record, pd.DataFrame(add).astype(str)], ignore_index=True)
        record = settle(record, data)
        record.to_csv(rpath, index=False)

        meta = {
            "rules_version": RULES_VERSION,
            "session_us": session,
            "session_uk": session_uk,
            "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "universe": int(len(uni)),
            "measured": int(len(allm)),
            "missing": missing,
            "stale": stale,
            "leaders": int(len(leaders)),
            "events": int(len(events)),
            "sources": {k: int(v) for k, v in pd.Series(list(src.values())).value_counts().items()},
        }
        json.dump(meta, open(meta_path, "w"), indent=1)

        md = [f"# Broad scan: US session {session}" + (f", London {session_uk}" if session_uk else ""),
              "",
              f"Generated {meta['generated_utc']} UTC. Rules version {RULES_VERSION}; the rules are in `scan/README.md`. "
              f"{len(allm)} of {len(uni)} stocks measured ({len(missing)} without prices, {len(stale)} not traded or stale). "
              "These lists only point at stocks: every figure used in a decision is fetched again from the playbook's sources.",
              "", f"## Events ({len(events)})", "",
              "| # | Stock | Name | Mkt | Day | vs index | Gap | Close in range | Volume x | Above 50d |",
              "|---|---|---|---|---|---|---|---|---|---|"]
        for _, r in events.iterrows():
            md.append(f"| {r['rank']} | {r['ticker']} | {r['name']} | {r['market']} | {fmt_pct(r['chg_1d'])} | {fmt_pct(r['rel_1d'])} | "
                      f"{fmt_pct(r['gap'])} | {r['close_loc']:.0%} | {r['vol_ratio']:.1f} | {'yes' if r['above_50'] else 'no'} |")
        md += ["", f"## Leaders ({len(leaders)})", "",
               "| # | Stock | Name | Mkt | 12-1 month vs index | 20 days vs index | From 52w high | Day |",
               "|---|---|---|---|---|---|---|---|"]
        for _, r in leaders.iterrows():
            md.append(f"| {r['rank']} | {r['ticker']} | {r['name']} | {r['market']} | {fmt_pct(r['mom_12_1_rel'])} | "
                      f"{fmt_pct(r['rel_20d'])} | {fmt_pct(r['from_high'])} | {fmt_pct(r['chg_1d'])} |")
        md += ["", "## Record (top 10 of each list, settled after five sessions)", "",
               "Excess is the stock's return less its index (S&P 500 through SPY, or the FTSE 100). "
               "\"From next open\" is the return an order entered that evening could have caught.", "",
               "| List | Which rows | Settled | Beat index | Mean excess, close to close (pts) | Mean excess from next open (pts) |",
               "|---|---|---|---|---|---|"]
        md += record_summary(record)
        md += ["", f"Open rows waiting to settle: {int((record['settled_on'].astype(str).str.len() < 5).sum())}."]
        open(os.path.join(out, "latest.md"), "w").write("\n".join(md) + "\n")
        log(f"session {session}: {len(events)} events, {len(leaders)} leaders written")
        return 0
    except Exception:  # noqa: BLE001
        log("ERROR\n" + traceback.format_exc())
        return 1
    finally:
        if not skipped:
            open(os.path.join(out, "log.txt"), "w").write("\n".join(LOG) + "\n")


if __name__ == "__main__":
    sys.exit(main())
