"""Shared fixtures for the regression tests (pipeline 7.3, 19 Oct 2026; frozen snapshot from 19 Oct evening).

Run from the repository root:  python -m pytest -q tests
The tests read the scripts from this checkout and the game data from a FROZEN snapshot of the Fri 16 Oct 2026 files
(`tests/fixtures/snapshot-2026-10-16/`, the data as mirrored at main f9241ee), never from `data/`. So a nightly data
commit can neither break nor silently pass a code test. Whether the live `data/` files are sound is a separate
question, answered by `scripts/check_data.py` and its workflow. They write nothing outside a temporary folder and
fetch nothing from the network.
"""
import copy
import gzip
import importlib.util
import json
import shutil
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SNAPSHOT = REPO / "tests" / "fixtures" / "snapshot-2026-10-16"
DATA_FILES = ("history", "ledger", "macro", "panel", "stocks")
STATE_DOC_LINE = "a9cde88a299142e44096fa7ab69490429d2f05d3aa456652ba04bda275cc9a4a  state/ft-game-state.md"   # as at f9241ee


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="session")
def repo(tmp_path_factory):
    """A folder laid out like the repository's data side (data/*.json, state/last-sync.md), unpacked from the frozen
    16 Oct snapshot. Tests that need the scripts use REPO."""
    root = tmp_path_factory.mktemp("snapshot")
    (root / "data").mkdir()
    (root / "state").mkdir()
    for n in DATA_FILES:
        with gzip.open(SNAPSHOT / f"{n}.json.gz", "rb") as src, open(root / "data" / f"{n}.json", "wb") as dst:
            shutil.copyfileobj(src, dst)
    shutil.copy(SNAPSHOT / "last-sync.md", root / "state" / "last-sync.md")
    # 7.6: every mirror must record the state doc too. The frozen last-sync.md (unchanged) left that line out, though the
    # real mirror at f9241ee recorded it; the state doc of that commit is frozen beside it, and its line is restored in
    # this temporary copy only. tests/test_check_data.py checks that the frozen record on its own now fails.
    shutil.copy(SNAPSHOT / "ft-game-state.md", root / "state" / "ft-game-state.md")
    with open(root / "state" / "last-sync.md", "r+", encoding="utf-8") as f:
        text = f.read().rstrip("\n")
        assert text.endswith("~~~")
        f.seek(0)
        f.write(text[:-3] + STATE_DOC_LINE + "\n~~~\n")
        f.truncate()
    return root


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
def stored(repo):
    """The frozen 16 Oct ledger, history (keyed by (ticker, date)) and stocks, read once."""
    ledger = json.loads((repo / "data" / "ledger.json").read_text(encoding="utf-8"))
    hist = {(r["ticker"], r["date"]): r for r in json.loads((repo / "data" / "history.json").read_text(encoding="utf-8"))}
    stocks = json.loads((repo / "data" / "stocks.json").read_text(encoding="utf-8"))
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
