"""Historical outputs, 7.5 against 7.6 (Claude, 19 Oct 2026, late evening).

    python3 proposals/claude/2026-10-19-evidence-4/compare_75_76.py --old <checkout of main 1b89752> --new <this branch>

On the frozen 16 Oct snapshot: (1) the 16 Oct session re-run end to end with `run`, each version on identical inputs,
and every output file compared; (2) the performance log, the contribution rows and the STANDSTILL rows rebuilt from
scratch by each version and compared row by row; (3) the data check on the snapshot. Writes only to a temporary folder.
"""
import argparse
import contextlib
import gzip
import importlib.util
import io
import json
import shutil
import sys
import tempfile
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--old", type=Path, required=True)
ap.add_argument("--new", type=Path, required=True)
A = ap.parse_args()
SNAP = A.new / "tests/fixtures/snapshot-2026-10-16"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def unpack(dst):
    (dst / "data").mkdir(parents=True)
    for n in ("history", "ledger", "macro", "panel", "stocks"):
        with gzip.open(SNAP / f"{n}.json.gz", "rb") as s, open(dst / "data" / f"{n}.json", "wb") as d:
            shutil.copyfileobj(s, d)


sys.path.insert(0, str(A.new / "tests"))
build = load(A.new / "tests/test_run.py", "builder")
out = {"session": None, "files": {}, "rebuild": {}, "printout_only_in_new": [], "printout_only_in_old": []}
with tempfile.TemporaryDirectory() as t:
    tmp = Path(t)
    unpack(tmp / "in")
    stored = {"ledger": json.loads((tmp / "in/data/ledger.json").read_text()),
              "hist": {(r["ticker"], r["date"]): r for r in json.loads((tmp / "in/data/history.json").read_text())},
              "stocks": json.loads((tmp / "in/data/stocks.json").read_text())}
    res = {}
    for tag, root in (("old", A.old), ("new", A.new)):
        pl = load(root / "scripts/ft_pipeline.py", "pl_" + tag)
        work = tmp / tag
        work.mkdir()
        today, session = build.build_today(pl, tmp / "in", work, stored)
        out["session"] = session
        led, txt, od = build.run(pl, tmp / "in", work, today)
        res[tag] = (pl, od, txt)
    pl_old, od_old, txt_old = res["old"]
    pl_new, od_new, txt_new = res["new"]
    for f in sorted(p.name for p in od_new.iterdir()):
        a, b = (od_old / f).read_bytes(), (od_new / f).read_bytes()
        if a == b:
            out["files"][f] = "identical"
            continue
        if f == "ledger.json":
            la, lb = json.loads(a), json.loads(b)
            sa, sb = {json.dumps(r, sort_keys=True) for r in la}, {json.dumps(r, sort_keys=True) for r in lb}
            out["files"][f] = {"rows_old": len(la), "rows_new": len(lb), "only_in_new": sorted(sb - sa), "only_in_old": sorted(sa - sb)}
        else:
            out["files"][f] = "DIFFERENT"
    lo, ln = set(txt_old.splitlines()), set(txt_new.splitlines())
    out["printout_only_in_new"] = [x for x in txt_new.splitlines() if x not in lo]
    out["printout_only_in_old"] = [x for x in txt_old.splitlines() if x not in ln]
    # (2) the performance log and STANDSTILL rebuilt from nothing
    for tag, pl in (("old", pl_old), ("new", pl_new)):
        L = [dict(r) for r in stored["ledger"] if r["table"] not in ("perf", "contrib", "standstill")]
        pl._SERIES.clear(); pl.INCOMPLETE.clear(); pl.WARN.clear()
        with contextlib.redirect_stdout(io.StringIO()):
            pl.update_performance(L, stored["hist"], "SPY", out["session"])
            ss = pl.standstill_rows(L, stored["hist"], "SPY", out["session"])
        out["rebuild"][tag] = {"perf": [(r["date"], r["value_est"], r["day_pct"]) for r in L if r["table"] == "perf"],
                               "contrib": sorted((r["date"], r["name"], r["contrib_pts"]) for r in L if r["table"] == "contrib"),
                               "standstill": sorted((r["name"], r["kind"], r["value"], r["text"]) for r in ss),
                               "incomplete": list(pl.INCOMPLETE)}
    ro, rn = out["rebuild"]["old"], out["rebuild"]["new"]
    out["rebuild_identical"] = {k: ro[k] == rn[k] for k in ("perf", "contrib", "standstill", "incomplete")}
    out["rebuild_final_value"] = {"old": ro["perf"][-1], "new": rn["perf"][-1]}
    del out["rebuild"]
print(json.dumps(out, indent=1))
