"""Claude's own reproductions of ChatGPT's PR #5 findings (19 Oct 2026, late evening).

Written independently of ChatGPT's review_checks.py: every case is built here from the pipeline's public functions
and the frozen 16 Oct snapshot or the synthetic 20 to 27 Nov calendar in tests/test_calendar.py. Expected figures are
computed by hand from prices, never by calling the pipeline's own valuation.

    python3 proposals/claude/2026-10-19-evidence-4/repro_pr5.py --repo <checkout>  [--data snapshot|live]

Prints one JSON object. Every key ends in a verdict: "defect" when the code does what the finding says, "ok" when it
does not. It writes only to a temporary folder.
"""
import argparse
import contextlib
import copy
import datetime as dt
import gzip
import hashlib
import importlib.util
import io
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--repo", type=Path, required=True)
ap.add_argument("--data", choices=["snapshot", "live"], default="snapshot")
A = ap.parse_args()
REPO = A.repo.resolve()
sys.path.insert(0, str(REPO / "tests"))


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


pl = load(REPO / "scripts/ft_pipeline.py", "repro_pipeline")
ck = load(REPO / "scripts/check_data.py", "repro_check")
cal = load(REPO / "tests/test_calendar.py", "repro_calendar")
OUT = {"pipeline_version": pl.PIPELINE_VERSION,
       "pipeline_sha256": hashlib.sha256((REPO / "scripts/ft_pipeline.py").read_bytes()).hexdigest()}


def reset():
    pl._SERIES.clear()
    pl.INCOMPLETE.clear()
    pl.WARN.clear()


def data_folder(tmp):
    """data/ and state/last-sync.md: the frozen 16 Oct snapshot, or the live data/ files of the checkout."""
    (tmp / "data").mkdir()
    (tmp / "state").mkdir()
    snap = REPO / "tests/fixtures/snapshot-2026-10-16"
    for n in ("history", "ledger", "macro", "panel", "stocks"):
        if A.data == "snapshot":
            with gzip.open(snap / f"{n}.json.gz", "rb") as s, open(tmp / "data" / f"{n}.json", "wb") as d:
                shutil.copyfileobj(s, d)
        else:
            shutil.copy(REPO / "data" / f"{n}.json", tmp / "data" / f"{n}.json")
    shutil.copy(snap / "last-sync.md" if A.data == "snapshot" else REPO / "state/last-sync.md", tmp / "state/last-sync.md")
    if A.data == "snapshot":
        # the frozen manifest left out the state doc that the real f9241ee mirror recorded; restore it in this copy so
        # the baseline is a complete manifest (the state doc is that commit's, read from git)
        import subprocess
        doc = subprocess.run(["git", "-C", str(REPO), "show", "f9241ee:state/ft-game-state.md"], capture_output=True, check=True).stdout
        (tmp / "state/ft-game-state.md").write_bytes(doc)
        t = (tmp / "state/last-sync.md").read_text(encoding="utf-8").rstrip("\n")
        (tmp / "state/last-sync.md").write_text(t[:-3] + hashlib.sha256(doc).hexdigest() + "  state/ft-game-state.md\n~~~\n", encoding="utf-8")
    if A.data == "live":
        shutil.copy(REPO / "state/ft-game-state.md", tmp / "state/ft-game-state.md")


def resync(tmp):
    """Rewrite the hashes in last-sync.md honestly after a deliberate edit, so only the edited content is on trial."""
    p = tmp / "state/last-sync.md"
    t = p.read_text(encoding="utf-8")
    for f in re.findall(r"^[0-9a-f]{64}\s+(\S+)\s*$", t, flags=re.M):
        if (tmp / f).exists():
            h = hashlib.sha256((tmp / f).read_bytes()).hexdigest()
            t = re.sub(r"^[0-9a-f]{64}(\s+" + re.escape(f) + r"\s*)$", h + r"\1", t, flags=re.M)
    p.write_text(t, encoding="utf-8")


