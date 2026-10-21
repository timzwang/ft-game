"""Pipeline 7.6 against 7.7 (Claude, 21 Oct 2026): 7.7 adds the `feed` command and must change nothing else.

    python3 proposals/claude/2026-10-21-evidence/compare_76_77.py --old <file of 7.6> --new scripts/ft_pipeline.py --data <folder with data/*.json>

The last stored session is re-run end to end with `run`, each version on identical inputs built by tests/test_run.py's
builder, and every output file and every printed line compared. Run once on the frozen 16 Oct snapshot (tests/fixtures)
and once on the 20 Oct mirror (main 323663b). Writes only to a temporary folder.
"""
import argparse
import gzip
import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--old", type=Path, required=True)
ap.add_argument("--new", type=Path, required=True)
ap.add_argument("--data", type=Path, help="a folder holding data/*.json; default: the frozen 16 Oct snapshot")
A = ap.parse_args()
REPO = Path(__file__).resolve().parents[3]


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


sys.path.insert(0, str(REPO / "tests"))
build = load(REPO / "tests/test_run.py", "builder")
out = {"data": str(A.data or "snapshot-2026-10-16"), "session": None, "files": {}, "printout_only_in_new": [], "printout_only_in_old": []}
with tempfile.TemporaryDirectory() as t:
    tmp = Path(t)
    (tmp / "in/data").mkdir(parents=True)
    for n in ("history", "ledger", "macro", "panel", "stocks"):
        if A.data:
            shutil.copy(A.data / "data" / f"{n}.json", tmp / "in/data" / f"{n}.json")
        else:
            with gzip.open(REPO / "tests/fixtures/snapshot-2026-10-16" / f"{n}.json.gz", "rb") as s, open(tmp / "in/data" / f"{n}.json", "wb") as d:
                shutil.copyfileobj(s, d)
    stored = {"ledger": json.loads((tmp / "in/data/ledger.json").read_text()),
              "hist": {(r["ticker"], r["date"]): r for r in json.loads((tmp / "in/data/history.json").read_text())},
              "stocks": json.loads((tmp / "in/data/stocks.json").read_text())}
    res = {}
    for tag, path in (("old", A.old), ("new", A.new)):
        pl = load(path, "pl_" + tag)
        work = tmp / tag
        work.mkdir()
        today, session = build.build_today(pl, tmp / "in", work, stored)
        out["session"] = session
        led, txt, od = build.run(pl, tmp / "in", work, today)
        res[tag] = (od, txt)
    (od_old, txt_old), (od_new, txt_new) = res["old"], res["new"]
    for f in sorted(p.name for p in od_new.iterdir()):
        out["files"][f] = "identical" if (od_old / f).read_bytes() == (od_new / f).read_bytes() else "DIFFERENT"
    lo, ln = set(txt_old.splitlines()), set(txt_new.splitlines())
    out["printout_only_in_new"] = [x for x in txt_new.splitlines() if x not in lo]
    out["printout_only_in_old"] = [x for x in txt_old.splitlines() if x not in ln]
print(json.dumps(out, indent=1))
