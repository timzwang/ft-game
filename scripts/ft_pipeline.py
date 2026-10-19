#!/usr/bin/env python3
"""ft_pipeline.py: one tested pipeline for the FT Stock Picking Game. Version 7.5 (prepared 19 Oct 2026, not deployed).

Version 7.5 (prepared by Claude on 19 Oct 2026 after Tim's review brief, priority A; needs Tim's approval to deploy)
prices a change that fills on a day that is not a US session. The game's one such day is Thu 26 Nov 2026: London
trades, the US is shut. An order entered before that morning's cut-off fills its London legs at the 26 Nov London open:
  - the performance log and the STANDSTILL test price a buy or sale at the stock's own open on its fill date when that
    date is not a benchmark session and the stock traded then (fill_days, fill_row); a US leg given the same date has
    no 26 Nov row and fills at the 27 Nov open, as before. In 7.4 every leg was priced at the 27 Nov open;
  - a change filling on such a date gets its STANDSTILL change row (7.4 left it out);
  - a corrected row on such a date recalculates the following session;
  - the session list is still the benchmark's: 26 and 27 Nov are one performance line, measured from the 25 Nov close;
  - with every fill on a benchmark session, as in every change to date, every figure is identical to version 7.4.

Version 7.4 (19 Oct 2026, approved by Tim after ChatGPT's follow-up review) records what each order change is expected
to add before it fills, so the STANDSTILL test can later say whether the expectation was right:
  - "order_expected" in today.json (and order.json for `reorder`): {"pts": expected points over the five sessions from
    the fill, the new order held fixed against the order before it held fixed (the same measure as a STANDSTILL change
    row), "thesis": why, "invalidation": what would show it wrong}. Stored as an "expect" row (forecast, text, plan);
  - an expectation can be restated until the change fills; after that it is locked and a new one is refused, so the
    forecast is never adjusted after the fact. A change with no expectation gets a WARNING;
  - STANDSTILL change rows carry the expectation (forecast) and, once complete, actual minus expected (surprise);
    EXPECTED BENEFIT sums them up in `run` and `report`;
  - with no order_expected given every figure is identical to version 7.3.

Version 7.3 (19 Oct 2026, approved by Tim after ChatGPT's repository review of 18 Oct) fixes settlement and the calendar:
  - confidence ratings settle over one window of five benchmark sessions starting at the fill date, and only with the
    stock's own row on the fill date (with a traded open) and on the window's last date; a missing or estimated row
    waits, and after 15 sessions the rating settles as "n/a" with the reason in `unit` (before, the first five rows the
    stock happened to have were used, so a missing day shifted the stock's window away from the index's);
  - shadow ratings need the stock's close on the exact end date; a missing one waits, then "n/a" (before, an earlier
    close could be used under the end date's label);
  - an FT reading already stored takes fields given later for it (`top2_return_pct`, `players`, `note`); before, the
    repeat was dropped;
  - US calendar: 26 Nov 2026 is not a US session and 27 Nov closes at 13:00 New York (18:00 UK), for the next-session
    date, the sessions-ahead count and RECONCILE's "read before the close" test;
  - a stored row marked as having no traded open keeps that mark when it is given back, and a change of mark alone
    counts as a correction; market_closed entries are kept in the ledger (a "meta" row) so a later rebuild still
    knows the market was shut;
  - results budget: reports dated 27 to 30 Oct 2026 are judged against 1.0 points instead of 0.6 (agreed by Tim on
    19 Oct for the October results cluster); the budgets in force are written to a "meta" row for the page;
  - with complete prices every figure is identical to version 7.2.

Version 7.2 (18 Oct 2026, approved by Tim after ChatGPT's challenge of the audit verification) changes data integrity only:
  - open provenance: a price row given without an open stores the close as its open, marked open_obs = false, and is
    never used as a fill price (before, any row with a volume counted as having a traded open);
  - performance: a session is recorded only when every stock held or traded that day is priced and every buy or sale
    has a traded open or a stated fill price; otherwise it and every later session wait (PERFORMANCE INCOMPLETE) and are
    added by the next run that has the rows. A market that was shut goes under market_closed in today.json
    ([{"ticker": ..., "date": ...}]) and the holding counts as unchanged. Before, the stock was skipped with a warning;
  - drift: a reporter whose next-session open never arrives settles after 15 sessions as "n/a" (close-basis figure
    kept in cum_pct), so it no longer counts as a win or loss in the calibration;
  - with complete prices every figure is identical to version 7.1.

Version 7.1 (18 Oct 2026, approved by Tim after the second audit review) changes only the STANDSTILL test:
  - week rows: the standstill is now the order in force at the close of the session BEFORE the week, priced from
    the week's first session, so a change that fills on a Monday (a weekend rebuild) is judged too; before, the
    standstill was the order after Monday's fill, which left those changes out by construction;
  - inception rows: the first order, never changed, held from the first fill to the latest session, "as entered"
    (with its cash) and "fully invested" (the same stocks scaled to 100%), against the actual estimate over the same
    sessions; priced up to the last session with every price, never filled with a guess;
  - STANDSTILL NEEDS and the template also name the stocks of the first order that are no longer on the list.

Version 7 adds, at Tim's request after the outside audit of 17 Oct 2026:
  - drift trades settled from the next session's open (the price an order can actually get), with the old
    reaction-close figure kept beside it (cum_pct, spx_cum_pct) for continuity;
  - STANDSTILL: every order change judged against keeping the order before it, both held fixed for up to five
    sessions from the change's fill, and each week's changes judged against the order in force at the week's
    first session ("standstill" rows in the ledger, rebuilt every run);
  - RESULTS TOTAL: the weight x implied move of every holding reporting inside the next five and ten sessions, added up;
  - RECONCILE: each value Tim reads off the FT site set beside the estimate for that session, flagged when it was read
    before the US close;
  - JUDGEMENT TEST: whether the 40 judgement points (catalyst, revisions) add anything to the 60 price and session
    points, from the shadow ratings (which now store both parts);
  - the template names stocks sold in the last five sessions that are no longer on the list, whose rows the
    standstill test needs under extra_history.

Commands
  python3 ft_pipeline.py run     --stocks stocks.json --ledger ledger.json --history history.json --macro macro.json --today today.json --out OUTDIR
  python3 ft_pipeline.py refresh --stocks stocks.json --quotes quotes.json [--ledger ledger.json] --out OUTDIR
  python3 ft_pipeline.py reorder --stocks stocks.json --ledger ledger.json --order order.json --out OUTDIR
  python3 ft_pipeline.py report  --ledger ledger.json [--since 2026-10-05]
  python3 ft_pipeline.py template --stocks stocks.json [--ledger ledger.json] [--history history.json] --out today.json
  python3 ft_pipeline.py closes  --history history.json --today today.json --ticker MSFT --first F --last L --closes "c1,c2,..." [--panel panel.json]
  python3 ft_pipeline.py panel   --panel panel.json [--history history.json]          (or --init members.json --out panel.json, once)

`run` and `template` also take --panel panel.json. The panel is 30 stocks fixed on 15 Oct 2026 by a rule that does not
look at how they have done (part E of the rules doc). Their closes live in panel.json, not in history.json, so the page
stays light. `closes --panel panel.json` sends a panel stock's feed to "panel_history" in today.json; `run` stores it and
tests the price-only points: on every fifth session counted from the day the panel was fixed, it ranks the panel by
points and by the next five sessions' return against the index, and averages that rank correlation over the dates,
separately before and after the day the panel was fixed. The result goes to the ledger as "calib" rows (kinds
panel-summary, panel-part, panel-band) and is printed under PANEL TEST.

`run` also takes "drift": a list of the day's reporters for the earnings-drift scan, one entry each:
 {"date": reaction session, "name", "ticker", "reported": "15 Oct, before US open", "eps_actual", "eps_est", "rev_actual",
  "rev_est" (the same units for each pair), "guidance": "raised|reaffirmed|lowered|none", "prev_close", "open", "high",
  "low", "close", "volume", "avg_vol_20d", "ma50", "ma200", "implied_pct", "note"}
It runs six tests (beat, raised, reaction, held, volume, trend), logs a "drift" row with the verdict (enter, watch or
fail) and settles it five sessions later against the index. A reporter not on the list keeps its stored prices until
then; the DRIFT WAITING line names those whose prices have to be supplied (one-year feed or history page).

`closes` adds a long run of daily closes from a price feed to today.json. A feed gives the closes as one line, in
order, with the date (YYYY-MM-DD) or the timestamp (seconds or milliseconds) of its first and last record. The command
lines them up with the benchmark's stored sessions between those two dates, refuses the lot if the count differs or if
any close disagrees by more than 0.5% with one already stored for that stock, and appends close-only rows for the
days the store does not have to that stock's `history` in today.json (or to `extra_history` for a ticker that is not
a stock on the list). Either order works: if the first date is later than the last, the list is read as newest first.

`template` writes a today.json skeleton from the last stocks.json: every stock with its ticker, theme, status, note,
link, the current order with weights and ratings, and yesterday's averages, 52-week range, target and judgement points
as starting values. Fill in the dates, the new history rows and fresh figures, and change whatever the review changes.

`run` also keeps a store of government bond yields and commodity prices (macro.json), works out simple and
exponential moving averages from stored closes for any stock with 200 or more of them, makes a day-ahead call
(the chance the next session closes up, from similar past days), logs a shadow rating for every scored stock and
checks past ratings against what happened.

`run` also tracks crypto. Bitcoin, Ether, Solana and XRP prices at the US close are stored beside the yields and
commodities. Two US-listed funds that hold nothing but the coin, IBIT (Bitcoin) and ETHA (Ether), are stored as price
histories because they trade in stock-market hours, so their daily moves line up with every stock's. From them the run
reads Bitcoin's trend and works out, for every stock, the move that has gone with a 1% move in Bitcoin and in Ether.
A stock whose theme is "Crypto", or whose daily moves have a correlation of 0.5 or more with either fund over 60 or
more sessions, is marked crypto-linked and carries a flag that names Bitcoin's trend. A watchlist stock whose note
starts "Crypto tracker:" is left out of the ROTATE OUT line: it stays on the list whatever it scores.

`run` (evening review) merges new price rows into the history store, calculates indicators and a
score out of 100 for every stock, checks the order against the game's rules, estimates the
portfolio's weighted return for each new session, resolves confidence ratings whose five-day window
has closed, writes risk and scenario tables, and produces stocks.json, ledger.json, history.json and macro.json
for the watchlist page. `refresh` (afternoon) only updates prices and the weighted move so far.

A position's effect on the portfolio is its weight times its return. Every portfolio figure here is
a sum of weight x return, never an average of returns.

today.json for `run` (null or omit anything unknown):
{
 "date": "2026-10-09",                 last completed session the data refers to
 "next_session": "2026-10-12",         the next trading day (the day the call is for); defaults to the next weekday
 "macro": {"date": "2026-10-09", "oil_proxy": "OIL", "values": {"us2y","us10y","us30y","uk10y","de10y","fr10y","it10y","jp10y","brent","wti","natgas","gold",
                                                                              "btc","eth","sol","xrp"}},
                                       closing yields in percent, commodity prices, and coin prices in dollars at the US close;
                                       leave out or null what was not published
 "macro_history": [{"date","series","value"}],     optional backfill of the same series
 "daycall": {"bull": "...", "bear": "...", "adjust": 0, "port_adjust": 0, "reason": "..."},
                                       the two written cases and an optional move of up to 5 points either way to the model's figure
 "extra_history": {"OIL": [rows], "SHEL-US": [rows], "IBIT": [rows], "ETHA": [rows]},
                                       price rows for tickers that are not stocks on the list: the oil series, any
                                       US-listed line named as a stock's "trend_ticker", and the Bitcoin and Ether funds
 "prices_as_of": "Fri 9 Oct close", "order_for": "Mon 12 Oct open", "effective": "2026-10-12",
 "regime": "mixed", "regime_label": "Mixed, fragile",
 "benchmark": {"ticker": "SPY", "change_52w_pct": 16.85, "history": [{"date","open","high","low","close","volume"}]},
 "order": [{"name": "Exxon Mobil", "weight": 15, "confidence": 61, "effective": null}],   cash is the remainder; give
                                       "effective" only for a stock that fills on a different day from the rest, and
                                       "fill_price" only when the game filled it at a price other than that day's open
 "order_reason": "why the order changed, one or two sentences",
 "order_expected": {"pts": 0.2, "thesis": "...", "invalidation": "..."},   version 7.4, with every change of order: the
                                       points the new order is expected to add over the five sessions from its fill
                                       against keeping the order before it (both held fixed, as STANDSTILL measures it),
                                       why, and what would show it wrong. Locked once the change has filled
 "stocks": [{"name","ticker","market":"US|UK","currency":"USD|GBX","theme","status","note","link",
             "quote": {"price","prev_close","open","high","low","volume","week52_high","week52_low","target","next_results"},
             "stats": {"ma50","ma200","rsi","change_52w_pct","avg_vol_20d","trend_price","trend_ticker"},
                                       published figures are only used while the stock (or its trend_ticker) has
                                       fewer than 200 stored closes; after that they are worked out here
             "added": "2026-10-08",    the day the stock joined the list
             "history": [{"date","open","high","low","close","volume"}],
             "catalyst_pts","catalyst_note","revisions_pts","revisions_note"}],
 "events": [{"date","time_uk","name","stock","kind","confirmed","implied_pct","text","plan","last_order","forecast","previous","actual","surprise"}],
 "revisions": [{"date","stock","bank","action","text"}],
 "alerts": [{"date","time_uk","stock","text"}],
 "scenarios": [{"name": "Ceasefire", "shocks": {"Energy": -5, "Defence": -3, "AI and chips": 2, "Other": 0}}],
                                       theme names exactly as the stocks use them; supplying the list replaces the stored one,
                                       so give every scenario; with none supplied the stored ones are rebuilt on today's weights.
                                       A "Bitcoin" entry is not a theme: it is an assumed move in Bitcoin, applied to every
                                       crypto-linked holding through its measured link, on top of the theme moves
                                       ({"name": "Bitcoin falls 15%", "shocks": {"Bitcoin": -15, "Other": 0}})
 "results_budget": 0.6,                optional: the points of the portfolio allowed per results report (default 0.6);
                                       reports inside RESULTS_BUDGET_WINDOWS (27 to 30 Oct 2026: 1.0) use the higher figure
 "market_closed": [{"ticker","date"}], optional: a market that was shut that day (kept in the ledger from version 7.3)
 "reported": {"date","time_uk","value","rank","players","top2_return_pct","note"},
 "postmortems": [{"name","text","lesson"}],
 "fixes": [{"name": "Shell", "old_effective": "2026-10-12", "new_effective": "2026-10-09", "fill_price": 3795.5}]
                                       correct a fill date and, optionally, the fill price (same dates to change only the price)
}
In "quote", price, open, high, low and volume describe the session named by "date"; the day's move is measured from
the stored close of the session before whenever the store has it. Keys that start with an underscore are ignored.
Events are kept between runs: a new event updates one with the same date and name (fields left out are kept), a new results date for a
stock replaces that stock's future results date, and {"date","name","remove": true} deletes one. Scenarios are
replaced only when supplied. Revisions and alerts are added to a running log.

order.json for `reorder` (a morning change to the order, between evening runs; every stock must already be in stocks.json):
{"effective": "2026-10-12", "entered": "2026-10-12", "order_for": "Mon 12 Oct open", "order_reason": "why",
 "order_expected": {"pts": 0.2, "thesis": "...", "invalidation": "..."},
 "order": [{"name": "Exxon Mobil", "weight": 15, "confidence": 60}]}

quotes.json for `refresh`:
{"date": "2026-10-12", "prices_as_of": "Mon 12 Oct, 16:45 UK", "quotes": {"XOM": {"price","prev_close","open"}},
 "alerts": [{"time_uk": "16:45", "stock": "TSMC", "text": "..."}],      optional; with --ledger they are added to the log
 "macro_now": {"as_of": "07:30 UK", "values": {"us10y": 5.26, "uk10y": 5.45, "brent": 105.1, "btc": 84100}},   optional live
                                       readings; with a Bitcoin reading the output gives the move that has gone with it
                                       for every crypto-linked stock
 "daycall": {"date": "2026-10-12", "adjust": -3, "port_adjust": 0, "reason": "..."}}   optional morning revision, up to 5 points
"quotes" may be empty when only the macro readings or the day call are being updated.
"""
import json
import math
import os
import sys

PIPELINE_VERSION = "7.5"

# Version 7.3: the US calendar for the rest of the game (NYSE and Nasdaq), and the results budget windows Tim agreed.
US_CLOSED = {"2026-11-26"}                        # Thanksgiving: US markets shut (London trades)
US_EARLY_CLOSE_NY = {"2026-11-27": "13:00"}       # the day after Thanksgiving, the game's last day: 13:00 New York
RESULTS_BUDGET_WINDOWS = [                        # (first report date, last report date, points, why)
    ("2026-10-27", "2026-10-30", 1.0, "October results cluster: Tim agreed 1.0 points per report on 19 Oct"),
]
SETTLE_TIMEOUT = 15                               # sessions after which an unsettled rating with missing rows is "n/a"


def results_budget_for(date, default=0.6):
    """The points allowed per results report dated `date`: the default (0.6, or what part D's stance sets) unless the
    date falls in an agreed window, whose budget then applies if it is higher."""
    out = default
    for lo, hi, pts, _why in RESULTS_BUDGET_WINDOWS:
        if lo <= (date or "") <= hi:
            out = max(out, pts)
    return out

LEDGER_KEYS = ["id", "table", "date", "time_uk", "effective", "name", "ticker", "stock", "kind", "bank", "action", "theme",
               "weight", "from_w", "to_w", "score", "confidence", "ret_pct", "spx_ret_pct", "beat", "contrib_pts",
               "value_est", "value_reported", "day_pct", "cum_pct", "spx_cum_pct", "rank", "players", "percentile",
               "implied_pct", "impact_pct", "vol_pct", "risk_share_pct", "value", "days", "confirmed", "window_end",
               "plan", "last_order", "lesson", "text",
               "chg_1d", "chg_5d", "chg_20d", "unit", "live", "live_chg", "forecast", "previous", "actual", "surprise",
               "adj_eve", "adj_morn"]
STOCK_KEYS = ["name", "ticker", "market", "group", "theme", "weight", "confidence", "currency", "price", "day_chg",
              "day_pct", "gap_pct", "from_open_pct", "five_day_pct", "month_pct", "contrib_pts", "score", "trend_pts",
              "short_pts", "catalyst_pts", "revisions_pts", "vs_20d_pct", "vs_50d_pct", "off_high_pct", "rsi",
              "atr_pct", "weight_cap_pct", "risk_share_pct", "flags", "spark", "next_results", "target", "upside_pct",
              "status", "note", "link", "live_from", "order_for", "regime", "prices_as_of", "scores_as_of",
              "today_est_pct", "week52_high", "week52_low", "ma50", "ma200", "change_52w_pct", "avg_vol_20d",
              "trend_price", "catalyst_note", "revisions_note", "fill_price",
              "tier", "added", "ma10", "ma20", "ma100", "ema10", "ema20", "ema50", "ema200", "vs_200d_pct", "ema_stack",
              "cross", "ma_source", "trend_ticker",
              "btc_beta", "btc_corr", "btc_net", "eth_beta", "eth_corr", "crypto_days", "crypto_link"]
WARN = []


def warn(msg):
    if msg not in WARN:
        WARN.append(msg)


def num(x):
    try:
        if x is None or x == "":
            return None
        v = float(x)
        return None if (v != v or v in (float("inf"), float("-inf"))) else v
    except (TypeError, ValueError):
        return None


def pct(a, b):
    if a is None or b is None or b == 0:
        return None
    return (a / b - 1.0) * 100.0


def r2(v, n=2):
    return None if v is None else round(v, n)


def load(path, default):
    if path and os.path.exists(path):
        return json.load(open(path))
    return default


def lrow(table, **kw):
    row = {k: None for k in LEDGER_KEYS}
    row["table"] = table
    for k, v in kw.items():
        if k not in row:
            raise KeyError("unknown ledger field " + k)
        row[k] = v
    return row


def band(value, steps, default=0):
    for threshold, points in steps:
        if value >= threshold:
            return points
    return default


# ---------------------------------------------------------------- history store
def merge_history(hist, ticker, rows):
    """hist: dict (ticker, date) -> row. New rows replace old ones for the same day.
    Returns the dates whose row is new or whose stored open or close changed by more than 0.01%."""
    changed = []
    for r in rows or []:
        d = str(r.get("date") or "")[:10]
        o, h, l, c = num(r.get("open")), num(r.get("high")), num(r.get("low")), num(r.get("close"))
        v = num(r.get("volume"))
        if len(d) != 10 or c is None or c <= 0:
            warn(f"{ticker} {d}: row skipped (no date or close)")
            continue
        imputed = o is None or r.get("open_obs") is False   # no open supplied, or a stored row given back still marked
        if o is None:
            o = c
        if h is None:
            h = max(o, c)
        if l is None:
            l = min(o, c)
        if h < l or not (l * 0.995 <= c <= h * 1.005) or not (l * 0.995 <= o <= h * 1.005):
            warn(f"{ticker} {d}: row skipped (open/high/low/close inconsistent: {o}, {h}, {l}, {c})")
            continue
        old = hist.get((ticker, d))
        if (old is None or abs(old["close"] / c - 1) > 1e-4 or abs(old["open"] / o - 1) > 1e-4
                or (old.get("open_obs") is False) != imputed):
            changed.append(d)             # new for that day, or corrected (a change of open provenance alone counts)
        row = {"ticker": ticker, "date": d, "open": o, "high": h, "low": l, "close": c, "volume": v}
        if imputed:
            row["open_obs"] = False
        hist[(ticker, d)] = row
    return changed


_SERIES = {}


def series(hist, ticker):
    key = (id(hist), ticker, len(hist))
    if key in _SERIES:
        return _SERIES[key]
    rows = sorted((r for (t, _), r in hist.items() if t == ticker), key=lambda r: r["date"])
    for a, b in zip(rows, rows[1:]):
        ch = pct(b["close"], a["close"])
        if ch is not None and abs(ch) > 35:
            warn(f"{ticker} {b['date']}: close moved {ch:.1f}% in a day; check for a typo or a split")
    _SERIES[key] = rows
    return rows


def sma(vals, n):
    return sum(vals[-n:]) / n if len(vals) >= n else None


def atr_pct(rows, n=14):
    if len(rows) < n + 1:
        return None
    trs = []
    for prev, cur in zip(rows[-n - 1:-1], rows[-n:]):
        trs.append(max(cur["high"] - cur["low"], abs(cur["high"] - prev["close"]), abs(cur["low"] - prev["close"])))
    return (sum(trs) / n) / rows[-1]["close"] * 100.0


def rsi_wilder(closes, n=14):
    """Wilder's RSI from stored closes. Needs n+1 closes; closer to published figures with more history."""
    if len(closes) < n + 1:
        return None
    ch = [b - a for a, b in zip(closes, closes[1:])]
    gain = sum(max(c, 0.0) for c in ch[:n]) / n
    loss = sum(max(-c, 0.0) for c in ch[:n]) / n
    for c in ch[n:]:
        gain = (gain * (n - 1) + max(c, 0.0)) / n
        loss = (loss * (n - 1) + max(-c, 0.0)) / n
    if loss == 0:
        return 100.0
    return 100.0 - 100.0 / (1.0 + gain / loss)


def ret_n(closes, n):
    return pct(closes[-1], closes[-1 - n]) if len(closes) > n else None


def daily_returns(rows):
    return {b["date"]: b["close"] / a["close"] - 1.0 for a, b in zip(rows, rows[1:])}


