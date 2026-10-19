"""Version 7.4 (19 Oct 2026): the expected benefit recorded with each change of order, and its settlement against the
STANDSTILL change row."""
import copy

import pytest

from test_run import build_today, run


def trade(pl, eff, entered="2026-10-18"):
    return pl.lrow("trade", date=entered, effective=eff, name="Test", ticker="TEST", from_w=0.0, to_w=10.0)


def test_recorded_before_the_fill(pl):
    L = pl.record_expectation([trade(pl, "2026-10-19")], {"pts": 0.25, "thesis": "t", "invalidation": "i"},
                              "2026-10-19", "2026-10-18", True, False)
    x = [r for r in L if r["table"] == "expect"]
    assert len(x) == 1 and x[0]["forecast"] == 0.25 and x[0]["text"] == "t" and x[0]["plan"] == "i" and x[0]["days"] == 5
    L = pl.record_expectation(L, {"pts": 0.1}, "2026-10-19", "2026-10-19", False, False, "06:40")   # restated before the fill
    x = [r for r in L if r["table"] == "expect"]
    assert len(x) == 1 and x[0]["forecast"] == 0.1 and x[0]["date"] == "2026-10-19"
    assert not pl.WARN


def test_locked_once_filled(pl):
    L = pl.record_expectation([trade(pl, "2026-10-19")], {"pts": 0.25}, "2026-10-19", "2026-10-18", True, False)
    L = pl.record_expectation(L, {"pts": 0.9}, "2026-10-19", "2026-10-20", False, True)
    assert [r["forecast"] for r in L if r["table"] == "expect"] == [0.25]
    assert any("locked" in w for w in pl.WARN)


def test_hindsight_refused(pl):
    L = pl.record_expectation([trade(pl, "2026-10-19")], {"pts": 0.25}, "2026-10-19", "2026-10-20", False, True)
    assert not [r for r in L if r["table"] == "expect"] and any("hindsight" in w for w in pl.WARN)


def test_missing_expectation_warns(pl):
    L = pl.record_expectation([trade(pl, "2026-10-19")], None, "2026-10-19", "2026-10-18", True, False)
    assert not [r for r in L if r["table"] == "expect"] and any("no expected benefit" in w for w in pl.WARN)


def test_no_change_records_nothing(pl):
    L = pl.record_expectation([], {"pts": 0.25}, "2026-10-19", "2026-10-18", False, False)
    assert L == [] and any("does not change anything" in w for w in pl.WARN)


def test_standstill_carries_the_expectation(pl, data):
    """On the stored files: give the 12 and 13 Oct changes expectations and check forecast, surprise and the summary."""
    L = copy.deepcopy(data["ledger"])
    L.append(pl.lrow("expect", date="2026-10-11", effective="2026-10-12", name="Change for 2026-10-12", forecast=0.5))
    L.append(pl.lrow("expect", date="2026-10-12", effective="2026-10-13", name="Change for 2026-10-13", forecast=0.2))
    L.append(pl.lrow("expect", date="2026-10-18", effective="2026-10-19", name="Change for 2026-10-19", forecast=0.3))
    rows = {r["effective"]: r for r in pl.standstill_rows(L, data["hist"], "SPY", "2026-10-16") if r["kind"] == "change"}
    r12, r13 = rows["2026-10-12"], rows["2026-10-13"]
    assert r12["forecast"] == 0.5 and r12["confirmed"] == "complete"
    assert r12["surprise"] == pytest.approx(r12["value"] - 0.5, abs=1e-3)
    assert r13["forecast"] == 0.2 and r13["surprise"] is None              # four sessions: not complete yet
    assert rows["2026-10-14"]["forecast"] is None
    lines = pl.expectation_lines(L + list(rows.values()))
    assert lines[0].startswith("EXPECTED BENEFIT: 3 change(s) with an expectation, 1 settled")
    right = (r12["value"] > 0) == True                                      # expected +0.5
    assert f"the right direction in {int(right)} of 1" in lines[0]
    assert any("waiting to fill: Change for 2026-10-19" in l for l in lines)


def test_no_expectations_no_change_in_output(pl, data):
    """Without expect rows, standstill rows are exactly as 7.3 made them (forecast and surprise stay empty)."""
    rows = pl.standstill_rows(copy.deepcopy(data["ledger"]), data["hist"], "SPY", "2026-10-16")
    assert all(r["forecast"] is None and r["surprise"] is None for r in rows)
    assert pl.expectation_lines(data["ledger"]) == []


def changed_order(today):
    for o in today["order"]:
        if o["name"] == "Coca-Cola":
            o["weight"] = 15
        if o["name"] == "Exxon Mobil":
            o["weight"] = 20
    today.update({"effective": "2026-10-19", "entered": "2026-10-18", "order_reason": "test change"})


def test_run_records_and_reports(pl, repo, tmp_path, stored):
    today, _ = build_today(pl, repo, tmp_path, stored)
    changed_order(today)
    today["order_expected"] = {"pts": 0.15, "thesis": "oil", "invalidation": "Brent below 100"}
    led, out, _ = run(pl, repo, tmp_path, today)
    x = [r for r in led if r["table"] == "expect"]
    assert len(x) == 1 and x[0]["effective"] == "2026-10-19" and x[0]["forecast"] == 0.15 and x[0]["id"]
    assert "EXPECTED BENEFIT: 1 change(s) with an expectation, 0 settled" in out
    assert "waiting to fill: Change for 2026-10-19" in out


def test_run_without_expectation_warns(pl, repo, tmp_path, stored):
    today, _ = build_today(pl, repo, tmp_path, stored)
    changed_order(today)
    led, out, _ = run(pl, repo, tmp_path, today)
    assert not [r for r in led if r["table"] == "expect"]
    assert "WARNING: the order changes at the open of 2026-10-19 but no expected benefit was given" in out


def test_template_has_the_field(pl, repo, tmp_path, stored):
    today, _ = build_today(pl, repo, tmp_path, stored)
    assert today["order_expected"] == {"pts": None, "thesis": "", "invalidation": ""}
