#!/usr/bin/env python3
"""Do the scan's leading names add anything the portfolio does not already hold? (Claude, 19 Oct 2026 evening.)

Reads data/ledger.json, data/history.json and data/stocks.json. For the order in force (Mon 19 Oct) and every watchlist
stock with enough stored prices, over the latest 60 common sessions:
  - correlation of the candidate's daily return with the portfolio's daily return (weights fixed at today's order);
  - its highest correlation with any single holding, and which;
  - its theme and the theme's weight in the order now.
London lines use their US-listed shares where the store has them (SHEL-US, BP-US), as the pipeline's analysis does.
Run from the repository root: python3 -I proposals/claude/2026-10-19-evidence-3/portfolio_fit.py
"""
import json
import math
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
H = json.loads((REPO / "data" / "history.json").read_text())
S = json.loads((REPO / "data" / "stocks.json").read_text())
LINE = {"SHEL": "SHEL-US", "BP.": "BP-US"}
closes = {}
for r in H:
    closes.setdefault(r["ticker"], {})[r["date"]] = r["close"]


def rets(t):
    c = closes.get(LINE.get(t, t), {})
    ds = sorted(c)
    return {ds[i]: c[ds[i]] / c[ds[i - 1]] - 1 for i in range(1, len(ds))}


def corr(a, b):
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    sa = math.sqrt(sum((x - ma) ** 2 for x in a))
    sb = math.sqrt(sum((y - mb) ** 2 for y in b))
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (sa * sb) if sa and sb else float("nan")


held = {r["name"]: (r["ticker"], r["weight"], r["theme"]) for r in S if r["group"] == "Portfolio" and (r["weight"] or 0) > 0}
watch = {r["name"]: (r["ticker"], r["score"], r["theme"]) for r in S if r["group"] == "Watchlist"}
themes = {}
for n, (t, w, th) in held.items():
    themes[th] = themes.get(th, 0) + w
R = {n: rets(t) for n, (t, _, _) in {**{k: (v[0], 0, 0) for k, v in held.items()}, **{k: (v[0], 0, 0) for k, v in watch.items()}}.items()}
common = set.intersection(*(set(R[n]) for n in held))
common = sorted(common)[-60:]
port = [sum(held[n][1] / 100 * R[n][d] for n in held) for d in common]
print(f"Order in force (Mon 19 Oct): themes {', '.join(f'{k} {v:g}%' for k, v in sorted(themes.items(), key=lambda x: -x[1]))}; "
      f"{len(common)} common sessions to {common[-1]}")
print("\nHoldings, correlation with the rest of the portfolio:")
for n, (t, w, th) in sorted(held.items(), key=lambda x: -x[1][1]):
    rest = [sum(held[m][1] / 100 * R[m][d] for m in held if m != n) for d in common]
    print(f"    {n:18} {w:4g}%  {th:17}  {corr([R[n][d] for d in common], rest):+.2f}")
print("\nWatchlist, by score: correlation with the portfolio, highest with one holding")
out = []
for n, (t, sc, th) in watch.items():
    if not all(d in R[n] for d in common):
        continue
    x = [R[n][d] for d in common]
    pc = corr(x, port)
    best = max(((corr(x, [R[m][d] for d in common]), m) for m in held), key=lambda z: z[0])
    out.append((sc, n, th, pc, best))
for sc, n, th, pc, (bc, bm) in sorted(out, key=lambda z: -z[0]):
    print(f"    {n:20} score {sc:3}  {th:17} (theme now {themes.get(th, 0):g}%)  with portfolio {pc:+.2f}, highest {bc:+.2f} ({bm})")