# ---------------------------------------------------------------- scoring
def score_stock(s, rows, bench_rows, bench_52w, regime, trend_rows=None, date=None):
    q, st = s.get("quote") or {}, s.get("stats") or {}
    gaps, flags = [], []
    last = rows[-1] if rows else {}
    prev_row = rows[-2] if len(rows) > 1 else {}
    price = num(q.get("price")) or last.get("close")
    if date and last.get("date") == date and prev_row.get("close"):
        prev = prev_row["close"]                    # the stored close of the session before, as the contribution log uses
    else:
        prev = num(q.get("prev_close")) or prev_row.get("close")
    opn = num(q.get("open")) or last.get("open")
    high = num(q.get("high")) or last.get("high")
    low = num(q.get("low")) or last.get("low")
    vol = num(q.get("volume")) or last.get("volume")
    closes = [r["close"] for r in rows]
    vols = [r["volume"] for r in rows if r.get("volume")]
    ma20 = sma(closes, 20)
    trows = trend_rows if trend_rows else rows          # a UK stock can take its trend from its US-listed line
    tcl = [r["close"] for r in trows]
    ind = indicators(trows)
    inhouse = len(tcl) >= 200
    hi52 = num(q.get("week52_high"))
    if inhouse:                                          # a year of stored closes: work the averages out here
        ma50, ma200, rsi = ind["ma50"], ind["ma200"], rsi_wilder(tcl)
        tprice = tcl[-1] if trend_rows else (price or tcl[-1])
        chg52 = pct(tcl[-1], tcl[-min(252, len(tcl))])       # a year back, or as far back as the store goes (200 sessions or more)
        if hi52 is None and not trend_rows:
            hi52 = max(closes[-252:])
        ma_source = "stored prices"
    else:
        ma50 = num(st.get("ma50"))
        tprice = num(st.get("trend_price")) or price
        if ma50 is None and num(st.get("trend_price")) is None:
            ma50 = sma(closes, 50)
        ma200, rsi = num(st.get("ma200")), num(st.get("rsi"))
        chg52 = num(st.get("change_52w_pct"))
        ma_source = "published page" if (ma50 is not None or ma200 is not None) else "not available"
    avgvol = (sum(vols[-21:-1]) / 20 if len(vols) >= 21 else None) or num(st.get("avg_vol_20d"))
    if bench_52w is None and len(bench_rows) >= 252:
        bench_52w = pct(bench_rows[-1]["close"], bench_rows[-252]["close"])

    if price is not None and high is not None and low is not None and not (low * 0.995 <= price <= high * 1.005):
        warn(f"{s['name']}: price outside the day's range")
    if price is not None and hi52 is not None and price > hi52:
        hi52 = price
    if tprice is not None and ma50 is not None and not (0.5 <= tprice / ma50 <= 2.0):
        warn(f"{s['name']}: 50-day average looks wrong for this price (check currency)")
        ma50 = None
    if rsi is not None and not (0 <= rsi <= 100):
        warn(f"{s['name']}: RSI out of range")
        rsi = None
    rsi_from_history = False
    if rsi is None:
        rsi = rsi_wilder(closes)
        rsi_from_history = rsi is not None and not inhouse

    vs20 = pct(price, ma20)
    vs50, vs200 = pct(tprice, ma50), pct(tprice, ma200)
    off_high = pct(price, hi52)
    day_pct, gap_pct, from_open = pct(price, prev), pct(opn, prev), pct(price, opn)
    five, month = ret_n(closes, 5), ret_n(closes, 21)
    bcl = [r["close"] for r in bench_rows]
    b5 = ret_n(bcl, 5)
    n2 = min(42, len(closes) - 1, len(bcl) - 1)      # up to two months, on whatever history both have
    two_m = ret_n(closes, n2) if n2 >= 21 else None
    b2m = ret_n(bcl, n2) if n2 >= 21 else None
    rs5 = five - b5 if (five is not None and b5 is not None) else None
    rs2m = two_m - b2m if (two_m is not None and b2m is not None) else None
    rs52 = chg52 - bench_52w if (chg52 is not None and bench_52w is not None) else None
    range_pos = (price - low) / (high - low) if (price is not None and high is not None and low is not None and high > low) else None
    vol_ratio = vol / avgvol if (vol and avgvol) else None
    atr = atr_pct(rows)

    p = {}
    if vs50 is None:
        p["vs_50d"] = 6; gaps.append("50-day average")
    elif vs50 < -5: p["vs_50d"] = 0
    elif vs50 < 0: p["vs_50d"] = 3
    elif vs50 < 2: p["vs_50d"] = 8
    elif vs50 <= 15: p["vs_50d"] = 12
    elif vs50 <= 25: p["vs_50d"] = 8
    else: p["vs_50d"] = 4
    if ma50 is None or ma200 is None or tprice is None:
        p["structure"] = 4; gaps.append("200-day average")
    else:
        p["structure"] = (5 if ma50 > ma200 else 0) + (3 if tprice > ma200 else 0)
    if off_high is None:
        p["near_high"] = 5; gaps.append("52-week high")
    else:
        p["near_high"] = band(off_high, [(-3, 10), (-8, 7), (-15, 4), (-25, 2)])
    if rs52 is None:
        p["rs_52w"] = 2; gaps.append("52-week change")
    else:
        p["rs_52w"] = band(rs52, [(30, 4), (10, 3), (0, 1)])
    if rs2m is None:
        p["rs_2m"] = 1; gaps.append("two-month return")
    else:
        p["rs_2m"] = band(rs2m, [(5, 2), (0, 1)])
    if rsi is None:
        p["rsi"] = 2; gaps.append("RSI")
    elif rsi > 80: p["rsi"] = 0
    elif rsi >= 70: p["rsi"] = 2
    elif rsi >= 50: p["rsi"] = 4
    elif rsi >= 40: p["rsi"] = 2
    else: p["rsi"] = 0
    trend = p["vs_50d"] + p["structure"] + p["near_high"] + p["rs_52w"] + p["rs_2m"] + p["rsi"]

    if rs5 is None:
        p["rs_5d"] = 4; gaps.append("5-day return")
    else:
        p["rs_5d"] = band(rs5, [(3, 8), (1, 6), (0, 4), (-2, 2)])
    if from_open is None or range_pos is None:
        p["session"] = 3; gaps.append("open, high or low")
    else:
        p["session"] = (3 if from_open > 0 else 0) + (3 if range_pos >= 0.5 else 0)
    if day_pct is None or vol_ratio is None:
        p["volume"] = 3; gaps.append("volume")
    elif day_pct > 0:
        p["volume"] = 6 if vol_ratio >= 1.3 else 4 if vol_ratio >= 0.8 else 2
    else:
        p["volume"] = 0 if vol_ratio >= 1.3 else 2
    short = p["rs_5d"] + p["session"] + p["volume"]

    cat, rev = num(s.get("catalyst_pts")), num(s.get("revisions_pts"))
    if cat is None:
        cat = 6; gaps.append("catalyst not rated")
    if rev is None:
        rev = 8; gaps.append("revisions not rated")
    cat, rev = max(0, min(20, cat)), max(0, min(20, rev))
    score = int(round(trend + short + cat + rev))

    if vs50 is not None and vs50 < 0: flags.append("below 50-day average")
    if ma50 is not None and ma200 is not None and ma50 < ma200: flags.append("downtrend: 50-day below 200-day")
    if vs50 is not None and vs50 > 15: flags.append("extended: more than 15% above 50-day")
    if rsi is not None and rsi > 75: flags.append("overbought: RSI above 75")
    if rsi is not None and rsi < 35: flags.append("oversold: RSI below 35")
    if day_pct is not None and vol_ratio is not None and day_pct < 0 and vol_ratio >= 1.3: flags.append("heavy-volume down day")
    if gap_pct is not None and from_open is not None and gap_pct > 1 and from_open < 0: flags.append("faded gap")
    if off_high is not None and off_high >= -0.5: flags.append("at 52-week high")
    if ind["cross"]: flags.append(ind["cross"])
    if rsi_from_history: gaps.append("RSI worked out from stored prices, not a published figure")

    conf = 50 + 0.35 * (score - 40)   # a score of 40 is treated as a coin flip; an unvalidated starting assumption
    if regime == "risk-off":
        conf -= 3
    conf = int(round(max(40, min(68, conf))))
    cap = int(max(5, min(20, round(30.0 / atr / 5.0) * 5))) if atr else None
    target = num(q.get("target"))
    return {
        "price": price, "day_chg": (price - prev) if (price is not None and prev is not None) else None,
        "day_pct": day_pct, "gap_pct": gap_pct, "from_open_pct": from_open, "five_day_pct": five, "month_pct": month,
        "score": score, "confidence_anchor": conf, "trend_pts": trend, "short_pts": short, "catalyst_pts": cat,
        "revisions_pts": rev, "parts": p, "vs_20d_pct": vs20, "vs_50d_pct": vs50, "vs_200d_pct": vs200,
        "off_high_pct": off_high, "rsi": rsi, "atr_pct": atr, "weight_cap_pct": cap, "rs_5d_pp": rs5, "rs_2m_pp": rs2m,
        "rs_52w_pp": rs52, "vol_ratio": vol_ratio, "range_pos": range_pos, "flags": flags, "data_gaps": gaps,
        "spark": "|".join(f"{c:.2f}" for c in closes[-20:]), "target": target, "upside_pct": pct(target, price),
        "ma50": ma50, "ma200": ma200, "ma_source": ma_source, "change_52w_pct": chg52, "avg_vol_20d": avgvol,
        "trend_price": tprice if (trend_rows or num(st.get("trend_price")) is not None) else None,
        "ma10": ind["ma10"] if not trend_rows else None, "ma20": ma20, "ma100": ind["ma100"] if inhouse else None,
        "ema10": ind["ema10"] if inhouse else None, "ema20": ind["ema20"] if inhouse else None,
        "ema50": ind["ema50"] if inhouse else None, "ema200": ind["ema200"] if inhouse else None,
        "ema_stack": ind["ema_stack"] if inhouse else "", "cross": ind["cross"] if inhouse else "",
        "week52_high": hi52, "closes_stored": len(tcl),
    }


# ---------------------------------------------------------------- order and weights
def check_order(order):
    errs = []
    names = [o["name"] for o in order]
    if len(set(names)) != len(names):
        errs.append("a stock appears twice in the order")
    ws = [num(o.get("weight")) or 0 for o in order]
    if len([w for w in ws if w > 0]) < 5:
        errs.append("fewer than 5 stocks")
    if len(ws) > 20:
        errs.append("more than 20 stocks")
    for o, w in zip(order, ws):
        if w and not (5 <= w <= 25):
            errs.append(f"{o['name']} weight {w} is outside 5 to 25")
    cash = 100 - sum(ws)
    if cash < -1e-9:
        errs.append(f"weights total {sum(ws)}, above 100")
    if cash > 25 + 1e-9:
        errs.append(f"cash would be {cash}, above the 25 maximum")
    return errs, round(cash, 4)


def live_weights(ledger, date):
    """Weight of each name on a session date: the latest position row whose effective date is on or before it."""
    out = {}
    for r in ledger:
        if r["table"] == "position" and r["effective"] and r["effective"] <= date:
            cur = out.get(r["name"])
            if cur is None or r["effective"] >= cur[0]:
                out[r["name"]] = (r["effective"], num(r["weight"]) or 0.0, r["ticker"])
    return {n: (w, t) for n, (e, w, t) in out.items() if w > 0}


def position_start(ledger, name, date):
    """Effective date of the current unbroken holding of `name` as of `date`."""
    rows = sorted((r for r in ledger if r["table"] == "position" and r["name"] == name and r["effective"] <= date),
                  key=lambda r: r["effective"])
    start = None
    for r in rows:
        if (num(r["weight"]) or 0) > 0:
            start = start or r["effective"]
        else:
            start = None
    return start


def apply_order(ledger, order, eff, entered, reason, tickers, scores):
    """Record the difference between the order and the weights already logged for its effective date."""
    new = {o["name"]: num(o["weight"]) or 0.0 for o in order}
    pending = {}
    for r in ledger:                                          # fills logged for a date after this order's
        if r["table"] == "position" and r["effective"] > eff:
            pending[r["name"]] = max(pending.get(r["name"], ""), r["effective"])
    eff_of = {o["name"]: (o.get("effective") or pending.get(o["name"]) or eff) for o in order}
    for n, e_ in pending.items():
        eff_of.setdefault(n, e_)
    cur = {}
    for e_ in sorted(set(eff_of.values()) | {eff}):          # each name is compared at its own fill date
        for n, (w, t) in live_weights(ledger, e_).items():
            if eff_of.get(n, eff) == e_:
                cur[n] = w
    for n in sorted(set(cur) | set(new)):
        if abs(cur.get(n, 0.0) - new.get(n, 0.0)) <= 1e-9:
            continue
        o = next((x for x in order if x["name"] == n), {})
        e = eff_of.get(n, eff)
        tick = tickers.get(n) or next((r["ticker"] for r in ledger if r["table"] == "position" and r["name"] == n), None)
        earlier = sorted((r for r in ledger if r["table"] == "position" and r["name"] == n and r["effective"] < e),
                         key=lambda r: r["effective"])
        held_before = bool(earlier) and (num(earlier[-1]["weight"]) or 0) > 0
        ledger = [r for r in ledger if not (r["table"] == "position" and r["name"] == n and r["effective"] == e)]   # superseded before it filled
        ledger.append(lrow("position", effective=e, name=n, ticker=tick, weight=new.get(n, 0.0), value=num(o.get("fill_price"))))
        ledger.append(lrow("trade", date=entered, effective=e, name=n, ticker=tick,
                           from_w=cur.get(n, 0.0), to_w=new.get(n, 0.0), text=reason))
        if cur.get(n, 0.0) == 0 and new.get(n, 0.0) > 0 and not held_before:
            ledger.append(lrow("confidence", date=entered, effective=e, name=n, ticker=tick,
                               score=scores.get(n), confidence=num(o.get("confidence"))))
        if new.get(n, 0.0) == 0:      # a position cancelled before it ever filled has no rating to resolve
            ledger = [r for r in ledger if not (r["table"] == "confidence" and r["name"] == n and r["effective"] == e
                                                and r["beat"] in (None, ""))]
    return ledger


def record_expectation(ledger, exp, eff, entered, changed, started):
    """Version 7.4: store the expected benefit of the change filling at `eff` as an "expect" row. `changed`: this run
    logged new trades for `eff`. `started`: the change has already filled, so its five-session window has begun and
    the expectation is locked (a first one given now would be hindsight and is refused)."""
    exp = exp or {}
    pts = num(exp.get("pts"))
    old = next((r for r in ledger if r["table"] == "expect" and r["effective"] == eff), None)
    if pts is None:
        if changed and old is None:
            warn(f"the order changes at the open of {eff} but no expected benefit was given (order_expected.pts); "
                 "it can be added until the change fills, never after")
        elif changed:
            warn(f"the order for {eff} changed again: the expected benefit given on {old['date']} "
                 f"({num(old['forecast']):+.2f} points) still stands unless order_expected is given again")
        return ledger
    if not any(r["table"] == "trade" and r["effective"] == eff for r in ledger):
        warn(f"order_expected was given but the order for {eff} does not change anything: not recorded")
        return ledger
    if started:
        if old is None:
            warn(f"the change at {eff} has already filled: an expected benefit given now would be hindsight, so it is not recorded")
        elif abs((num(old["forecast"]) or 0.0) - pts) > 1e-9:
            warn(f"the expected benefit for the change at {eff} is locked since it filled: kept {num(old['forecast']):+.2f} "
                 f"points (given on {old['date']}), not {pts:+.2f}")
        return ledger
    ledger = [r for r in ledger if r is not old]
    ledger.append(lrow("expect", date=entered, effective=eff, name=f"Change for {eff}", forecast=r2(pts, 3), days=5,
                       text=str(exp.get("thesis") or ""), plan=str(exp.get("invalidation") or "")))
    return ledger


def expectation_lines(ledger):
    """Version 7.4: the EXPECTED BENEFIT summary, from the STANDSTILL change rows that carry an expectation."""
    recorded = [r for r in ledger if r["table"] == "expect"]
    if not recorded:
        return []
    rows = sorted((r for r in ledger if r["table"] == "standstill" and r["kind"] == "change" and r["forecast"] is not None),
                  key=lambda r: r["date"])
    done = [r for r in rows if r["confirmed"] == "complete" and r["value"] is not None]
    out = [f"EXPECTED BENEFIT: {len(recorded)} change(s) with an expectation, {len(done)} settled over five sessions"]
    if done:
        exp_t, act_t = sum(num(r["forecast"]) for r in done), sum(r["value"] for r in done)
        right = sum(1 for r in done if (r["value"] > 0) == (num(r["forecast"]) > 0))
        out[0] += f": expected {exp_t:+.3f} points in all, actual {act_t:+.3f}; the right direction in {right} of {len(done)}"
    for r in rows[-5:]:
        act = "not priced" if r["value"] is None else f"{r['value']:+.3f}"
        out.append(f"    {r['name'][:26].ljust(27)} expected {num(r['forecast']):+.3f}, actual {act} ({r['confirmed']})"
                   + (f", actual minus expected {r['surprise']:+.3f}" if r["surprise"] is not None else ""))
    waiting = sorted(r["effective"] for r in recorded if not any(x["effective"] == r["effective"] for x in rows))
    if waiting:
        out.append("    waiting to fill: " + ", ".join(f"Change for {w}" for w in waiting))
    return out


# ---------------------------------------------------------------- performance
INCOMPLETE = []


def fill_days(ledger, dprev, d):
    """Version 7.5: name -> the effective date of the latest position row taking effect after `dprev` and on or before
    the benchmark session `d`. It differs from `d` only when a change filled on a day that is not a benchmark session:
    in this game, a London leg filling on 26 Nov 2026, when London trades and the US is shut."""
    out = {}
    for r in ledger:
        if r["table"] == "position" and r["effective"] and (dprev or "") < r["effective"] <= d:
            if r["effective"] > out.get(r["name"], ""):
                out[r["name"]] = r["effective"]
    return out


def fill_row(hist, tick, fd, d, cur):
    """Version 7.5: the row whose open a buy or sale filled at, and its date. The stock's own row on the fill day `fd`
    when that is not the session `d` and the stock traded then with a recorded open (a London stock on 26 Nov);
    otherwise the session's own row `cur`, exactly as before (a US stock ordered for 26 Nov fills at the 27 Nov open)."""
    if fd and fd != d and tick:
        row = hist.get((tick, fd))
        if row and real_open(row):
            return row, fd
    return cur, d


def update_performance(ledger, hist, bench, today_date, closed=None):
    """Version 7.2: a session is recorded only when every stock held or traded that day is priced (and every buy or
    sell has a traded open or a stated fill price). Otherwise it and every later session wait, INCOMPLETE says why,
    and the next run with the missing rows adds them. `closed` lists (ticker, date) pairs whose market was shut: the
    holding counts as unchanged that day."""
    closed = set(closed or [])
    meta = {r["name"]: r for r in ledger if r["table"] == "meta"}
    start_date = meta["start_date"]["text"]
    start_value = num(meta["start_value"]["value"])
    spy_base = num(meta["spy_base"]["value"])
    brow = {r["date"]: r for r in series(hist, bench)}
    sessions = sorted(d for d in brow if start_date <= d <= today_date)
    done = {r["date"] for r in ledger if r["table"] == "perf" and r["value_est"] is not None}
    perf_rows = sorted((r for r in ledger if r["table"] == "perf" and r["value_est"] is not None), key=lambda r: r["date"])
    value = perf_rows[-1]["value_est"] if perf_rows else start_value
    added = []
    fills = {(r["name"], r["effective"]): num(r["value"]) for r in ledger if r["table"] == "position" and num(r["value"])}
    all_dates = sorted(brow)
    for d in sessions:
        if d in done:
            continue
        i = all_dates.index(d)
        dprev = all_dates[i - 1] if i > 0 else None
        w_new = live_weights(ledger, d)
        w_prev = live_weights(ledger, dprev) if (dprev and dprev >= start_date) else {}
        fdays = fill_days(ledger, dprev, d)               # v7.5: a London leg may have filled on 26 Nov (US shut)
        day, rows_d, gaps = 0.0, [], []
        for name in sorted(set(w_new) | set(w_prev)):
            wn, tick = w_new.get(name, (0.0, None))
            wp, tick2 = w_prev.get(name, (0.0, None))
            tick = tick or tick2
            cur = hist.get((tick, d))
            prv = None
            if cur:
                cutoff = dprev or ""
                earlier = [r for r in series(hist, tick) if r["date"] <= cutoff]
                prv = earlier[-1] if earlier else None
            kept, added_w, sold = min(wp, wn), max(wn - wp, 0.0), max(wp - wn, 0.0)
            if not cur:
                if (tick, d) in closed and not added_w and not sold:
                    cur = prv = {"open": 1.0, "close": 1.0}       # market shut: the holding is unchanged that day
                else:
                    gaps.append(f"{name} ({tick}): no price row")
                    continue
            if kept and not prv:
                gaps.append(f"{name} ({tick}): no earlier close")
                continue
            frow, fd = fill_row(hist, tick, fdays.get(name), d, cur) if (added_w or sold) else (cur, d)
            if (added_w and not fills.get((name, fd)) or sold) and not real_open(frow):
                gaps.append(f"{name} ({tick}): no traded open for the {'buy' if added_w else 'sale'}")
                continue
            contrib = 0.0
            if kept:
                contrib += kept * (cur["close"] / prv["close"] - 1.0)
            if added_w:
                contrib += added_w * (cur["close"] / (fills.get((name, fd)) or frow["open"]) - 1.0)   # bought at the open, or at a stated fill price
            if sold:
                contrib += sold * (frow["open"] / prv["close"] - 1.0)         # sold at the open
            day += contrib
            if wn or wp:
                rows_d.append(lrow("contrib", date=d, name=name, ticker=tick, weight=wn,
                                   ret_pct=r2(contrib / (wn or wp) * 100.0), contrib_pts=r2(contrib, 3)))
        if gaps:
            INCOMPLETE.append(f"{d}: " + "; ".join(gaps))
            warn(f"performance stops before {d}: " + "; ".join(gaps) + ". Give the missing rows (or list a closed market) and re-run")
            break                                         # later sessions wait too, so the value is never chained over a gap
        ledger.extend(rows_d)
        value = value * (1.0 + day / 100.0)
        spx = pct(brow[d]["close"], spy_base)
        ledger.append(lrow("perf", date=d, value_est=r2(value), day_pct=r2(day, 3),
                           cum_pct=r2(pct(value, start_value), 3), spx_cum_pct=r2(spx, 3)))
        added.append(d)
    return added


def resolve_confidence(ledger, hist, bench, timeout=SETTLE_TIMEOUT):
    """Version 7.3: a rating settles over one window, the first five benchmark sessions on or after its fill date
    (`effective`). The stock is bought at its own open on the fill date and valued at its close on the window's last
    date; the index from its open on the window's first session to its close on the last. Both stock rows must be
    there and the opening one must carry a traded open (real_open), and the index's opening row too; otherwise the
    rating waits, and once `timeout` sessions have passed it settles as "n/a" with the reason in `unit`."""
    bser = series(hist, bench)
    n = 0
    for r in ledger:
        if r["table"] != "confidence" or r["beat"] not in (None, "") or not r["effective"]:
            continue
        bafter = [x for x in bser if x["date"] >= r["effective"]]
        if len(bafter) < 5:
            continue
        end = bafter[4]["date"]
        r["window_end"] = end
        ser = {x["date"]: x for x in series(hist, r["ticker"])}
        start, fin = ser.get(r["effective"]), ser.get(end)
        why = None
        if not start:
            why = f"no row for {r['effective']}"
        elif not real_open(start):
            why = f"no traded open for {r['effective']}"
        elif not fin:
            why = f"no close for {end}"
        elif not real_open(bafter[0]):
            why = f"no traded open for the index on {bafter[0]['date']}"
        if why:
            if len(bafter) > timeout:
                r["beat"], r["unit"] = "n/a", "not scored: " + why
                n += 1
            continue
        s_ret = pct(fin["close"], start["open"])
        b_ret = pct(bafter[4]["close"], bafter[0]["open"])
        r["ret_pct"], r["spx_ret_pct"] = r2(s_ret), r2(b_ret)
        r["beat"] = "yes" if s_ret > b_ret else "no"
        r["unit"] = None
        n += 1
    return n


def add_postmortems(ledger, today_date, notes):
    notes = {n["name"]: n for n in (notes or [])}
    done = {(r["name"], r["effective"]) for r in ledger if r["table"] == "postmortem"}
    live = live_weights(ledger, today_date)
    names = {r["name"] for r in ledger if r["table"] == "contrib"}
    out = []
    for name in sorted(names):
      rows = sorted((r for r in ledger if r["table"] == "contrib" and r["name"] == name), key=lambda r: r["date"])
      runs, cur_run = [], []
      for r in rows:                       # a row with weight 0 is the day the position was sold at the open
          cur_run.append(r)
          if (num(r["weight"]) or 0) == 0:
              runs.append(cur_run)
              cur_run = []
      if cur_run and name not in live:
          runs.append(cur_run)
      for run in runs:
        entry, exit_ = run[0]["date"], run[-1]["date"]
        if (name, entry) in done or not any((num(r["weight"]) or 0) > 0 for r in run):
            continue
        total = sum(num(r["contrib_pts"]) or 0 for r in run)
        growth = 1.0
        for r in run:
            if r["ret_pct"] is not None:
                growth *= 1 + r["ret_pct"] / 100.0
        reason = next((r["text"] for r in ledger if r["table"] == "trade" and r["name"] == name and (num(r["to_w"]) or 0) > 0), "")
        nt = notes.get(name, {})
        ledger.append(lrow("postmortem", date=exit_, effective=entry, name=name, ret_pct=r2((growth - 1) * 100),
                           contrib_pts=r2(total, 3), days=len([r for r in run if (num(r["weight"]) or 0) > 0]),
                           text=(nt.get("text") or reason or ""), lesson=nt.get("lesson") or ""))
        out.append(name)
    return out


