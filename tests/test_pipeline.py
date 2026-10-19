"""Regression tests for scripts/ft_pipeline.py. Every test asserts; a false result fails the run.

Covers the stored game data (figures must not move) and each fix in version 7.3, plus the 7.2 protections it keeps.
"""
import copy
import datetime as dt
import json

import pytest

from conftest import DATES, bar, perf_rows


def weekdays(start, n):
    d, out = dt.date.fromisoformat(start), []
    while len(out) < n:
        if d.weekday() < 5:
            out.append(d.isoformat())
        d += dt.timedelta(days=1)
    return out


def synthetic(dates, ticker="TEST", step=1.0):
    h = {("SPY", d): bar("SPY", d, 100.0) for d in dates}
    h.update({(ticker, d): bar(ticker, d, 100.0 + i * step) for i, d in enumerate(dates)})
    return h


# ----------------------------------------------------------------- stored figures stay put

def test_version(pl):
    assert pl.PIPELINE_VERSION == "7.4"


def test_performance_rebuild_matches_stored(pl, data):
    rows = [r for r in data["ledger"] if r["table"] not in ("perf", "contrib")]
    pl.update_performance(rows, data["hist"], "SPY", "2026-10-16")
    assert perf_rows(rows) == perf_rows(data["ledger"])
    assert perf_rows(rows)[-1][1] == pytest.approx(101435.76, abs=0.005)


def test_missing_holding_row_stops_then_repairs(pl, data):
    hist = dict(data["hist"])
    del hist[("XOM", "2026-10-14")]
    rows = [r for r in data["ledger"] if r["table"] not in ("perf", "contrib")]
    pl.update_performance(rows, hist, "SPY", "2026-10-16")
    assert perf_rows(rows)[-1][0] == "2026-10-13"
    assert pl.INCOMPLETE
    pl.INCOMPLETE.clear()
    pl.update_performance(rows, data["hist"], "SPY", "2026-10-16")
    got, want = perf_rows(rows), perf_rows(data["ledger"])
    assert [g[0] for g in got] == [w[0] for w in want]
    assert got[-1] == want[-1]
    assert max(abs(g[1] - w[1]) for g, w in zip(got, want)) <= 0.011    # rounding of an intermediate day only


def test_stored_confidence_ratings_reproduce(pl, data):
    """Every rating settled under 7.2 settles the same way under 7.3's stricter rule."""
    done = [r for r in data["ledger"] if r["table"] == "confidence" and r["beat"] in ("yes", "no")]
    assert len(done) >= 11
    fresh = copy.deepcopy(done)
    for r in fresh:
        r["beat"] = r["window_end"] = r["ret_pct"] = r["spx_ret_pct"] = None
    pl.resolve_confidence(fresh, data["hist"], "SPY")
    for a, b in zip(done, fresh):
        assert (a["name"], a["beat"], a["ret_pct"], a["spx_ret_pct"], a["window_end"]) == \
               (b["name"], b["beat"], b["ret_pct"], b["spx_ret_pct"], b["window_end"])


def test_stored_shadow_ratings_reproduce(pl, data):
    """Settled shadow ratings whose prices are still stored settle the same way again. Stocks dropped from the list
    lose their rows (so they cannot be recomputed), and Shell's 9 Oct rating settled before its 9 and 12 Oct rows were
    corrected on 18 Oct (3.75 stored, 3.81 now, same verdict)."""
    done = [r for r in data["ledger"] if r["table"] == "shadow" and r["beat"] in ("yes", "no")]
    tickers = {t for (t, _) in data["hist"]}
    done = [r for r in done if r["ticker"] in tickers]
    assert len(done) >= 30
    fresh = copy.deepcopy(done)
    for r in fresh:
        r["beat"] = r["window_end"] = r["ret_pct"] = r["spx_ret_pct"] = None
    pl.resolve_shadow(fresh, data["hist"], "SPY")
    for a, b in zip(done, fresh):
        assert (a["beat"], a["spx_ret_pct"], a["window_end"]) == (b["beat"], b["spx_ret_pct"], b["window_end"])
        if (a["ticker"], a["date"]) == ("SHEL", "2026-10-09"):
            assert b["ret_pct"] == pytest.approx(a["ret_pct"], abs=0.1)
        else:
            assert a["ret_pct"] == b["ret_pct"]


def test_standstill_reproduces(pl, data):
    rows = pl.standstill_rows(copy.deepcopy(data["ledger"]), data["hist"], "SPY", "2026-10-16")
    stored = {r["name"]: r["value"] for r in data["ledger"] if r["table"] == "standstill"}
    assert rows
    for r in rows:
        if r["value"] is not None:
            assert r["value"] == pytest.approx(stored[r["name"]], abs=0.002)


# ----------------------------------------------------------------- open provenance (7.2, kept and tightened in 7.3)

