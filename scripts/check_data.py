#!/usr/bin/env python3
"""check_data.py: integrity and freshness checks on the stored game data (added 19 Oct 2026, playbook 6.11).

Run from the repository root (standard library only; it reads the pipeline for its constants and never writes):

    python3 -I scripts/check_data.py                 integrity checks on data/ and state/last-sync.md
    python3 -I scripts/check_data.py --fresh         also checks that the latest nightly mirror is recent and complete
    python3 -I scripts/check_data.py --now 2026-10-19T23:00:00Z --fresh     (a fixed clock, for tests)

Every check prints PASS, WARN or FAIL. The exit code is 1 if any check failed, else 0. The GitHub workflow
`.github/workflows/data-check.yml` runs it on every push that changes data/ or state/, and with --fresh on a schedule
after each evening and weekly review, so a run that did not publish, or published incomplete data, shows as a red
check in the repository.

What is checked (FAIL unless marked WARN):
  files       every data file parses, with the expected shape
  ledger      every row has exactly the pipeline's ledger fields; ids are unique; tables are known ones
  history     one row per ticker and date; prices above zero; low <= open, close <= high; no date in the future
  order       stocks.json's holdings match the latest order in the ledger; game rules: 5 to 20 holdings,
              each 5% to 25%, cash 0% to 25%, weights adding to 100
  performance one row per benchmark session from the first fill, none missing in between; each day's value
              compounds from the one before; contributions add up to the day's return (weight x return), and
              (7.6) every stock held or traded that session has its own contribution row
  recalc      (19 Oct evening) every stored value matches the pipeline's own recalculation from the stored positions
              and prices, within RECALC_CREDITS; this also catches a fill priced from an estimated open
  results     every holding whose next-results text names a date has a results event ON that date (7.6: an event on
              another date is a FAIL unless marked confirmed "uncertain" with its reason, a WARN; two future events
              for one holding are a FAIL); an implied move is missing for a report inside five sessions (FAIL) or
              inside ten (WARN), unless the event's text or plan says "implied move unavailable" (or "not available")
              with the source tried and the date (WARN: the 6% then used in RESULTS TOTAL is an assumption, never a
              market estimate; 7.6: without the source and date, FAIL inside five sessions); a stored implied move
              that names no source (WARN, 7.6); the event's last order is missing, unreadable, not a deadline
              "before"/"by" a time at or before CUTOFF_UK, names the wrong weekday, or is later than part C allows on
              the stock's own market calendar (7.6: London's for a London stock) (FAIL inside five sessions, WARN
              inside ten)
  sync        each data/ and state/ file listed in state/last-sync.md has the sha256 recorded there, and (7.6) the
              list holds all six files a mirror records (REQUIRED_SYNC)
  --fresh     the last mirror ran within FRESH_HOURS; the benchmark's latest stored session is the latest US session
              that has closed; performance is recorded up to that session
"""
import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BENCH = "SPY"
FRESH_HOURS = 6              # the scheduled check runs about 1.5 to 2 hours after a review's publish
SETTLE_MINUTES = 30          # a US session counts as available this long after its close
KNOWN_TABLES = {"alert", "analog", "calib", "confidence", "contrib", "corr", "daycall", "drift", "event", "expect", "macro",
                "meta", "perf", "position", "postmortem", "reported", "revision", "risk", "scenario", "shadow", "standstill",
                "theme", "trade"}
RECALC_CREDITS = 0.05        # stored against recalculated value; the pipeline rounds each day to the cent
GAME_END = "2026-11-27"
CUTOFF_UK = "07:00"          # playbook part C: the order cut-off until the FT confirms otherwise (change it there, here and in ft_pipeline.py)
_MONTH = {m: i + 1 for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])}


def _day_in(text):
    """The first 'D Mon' in free text ("Before 07:00 Mon 26 Oct" -> 2026-10-26), October to December as 2026."""
    for d, m in re.findall(r"\b(\d{1,2})\s+([A-Za-z]{3})[a-z]*\b", text or ""):
        mon = _MONTH.get(m.lower())
        if mon:
            try:
                return dt.date(2026 if mon >= 10 else 2027, mon, int(d)).isoformat()
            except ValueError:
                return None
    return None