def run_check(tmp, now="2026-10-19T19:00:00Z"):
    reset()
    rep = ck.check(tmp, dt.datetime.strptime(now, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc), False, pl)
    return rep


def jl(p):
    return json.loads(p.read_text(encoding="utf-8"))


def jw(p, x):
    p.write_text(json.dumps(x), encoding="utf-8")


def add_abbvie(ledger):
    """The event the 19 Oct evening review is due to add (state doc section 2), so the other checks are reached."""
    if not any(r["table"] == "event" and r["kind"] == "results" and r["stock"] == "AbbVie" for r in ledger):
        r = pl.lrow("event", kind="results", stock="AbbVie", name="AbbVie results", date="2026-10-30",
                    time_uk="before US open", last_order="Before 07:00 Thu 29 Oct", confirmed="yes")
        r["id"] = "event:2026-10-30:AbbVie results"
        ledger.append(r)
    return ledger


# ---------------------------------------------------------------- F2: dated earnings coverage
with tempfile.TemporaryDirectory() as t:
    tmp = Path(t)
    data_folder(tmp)
    lp = tmp / "data/ledger.json"
    L0 = add_abbvie(jl(lp))
    jw(lp, L0)
    resync(tmp)
    base = run_check(tmp)
    held = {n: w for n, (w, _t) in pl.live_weights(L0, "9999-12-31").items()}
    reset()
    tot_base = pl.results_total(L0, held, "2026-10-16")[10]
    # (a) Coca-Cola's only event moved to a date outside the game
    L = copy.deepcopy(L0)
    for r in L:
        if r["table"] == "event" and r["kind"] == "results" and r["stock"] == "Coca-Cola":
            r["date"] = "2027-01-15"
    jw(lp, L)
    resync(tmp)
    rep = run_check(tmp)
    reset()
    tot = pl.results_total(L, held, "2026-10-16")[10]
    stocks = {s["name"]: s for s in jl(tmp / "data/stocks.json")}
    miss = pl.missing_results_events(L, {n: stocks[n]["next_results"] for n in held}, "2026-10-16")
    OUT["F2a_wrong_date"] = {"check_failures": rep.failed, "check_failures_with_correct_date": base.failed,
                             "results_lines": [x for x in rep.lines if " results:" in x],
                             "pipeline_results_missing": [m[0] for m in miss],
                             "ten_session_total_pts": round(tot[0], 3), "with_correct_date_pts": round(tot_base[0], 3),
                             "verdict": "defect" if rep.failed == base.failed and not miss else "ok"}
    # (b) a duplicate event: a second Coca-Cola results event on the right date
    L = copy.deepcopy(L0)
    dup = copy.deepcopy(next(r for r in L if r["table"] == "event" and r["kind"] == "results" and r["stock"] == "Coca-Cola"))
    dup["id"] = dup["id"] + ":2"
    L.append(dup)
    jw(lp, L)
    resync(tmp)
    rep = run_check(tmp)
    reset()
    tot = pl.results_total(L, held, "2026-10-16")[10]
    OUT["F2b_duplicate_event"] = {"check_failures": rep.failed, "ten_session_total_pts": round(tot[0], 3),
                                  "reports_counted": tot[1], "correct_pts": round(tot_base[0], 3),
                                  "verdict": "defect" if rep.failed == base.failed or abs(tot[0] - tot_base[0]) > 1e-9 else "ok"}
    # (c) a genuinely uncertain date, marked as such: must be reported as uncertain, not silently passed or failed
    L = copy.deepcopy(L0)
    for r in L:
        if r["table"] == "event" and r["kind"] == "results" and r["stock"] == "Coca-Cola":
            r["date"], r["confirmed"] = "2026-10-28", "uncertain"
            r["text"] = "Date unconfirmed: company IR page says 27 Oct, Nasdaq calendar says 28 Oct (checked 19 Oct)"
    jw(lp, L)
    resync(tmp)
    rep = run_check(tmp)
    OUT["F2c_uncertain_marked"] = {"check_failures": rep.failed, "lines": [x for x in rep.lines if " results:" in x]}

