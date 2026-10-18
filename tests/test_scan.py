"""Regression tests for scan/scan.py (19 Oct 2026). Offline only: synthetic prices, a temporary output folder."""
import contextlib
import datetime as dt
import io
import json
import sys

import pytest

pd = pytest.importorskip("pandas")


def frame(dates):
    n = len(dates)
    return pd.DataFrame({"Open": [100.0 + i for i in range(n)], "High": [102.0 + i for i in range(n)],
                         "Low": [99.0 + i for i in range(n)], "Close": [101.0 + i for i in range(n)],
                         "Volume": [1000] * n}, index=pd.to_datetime(dates))


def bdays(start, n):
    return [d.strftime("%Y-%m-%d") for d in pd.bdate_range(start=start, periods=n)]


def record_for(session):
    return pd.DataFrame([{"session": session, "list": "events", "rank": 1, "ticker": "TEST", "market": "US", "new": True,
                          "bench": "SPY", "settled_on": ""}])


def test_settle_complete_uses_benchmark_dates(scan_mod):
    dates = bdays("2026-10-19", 8)
    rec = scan_mod.settle(record_for(dates[0]), {"SPY": frame(dates), "TEST": frame(dates)})
    assert rec.iloc[0]["settled_on"] == dates[5]
    assert rec.iloc[0]["ret_5"] == pytest.approx(106.0 / 101.0 - 1)
    assert rec.iloc[0]["ret_5_open"] == pytest.approx(106.0 / 101.0 - 1)   # open of the next session is 101


def test_settle_missing_stock_session_waits_then_closes_empty(scan_mod):
    dates = bdays("2026-10-19", 8)
    gap = [d for d in dates if d != dates[1]]
    rec = scan_mod.settle(record_for(dates[0]), {"SPY": frame(dates), "TEST": frame(gap)})
    assert rec.iloc[0]["settled_on"] == ""                         # 7.2 moved the window to 21 to 27 Oct here
    long_ = bdays("2026-10-19", 22)
    rec = scan_mod.settle(record_for(long_[0]), {"SPY": frame(long_), "TEST": frame([d for d in long_ if d != long_[1]])})
    assert rec.iloc[0]["settled_on"] == long_[5]
    assert pd.isna(rec.iloc[0].get("excess_5"))


def test_summary_skips_rows_closed_without_figures(scan_mod):
    rec = pd.DataFrame([
        {"session": "2026-10-19", "list": "leaders", "rank": 1, "ticker": "A", "market": "US", "new": True, "bench": "SPY",
         "settled_on": "2026-10-26", "excess_5": 0.02, "excess_5_open": 0.01},
        {"session": "2026-10-19", "list": "leaders", "rank": 2, "ticker": "B", "market": "US", "new": True, "bench": "SPY",
         "settled_on": "2026-10-26", "excess_5": float("nan"), "excess_5_open": float("nan")},
    ])
    line = next(l for l in scan_mod.record_summary(rec) if l.startswith("| leaders | all rows"))
    assert "| 1 | 100% |" in line


@pytest.mark.parametrize("now,expect_waiting", [
    (dt.datetime(2026, 11, 27, 13, 10), True),       # before 13:15 New York on the half-day
    (dt.datetime(2026, 11, 27, 13, 20), False),      # after it: the 27 Nov bar is final
    (dt.datetime(2026, 11, 25, 16, 10), True),
    (dt.datetime(2026, 11, 25, 16, 20), False),
])
def test_us_session_final_knows_the_half_day(scan_mod, monkeypatch, now, expect_waiting):
    class Fake(dt.datetime):
        @classmethod
        def now(cls, tz=None):
            return now.replace(tzinfo=tz)
    monkeypatch.setattr(scan_mod, "datetime", Fake)
    day = now.strftime("%Y-%m-%d")
    spy = frame([(now - dt.timedelta(days=1)).strftime("%Y-%m-%d"), day])
    _session, waiting = scan_mod.us_session_final(spy)
    assert waiting is expect_waiting


def test_offline_scan_runs_and_repeats_cleanly(scan_mod, tmp_path):
    fixtures, out = tmp_path / "fixtures", tmp_path / "out"
    fixtures.mkdir()
    pd.DataFrame([{"ticker": "ALPHA", "name": "Alpha", "market": "US", "index": "test", "sector": "Test"},
                  {"ticker": "BETA.L", "name": "Beta", "market": "UK", "index": "test", "sector": "Test"}]).to_csv(fixtures / "universe.csv", index=False)
    sessions = pd.bdate_range(end="2026-10-16", periods=300)
    for t in ("ALPHA", "BETA.L", "SPY", "^FTSE"):
        stock = t not in ("SPY", "^FTSE")
        closes = [100 + i * (0.3 if stock else 0.05) for i in range(300)]
        bars = pd.DataFrame({"Open": closes, "High": [c * 1.01 for c in closes], "Low": [c * 0.99 for c in closes],
                             "Close": closes, "Volume": [10_000_000] * 300}, index=sessions)
        bars.index.name = "Date"
        if stock:
            p = closes[-2]
            bars.loc[sessions[-1], ["Open", "High", "Low", "Close", "Volume"]] = [p * 1.04, p * 1.06, p * 1.03, p * 1.05, 20_000_000]
        bars.to_csv(fixtures / (t.replace("^", "_") + ".csv"))
    argv = sys.argv
    try:
        sys.argv = ["scan.py", "--offline", str(fixtures), "--out", str(out)]
        with contextlib.redirect_stdout(io.StringIO()):
            assert scan_mod.main() == 0
            first = pd.read_csv(out / "record.csv")
            assert scan_mod.main() == 0
            second = pd.read_csv(out / "record.csv")
    finally:
        sys.argv = argv
    assert len(first) == len(second) == 4
    assert json.loads((out / "latest.json").read_text(encoding="utf-8"))