# ---------------------------------------------------------------- risk
def risk_tables(order, stocks_by_name, hist, scenarios, links=None):
    held = [(o["name"], num(o["weight"]) or 0.0) for o in order if (num(o.get("weight")) or 0) > 0]
    rets = {}
    for name, _ in held:
        tick = stocks_by_name[name]["ticker"]
        rets[name] = daily_returns(series(hist, tick))
    dates = None
    for name in rets:
        ds = set(rets[name])
        dates = ds if dates is None else dates & ds
    dates = sorted(dates or [])[-40:]
    rows, corr_rows = [], []
    port_vol = None
    if len(dates) >= 15:
        m = {n: [rets[n][d] * 100.0 for d in dates] for n, _ in held}
        mean = {n: sum(v) / len(v) for n, v in m.items()}
        def cov(a, b):
            return sum((x - mean[a]) * (y - mean[b]) for x, y in zip(m[a], m[b])) / (len(dates) - 1)
        names = [n for n, _ in held]
        w = dict(held)
        c = {(a, b): cov(a, b) for a in names for b in names}
        var = sum(w[a] / 100 * w[b] / 100 * c[(a, b)] for a in names for b in names)
        port_vol = math.sqrt(var) if var > 0 else 0.0
        for a in names:
            marg = sum(w[b] / 100 * c[(a, b)] for b in names)
            share = (w[a] / 100 * marg / var * 100.0) if var > 0 else None
            rows.append(lrow("risk", name=a, weight=w[a], theme=stocks_by_name[a].get("theme"),
                             vol_pct=r2(math.sqrt(c[(a, a)])), risk_share_pct=r2(share, 1)))
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                den = math.sqrt(c[(a, a)] * c[(b, b)])
                if den > 0:
                    corr_rows.append(lrow("corr", name=f"{a} / {b}", value=r2(c[(a, b)] / den)))
        corr_rows.sort(key=lambda r: -r["value"])
    else:
        for n, wt in held:
            rows.append(lrow("risk", name=n, weight=wt, theme=stocks_by_name[n].get("theme")))
    themes = {}
    for n, wt in held:
        t = stocks_by_name[n].get("theme") or "Other"
        themes[t] = themes.get(t, 0.0) + wt
    theme_rows = [lrow("theme", name=t, weight=r2(wt)) for t, wt in sorted(themes.items(), key=lambda x: -x[1])]
    theme_rows.append(lrow("theme", name="Cash", weight=r2(100 - sum(wt for _, wt in held))))
    scen_rows = []
    for sc in scenarios or []:
        shocks = sc.get("shocks") or {}
        impact, bits = 0.0, []
        for t, wt in sorted(themes.items(), key=lambda x: -x[1]):
            sh = num(shocks.get(t))
            if sh is None:
                sh = num(shocks.get("Other")) or 0.0
            impact += wt / 100.0 * sh
            bits.append(f"{t} {wt:g}% x {sh:+g}%")
        bsh = num(shocks.get("Bitcoin"))
        if bsh is not None:                        # an assumed move in Bitcoin, through each linked holding's measured link
            for n, wt in held:
                lk = (links or {}).get(n) or {}
                if lk.get("linked") and lk.get("btc_beta") is not None:
                    mv = lk["btc_beta"] * bsh
                    impact += wt / 100.0 * mv
                    bits.append(f"{n} {wt:g}% x {mv:+.1f}% (moves {lk['btc_beta']:.2f}% for each 1% in Bitcoin)")
            if not any(((links or {}).get(n) or {}).get("linked") for n, _ in held):
                bits.append("no crypto-linked holding, so a Bitcoin move adds nothing")
        scen_rows.append(lrow("scenario", name=sc["name"], impact_pct=r2(impact), text="; ".join(bits), plan=json.dumps(shocks, sort_keys=True)))
    return rows, corr_rows[:6], theme_rows, scen_rows, port_vol


def portfolio_fit(weights, names, tick_of, hist, themes, n=60):
    """Version 7.5, printed only: for each candidate, the correlation of its daily returns with the order's (weights
    fixed) and its highest correlation with one holding, over the latest `n` sessions all of them share, plus its theme's
    weight in the order now. Answers "does it add anything, or is it more of what is held?" beside the standalone score.
    `tick_of` maps a name to the ticker to measure (a London stock's US-listed line where the pipeline uses one)."""
    if not weights or not names:
        return []
    rets = {k: daily_returns(series(hist, tick_of.get(k))) for k in set(weights) | set(names) if tick_of.get(k)}
    if not all(k in rets for k in weights):
        return []
    common = set.intersection(*(set(rets[k]) for k in weights))
    theme_w = {}
    for k, w in weights.items():
        theme_w[themes.get(k, "Other")] = theme_w.get(themes.get(k, "Other"), 0.0) + w

    def corr(a, b):
        ma, mb = sum(a) / len(a), sum(b) / len(b)
        sa = math.sqrt(sum((x - ma) ** 2 for x in a))
        sb = math.sqrt(sum((y - mb) ** 2 for y in b))
        return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (sa * sb) if sa and sb else 0.0

    out = []
    for c in names:
        if c not in rets:
            continue
        ds = sorted(common & set(rets[c]))[-n:]
        if len(ds) < 20:
            continue
        x = [rets[c][d] for d in ds]
        port = [sum(w / 100.0 * rets[k][d] for k, w in weights.items()) for d in ds]
        best = max(((corr(x, [rets[k][d] for d in ds]), k) for k in weights), key=lambda z: z[0])
        out.append((c, {"corr": corr(x, port), "best": best[0], "best_name": best[1], "n": len(ds),
                        "theme": themes.get(c, "Other"), "theme_w": theme_w.get(themes.get(c, "Other"), 0.0)}))
    return out


# ---------------------------------------------------------------- moving averages
def ema(vals, n):
    """Exponential moving average, seeded with the simple average of the first n values."""
    if len(vals) < n:
        return None
    k = 2.0 / (n + 1)
    e = sum(vals[:n]) / n
    for v in vals[n:]:
        e = v * k + e * (1 - k)
    return e


def indicators(rows):
    """Simple and exponential averages from stored closes, the order they sit in, and any recent 50/200-day cross."""
    closes = [r["close"] for r in rows]
    out = {f"ma{n}": sma(closes, n) for n in (10, 20, 50, 100, 200)}
    out.update({f"ema{n}": ema(closes, n) for n in (10, 20, 50, 200)})
    last = closes[-1] if closes else None
    e = [out["ema10"], out["ema20"], out["ema50"], out["ema200"]]
    out["ema_stack"] = ""
    if last is not None and all(x is not None for x in e):
        out["ema_stack"] = "up" if last > e[0] > e[1] > e[2] > e[3] else "down" if last < e[0] < e[1] < e[2] < e[3] else "mixed"
    out["cross"] = ""
    if len(closes) >= 221:
        diff = []
        for k in range(21):                       # newest first
            sub = closes[:len(closes) - k]
            diff.append(sma(sub, 50) - sma(sub, 200))
        for k in range(20):
            if diff[k] > 0 >= diff[k + 1]:
                out["cross"] = "golden cross on " + rows[len(rows) - 1 - k]["date"]
                break
            if diff[k] < 0 <= diff[k + 1]:
                out["cross"] = "death cross on " + rows[len(rows) - 1 - k]["date"]
                break
    return out


def tier_of(score, flags):
    """Strength band tied to the decision rules: strong can be bought as a core position, weak should be replaced."""
    if score is None:
        return ""
    if score < 45 or any(f.startswith("downtrend") for f in flags):
        return "weak"
    if score >= 60 and not any(f.startswith("below 50-day") for f in flags):
        return "strong"
    return "middling"


# ---------------------------------------------------------------- macro: yields and oil
MACRO_SERIES = [("us2y", "US 2-year yield", "yield"), ("us10y", "US 10-year yield", "yield"),
                ("us30y", "US 30-year yield", "yield"), ("uk10y", "UK 10-year gilt yield", "yield"),
                ("de10y", "German 10-year yield", "yield"), ("fr10y", "French 10-year yield", "yield"),
                ("it10y", "Italian 10-year yield", "yield"), ("jp10y", "Japanese 10-year yield", "yield"),
                ("brent", "Brent crude, $ a barrel", "commodity"), ("wti", "WTI crude, $ a barrel", "commodity"),
                ("natgas", "US natural gas, $", "commodity"), ("gold", "Gold, $ an ounce", "commodity"),
                ("btc", "Bitcoin, $", "crypto"), ("eth", "Ether, $", "crypto"), ("sol", "Solana, $", "crypto"),
                ("xrp", "XRP, $", "crypto")]
CRYPTO_PROXY = {"btc": "IBIT", "eth": "ETHA"}       # US-listed spot funds: their closes line up with stock sessions
CRYPTO_NAME = {"btc": "Bitcoin", "eth": "Ether"}
CRYPTO_SERIES = ("btc", "eth", "sol", "xrp")
MACRO_SPREADS = [("us10y", "us2y", "US 10-year minus 2-year"), ("uk10y", "us10y", "UK minus US 10-year"),
                 ("it10y", "de10y", "Italy minus Germany 10-year")]


def merge_macro(mac, rows):
    n = 0
    for r in rows or []:
        d, s, v = str(r.get("date") or "")[:10], r.get("series"), num(r.get("value"))
        if len(d) != 10 or not s or v is None:
            continue
        if s in ("us2y", "us10y", "us30y", "uk10y", "de10y", "fr10y", "it10y", "jp10y") and not (-1 <= v <= 25):
            warn(f"macro {s} {d}: {v} is not a plausible yield; skipped")
            continue
        if v <= 0 and s in ("brent", "wti", "natgas", "gold") + CRYPTO_SERIES:
            continue
        if mac.get((s, d)) != v:
            n += 1
        mac[(s, d)] = v
    return n


def mseries(mac, s, upto=None):
    return sorted((d, v) for (k, d), v in mac.items() if k == s and (upto is None or d <= upto))


def macro_panel(mac, hist, date, oil_proxy):
    rows, facts = [], {}
    for s, label, kind in MACRO_SERIES:
        ser = mseries(mac, s, date)
        if not ser:
            continue
        vals = [v for _, v in ser]
        last_d, last = ser[-1]
        def chg(n):
            if len(vals) <= n:
                return None
            return (last - vals[-1 - n]) * 100.0 if kind == "yield" else pct(last, vals[-1 - n])
        c1, c5, c20 = chg(1), chg(5), chg(20)
        unit, note = ("bp" if kind == "yield" else "%"), ""
        proxy = oil_proxy if s == "brent" else CRYPTO_PROXY.get(s)
        if proxy and (s == "brent" or series(hist, proxy)):
            pc = [r["close"] for r in series(hist, proxy) if r["date"] <= date]
            px = lambda n: pct(pc[-1], pc[-1 - n]) if len(pc) > n else None
            if c1 is None: c1 = px(1)
            if c5 is None: c5, note = px(5), f"changes over 5 and 20 sessions are from the {proxy} fund until the price series is long enough"
            if c20 is None: c20 = px(20)
        yr = vals[-252:]
        pos = (last - min(yr)) / (max(yr) - min(yr)) * 100.0 if (len(yr) >= 60 and max(yr) > min(yr)) else None
        facts[s] = {"last": last, "c1": c1, "c5": c5, "c20": c20, "date": last_d}
        if last_d < date:
            note = (note + "; " if note else "") + f"latest figure is for {last_d}"
        rows.append(lrow("macro", date=last_d, name=label, ticker=s, kind=kind, value=r2(last, 3 if kind == "yield" else 4 if (kind == "crypto" and last < 10) else 2),
                         chg_1d=r2(c1, 1 if kind == "yield" else 2), chg_5d=r2(c5, 1 if kind == "yield" else 2),
                         chg_20d=r2(c20, 1 if kind == "yield" else 2), unit=unit, percentile=r2(pos, 0), text=note))
    for a, b, label in MACRO_SPREADS:
        sa, sb = dict(mseries(mac, a, date)), dict(mseries(mac, b, date))
        common = sorted(set(sa) & set(sb))
        if not common:
            continue
        sp = [(sa[d] - sb[d]) * 100.0 for d in common]
        ch = lambda n: sp[-1] - sp[-1 - n] if len(sp) > n else None
        rows.append(lrow("macro", date=common[-1], name=label, ticker=f"{a}-{b}", kind="spread", value=r2(sp[-1], 0),
                         chg_1d=r2(ch(1), 1), chg_5d=r2(ch(5), 1), chg_20d=r2(ch(20), 1), unit="bp", text=""))
    # backdrop: a plain reading of the week's moves in yields and oil
    pts, bits = 0, []
    y = facts.get("us10y")
    if y and y["c5"] is not None:
        if y["c5"] >= 10: pts -= 1; bits.append(f"US 10-year yield up {y['c5']:.0f}bp in five sessions to {y['last']:.2f}%: a headwind for shares, most of all long-duration growth")
        elif y["c5"] <= -10: pts += 1; bits.append(f"US 10-year yield down {-y['c5']:.0f}bp in five sessions to {y['last']:.2f}%: a tailwind for shares")
        else: bits.append(f"US 10-year yield little changed over five sessions ({y['c5']:+.0f}bp) at {y['last']:.2f}%")
    o = facts.get("brent")
    if o and o["c5"] is not None:
        if o["c5"] >= 5: pts -= 1; bits.append(f"Brent up {o['c5']:.1f}% in five sessions to ${o['last']:.2f}: an inflation worry for the market, a support for energy holdings")
        elif o["c5"] <= -5: pts += 1; bits.append(f"Brent down {-o['c5']:.1f}% in five sessions to ${o['last']:.2f}: eases inflation worry, a drag on energy holdings")
        else: bits.append(f"Brent little changed over five sessions ({o['c5']:+.1f}%) at ${o['last']:.2f}")
    g = facts.get("uk10y")
    if g:
        bits.append(f"UK 10-year gilt {g['last']:.2f}%" + (f" ({g['c5']:+.0f}bp in five sessions)" if g["c5"] is not None else ""))
    label = "headwind" if pts < 0 else "tailwind" if pts > 0 else "neutral"
    if facts:
        rows.append(lrow("macro", date=date, name="Backdrop for shares", ticker="backdrop", kind="backdrop", value=pts, action=label,
                         text="; ".join(bits)))
    return rows, facts, label


def ols_slope(xs, ys):
    n = len(xs)
    if n < 30:
        return None, None
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    if sxx <= 0 or syy <= 0:
        return None, None
    return sxy / sxx, sxy / math.sqrt(sxx * syy)


def slope_net(x1, x2, y):
    """Slope of y on x2 with x1 in the same fit (two-variable least squares). None with fewer than 30 points."""
    n = len(y)
    if n < 30:
        return None
    m1, m2, my = sum(x1) / n, sum(x2) / n, sum(y) / n
    s11 = sum((a - m1) ** 2 for a in x1)
    s22 = sum((b - m2) ** 2 for b in x2)
    s12 = sum((a - m1) * (b - m2) for a, b in zip(x1, x2))
    s1y = sum((a - m1) * (c - my) for a, c in zip(x1, y))
    s2y = sum((b - m2) * (c - my) for b, c in zip(x2, y))
    den = s11 * s22 - s12 * s12
    if s11 <= 0 or s22 <= 0 or den <= 1e-9 * s11 * s22:
        return None
    return (s11 * s2y - s12 * s1y) / den


def crypto_trend(hist, date):
    """Bitcoin's and Ether's trend from the closes of their US-listed funds. Returns (ledger rows, {coin: facts})."""
    rows, facts = [], {}
    for key, tick in CRYPTO_PROXY.items():
        c = [r["close"] for r in series(hist, tick) if r["date"] <= date]
        if len(c) < 50:
            continue
        last, v20, v50, v200 = c[-1], pct(c[-1], sma(c, 20)), pct(c[-1], sma(c, 50)), pct(c[-1], sma(c, 200))
        state = ("up" if v50 > 0 and (v200 is None or v200 > 0) else
                 "down" if v50 < 0 and (v200 is None or v200 < 0) else "mixed")
        c5, c20 = ret_n(c, 5), ret_n(c, 20)
        side = lambda v: f"{abs(v):.1f}% {'above' if v >= 0 else 'below'}"
        text = (f"{CRYPTO_NAME[key]}, read through the {tick} fund, is {side(v20)} its 20-day average, {side(v50)} its 50-day average"
                + (f" and {side(v200)} its 200-day average" if v200 is not None else "")
                + (f"; {c5:+.1f}% over five sessions" if c5 is not None else "")
                + (f" and {c20:+.1f}% over twenty" if c20 is not None else "") + f". Trend: {state}.")
        facts[key] = {"state": state, "v20": v20, "v50": v50, "v200": v200, "c5": c5, "c20": c20, "days": len(c), "text": text}
        rows.append(lrow("macro", date=date, name=f"{CRYPTO_NAME[key]} trend", ticker=f"trend:{key}", kind="crypto-trend",
                         value=r2(v50), percentile=r2(v200), chg_1d=r2(v20), chg_5d=r2(c5), chg_20d=r2(c20), unit="%", action=state,
                         days=len(c), text=text))
    return rows, facts


def crypto_links(hist, bench, tick_of, themes, date, n=120):
    """For every stock: the move that has gone with a 1% move in Bitcoin and in Ether over the last n sessions, from its
    daily returns against the IBIT and ETHA funds, and Bitcoin's slope with the S&P 500 in the same fit (btc_net).
    A stock is crypto-linked if its theme is "Crypto" or either correlation is 0.5 or more over 60 or more sessions."""
    out = {}
    mk = daily_returns(series(hist, bench))
    drv = {k: daily_returns(series(hist, t)) for k, t in CRYPTO_PROXY.items()}
    if not any(drv.values()):
        return out
    for name, tick in tick_of.items():
        a = daily_returns(series(hist, tick))
        rec = {}
        for k, b in drv.items():
            ds = sorted(d for d in a if d in b and d <= date)[-n:]
            slope, corr = ols_slope([b[d] for d in ds], [a[d] for d in ds])
            if slope is None:
                continue
            rec[k + "_beta"], rec[k + "_corr"] = slope, corr
            rec["crypto_days"] = max(rec.get("crypto_days") or 0, len(ds))
            if k == "btc":
                d2 = [d for d in ds if d in mk]
                rec["btc_net"] = slope_net([mk[d] for d in d2], [b[d] for d in d2], [a[d] for d in d2])
        best = max([v for v in (rec.get("btc_corr"), rec.get("eth_corr")) if v is not None] or [-1.0])
        rec["linked"] = (themes.get(name) == "Crypto") or ((rec.get("crypto_days") or 0) >= 60 and best >= 0.5)
        if rec["linked"] or len(rec) > 1:
            out[name] = rec
    return out


def port_returns(weights, tick_of, hist):
    """Daily return of today's weights applied to past days: date -> % (only days where at least 70% of the invested weight has a price)."""
    rets = {n: daily_returns(series(hist, tick_of[n])) for n, w in weights.items() if w > 0 and n in tick_of}
    invested = sum(w for n, w in weights.items() if w > 0)
    dates = set()
    for r in rets.values():
        dates |= set(r)
    out = {}
    for d in sorted(dates):
        have = sum(weights[n] for n in rets if d in rets[n])
        if invested and have / invested >= 0.7:
            out[d] = sum(weights[n] * rets[n][d] for n in rets if d in rets[n])     # weight (%) x return = points of the portfolio
    return out


def sensitivities(mac, hist, bench, oil_proxy, weights, tick_of, date):
    rows = []
    port = port_returns(weights, tick_of, hist)
    brets = {d: v * 100.0 for d, v in daily_returns(series(hist, bench)).items()}
    oil = {d: v * 100.0 for d, v in daily_returns(series(hist, oil_proxy)).items()} if oil_proxy else {}
    y = mseries(mac, "us10y", date)
    dy = {b[0]: (b[1] - a[1]) * 100.0 for a, b in zip(y, y[1:])}
    btc = {d: v * 100.0 for d, v in daily_returns(series(hist, CRYPTO_PROXY["btc"])).items()}
    drivers = [(oil, 1.0, "a 1% rise in oil", "oil"), (dy, 10.0, "a 10bp rise in the US 10-year yield", "yield")]
    if btc:
        drivers.append((btc, 10.0, "a 10% rise in Bitcoin", "btc"))
    for who, rr in (("Portfolio", port), ("S&P 500", brets)):
        for drv, scale, what, key in drivers:
            ds = sorted(d for d in rr if d in drv and d <= date)[-120:]
            slope, corr = ols_slope([drv[d] for d in ds], [rr[d] for d in ds])
            if slope is None:
                continue
            rows.append(lrow("macro", date=date, name=f"{who}: move that has gone with {what}", ticker=f"sens:{who}:{key}", kind="sensitivity",
                             value=r2(slope * scale, 2), unit="%", days=len(ds), percentile=r2(corr, 2),
                             text=f"Over the last {len(ds)} sessions, {what} has gone with a {slope * scale:+.2f}% move in {'the portfolio at today' + chr(39) + 's weights' if who == 'Portfolio' else 'the S&P 500'} (correlation {corr:+.2f})."))
    return rows


# ---------------------------------------------------------------- day-ahead call from similar past days
def lookup_le(pairs, d, max_gap=6):
    """Latest value dated on or before d (pairs sorted by date); None if older than max_gap calendar days."""
    import bisect
    i = bisect.bisect_right(pairs, (d, float("inf"))) - 1
    if i < 0:
        return None
    dd, v = pairs[i]
    y1, m1, d1 = int(d[:4]), int(d[5:7]), int(d[8:10])
    y0, m0, d0 = int(dd[:4]), int(dd[5:7]), int(dd[8:10])
    gap = (y1 - y0) * 372 + (m1 - m0) * 31 + (d1 - d0)
    return v if gap <= max_gap + 3 else None


def day_features(bser, mac, oil_rows):
    c = [r["close"] for r in bser]
    dates = [r["date"] for r in bser]
    y = mseries(mac, "us10y")
    oil = [(r["date"], r["close"]) for r in oil_rows]
    out = []
    for i in range(20, len(bser)):
        rets = [pct(c[j], c[j - 1]) for j in range(i - 9, i + 1)]
        mu = sum(rets) / len(rets)
        f = {"date": dates[i], "r1": pct(c[i], c[i - 1]), "r5": pct(c[i], c[i - 5]), "dist20": pct(c[i], sum(c[i - 19:i + 1]) / 20.0),
             "vol10": math.sqrt(sum((x - mu) ** 2 for x in rets) / (len(rets) - 1)),
             "next": pct(c[i + 1], c[i]) if i + 1 < len(c) else None, "next_date": dates[i + 1] if i + 1 < len(c) else None}
        y0, y1, y5 = lookup_le(y, dates[i]), lookup_le(y, dates[i - 1]), lookup_le(y, dates[i - 5])
        f["dy1"] = (y0 - y1) * 100.0 if (y0 is not None and y1 is not None) else None
        f["dy5"] = (y0 - y5) * 100.0 if (y0 is not None and y5 is not None) else None
        o0, o1, o5 = lookup_le(oil, dates[i]), lookup_le(oil, dates[i - 1]), lookup_le(oil, dates[i - 5])
        f["o1"] = pct(o0, o1) if (o0 and o1) else None
        f["o5"] = pct(o0, o5) if (o0 and o5) else None
        out.append(f)
    return out


FEATS = ("r1", "r5", "dist20", "vol10", "dy1", "dy5", "o1", "o5")
CONDITIONS = [
    ("the S&P 500 rose more than 0.5%", lambda f: f["r1"] > 0.5), ("the S&P 500 fell more than 0.5%", lambda f: f["r1"] < -0.5),
    ("the S&P 500 moved less than 0.5%", lambda f: -0.5 <= f["r1"] <= 0.5),
    ("the S&P 500 was above its 20-day average", lambda f: f["dist20"] > 0), ("the S&P 500 was below its 20-day average", lambda f: f["dist20"] <= 0),
    ("the S&P 500 was up more than 1% over five sessions", lambda f: f["r5"] > 1), ("the S&P 500 was down more than 1% over five sessions", lambda f: f["r5"] < -1),
    ("the US 10-year yield rose 5bp or more on the day", lambda f: f["dy1"] >= 5), ("the US 10-year yield fell 5bp or more on the day", lambda f: f["dy1"] <= -5),
    ("the US 10-year yield moved less than 5bp on the day", lambda f: -5 < f["dy1"] < 5),
    ("the US 10-year yield was up 10bp or more over five sessions", lambda f: f["dy5"] >= 10),
    ("the US 10-year yield was down 10bp or more over five sessions", lambda f: f["dy5"] <= -10),
    ("oil rose 2% or more on the day", lambda f: f["o1"] >= 2), ("oil fell 2% or more on the day", lambda f: f["o1"] <= -2),
    ("oil was up 5% or more over five sessions", lambda f: f["o5"] >= 5), ("oil was down 5% or more over five sessions", lambda f: f["o5"] <= -5),
]


def day_call(hist, mac, bench, oil_proxy, weights, tick_of, date, k=40, shrink=40):
    """Chance that the next session closes up, from the k past days most like today on eight measures
    (S&P 500 move over one and five days, distance from its 20-day average, 10-day volatility, the US 10-year
    yield's move over one and five days, oil's move over one and five days), pulled halfway back to the usual rate."""
    bser = [r for r in series(hist, bench) if r["date"] <= date]
    oil_rows = [r for r in series(hist, oil_proxy) if r["date"] <= date] if oil_proxy else []
    feats = [f for f in day_features(bser, mac, oil_rows) if all(f[x] is not None for x in FEATS)]
    if not feats or feats[-1]["date"] != date:
        return None
    today, past = feats[-1], [f for f in feats[:-1] if f["next"] is not None]
    if len(past) < 120:
        return None
    sd = {}
    for x in FEATS:
        vals = [f[x] for f in past]
        mu = sum(vals) / len(vals)
        sd[x] = math.sqrt(sum((v - mu) ** 2 for v in vals) / (len(vals) - 1)) or 1.0
    dist = lambda f: math.sqrt(sum(((f[x] - today[x]) / sd[x]) ** 2 for x in FEATS))
    ranked = sorted(past, key=dist)
    port = port_returns(weights, tick_of, hist)
    out = {"features": today, "sample": len(past), "from": past[0]["date"], "evidence": []}
    for who in ("S&P 500", "Portfolio"):
        if who == "S&P 500":
            pool, nxt, kk = past, (lambda f: f["next"]), k
        else:
            pool, nxt, kk = [f for f in past if f["next_date"] in port], (lambda f: port[f["next_date"]]), min(k, 30)
            if len(pool) < 120:
                continue
        base = sum(1 for f in pool if nxt(f) > 0) / len(pool)
        near = [f for f in ranked if (who == "S&P 500" or f["next_date"] in port)][:kk]
        ups = sum(1 for f in near if nxt(f) > 0)
        p = (ups + shrink * base) / (len(near) + shrink) * 100.0
        out[who] = {"p": p, "base": base * 100.0, "k": len(near), "ups": ups, "mean": sum(nxt(f) for f in near) / len(near),
                    "pool": len(pool), "dates": [f["date"] for f in near[:5]], "cover": None}
        if who == "Portfolio":
            invested = sum(w for w in weights.values() if w > 0)
            have = sum(w for n, w in weights.items() if w > 0 and n in tick_of and len(series(hist, tick_of[n])) >= 150)
            out[who]["cover"] = have / invested * 100.0 if invested else None
        for label, test in CONDITIONS:
            if not test(today):
                continue
            grp = [f for f in pool if test(f)]
            if len(grp) < 15:
                continue
            rate = sum(1 for f in grp if nxt(f) > 0) / len(grp) * 100.0
            mean = sum(nxt(f) for f in grp) / len(grp)
            kind = "bull" if rate >= base * 100.0 + 2 else "bear" if rate <= base * 100.0 - 2 else "neutral"
            out["evidence"].append(lrow("analog", date=date, name="After days when " + label, stock=who, kind=kind, days=len(grp),
                                        percentile=r2(rate, 0), value=r2(mean, 3),
                                        text=f"{who} rose the next day {rate:.0f}% of the time ({len(grp)} days, average {mean:+.2f}%), against a usual {base * 100:.0f}%"))
    return out


