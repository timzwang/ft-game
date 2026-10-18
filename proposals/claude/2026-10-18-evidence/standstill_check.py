"""Run pipeline v7's own standstill_rows on the live ledger and history (read-only), then again with the 18 Oct fetched rows added."""
import importlib.util, json, sys
s = importlib.util.spec_from_file_location("v7", sys.argv[1]); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
L = json.load(open(sys.argv[2])); H = json.load(open(sys.argv[3])); X = json.load(open(sys.argv[4]))
for label, rows in (("stored data only", H), ("stored + fetched 18 Oct", H + [{k: r[k] for k in ("ticker","date","open","high","low","close","volume")} for r in X])):
    hist = {(r["ticker"], r["date"]): r for r in rows}
    m._SERIES.clear()
    out = m.standstill_rows([dict(r) for r in L], hist, "SPY", "2026-10-16")
    print("==", label)
    for r in out:
        print(r["kind"], r["name"], r["days"], r["confirmed"], "effect", r["value"], "| new/actual", r["ret_pct"], "old/standstill", r["spx_ret_pct"], "|", r["text"][:110])
