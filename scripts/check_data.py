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
              compounds from the one before; contributions add up to the day's return (weight x return)
  results     every holding whose next-results text names a date has a results event on that date;
              an implied move is missing for a report inside five sessions (FAIL) or inside ten (WARN)
  sync        each data/ and state/ file listed in state/last-sync.md has the sha256 recorded there
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
        contrib = {}
        for x in ledger:
            if x["table"] == "contrib" and pl.num(x["contrib_pts"]) is not None:
                contrib[x["date"]] = contrib.get(x["date"], 0.0) + pl.num(x["contrib_pts"])
        for x in perf:
            if x["date"] in contrib and abs(contrib[x["date"]] - (pl.num(x["day_pct"]) or 0)) > 0.01:
                errs.append(f"{x['date']}: contributions add to {contrib[x['date']]:+.3f} points against a day's return of {x['day_pct']:+.3f}%")
    if errs:
        r.fail("performance", "; ".join(errs[:6]))
    elif perf:
        r.ok("performance", f"{len(perf)} sessions to {perf[-1]['date']}, none missing, values compound, contributions add up")
    else:
        r.warn("performance", "no performance rows yet")
    last_perf = perf[-1]["date"] if perf else None
    if bench_dates and last_perf and bench_dates[-1] > last_perf:
        r.warn("performance", f"benchmark prices run to {bench_dates[-1]} but performance only to {last_perf} (PERFORMANCE INCOMPLETE)")

    # results events and implied moves
    asof = last_perf or (bench_dates[-1] if bench_dates else today_utc)
    nexts = {x["name"]: x.get("next_results") for x in stocks if x["name"] in held}
    missing_ev = pl.missing_results_events(ledger, nexts, asof)
    if missing_ev:
        r.fail("results", "holding(s) with a results date but no results event: "
               + ", ".join(f"{n} ({d})" for n, d, _ in missing_ev))
    ahead5, ahead10 = set(pl._sessions_ahead(asof, 5)), set(pl._sessions_ahead(asof, 10))
    no_move5, no_move10 = [], []
    for x in ledger:
        if x["table"] == "event" and x["kind"] == "results" and x["stock"] in held and pl.num(x["implied_pct"]) is None:
            if x["date"] in ahead5:
                no_move5.append(f"{x['stock']} ({x['date']})")
            elif x["date"] in ahead10:
                no_move10.append(f"{x['stock']} ({x['date']})")
    if no_move5:
        r.fail("results", "no implied move for a report inside five sessions: " + ", ".join(sorted(no_move5)))
    if no_move10:
        r.warn("results", "no implied move yet for a report inside ten sessions: " + ", ".join(sorted(no_move10)))
    if not (missing_ev or no_move5):
        r.ok("results", f"every holding's results date has an event (as of {asof})")

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
        if not listed:
            r.fail("sync", "no file hashes found in state/last-sync.md")
        elif bad:
            r.fail("sync", "files changed since the last sync record: " + ", ".join(bad))
        else:
            r.ok("sync", f"{len(listed)} files match state/last-sync.md" + (f" (run {m.group(1)})" if m else ""))

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