def next_weekday(d):
    """The next US session after d: the next weekday, skipping US_CLOSED (version 7.3)."""
    import datetime
    x = datetime.date(int(d[:4]), int(d[5:7]), int(d[8:10])) + datetime.timedelta(days=1)
    while x.weekday() >= 5 or x.isoformat() in US_CLOSED:
        x += datetime.timedelta(days=1)
    return x.isoformat()


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def write_day_call(ledger, call, target, date, notes):
    """One row per target session for the S&P 500 and one for the portfolio. The model's figure goes in `score`; the
    reviewer may move it by up to 5 points with a reason (`adj_eve`), and the morning check by up to 5 more (`adj_morn`)."""
    notes = notes or {}
    for who in ("S&P 500", "Portfolio"):
        c = call.get(who)
        if not c:                                      # no figure this time: an open row from an earlier run is marked as such
            stale = next((r for r in ledger if r["table"] == "daycall" and r["date"] == target and r["name"] == who and r["ret_pct"] is None), None)
            if stale and "earlier weights" not in (stale["action"] or ""):
                stale["action"] = (stale["action"] or "") + "; worked out on earlier weights, because too few of the present holdings have a year of stored prices"
            continue
        old = next((r for r in ledger if r["table"] == "daycall" and r["date"] == target and r["name"] == who), None)
        if old and old["ret_pct"] is not None:
            continue                                   # already settled
        adj = clamp(num(notes.get("adjust" if who == "S&P 500" else "port_adjust")) or 0.0, -5, 5)
        if old and not (notes.get("bull") or notes.get("bear") or notes.get("reason")):
            adj = num(old["adj_eve"]) or 0.0            # nothing written this time: the earlier cases and adjustment stand
        morn = (num(old["adj_morn"]) or 0.0) if old else 0.0
        final = int(round(clamp(c["p"] + adj + morn, 1, 99)))
        row = lrow("daycall", date=target, effective=date, name=who, kind="green" if final >= 50 else "red",
                   score=r2(c["p"], 1), confidence=final, adj_eve=adj, adj_morn=morn, percentile=r2(c["base"], 1), days=c["k"],
                   value=r2(c["mean"], 3), text=notes.get("bull") or (old or {}).get("text") or "",
                   plan=notes.get("bear") or (old or {}).get("plan") or "",
                   lesson=notes.get("reason") or (old or {}).get("lesson") or "",
                   action=f"{c['ups']} of the {c['k']} most similar days were followed by a rise (average {c['mean']:+.2f}%); usual rate {c['base']:.0f}% over {c['pool']} days"
                          + (f"; uses the holdings with a long price history, {c['cover']:.0f}% of the invested weight" if c.get("cover") is not None and c["cover"] < 99.5 else ""))
        if old:
            ledger.remove(old)
        ledger.append(row)


def resolve_day_calls(ledger, hist, bench):
    bser = series(hist, bench)
    idx = {r["date"]: i for i, r in enumerate(bser)}
    perf = {r["date"]: r["day_pct"] for r in ledger if r["table"] == "perf"}
    n = 0
    for r in ledger:
        if r["table"] != "daycall" or r["ret_pct"] is not None:
            continue
        ret = None
        if r["name"] == "S&P 500" and r["date"] in idx and idx[r["date"]] > 0:
            ret = pct(bser[idx[r["date"]]]["close"], bser[idx[r["date"]] - 1]["close"])
        elif r["name"] == "Portfolio" and perf.get(r["date"]) is not None and r["date"] in idx:
            ret = perf[r["date"]]
        if ret is None:
            continue
        r["ret_pct"] = r2(ret, 3)
        r["beat"] = "yes" if ((r["confidence"] or 0) >= 50) == (ret > 0) else "no"
        n += 1
    return n


# ---------------------------------------------------------------- calibration: does the score carry information?
SCORE_BANDS = [(70, 200, "Score 70 and above"), (60, 69, "Score 60 to 69"), (45, 59, "Score 45 to 59"), (0, 44, "Score below 45")]
PRICE_BANDS = [(36, 99, "36 to 48 points"), (28, 35, "28 to 35 points"), (20, 27, "20 to 27 points"), (0, 19, "Below 20 points")]


def add_shadow(ledger, date, scores, tick_of, hist):
    """A rating for every scored stock every evening, held or not, so the score can be checked against what happened next."""
    for name, x in scores.items():
        row = hist.get((tick_of[name], date))
        if not row:
            continue
        ledger[:] = [r for r in ledger if not (r["table"] == "shadow" and r["date"] == date and r["name"] == name and r["beat"] is None)]
        if any(r["table"] == "shadow" and r["date"] == date and r["name"] == name for r in ledger):
            continue
        parts = {"quant": r2((num(x.get("trend_pts")) or 0) + (num(x.get("short_pts")) or 0), 1),
                 "judg": r2((num(x.get("catalyst_pts")) or 0) + (num(x.get("revisions_pts")) or 0), 1)}
        ledger.append(lrow("shadow", date=date, name=name, ticker=tick_of[name], score=x["score"], confidence=x["confidence_anchor"],
                           value=row["close"], theme=tier_of(x["score"], x["flags"]), text="; ".join(x["flags"]),
                           plan=json.dumps(parts)))


def resolve_shadow(ledger, hist, bench):
    bser = series(hist, bench)
    bidx = {r["date"]: i for i, r in enumerate(bser)}
    n = 0
    for r in ledger:
        if r["table"] != "shadow" or r["beat"] is not None or r["date"] not in bidx:
            continue
        i = bidx[r["date"]]
        if i + 5 >= len(bser):
            continue
        end = bser[i + 5]["date"]
        ser = series(hist, r["ticker"])
        start = next((x for x in ser if x["date"] == r["date"]), None)
        fin = next((x for x in ser if x["date"] == end), None)       # version 7.3: the exact end date, never an earlier close
        if not start or not fin:
            if i + SETTLE_TIMEOUT < len(bser):
                r["beat"], r["window_end"] = "n/a", end        # no prices arrived for three weeks: leave it out of the count
            continue                                   # the stock's prices do not reach the end of the window yet
        s_ret, b_ret = pct(fin["close"], start["close"]), pct(bser[i + 5]["close"], bser[i]["close"])
        r["window_end"], r["ret_pct"], r["spx_ret_pct"] = end, r2(s_ret), r2(b_ret)
        r["beat"] = "yes" if s_ret > b_ret else "no"
        n += 1
    return n


PART_NAMES = [("vs_50d", "distance from the 50-day average"), ("structure", "50-day and 200-day order"),
              ("near_high", "closeness to the 52-week high"), ("rs_52w", "one-year return against the index"),
              ("rs_2m", "two-month return against the index"), ("rsi", "RSI band"), ("rs_5d", "five-day return against the index")]


def price_parts(c, b):
    """The part of the score that needs only closing prices (48 of the 100 points), split into its seven parts, for a
    stock's closes c and the benchmark's closes b over the same dates, both ending on the day being scored. The bands
    are the ones score_stock uses."""
    price, ma50, ma200 = c[-1], sma(c, 50), sma(c, 200)
    vs50 = pct(price, ma50)
    p = {}
    p["vs_50d"] = 0 if vs50 < -5 else 3 if vs50 < 0 else 8 if vs50 < 2 else 12 if vs50 <= 15 else 8 if vs50 <= 25 else 4
    p["structure"] = (5 if ma50 > ma200 else 0) + (3 if price > ma200 else 0)
    p["near_high"] = band(pct(price, max(c[-252:])), [(-3, 10), (-8, 7), (-15, 4), (-25, 2)])
    span = min(251, len(c) - 1)
    p["rs_52w"] = band(pct(c[-1], c[-1 - span]) - pct(b[-1], b[-1 - span]), [(30, 4), (10, 3), (0, 1)])
    p["rs_2m"] = band(pct(c[-1], c[-43]) - pct(b[-1], b[-43]), [(5, 2), (0, 1)])
    rsi = rsi_wilder(c)
    p["rsi"] = 0 if rsi > 80 else 2 if rsi >= 70 else 4 if rsi >= 50 else 2 if rsi >= 40 else 0
    p["rs_5d"] = band(pct(c[-1], c[-6]) - pct(b[-1], b[-6]), [(3, 8), (1, 6), (0, 4), (-2, 2)])
    return p


def price_points(c, b):
    return sum(price_parts(c, b).values())


# ---------------------------------------------------------------- the panel test: 30 stocks fixed in advance
def ranks(xs):
    """Average ranks (1 = smallest), ties sharing the mean of their places."""
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    out = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            out[order[k]] = (i + j) / 2.0 + 1.0
        i = j + 1
    return out


def spearman(xs, ys):
    if len(xs) < 3:
        return None
    rx, ry = ranks(xs), ranks(ys)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    sxy = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    sxx, syy = sum((a - mx) ** 2 for a in rx), sum((b - my) ** 2 for b in ry)
    if sxx <= 0 or syy <= 0:
        return None                                    # every stock had the same points (or the same return) that day
    return sxy / math.sqrt(sxx * syy)


def mean_t(vals):
    """Mean, t-statistic (mean over its standard error) and count."""
    vals = [v for v in vals if v is not None]
    n = len(vals)
    if n == 0:
        return None, None, 0
    m = sum(vals) / n
    if n < 2:
        return m, None, n
    sd = math.sqrt(sum((v - m) ** 2 for v in vals) / (n - 1))
    return m, (m / (sd / math.sqrt(n)) if sd > 0 else None), n


PANEL_MIN_CLOSES = 252        # a full year up to the day being scored, so every part is worked out as the score does
PANEL_MIN_STOCKS = 10         # a date counts only if at least this many panel stocks can be scored on it
PANEL_STEP = 5                # non-overlapping five-session windows


def panel_series(panel, hist):
    """date -> close for every panel member, from panel.json, with any closes the main store holds for the same ticker
    (a panel stock that is also on the list) laid over them."""
    out = {}
    for m in panel.get("members") or []:
        t = m["ticker"]
        d = {r[0]: r[1] for r in (panel.get("closes") or {}).get(t, [])}
        for r in series(hist, t):
            d[r["date"]] = r["close"]
        out[t] = d
    return out


def panel_obs(panel, hist, bench):
    """One observation per panel stock per signal date: the price-only points and their parts on that date, and the
    stock's return minus the index's over the next five sessions (and, as a check, over five sessions starting a day
    later, which leaves out the first night's gap that an order filling at the next open cannot catch). Signal dates
    are every fifth benchmark session counted from the date the panel was fixed, so no two windows of one stock overlap."""
    bser = series(hist, bench)
    bd = [r["date"] for r in bser]
    bc = [r["close"] for r in bser]
    frozen = panel.get("frozen") or "9999-12-31"
    anchor = next((i for i, d in enumerate(bd) if d >= frozen), len(bd))
    sigs = [i for i in range(len(bd)) if (i - anchor) % PANEL_STEP == 0]
    obs = []
    for t, closes in panel_series(panel, hist).items():
        idx = [i for i, d in enumerate(bd) if d in closes]           # benchmark sessions this stock has a close for
        if len(idx) < PANEL_MIN_CLOSES:
            continue
        pos = {i: k for k, i in enumerate(idx)}
        c = [closes[bd[i]] for i in idx]
        b = [bc[i] for i in idx]
        for i in sigs:
            k = pos.get(i)
            if k is None or k + 1 < PANEL_MIN_CLOSES or k + 5 >= len(idx) or idx[k + 5] != i + 5:
                continue                                              # not enough history, or the window is not complete
            parts = price_parts(c[:k + 1], b[:k + 1])
            ex = pct(c[k + 5], c[k]) - pct(b[k + 5], b[k])
            ex_late = (pct(c[k + 6], c[k + 1]) - pct(b[k + 6], b[k + 1])) if (k + 6 < len(idx) and idx[k + 6] == i + 6) else None
            obs.append({"date": bd[i], "ticker": t, "pts": sum(parts.values()), "parts": parts, "ex": ex, "ex_late": ex_late,
                        "live": bd[i] >= frozen})
    return obs


def panel_stats(obs, key="pts", ret="ex"):
    by_date = {}
    for o in obs:
        if o.get(ret) is None:
            continue
        x = o[key] if key == "pts" else o["parts"][key]
        by_date.setdefault(o["date"], []).append((x, o[ret]))
    ics, spreads = [], []
    for d, xs in sorted(by_date.items()):
        if len(xs) < PANEL_MIN_STOCKS:
            continue
        ic = spearman([a for a, _ in xs], [b for _, b in xs])
        if ic is not None:
            ics.append(ic)
        srt = sorted(xs, key=lambda v: v[0])
        third = len(srt) // 3
        if third >= 3 and srt[-third][0] > srt[third - 1][0]:          # only when the top and bottom thirds differ in points
            spreads.append(sum(v for _, v in srt[-third:]) / third - sum(v for _, v in srt[:third]) / third)
    m_ic, t_ic, n_ic = mean_t(ics)
    m_sp, t_sp, n_sp = mean_t(spreads)
    return {"ic": m_ic, "ic_t": t_ic, "dates": n_ic, "ic_pos": (sum(1 for v in ics if v > 0) / len(ics) * 100.0) if ics else None,
            "spread": m_sp, "spread_t": t_sp, "spread_dates": n_sp,
            "cases": sum(len(v) for d, v in by_date.items() if len(v) >= PANEL_MIN_STOCKS)}


def panel_verdict(s):
    """The test fixed on 15 Oct 2026, before any panel data was seen. The measure is the average, over signal dates, of
    the rank correlation across the panel between the price-only points and the next five sessions' return against
    the index."""
    if s["dates"] < 8:
        return "too few dates to judge (at least 8 are needed)"
    if s["ic"] >= 0.03 and (s["ic_t"] or 0) >= 2.0:
        return "the price points rank stocks usefully over five sessions"
    if s["ic"] <= -0.03 and (s["ic_t"] or 0) <= -2.0:
        return "the price points rank stocks the wrong way over five sessions"
    return "no evidence that the price points rank stocks over five sessions"


def panel_rows(panel, hist, bench, date):
    if not (panel.get("members")):
        return [], None
    obs = panel_obs(panel, hist, bench)
    rows, summary = [], {}
    for period, sub in (("history", [o for o in obs if not o["live"]]), ("live", [o for o in obs if o["live"]])):
        s = panel_stats(sub)
        s_late = panel_stats(sub, ret="ex_late")
        verdict = panel_verdict(s) if s["dates"] else "no complete windows yet"
        summary[period] = (s, s_late, verdict)
        f2 = lambda v, d=3: "n/a" if v is None else f"{v:+.{d}f}"
        rows.append(lrow("calib", date=date, name=f"Panel test, {period}", kind="panel-summary", days=s["dates"],
                         value=r2(s["ic"], 3), percentile=r2(s["ic_pos"], 0), contrib_pts=r2(s["spread"], 2),
                         confidence=r2(s["ic_t"], 2), impact_pct=r2(s_late["ic"], 3), action=verdict,
                         text=(f"{s['cases']} cases over {s['dates']} dates; average rank correlation {f2(s['ic'])} (t {f2(s['ic_t'], 1)}), "
                               f"positive on {('n/a' if s['ic_pos'] is None else format(s['ic_pos'], '.0f') + '%')} of dates; top third minus bottom third "
                               f"{f2(s['spread'], 2)} points a window (t {f2(s['spread_t'], 1)}); starting a day later {f2(s_late['ic'])}. "
                               f"Verdict: {verdict}.")))
        if period == "history":
            for key, label in PART_NAMES:
                ps = panel_stats(sub, key=key)
                rows.append(lrow("calib", date=date, name=f"Part: {label}", kind="panel-part", days=ps["dates"],
                                 value=r2(ps["ic"], 3), confidence=r2(ps["ic_t"], 2), percentile=r2(ps["ic_pos"], 0),
                                 text=f"average rank correlation {f2(ps['ic'])} (t {f2(ps['ic_t'], 1)}) over {ps['dates']} dates"))
            for lo, hi, label in PRICE_BANDS:
                g = [o for o in sub if lo <= o["pts"] <= hi]
                rows.append(lrow("calib", date=date, name=label, kind="panel-band", days=len(g),
                                 percentile=r2(sum(1 for o in g if o["ex"] > 0) / len(g) * 100.0, 0) if g else None,
                                 value=r2(sum(o["ex"] for o in g) / len(g), 2) if g else None))
    return rows, summary


def panel_status(panel, hist, bench):
    """Which panel stocks are short of a usable history, and which are behind the benchmark's last session."""
    last_b = (series(hist, bench) or [{"date": ""}])[-1]["date"]
    short, behind = [], []
    for t, d in panel_series(panel, hist).items():
        n = len([x for x in d if x <= last_b])
        lst = max(d) if d else "none"
        if n < 400:
            short.append(f"{t} ({n})")
        elif lst < last_b:
            behind.append(f"{t} (last {lst})")
    return short, behind, last_b


# ---------------------------------------------------------------- earnings drift: beat, raise and follow-through
DRIFT_TESTS = [("beat", "beat on earnings and revenue"), ("raised", "raised guidance"),
               ("reaction", "up 3% or more on the day and 2 points or more ahead of the index"),
               ("held", "closed at or above its open, in the upper half of the day's range"),
               ("volume", "volume at least 1.5 times its 20-day average"),
               ("trend", "above its 50-day average and not in a downtrend")]


def surprise_pct(act, est):
    if act is None or est is None:
        return None
    if est == 0:
        return None
    return (act - est) / abs(est) * 100.0


def drift_eval(d, hist, bench):
    """Tests one reporter's first full session after its results. Returns the figures, each test's result (True,
    False, or None when an input is missing) and the verdict."""
    t, date = d["ticker"], d["date"]
    prev = num(d.get("prev_close"))
    if prev is None:
        before = [r for r in series(hist, t) if r["date"] < date]
        prev = before[-1]["close"] if before else None
    o, h, l, c, v = (num(d.get(k)) for k in ("open", "high", "low", "close", "volume"))
    avgv, ma50, ma200 = num(d.get("avg_vol_20d")), num(d.get("ma50")), num(d.get("ma200"))
    bser = series(hist, bench)
    bi = next((i for i, r in enumerate(bser) if r["date"] == date), None)
    spx = pct(bser[bi]["close"], bser[bi - 1]["close"]) if (bi is not None and bi > 0) else None
    f = {"prev_close": prev, "gap_pct": pct(o, prev), "day_pct": pct(c, prev), "from_open_pct": pct(c, o),
         "range_pos": ((c - l) / (h - l)) if (None not in (c, h, l) and h > l) else None,
         "vol_ratio": (v / avgv) if (v and avgv) else None, "spx_day_pct": spx,
         "vs_50d_pct": pct(c, ma50), "eps_surprise_pct": surprise_pct(num(d.get("eps_actual")), num(d.get("eps_est"))),
         "rev_surprise_pct": surprise_pct(num(d.get("rev_actual")), num(d.get("rev_est"))), "implied_pct": num(d.get("implied_pct"))}
    f["excess_day"] = (f["day_pct"] - spx) if (f["day_pct"] is not None and spx is not None) else None
    g = str(d.get("guidance") or "").strip().lower()
    tests = {}
    es, rs = f["eps_surprise_pct"], f["rev_surprise_pct"]
    tests["beat"] = None if (es is None or rs is None) else (es > 0 and rs >= 0)
    tests["raised"] = None if not g else (g == "raised")
    tests["reaction"] = None if (f["day_pct"] is None or f["excess_day"] is None) else (f["day_pct"] >= 3 and f["excess_day"] >= 2)
    tests["held"] = None if (f["from_open_pct"] is None or f["range_pos"] is None) else (f["from_open_pct"] >= 0 and f["range_pos"] >= 0.5)
    tests["volume"] = None if f["vol_ratio"] is None else f["vol_ratio"] >= 1.5
    tests["trend"] = None if (ma50 is None or c is None) else (c > ma50 and not (ma200 is not None and ma50 < ma200))
    core = tests["beat"] is True and tests["reaction"] is True and tests["trend"] is True
    if core and all(tests[k] is True for k in ("raised", "held", "volume")):
        verdict = "enter"
    elif core:
        verdict = "watch"
    else:
        verdict = "fail"
    f["max_weight"] = (5 if (f["vs_50d_pct"] is not None and f["vs_50d_pct"] > 15) else 10) if verdict == "enter" else None
    if f["implied_pct"] is not None and f["day_pct"] is not None:
        f["beyond_implied"] = abs(f["day_pct"]) > f["implied_pct"]
    return f, tests, verdict


def add_drift(ledger, items, hist, bench, listed_tickers):
    out = []
    for d in items or []:
        if not d.get("ticker") or not d.get("date") or num(d.get("close")) is None:
            warn(f"drift entry {d.get('name') or d.get('ticker')}: needs ticker, date and close; left out")
            continue
        if d["ticker"] not in listed_tickers:            # the reaction-day row, so the five-session window can be settled later
            merge_history(hist, d["ticker"], [{k: d.get(k) for k in ("date", "open", "high", "low", "close", "volume")}])
        f, tests, verdict = drift_eval(d, hist, bench)
        passed = sum(1 for v in tests.values() if v is True)
        miss = [k for k, v in tests.items() if v is None]
        fmt = lambda v, s="%": "n/a" if v is None else f"{v:+.1f}{s}"
        text = (f"{d.get('reported') or 'results'}: EPS {fmt(f['eps_surprise_pct'])} against forecast, revenue {fmt(f['rev_surprise_pct'])}, "
                f"guidance {d.get('guidance') or 'not given'}; gap {fmt(f['gap_pct'])}, open to close {fmt(f['from_open_pct'])}, day {fmt(f['day_pct'])} "
                f"against the index {fmt(f['spx_day_pct'])}; volume {('n/a' if f['vol_ratio'] is None else format(f['vol_ratio'], '.1f') + 'x')} average; "
                f"{('n/a' if f['vs_50d_pct'] is None else format(f['vs_50d_pct'], '+.1f') + '%')} from its 50-day. "
                + "Failed: " + (", ".join(k for k, v in tests.items() if v is False) or "none")
                + (". Missing: " + ", ".join(miss) if miss else "") + (f". {d.get('note')}" if d.get("note") else ""))
        ledger[:] = [r for r in ledger if not (r["table"] == "drift" and r["date"] == d["date"] and r["ticker"] == d["ticker"] and r["beat"] is None)]
        if any(r["table"] == "drift" and r["date"] == d["date"] and r["ticker"] == d["ticker"] for r in ledger):
            continue
        ledger.append(lrow("drift", date=d["date"], name=d.get("name") or d["ticker"], ticker=d["ticker"], kind=verdict,
                           score=passed, value=num(d.get("close")), day_pct=r2(f["day_pct"]), implied_pct=f["implied_pct"],
                           stock=d.get("reported") or "", text=text, weight=f["max_weight"],
                           plan=json.dumps({k: (round(v, 3) if isinstance(v, float) else v) for k, v in f.items()}
                                           | {"tests": tests, "guidance": d.get("guidance") or ""})))
        out.append((d.get("name") or d["ticker"], verdict, passed, tests, f))
    return out


def real_open(row):
    """True when a stored row carries a traded open. Rows added by `closes` hold only a close (open = high = low =
    close, no volume), so their open cannot be used as a fill price."""
    if not row:
        return False
    if row.get("open_obs") is False:                     # version 7.2: the open was never supplied, whatever the volume
        return False
    return not (row.get("volume") is None and row["open"] == row["close"] == row["high"] == row["low"])


def resolve_drift(ledger, hist, bench):
    """The tradable result: bought at the open of the session after the reaction day (the first fill an order can get)
    and valued at the close five sessions after the reaction day, against the index over the same span (ret_pct,
    spx_ret_pct, beat). The version 6 figure, from the reaction day's close, is kept beside it (cum_pct, spx_cum_pct).
    If the next session's open never arrives, the row settles on the close basis after 15 sessions and says so (unit)."""
    bser = series(hist, bench)
    bidx = {r["date"]: i for i, r in enumerate(bser)}
    n = 0
    for r in ledger:
        if r["table"] != "drift" or r["beat"] is not None or r["date"] not in bidx:
            continue
        i = bidx[r["date"]]
        if i + 5 >= len(bser):
            continue
        end = bser[i + 5]["date"]
        ser = series(hist, r["ticker"])
        start = next((x for x in ser if x["date"] == r["date"]), None)
        fin = next((x for x in ser if x["date"] == end), None)
        nxt = next((x for x in ser if x["date"] == bser[i + 1]["date"]), None)
        if not start or not fin:
            if i + 15 < len(bser):
                r["beat"], r["window_end"] = "n/a", end
            continue
        c_ret, cb_ret = pct(fin["close"], start["close"]), pct(bser[i + 5]["close"], bser[i]["close"])
        if real_open(nxt):
            s_ret, b_ret = pct(fin["close"], nxt["open"]), pct(bser[i + 5]["close"], bser[i + 1]["open"])
            basis = "from the next open"
        elif i + 15 < len(bser):                         # version 7.2: no tradable open, so no win or loss
            r["window_end"], r["cum_pct"], r["spx_cum_pct"] = end, r2(c_ret), r2(cb_ret)
            r["unit"], r["beat"] = "next open never supplied: close-basis figure kept, not scored", "n/a"
            n += 1
            continue
        else:
            continue                                    # wait for the next session's full row
        r["window_end"], r["ret_pct"], r["spx_ret_pct"] = end, r2(s_ret), r2(b_ret)
        r["cum_pct"], r["spx_cum_pct"], r["unit"] = r2(c_ret), r2(cb_ret), basis
        r["beat"] = "yes" if s_ret > b_ret else "no"
        n += 1
    return n