def test_missing_open_is_marked_and_kept_on_round_trip(pl):
    h = {}
    pl.merge_history(h, "TEST", [{"date": "2026-10-19", "high": 110, "low": 99, "close": 105, "volume": 1000000}])
    row = copy.deepcopy(h[("TEST", "2026-10-19")])
    assert row["open_obs"] is False and pl.real_open(row) is False
    changed = pl.merge_history(h, "TEST", [row])                  # the stored row given back, numeric open and all
    assert h[("TEST", "2026-10-19")].get("open_obs") is False
    assert pl.real_open(h[("TEST", "2026-10-19")]) is False
    assert changed == []                                          # nothing new, so nothing recalculated


def test_provenance_change_alone_counts_as_correction(pl):
    h = {}
    pl.merge_history(h, "TEST", [{"date": "2026-10-19", "high": 110, "low": 99, "close": 105, "volume": 10}])
    changed = pl.merge_history(h, "TEST", [{"date": "2026-10-19", "open": 105, "high": 110, "low": 99, "close": 105, "volume": 10}])
    assert changed == ["2026-10-19"]
    assert pl.real_open(h[("TEST", "2026-10-19")]) is True


# ----------------------------------------------------------------- confidence settlement (7.3)

def conf_row(pl, eff):
    return pl.lrow("confidence", effective=eff, name="Test", ticker="TEST", confidence=55)


def test_confidence_complete_window(pl):
    h = synthetic(DATES)
    rows = [conf_row(pl, DATES[0])]
    pl.resolve_confidence(rows, h, "SPY")
    assert rows[0]["window_end"] == DATES[4]
    assert rows[0]["ret_pct"] == pytest.approx(4.0)               # open 100 on the 19th, close 104 on the 23rd
    assert rows[0]["beat"] == "yes"


def test_confidence_missing_entry_row_waits_then_na(pl):
    dates = weekdays("2026-10-19", 22)
    h = synthetic(dates)
    del h[("TEST", dates[0])]
    short = {k: v for k, v in h.items() if k[1] <= dates[6]}
    rows = [conf_row(pl, dates[0])]
    pl.resolve_confidence(rows, short, "SPY")
    assert rows[0]["beat"] is None and rows[0]["window_end"] == dates[4]
    pl._SERIES.clear()
    pl.resolve_confidence(rows, h, "SPY")
    assert rows[0]["beat"] == "n/a" and "no row" in rows[0]["unit"] and rows[0]["ret_pct"] is None


def test_confidence_estimated_entry_open_is_not_scored(pl):
    dates = weekdays("2026-10-19", 22)
    h = synthetic(dates)
    h[("TEST", dates[0])]["open_obs"] = False
    rows = [conf_row(pl, dates[0])]
    pl.resolve_confidence(rows, {k: v for k, v in h.items() if k[1] <= dates[6]}, "SPY")
    assert rows[0]["beat"] is None
    pl._SERIES.clear()
    pl.resolve_confidence(rows, h, "SPY")
    assert rows[0]["beat"] == "n/a" and "traded open" in rows[0]["unit"]


def test_confidence_missing_end_row_never_borrows_another_day(pl):
    h = synthetic(DATES)
    del h[("TEST", DATES[4])]
    rows = [conf_row(pl, DATES[0])]
    pl.resolve_confidence(rows, h, "SPY")
    assert rows[0]["beat"] is None and rows[0]["ret_pct"] is None


# ----------------------------------------------------------------- shadow settlement (7.3)

def test_shadow_missing_end_waits_then_na(pl):
    dates = weekdays("2026-10-19", 22)
    h = synthetic(dates)
    del h[("TEST", dates[5])]
    rows = [pl.lrow("shadow", date=dates[0], name="Test", ticker="TEST")]
    pl.resolve_shadow(rows, {k: v for k, v in h.items() if k[1] <= dates[7]}, "SPY")
    assert rows[0]["beat"] is None and rows[0]["ret_pct"] is None
    pl._SERIES.clear()
    pl.resolve_shadow(rows, h, "SPY")
    assert rows[0]["beat"] == "n/a" and rows[0]["window_end"] == dates[5]


def test_shadow_complete(pl):
    h = synthetic(DATES)
    rows = [pl.lrow("shadow", date=DATES[0], name="Test", ticker="TEST")]
    pl.resolve_shadow(rows, h, "SPY")
    assert rows[0]["window_end"] == DATES[5] and rows[0]["ret_pct"] == pytest.approx(5.0) and rows[0]["beat"] == "yes"


# ----------------------------------------------------------------- drift and holidays (7.2, kept)

def test_drift_without_next_open_is_na(pl, data):
    bser = pl.series(data["hist"], "SPY")
    reaction, nxt = bser[-20]["date"], bser[-19]["date"]
    h = dict(data["hist"])
    h[("XOM", nxt)] = dict(h[("XOM", nxt)], open_obs=False)
    rows = [pl.lrow("drift", date=reaction, name="Exxon Mobil", ticker="XOM", kind="enter")]
    pl.resolve_drift(rows, h, "SPY")
    assert rows[0]["beat"] == "n/a" and rows[0]["ret_pct"] is None


