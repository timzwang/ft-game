"""Pipeline 7.2 against 7.3 on the same inputs (19 Oct 2026).

Re-runs the last stored session (Fri 16 Oct) end to end with both scripts from the same today.json and stored files,
then compares every output file. Expected: stocks, history, macro, panel and scores byte for byte the same; the
ledger the same except the new "results_budget" meta row (7.3 writes it on every run).

    python proposals/claude/2026-10-19-evidence/compare_72_73.py --old OLD_7_2.py --repo .
    (git show 25e8a93:scripts/ft_pipeline.py > OLD_7_2.py gives the 7.2 script)
"""
import argparse
import contextlib
import importlib.util
import io
import json
import sys
import tempfile
from pathlib import Path


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def today_json(pl, repo, tmp):
    tpl = tmp / "template.json"
    with contextlib.redirect_stdout(io.StringIO()):
        pl.cmd_template({"stocks": str(repo / "data/stocks.json"), "ledger": str(repo / "data/ledger.json"),
                         "history": str(repo / "data/history.json"), "panel": str(repo / "data/panel.json"), "out": str(tpl)})
    today = json.loads(tpl.read_text(encoding="utf-8"))
    ledger = json.loads((repo / "data/ledger.json").read_text(encoding="utf-8"))
    hist = {(r["ticker"], r["date"]): r for r in json.loads((repo / "data/history.json").read_text(encoding="utf-8"))}
    stocks = {r["ticker"]: r for r in json.loads((repo / "data/stocks.json").read_text(encoding="utf-8"))}
    session = max(r["date"] for r in ledger if r["table"] == "perf")
    today.update({"date": session, "prices_as_of": "stored close", "order_for": "next open"})
    for s in today["stocks"]:
        b = hist.get((s["ticker"], session))
        if b:
            s["quote"].update({k: b[k] for k in ("open", "high", "low", "volume")})
            s["quote"]["price"] = b["close"]
            before = sorted((r for (t, d), r in hist.items() if t == s["ticker"] and d < session), key=lambda r: r["date"])
            s["quote"]["prev_close"] = before[-1]["close"] if before else None
        for k in ("week52_high", "week52_low", "target"):
            s["quote"][k] = (stocks.get(s["ticker"]) or {}).get(k)
    path = tmp / "today.json"
    path.write_text(json.dumps(today), encoding="utf-8")
    return path, session


def run(pl, repo, today, out):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        pl.cmd_run({"today": str(today), "ledger": str(repo / "data/ledger.json"), "history": str(repo / "data/history.json"),
                    "macro": str(repo / "data/macro.json"), "panel": str(repo / "data/panel.json"), "out": str(out)})
    return buf.getvalue()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--old", type=Path, required=True)
    ap.add_argument("--repo", type=Path, default=Path("."))
    a = ap.parse_args()
    repo = a.repo.resolve()
    new = load(repo / "scripts/ft_pipeline.py", "pl73")
    old = load(a.old, "pl72")
    result = {"old_version": old.PIPELINE_VERSION, "new_version": new.PIPELINE_VERSION}
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        today, session = today_json(new, repo, tmp)
        result["session"] = session
        text = {}
        for name, pl in (("old", old), ("new", new)):
            pl._SERIES.clear(); pl.WARN.clear(); pl.INCOMPLETE.clear()
            text[name] = run(pl, repo, today, tmp / name)
        files = sorted(p.name for p in (tmp / "new").iterdir())
        result["files"] = {}
        for f in files:
            o, n = (tmp / "old" / f).read_bytes(), (tmp / "new" / f).read_bytes()
            if f != "ledger.json":
                result["files"][f] = "identical" if o == n else "DIFFERENT"
                continue
            lo, ln = json.loads(o), json.loads(n)
            only_new = [r for r in ln if r not in lo]
            only_old = [r for r in lo if r not in ln]
            result["files"][f] = {"rows_old": len(lo), "rows_new": len(ln),
                                  "only_in_new": [(r["table"], r["name"]) for r in only_new],
                                  "only_in_old": [(r["table"], r["name"]) for r in only_old]}
        result["printout_lines_only_in_new"] = [l for l in text["new"].splitlines() if l not in text["old"].splitlines()]
        result["printout_lines_only_in_old"] = [l for l in text["old"].splitlines() if l not in text["new"].splitlines()]
    print(json.dumps(result, indent=1))
    ok = all(v == "identical" for k, v in result["files"].items() if k != "ledger.json") and \
        result["files"]["ledger.json"]["only_in_old"] == [] and \
        all(t_ == "meta" for t_, _ in result["files"]["ledger.json"]["only_in_new"])
    print("RESULT:", "same figures (only the new meta rows differ)" if ok else "DIFFERENCES FOUND")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