def drift_need_open(ledger, hist, bench):
    """Open drift rows whose session after the reaction day has passed but has no traded open stored."""
    bser = series(hist, bench)
    bidx = {r["date"]: i for i, r in enumerate(bser)}
    out = []
    for r in ledger:
        if r["table"] != "drift" or r["beat"] is not None or r["date"] not in bidx:
            continue
        i = bidx[r["date"]]
        if i + 1 >= len(bser):
            continue
        d1 = bser[i + 1]["date"]
        if not real_open(hist.get((r["ticker"], d1))):
            out.append((r["name"], r["ticker"], d1))
    return sorted(set(out))


# ---------------------------------------------------------------- version 7: standstill, results total, reconcile, judgement
def _tick_map(ledger):
    return {r["name"]: r["ticker"] for r in ledger if r["table"] == "position" and r["ticker"]}


def _row_on_or_before(hist, tick, d):
    rows = [r for r in series(hist, tick) if r["date"] <= d]
    return rows[-1] if rows else None


def port_day(w_prev, w_new, d, dprev, hist, tick_of, fills, fdays=None):
    """Weighted return (points) of moving from weights w_prev (held at dprev's close) to w_new on session d, with the
    game's rules: kept weight close over previous close, added weight close over the open (or a stated fill price),
    sold weight open over previous close. `fdays` (version 7.5, from fill_days): a leg that filled on a day that is not
    a benchmark session (a London leg on 26 Nov) is priced at that day's open. Returns (points, missing tickers)."""
    pts, missing = 0.0, set()
    for name in set(w_prev) | set(w_new):
        wp, wn = w_prev.get(name, 0.0), w_new.get(name, 0.0)
        if not wp and not wn:
            continue
        tick = tick_of.get(name)
        cur = hist.get((tick, d)) if tick else None
        prv = _row_on_or_before(hist, tick, dprev) if tick else None
        if not cur or not prv:
            missing.add(tick or name)
            continue
        kept, add_w, sold = min(wp, wn), max(wn - wp, 0.0), max(wp - wn, 0.0)
        frow, fd = fill_row(hist, tick, (fdays or {}).get(name), d, cur) if (add_w or sold) else (cur, d)
        if kept:
            pts += kept * (cur["close"] / prv["close"] - 1.0)
        if add_w:
            if not real_open(frow) and not fills.get((name, fd)):
                missing.add(tick)
                continue
            pts += add_w * (cur["close"] / (fills.get((name, fd)) or frow["open"]) - 1.0)
        if sold:
            if not real_open(frow):
                missing.add(tick)
                continue
            pts += sold * (frow["open"] / prv["close"] - 1.0)
    return pts, missing


def _weights(ledger, d):
    return {n: w for n, (w, t) in live_weights(ledger, d).items()}


def standstill_rows(ledger, hist, bench, date, horizon=5):
    """Two tests of whether changing the order paid, both from stored prices and the game's fill rules.
    change: for each effective date E, the new order and the order before it, each held fixed from E for up to
            `horizon` sessions (the new one filling at E's open); the gap is what the decision added.
    week:   for each week, the actual estimate against the order in force after the week's first session held fixed."""
    meta = {r["name"]: r for r in ledger if r["table"] == "meta"}
    start = (meta.get("start_date") or {}).get("text") or "0000-00-00"
    dates = [r["date"] for r in series(hist, bench) if start <= r["date"] <= date]
    tick_of = _tick_map(ledger)
    fills = {(r["name"], r["effective"]): num(r["value"]) for r in ledger if r["table"] == "position" and num(r["value"])}
    rows = []
    # v7.5: a change whose fill date is not a benchmark session (a London leg on 26 Nov) is judged from the next
    # session, with its legs priced at their own fill-day opens; before, it was left out. Any other date is unchanged.
    sess_of = {}
    for e_raw in {r["effective"] for r in ledger if r["table"] == "trade" and r["effective"]}:
        s_ = e_raw if e_raw in dates else next((x for x in dates if x > e_raw), None)
        if s_ is not None:
            sess_of[e_raw] = s_
    effs = sorted(sess_of)
    for e in effs:
        i = dates.index(sess_of[e])
        if i == 0:
            continue                                    # the first order replaced cash: nothing to compare
        dprev = dates[i - 1]
        w_old, w_new = _weights(ledger, dprev), _weights(ledger, dates[i])
        if not w_old:
            continue
        span = dates[i:i + horizon]
        fd_ = fill_days(ledger, dprev, dates[i])
        v_new = v_old = 1.0
        miss = set()
        prev_d = dprev
        for k, d in enumerate(span):
            a, m1 = port_day(w_old if k == 0 else w_new, w_new, d, prev_d, hist, tick_of, fills, fd_ if k == 0 else None)
            b, m2 = port_day(w_old, w_old, d, prev_d, hist, tick_of, fills)
            miss |= m1 | m2
            v_new *= 1 + a / 100.0
            v_old *= 1 + b / 100.0
            prev_d = d
        eff_pts = (v_new - v_old) * 100.0
        changes = sorted(n for n in set(w_old) | set(w_new) if abs(w_old.get(n, 0) - w_new.get(n, 0)) > 1e-9)
        what = ", ".join(f"{n} {w_old.get(n, 0):g} to {w_new.get(n, 0):g}" for n in changes)
        rows.append(lrow("standstill", date=e, effective=e, kind="change", days=len(span),
                         ret_pct=None if miss else r2((v_new - 1) * 100.0, 3), spx_ret_pct=None if miss else r2((v_old - 1) * 100.0, 3),
                         value=None if miss else r2(eff_pts, 3),
                         confirmed="incomplete" if miss else ("complete" if len(span) == horizon else "running"),
                         window_end=span[-1], name=f"Change for {e}",
                         text=what + (f". Missing prices: {', '.join(sorted(miss))}" if miss else "")))
        x_ = next((r for r in ledger if r["table"] == "expect" and r["effective"] == e), None)    # version 7.4
        if x_ is not None and num(x_["forecast"]) is not None:
            rows[-1]["forecast"] = num(x_["forecast"])
            if rows[-1]["confirmed"] == "complete" and rows[-1]["value"] is not None:
                rows[-1]["surprise"] = r2(rows[-1]["value"] - num(x_["forecast"]), 3)
    perf = {r["date"]: num(r["day_pct"]) for r in ledger if r["table"] == "perf" and r["day_pct"] is not None}
    weeks = {}
    for d in dates:
        y, wk, _ = __import__("datetime").date.fromisoformat(d).isocalendar()
        weeks.setdefault((y, wk), []).append(d)
    for key in sorted(weeks):
        ds = weeks[key]
        i0 = dates.index(ds[0])
        if i0 > 0:                                      # v7.1: the order in force before the week, so a Monday fill is judged
            base_d, priced = dates[i0 - 1], ds
        elif len(ds) >= 2:                              # the first week: nothing before the first order, so start after its fill
            base_d, priced = ds[0], ds[1:]
        else:
            continue
        w0 = _weights(ledger, base_d)
        v_act = v_st = 1.0
        miss = set()
        prev_d = base_d
        for d in priced:
            if d not in perf:
                miss.add("estimate for " + d)
                continue
            v_act *= 1 + perf[d] / 100.0
            b, m = port_day(w0, w0, d, prev_d, hist, tick_of, fills)
            miss |= m
            v_st *= 1 + b / 100.0
            prev_d = d
        n_changes = len([e for e in effs if priced[0] <= e <= ds[-1]])
        rows.append(lrow("standstill", date=ds[0], kind="week", days=len(priced), window_end=ds[-1],
                         ret_pct=None if miss else r2((v_act - 1) * 100.0, 3), spx_ret_pct=None if miss else r2((v_st - 1) * 100.0, 3),
                         value=None if miss else r2((v_act - v_st) * 100.0, 3), name=f"Week from {ds[0]}",
                         confirmed="incomplete" if miss else "complete",
                         text=f"{n_changes} change(s) in the week; standstill = the order in force at the close of {base_d}"
                              + (f". Missing prices: {', '.join(sorted(miss))}" if miss else "")))
    all_b = [r["date"] for r in series(hist, bench) if r["date"] < (dates[0] if dates else "")]
    rows += inception_rows(ledger, hist, dates, tick_of, fills, perf, all_b[-1] if all_b else None)
    return rows


def inception_rows(ledger, hist, dates, tick_of, fills, perf, before=None):
    """v7.1: the first order never changed, from its fill at the open of the first session to the latest session with
    every price, as entered (with its cash) and fully invested (the same stocks scaled to 100%), against the actual
    estimate over the same sessions. Never filled with a guess: the row stops at the last fully priced session."""
    if not dates:
        return []
    w_first = _weights(ledger, dates[0])
    tot = sum(w_first.values())
    if not w_first or tot <= 0:
        return []
    out = []
    for label, w in (("as entered", w_first), ("fully invested", {n: v * 100.0 / tot for n, v in w_first.items()})):
        v_act = v_st = 1.0
        last, n, miss_at = None, 0, None
        prev_d = None
        for k, d in enumerate(dates):
            if d not in perf:
                miss_at = (d, {"estimate for " + d})
                break
            if k == 0:                                  # the first order fills at this session's open
                b, m = port_day({}, w, d, before or d, hist, tick_of, fills)
            else:
                b, m = port_day(w, w, d, prev_d, hist, tick_of, fills)
            if m:
                miss_at = (d, m)
                break
            v_act *= 1 + perf[d] / 100.0
            v_st *= 1 + b / 100.0
            last, n, prev_d = d, n + 1, d
        if last is None:
            continue
        done = last == dates[-1]
        what = ", ".join(f"{nm} {wt:.4g}" for nm, wt in sorted(w.items(), key=lambda x: (-x[1], x[0])))
        out.append(lrow("standstill", date=dates[0], kind="inception", days=n, window_end=last,
                        ret_pct=r2((v_act - 1) * 100.0, 3), spx_ret_pct=r2((v_st - 1) * 100.0, 3),
                        value=r2((v_act - v_st) * 100.0, 3), name=f"Inception, {label}",
                        confirmed="complete" if done else f"priced to {last}",
                        text=(f"first order never changed ({what}" + (f", cash {100 - tot:g}" if label == "as entered" and tot < 100 else "") + ")"
                              + ("" if done else f". Not priced from {miss_at[0]}: missing {', '.join(sorted(miss_at[1]))}"))))
    return out


def standstill_needs(ledger, hist, bench, date, listed, horizon=5):
    """Stocks sold within the last `horizon` sessions that are no longer on the list and lack a row for `date`."""
    dates = [r["date"] for r in series(hist, bench) if r["date"] <= date]
    recent = set(dates[-horizon:])
    out = []
    for r in ledger:
        if r["table"] == "trade" and r["effective"] in recent and (num(r["to_w"]) or 0) < (num(r["from_w"]) or 0):
            t = r["ticker"]
            if t and t not in listed and not hist.get((t, date)):
                out.append((r["name"], t))
    out += [(n, t) for n, t in inception_tickers(ledger) if t not in listed and not hist.get((t, date))]   # v7.1
    return sorted(set(out))


def inception_tickers(ledger):
    """v7.1: (name, ticker) of every stock in the first order, which the inception standstill keeps pricing."""
    meta = {r["name"]: r for r in ledger if r["table"] == "meta"}
    start = (meta.get("start_date") or {}).get("text")
    if not start:
        return []
    tick_of = _tick_map(ledger)
    return sorted((n, tick_of.get(n)) for n in live_weights(ledger, start) if tick_of.get(n))


def _sessions_ahead(date, n):
    """The next n weekdays after `date` (US holidays aside), as YYYY-MM-DD."""
    import datetime as _dt
    d = _dt.date.fromisoformat(date)
    out = []
    while len(out) < n:
        d += _dt.timedelta(days=1)
        if d.weekday() < 5 and d.isoformat() not in US_CLOSED:
            out.append(d.isoformat())
    return out


def results_total(ledger, weights, date, default_move=6.0):
    """Holdings reporting inside the next 5 and 10 sessions: weight x implied move added up (a missing implied move
    counts at default_move). Returns {5: (points, reports, missing), 10: (...)}."""
    out = {}
    for n in (5, 10):
        ahead = set(_sessions_ahead(date, n))
        pts, k, missing = 0.0, 0, []
        for e in ledger:
            if e["table"] == "event" and e["kind"] == "results" and e["stock"] in weights and (e["date"] or "") in ahead and weights[e["stock"]] > 0:
                mv = num(e["implied_pct"])
                if mv is None:
                    missing.append(e["stock"])
                    mv = default_move
                pts += weights[e["stock"]] * mv / 100.0
                k += 1
        out[n] = (pts, k, missing)
    return out


_MONTHS = {m: i + 1 for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])}


def results_date_from_text(text):
    """The date in a stock's free-text next_results ("30 Oct, before US open", "28 Oct (time est.)") as YYYY-MM-DD, or
    None when it names no day ("mid Jan 2027 (est.)" has none). October to December are 2026, other months 2027."""
    import re
    m = re.search(r"\b(\d{1,2})\s+([A-Za-z]{3})[a-z]*\b(?:\s+(20\d\d))?", text or "")
    if not m or m.group(2).lower() not in _MONTHS:
        return None
    mon = _MONTHS[m.group(2).lower()]
    year = int(m.group(3)) if m.group(3) else (2026 if mon >= 10 else 2027)
    try:
        import datetime as _dt
        return _dt.date(year, mon, int(m.group(1))).isoformat()
    except ValueError:
        return None


def missing_results_events(ledger, holdings, date, last="2026-11-27"):
    """Version 7.3 (ChatGPT review, finding 1): holdings whose own next-results text names a date after `date` and up to
    the game's end, with no results event stored for that stock on or after `date`. `holdings` maps name -> text.
    The results total and the page read events only, so such a holding would be left out of both."""
    have = {r["stock"] for r in ledger if r["table"] == "event" and r["kind"] == "results" and (r["date"] or "") > date}
    out = []
    for name, text in sorted(holdings.items()):
        d = results_date_from_text(text)
        if d and date < d <= last and name not in have:
            out.append((name, d, text))
    return out


def us_close_uk(d):
    """The US close (16:00 New York, or the early close in US_EARLY_CLOSE_NY) in UK time on date d, as HH:MM."""
    try:
        import datetime as _dt
        from zoneinfo import ZoneInfo
        ny = _dt.datetime.fromisoformat(d + "T" + US_EARLY_CLOSE_NY.get(d, "16:00")).replace(tzinfo=ZoneInfo("America/New_York"))
        return ny.astimezone(ZoneInfo("Europe/London")).strftime("%H:%M")
    except Exception:  # noqa: BLE001
        return "21:00"


def reconcile(ledger):
    """Sets value_est on every `reported` row to the estimate at the close of the last session on or before its date,
    and returns (row, estimate, gap, read_before_close) for each."""
    perf = sorted((r for r in ledger if r["table"] == "perf" and r["value_est"] is not None), key=lambda r: r["date"])
    out = []
    for r in sorted((r for r in ledger if r["table"] == "reported"), key=lambda r: (r["date"] or "", r["time_uk"] or "")):
        p = [x for x in perf if x["date"] <= (r["date"] or "")]
        if not p or r["value_reported"] is None:
            continue
        est = p[-1]["value_est"]
        r["value_est"] = est
        t = (r["time_uk"] or "").strip()
        early = p[-1]["date"] == r["date"] and len(t) == 5 and t[2] == ":" and t < us_close_uk(r["date"])
        out.append((r, est, num(r["value_reported"]) - est, early))
    return out


def judgement_rows(ledger, hist, bench, date, step=5, min_stocks=8):
    """Do the 40 judgement points add to the 60 price and session points? On settled shadow ratings that store both
    parts, every `step`-th session (so no two windows overlap), rank the stocks by the full score, by each half, and by
    the five-session return against the index; average each rank correlation over the dates."""
    done = [r for r in ledger if r["table"] == "shadow" and r["beat"] in ("yes", "no") and r["plan"]]
    by_date = {}
    for r in done:
        try:
            pr = json.loads(r["plan"])
        except ValueError:
            continue
        if pr.get("quant") is None or pr.get("judg") is None:
            continue
        by_date.setdefault(r["date"], []).append((num(r["score"]), pr["quant"], pr["judg"], r["ret_pct"] - r["spx_ret_pct"]))
    bdates = [r["date"] for r in series(hist, bench)]
    pos = {d: i for i, d in enumerate(bdates)}
    chosen, last = [], None
    for d in sorted(d for d in by_date if d in pos and len(by_date[d]) >= min_stocks):
        if last is None or pos[d] - pos[last] >= step:
            chosen.append(d)
            last = d
    rows = []
    for k, label in ((0, "Full score (100)"), (1, "Price and session points (60)"), (2, "Judgement points (40)")):
        cs = [spearman([x[k] for x in by_date[d]], [x[3] for x in by_date[d]]) for d in chosen]
        m, t, n = mean_t(cs)
        rows.append(lrow("calib", date=date, name=label, kind="judgement", days=n, value=r2(m, 3), confidence=r2(t, 1),
                         text=(f"average rank correlation {m:+.3f} (t {('n/a' if t is None else format(t, '+.1f'))}) over {n} dates"
                               if n else f"no settled dates yet ({len(done)} settled ratings store both parts)")))
    return rows


def drift_rows(ledger, date):
    rows = []
    done = [r for r in ledger if r["table"] == "drift" and r["beat"] in ("yes", "no")]
    for v, label in (("enter", "Drift scan: passed (enter)"), ("watch", "Drift scan: partial (watch)"), ("fail", "Drift scan: failed")):
        g = [r for r in done if r["kind"] == v]
        open_ = len([r for r in ledger if r["table"] == "drift" and r["kind"] == v and r["beat"] is None])
        rows.append(lrow("calib", date=date, name=label, kind="drift", days=len(g),
                         percentile=r2(sum(1 for r in g if r["beat"] == "yes") / len(g) * 100.0, 0) if g else None,
                         value=r2(sum(r["ret_pct"] - r["spx_ret_pct"] for r in g) / len(g), 2) if g else None,
                         text=f"{open_} still inside their five-session window"))
    return rows


def backtest_price_points(hist, bench, skip):
    """For every stock with at least 206 stored closes: the price-only points on each past day against the next five
    sessions' return minus the benchmark's. A rough check, not proof: the stocks were chosen with hindsight and the
    five-day windows overlap."""
    bser = series(hist, bench)
    bidx = {r["date"]: i for i, r in enumerate(bser)}
    bc = [r["close"] for r in bser]
    obs = []
    for t in sorted({k[0] for k in hist}):
        if t == bench or t in skip:
            continue
        ser = [r for r in series(hist, t) if r["date"] in bidx]
        if len(ser) < 206:
            continue
        c = [r["close"] for r in ser]
        for i in range(199, len(ser) - 5):
            j, j5 = bidx[ser[i]["date"]], bidx[ser[i + 5]["date"]]
            if j < 251 and j < i:
                continue
            bsub = [bc[bidx[r["date"]]] for r in ser[:i + 1]]
            pts = price_points(c[:i + 1], bsub)
            obs.append((pts, pct(c[i + 5], c[i]) - pct(bc[j5], bc[j]), t))
    return obs


def calibration_rows(ledger, hist, bench, skip, date):
    rows = []
    done = [r for r in ledger if r["table"] == "shadow" and r["beat"] in ("yes", "no")]
    open_ = len([r for r in ledger if r["table"] == "shadow" and r["beat"] is None])
    for lo, hi, label in SCORE_BANDS:
        g = [r for r in done if r["score"] is not None and lo <= r["score"] <= hi]
        rows.append(lrow("calib", date=date, name=label, kind="live", days=len(g),
                         percentile=r2(sum(1 for r in g if r["beat"] == "yes") / len(g) * 100.0, 0) if g else None,
                         value=r2(sum(r["ret_pct"] - r["spx_ret_pct"] for r in g) / len(g), 2) if g else None,
                         confidence=r2(sum(r["confidence"] for r in g) / len(g), 0) if g else None,
                         text=f"{open_} ratings still inside their five-day window" if lo == 70 else ""))
    obs = backtest_price_points(hist, bench, skip)
    for lo, hi, label in PRICE_BANDS:
        g = [o for o in obs if lo <= o[0] <= hi]
        rows.append(lrow("calib", date=date, name=label, kind="backtest", days=len(g),
                         percentile=r2(sum(1 for o in g if o[1] > 0) / len(g) * 100.0, 0) if g else None,
                         value=r2(sum(o[1] for o in g) / len(g), 2) if g else None,
                         text=(f"{len(obs)} stock-days from {len({o[2] for o in obs})} stocks" if lo == 36 else "")))
    if len(obs) >= 30:
        slope, corr = ols_slope([o[0] for o in obs], [o[1] for o in obs])
        rows.append(lrow("calib", date=date, name="Link between points and the next five sessions", kind="backtest-summary", days=len(obs),
                         value=r2(slope * 10 if slope is not None else None, 2), percentile=r2(corr, 3),
                         text=(f"Correlation {corr:+.3f}; ten more points went with {slope * 10:+.2f} points of extra five-day return. "
                               "Treat with care: the five-day windows overlap and the stocks were picked with hindsight.") if corr is not None else ""))
    return rows, obs


