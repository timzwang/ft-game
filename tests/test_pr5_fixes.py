"""Version 7.6 (prepared 19 Oct 2026, late evening): regression tests for the gaps ChatGPT's independent review of 7.5
reproduced (PR #5), each with a negative case that failed on 7.5 and a positive control that must still pass.

Expected figures are computed here by hand from the synthetic prices in test_calendar.py, never from the pipeline's
own valuation. Assumptions M1 to M3 (test_calendar.py) still apply: how the FT itself fills a mixed order on 26 Nov
and whether it resets weights at the 26 Nov London close are NOT established by these tests.
"""
import copy
import json

import pytest

from test_calendar import MARKETS, V0, c, chain, first_days, history, kept, ledger, london_change_on_26, o, perf
from test_check_data import cd, edit, resync, run, tmp_repo  # noqa: F401  (fixtures)

def v25():
    return chain([0.0] + first_days({"USA": 50, "UKA": 50}))


def control_26_value():
    """Test 6's hand value: UK One 50 to 30 and UK Two 0 to 20 filling at the 26 Nov London opens."""
    d27 = (kept(50, "USA", "2026-11-25", "2026-11-27") + kept(30, "UKA", "2026-11-25", "2026-11-27")
           + 20 * (o("UKA", "2026-11-26") / c("UKA", "2026-11-25") - 1)
           + 20 * (c("UKB", "2026-11-27") / o("UKB", "2026-11-26") - 1))
    return v25() * (1 + d27 / 100)


# ------------------------------------------------------------------ finding 4: a missing or estimated 26 Nov London open

@pytest.mark.parametrize("ticker,how", [("UKB", "missing"), ("UKB", "estimated"), ("UKA", "estimated"), ("UKA", "missing")])
def test_missing_or_estimated_26_nov_london_open_waits(pl, ticker, how):
    """Expected: London traded on 26 Nov, so a buy (UK Two) or sale (UK One) filling then without a traded 26 Nov open
    cannot be priced; the 27 Nov line waits (PERFORMANCE INCOMPLETE) instead of using the 27 Nov open. 7.5 recorded
    107,964.31 (or 107,926.95 for the sale) with no warning."""
    h = history()
    if how == "missing":
        del h[(ticker, "2026-11-26")]
    else:
        h[(ticker, "2026-11-26")]["open_obs"] = False
    L = london_change_on_26(pl)
    pl.update_performance(L, h, "SPY", "2026-11-27", markets=MARKETS)
    assert "2026-11-27" not in perf(L)
    assert pl.INCOMPLETE and "2026-11-26" in pl.INCOMPLETE[0] and ticker in pl.INCOMPLETE[0]


def test_26_nov_open_arriving_later_completes_the_line(pl):
    """Positive control: once the 26 Nov row is given, the next run records the hand value (test 6)."""
    h = history()
    row = h.pop(("UKB", "2026-11-26"))
    L = london_change_on_26(pl)
    pl.update_performance(L, h, "SPY", "2026-11-27", markets=MARKETS)
    assert "2026-11-27" not in perf(L)
    pl.INCOMPLETE.clear()
    h[("UKB", "2026-11-26")] = row
    pl.update_performance(L, h, "SPY", "2026-11-27", markets=MARKETS)
    assert not pl.INCOMPLETE
    assert perf(L)["2026-11-27"]["value_est"] == pytest.approx(control_26_value(), abs=0.01)


