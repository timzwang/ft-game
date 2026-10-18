"""Shared fixtures for the regression tests (pipeline 7.3, 19 Oct 2026).

Run from the repository root:  python -m pytest -q tests
The tests read the stored data files and the scripts from this checkout only; they write nothing outside a
temporary folder and fetch nothing from the network.
"""
import copy
import importlib.util
import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="session")
def repo():
    return REPO


@pytest.fixture()
def pl():
    """The pipeline, with its module-level caches emptied for each test."""
    mod = _load(REPO / "scripts" / "ft_pipeline.py", "ft_pipeline_under_test")
    mod._SERIES.clear()
    mod.WARN.clear()
    mod.INCOMPLETE.clear()
    return mod


@pytest.fixture(scope="session")
def scan_mod():
    pytest.importorskip("pandas")
    return _load(REPO / "scan" / "scan.py", "scan_under_test")


@pytest.fixture(scope="session")
def stored():
    """The stored ledger, history (keyed by (ticker, date)) and stocks, read once."""
    ledger = json.loads((REPO / "data" / "ledger.json").read_text(encoding="utf-8"))
    hist = {(r["ticker"], r["date"]): r for r in json.loads((REPO / "data" / "history.json").read_text(encoding="utf-8"))}
    stocks = json.loads((REPO / "data" / "stocks.json").read_text(encoding="utf-8"))
    return {"ledger": ledger, "hist": hist, "stocks": stocks}


@pytest.fixture()
def data(stored):
    """A deep copy, so a test can change it freely."""
    return copy.deepcopy(stored)


def perf_rows(ledger):
    return [(r["date"], r["value_est"], r["day_pct"]) for r in ledger if r["table"] == "perf"]


def bar(ticker, date, value, observed=True, volume=100):
    row = {"ticker": ticker, "date": date, "open": value, "high": value + 1, "low": value - 1, "close": value, "volume": volume}
    if not observed:
        row["open_obs"] = False
    return row


# Seven US sessions after the game's last stored one, for synthetic cases.
DATES = ["2026-10-19", "2026-10-20", "2026-10-21", "2026-10-22", "2026-10-23", "2026-10-26", "2026-10-27"]