# ---------------------------------------------------------------- commands
def cmd_run(a):
    today = json.load(open(a["today"]))
    ledger = load(a.get("ledger"), [])
    hist = {(r["ticker"], r["date"]): r for r in load(a.get("history"), [])}
    ledger = [{k: r.get(k) for k in LEDGER_KEYS} for r in ledger]
    date = today["date"]
    bench = (today.get("benchmark") or {}).get("ticker") or "SPY"
    mac = {(r["series"], r["date"]): r["value"] for r in load(a.get("macro"), [])}
    mnew = merge_macro(mac, today.get("macro_history"))
    mt = today.get("macro") or {}
    mnew += merge_macro(mac, [{"date": mt.get("date") or date, "series": s_, "value": v_} for s_, v_ in (mt.get("values") or {}).items()])
    oil_proxy = mt.get("oil_proxy") or "OIL"
    revised = {}
    extra = sorted((today.get("extra_history") or {}).items())
    for tick_, rows_ in [(bench, (today.get("benchmark") or {}).get("history"))] + [(s["ticker"], s.get("history")) for s in today["stocks"]] + extra:
        for d_ in merge_history(hist, tick_, rows_):
            revised.setdefault(d_, []).append(tick_)
    bench_rows = series(hist, bench)
    bench_52w = num((today.get("benchmark") or {}).get("change_52w_pct"))
    by_name = {s["name"]: s for s in today["stocks"]}
    panel = load(a.get("panel"), None) if a.get("panel") else None
    panel_new = 0
    if panel is not None:
        members_ = {m["ticker"] for m in panel.get("members") or []}
        pcl_ = panel.setdefault("closes", {})
        for t_, rows_ in sorted((today.get("panel_history") or {}).items()):
            if t_ not in members_:
                warn(f"panel_history for {t_}: not a panel member, left out")
                continue
            have_ = {r_[0]: r_[1] for r_ in pcl_.get(t_, [])}
            for r_ in rows_ or []:
                d_, c_ = str(r_.get("date") or "")[:10], num(r_.get("close"))
                if len(d_) == 10 and c_ and c_ > 0:
                    panel_new += d_ not in have_
                    have_[d_] = c_
            pcl_[t_] = sorted([d_, c_] for d_, c_ in have_.items())
    elif today.get("panel_history"):
        warn("panel_history given but no --panel file: the panel closes were not stored")
    if panel is not None:                        # a panel stock that is also on the list: keep its closes in the panel too
        pcl_ = panel.setdefault("closes", {})
        for m_ in panel.get("members") or []:
            t_ = m_["ticker"]
            ser_ = series(hist, t_)
            if ser_:
                have_ = {r_[0]: r_[1] for r_ in pcl_.get(t_, [])}
                for r_ in ser_:
                    panel_new += r_["date"] not in have_
                    have_[r_["date"]] = r_["close"]
                pcl_[t_] = sorted([d_, c_] for d_, c_ in have_.items())
    if len(by_name) != len(today["stocks"]):
        sys.exit("ERROR: duplicate stock names in today.json")

    # order
    order = today.get("order") or []
    errs, cash = check_order(order)
    for o in order:
        if o["name"] not in by_name:
            errs.append(f"{o['name']} is in the order but not in stocks")
    if errs:
        sys.exit("ERROR in order: " + "; ".join(errs))

    before = {}
    for r in ledger:
        before[r["table"]] = before.get(r["table"], 0) + 1
    perf_before = {r["date"] for r in ledger if r["table"] == "perf"}

    kept_notes = {}
    done_perf = {r["date"] for r in ledger if r["table"] == "perf"}
    ever_held = {r["ticker"] for r in ledger if r["table"] == "position"} | {bench}
    bdates_ = [r["date"] for r in series(hist, bench)]
    def _held_near(d_):                           # v7.1: a row for day d moves the estimate only if the stock was held on d or the session before
        i_ = bdates_.index(d_) if d_ in bdates_ else None
        days_ = [d_] + ([bdates_[i_ - 1]] if i_ else [])
        out_ = {bench}
        for x_ in days_:
            out_ |= {t for n, (w, t) in live_weights(ledger, x_).items()}
        return out_
    revised = {d_: [t_ for t_ in ts_ if t_ in ever_held and t_ in _held_near(d_)] for d_, ts_ in revised.items()}
    revised = {d_: ts_ for d_, ts_ in revised.items() if ts_}
    # v7.5: a corrected row on a day that is not a benchmark session (London on 26 Nov) can change the next session's
    # line, whose fills may use its open, so it counts as a correction to that session. Benchmark dates are unchanged.
    sess_ = lambda d_: d_ if d_ in bdates_ else next((x_ for x_ in bdates_ if x_ > d_), None)
    revised_s = {}
    for d_, ts_ in revised.items():
        if sess_(d_):
            revised_s.setdefault(sess_(d_), []).extend(ts_)
    stale = sorted(d_ for d_ in revised_s if d_ in done_perf)
    if stale:                       # a stored price was corrected after that session was logged: redo from there
        cut = stale[0]
        for r in ledger:
            if r["table"] == "postmortem" and r["date"] and r["date"] >= cut:
                kept_notes[r["name"]] = {"name": r["name"], "text": r["text"], "lesson": r["lesson"]}
            if r["table"] == "confidence" and r["window_end"] and r["window_end"] >= cut:
                r["window_end"] = r["beat"] = r["ret_pct"] = r["spx_ret_pct"] = None
        ledger = [r for r in ledger if not (r["table"] in ("perf", "contrib", "postmortem") and r["date"] and r["date"] >= cut)]
        print(f"RECALCULATED from {cut}: prices arrived late or were corrected for " + ", ".join(f"{d_} ({', '.join(sorted(set(t_)))})" for d_, t_ in sorted(revised_s.items()) if d_ in done_perf))
    for fx in today.get("fixes") or []:
        n, old, new = fx.get("name"), fx.get("old_effective"), fx.get("new_effective")
        hit = 0
        for r in ledger:
            if r["table"] in ("position", "trade", "confidence") and r["name"] == n and r["effective"] == old:
                r["effective"] = new
                hit += 1
                if r["table"] == "position" and "fill_price" in fx:
                    r["value"] = num(fx.get("fill_price"))
                if r["table"] == "confidence":
                    r["window_end"] = r["beat"] = r["ret_pct"] = r["spx_ret_pct"] = None
        if hit:
            cut = min(old, new)
            for r in ledger:
                if r["table"] == "postmortem" and r["date"] and r["date"] >= cut:
                    kept_notes[r["name"]] = {"name": r["name"], "text": r["text"], "lesson": r["lesson"]}
            ledger = [r for r in ledger if not (r["table"] in ("perf", "contrib", "postmortem") and r["date"] and r["date"] >= cut)]
            print(f"FIX applied: {n} fill date {old} -> {new}" + (f", fill price {fx.get('fill_price')}" if "fill_price" in fx else "")
                  + f"; performance from {cut} recalculated")
        else:
            warn(f"fix for {n} ({old} -> {new}) matched nothing")

    # first run: seed meta rows
    if not any(r["table"] == "meta" for r in ledger):
        st = today.get("start") or {}
        ledger.append(lrow("meta", name="start_date", text=st.get("date") or date))
        ledger.append(lrow("meta", name="start_value", value=num(st.get("value")) or 100000.0))
        ledger.append(lrow("meta", name="spy_base", value=num(st.get("spy_base")) or (bench_rows[-1]["open"] if bench_rows else None)))

    # scores
    regime = today.get("regime") or "mixed"
    sc = {}
    for s in today["stocks"]:
        tt = (s.get("stats") or {}).get("trend_ticker")
        trows = series(hist, tt) if tt else None
        if tt and (not trows or trows[-1]["date"] != date):
            warn(f"{s['name']}: no {tt} row for {date}; its trend figures use {trows[-1]['date'] if trows else 'nothing'}")
        sc[s["name"]] = score_stock(s, series(hist, s["ticker"]), bench_rows, bench_52w, regime, trows, date)
    tick_of = {s["name"]: s["ticker"] for s in today["stocks"]}

    # positions and trades (only when the order differs from what is already recorded for its effective date)
    eff = today.get("effective")
    if order and eff:
        n_tr_ = len([r for r in ledger if r["table"] == "trade"])
        ledger = apply_order(ledger, order, eff, today.get("entered") or date, today.get("order_reason") or "",
                             {n: s_["ticker"] for n, s_ in by_name.items()}, {n: x["score"] for n, x in sc.items()})
        ledger = record_expectation(ledger, today.get("order_expected"), eff, today.get("entered") or date,
                                    len([r for r in ledger if r["table"] == "trade"]) > n_tr_, date >= eff)

    if not hist.get((bench, date)):
        warn(f"no {bench} row for {date} in the history store, so performance for that session cannot be added")
    closed_now = {(c_.get("ticker"), c_.get("date")) for c_ in (today.get("market_closed") or []) if c_.get("ticker") and c_.get("date")}
    mc_row = next((r for r in ledger if r["table"] == "meta" and r["name"] == "market_closed"), None)
    try:
        closed_all = {tuple(x) for x in json.loads(mc_row["text"])} if mc_row and mc_row["text"] else set()
    except (ValueError, TypeError):
        closed_all = set()
    if closed_now - closed_all:           # version 7.3: kept, so a later rebuild still knows the market was shut
        closed_all |= closed_now
        if mc_row is None:
            mc_row = lrow("meta", name="market_closed")
            ledger.append(mc_row)
        mc_row["text"] = json.dumps(sorted(list(x) for x in closed_all))
    added = update_performance(ledger, hist, bench, date, closed_all)
    bud0_ = num(today.get("results_budget")) or 0.6
    rb_row = next((r for r in ledger if r["table"] == "meta" and r["name"] == "results_budget"), None)
    if rb_row is None:
        rb_row = lrow("meta", name="results_budget")
        ledger.append(rb_row)
    rb_row["value"] = bud0_               # version 7.3: the budgets in force, for the page
    rb_row["text"] = json.dumps({"default": bud0_, "windows": [{"from": lo, "to": hi, "budget": pts, "why": why}
                                                               for lo, hi, pts, why in RESULTS_BUDGET_WINDOWS]})
    resolved = resolve_confidence(ledger, hist, bench)

    # macro panel, day-ahead call, shadow ratings and calibration
    wts = {o["name"]: num(o["weight"]) or 0.0 for o in order}
    mrows, mfacts, backdrop = macro_panel(mac, hist, date, oil_proxy)
    ana_tick = {}
    for s in today["stocks"]:                       # a London stock with a short history borrows its US-listed line here
        tt_ = (s.get("stats") or {}).get("trend_ticker")
        ana_tick[s["name"]] = tt_ if (tt_ and len(series(hist, s["ticker"])) < 150 <= len(series(hist, tt_))) else s["ticker"]
    mrows += sensitivities(mac, hist, bench, oil_proxy, wts, ana_tick, date)
    crows_, cfacts = crypto_trend(hist, date)
    mrows += crows_
    links = crypto_links(hist, bench, ana_tick, {s["name"]: s.get("theme") for s in today["stocks"]}, date)
    btc_state = (cfacts.get("btc") or {}).get("state")
    for n_, lk_ in links.items():                   # a flag on every crypto-linked stock, naming Bitcoin's trend
        if lk_["linked"]:
            sc[n_]["flags"].append("moves with Bitcoin" + (f", whose trend is {btc_state}" if btc_state else ""))
    target = today.get("next_session") or next_weekday(date)
    call = day_call(hist, mac, bench, oil_proxy, wts, ana_tick, date)
    if call:
        write_day_call(ledger, call, target, date, today.get("daycall"))
    calls_done = resolve_day_calls(ledger, hist, bench)
    for sd_ in today.get("shadow_seed") or []:
        if not any(r["table"] == "shadow" and r["date"] == sd_["date"] and r["name"] == sd_["name"] for r in ledger) and hist.get((sd_["ticker"], sd_["date"])):
            ledger.append(lrow("shadow", date=sd_["date"], name=sd_["name"], ticker=sd_["ticker"], score=num(sd_.get("score")),
                               confidence=num(sd_.get("confidence")), value=hist[(sd_["ticker"], sd_["date"])]["close"],
                               theme=sd_.get("tier") or "", text=sd_.get("flags") or ""))
    add_shadow(ledger, date, sc, tick_of, hist)
    shadow_done = resolve_shadow(ledger, hist, bench)
    drift_new = add_drift(ledger, today.get("drift"), hist, bench, {s["ticker"] for s in today["stocks"]})
    drift_done = resolve_drift(ledger, hist, bench)
    listed = {s["ticker"] for s in today["stocks"]} | {bench, oil_proxy} | set(CRYPTO_PROXY.values()) | ever_held | {(s.get("stats") or {}).get("trend_ticker") for s in today["stocks"]} | {r["ticker"] for r in ledger if r["table"] == "contrib"}
    drift_open = {r["ticker"] for r in ledger if r["table"] == "drift" and r["beat"] is None}
    drift_wait = sorted({(r["name"], r["ticker"], r["date"]) for r in ledger if r["table"] == "drift" and r["beat"] is None
                         and r["ticker"] not in listed and (series(hist, r["ticker"]) or [{"date": ""}])[-1]["date"] < date})
    listed |= drift_open
    waiting = sorted({(r["name"], r["ticker"]) for r in ledger if r["table"] == "shadow" and r["beat"] is None and r["ticker"] not in listed
                      and (series(hist, r["ticker"]) or [{"date": ""}])[-1]["date"] < date})
    pruned = sorted({t_ for (t_, _) in hist if t_ not in listed and not any(r["table"] == "shadow" and r["beat"] is None and r["ticker"] == t_ for r in ledger)})
    for k_ in [k_ for k_ in hist if k_[0] in pruned]:
        del hist[k_]
    skip_bt = {oil_proxy} | set(CRYPTO_PROXY.values()) | {(s.get("stats") or {}).get("trend_ticker") for s in today["stocks"]}
    crows, bt_obs = calibration_rows(ledger, hist, bench, skip_bt, date)
    prows, psum = panel_rows(panel, hist, bench, date) if panel is not None else ([], None)
    crows += prows + drift_rows(ledger, date) + judgement_rows(ledger, hist, bench, date)
    drift_open_need = drift_need_open(ledger, hist, bench)
    still_need = standstill_needs(ledger, hist, bench, date, {s["ticker"] for s in today["stocks"]})
    for n_ in today.get("postmortems") or []:
        kept_notes[n_["name"]] = n_
    closed = add_postmortems(ledger, date, list(kept_notes.values()))

    rep = today.get("reported") or {}
    if num(rep.get("value")) is not None or num(rep.get("rank")) is not None:
        rk, pl = num(rep.get("rank")), num(rep.get("players"))
        key = (rep.get("date") or date, num(rep.get("value")), rk)
        same = [r for r in ledger if r["table"] == "reported" and (r["date"], r["value_reported"], r["rank"]) == key]
        for r in same:                       # version 7.3: a repeat of a stored reading fills in what it adds
            if num(rep.get("top2_return_pct")) is not None:
                r["value"] = num(rep.get("top2_return_pct"))
            if num(rep.get("players")) is not None:
                r["players"] = num(rep.get("players"))
                r["percentile"] = r2(rk / r["players"] * 100.0, 1) if (rk and r["players"]) else r["percentile"]
            if rep.get("note") and rep.get("note") not in (r["text"] or ""):
                r["text"] = ((r["text"] + " ") if r["text"] else "") + rep.get("note")
        if not same:
            ledger.append(lrow("reported", date=rep.get("date") or date, time_uk=rep.get("time_uk"),
                               value_reported=num(rep.get("value")), rank=rk, players=pl,
                               percentile=r2(rk / pl * 100.0, 1) if (rk and pl) else None,
                               value=num(rep.get("top2_return_pct")), text=rep.get("note") or ""))

    # replace-on-every-run tables
    scen_in = today.get("scenarios")
    if not scen_in:                                 # none supplied: rebuild the stored ones on today's weights
        try:
            scen_in = [{"name": r["name"], "shocks": json.loads(r["plan"])} for r in ledger if r["table"] == "scenario" and r["plan"]]
        except ValueError:
            scen_in = []
    risk, corr, themes, scen, port_vol = risk_tables(order, by_name, hist, scen_in, links)
    keep_scen = [r for r in ledger if r["table"] == "scenario"] if not scen_in else []
    ledger = [r for r in ledger if r["table"] not in ("risk", "corr", "theme", "scenario", "macro", "analog", "calib", "standstill")]
    ledger += risk + corr + themes + (scen or keep_scen) + mrows + (call["evidence"] if call else []) + crows
    ledger += standstill_rows(ledger, hist, bench, date)
    recon = reconcile(ledger)
    scen = scen or keep_scen
    for e in today.get("events") or []:
        old_e = next((r for r in ledger if r["table"] == "event" and r["date"] == e.get("date") and r["name"] == e.get("name")), None)
        ledger = [r for r in ledger if r is not old_e]
        if e.get("remove"):
            continue
        if e.get("kind") == "results" and e.get("stock"):
            ledger = [r for r in ledger if not (r["table"] == "event" and r["kind"] == "results"
                                                and r["stock"] == e["stock"] and (r["date"] or "") > date)]
        keep = lambda k_, d_=None: e.get(k_) if e.get(k_) not in (None, "") else ((old_e or {}).get(k_) if old_e else d_)   # a later run can add the actual figure without repeating the rest
        ledger.append(lrow("event", date=e.get("date"), time_uk=keep("time_uk"), name=e.get("name"), stock=keep("stock"),
                           kind=keep("kind"), confirmed=keep("confirmed"), implied_pct=num(keep("implied_pct")),
                           text=keep("text", "") or "", plan=keep("plan", "") or "", last_order=keep("last_order", "") or "",
                           forecast=keep("forecast"), previous=keep("previous"), actual=keep("actual"), surprise=keep("surprise")))
    bidx_ = {r["date"]: i for i, r in enumerate(bench_rows)}
    y10 = mseries(mac, "us10y")
    for r in ledger:                                   # what the market did on the day of each macro release
        if r["table"] == "event" and r["kind"] == "macro" and r["date"] in bidx_ and bidx_[r["date"]] > 0:
            i_ = bidx_[r["date"]]
            r["spx_ret_pct"] = r2(pct(bench_rows[i_]["close"], bench_rows[i_ - 1]["close"]))
            y0_, y1_ = dict(y10).get(r["date"]), lookup_le(y10, bench_rows[i_ - 1]["date"])      # no figure that day (bond market shut): left blank
            r["chg_1d"] = r2((y0_ - y1_) * 100.0, 1) if (y0_ is not None and y1_ is not None) else None
    seen = {(r["date"], r["stock"], r["bank"], r["action"]) for r in ledger if r["table"] == "revision"}
    for v in today.get("revisions") or []:
        if (v.get("date"), v.get("stock"), v.get("bank"), v.get("action")) not in seen:
            ledger.append(lrow("revision", date=v.get("date"), stock=v.get("stock"), bank=v.get("bank"),
                               action=v.get("action"), text=v.get("text") or ""))
    seen = {(r["date"], r["time_uk"], r["stock"], r["text"]) for r in ledger if r["table"] == "alert"}
    for v in today.get("alerts") or []:
        if (v.get("date"), v.get("time_uk"), v.get("stock"), v.get("text")) not in seen:
            ledger.append(lrow("alert", date=v.get("date"), time_uk=v.get("time_uk"), stock=v.get("stock"), text=v.get("text") or ""))

    # stocks.json for the page
    weights = {o["name"]: num(o["weight"]) or 0.0 for o in order}
    confs = {o["name"]: num(o.get("confidence")) for o in order}
    risk_share = {r["name"]: r["risk_share_pct"] for r in risk}
    last_contrib = {r["name"]: r["contrib_pts"] for r in ledger if r["table"] == "contrib" and r["date"] == date}
    perf_today = next((r for r in ledger if r["table"] == "perf" and r["date"] == date), None)
    common = {"order_for": today.get("order_for") or "", "regime": today.get("regime_label") or regime,
              "prices_as_of": today.get("prices_as_of") or date, "scores_as_of": today.get("prices_as_of") or date,
              "today_est_pct": perf_today["day_pct"] if perf_today else None}
    rows = []
    for s in today["stocks"]:
        x, n = sc[s["name"]], s["name"]
        held = weights.get(n, 0.0) > 0
        row = {k: None for k in STOCK_KEYS}
        row.update({"tier": tier_of(x["score"], x["flags"]), "added": s.get("added") or date,
                    "trend_ticker": (s.get("stats") or {}).get("trend_ticker")})
        row.update({"name": n, "ticker": s["ticker"], "market": s.get("market") or "US", "theme": s.get("theme") or "Other",
                    "group": "Portfolio" if held else "Watchlist", "weight": weights.get(n) if held else None,
                    "confidence": confs.get(n) if held else None, "currency": s.get("currency") or "USD",
                    "status": "Holding" if held else ("Watching" if (s.get("status") or "Holding") == "Holding" else s["status"]), "note": s.get("note") or "",
                    "link": s.get("link") or "", "next_results": (s.get("quote") or {}).get("next_results") or "",
                    "flags": "; ".join(x["flags"]), "spark": x["spark"],
                    "risk_share_pct": risk_share.get(n) if held else None, "contrib_pts": last_contrib.get(n) if held else None,
                    "live_from": position_start(ledger, n, "9999-12-31") if held else None})
        if held:
            row["fill_price"] = next((num(r["value"]) for r in ledger if r["table"] == "position" and r["name"] == n
                                      and r["effective"] == row["live_from"] and num(r["value"])), None)
        for k in ("price", "day_chg", "day_pct", "gap_pct", "from_open_pct", "five_day_pct", "month_pct", "vs_20d_pct",
                  "vs_50d_pct", "off_high_pct", "rsi", "atr_pct", "target", "upside_pct", "vs_200d_pct", "ma10", "ma20",
                  "ma100", "ema10", "ema20", "ema50", "ema200", "ma50", "ma200", "change_52w_pct", "trend_price"):
            row[k] = r2(x[k])
        for k in ("ema_stack", "cross", "ma_source"):
            row[k] = x[k]
        lk = links.get(n) or {}
        for k in ("btc_beta", "btc_corr", "btc_net", "eth_beta", "eth_corr"):
            row[k] = r2(lk.get(k))
        row["crypto_days"] = lk.get("crypto_days")
        row["crypto_link"] = "yes" if lk.get("linked") else ("" if links else None)
        for k in ("score", "trend_pts", "short_pts", "catalyst_pts", "revisions_pts", "weight_cap_pct"):
            row[k] = x[k]
        q_, st_ = s.get("quote") or {}, s.get("stats") or {}
        row.update({"week52_high": r2(x["week52_high"]) if x["week52_high"] is not None else num(q_.get("week52_high")), "week52_low": num(q_.get("week52_low")),
                    "avg_vol_20d": r2(x["avg_vol_20d"], 0),
                    "catalyst_note": s.get("catalyst_note") or "", "revisions_note": s.get("revisions_note") or ""})
        row.update(common)
        rows.append(row)
    cash_row = {k: None for k in STOCK_KEYS}
    cash_row.update({"name": "Cash", "ticker": "", "market": "", "group": "Cash", "theme": "Cash", "weight": cash,
                     "currency": "", "status": "Cash", "note": today.get("cash_note") or "", "link": "", "flags": "",
                     "spark": "", "next_results": ""})
    cash_row.update(common)
    rows.append(cash_row)

    after = {}
    for r in ledger:
        after[r["table"]] = after.get(r["table"], 0) + 1
    for t in ("meta", "trade", "reported", "revision", "alert", "daycall", "shadow", "drift"):
        if after.get(t, 0) < before.get(t, 0):
            sys.exit(f"ERROR: the new ledger would lose {t} rows ({before.get(t)} -> {after.get(t, 0)}); nothing written")
    if not perf_before <= {r["date"] for r in ledger if r["table"] == "perf"}:
        sys.exit("ERROR: the new ledger would lose performance days; nothing written")
    ledger.sort(key=lambda r: (r["table"], r["date"] or r["effective"] or "", r["time_uk"] or ""))
    used = {}
    for r in ledger:                                   # a unique key per row, for the page's tables
        base = ":".join(str(x) for x in (r["table"], r["date"] or r["effective"] or "", r["name"] or r["stock"] or "") if x != "")
        used[base] = used.get(base, 0) + 1
        r["id"] = base if used[base] == 1 else f"{base}:{used[base]}"

    os.makedirs(a["out"], exist_ok=True)
    json.dump(rows, open(os.path.join(a["out"], "stocks.json"), "w"), indent=1)
    json.dump(ledger, open(os.path.join(a["out"], "ledger.json"), "w"), separators=(",", ":"))
    hrows = sorted(hist.values(), key=lambda r: (r["ticker"], r["date"]))
    json.dump(hrows, open(os.path.join(a["out"], "history.json"), "w"), separators=(",", ":"))
    mout = [{"date": d_, "series": s_, "value": v_} for (s_, d_), v_ in sorted(mac.items(), key=lambda kv: (kv[0][0], kv[0][1]))]
    json.dump(mout, open(os.path.join(a["out"], "macro.json"), "w"), separators=(",", ":"))
    json.dump({n: x for n, x in sc.items()}, open(os.path.join(a["out"], "scores.json"), "w"), indent=1)
    if panel is not None:
        json.dump(panel, open(os.path.join(a["out"], "panel.json"), "w"), separators=(",", ":"))

    # ---- printed summary
    f = lambda v, w=7, d=2: ("" if v is None else (f"{v:.{d}f}" if isinstance(v, float) else str(v))).rjust(w)
    print(f"Pipeline version {PIPELINE_VERSION}. Session {date}; order effective {eff}; regime {regime}; {len(hrows)} history rows")
    print("\nSCORES (highest first)")
    print("Stock".ljust(20) + "  Wt Score Anchor Trend Short Cat Rev  vs50d% offHigh%   RSI  ATR% Cap  Tier      EMAs   Flags")
    for n, x in sorted(sc.items(), key=lambda kv: -kv[1]["score"]):
        print(n[:19].ljust(20) + f(weights.get(n) or None, 4, 0) + f(x["score"], 6) + f(x["confidence_anchor"], 7) + f(x["trend_pts"], 6)
              + f(x["short_pts"], 6) + f(int(x["catalyst_pts"]), 4) + f(int(x["revisions_pts"]), 4) + f(x["vs_50d_pct"])
              + f(x["off_high_pct"], 9) + f(x["rsi"], 6, 1) + f(x["atr_pct"], 6) + f(x["weight_cap_pct"], 4) + "  "
              + tier_of(x["score"], x["flags"]).ljust(10) + (x["ema_stack"] or "-").ljust(7) + "; ".join(x["flags"]))
        if x["data_gaps"]:
            print("      data gaps: " + ", ".join(x["data_gaps"]))
    print(f"\nORDER check passed: {len([w for w in weights.values() if w > 0])} stocks, cash {cash:g}%")
    for n, w in weights.items():
        x = sc[n]
        notes = []
        if x["weight_cap_pct"] and w > x["weight_cap_pct"]: notes.append(f"above volatility cap {x['weight_cap_pct']}%")
        if x["score"] < 45: notes.append("score below 45")
        if any(fl.startswith("downtrend") for fl in x["flags"]): notes.append("downtrend")
        lk = links.get(n) or {}
        if lk.get("linked") and w > 0 and btc_state == "down": notes.append("crypto-linked while Bitcoin's trend is down")
        if lk.get("linked") and w > 10: notes.append(f"crypto-linked at {w:g}%, above the 10% maximum for such a stock")
        if notes: print(f"  NOTE {n}: " + ", ".join(notes))
    cw = sum(w for n, w in weights.items() if (links.get(n) or {}).get("linked"))
    if cw > 15: print(f"  NOTE: crypto-linked holdings total {cw:g}%, above the 15% guide")
    nheld = len([w for w in weights.values() if w > 0])
    if not 6 <= nheld <= 10: print(f"  NOTE: {nheld} holdings; the usual range is 6 to 10")
    for n, w in weights.items():
        if w > 20: print(f"  NOTE {n}: weight {w:g}% is above the usual 20% maximum")
    for r in themes:
        if r["name"] != "Cash" and r["weight"] > 45: print(f"  NOTE theme {r['name']}: {r['weight']:g}% is above the 45% guide")
    bud0 = num(today.get("results_budget")) or 0.6
    for e in (r for r in ledger if r["table"] == "event" and r["kind"] == "results" and r["stock"] in weights):
        if e["date"] > date and e["implied_pct"] is not None:
            risk_pts = weights[e["stock"]] * e["implied_pct"] / 100.0
            bud = results_budget_for(e["date"], bud0)
            tag = f"ABOVE the {bud:g} budget" if risk_pts > bud + 1e-9 else f"within the {bud:g} budget"
            print(f"  RESULTS {e['stock']} {e['date']}: weight {weights[e['stock']]:g}% x implied move {e['implied_pct']:g}% = {risk_pts:.2f} points, {tag}")
        elif e["date"] > date:
            print(f"  RESULTS {e['stock']} {e['date']}: no implied move stored yet")
    for n_, (pts_, k_, miss_) in results_total(ledger, weights, date).items():
        if k_:
            print(f"  RESULTS TOTAL next {n_} sessions: {pts_:.2f} points across {k_} report(s)"
                  + (f"; no implied move yet for {', '.join(miss_)} (counted at an assumed 6%, not a market estimate)" if miss_ else ""))
    held_text = {n_: ((by_name.get(n_) or {}).get("quote") or {}).get("next_results") or "" for n_, w_ in weights.items() if w_ > 0}
    for n_, d_, t_ in missing_results_events(ledger, held_text, date):
        warn(f"{n_} is held and its stock data says results on {d_} (\"{t_}\"), but no results event is stored, so RESULTS TOTAL "
             f"and the page leave it out: add it under events (kind \"results\") with its time and implied move")
        print(f"  RESULTS MISSING {n_}: results {d_} per its stock data, but no results event; it is not in RESULTS TOTAL")
    evs = sorted((r for r in ledger if r["table"] == "event"), key=lambda r: (r["date"] or "", r["time_uk"] or ""))
    print("\nEVENTS ahead (use these exact names to update one):")
    for r in [r for r in evs if (r["date"] or "") > date][:10]:
        print(f"    {r['date']} {r['time_uk'] or ''} | {r['name']} | {r['kind']}" + (f" | forecast {r['forecast']}" if r["forecast"] else "") + (f" | implied move {r['implied_pct']:g}%" if r["implied_pct"] is not None else ""))
    for r in [r for r in evs if r["kind"] == "macro" and (r["date"] or "") <= date and (r["date"] or "") >= (bench_rows[-6]["date"] if len(bench_rows) > 6 else "")]:
        if r["actual"]:
            print(f"    RELEASE {r['date']} | {r['name']} | actual {r['actual']} against forecast {r['forecast'] or 'n/a'} | S&P 500 {r['spx_ret_pct'] if r['spx_ret_pct'] is not None else 'n/a'}% that day, 10-year yield {r['chg_1d'] if r['chg_1d'] is not None else 'n/a'}bp")
        elif r["forecast"] or r["previous"]:
            print(f"    NEEDS ACTUAL {r['date']} | {r['name']} | forecast {r['forecast'] or 'n/a'}")
    print("\nTHEMES: " + ", ".join(f"{r['name']} {r['weight']:g}%" for r in themes))
    if port_vol is not None:
        print(f"RISK: estimated daily volatility {port_vol:.2f}% of the portfolio; share of risk by position: "
              + ", ".join(f"{r['name']} {r['risk_share_pct']:g}%" for r in sorted(risk, key=lambda r: -(r['risk_share_pct'] or 0))))
    for r in scen:
        print(f"SCENARIO {r['name']}: {r['impact_pct']:+.2f}% ({r['text']})")
    if added:
        for d in added:
            p_ = next(r for r in ledger if r["table"] == "perf" and r["date"] == d)
            print(f"PERFORMANCE {d}: day {p_['day_pct']:+.3f}%, value {p_['value_est']:.0f}, since start {p_['cum_pct']:+.3f}% vs S&P 500 {p_['spx_cum_pct']:+.3f}%")
            for c in sorted((r for r in ledger if r["table"] == "contrib" and r["date"] == d), key=lambda r: -(r["contrib_pts"] or 0)):
                print(f"    {c['name'][:18].ljust(19)} weight {c['weight']:g}% x return {c['ret_pct'] if c['ret_pct'] is not None else 0:+.2f}% = {c['contrib_pts']:+.3f} points")
    else:
        print("PERFORMANCE: no new session to add")
    for x_ in INCOMPLETE:
        print(f"PERFORMANCE INCOMPLETE {x_}. This session and any later one are not recorded until the row is given (or the market listed under market_closed)")
    reps = sorted((r for r in ledger if r["table"] == "reported" and r["percentile"] is not None), key=lambda r: (r["date"], r["time_uk"] or ""))
    if reps:
        r_ = reps[-1]
        print(f"RANK (reported {r_['date']}): {int(r_['rank'])} of {int(r_['players'])}, top {r_['percentile']:g}%; the top 2% needs {int(r_['players'] * 0.02)} or better. "
              + ("Inside the target: protect it." if r_["percentile"] <= 2 else "Outside the target: keep risk on within the guardrails."))
    for r_, est_, gap_, early_ in recon[-4:]:
        print(f"RECONCILE {r_['date']} {r_['time_uk'] or ''}: FT {r_['value_reported']:.0f} against the estimate {est_:.0f} at the close, "
              f"gap {gap_:+.0f} credits ({gap_ / est_ * 100:+.2f}%)" + (" (read before the US close: not comparable)" if early_ else ""))
    ss_ = [r for r in ledger if r["table"] == "standstill"]
    if ss_:
        print("STANDSTILL (what changing the order added against not changing it; points of the portfolio):")
        sel_ = (sorted((r for r in ss_ if r["kind"] == "change"), key=lambda r: r["date"])[-5:]
                + sorted((r for r in ss_ if r["kind"] == "week"), key=lambda r: r["date"])[-3:]
                + [r for r in ss_ if r["kind"] == "inception"])
        for r in sel_:
            v_ = "not priced" if r["value"] is None else f"{r['value']:+.3f}"
            print(f"    {r['name'][:26].ljust(27)} {v_} over {r['days']} session(s), {r['confirmed']}; {r['text']}"
                  + (f"; expected {r['forecast']:+.3f}" if r["forecast"] is not None else ""))
    for l_ in expectation_lines(ledger):
        print(l_)
    if still_need: print("STANDSTILL NEEDS today's row under extra_history for stocks sold in the last five sessions or in the first order "
                         "and no longer on the list: " + ", ".join(f"{n_} ({t_})" for n_, t_ in still_need))
    if resolved: print(f"CONFIDENCE: {resolved} rating(s) resolved")
    src_n = {}
    for x in sc.values():
        src_n[x["ma_source"]] = src_n.get(x["ma_source"], 0) + 1
    print("AVERAGES: " + ", ".join(f"{v} from {k}" for k, v in sorted(src_n.items())) + ". Short of 200 stored closes: "
          + (", ".join(f"{n} ({x['closes_stored']})" for n, x in sc.items() if x["ma_source"] != "stored prices") or "none"))
    wl = sorted(((n, x) for n, x in sc.items() if not weights.get(n)), key=lambda kv: -kv[1]["score"])
    print(f"\nWATCHLIST: {len(wl)} names (keep it to about 20). "
          + "; ".join(f"{t_}: " + (", ".join(f"{n} {x['score']}" for n, x in wl if tier_of(x['score'], x['flags']) == t_) or "none") for t_ in ("strong", "middling", "weak")))
    soon = {r["stock"] for r in ledger if r["table"] == "event" and r["kind"] == "results" and date < (r["date"] or "") <= next_weekday(next_weekday(next_weekday(next_weekday(next_weekday(date)))))}
    keep_ = [n for n, x in wl if str(by_name[n].get("note") or "").startswith("Crypto tracker")]
    out_ = [n for n, x in wl if tier_of(x["score"], x["flags"]) == "weak" and n not in soon and n not in keep_]
    if out_: print("  ROTATE OUT candidates (weak, no results inside five sessions): " + ", ".join(out_))
    if keep_: print("  KEPT whatever they score (their notes start \"Crypto tracker:\"): " + ", ".join(keep_))
    fit_ = portfolio_fit({n_: w_ for n_, w_ in weights.items() if w_ > 0}, [n for n, x in wl if tier_of(x["score"], x["flags"]) == "strong"],
                         ana_tick, hist, {s_["name"]: s_.get("theme") or "Other" for s_ in today["stocks"]})
    if fit_:                                          # v7.5: printed only; it changes no file
        print("  PORTFOLIO FIT of the strong names (a high score is not a reason by itself: what does the stock add to this order?):")
        for n_, f_ in fit_:
            print(f"    {n_[:22].ljust(23)} score {sc[n_]['score']:>3}  {f_['theme']} (now {f_['theme_w']:g}% of the order)  "
                  f"correlation with the order {f_['corr']:+.2f}, highest {f_['best']:+.2f} with {f_['best_name']} ({f_['n']} sessions)"
                  + ("  SAME RISK AS A HOLDING: a swap, not an addition" if f_["best"] >= 0.8 else ""))
    print(f"\nMACRO ({mnew} new figures): backdrop for shares is {backdrop.upper()}")
    for r in mrows:
        if r["kind"] in ("yield", "commodity", "spread", "crypto"):
            u = r["unit"]
            fm = lambda v: "n/a" if v is None else (f"{v:+.0f}bp" if u == "bp" else f"{v:+.1f}%")
            vt_ = f"{r['value']:>9.4f}" if (r["kind"] == "crypto" and r["value"] < 10) else f"{r['value']:>9.2f}"
            print(f"    {r['name'][:30].ljust(31)} {vt_}   1 day {fm(r['chg_1d'])}, 5 days {fm(r['chg_5d'])}, 20 days {fm(r['chg_20d'])}" + (f"   [{r['text']}]" if r["text"] else ""))
    for r in mrows:
        if r["kind"] in ("backdrop", "sensitivity"):
            print("    " + r["text"])
    if cfacts or links:
        print("\nCRYPTO: " + (f"Bitcoin's trend is {btc_state.upper()}." if btc_state else "no trend reading yet (it needs 50 closes of the IBIT fund)."))
        for k_ in CRYPTO_PROXY:
            if k_ in cfacts:
                print("    " + cfacts[k_]["text"])
        ln_ = sorted(((n_, lk_) for n_, lk_ in links.items() if lk_.get("btc_beta") is not None), key=lambda kv: -(kv[1].get("btc_corr") or 0))
        show_ = [(n_, lk_) for n_, lk_ in ln_ if lk_["linked"] or weights.get(n_)] or ln_[:3]
        if show_:
            print("    MOVES WITH BITCOIN (the move that has gone with a 1% move in Bitcoin; crypto-linked stocks and holdings):")
        for n_, lk_ in show_:
            z_ = lambda v_: round(v_, 2) + 0.0
            print(f"    {n_[:19].ljust(20)} {z_(lk_['btc_beta']):+.2f}% (correlation {z_(lk_['btc_corr']):+.2f} over {lk_['crypto_days']} sessions"
                  + (f"; {z_(lk_['btc_net']):+.2f}% with the S&P 500 allowed for" if lk_.get("btc_net") is not None else "")
                  + (f"; Ether {z_(lk_['eth_beta']):+.2f}%, correlation {z_(lk_['eth_corr']):+.2f}" if lk_.get("eth_beta") is not None else "") + ")"
                  + ("  CRYPTO-LINKED" if lk_["linked"] else "") + (f"  held at {weights[n_]:g}%" if weights.get(n_) else ""))
        short_ = [n_ for n_, lk_ in links.items() if lk_["linked"] and lk_.get("btc_beta") is None]
        if short_: print("    No measured link yet (fewer than 30 sessions stored) for: " + ", ".join(short_))
    if call:
        ft_ = call["features"]
        print(f"\nDAY CALL for {target} (from {call['sample']} sessions since {call['from']}; today: S&P {ft_['r1']:+.2f}% on the day and {ft_['r5']:+.2f}% over five, "
              f"{ft_['dist20']:+.2f}% from its 20-day average, 10-year yield {ft_['dy1']:+.0f}bp on the day and {ft_['dy5']:+.0f}bp over five, oil {ft_['o1']:+.1f}% and {ft_['o5']:+.1f}%)")
        for who in ("S&P 500", "Portfolio"):
            row_ = next((r for r in ledger if r["table"] == "daycall" and r["date"] == target and r["name"] == who), None)
            if row_ and who in call:
                print(f"    {who}: {row_['kind'].upper()} {row_['confidence']}% chance of an up day (model {row_['score']:.0f}, usual rate {row_['percentile']:.0f}, reviewer {row_['adj_eve']:+g}). {row_['action']}. Nearest days: {', '.join(call[who]['dates'])}")
            elif who not in call:
                print(f"    {who}: NO FIGURE on these weights: less than 70% of the invested weight has a year of stored prices."
                      + (f" The stored row ({row_['kind']} {row_['confidence']}%) is from an earlier run on other weights." if row_ else ""))
        for e in call["evidence"]:
            print(f"    {e['kind'].upper().ljust(7)} {e['name']}: {e['text']}")
        if not (today.get("daycall") or {}).get("bull"):
            print("    Write the bull case and the bear case into today.json under \"daycall\" and run again.")
    else:
        print("\nDAY CALL: none made. " + (f"There is no {bench} row for {date} yet." if not hist.get((bench, date)) else
              "It needs a row for the session and at least 140 earlier sessions for the benchmark, the US 10-year yield and oil."))
    if calls_done: print(f"DAY CALLS settled: {calls_done}")
    dc = [r for r in ledger if r["table"] == "daycall" and r["beat"] in ("yes", "no") and r["name"] == "S&P 500"]
    if dc: print(f"DAY CALL RECORD (S&P 500): {len([r for r in dc if r['beat'] == 'yes'])} right of {len(dc)}")
    if waiting: print("SHADOW: to settle the ratings of stocks no longer on the list, give their latest daily rows under extra_history (one history page each): "
                      + ", ".join(f"{n_} ({t_})" for n_, t_ in waiting))
    if pruned: print("PRUNED the stored prices of stocks no longer on the list: " + ", ".join(pruned))
    print(f"\nCALIBRATION: {shadow_done} shadow rating(s) settled this run; {len([r for r in ledger if r['table'] == 'shadow'])} logged in all")
    for r in crows:
        if r["kind"] == "judgement":
            print(f"    JUDGEMENT TEST {r['name'].ljust(30)} {r['text']}")
    for r in crows:
        if r["days"] and r["kind"] in ("live", "backtest", "backtest-summary"):
            if r["kind"] == "backtest-summary": print("    BACKTEST (stocks picked with hindsight) " + r["text"])
            else: print(f"    {r['kind'].upper().ljust(9)} {r['name'].ljust(20)} {r['days']:>5} cases, beat the index {r['percentile']:.0f}% of the time, average gap {r['value']:+.2f} points")
    if panel is not None:
        short_, behind_, lb_ = panel_status(panel, hist, bench)
        print(f"\nPANEL TEST ({len(panel.get('members') or [])} stocks fixed on {panel.get('frozen')}; {panel_new} new closes stored this run; "
              "the measure and the verdict rule were fixed before any panel data was seen)")
        for r in crows:
            if r["kind"] == "panel-summary":
                print(f"    {r['name'].upper()}: {r['text']}")
        parts_ = [r for r in crows if r["kind"] == "panel-part" and r["days"]]
        if parts_:
            print("    BY PART (history): " + "; ".join(f"{r['name'][6:]} {('n/a' if r['value'] is None else format(r['value'], '+.3f'))} (t {('n/a' if r['confidence'] is None else format(r['confidence'], '+.1f'))})" for r in parts_))
        for r in crows:
            if r["kind"] == "panel-band" and r["days"]:
                print(f"    BAND (history) {r['name'].ljust(16)} {r['days']:>5} cases, beat the index {r['percentile']:.0f}% of the time, average gap {r['value']:+.2f} points")
        if short_: print("    PANEL NEEDS a two-year history (fewer than 400 closes stored): " + ", ".join(short_))
        if behind_: print(f"    PANEL BEHIND {lb_}: " + ", ".join(behind_))
    if drift_new or any(r["table"] == "drift" for r in ledger):
        print("\nDRIFT SCAN")
        for n_, v_, p_, t_, f_ in drift_new:
            print(f"    {n_[:22].ljust(23)} {v_.upper().ljust(6)} {p_} of 6 tests passed"
                  + (f"; at most {f_['max_weight']}%" if f_.get("max_weight") else "")
                  + "; " + ", ".join(f"{k} {'yes' if t_[k] is True else 'no' if t_[k] is False else 'missing'}" for k, _ in DRIFT_TESTS))
        for r in crows:
            if r["kind"] == "drift":
                print(f"    RECORD {r['name'].ljust(30)} {r['days']:>3} settled" + (f", beat the index {r['percentile']:.0f}% of the time, average gap {r['value']:+.2f} points" if r["days"] else "") + f"; {r['text']}")
        if drift_done: print(f"    {drift_done} drift window(s) settled this run")
        if drift_wait: print("    DRIFT WAITING for prices (give closes from the reaction date under extra_history): "
                             + ", ".join(f"{n_} ({t_}, from {d_})" for n_, t_, d_ in drift_wait))
        if drift_open_need: print("    DRIFT NEEDS the full row (open, high, low, close, volume) from the history page for the session after the reaction day: "
                                  + ", ".join(f"{n_} ({t_}, {d_})" for n_, t_, d_ in drift_open_need))
    if closed: print("POST-MORTEMS added for: " + ", ".join(closed))
    for w_ in WARN:
        print("WARNING: " + w_)


