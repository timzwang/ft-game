"""Minimal reproducible example: drift settlement in pipeline v6 (close basis) vs v7 (next-open basis).
Run: python3 drift_repro.py <path to v6 script> <path to v7 script>"""
import importlib.util, sys
def load(p, n):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
v6, v7 = load(sys.argv[1], "v6"), load(sys.argv[2], "v7")
days = ["2026-11-02", "2026-11-03", "2026-11-04", "2026-11-05", "2026-11-06", "2026-11-09", "2026-11-10"]
# Reporter XYZ: reaction day 2 Nov closes 100; gaps up to 108 at the 3 Nov open (the first price an order can get), closes 108 on 9 Nov.
xyz = {"2026-11-02": (95, 100), "2026-11-03": (108, 107), "2026-11-04": (107, 107.5), "2026-11-05": (107.5, 107),
       "2026-11-06": (107, 107.8), "2026-11-09": (107.8, 108), "2026-11-10": (108, 108)}
spy = {d: (500.0, 500.0) for d in days}       # flat index, so excess = own return
def hist():
    h = {}
    for d in days:
        o, c = xyz[d]; h[("XYZ", d)] = {"ticker": "XYZ", "date": d, "open": o, "high": max(o, c), "low": min(o, c), "close": c, "volume": 1e6}
        o, c = spy[d]; h[("SPY", d)] = {"ticker": "SPY", "date": d, "open": o, "high": o, "low": o, "close": c, "volume": 1e6}
    return h
for name, mod in (("v6", v6), ("v7", v7)):
    mod._SERIES.clear() if hasattr(mod, "_SERIES") else None
    led = [mod.lrow("drift", date="2026-11-02", name="XYZ", ticker="XYZ", kind="enter")]
    mod.resolve_drift(led, hist(), "SPY")
    r = led[0]
    print(name, "ret_pct", r["ret_pct"], "spx", r["spx_ret_pct"], "beat", r["beat"], "basis", r.get("unit") or "reaction close")
print("Expected tradable result: bought at the 3 Nov open 108, valued at the 9 Nov close 108: 0.00%. v6 reports +8.00% (includes the gap no order could capture).")