def test_stated_fill_price_is_an_explicit_fill(pl):
    """Expected: with no 26 Nov row but a fill price stated for the buy (as the game shows it), the buy is priced at
    that price; no next-day open is substituted."""
    h = history()
    del h[("UKB", "2026-11-26")]
    L = london_change_on_26(pl)
    for r in L:
        if r["table"] == "position" and r["name"] == "UK Two" and r["effective"] == "2026-11-26":
            r["value"] = 478.0
    pl.update_performance(L, h, "SPY", "2026-11-27", markets=MARKETS)
    d27 = (kept(50, "USA", "2026-11-25", "2026-11-27") + kept(30, "UKA", "2026-11-25", "2026-11-27")
           + 20 * (o("UKA", "2026-11-26") / c("UKA", "2026-11-25") - 1) + 20 * (c("UKB", "2026-11-27") / 478.0 - 1))
    assert not pl.INCOMPLETE
    assert perf(L)["2026-11-27"]["value_est"] == pytest.approx(v25() * (1 + d27 / 100), abs=0.01)


def test_unknown_market_without_a_row_waits(pl):
    """Expected: with no listing market known, a missing 26 Nov row could be a shut market or a missing quote, so the
    line waits rather than guess. (Test 6 is the control: an unknown market WITH a traded 26 Nov row uses it.)"""
    h = history()
    del h[("UKB", "2026-11-26")]
    L = london_change_on_26(pl)
    pl.update_performance(L, h, "SPY", "2026-11-27")
    assert "2026-11-27" not in perf(L) and "not known" in pl.INCOMPLETE[0]


def test_listing_market_is_kept_in_the_ledger(pl):
    """Expected: the listing_market meta row written by `run` is what a later rebuild uses (check_data's recalc too):
    the US legs of test 6b then fill at the 27 Nov open without the caller passing markets."""
    L = london_change_on_26(pl, us_leg=True)
    L = pl.keep_listing_markets(L, MARKETS)
    assert json.loads(next(r for r in L if r["table"] == "meta" and r["name"] == "listing_market")["text"]) == MARKETS
    before = len(L)
    L = pl.keep_listing_markets(L, {"USA": "US"})                      # nothing new: no second row, no rewrite
    assert len(L) == before
    pl.update_performance(L, history(), "SPY", "2026-11-27")
    assert not pl.INCOMPLETE and "2026-11-27" in perf(L)


def test_us_leg_on_its_own_holiday_still_fills_next_session(pl):
    """Control for M2: a US stock ordered for 26 Nov (its market shut) fills at the 27 Nov open with no 26 Nov row."""
    assert pl.market_open("US", "2026-11-26") is False and pl.market_open("UK", "2026-11-26") is True
    assert pl.market_open(None, "2026-11-26") is None and pl.market_open("UK", "2026-11-28") is False


# ------------------------------------------------------------------ finding 5: changes on both 26 and 27 Nov

def both_days(pl):
    L = london_change_on_26(pl)
    L += ledger(pl, [("2026-11-27", "UKA", 20), ("2026-11-27", "UKB", 30)])[3:]
    return L


def test_changes_on_26_and_27_nov_are_each_priced(pl):
    """Expected (M3, no reset at the 26 Nov close): UK One 50 -> 30 at the 26 Nov open then -> 20 at the 27 Nov open;
    UK Two 0 -> 20 at the 26 Nov open then -> 30 at the 27 Nov open; every leg at its own open. 7.5 kept only the
    27 Nov weights and priced the whole move at the 27 Nov open: 108,359.20 against 107,104.45."""
    L = both_days(pl)
    pl.update_performance(L, history(), "SPY", "2026-11-27", markets=MARKETS)
    pts = (kept(50, "USA", "2026-11-25", "2026-11-27") + kept(20, "UKA", "2026-11-25", "2026-11-27")
           + 20 * (o("UKA", "2026-11-26") / c("UKA", "2026-11-25") - 1) + 10 * (o("UKA", "2026-11-27") / c("UKA", "2026-11-25") - 1)
           + 20 * (c("UKB", "2026-11-27") / o("UKB", "2026-11-26") - 1) + 10 * (c("UKB", "2026-11-27") / o("UKB", "2026-11-27") - 1))
    assert not pl.INCOMPLETE
    assert perf(L)["2026-11-27"]["value_est"] == pytest.approx(v25() * (1 + pts / 100), abs=0.01)
    assert perf(L)["2026-11-27"]["value_est"] == pytest.approx(107104.45, abs=0.01)
    contrib = {r["name"]: r["contrib_pts"] for r in L if r["table"] == "contrib" and r["date"] == "2026-11-27"}
    assert sum(contrib.values()) == pytest.approx(perf(L)["2026-11-27"]["day_pct"], abs=0.002)