def cmd_refresh(a):
    rows = json.load(open(a["stocks"]))
    q = json.load(open(a["quotes"]))
    quotes, today = q.get("quotes") or {}, q.get("date")
    keys = set(rows[0].keys())
    total, have, noq = 0.0, False, []
    for r in rows:
        x = quotes.get(r.get("ticker") or "")
        if r["group"] == "Portfolio" and quotes and (not x or num(x.get("price")) is None):
            r["contrib_pts"] = None
            noq.append(r["name"])
        if r["group"] == "Cash" or not x:
            continue
        price, prev, opn = num(x.get("price")), num(x.get("prev_close")), num(x.get("open"))
        if price is None:
            continue
        r["price"] = r2(price)
        r["day_chg"] = r2(price - prev) if prev is not None else None
        r["day_pct"], r["gap_pct"], r["from_open_pct"] = r2(pct(price, prev)), r2(pct(opn, prev)), r2(pct(price, opn))
        if num(r.get("target")) is not None:
            r["upside_pct"] = r2(pct(num(r["target"]), price))
        if r["group"] == "Portfolio" and num(r.get("weight")):
            base = (num(r.get("fill_price")) or opn) if (r.get("live_from") and today and r["live_from"] == today) else prev
            if r.get("live_from") and today and r["live_from"] > today:
                r["contrib_pts"] = None                      # not bought yet
                continue
            move = pct(price, base) or 0.0
            r["contrib_pts"] = r2(num(r["weight"]) * move / 100.0, 3)
            total += r["contrib_pts"]
            have = True
    for r in rows:
        if quotes:
            r["prices_as_of"] = q.get("prices_as_of") or r.get("prices_as_of")
        if "today_est_pct" in r:
            r["today_est_pct"] = r2(total, 3) if have else r.get("today_est_pct")
    assert all(set(r.keys()) == keys for r in rows), "field sets differ between rows"
    os.makedirs(a["out"], exist_ok=True)
    json.dump(rows, open(os.path.join(a["out"], "stocks.json"), "w"), indent=1)
    if noq:
        print("NO QUOTE for holdings: " + ", ".join(noq) + ". They are left out of the weighted move so far.")
    if a.get("ledger"):
        ledger = [{k: r.get(k) for k in LEDGER_KEYS} for r in json.load(open(a["ledger"]))]
        mn = q.get("macro_now") or {}
        n_live = 0
        for r in ledger:                           # latest reading beside the last daily figure
            v = num((mn.get("values") or {}).get(r["ticker"])) if r["table"] == "macro" else None
            if v is None or r["value"] is None:
                continue
            r["live"] = v
            r["live_chg"] = r2((v - r["value"]) * 100.0, 1) if r["kind"] == "yield" else r2(pct(v, r["value"]), 2)
            r["time_uk"] = mn.get("as_of") or ""
            n_live += 1
        if mn:
            print(f"MACRO: {n_live} live readings stored ({mn.get('as_of') or 'no time given'})")
            for r in ledger:
                if r["table"] == "macro" and r["live"] is not None and r["time_uk"] == (mn.get("as_of") or ""):
                    print(f"    {r['name'][:30].ljust(31)} {r['live']:>9.2f}  ({r['live_chg']:+g}{'bp' if r['kind'] == 'yield' else '%'} against the last daily figure of {r['value']:g})")
            b_ = next((r for r in ledger if r["table"] == "macro" and r["ticker"] == "btc" and r["live_chg"] is not None
                       and r["time_uk"] == (mn.get("as_of") or "")), None)
            for r in rows if b_ else []:
                if r.get("crypto_link") == "yes" and num(r.get("btc_beta")) is not None:
                    print(f"    CRYPTO {r['name']}: Bitcoin is {b_['live_chg']:+g}% against its last stored close; that has gone with about "
                          f"{num(r['btc_beta']) * b_['live_chg']:+.1f}% in this stock"
                          + (f" (weight {r['weight']:g}%: {num(r['weight']) * num(r['btc_beta']) * b_['live_chg'] / 100.0:+.2f} points)" if num(r.get("weight")) else " (not held)"))
        dcq = q.get("daycall") or {}
        if dcq:
            tgt_ = dcq.get("date") or today
            hit_ = 0
            for r in ledger:
                if r["table"] == "daycall" and r["date"] == tgt_ and r["ret_pct"] is None:
                    key_ = "adjust" if r["name"] == "S&P 500" else "port_adjust"
                    if num(dcq.get(key_)) is None:
                        continue
                    r["adj_morn"] = clamp(num(dcq.get(key_)), -5, 5)
                    r["confidence"] = int(round(clamp((num(r["score"]) or 50.0) + (num(r["adj_eve"]) or 0.0) + r["adj_morn"], 1, 99)))
                    r["kind"] = "green" if r["confidence"] >= 50 else "red"
                    if dcq.get("reason"):
                        base_ = (r["lesson"] or "").split(" | Morning: ")[0]
                        r["lesson"] = (base_ + " | Morning: " if base_ else "Morning: ") + dcq["reason"]
                    hit_ += 1
                    print(f"DAY CALL {tgt_} {r['name']}: now {r['kind'].upper()} {r['confidence']}% (model {r['score']:.0f}, evening {r['adj_eve']:+g}, morning {r['adj_morn']:+g})")
            if not hit_:
                print(f"DAY CALL: no open call for {tgt_} to revise")
        seen = {(r["date"], r["time_uk"], r["stock"], r["text"]) for r in ledger if r["table"] == "alert"}
        ids = {r["id"] for r in ledger}
        n_new = 0
        for v in q.get("alerts") or []:
            key = (v.get("date") or today, v.get("time_uk"), v.get("stock"), v.get("text") or "")
            if key in seen or not key[3]:
                continue
            row = lrow("alert", date=key[0], time_uk=key[1], stock=key[2], text=key[3])
            base, k = f"alert:{key[0]}:{key[2] or ''}", 1
            rid = base
            while rid in ids:
                k += 1
                rid = f"{base}:{k}"
            row["id"] = rid
            ids.add(rid)
            ledger.append(row)
            n_new += 1
        json.dump(ledger, open(os.path.join(a["out"], "ledger.json"), "w"), separators=(",", ":"))
        print(f"ALERTS: {n_new} added to the log; ledger.json written")
    print(f"Refreshed {len([r for r in rows if quotes.get(r.get('ticker') or '')])} of {len(rows) - 1} stocks; "
          f"weighted move so far {total:+.3f}% of the portfolio")
    for r in sorted((r for r in rows if r["group"] == "Portfolio"), key=lambda r: -(r["contrib_pts"] or 0)):
        if r["contrib_pts"] is None:
            print(f"  {r['name'][:18].ljust(19)} weight {r['weight']:g}%: " + ("no quote" if r["name"] in noq else f"not bought yet (fills {r.get('live_from')})"))
        else:
            print(f"  {r['name'][:18].ljust(19)} weight {r['weight']:g}% x {(r['contrib_pts'] / r['weight'] * 100):+.2f}% = {r['contrib_pts']:+.3f} points")
    print("  (A weight change that fills today is treated as held since the previous close; the evening run is exact.)")


def cmd_reorder(a):
    rows = json.load(open(a["stocks"]))
    ledger = [{k: r.get(k) for k in LEDGER_KEYS} for r in json.load(open(a["ledger"]))]
    o = json.load(open(a["order"]))
    order, eff = o.get("order") or [], o.get("effective")
    errs, cash = check_order(order)
    names = {r["name"] for r in rows if r["group"] != "Cash"}
    errs += [f"{x['name']} is not in stocks.json (new names go in through the evening run)" for x in order if x["name"] not in names]
    if not eff:
        errs.append("no effective date")
    if errs:
        sys.exit("ERROR in order: " + "; ".join(errs))
    n_before = len([r for r in ledger if r["table"] == "trade"])
    ledger = apply_order(ledger, order, eff, o.get("entered") or eff, o.get("order_reason") or "",
                         {r["name"]: r["ticker"] for r in rows}, {r["name"]: r.get("score") for r in rows})
    ledger = record_expectation(ledger, o.get("order_expected"), eff, o.get("entered") or eff,
                                len([r for r in ledger if r["table"] == "trade"]) > n_before, (o.get("entered") or eff) > eff)
    if len([r for r in ledger if r["table"] == "trade"]) < n_before:
        sys.exit("ERROR: the new ledger would lose rows; nothing written")
    w = {x["name"]: num(x["weight"]) or 0.0 for x in order}
    c = {x["name"]: num(x.get("confidence")) for x in order}
    for r in rows:
        r.setdefault("fill_price", None)
        for k_ in ("btc_beta", "btc_corr", "btc_net", "eth_beta", "eth_corr", "crypto_days", "crypto_link"):
            r.setdefault(k_, None)
        if r["group"] == "Cash":
            r["weight"] = cash
        elif w.get(r["name"], 0) > 0:
            r.update({"group": "Portfolio", "weight": w[r["name"]], "confidence": c[r["name"]], "status": "Holding",
                      "live_from": position_start(ledger, r["name"], "9999-12-31")})
        elif r["group"] == "Portfolio":
            r.update({"group": "Watchlist", "weight": None, "confidence": None, "status": "Watching", "live_from": None,
                      "contrib_pts": None, "risk_share_pct": None, "fill_price": None})
        if o.get("order_for"):
            r["order_for"] = o["order_for"]
    used = {}
    ledger.sort(key=lambda r: (r["table"], r["date"] or r["effective"] or "", r["time_uk"] or ""))
    for r in ledger:
        base = ":".join(str(x) for x in (r["table"], r["date"] or r["effective"] or "", r["name"] or r["stock"] or "") if x != "")
        used[base] = used.get(base, 0) + 1
        r["id"] = base if used[base] == 1 else f"{base}:{used[base]}"
    os.makedirs(a["out"], exist_ok=True)
    json.dump(rows, open(os.path.join(a["out"], "stocks.json"), "w"), indent=1)
    json.dump(ledger, open(os.path.join(a["out"], "ledger.json"), "w"), separators=(",", ":"))
    print(f"ORDER check passed: {len([x for x in w.values() if x > 0])} stocks, cash {cash:g}%, effective {eff}")
    for r in sorted((r for r in ledger if r["table"] == "trade" and r["effective"] == eff), key=lambda r: r["name"]):
        print(f"  {r['name']}: {r['from_w']:g}% -> {r['to_w']:g}%")
    print("  (Risk, theme and scenario tables are refreshed by the next evening run.)")


