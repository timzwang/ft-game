#!/usr/bin/env python3
"""Independent reconstruction of every discretionary order change (Claude, 19 Oct 2026, evening review of ChatGPT's
follow-up). Written from scratch: it reads only data/ledger.json (position rows) and data/history.json (prices) and
does NOT call the pipeline, so it is a second opinion on the STANDSTILL change rows.

For each change filling at the open of E:
  - legs: the weight change of every stock (new minus old), including cash;
  - effect over the change's own window (E to the 5th session from E, or the latest stored session), buy and hold
    from E's open for every leg (both the new and the old order earn the previous close to E's open on the weight
    they share, so the difference starts at the open). The pipeline's STANDSTILL rows reset weights daily; the gap
    between the two methods is second order;
  - split into: cash deployed at the market (net weight change x SPY's return) and selection (each leg's weight
    change x its return above SPY over the same window);
  - each leg's contribution, so it is visible whether one sector move explains the result.
Nothing here is a forecast. Run from the repository root:  python3 -I proposals/claude/2026-10-19-evidence-3/change_attribution.py
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
L = json.loads((REPO / "data" / "ledger.json").read_text())
H = json.loads((REPO / "data" / "history.json").read_text())
px = {(r["ticker"], r["date"]): r for r in H}
spy = sorted(r["date"] for r in H if r["ticker"] == "SPY")
pos = sorted((r for r in L if r["table"] == "position"), key=lambda r: r["effective"])
tick = {r["name"]: r["ticker"] for r in pos}
theme = {r["name"]: r["theme"] for r in L if r["table"] == "risk"}
theme.update({"RTX": "Defence", "Lockheed Martin": "Defence", "Nvidia": "AI and chips", "TSMC": "AI and chips",
              "Goldman Sachs": "Banks", "Meta Platforms": "AI and chips", "Palantir": "Software",
              "Coca-Cola": "Consumer staples", "Microsoft": "Software", "Eli Lilly": "Health care",
              "Exxon Mobil": "Energy", "Chevron": "Energy", "Shell": "Energy", "AbbVie": "Health care"})


def weights(d):
    w = {}
    for r in pos:
        if r["effective"] <= d:
            w[r["name"]] = r["weight"] or 0.0
    return {n: x for n, x in w.items() if x > 0}


def ret(t, d0, d1, start="open"):
    a, b = px.get((t, d0)), px.get((t, d1))
    if not a or not b:
        return None
    return b["close"] / a[start] - 1.0


effs = sorted({r["effective"] for r in pos})
first = effs[0]
last = spy[-1]
out = []
for e in effs[1:]:
    if e > last:
        print(f"Change for {e}: not filled in the stored data (prices end {last})")
        continue
    i = spy.index(e)
    window = spy[i:i + 5]
    end = window[-1]
    w0, w1 = weights(spy[i - 1]), weights(e)
    legs = {n: w1.get(n, 0.0) - w0.get(n, 0.0) for n in set(w0) | set(w1)}
    legs = {n: d for n, d in legs.items() if abs(d) > 1e-9}
    r_spy = ret("SPY", e, end)
    total, sel, rows = 0.0, 0.0, []
    for n, d in sorted(legs.items(), key=lambda x: x[1]):
        r = ret(tick[n], e, end)
        total += d * r
        sel += d * (r - r_spy)
        rows.append((n, theme.get(n, "?"), d, r * 100, d * r, d * (r - r_spy)))
    net = sum(legs.values())
    print(f"Change for {e} (window {e} to {end}, {len(window)} session(s){'' if len(window) == 5 else ', running'}): "
          f"effect {total:+.3f} points = cash deployed {net * r_spy:+.3f} (net weight {net:+g} x SPY {r_spy * 100:+.2f}%) "
          f"+ selection {sel:+.3f}")
    for n, th, d, r, c, s in rows:
        print(f"    {n:16} {th:17} {d:+5g}  return {r:+6.2f}%  effect {c:+.3f}  vs SPY {s:+.3f}")
    out.append({"effective": e, "window_end": end, "sessions": len(window), "effect_pts": round(total, 3),
                "cash_pts": round(net * r_spy, 3), "selection_pts": round(sel, 3),
                "legs": [{"name": n, "theme": th, "dw": d, "ret_pct": round(r, 2), "pts": round(c, 3)} for n, th, d, r, c, s in rows]})

# Inception baselines, buy and hold from the first fill to the latest stored close
w_first = weights(first)
tot = sum(w_first.values())
bh = sum(w * ret(tick[n], first, last) for n, w in w_first.items())
bh_full = bh * 100.0 / tot
act = next(r for r in L if r["table"] == "perf" and r["date"] == last)["cum_pct"]
spy_ret = (px[("SPY", last)]["close"] / 776.24 - 1) * 100       # spy_base meta row
print(f"\nFirst order held (buy and hold from {first} open to {last} close): as entered {bh:+.3f}%, fully invested "
      f"{bh_full:+.3f}%; actual estimate {act:+.3f}%; SPY {spy_ret:+.3f}%")
print(f"Changes against the first order: as entered {act - bh:+.3f} points, fully invested {act - bh_full:+.3f} points")
json.dump(out, sys.stdout if "--json" in sys.argv else open("/dev/null", "w"), indent=1)