# ---------------------------------------------------------------- F3: hindsight through reorder
with tempfile.TemporaryDirectory() as t:
    tmp = Path(t)
    data_folder(tmp)
    L = jl(tmp / "data/ledger.json")
    last_perf = max(r["date"] for r in L if r["table"] == "perf")
    eff = last_perf
    wts = pl.live_weights(L, eff)
    order = [{"name": n, "weight": w, "confidence": 55} for n, (w, _t) in wts.items()]
    names = sorted(wts)
    order = [dict(x) for x in order]
    # a real change on the completed session: move 5 points between the two first names
    order[0]["weight"] -= 5
    order[1]["weight"] += 5
    res = {}
    for label, entered in (("entered_same_day", eff), ("entered_next_day", (dt.date.fromisoformat(eff) + dt.timedelta(days=1)).isoformat())):
        o = {"order": order, "effective": eff, "entered": entered,
             "order_expected": {"pts": 9.99, "thesis": "written after the close of " + eff, "invalidation": "n/a"}}
        jw(tmp / "o.json", o)
        reset()
        with contextlib.redirect_stdout(io.StringIO()):
            pl.cmd_reorder({"stocks": str(tmp / "data/stocks.json"), "ledger": str(tmp / "data/ledger.json"),
                            "order": str(tmp / "o.json"), "out": str(tmp / ("out_" + label))})
        out = jl(tmp / ("out_" + label) / "ledger.json")
        res[label] = {"accepted": [r["forecast"] for r in out if r["table"] == "expect" and r["effective"] == eff],
                      "warnings": list(pl.WARN)}
    OUT["F3_reorder_after_completed_session"] = {"effective": eff, "latest_perf_session": last_perf, **res,
                                                 "verdict": "defect" if res["entered_same_day"]["accepted"] else "ok"}

# ---------------------------------------------------------------- F4 and F5: 26 and 27 Nov
def value27(L, hist):
    reset()
    with contextlib.redirect_stdout(io.StringIO()):
        pl.update_performance(L, hist, "SPY", "2026-11-27")
    p = cal.perf(L)
    return (p["2026-11-27"]["value_est"] if "2026-11-27" in p else None), list(pl.INCOMPLETE)


v_ok, inc = value27(cal.london_change_on_26(pl), cal.history())
OUT["F4_control_real_26_open"] = {"value": v_ok, "incomplete": inc}
for label in ("missing_26_row", "imputed_26_open"):
    h = cal.history()
    if label == "missing_26_row":
        del h[("UKB", "2026-11-26")]
    else:
        h[("UKB", "2026-11-26")]["open_obs"] = False
    v, inc = value27(cal.london_change_on_26(pl), h)
    # hand value if the 27 Nov open were (wrongly) used for both London legs
    v25 = cal.chain([0.0] + cal.first_days({"USA": 50, "UKA": 50}))
    wrong = v25 * (1 + (cal.kept(50, "USA", "2026-11-25", "2026-11-27") + cal.kept(30, "UKA", "2026-11-25", "2026-11-27")
                        + 20 * (cal.o("UKA", "2026-11-27") / cal.c("UKA", "2026-11-25") - 1)
                        + 20 * (cal.c("UKB", "2026-11-27") / cal.o("UKB", "2026-11-27") - 1)) / 100)
    OUT["F4_" + label] = {"value": v, "incomplete": inc, "value_if_27_open_used": round(wrong, 2),
                          "verdict": "defect" if v is not None and not inc else "ok"}
# the London leg's sale side too: UK One sold at an unobserved 26 Nov open
h = cal.history()
h[("UKA", "2026-11-26")]["open_obs"] = False
v, inc = value27(cal.london_change_on_26(pl), h)
OUT["F4_sale_leg_imputed_26_open"] = {"value": v, "incomplete": inc, "verdict": "defect" if v is not None and not inc else "ok"}