_WEEKDAY = {"mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6}
REQUIRED_SYNC = ("data/history.json", "data/ledger.json", "data/macro.json", "data/panel.json", "data/stocks.json",
                 "state/ft-game-state.md")                       # 7.6: what every nightly and weekly mirror (G6) records


def _prev_session(day, pl, market=None):
    """The session before `day` on the listing's market (7.6: London's calendar for a London stock; the US calendar
    otherwise, which is also the conservative choice when the market is not known)."""
    shut = getattr(pl, "LONDON_CLOSED", set()) if market == "UK" else pl.US_CLOSED
    d = dt.date.fromisoformat(day) - dt.timedelta(days=1)
    while d.weekday() >= 5 or d.isoformat() in shut:
        d -= dt.timedelta(days=1)
    return d.isoformat()


def last_order_problem(ev, pl, market=None):
    """Why a held stock's results event has no usable last order, or None. Playbook part C: results after the US close on
    day D need the order before the cut-off on D; anything else (before the open, a London 07:00 release, a time during
    the session or no time) needs it before the cut-off on the session before D, on the stock's own market (7.6).
    7.6: the last order must say plainly that it is a deadline at or before the cut-off ("Before 07:00 Wed 28 Oct",
    "by 06:30 ..."): a missing time, "any time" or "after" wording is a problem, and a weekday that does not match the
    date is unreadable."""
    lo = (ev.get("last_order") or "").strip()
    if not lo or lo.lower() == "passed":
        return "none recorded"
    day, t = ev["date"], (ev.get("time_uk") or "").lower()
    hm = re.search(r"\b(\d\d):(\d\d)\b", t)
    after = "after" in t or bool(hm and hm.group(0) >= pl.us_close_uk(day))
    latest = day if after else _prev_session(day, pl, market)
    when = _day_in(lo)
    if when is None:
        return f"no date readable in '{lo}'"
    wd = re.search(r"\b(mon|tue|wed|thu|fri|sat|sun)[a-z]*\b\.?\s+\d{1,2}\s+[A-Za-z]{3}", lo, flags=re.I)
    if wd and _WEEKDAY[wd.group(1).lower()] != dt.date.fromisoformat(when).weekday():
        return f"'{lo}' names a weekday that is not {when}'s"
    if when > latest:
        return f"'{lo}' is later than the last possible order day, {latest}"
    times = re.findall(r"\b\d\d:\d\d\b", lo)
    if not times:
        return f"'{lo}' gives no time; it must say before {CUTOFF_UK} UK (or earlier)"
    if any(x > CUTOFF_UK for x in times):
        return f"'{lo}' names a time after the {CUTOFF_UK} UK cut-off"
    if re.search(r"\b(after|from|any ?time|anytime|until|till)\b", lo, flags=re.I) or not re.search(
            r"\b(before|by|no later than|latest)\b", lo, flags=re.I):
        return f"'{lo}' does not read as a deadline at or before the cut-off (write \"Before {CUTOFF_UK} <Day D Mon>\")"
    return None


_SOURCE = re.compile(r"(\b[a-z0-9-]+\.(?:com|co\.uk|net|org|io)\b|earnings-watcher|barchart|market ?chameleon|option|nasdaq|cboe|"
                     r"yahoo|investing|zacks|marketbeat|stockanalysis|tradingview|straddle)", re.I)
_DATE_IN = re.compile(r"\b(\d{1,2}\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*|\d{4}-\d\d-\d\d)\b", re.I)


def unavailable_reason_problem(note):
    """7.6: a recorded absence of an implied move must say which source was tried and when: "Implied move unavailable:
    earnings-watcher page has no figure for KO, checked 19 Oct". Returns why it is not enough, or None."""
    m = re.search(r"implied move (?:unavailable|not available)\s*[:,;(-]?\s*(.*)", note or "", flags=re.I | re.S)
    rest = (m.group(1) if m else "").strip()
    missing = []
    if not _SOURCE.search(rest):
        missing.append("the source tried")
    if not _DATE_IN.search(rest):
        missing.append("the date checked")
    if len(re.findall(r"[A-Za-z]{2,}", rest)) < 4:
        missing.append("what happened")
    return ("it does not give " + ", ".join(missing)) if missing else None


def load_pipeline():
    spec = importlib.util.spec_from_file_location("ft_pipeline_for_check", REPO / "scripts" / "ft_pipeline.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Report:
    def __init__(self):
        self.lines, self.failed = [], 0

    def add(self, level, check, msg):
        self.lines.append(f"{level} {check}: {msg}")
        if level == "FAIL":
            self.failed += 1

    def ok(self, check, msg):
        self.add("PASS", check, msg)

    def warn(self, check, msg):
        self.add("WARN", check, msg)

    def fail(self, check, msg):
        self.add("FAIL", check, msg)


def ny_tz():
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo("America/New_York")
    except Exception:                         # no time-zone database: fall back to a fixed offset by date
        return None


def ny_close_utc(day, pl):
    """The UTC time of the US close on `day` (YYYY-MM-DD), early closes included."""
    hhmm = pl.US_EARLY_CLOSE_NY.get(day, "16:00")
    h, m = (int(x) for x in hhmm.split(":"))
    d = dt.date.fromisoformat(day)
    tz = ny_tz()
    if tz is not None:
        local = dt.datetime(d.year, d.month, d.day, h, m, tzinfo=tz)
        return local.astimezone(dt.timezone.utc)
    offset = 4 if dt.date(2026, 3, 8) <= d < dt.date(2026, 11, 1) else 5      # 2026 US daylight saving dates
    return dt.datetime(d.year, d.month, d.day, h + offset, m, tzinfo=dt.timezone.utc)


def expected_session(now, pl):
    """The latest US session whose close was at least SETTLE_MINUTES before `now` (a UTC datetime)."""
    d = now.date()
    for _ in range(15):
        day = d.isoformat()
        if d.weekday() < 5 and day not in pl.US_CLOSED and now >= ny_close_utc(day, pl) + dt.timedelta(minutes=SETTLE_MINUTES):
            return day
        d -= dt.timedelta(days=1)
    return None


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(repo, now, fresh, pl):
    r = Report()
    data = {}
    shapes = {"stocks": list, "ledger": list, "history": list, "macro": list, "panel": dict}
    for name, kind in shapes.items():
        p = repo / "data" / f"{name}.json"
        try:
            data[name] = json.loads(p.read_text(encoding="utf-8"))
        except FileNotFoundError:
            r.fail("files", f"data/{name}.json is missing")
            continue
        except ValueError as e:
            r.fail("files", f"data/{name}.json does not parse: {e}")
            continue
        if not isinstance(data[name], kind):
            r.fail("files", f"data/{name}.json is a {type(data[name]).__name__}, expected a {kind.__name__}")
            del data[name]
    if not all(k in data for k in ("stocks", "ledger", "history")):
        return r
    r.ok("files", "all five data files parse" if len(data) == 5 else f"{len(data)} of 5 data files parse")
    ledger, hist_rows, stocks = data["ledger"], data["history"], data["stocks"]

    # ledger
    bad_keys = [x.get("id") for x in ledger if list(x.keys()) != pl.LEDGER_KEYS]
    ids = [x.get("id") for x in ledger]
    dup = sorted({i for i in ids if ids.count(i) > 1}) if len(set(ids)) != len(ids) else []
    tables = {x.get("table") for x in ledger} - KNOWN_TABLES
    if bad_keys:
        r.fail("ledger", f"{len(bad_keys)} row(s) without exactly the pipeline's fields, e.g. {bad_keys[:3]}")
    if dup or None in ids or "" in ids:
        r.fail("ledger", f"ids not unique or empty: {dup[:5]}")
    if tables:
        r.fail("ledger", f"unknown table(s): {sorted(map(str, tables))}")
    if not (bad_keys or dup or tables or None in ids or "" in ids):
        r.ok("ledger", f"{len(ledger)} rows, fields and ids in order")

    # history
    today_utc = now.date().isoformat()
    seen, problems = set(), []
    for x in hist_rows:
        key = (x.get("ticker"), x.get("date"))
        if key in seen:
            problems.append(f"duplicate row {key}")
        seen.add(key)
        try:
            dt.date.fromisoformat(x["date"])
            o, h, lo, c = (float(x[k]) for k in ("open", "high", "low", "close"))
        except (KeyError, TypeError, ValueError):
            problems.append(f"unreadable row {key}")
            continue
        if min(o, h, lo, c) <= 0:
            problems.append(f"price at or below zero {key}")
        elif lo > min(o, c) * (1 + 1e-9) or h < max(o, c) * (1 - 1e-9):
            problems.append(f"open or close outside the day's range {key}")
        if x["date"] > today_utc:
            problems.append(f"date in the future {key}")
    if problems:
        r.fail("history", f"{len(problems)} problem(s): " + "; ".join(problems[:5]))
    else:
        r.ok("history", f"{len(hist_rows)} rows, one per ticker and date, prices consistent")
    hist = {(x["ticker"], x["date"]): x for x in hist_rows if "ticker" in x and "date" in x}
    bench_dates = sorted(d for (t, d) in hist if t == BENCH)

    # order and game rules
    held = {x["name"]: float(x["weight"] or 0) for x in stocks if x.get("group") == "Portfolio" and (x.get("weight") or 0) > 0}
    cash_rows = [x for x in stocks if x.get("group") == "Cash"]
    cash = float(cash_rows[0]["weight"] or 0) if len(cash_rows) == 1 else None
    errs = []
    if cash is None:
        errs.append(f"{len(cash_rows)} cash rows, expected 1")
    else:
        if not 0 <= cash <= 25:
            errs.append(f"cash {cash:g}% outside 0% to 25%")
        if abs(sum(held.values()) + cash - 100) > 0.01:
            errs.append(f"holdings and cash add to {sum(held.values()) + cash:g}%")
    if not 5 <= len(held) <= 20:
        errs.append(f"{len(held)} holdings, the game allows 5 to 20")
    errs += [f"{n} at {w:g}% (5% to 25% allowed)" for n, w in held.items() if not 5 <= w <= 25]
    latest = {n: w for n, (w, _t) in pl.live_weights(ledger, "9999-12-31").items() if w > 0}
    if {n: round(w, 6) for n, w in latest.items()} != {n: round(w, 6) for n, w in held.items()}:
        diff = sorted(set(latest.items()) ^ set(held.items()))
        errs.append(f"stocks.json holdings differ from the latest order in the ledger: {diff[:6]}")
    if errs:
        r.fail("order", "; ".join(errs))
    else:
        r.ok("order", f"{len(held)} holdings, cash {cash:g}%, matching the latest order")

    # performance
    perf = sorted((x for x in ledger if x["table"] == "perf"), key=lambda x: x["date"])
    meta = {x["name"]: x for x in ledger if x["table"] == "meta"}
    start_value = pl.num((meta.get("start_value") or {}).get("value")) or 100000.0
    errs = []
    if perf:
        pdates = [x["date"] for x in perf]
        if len(set(pdates)) != len(pdates):
            errs.append("more than one row for a session")
        span = [d for d in bench_dates if pdates[0] <= d <= pdates[-1]]
        missing = sorted(set(span) - set(pdates))
        extra = sorted(set(pdates) - set(bench_dates))
        if missing:
            errs.append(f"no performance row for benchmark session(s) {missing}")
        if extra:
            errs.append(f"performance row(s) on day(s) with no benchmark session {extra}")
        prev = start_value
        for x in perf:
            v, d_ = pl.num(x["value_est"]), pl.num(x["day_pct"])
            if v is None or d_ is None:
                errs.append(f"{x['date']}: no value or day's return")
                break
            if abs(prev * (1 + d_ / 100.0) - v) > max(1.5, prev * 2e-5):
                errs.append(f"{x['date']}: value {v:.2f} does not follow from {prev:.2f} and {d_:+.3f}%")
            prev = v
        contrib, named = {}, {}
        for x in ledger:
            if x["table"] == "contrib" and pl.num(x["contrib_pts"]) is not None:
                contrib[x["date"]] = contrib.get(x["date"], 0.0) + pl.num(x["contrib_pts"])
                named.setdefault(x["date"], set()).add(x["name"])
        start_d = (meta.get("start_date") or {}).get("text") or ""
        for x in perf:
            d = x["date"]
            i = bench_dates.index(d) if d in bench_dates else -1
            dprev = bench_dates[i - 1] if i > 0 else None
            # 7.6: every stock held or traded that session needs its own contribution row; before, a session with no rows
            # at all passed as "contributions add up"
            want = set(pl.live_weights(ledger, d)) | (set(pl.live_weights(ledger, dprev)) if dprev and dprev >= start_d else set())
            # 26 Oct: only a row with a weight above zero adds a name here. A zero row for a name not held the session
            # before is no trade (an order replaced before it filled leaves one: Hasbro, 22 Oct), and a sale of a name
            # that was held is already covered by the previous session's weights.
            want |= {r_["name"] for r_ in ledger if r_["table"] == "position" and (dprev or "") < (r_["effective"] or "") <= d
                     and (pl.num(r_["weight"]) or 0) > 0}
            lack = sorted(want - named.get(d, set()))
            if lack:
                errs.append(f"{d}: no contribution row for {', '.join(lack[:6])}")
            elif abs(contrib.get(d, 0.0) - (pl.num(x["day_pct"]) or 0)) > 0.01:
                errs.append(f"{d}: contributions add to {contrib.get(d, 0.0):+.3f} points against a day's return of {x['day_pct']:+.3f}%")
    if errs:
        r.fail("performance", "; ".join(errs[:6]))
    elif perf:
        r.ok("performance", f"{len(perf)} sessions to {perf[-1]['date']}, none missing, values compound, contributions add up")
    else:
        r.warn("performance", "no performance rows yet")
    last_perf = perf[-1]["date"] if perf else None
    if bench_dates and last_perf and bench_dates[-1] > last_perf:
        r.warn("performance", f"benchmark prices run to {bench_dates[-1]} but performance only to {last_perf} (PERFORMANCE INCOMPLETE)")

    # recalculation (19 Oct evening): the stored log against the pipeline's own valuation of the stored positions and
    # prices. Catches a corrupted price or position row, and a fill priced from an estimated open (the pipeline refuses
    # one, so the recalculated log would stop short).
    if perf:
        try:
            redo = [dict(x) for x in ledger if x["table"] not in ("perf", "contrib")]
            mc = next((x for x in ledger if x["table"] == "meta" and x["name"] == "market_closed"), None)
            closed = {tuple(c) for c in json.loads(mc["text"])} if mc and mc.get("text") else set()
            pl._SERIES.clear()
            pl.INCOMPLETE.clear()
            pl.update_performance(redo, hist, BENCH, last_perf, closed)
            got = {x["date"]: pl.num(x["value_est"]) for x in redo if x["table"] == "perf"}
            bad = [f"{x['date']} stored {pl.num(x['value_est']):.2f}, recalculated {got.get(x['date']) if got.get(x['date']) is None else round(got[x['date']], 2)}"
                   for x in perf if got.get(x["date"]) is None or abs(got[x["date"]] - pl.num(x["value_est"])) > RECALC_CREDITS]
            if bad:
                r.fail("recalc", f"stored values differ from a recalculation from positions and prices: {'; '.join(bad[:4])}"
                       + (f" ({pl.INCOMPLETE[0]})" if pl.INCOMPLETE else ""))
            else:
                r.ok("recalc", f"{len(perf)} stored values match a recalculation from positions and prices (within {RECALC_CREDITS} credits)")
        except Exception as e:  # noqa: BLE001  a check must report, not crash the workflow
            r.fail("recalc", f"could not recalculate: {type(e).__name__}: {e}")

    # results events, implied moves and last order deadlines
    asof = last_perf or (bench_dates[-1] if bench_dates else today_utc)
    nexts = {x["name"]: x.get("next_results") for x in stocks if x["name"] in held}
    mkt = {x["name"]: x.get("market") for x in stocks}
    cov = pl.results_coverage(ledger, nexts, asof, GAME_END) if hasattr(pl, "results_coverage") else None
    missing_ev = cov["missing"] if cov else pl.missing_results_events(ledger, nexts, asof)
    if missing_ev:
        r.fail("results", "holding(s) with a results date but no results event: "
               + ", ".join(f"{n} ({d})" for n, d, _ in missing_ev))
    wrong = cov["wrong_date"] if cov else []
    if wrong:                                               # 7.6: an event on another date does not cover the report
        r.fail("results", "holding(s) whose results event is not on the date their stock data gives (correct it, or mark "
               "the event confirmed \"uncertain\" with the reason): " + "; ".join(f"{n}: stock data {d}, event(s) {', '.join(ds)}"
                                                                      for n, d, ds in wrong))
    dups = cov["duplicate"] if cov else []
    if dups:
        r.fail("results", "more than one future results event for a holding: " + "; ".join(f"{n} ({', '.join(ds)})" for n, ds in dups))
    if cov and cov["uncertain"]:
        r.warn("results", "results date marked uncertain: " + "; ".join(f"{n}: stock data {d}, event {de} ({why})"
                                                                     for n, d, de, why in cov["uncertain"]))
    ahead5, ahead10 = set(pl._sessions_ahead(asof, 5)), set(pl._sessions_ahead(asof, 10))
    no_move5, no_move10, documented, thin5, thin10, unsourced, late5, late10 = [], [], [], [], [], [], [], []
    for x in ledger:
        if not (x["table"] == "event" and x["kind"] == "results" and x["stock"] in held and (x["date"] or "") > asof):
            continue
        tag = f"{x['stock']} ({x['date']})"
        if x["date"] not in ahead10:
            continue
        note = f"{x.get('text') or ''} {x.get('plan') or ''}"
        if pl.num(x["implied_pct"]) is None:
            if re.search(r"implied move (unavailable|not available)", note, flags=re.I):   # an absence: what was tried, when
                why = unavailable_reason_problem(note)
                if why:
                    (thin5 if x["date"] in ahead5 else thin10).append(f"{tag}: {why}")
                else:
                    documented.append(tag)
            elif x["date"] in ahead5:
                no_move5.append(tag)
            else:
                no_move10.append(tag)
        elif not _SOURCE.search(note):
            unsourced.append(tag)
        problem = last_order_problem(x, pl, mkt.get(x["stock"]))
        if problem:
            (late5 if x["date"] in ahead5 else late10).append(f"{x['stock']} ({x['date']}): {problem}")
    if no_move5:
        r.fail("results", "no implied move for a report inside five sessions: " + ", ".join(sorted(no_move5)))
    if thin5:
        r.fail("results", "implied move recorded as unavailable without a usable reason, report inside five sessions: " + "; ".join(sorted(thin5)))
    if no_move10:
        r.warn("results", "no implied move yet for a report inside ten sessions: " + ", ".join(sorted(no_move10)))
    if thin10:
        r.warn("results", "implied move recorded as unavailable without a usable reason: " + "; ".join(sorted(thin10)))
    if documented:
        r.warn("results", "implied move recorded as unavailable (the 6% in RESULTS TOTAL is an assumption, not a market "
               "estimate): " + ", ".join(sorted(documented)))
    if unsourced:
        r.warn("results", "implied move stored without naming its source in the event's text: " + ", ".join(sorted(unsourced)))
    if late5:
        r.fail("results", "last order for a report inside five sessions is missing or later than the rule allows: " + "; ".join(sorted(late5)))
    if late10:
        r.warn("results", "last order for a report inside ten sessions is missing or later than the rule allows: " + "; ".join(sorted(late10)))
    if not (missing_ev or wrong or dups or no_move5 or thin5 or late5):
        r.ok("results", f"every holding's results date has an event on that date (as of {asof})")

    # sync record
    sync = repo / "state" / "last-sync.md"
    run_at = None
    if not sync.exists():
        r.fail("sync", "state/last-sync.md is missing")
    else:
        text = sync.read_text(encoding="utf-8")
        m = re.search(r"Run:[^\n]*?(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ)", text)
        run_at = dt.datetime.strptime(m.group(1), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc) if m else None
        listed = [(h, f) for h, f in re.findall(r"^([0-9a-f]{64})\s+\*?(\S+)\s*$", text, flags=re.M)
                  if f.startswith(("data/", "state/"))]              # what the nightly mirror (G6) records
        bad = []
        for h, f in listed:
            p = repo / f
            if not p.exists():
                bad.append(f"{f} missing")
            elif sha256(p) != h:
                bad.append(f"{f} differs")
        absent = [f for f in REQUIRED_SYNC if f not in {f_ for _h, f_ in listed}]       # 7.6: the whole manifest
        if not listed:
            r.fail("sync", "no file hashes found in state/last-sync.md")
        if absent:
            r.fail("sync", f"state/last-sync.md does not record {', '.join(absent)}: every mirror records all {len(REQUIRED_SYNC)} files")
        if bad:
            r.fail("sync", "files changed since the last sync record: " + ", ".join(bad))
        if listed and not absent and not bad:
            r.ok("sync", f"all {len(listed)} files match state/last-sync.md" + (f" (run {m.group(1)})" if m else ""))

    # freshness
    if fresh:
        exp = expected_session(now, pl)
        age = (now - run_at).total_seconds() / 3600 if run_at else None
        if run_at is None:
            r.fail("fresh", "no run time in state/last-sync.md")
        elif age > FRESH_HOURS or age < -0.25:
            r.fail("fresh", f"the last mirror ran {age:.1f} hours ago ({run_at:%Y-%m-%d %H:%M}Z); expected within {FRESH_HOURS}")
        else:
            r.ok("fresh", f"the last mirror ran {age:.1f} hours ago")
        if exp and (not bench_dates or bench_dates[-1] < exp):
            r.fail("fresh", f"benchmark prices end at {bench_dates[-1] if bench_dates else 'nothing'}; the latest closed US session is {exp}")
        elif exp and last_perf != exp:
            r.fail("fresh", f"performance recorded to {last_perf}; the latest closed US session is {exp}")
        elif exp:
            r.ok("fresh", f"prices and performance run to {exp}, the latest closed US session")
    return r


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", type=Path, default=REPO)
    ap.add_argument("--fresh", action="store_true", help="also check that the latest nightly mirror is recent and complete")
    ap.add_argument("--now", help="the time to check against, YYYY-MM-DDTHH:MM:SSZ (default: the clock)")
    a = ap.parse_args(argv)
    now = (dt.datetime.strptime(a.now, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc) if a.now
           else dt.datetime.now(dt.timezone.utc).replace(microsecond=0))
    pl = load_pipeline()
    rep = check(a.repo.resolve(), now, a.fresh, pl)
    print(f"Data check at {now:%Y-%m-%dT%H:%M:%SZ} (pipeline {pl.PIPELINE_VERSION}):")
    for line in rep.lines:
        print("  " + line)
    print(f"{'FAILED' if rep.failed else 'PASSED'}: {rep.failed} failure(s), "
          f"{sum(1 for x in rep.lines if x.startswith('WARN'))} warning(s)")
    return 1 if rep.failed else 0


if __name__ == "__main__":
    sys.exit(main())
