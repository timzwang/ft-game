import argparse
import copy
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_checks(repo, dependencies=None):
    if dependencies:
        sys.path.insert(0, str(dependencies))
    pipeline = load_module(repo / "scripts/ft_pipeline.py", "review_pipeline")
    scan = load_module(repo / "scan/scan.py", "review_scan")
    ledger = json.loads((repo / "data/ledger.json").read_text(encoding="utf-8"))
    history = {(row["ticker"], row["date"]): row for row in json.loads((repo / "data/history.json").read_text(encoding="utf-8"))}
    findings = {}

    def reset():
        pipeline._SERIES.clear()
        pipeline.WARN.clear()
        pipeline.INCOMPLETE.clear()

    def performance(rows):
        return [(row["date"], row["value_est"], row["day_pct"]) for row in rows if row["table"] == "perf"]

    def rebuild(prices):
        reset()
        rows = [copy.deepcopy(row) for row in ledger if row["table"] not in ("perf", "contrib")]
        pipeline.update_performance(rows, prices, "SPY", "2026-10-16")
        return rows

    rebuilt = rebuild(history)
    findings["complete_performance_rebuild"] = {"matches_stored": performance(rebuilt) == performance(ledger), "last": performance(rebuilt)[-1]}
    assert findings["complete_performance_rebuild"]["matches_stored"]

    missing = dict(history)
    del missing[("XOM", "2026-10-14")]
    partial = rebuild(missing)
    last_before_repair = performance(partial)[-1][0]
    reset()
    pipeline.update_performance(partial, history, "SPY", "2026-10-16")
    maximum_value_difference = max(abs(actual[1] - expected[1]) for actual, expected in zip(performance(partial), performance(ledger)))
    findings["missing_holding_and_backfill"] = {"stops_at": last_before_repair, "repair_matches_stored": performance(partial) == performance(ledger), "maximum_value_difference_credits": round(maximum_value_difference, 4), "last": performance(partial)[-1]}
    assert last_before_repair == "2026-10-13"
    assert maximum_value_difference <= 0.011
    assert performance(partial)[-1] == performance(ledger)[-1]

    reset()
    rows = {}
    pipeline.merge_history(rows, "TEST", [{"date": "2026-10-19", "high": 110, "low": 99, "close": 105, "volume": 1000000}])
    placeholder = copy.deepcopy(rows[("TEST", "2026-10-19")])
    findings["missing_open_is_rejected"] = {"open_obs": placeholder.get("open_obs"), "real_open": pipeline.real_open(placeholder)}
    assert findings["missing_open_is_rejected"]["real_open"] is False
    pipeline.merge_history(rows, "TEST", [placeholder])
    findings["provenance_round_trip"] = {"expected_real_open": False, "actual_real_open": pipeline.real_open(rows[("TEST", "2026-10-19")]), "row_after_round_trip": rows[("TEST", "2026-10-19")]}

    reset()
    benchmark_rows = pipeline.series(history, "SPY")
    reaction = benchmark_rows[-20]["date"]
    next_date = benchmark_rows[-19]["date"]
    drift_history = dict(history)
    drift_history[("XOM", next_date)] = dict(history[("XOM", next_date)], open_obs=False)
    drift_rows = [pipeline.lrow("drift", date=reaction, name="Exxon Mobil", ticker="XOM", kind="enter")]
    pipeline.resolve_drift(drift_rows, drift_history, "SPY")
    findings["drift_missing_next_open"] = {key: drift_rows[0][key] for key in ("beat", "ret_pct", "cum_pct", "unit")}
    assert drift_rows[0]["beat"] == "n/a"
    assert drift_rows[0]["ret_pct"] is None

    reset()
    standstill = pipeline.standstill_rows(copy.deepcopy(ledger), history, "SPY", "2026-10-16")
    findings["standstill"] = {row["name"]: row["value"] for row in standstill if row["kind"] in ("inception", "week") or row["date"] == "2026-10-12"}
    stored_standstill = {row["name"]: row["value"] for row in ledger if row["table"] == "standstill"}
    assert all(abs(row["value"] - stored_standstill[row["name"]]) < 0.002 for row in standstill if row["value"] is not None)

    dates = ["2026-10-19", "2026-10-20", "2026-10-21", "2026-10-22", "2026-10-23", "2026-10-26", "2026-10-27"]
    def price(ticker, date, value, observed=True):
        row = {"ticker": ticker, "date": date, "open": value, "high": value + 1, "low": value - 1, "close": value, "volume": 100}
        if not observed:
            row["open_obs"] = False
        return row

    synthetic = {("SPY", date): price("SPY", date, 100) for date in dates}
    synthetic.update({("TEST", date): price("TEST", date, 100 + index) for index, date in enumerate(dates)})
    confidence_rows = [pipeline.lrow("confidence", effective=dates[0], name="Test", ticker="TEST", confidence=55)]
    gap_history = {key: value for key, value in synthetic.items() if key != ("TEST", dates[0])}
    reset()
    pipeline.resolve_confidence(confidence_rows, gap_history, "SPY")
    findings["confidence_missing_entry_session"] = {"expected": "wait or n/a", "actual_beat": confidence_rows[0]["beat"], "actual_return": confidence_rows[0]["ret_pct"], "labelled_window_end": confidence_rows[0]["window_end"], "actual_stock_start": dates[1], "actual_stock_end": dates[5]}

    imputed_history = copy.deepcopy(synthetic)
    imputed_history[("TEST", dates[0])]["open_obs"] = False
    confidence_rows = [pipeline.lrow("confidence", effective=dates[0], name="Test", ticker="TEST", confidence=55)]
    reset()
    pipeline.resolve_confidence(confidence_rows, imputed_history, "SPY")
    findings["confidence_imputed_entry_open"] = {"expected": "wait or n/a", "actual_beat": confidence_rows[0]["beat"], "actual_return": confidence_rows[0]["ret_pct"]}

    shadow_history = {key: value for key, value in synthetic.items() if key != ("TEST", dates[5])}
    shadow_rows = [pipeline.lrow("shadow", date=dates[0], name="Test", ticker="TEST")]
    reset()
    pipeline.resolve_shadow(shadow_rows, shadow_history, "SPY")
    findings["shadow_missing_end_session"] = {"expected": "wait or n/a", "actual_beat": shadow_rows[0]["beat"], "actual_return": shadow_rows[0]["ret_pct"], "labelled_window_end": shadow_rows[0]["window_end"], "actual_stock_end": dates[4]}

    holiday_ledger = [
        pipeline.lrow("meta", name="start_date", text=dates[0]),
        pipeline.lrow("meta", name="start_value", value=100000),
        pipeline.lrow("meta", name="spy_base", value=100),
        pipeline.lrow("position", effective=dates[0], name="Test", ticker="TEST", weight=100)
    ]
    holiday_history = {key: value for key, value in synthetic.items() if key != ("TEST", dates[1])}
    reset()
    pipeline.update_performance(holiday_ledger, holiday_history, "SPY", dates[2], {("TEST", dates[1])})
    findings["market_closed_unchanged_holding"] = {"sessions": len(performance(holiday_ledger)), "closed_day_return": performance(holiday_ledger)[1][2], "incomplete": list(pipeline.INCOMPLETE)}
    assert len(performance(holiday_ledger)) == 3
    assert performance(holiday_ledger)[1][2] == 0
    holiday_ledger.append(pipeline.lrow("position", effective=dates[1], name="Test", ticker="TEST", weight=90))
    holiday_ledger = [row for row in holiday_ledger if row["table"] not in ("perf", "contrib")]
    reset()
    pipeline.update_performance(holiday_ledger, holiday_history, "SPY", dates[2], {("TEST", dates[1])})
    findings["market_closed_does_not_allow_trade"] = {"sessions": len(performance(holiday_ledger)), "incomplete": list(pipeline.INCOMPLETE)}
    assert len(performance(holiday_ledger)) == 1

    reset()
    weights = {row["name"]: row["weight"] for row in json.loads((repo / "data/stocks.json").read_text(encoding="utf-8")) if row["group"] == "Portfolio"}
    totals = pipeline.results_total(ledger, weights, "2026-10-16")
    with_abbvie = ledger + [pipeline.lrow("event", date="2026-10-30", name="AbbVie results", stock="AbbVie", kind="results")]
    findings["missing_abbvie_event"] = {"abbvie_weight": weights["AbbVie"], "stored_total_10": totals[10], "with_state_doc_date_10": pipeline.results_total(with_abbvie, weights, "2026-10-16")[10]}
    assert round(totals[10][0], 2) == 5.4
    assert round(pipeline.results_total(with_abbvie, weights, "2026-10-16")[10][0], 2) == 6.0

    reported_rows = [row for row in ledger if row["table"] == "reported"]
    findings["top2_record"] = {key: reported_rows[-1][key] for key in ("date", "value_reported", "value")}
    findings["counts"] = dict(Counter(row["table"] for row in ledger))
    findings["us_close_27_nov"] = {"expected_uk_time": "18:00", "actual": pipeline.us_close_uk("2026-11-27")}

    import pandas as pd
    def frame(indices):
        return pd.DataFrame({"Open": [100 + index for index in range(len(indices))], "High": [102 + index for index in range(len(indices))], "Low": [99 + index for index in range(len(indices))], "Close": [101 + index for index in range(len(indices))], "Volume": [1000] * len(indices)}, index=pd.to_datetime(indices))

    record = pd.DataFrame([{"session": dates[0], "list": "events", "rank": 1, "ticker": "TEST", "market": "US", "new": True, "bench": "SPY", "settled_on": ""}])
    prices = {"SPY": frame(dates), "TEST": frame([date for date in dates if date != dates[1]])}
    settled = scan.settle(record, prices)
    findings["scan_missing_session"] = {"expected_window_end": dates[5], "actual_window_end": settled.iloc[0]["settled_on"], "expected_entry": dates[1], "actual_entry": dates[2]}
    assert settled.iloc[0]["settled_on"] == dates[6]
    import contextlib
    import io
    import tempfile
    with tempfile.TemporaryDirectory(prefix="ft-game-review-") as temporary:
        temporary_root = Path(temporary)
        fixtures = temporary_root / "fixtures"
        fixtures.mkdir()
        output = temporary_root / "scan-output"
        pd.DataFrame([
            {"ticker": "ALPHA", "name": "Alpha", "market": "US", "index": "test", "sector": "Test"},
            {"ticker": "BETA.L", "name": "Beta", "market": "UK", "index": "test", "sector": "Test"}
        ]).to_csv(fixtures / "universe.csv", index=False)
        sessions = pd.bdate_range(end="2026-10-16", periods=300)
        for ticker in ("ALPHA", "BETA.L", "SPY", "^FTSE"):
            stock = ticker not in ("SPY", "^FTSE")
            closes = [100 + index * (0.3 if stock else 0.05) for index in range(300)]
            bars = pd.DataFrame({"Open": closes, "High": [value * 1.01 for value in closes], "Low": [value * 0.99 for value in closes], "Close": closes, "Volume": [10000000] * 300}, index=sessions)
            bars.index.name = "Date"
            if stock:
                previous = closes[-2]
                bars.loc[sessions[-1], ["Open", "High", "Low", "Close", "Volume"]] = [previous * 1.04, previous * 1.06, previous * 1.03, previous * 1.05, 20000000]
            bars.to_csv(fixtures / (ticker.replace("^", "_") + ".csv"))
        previous_arguments = sys.argv
        try:
            sys.argv = ["scan.py", "--offline", str(fixtures), "--out", str(output)]
            with contextlib.redirect_stdout(io.StringIO()):
                first_exit = scan.main()
                first_record = pd.read_csv(output / "record.csv")
                second_exit = scan.main()
                second_record = pd.read_csv(output / "record.csv")
        finally:
            sys.argv = previous_arguments
        findings["scan_offline_smoke"] = {"first_exit": first_exit, "second_exit": second_exit, "first_record_rows": len(first_record), "second_record_rows": len(second_record), "metadata": json.loads((output / "latest.json").read_text(encoding="utf-8"))}
        assert first_exit == second_exit == 0
        assert len(first_record) == len(second_record) == 4

        template_file = temporary_root / "today.json"
        with contextlib.redirect_stdout(io.StringIO()):
            pipeline.cmd_template({"stocks": str(repo / "data/stocks.json"), "ledger": str(repo / "data/ledger.json"), "history": str(repo / "data/history.json"), "panel": str(repo / "data/panel.json"), "out": str(template_file)})
        today = json.loads(template_file.read_text(encoding="utf-8"))
        today.update({"date": "2026-10-16", "next_session": "2026-10-19", "effective": "2026-10-19", "entered": "2026-10-18", "prices_as_of": "Fri 16 Oct close", "order_for": "Mon 19 Oct open"})
        current_report = reported_rows[-1]
        today["reported"] = {"date": current_report["date"], "time_uk": current_report["time_uk"], "value": current_report["value_reported"], "rank": current_report["rank"], "players": current_report["players"], "top2_return_pct": 6.5}
        stored_stocks = json.loads((repo / "data/stocks.json").read_text(encoding="utf-8"))
        for stock in today["stocks"]:
            stored = next(row for row in stored_stocks if row["ticker"] == stock["ticker"])
            bar = history.get((stock["ticker"], "2026-10-16"))
            if bar:
                stock["quote"].update({key: bar[key] for key in ("open", "high", "low", "volume")})
                stock["quote"]["price"] = bar["close"]
                before = sorted((row for (ticker, date), row in history.items() if ticker == stock["ticker"] and date < "2026-10-16"), key=lambda row: row["date"])
                stock["quote"]["prev_close"] = before[-1]["close"] if before else None
            for key in ("week52_high", "week52_low", "target"):
                stock["quote"][key] = stored.get(key)
        template_file.write_text(json.dumps(today), encoding="utf-8")
        reset()
        pipeline_output = temporary_root / "pipeline-output"
        with contextlib.redirect_stdout(io.StringIO()):
            pipeline.cmd_run({"today": str(template_file), "ledger": str(repo / "data/ledger.json"), "history": str(repo / "data/history.json"), "macro": str(repo / "data/macro.json"), "panel": str(repo / "data/panel.json"), "out": str(pipeline_output)})
        output_ledger = json.loads((pipeline_output / "ledger.json").read_text(encoding="utf-8"))
        findings["pipeline_template_run_smoke"] = {"files_written": sorted(path.name for path in pipeline_output.iterdir()), "performance_unchanged": performance(output_ledger) == performance(ledger), "incomplete": list(pipeline.INCOMPLETE)}
        assert findings["pipeline_template_run_smoke"]["performance_unchanged"]
        updated_report = next(row for row in output_ledger if row["table"] == "reported" and row["date"] == current_report["date"] and row["rank"] == current_report["rank"])
        findings["top2_existing_report_update"] = {"expected": 6.5, "actual": updated_report["value"]}
    return findings


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--dependencies", type=Path)
    arguments = parser.parse_args()
    print(json.dumps(run_checks(arguments.repo, arguments.dependencies), indent=2))
