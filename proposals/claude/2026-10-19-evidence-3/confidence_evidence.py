#!/usr/bin/env python3
"""What the settled confidence and shadow ratings can and cannot show (Claude, 19 Oct 2026 evening).

Reads data/ledger.json only. Prints, for the order's confidence ratings and the nightly shadow ratings:
  - how many have settled, and from how many distinct rating dates and five-session windows;
  - hit rate, mean rating and Brier score (treating the rating as if it were a probability, which is the question);
  - per rating date, the rank correlation between the anchor and the excess return;
  - the number of independent observations a 10-point calibration claim would need.
Run from the repository root: python3 -I proposals/claude/2026-10-19-evidence-3/confidence_evidence.py
"""
import json
import math
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
L = json.loads((REPO / "data" / "ledger.json").read_text())


def ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(xs):
        j = i
        while j + 1 < len(xs) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2.0
        i = j + 1
    return r


def spearman(a, b):
    ra, rb = ranks(a), ranks(b)
    ma, mb = sum(ra) / len(ra), sum(rb) / len(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = math.sqrt(sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb))
    return num / den if den else float("nan")


for table in ("confidence", "shadow"):
    rows = [r for r in L if r["table"] == table and r["beat"] in ("yes", "no")]
    if not rows:
        continue
    key = "effective" if table == "confidence" else "date"
    dates = sorted({r[key] for r in rows})
    windows = sorted({r["window_end"] for r in rows})
    hits = sum(r["beat"] == "yes" for r in rows)
    mean_conf = sum(r["confidence"] for r in rows) / len(rows)
    brier = sum((r["confidence"] / 100 - (r["beat"] == "yes")) ** 2 for r in rows) / len(rows)
    print(f"{table.upper()}: {len(rows)} settled, from {len(dates)} rating date(s) {dates} and {len(windows)} window end(s) {windows}")
    print(f"    beat the index {hits} of {len(rows)} ({hits / len(rows) * 100:.0f}%), mean rating {mean_conf:.1f}, "
          f"Brier {brier:.3f} (a constant 50 scores 0.250)")
    by = defaultdict(list)
    for r in rows:
        by[r[key]].append(r)
    for d in dates:
        g = by[d]
        if len(g) >= 5:
            rho = spearman([x["confidence"] for x in g], [x["ret_pct"] - x["spx_ret_pct"] for x in g])
            print(f"    {d}: {len(g)} ratings, rank correlation of rating with excess return {rho:+.2f}")
    bands = [(0, 49), (50, 54), (55, 59), (60, 64), (65, 100)]
    for lo, hi in bands:
        b = [r for r in rows if lo <= r["confidence"] <= hi]
        if b:
            print(f"    rated {lo} to {hi}: {len(b)}, beat {sum(r['beat'] == 'yes' for r in b)}")
# Sample size for a calibration claim: telling a true 60% from 50% at the usual 5% two-sided level with 80% power needs
# about n = ((1.96 * sqrt(0.25) + 0.84 * sqrt(0.24)) / 0.10) ** 2 independent forecasts.
n = ((1.96 * math.sqrt(0.25) + 0.84 * math.sqrt(0.24)) / 0.10) ** 2
print(f"\nIndependent forecasts needed to tell 60% from 50% (5% level, 80% power): about {n:.0f}. Ratings made on the same date "
      "share one market move, and windows five sessions apart are the only non-overlapping ones: about six remain before 27 Nov.")