def test_bought_on_26_and_sold_on_27_is_priced_open_to_open(pl):
    """Expected: a London stock bought at the 26 Nov open and sold at the 27 Nov open earns 27 open over 26 open (the
    most recent lot is sold first) and still gets a contribution row, though it is held at neither close."""
    L = ledger(pl, [("2026-11-20", "USA", 50), ("2026-11-20", "UKA", 50),
                    ("2026-11-26", "UKA", 30), ("2026-11-26", "UKB", 20), ("2026-11-27", "UKA", 50), ("2026-11-27", "UKB", 0)])
    pl.update_performance(L, history(), "SPY", "2026-11-27", markets=MARKETS)
    ukb = 20 * (o("UKB", "2026-11-27") / o("UKB", "2026-11-26") - 1)
    uka = (30 * (c("UKA", "2026-11-27") / c("UKA", "2026-11-25") - 1) + 20 * (o("UKA", "2026-11-26") / c("UKA", "2026-11-25") - 1)
           + 20 * (c("UKA", "2026-11-27") / o("UKA", "2026-11-27") - 1))
    contrib = {r["name"]: r["contrib_pts"] for r in L if r["table"] == "contrib" and r["date"] == "2026-11-27"}
    assert contrib["UK Two"] == pytest.approx(ukb, abs=0.001) and contrib["UK One"] == pytest.approx(uka, abs=0.001)


def test_missing_27_nov_open_for_the_second_change_waits(pl):
    """Negative: the second change's legs need the 27 Nov open; an estimated one stops the line."""
    h = history()
    h[("UKB", "2026-11-27")]["open_obs"] = False
    L = both_days(pl)
    pl.update_performance(L, h, "SPY", "2026-11-27", markets=MARKETS)
    assert "2026-11-27" not in perf(L) and pl.INCOMPLETE


def test_standstill_judges_each_change_against_the_order_it_replaced(pl):
    """Expected: two change rows with different values. 26 Nov: the 26 Nov order against the 25 Nov order. 27 Nov: the
    27 Nov order against the 26 Nov order, both paths having made the 26 Nov change at the 26 Nov opens. 7.5 gave both
    rows -0.614 and described both as 'UK One 50 to 20, UK Two 0 to 30'."""
    rows = {r["name"]: r for r in pl.standstill_rows(pl.keep_listing_markets(both_days(pl), MARKETS), history(), "SPY", "2026-11-27")
            if r["kind"] == "change"}
    r26, r27 = rows["Change for 2026-11-26"], rows["Change for 2026-11-27"]
    want26 = (20 * (o("UKA", "2026-11-26") / c("UKA", "2026-11-25") - 1) + 20 * (c("UKB", "2026-11-27") / o("UKB", "2026-11-26") - 1)
              - 20 * (c("UKA", "2026-11-27") / c("UKA", "2026-11-25") - 1))
    want27 = (10 * (o("UKA", "2026-11-27") / c("UKA", "2026-11-25") - 1) - 10 * (c("UKA", "2026-11-27") / c("UKA", "2026-11-25") - 1)
              + 10 * (c("UKB", "2026-11-27") / o("UKB", "2026-11-27") - 1))
    assert r26["value"] == pytest.approx(want26, abs=0.002) and r27["value"] == pytest.approx(want27, abs=0.002)
    assert r26["value"] != r27["value"]
    assert r26["text"] == "UK One 50 to 30, UK Two 0 to 20" and r27["text"] == "UK One 30 to 20, UK Two 20 to 30"


# ------------------------------------------------------------------ finding 3: prospective expectations