# F5: UK One 50 -> 30 and UK Two 0 -> 20 filling 26 Nov, then UK One 30 -> 20 and UK Two 20 -> 30 filling 27 Nov
L = cal.london_change_on_26(pl)
L += cal.ledger(pl, [("2026-11-27", "UKA", 20), ("2026-11-27", "UKB", 30)])[3:]
v, inc = value27(L, cal.history())
v25 = cal.chain([0.0] + cal.first_days({"USA": 50, "UKA": 50}))
o_, c_ = cal.o, cal.c
# by hand, under M3 (no reset at the 26 Nov close, so 26 and 27 Nov are one line): each leg priced at its own fill
pts = (cal.kept(50, "USA", "2026-11-25", "2026-11-27")
       + 20 * (c_("UKA", "2026-11-27") / c_("UKA", "2026-11-25") - 1)           # 20 of UK One held throughout
       + 20 * (o_("UKA", "2026-11-26") / c_("UKA", "2026-11-25") - 1)           # 20 sold at the 26 Nov open
       + 10 * (o_("UKA", "2026-11-27") / c_("UKA", "2026-11-25") - 1)           # 10 sold at the 27 Nov open
       + 20 * (c_("UKB", "2026-11-27") / o_("UKB", "2026-11-26") - 1)           # 20 bought at the 26 Nov open
       + 10 * (c_("UKB", "2026-11-27") / o_("UKB", "2026-11-27") - 1))          # 10 bought at the 27 Nov open
want = round(v25 * (1 + pts / 100), 2)
reset()
ch = [r for r in pl.standstill_rows(L, cal.history(), "SPY", "2026-11-27") if r["kind"] == "change"]
OUT["F5_changes_on_26_and_27"] = {"value": v, "hand_value": want, "difference": None if v is None else round(v - want, 2),
                                  "incomplete": inc,
                                  "standstill": [{"name": r["name"], "value": r["value"], "text": r["text"]} for r in ch],
                                  "verdict": "defect" if v is None or abs(v - want) > 0.02 or len(ch) < 2
                                  or (len(ch) >= 2 and ch[-1]["value"] == ch[-2]["value"]) else "ok"}

# ---------------------------------------------------------------- F6: deadlines
cases = {
    "london_0700_report_27_nov_valid": ({"date": "2026-11-27", "time_uk": "07:00", "stock": "Shell", "last_order": "Before 07:00 Thu 26 Nov"}, None),
    "us_preopen_report_27_nov_valid": ({"date": "2026-11-27", "time_uk": "before US open", "stock": "Coca-Cola", "last_order": "Before 07:00 Wed 25 Nov"}, None),
    "us_preopen_report_27_nov_too_late": ({"date": "2026-11-27", "time_uk": "before US open", "stock": "Coca-Cola", "last_order": "Before 07:00 Thu 26 Nov"}, "problem"),
    "after_close_valid": ({"date": "2026-10-28", "time_uk": "after US close", "stock": "Microsoft", "last_order": "Before 07:00 Wed 28 Oct"}, None),
    "no_time": ({"date": "2026-10-28", "time_uk": "after US close", "stock": "Microsoft", "last_order": "Any time Wed 28 Oct"}, "problem"),
    "after_wording": ({"date": "2026-10-28", "time_uk": "after US close", "stock": "Microsoft", "last_order": "After 07:00 Wed 28 Oct"}, "problem"),
    "old_0800": ({"date": "2026-10-29", "time_uk": "07:00", "stock": "Shell", "last_order": "Before 08:00 Wed 28 Oct"}, "problem"),
}
markets = {"Shell": "UK", "Coca-Cola": "US", "Microsoft": "US"}
res = {}
for k, (ev, want) in cases.items():
    try:
        got = ck.last_order_problem(ev, pl, markets.get(ev["stock"]))
    except TypeError:
        got = ck.last_order_problem(ev, pl)
    res[k] = {"problem": got, "expected": "a problem" if want else "none",
              "verdict": "ok" if bool(got) == bool(want) else "defect"}
OUT["F6_last_order"] = res

