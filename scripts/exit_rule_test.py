#!/usr/bin/env python3
"""Read-only test of the endgame exit rule on stored prices (3 Nov 2026; no live file reads or writes this).

The rule sells at the next open after a close below the open on volume of 1.3 times the 20-day average or more.
The fair question is not whether a signalled stock rises afterwards (on a sector sell-off everything rebounds) but
whether it does worse than the same list's stocks that gave no signal on the same date, because those are what the
sale buys. For each date: mean five-session return, next open to close, of the signalled names minus the others.
Dates are the unit of evidence, so a sector-wide day counts once. The list was chosen with hindsight: treat it as a
sanity check, not proof. Usage: python3 -I scripts/exit_rule_test.py [data/history.json]
"""
import json, math, statistics as st, sys, collections

TECH = "AMD MU SNDK ARM STX WDC SHOP DDOG NOW HOOD NET MPWR NTAP AMZN FTNT CRWD PANW ADI TXN FLEX AEIS".split()
path = sys.argv[1] if len(sys.argv) > 1 else "data/history.json"
H = json.load(open(path))
H = H if isinstance(H, list) else H["rows"]
by = collections.defaultdict(list)
for r in H:
    by[r["ticker"]].append(r)
rows = collections.defaultdict(dict)
for t in TECH:
    a = sorted((r for r in by.get(t, []) if r.get("volume") and r.get("open")), key=lambda r: r["date"])
    for i in range(21, len(a) - 5):
        r = a[i]
        avg = sum(x["volume"] for x in a[i - 20:i]) / 20
        fill = a[i + 1]["open"]
        if avg and fill:
            rows[r["date"]][t] = (r["close"] < r["open"] and r["volume"] >= 1.3 * avg, (a[i + 5]["close"] / fill - 1) * 100)


def test(lo, hi, label):
    d = []
    for m in rows.values():
        if len(m) < 10:
            continue
        sig = [v[1] for v in m.values() if v[0]]
        non = [v[1] for v in m.values() if not v[0]]
        if sig and non and lo <= len(sig) / len(m) < hi:
            d.append(st.mean(sig) - st.mean(non))
    if len(d) > 1:
        print(f"{label}: {len(d)} dates, sold minus kept over five sessions {st.mean(d):+.2f} points "
              f"(t {st.mean(d) / (st.stdev(d) / math.sqrt(len(d))):+.1f}), positive on {sum(x > 0 for x in d) / len(d):.0%}")


test(0, 2, "All signal dates")
test(0.4, 2, "Sector days (40% or more of the list signalled)")
test(0.15, 0.4, "Middling days (15% to 40%)")
test(0, 0.15, "Isolated signals (under 15%)")