def cmd_template(a):
    rows = json.load(open(a["stocks"]))
    first = rows[0] if rows else {}
    cash = next((r for r in rows if r["group"] == "Cash"), {})
    out = {
        "date": None, "next_session": None, "prices_as_of": "", "order_for": "", "effective": None, "entered": None,
        "macro": {"date": None, "oil_proxy": "OIL", "values": {k: None for k, _, _ in MACRO_SERIES}},
        "daycall": {"bull": "", "bear": "", "adjust": 0, "port_adjust": 0, "reason": ""},
        "extra_history": {t: [] for t in sorted({"OIL"} | {r.get("trend_ticker") for r in rows if r.get("trend_ticker")})},
        "regime": "mixed", "regime_label": first.get("regime") or "",
        "benchmark": {"ticker": "SPY", "change_52w_pct": None, "history": []},
        "order": [{"name": r["name"], "weight": r["weight"], "confidence": r["confidence"]} for r in rows if r["group"] == "Portfolio"],
        "order_reason": "", "order_expected": {"pts": None, "thesis": "", "invalidation": ""},
        "cash_note": cash.get("note") or "",
        "stocks": [{"name": r["name"], "ticker": r["ticker"], "market": r["market"], "currency": r["currency"], "theme": r.get("theme"),
                    "status": r["status"], "note": r["note"], "link": r["link"], "added": r.get("added"),
                    "quote": {"price": None, "open": None, "high": None, "low": None, "volume": None, "prev_close": None,
                              "week52_high": r.get("week52_high"), "week52_low": r.get("week52_low"), "target": r.get("target"),
                              "next_results": r.get("next_results") or ""},
                    "stats": ({"trend_ticker": r.get("trend_ticker")} if r.get("ma_source") == "stored prices" else   # worked out from stored prices: nothing to fetch
                              {"ma50": r.get("ma50"), "ma200": r.get("ma200"),
                               "rsi": r.get("rsi") if (r.get("ma50") is not None or r.get("ma200") is not None) else None,
                               "change_52w_pct": r.get("change_52w_pct"), "avg_vol_20d": r.get("avg_vol_20d"),
                               "trend_price": r.get("trend_price"), "trend_ticker": r.get("trend_ticker")}),
                    "history": [], "catalyst_pts": r.get("catalyst_pts"), "catalyst_note": r.get("catalyst_note") or "",
                    "revisions_pts": r.get("revisions_pts"), "revisions_note": r.get("revisions_note") or ""}
                   for r in rows if r["group"] != "Cash"],
        "events": [], "revisions": [], "alerts": [], "scenarios": [], "reported": None, "postmortems": [], "fixes": [],
    }
    path = a.get("out") if str(a.get("out", "")).endswith(".json") else os.path.join(a.get("out") or ".", "today.json")
    if a.get("history"):
        have_ = {r["ticker"] for r in json.load(open(a["history"]))}
        for t_ in sorted(set(CRYPTO_PROXY.values()) & have_):
            out["extra_history"][t_] = []
    if a.get("ledger"):                             # for reference only: `run` ignores keys that start with an underscore
        led = json.load(open(a["ledger"]))
        evs = sorted((r for r in led if r["table"] == "event"), key=lambda r: (r["date"] or "", r["time_uk"] or ""))
        out["_calendar"] = [{k: r.get(k) for k in ("date", "time_uk", "name", "kind", "stock", "forecast", "previous", "actual", "implied_pct")} for r in evs]
        try:
            out["_scenarios"] = [{"name": r["name"], "shocks": json.loads(r["plan"])} for r in led if r["table"] == "scenario" and r["plan"]]
        except ValueError:
            out["_scenarios"] = []
        calls = sorted((r for r in led if r["table"] == "daycall" and r["ret_pct"] is None), key=lambda r: r["date"])
        out["_open_calls"] = [{k: r.get(k) for k in ("date", "name", "kind", "confidence", "score", "adj_eve", "adj_morn")} for r in calls]
        print(f"Stored calendar: {len(out['_calendar'])} events copied to _calendar; {len(out['_scenarios'])} scenarios with their assumed moves copied to _scenarios.")
    if a.get("history"):
        last = {}
        for r in json.load(open(a["history"])):
            if r["date"] > last.get(r["ticker"], ""):
                last[r["ticker"]] = r["date"]
        ref = last.get("SPY", "")
        need_t = [x["ticker"] for x in out["stocks"]] + list(out["extra_history"])
        behind = [f"{t} (last {last.get(t, 'none')})" for t in need_t if last.get(t, "") < ref]
        out["_last_stored"] = {t: last.get(t) for t in ["SPY"] + need_t}
        print(f"Price store: SPY's last stored session is {ref or 'none'}. " + ("Behind it: " + ", ".join(behind) + ". Fetch a history page for each." if behind else "Every stock is up to that date."))
    out["drift"] = []
    if a.get("panel"):
        panel = json.load(open(a["panel"]))
        out["panel_history"] = {}
        hist_ = {(r["ticker"], r["date"]): r for r in json.load(open(a["history"]))} if a.get("history") else {}
        short_, behind_, lb_ = panel_status(panel, hist_, "SPY")
        print(f"Panel: {len(panel.get('members') or [])} stocks fixed on {panel.get('frozen')}. "
              + ("Short of a two-year history: " + ", ".join(short_) + ". " if short_ else "")
              + (f"Behind {lb_}: " + ", ".join(behind_) + "." if behind_ else ("Every panel stock is up to date." if not short_ else "")))
    if a.get("ledger") and a.get("history"):
        led_ = json.load(open(a["ledger"]))
        hrows_ = json.load(open(a["history"]))
        spy_ = sorted({r["date"] for r in hrows_ if r["ticker"] == "SPY"})[-5:]
        names_ = {x["ticker"] for x in out["stocks"]}
        sold_ = sorted({(r["name"], r["ticker"]) for r in led_ if r["table"] == "trade" and r["effective"] in spy_
                        and (num(r["to_w"]) or 0) < (num(r["from_w"]) or 0) and r["ticker"] and r["ticker"] not in names_})
        if sold_:
            print("Sold in the last five sessions and no longer on the list (the standstill test needs each one's row for the session under "
                  "extra_history, from its history page): " + ", ".join(f"{n_} ({t_})" for n_, t_ in sold_))
            for n_, t_ in sold_:
                out["extra_history"].setdefault(t_, [])
        inc_ = [(n_, t_) for n_, t_ in inception_tickers([{k: r.get(k) for k in LEDGER_KEYS} for r in led_]) if t_ not in names_]
        if inc_:                                      # v7.1: the inception standstill keeps pricing the first order
            have_ = {}
            for r in hrows_:
                if r["ticker"] in {t_ for _, t_ in inc_}:
                    have_[r["ticker"]] = max(have_.get(r["ticker"], ""), r["date"])
            print("First order, no longer on the list (the inception standstill needs every session's row under extra_history, "
                  "one history page each; give every session after the last stored one): "
                  + ", ".join(f"{n_} ({t_}, stored to {have_.get(t_, 'none')})" for n_, t_ in inc_))
            for n_, t_ in inc_:
                out["extra_history"].setdefault(t_, [])
    if a.get("ledger"):
        led_ = json.load(open(a["ledger"]))
        dw_ = sorted({(r["ticker"], r["date"]) for r in led_ if r["table"] == "drift" and r["beat"] is None})
        if dw_:
            print("Drift rows still open (their prices are needed until five sessions after the date): " + ", ".join(f"{t_} from {d_}" for t_, d_ in dw_))
    json.dump(out, open(path, "w"), indent=1)
    need = [r["name"] for r in rows if r["group"] != "Cash" and r.get("ma_source") != "stored prices"]
    print("Averages still needed from a published page for: " + (", ".join(need) or "none"))
    print(f"Template written to {path}: {len(out['stocks'])} stocks, {len(out['order'])} in the order. "
          "Set date, next_session, prices_as_of, order_for, effective, entered and macro; add each stock's row for the session and its quote; then run.")


def cmd_closes(a):
    import datetime
    for k in ("history", "today", "ticker", "first", "last", "closes"):
        if not a.get(k):
            sys.exit(f"ERROR: closes needs --{k}")
    hist = json.load(open(a["history"]))
    bench, tick = a.get("bench") or "SPY", a["ticker"]

    def day(x):
        x = str(x).strip()
        if x.isdigit() and len(x) >= 9:
            n = int(x)
            return datetime.datetime.fromtimestamp(n / 1000.0 if n > 1e11 else n, datetime.timezone.utc).strftime("%Y-%m-%d")
        return x[:10]

    d1, d2 = day(a["first"]), day(a["last"])
    vals = [num(v) for v in str(a["closes"]).replace("\n", ",").replace(";", ",").split(",") if v.strip()]
    if not vals or any(v is None or v <= 0 for v in vals):
        sys.exit("ERROR: the closes must be positive numbers separated by commas; nothing written")
    if d1 > d2:
        vals.reverse()
        d1, d2 = d2, d1
    sess = sorted({r["date"] for r in hist if r["ticker"] == bench and d1 <= r["date"] <= d2})
    if len(sess) != len(vals) or not sess or sess[0] != d1 or sess[-1] != d2:
        sys.exit(f"ERROR {tick}: {len(vals)} closes, but {bench} has {len(sess)} stored sessions from {d1} to {d2}"
                 + (f" (its own run from {sess[0]} to {sess[-1]})" if sess else "")
                 + "; the dates cannot be lined up, so nothing was written. Leave this stock for another night.")
    stored = {r["date"]: r for r in hist if r["ticker"] == tick}
    panel = load(a.get("panel"), None) if a.get("panel") else None
    to_panel = panel is not None and tick in {m["ticker"] for m in panel.get("members") or []}
    if to_panel:                                     # a panel stock: check against the panel's own closes as well
        for d_, c_ in (panel.get("closes") or {}).get(tick, []):
            stored.setdefault(d_, {"close": c_})
    both = [(d, v, stored[d]["close"]) for d, v in zip(sess, vals) if d in stored]
    bad = [x for x in both if abs(x[1] / x[2] - 1.0) > 0.005]
    if bad and a.get("force") != "yes":
        sys.exit(f"ERROR {tick}: {len(bad)} of {len(both)} closes disagree with the stored ones by more than 0.5%, for example "
                 + "; ".join(f"{d} feed {v:g} against stored {s:g}" for d, v, s in bad[:4])
                 + ". A split, a different share class or the wrong ticker would do this; nothing was written.")
    jumps = [(sess[i], pct(vals[i], vals[i - 1])) for i in range(1, len(vals)) if abs(pct(vals[i], vals[i - 1])) > 35]
    today = json.load(open(a["today"]))
    stock = next((s for s in today.get("stocks") or [] if s.get("ticker") == tick), None)
    if to_panel:
        rows = today.setdefault("panel_history", {}).setdefault(tick, [])
    elif stock is not None:
        rows = stock.setdefault("history", [])
    else:
        rows = today.setdefault("extra_history", {}).setdefault(tick, [])
    panel_have = {d_ for d_, _ in (panel.get("closes") or {}).get(tick, [])} if to_panel else set()
    have = {str(r.get("date"))[:10] for r in rows} | (panel_have if to_panel else set(stored))
    new = [{"date": d, "close": v} for d, v in zip(sess, vals) if d not in have]
    rows.extend(new)
    rows.sort(key=lambda r: str(r.get("date")))
    json.dump(today, open(a["today"], "w"), indent=1)
    print(f"{tick}: {len(vals)} closes from {d1} to {d2}; {len(both)} already stored"
          + (", all within 0.5%" if both and not bad else "" if both else " (nothing to check them against)")
          + f"; {len(new)} close-only rows added to " + ("panel_history" if to_panel else "its history" if stock is not None else "extra_history") + f" in {a['today']}.")
    for d, c in jumps:
        print(f"  CHECK {tick} {d}: the close moved {c:+.1f}% in a day; a split or a typing slip is more likely than a real move")


def cmd_report(a):
    ledger = json.load(open(a["ledger"]))
    since = a.get("since") or "0000-00-00"
    T = lambda t: [r for r in ledger if r["table"] == t]
    perf = sorted(T("perf"), key=lambda r: r["date"])
    if not perf:
        print("No completed sessions in the performance log yet.")
    else:
        last = perf[-1]
        print(f"TO DATE ({perf[0]['date']} to {last['date']}, {len(perf)} sessions): estimated value {last['value_est']:.0f}, "
              f"return {last['cum_pct']:+.2f}% vs S&P 500 {last['spx_cum_pct']:+.2f}% (gap {last['cum_pct'] - last['spx_cum_pct']:+.2f} points)")
        wk = [r for r in perf if r["date"] >= since]
        if wk and since != "0000-00-00":
            prior = [r for r in perf if r["date"] < since]
            v0 = prior[-1]["value_est"] if prior else next(r["value"] for r in T("meta") if r["name"] == "start_value")
            s0 = prior[-1]["spx_cum_pct"] if prior else 0.0
            pr = (wk[-1]["value_est"] / v0 - 1) * 100
            sr = ((1 + wk[-1]["spx_cum_pct"] / 100) / (1 + s0 / 100) - 1) * 100
            print(f"SINCE {since} ({len(wk)} sessions): portfolio {pr:+.2f}% vs S&P 500 {sr:+.2f}%")
        print("DAYS: " + "; ".join(f"{r['date'][5:]} {r['day_pct']:+.2f}%" for r in (wk or perf)))
        best, worst = max(perf, key=lambda r: r["day_pct"]), min(perf, key=lambda r: r["day_pct"])
        print(f"Best day {best['date']} {best['day_pct']:+.2f}%; worst day {worst['date']} {worst['day_pct']:+.2f}%")
        tot = {}
        for r in T("contrib"):
            if r["date"] >= since:
                tot[r["name"]] = tot.get(r["name"], 0.0) + (r["contrib_pts"] or 0.0)
        print("CONTRIBUTION BY POSITION (weight x return, summed over the period, in points of the portfolio):")
        for n, v in sorted(tot.items(), key=lambda kv: -kv[1]):
            print(f"    {n[:22].ljust(23)} {v:+.3f}")
    rep_rows = sorted(T("reported"), key=lambda r: (r["date"], r["time_uk"] or ""))
    for r in rep_rows[-5:]:
        pc = f", top {r['percentile']:g}%" if r["percentile"] is not None else ""
        rk = f", rank {int(r['rank'])} of {int(r['players'])}{pc}" if r["rank"] and r["players"] else ""
        print(f"REPORTED {r['date']} {r['time_uk'] or ''}: value {r['value_reported']}{rk}")
    if rep_rows and rep_rows[-1]["percentile"] is not None:
        pc = rep_rows[-1]["percentile"]
        print("RANK STANCE: " + ("inside the top 2% target: protect it, cut volatility from 13 Nov" if pc <= 2 else
              f"outside the target (top {pc:g}% against 2%): keep risk on within the guardrails; position {int(rep_rows[-1]['players'] * 0.02)} or better is needed"))
    for r in rep_rows:
        if r["value_est"] is not None and r["value_reported"] is not None:
            gap = r["value_reported"] - r["value_est"]
            early = (r["time_uk"] or "") and len(r["time_uk"]) == 5 and r["time_uk"] < us_close_uk(r["date"]) and any(
                p["date"] == r["date"] for p in perf)
            print(f"RECONCILE {r['date']} {r['time_uk'] or ''}: FT {r['value_reported']:.0f} against the estimate {r['value_est']:.0f}, "
                  f"gap {gap:+.0f} credits ({gap / r['value_est'] * 100:+.2f}%)" + (" (read before the US close: not comparable)" if early else ""))
    for r in sorted(T("standstill"), key=lambda r: (r["kind"], r["date"])):
        if (r["window_end"] or "") >= since:
            if r["value"] is None:
                print(f"STANDSTILL {r['name']}: not priced ({r['confirmed']}); {r['text']}")
            else:
                print(f"STANDSTILL {r['name']}: {r['value']:+.3f} points over {r['days']} session(s) "
                      f"({r['ret_pct']:+.3f}% against {r['spx_ret_pct']:+.3f}% for the order kept), {r['confirmed']}; {r['text']}"
                      + (f"; expected {r['forecast']:+.3f}" if r.get("forecast") is not None else ""))
    for l_ in expectation_lines([{k: r.get(k) for k in LEDGER_KEYS} for r in ledger]):
        print(l_)
    for r in T("calib"):
        if r["kind"] == "judgement":
            print(f"JUDGEMENT TEST {r['name']}: {r['text']}")
    rk_ = sorted((r for r in T("risk") if r["risk_share_pct"] is not None), key=lambda r: -r["risk_share_pct"])
    if rk_:
        print("RISK share by position: " + ", ".join(f"{r['name']} {r['risk_share_pct']:g}% (weight {r['weight']:g}%)" for r in rk_))
    cr_ = sorted((r for r in T("corr") if r["value"] is not None), key=lambda r: -r["value"])[:4]
    if cr_:
        print("MOST CORRELATED pairs: " + ", ".join(f"{r['name']} {r['value']:.2f}" for r in cr_))
    for r in sorted(T("scenario"), key=lambda r: r["impact_pct"] or 0):
        print(f"SCENARIO {r['name']}: {r['impact_pct']:+.2f}%")
    conf = T("confidence")
    done = [r for r in conf if r["beat"] in ("yes", "no")]
    print(f"CONFIDENCE: {len(done)} of {len(conf)} ratings resolved")
    for lo, hi, label in ((0, 54, "below 55"), (55, 59, "55 to 59"), (60, 100, "60 and above")):
        b = [r for r in done if r["confidence"] is not None and lo <= r["confidence"] <= hi]
        if b:
            hits = len([r for r in b if r["beat"] == "yes"])
            exp = sum(r["confidence"] for r in b) / len(b)
            print(f"    band {label}: {hits} of {len(b)} beat the index ({hits / len(b) * 100:.0f}%), average rating {exp:.0f}")
    for r in done:
        print(f"    {r['name'][:22].ljust(23)} rated {r['confidence']:g}, score {r['score']}, {r['ret_pct']:+.2f}% vs S&P {r['spx_ret_pct']:+.2f}%: {r['beat']}")
    for who in ("S&P 500", "Portfolio"):
        dcs = [r for r in T("daycall") if r["name"] == who and r["beat"] in ("yes", "no")]
        if dcs:
            hits = len([r for r in dcs if r["beat"] == "yes"])
            brier = sum(((r["confidence"] / 100.0) - (1.0 if r["ret_pct"] > 0 else 0.0)) ** 2 for r in dcs) / len(dcs)
            ups = len([r for r in dcs if r["ret_pct"] > 0])
            print(f"DAY CALLS ({who}): {hits} right of {len(dcs)}; {ups} of those days rose, so always saying green would have scored {ups}; "
                  f"Brier score {brier:.3f} (0.25 is what a coin flip scores, lower is better)")
            for r in sorted(dcs, key=lambda r: r["date"]):
                if r["date"] >= since:
                    print(f"    {r['date']}: said {r['kind']} at {r['confidence']}%, moved {r['ret_pct']:+.2f}%: {r['beat']}")
    for r in T("calib"):
        if r["days"] and r["kind"] in ("live", "backtest", "backtest-summary"):
            if r["kind"] == "backtest-summary": print("CALIBRATION backtest (stocks picked with hindsight): " + r["text"])
            else: print(f"CALIBRATION {r['kind']} {r['name']}: {r['days']} cases, beat the index {r['percentile']:.0f}% of the time, average gap {r['value']:+.2f} points")
    for r in T("calib"):
        if r["kind"] == "panel-summary":
            print(f"PANEL TEST {r['name'][12:]}: {r['text']}")
        elif r["kind"] == "panel-part" and r["days"]:
            print(f"PANEL PART {r['name'][6:]}: {r['text']}")
    for r in T("calib"):
        if r["kind"] == "drift":
            print(f"DRIFT {r['name'][12:]}: {r['days']} settled" + (f", beat the index {r['percentile']:.0f}% of the time, average gap {r['value']:+.2f} points" if r["days"] else "") + f"; {r['text']}")
    for r in sorted(T("drift"), key=lambda r: r["date"] or ""):
        if (r["date"] or "") >= since:
            res = (f"{r['ret_pct']:+.2f}% vs S&P {r['spx_ret_pct']:+.2f}% {r['unit'] or 'from the reaction close'}: {r['beat']}"
                   + (f" (from the reaction close {r['cum_pct']:+.2f}% vs {r['spx_cum_pct']:+.2f}%)" if r["cum_pct"] is not None and r["unit"] == "from the next open" else "")
                   ) if r["beat"] in ("yes", "no") else (r["beat"] or "open")
            print(f"    DRIFT {r['date']} {r['name'][:22].ljust(23)} {r['kind']}, {r['score']} of 6 tests; {res}")
    sh = T("shadow")
    print(f"SHADOW RATINGS: {len([r for r in sh if r['beat'] in ('yes', 'no')])} of {len(sh)} settled")
    for r in T("macro"):
        if r["kind"] == "backdrop": print(f"MACRO backdrop ({r['date']}): {r['action']}. {r['text']}")
    for r in sorted(T("event"), key=lambda r: r["date"] or ""):
        if r["kind"] == "macro" and r["actual"] and (r["date"] or "") >= since:
            print(f"MACRO RELEASE {r['date']} {r['name']}: actual {r['actual']} against forecast {r['forecast'] or 'n/a'} (previous {r['previous'] or 'n/a'}); "
                  f"S&P 500 {r['spx_ret_pct'] if r['spx_ret_pct'] is not None else 'n/a'}% that day, 10-year yield {r['chg_1d'] if r['chg_1d'] is not None else 'n/a'}bp")
    for r in sorted(T("trade"), key=lambda r: r["effective"] or ""):
        if (r["effective"] or "") >= since:
            print(f"TRADE {r['effective']}: {r['name']} {r['from_w']:g}% -> {r['to_w']:g}%")
    for r in T("postmortem"):
        if r["date"] >= since:
            print(f"CLOSED {r['name']}: held {r['effective']} to {r['date']} ({r['days']} sessions), return {r['ret_pct']:+.2f}%, contribution {r['contrib_pts']:+.3f} points. {r['lesson'] or ''}")


def cmd_panel(a):
    """--init members.json --out panel.json creates the panel file once; --panel panel.json [--history h.json] reports on it."""
    if a.get("init"):
        spec = json.load(open(a["init"]))
        if os.path.exists(a.get("out") or "") and a.get("force") != "yes":
            sys.exit("ERROR: the panel file already exists; the panel is fixed and is never rebuilt")
        tick = [m["ticker"] for m in spec["members"]]
        if len(set(tick)) != len(tick):
            sys.exit("ERROR: duplicate tickers in the panel")
        out = {"frozen": spec["frozen"], "rule": spec["rule"], "test": spec.get("test") or "", "source": spec.get("source") or "",
               "members": spec["members"], "closes": {}}
        json.dump(out, open(a["out"], "w"), separators=(",", ":"))
        print(f"Panel written to {a['out']}: {len(tick)} stocks fixed on {spec['frozen']}.")
        return
    panel = json.load(open(a["panel"]))
    hist = {(r["ticker"], r["date"]): r for r in json.load(open(a["history"]))} if a.get("history") else {}
    if a.get("merge"):                           # store closes collected with `closes --panel` without a full run
        members = {m["ticker"] for m in panel.get("members") or []}
        pcl, n = panel.setdefault("closes", {}), 0
        for t, rows in sorted((json.load(open(a["merge"])).get("panel_history") or {}).items()):
            if t not in members:
                continue
            have = {r[0]: r[1] for r in pcl.get(t, [])}
            for r in rows:
                d, c = str(r.get("date"))[:10], num(r.get("close"))
                if len(d) == 10 and c and c > 0:
                    n += d not in have
                    have[d] = c
            pcl[t] = sorted([d, c] for d, c in have.items())
        if not a.get("out"):
            sys.exit("ERROR: --merge needs --out")
        json.dump(panel, open(a["out"], "w"), separators=(",", ":"))
        print(f"{n} new panel closes stored in {a['out']}.")
    short, behind, lb = panel_status(panel, hist, "SPY")
    print(f"Panel fixed on {panel['frozen']}: {panel['rule']}")
    for m in panel["members"]:
        d = (panel.get("closes") or {}).get(m["ticker"], [])
        print(f"    {str(m.get('rank', '')).rjust(4)} {m['ticker'].ljust(6)} {m['name'][:30].ljust(31)} {len(d):>4} closes" + (f", {d[0][0]} to {d[-1][0]}" if d else ""))
    if short: print("Short of a two-year history: " + ", ".join(short))
    if behind: print(f"Behind {lb}: " + ", ".join(behind))
    if hist:
        rows, _ = panel_rows(panel, hist, "SPY", lb)
        for r in rows:
            if r["kind"] == "panel-summary":
                print(f"{r['name'].upper()}: {r['text']}")
            elif r["kind"] == "panel-part" and r["days"]:
                print(f"    {r['name']}: {r['text']}")
            elif r["kind"] == "panel-band" and r["days"]:
                print(f"    BAND {r['name']}: {r['days']} cases, beat the index {r['percentile']:.0f}% of the time, average gap {r['value']:+.2f} points")


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("run", "refresh", "reorder", "report", "template", "closes", "panel"):
        print(__doc__)
        sys.exit(1)
    args = sys.argv[2:]
    a = {args[i].lstrip("-"): args[i + 1] for i in range(0, len(args) - 1, 2)}
    if sys.argv[1] not in ("template", "closes", "panel"):
        a.setdefault("out", "out")
    {"run": cmd_run, "refresh": cmd_refresh, "reorder": cmd_reorder, "report": cmd_report, "template": cmd_template,
     "closes": cmd_closes, "panel": cmd_panel}[sys.argv[1]](a)


if __name__ == "__main__":
    main()