def reorder(pl, repo, tmp_path, eff, entered, entered_time=None, history_rows=None, change=True):
    led = json.loads((repo / "data" / "ledger.json").read_text(encoding="utf-8"))
    w = pl.live_weights(led, eff)
    order = [{"name": n, "weight": x, "confidence": 55} for n, (x, _t) in sorted(w.items())]
    if change:
        order[0]["weight"] -= 5
        order[1]["weight"] += 5
    o_ = {"order": order, "effective": eff, "entered": entered, "order_expected": {"pts": 0.3, "thesis": "t", "invalidation": "i"}}
    if entered_time:
        o_["entered_time"] = entered_time
    (tmp_path / "o.json").write_text(json.dumps(o_), encoding="utf-8")
    a = {"stocks": str(repo / "data" / "stocks.json"), "ledger": str(repo / "data" / "ledger.json"),
         "order": str(tmp_path / "o.json"), "out": str(tmp_path / "out")}
    if history_rows is not None:
        (tmp_path / "h.json").write_text(json.dumps(history_rows), encoding="utf-8")
        a["history"] = str(tmp_path / "h.json")
    pl.cmd_reorder(a)
    out = json.loads((tmp_path / "out" / "ledger.json").read_text(encoding="utf-8"))
    return [r for r in out if r["table"] == "expect" and r["effective"] == eff]


@pytest.mark.parametrize("change", [True, False])
def test_reorder_refuses_an_expectation_for_a_completed_session(pl, repo, tmp_path, change, capsys):
    """Negative (finding 3): the 16 Oct session is already in the performance log; an expectation entered 'on' 16 Oct
    for a change filling then is hindsight. 7.5 accepted +0.3 points without a warning."""
    assert reorder(pl, repo, tmp_path, "2026-10-16", "2026-10-16", change=change) == []
    assert any("performance is already recorded for 2026-10-16" in w for w in pl.WARN)


def test_reorder_pre_open_with_a_time_is_kept(pl, repo, tmp_path, capsys):
    """Positive control: the morning check at 06:40 UK for the open of a session not yet traded."""
    x = reorder(pl, repo, tmp_path, "2026-10-19", "2026-10-19", "06:40")
    assert [r["forecast"] for r in x] == [0.3] and x[0]["time_uk"] == "06:40"
    assert not [w for w in pl.WARN if "expected benefit" in w]


@pytest.mark.parametrize("t", ["07:00", "07:20", "21:45", "after close"])
def test_reorder_at_or_after_the_cut_off_is_refused(pl, repo, tmp_path, t, capsys):
    assert reorder(pl, repo, tmp_path, "2026-10-19", "2026-10-19", t) == []
    assert any("hindsight" in w for w in pl.WARN)


def test_reorder_same_day_without_a_time_warns(pl, repo, tmp_path, capsys):
    x = reorder(pl, repo, tmp_path, "2026-10-19", "2026-10-19")
    assert [r["forecast"] for r in x] == [0.3]
    assert any("no entry time" in w for w in pl.WARN)


def test_reorder_with_the_session_already_priced_is_refused(pl, repo, tmp_path, capsys):
    """Negative: no performance line yet, but the benchmark's 19 Oct row is stored, so that session has closed."""
    rows = [{"ticker": "SPY", "date": "2026-10-19", "open": 1, "high": 2, "low": 0.5, "close": 1.5, "volume": 1}]
    assert reorder(pl, repo, tmp_path, "2026-10-19", "2026-10-19", "06:40", history_rows=rows) == []
    assert any("SPY row for 2026-10-19" in w for w in pl.WARN)


def test_one_lock_for_both_entry_paths(pl):
    """run and reorder ask the same function; run adds its own session date."""
    L = [pl.lrow("perf", date="2026-10-16", value_est=V0, day_pct=0.0)]
    assert pl.expectation_lock(L, "2026-10-19", "2026-10-18") is None
    assert "run's session" in pl.expectation_lock(L, "2026-10-19", "2026-10-19", run_date="2026-10-19")
    assert "after the fill date" in pl.expectation_lock(L, "2026-10-19", "2026-10-20")
    assert "performance is already recorded" in pl.expectation_lock(L, "2026-10-16", "2026-10-15")