def holiday_ledger(pl):
    return [pl.lrow("meta", name="start_date", text=DATES[0]), pl.lrow("meta", name="start_value", value=100000),
            pl.lrow("meta", name="spy_base", value=100), pl.lrow("position", effective=DATES[0], name="Test", ticker="TEST", weight=100)]


def test_closed_market_carries_an_unchanged_holding(pl):
    h = {k: v for k, v in synthetic(DATES).items() if k != ("TEST", DATES[1])}
    L = holiday_ledger(pl)
    pl.update_performance(L, h, "SPY", DATES[2], {("TEST", DATES[1])})
    assert len(perf_rows(L)) == 3 and perf_rows(L)[1][2] == 0


def test_closed_market_never_allows_a_trade(pl):
    h = {k: v for k, v in synthetic(DATES).items() if k != ("TEST", DATES[1])}
    L = holiday_ledger(pl) + [pl.lrow("position", effective=DATES[1], name="Test", ticker="TEST", weight=90)]
    pl.update_performance(L, h, "SPY", DATES[2], {("TEST", DATES[1])})
    assert len(perf_rows(L)) == 1


# ----------------------------------------------------------------- calendar (7.3)

@pytest.mark.parametrize("day,uk", [("2026-10-19", "21:00"), ("2026-10-27", "20:00"), ("2026-11-02", "21:00"),
                                    ("2026-11-25", "21:00"), ("2026-11-27", "18:00")])
def test_us_close_in_uk_time(pl, day, uk):
    assert pl.us_close_uk(day) == uk


def test_next_session_skips_thanksgiving(pl):
    assert pl.next_weekday("2026-11-25") == "2026-11-27"
    assert pl.next_weekday("2026-10-23") == "2026-10-26"


def test_sessions_ahead_skip_thanksgiving(pl):
    assert pl._sessions_ahead("2026-11-24", 3) == ["2026-11-25", "2026-11-27", "2026-11-30"]


def test_final_reading_between_1800_and_2100_counts_as_after_close(pl):
    L = [pl.lrow("perf", date="2026-11-27", value_est=100000.0),
         pl.lrow("reported", date="2026-11-27", time_uk="18:30", value_reported=100010.0)]
    out = pl.reconcile(L)
    assert out and out[0][3] is False


# ----------------------------------------------------------------- results budget and totals (7.3)

def test_results_budget_windows(pl):
    assert pl.results_budget_for("2026-10-26") == 0.6
    assert pl.results_budget_for("2026-10-27") == 1.0
    assert pl.results_budget_for("2026-10-30") == 1.0
    assert pl.results_budget_for("2026-11-03") == 0.6
    assert pl.results_budget_for("2026-11-16", 0.8) == 0.8         # part D's stance from 13 Nov
    assert pl.results_budget_for("2026-10-28", 0.8) == 1.0


def test_results_total_counts_abbvie_once_its_event_exists(pl, data):
    weights = {r["name"]: r["weight"] for r in data["stocks"] if r["group"] == "Portfolio"}
    base = pl.results_total(data["ledger"], weights, "2026-10-16")[10]
    have_abbvie = any(r["table"] == "event" and r["kind"] == "results" and r["stock"] == "AbbVie" for r in data["ledger"])
    added = data["ledger"] + ([] if have_abbvie else [pl.lrow("event", date="2026-10-30", name="AbbVie results", stock="AbbVie", kind="results")])
    full = pl.results_total(added, weights, "2026-10-16")[10]
    assert full[1] == 7                                            # all seven holdings report inside ten sessions
    assert round(full[0], 2) == 6.0                                # at the 6% default, as the review computed
    assert have_abbvie or round(base[0], 2) == 5.4


def test_results_dates_parse(pl):
    assert pl.results_date_from_text("30 Oct, before US open") == "2026-10-30"
    assert pl.results_date_from_text("28 Oct (time est.)") == "2026-10-28"
    assert pl.results_date_from_text("19 Nov") == "2026-11-19"
    assert pl.results_date_from_text("mid Jan 2027 (est.)") is None
    assert pl.results_date_from_text("") is None


def test_missing_results_event_is_flagged(pl):
    L = [pl.lrow("event", date="2026-10-27", name="Coca-Cola results", stock="Coca-Cola", kind="results")]
    held = {"Coca-Cola": "27 Oct, before US open", "AbbVie": "30 Oct", "TSMC": "mid Jan 2027 (est.)", "Walmart": "19 Dec"}
    assert pl.missing_results_events(L, held, "2026-10-16") == [("AbbVie", "2026-10-30", "30 Oct")]


def test_stored_holdings_results_events(pl, data):
    """On the stored files: AbbVie is the one holding without an event (until the 19 Oct evening review adds it)."""
    held = {r["name"]: r["next_results"] for r in data["stocks"] if r["group"] == "Portfolio" and (r["weight"] or 0) > 0}
    date = max(r["date"] for r in data["ledger"] if r["table"] == "perf")
    missing = [m[0] for m in pl.missing_results_events(data["ledger"], held, date)]
    assert set(missing) <= {"AbbVie"}, f"holdings with a results date but no event: {missing}"
