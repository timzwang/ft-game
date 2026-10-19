"""Rebuild the performance log, contribution rows and STANDSTILL rows of a mirror commit's data with two pipeline
versions and compare them (Claude, 19 Oct 2026). Usage: rebuild_on_mirror.py --data <checkout with data/> --old <dir> --new <dir>"""
import argparse, contextlib, importlib.util, io, json
from pathlib import Path
ap = argparse.ArgumentParser(); ap.add_argument("--data", type=Path); ap.add_argument("--old", type=Path); ap.add_argument("--new", type=Path)
A = ap.parse_args()
led = json.loads((A.data / "data/ledger.json").read_text()); hist = {(r["ticker"], r["date"]): r for r in json.loads((A.data / "data/history.json").read_text())}
last = max(r["date"] for r in led if r["table"] == "perf")
out = {}
for tag, root in (("old", A.old), ("new", A.new)):
    spec = importlib.util.spec_from_file_location("pl_" + tag, root / "scripts/ft_pipeline.py"); pl = importlib.util.module_from_spec(spec); spec.loader.exec_module(pl)
    mc = next((r for r in led if r["table"] == "meta" and r["name"] == "market_closed"), None)
    closed = {tuple(c) for c in json.loads(mc["text"])} if mc and mc.get("text") else set()
    L = [dict(r) for r in led if r["table"] not in ("perf", "contrib", "standstill")]
    with contextlib.redirect_stdout(io.StringIO()):
        pl.update_performance(L, hist, "SPY", last, closed)
        ss = pl.standstill_rows(L, hist, "SPY", last)
    out[tag] = {"version": pl.PIPELINE_VERSION, "perf": [(r["date"], r["value_est"], r["day_pct"]) for r in L if r["table"] == "perf"],
                "contrib": sorted((r["date"], r["name"], r["contrib_pts"]) for r in L if r["table"] == "contrib"),
                "standstill": sorted((r["name"], r["kind"], r["value"], r["text"]) for r in ss), "incomplete": list(pl.INCOMPLETE)}
stored = [(r["date"], r["value_est"], r["day_pct"]) for r in sorted((r for r in led if r["table"] == "perf"), key=lambda r: r["date"])]
print(json.dumps({"data_last_session": last, "versions": [out["old"]["version"], out["new"]["version"]],
                  "identical": {k: out["old"][k] == out["new"][k] for k in ("perf", "contrib", "standstill", "incomplete")},
                  "rebuild_equals_stored_perf": out["new"]["perf"] == stored, "final": out["new"]["perf"][-1]}, indent=1))