# ------------------------------------------------------------------ finding 2: dated results coverage

def ko_event(L):
    return next(r for r in L if r["table"] == "event" and r["kind"] == "results" and r["stock"] == "Coca-Cola")


def add_abbvie(L):
    """The event the 19 Oct evening review is due to add (state doc section 2), copied from Exxon's row's shape."""
    x = copy.deepcopy(next(r for r in L if r["table"] == "event" and r["stock"] == "Exxon Mobil" and r["kind"] == "results"))
    x.update({"id": "event:2026-10-30:AbbVie results", "name": "AbbVie results", "stock": "AbbVie",
              "last_order": "Before 07:00 Thu 29 Oct", "confirmed": "yes"})
    L.append(x)


def both(*fns):
    def f(L):
        for fn in fns:
            fn(L)
    return f


@pytest.mark.parametrize("moved,phrase", [("2027-01-15", "no results event"), ("2026-11-12", "not on the date")])
def test_wrong_date_event_does_not_cover(cd, pl, tmp_repo, moved, phrase):  # noqa: F811
    """Negative (finding 2): Coca-Cola's only event moved away from its 27 Oct report, after the game (15 Jan 2027) or
    inside it (12 Nov). 7.5: no FAIL either way; with the January date the ten-session total quietly fell from 6.0 to
    4.8 points. Now RESULTS MISSING in the pipeline and a FAIL in the data check."""
    edit(tmp_repo, "ledger", both(add_abbvie, lambda L: ko_event(L).update(date=moved)))
    resync(cd, tmp_repo)
    fails, _ = run(cd, pl, tmp_repo)
    assert any(f.startswith("FAIL results") and phrase in f and "Coca-Cola" in f for f in fails)
    L = json.loads((tmp_repo / "data" / "ledger.json").read_text(encoding="utf-8"))
    stocks = {s["name"]: s["next_results"] for s in json.loads((tmp_repo / "data" / "stocks.json").read_text(encoding="utf-8"))}
    held = {n: w for n, (w, _t) in pl.live_weights(L, "9999-12-31").items()}
    assert [m[0] for m in pl.missing_results_events(L, {n: stocks[n] for n in held}, "2026-10-16")] == ["Coca-Cola"]


def test_correct_dates_pass(cd, pl, tmp_repo):  # noqa: F811
    """Positive control: every holding with an event on its own date (AbbVie added) passes the results check."""
    edit(tmp_repo, "ledger", add_abbvie)
    resync(cd, tmp_repo)
    fails, rep = run(cd, pl, tmp_repo)
    assert not [f for f in fails if f.startswith("FAIL results")]
    assert any(l.startswith("PASS results: every holding's results date has an event on that date") for l in rep.lines)


def test_duplicate_event_fails_and_counts_once(cd, pl, tmp_repo):  # noqa: F811
    """Negative: a second Coca-Cola event. 7.5 counted both: 7.2 points instead of 6.0 in the ten-session total."""
    def f(L):
        add_abbvie(L)
        d = copy.deepcopy(ko_event(L))
        d["id"] += ":2"
        L.append(d)
    edit(tmp_repo, "ledger", f)
    resync(cd, tmp_repo)
    fails, _ = run(cd, pl, tmp_repo)
    assert any("more than one future results event" in f and "Coca-Cola" in f for f in fails)
    L = json.loads((tmp_repo / "data" / "ledger.json").read_text(encoding="utf-8"))
    held = {n: w for n, (w, _t) in pl.live_weights(L, "9999-12-31").items()}
    pts, k, _m = pl.results_total(L, held, "2026-10-16")[10]
    assert k == 7 and pts == pytest.approx(6.0)