# ---------------------------------------------------------------- F7: integrity coverage
with tempfile.TemporaryDirectory() as t:
    tmp = Path(t)
    data_folder(tmp)
    lp = tmp / "data/ledger.json"
    L0 = add_abbvie(jl(lp))
    jw(lp, L0)
    resync(tmp)
    sp = tmp / "state/last-sync.md"
    sync0 = sp.read_text(encoding="utf-8")
    base = run_check(tmp)
    OUT["F7_control"] = {"failures": base.failed, "fail_lines": [x for x in base.lines if x.startswith("FAIL")]}
    # (a) a manifest listing one file
    st = tmp / "data/stocks.json"
    sp.write_text("Run: test 2026-10-19T18:58:17Z\n" + hashlib.sha256(st.read_bytes()).hexdigest() + "  data/stocks.json\n", encoding="utf-8")
    rep = run_check(tmp)
    OUT["F7a_one_file_manifest"] = {"failures_added": rep.failed - base.failed, "sync": [x for x in rep.lines if " sync:" in x],
                                    "verdict": "defect" if rep.failed == base.failed else "ok"}
    sp.write_text(sync0, encoding="utf-8")
    # (b) every contribution row deleted, hashes rewritten honestly
    jw(lp, [r for r in L0 if r["table"] != "contrib"])
    resync(tmp)
    rep = run_check(tmp)
    OUT["F7b_contributions_deleted"] = {"failures_added": rep.failed - base.failed,
                                        "performance": [x for x in rep.lines if " performance:" in x],
                                        "verdict": "defect" if rep.failed == base.failed else "ok"}
    # (b2) one holding's contribution row deleted on one day only (the sum then no longer matches): control
    one = next(r for r in L0 if r["table"] == "contrib" and abs(pl.num(r["contrib_pts"]) or 0) > 0.05)
    jw(lp, [r for r in L0 if r is not one])
    resync(tmp)
    rep = run_check(tmp)
    OUT["F7b2_one_contribution_deleted"] = {"failures_added": rep.failed - base.failed,
                                            "performance": [x for x in rep.lines if " performance:" in x]}
    # (b3) a whole day's contribution rows deleted
    d0 = one["date"]
    jw(lp, [r for r in L0 if not (r["table"] == "contrib" and r["date"] == d0)])
    resync(tmp)
    rep = run_check(tmp)
    OUT["F7b3_one_day_contributions_deleted"] = {"day": d0, "failures_added": rep.failed - base.failed,
                                                 "verdict": "defect" if rep.failed == base.failed else "ok"}
    # (c) a report inside five sessions marked "Implied move unavailable" with no reason
    L = copy.deepcopy(L0)
    for r in L:
        if r["table"] == "event" and r["kind"] == "results" and r["stock"] == "Coca-Cola":
            r["date"], r["implied_pct"], r["text"], r["plan"] = "2026-10-21", None, "Implied move unavailable", ""
            r["time_uk"], r["last_order"] = "before US open", "Before 07:00 Tue 20 Oct"
    s = jl(tmp / "data/stocks.json")
    for x in s:
        if x["name"] == "Coca-Cola":
            x["next_results"] = "21 Oct, before US open"
    jw(tmp / "data/stocks.json", s)
    jw(lp, L)
    resync(tmp)
    rep = run_check(tmp)
    bare = rep.failed
    for r in L:
        if r["table"] == "event" and r["kind"] == "results" and r["stock"] == "Coca-Cola":
            r["text"] = "Implied move unavailable: Barchart and Market Chameleon pages refused on 19 Oct 2026 (21:40 UK); no option chain readable"
    jw(lp, L)
    resync(tmp)
    rep2 = run_check(tmp)
    OUT["F7c_bare_unavailable"] = {"failures_bare": bare - base.failed, "failures_with_reason": rep2.failed - base.failed,
                                   "lines_bare": [x for x in rep.lines if " results:" in x],
                                   "verdict": "defect" if bare == base.failed else "ok"}

print(json.dumps(OUT, indent=1))