def test_unrelated_event_after_the_game_is_no_duplicate(cd, pl, tmp_repo):  # noqa: F811
    """Control: a later report outside the game (Jan 2027) beside the right one is not a duplicate and covers nothing."""
    def f(L):
        add_abbvie(L)
        d = copy.deepcopy(ko_event(L))
        d.update(id=d["id"] + ":jan", date="2027-01-15")
        L.append(d)
    edit(tmp_repo, "ledger", f)
    resync(cd, tmp_repo)
    fails, _ = run(cd, pl, tmp_repo)
    assert not [x for x in fails if x.startswith("FAIL results")]


@pytest.mark.parametrize("reason,ok", [("Date unconfirmed: the company says 27 Oct, Nasdaq's calendar 28 Oct (checked 19 Oct)", True),
                                       ("unclear", False)])
def test_uncertain_date_must_say_why(cd, pl, tmp_repo, reason, ok):  # noqa: F811
    """A genuinely unsettled date is shown as uncertain (WARN) only when marked so with a reason; otherwise it is a
    wrong date (FAIL)."""
    edit(tmp_repo, "ledger", both(add_abbvie, lambda L: ko_event(L).update(date="2026-10-28", confirmed="uncertain", text=reason)))
    resync(cd, tmp_repo)
    fails, rep = run(cd, pl, tmp_repo)
    wrong = [x for x in fails if "not on the date" in x]
    if ok:
        assert not wrong and any(l.startswith("WARN results: results date marked uncertain") for l in rep.lines)
    else:
        assert wrong


# ------------------------------------------------------------------ finding 6: deadlines

@pytest.mark.parametrize("ev,market,bad", [
    ({"date": "2026-11-27", "time_uk": "07:00", "last_order": "Before 07:00 Thu 26 Nov"}, "UK", None),     # London trades 26 Nov
    ({"date": "2026-11-27", "time_uk": "07:00", "last_order": "Before 07:00 Thu 26 Nov"}, "US", "later than"),
    ({"date": "2026-11-27", "time_uk": "before US open", "last_order": "Before 07:00 Wed 25 Nov"}, "US", None),
    ({"date": "2026-10-28", "time_uk": "after US close", "last_order": "Before 07:00 Wed 28 Oct"}, "US", None),
    ({"date": "2026-10-28", "time_uk": "after US close", "last_order": "By 06:30 Wed 28 Oct"}, "US", None),
    ({"date": "2026-10-28", "time_uk": "after US close", "last_order": "No later than 07:00 UK Wed 28 Oct"}, "US", None),
    ({"date": "2026-10-28", "time_uk": "after US close", "last_order": "Any time Wed 28 Oct"}, "US", "no time"),
    ({"date": "2026-10-28", "time_uk": "after US close", "last_order": "After 07:00 Wed 28 Oct"}, "US", "deadline"),
    ({"date": "2026-10-28", "time_uk": "after US close", "last_order": "07:00 Wed 28 Oct"}, "US", "deadline"),
    ({"date": "2026-10-28", "time_uk": "after US close", "last_order": "Before 07:00 Thu 28 Oct"}, "US", "weekday"),
    ({"date": "2026-10-29", "time_uk": "07:00", "last_order": "Before 08:00 Wed 28 Oct"}, "UK", "after the 07:00"),
])
def test_last_order_wording_and_calendar(cd, pl, ev, market, bad):  # noqa: F811
    got = cd.last_order_problem(ev, pl, market)
    assert (got is None) if bad is None else (got and bad in got), got


# ------------------------------------------------------------------ finding 7: integrity coverage

def test_one_file_manifest_fails(cd, pl, tmp_repo):  # noqa: F811
    """Negative: 7.5 printed 'PASS sync: 1 files match'."""
    p = tmp_repo / "state" / "last-sync.md"
    p.write_text("Run: test 2026-10-19T18:58:17Z\n" + cd.sha256(tmp_repo / "data" / "stocks.json") + "  data/stocks.json\n",
                 encoding="utf-8")
    fails, _ = run(cd, pl, tmp_repo)
    assert any(f.startswith("FAIL sync") and "does not record" in f and "data/ledger.json" in f for f in fails)


def test_frozen_manifest_without_the_state_doc_fails(cd, pl, tmp_repo):  # noqa: F811
    """The frozen snapshot's own last-sync.md (unchanged) left out the state doc: under 7.6 that alone is a FAIL."""
    from conftest import SNAPSHOT
    (tmp_repo / "state" / "last-sync.md").write_text((SNAPSHOT / "last-sync.md").read_text(encoding="utf-8"), encoding="utf-8")
    fails, _ = run(cd, pl, tmp_repo)
    assert any(f.startswith("FAIL sync") and "state/ft-game-state.md" in f for f in fails)


@pytest.mark.parametrize("which", ["all", "one day", "one holding"])
def test_missing_contribution_rows_fail(cd, pl, tmp_repo, which):  # noqa: F811
    """Negative: 7.5 printed 'contributions add up' with every contribution row deleted, or a whole day's."""
    def f(L):
        if which == "all":
            return [r for r in L if r["table"] != "contrib"]
        if which == "one day":
            return [r for r in L if not (r["table"] == "contrib" and r["date"] == "2026-10-14")]
        x = next(r for r in L if r["table"] == "contrib" and r["date"] == "2026-10-14" and r["name"] == "Shell")
        return [r for r in L if r is not x]
    edit(tmp_repo, "ledger", f)
    resync(cd, tmp_repo)
    fails, _ = run(cd, pl, tmp_repo)
    assert any(f.startswith("FAIL performance") and "no contribution row" in f for f in fails)


def move_ko(L, **kw):
    add_abbvie(L)
    ko_event(L).update({"date": "2026-10-21", "time_uk": "before US open", "last_order": "Before 07:00 Tue 20 Oct",
                        "implied_pct": None, "plan": ""}, **kw)


@pytest.mark.parametrize("text,level", [
    ("Implied move unavailable", "FAIL"),
    ("Implied move unavailable: not found", "FAIL"),
    ("Implied move unavailable: earnings-watcher had no page", "FAIL"),             # no date
    ("Implied move unavailable: earnings-watcher page shows no figure for KO, checked 19 Oct", "WARN"),
    ("Implied move not available (earnings-watcher page failed, 19 Oct): counted at 6%.", "WARN"),   # 19 Oct mirror's wording
    ("Implied move not available", "FAIL"),
])
def test_unavailable_implied_move_needs_source_and_date(cd, pl, tmp_repo, text, level):  # noqa: F811
    def f(s):
        for r in s:
            if r["name"] == "Coca-Cola":
                r["next_results"] = "21 Oct, before US open"
    edit(tmp_repo, "stocks", f)
    edit(tmp_repo, "ledger", lambda L: move_ko(L, text=text))
    resync(cd, tmp_repo)
    fails, rep = run(cd, pl, tmp_repo)
    thin = [x for x in fails if "without a usable reason" in x]
    if level == "FAIL":
        assert thin
    else:
        assert not thin and not [x for x in fails if x.startswith("FAIL results")]
        assert any(l.startswith("WARN results: implied move recorded as unavailable") for l in rep.lines)


@pytest.mark.parametrize("text,warned", [("Implied 4.1% (earnings-watcher, 19 Oct)", False), ("", True)])
def test_implied_move_names_its_source(cd, pl, tmp_repo, text, warned):  # noqa: F811
    def f(L):
        add_abbvie(L)
        ko_event(L).update(implied_pct=4.1, text=text)
    edit(tmp_repo, "ledger", f)
    resync(cd, tmp_repo)
    _, rep = run(cd, pl, tmp_repo)
    hit = any(l.startswith("WARN results: implied move stored without naming its source") and "Coca-Cola" in l for l in rep.lines)
    assert hit == warned
