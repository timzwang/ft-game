"""Independent reconstruction of the FT game portfolio (read-only; does not import ft_pipeline).

Game arithmetic as stated in playbook part C:
  - an order is a set of target weights (percent), filled at the next session's open;
  - weights reset to target at each close, so a session's portfolio return is the sum of weight x return;
  - on a session where a change fills: kept weight earns close/prev_close - 1, added weight earns close/open - 1,
    sold weight earns open/prev_close - 1; cash earns 0; no costs.
Benchmark: SPY price return from the 9 Oct open (776.24), the first fill, to each close.
"""
import csv, json, sys

H = json.load(open(sys.argv[1]))
EXTRA = json.load(open(sys.argv[2]))        # rows fetched 18 Oct for stocks no longer stored
P = {}
for r in H:
    P[(r["ticker"], r["date"])] = r
for r in EXTRA:
    P.setdefault((r["ticker"], r["date"]), r)   # stored rows win; extra rows only fill gaps

DAYS = ["2026-10-09", "2026-10-12", "2026-10-13", "2026-10-14", "2026-10-15", "2026-10-16"]
PREV = {"2026-10-09": "2026-10-08"}
for i in range(1, len(DAYS)):
    PREV[DAYS[i]] = DAYS[i - 1]

# Orders in force from the open of each session (from ledger position rows and the state doc trade log)
O = {}
O["2026-10-09"] = dict(XOM=15, CVX=15, SHEL=10, RTX=10, LMT=5, TSM=10, NVDA=10)          # cash 25
O["2026-10-12"] = dict(XOM=15, CVX=15, SHEL=10, TSM=10, NVDA=10, MSFT=15, KO=15, PLTR=5, GS=5)
O["2026-10-13"] = dict(O["2026-10-12"], SHEL=15, KO=20); del O["2026-10-13"]["NVDA"]
O["2026-10-14"] = dict(O["2026-10-13"], META=5); del O["2026-10-14"]["GS"]
O["2026-10-15"] = dict(O["2026-10-14"], MSFT=10, LLY=10); del O["2026-10-15"]["META"]
O["2026-10-16"] = dict(O["2026-10-15"], MSFT=15, LLY=15); del O["2026-10-16"]["TSM"]


def bar(t, d):
    return P.get((t, d))


def session(prev_w, new_w, d):
    """Portfolio return in points for session d, plus per-stock contributions and any missing prices."""
    pd = PREV[d]
    tot, parts, missing = 0.0, {}, []
    for t in sorted(set(prev_w) | set(new_w)):
        wp, wn = prev_w.get(t, 0), new_w.get(t, 0)
        b, pb = bar(t, d), bar(t, pd)
        need_prev = min(wp, wn) > 0 or wp > wn
        if b is None or (need_prev and pb is None):
            missing.append(t)
            continue
        c = 0.0
        k = min(wp, wn)
        if k:
            c += k * (b["close"] / pb["close"] - 1)
        if wn > wp:
            c += (wn - wp) * (b["close"] / b["open"] - 1)
        if wp > wn:
            c += (wp - wn) * (b["open"] / pb["close"] - 1)
        parts[t] = c
        tot += c
    return tot, parts, missing


def path(order_for_day):
    """Compound a strategy defined by the order in force each session. Returns list of (day, pts, value, missing)."""
    v, out, prev = 100000.0, [], {}
    for d in DAYS:
        w = order_for_day(d)
        if w is None:
            out.append((d, None, None, []))
            continue
        pts, parts, miss = session(prev, w, d)
        v *= 1 + pts / 100
        out.append((d, pts, v, miss, parts))
        prev = w
    return out


spy0 = bar("SPY", "2026-10-09")["open"]

# 1. Actual strategy
actual = path(lambda d: O[d])
rows = []
v_prev = 100000.0
for d, pts, v, miss, parts in actual:
    spy_day = (bar("SPY", d)["close"] / (bar("SPY", PREV[d])["close"] if d != "2026-10-09" else spy0) - 1) * 100
    spy_cum = (bar("SPY", d)["close"] / spy0 - 1) * 100
    rows.append(dict(date=d, port_pct=round(pts, 4), value=round(v, 2), cum_pct=round((v / 1e5 - 1) * 100, 4),
                     spy_day_pct=round(spy_day, 4), spy_cum_pct=round(spy_cum, 4),
                     excess_cum_pts=round((v / 1e5 - 1) * 100 - spy_cum, 4), missing=";".join(miss) or "none",
                     contributions=";".join(f"{t}:{c:+.4f}" for t, c in sorted(parts.items()))))
with open("daily_performance.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)
print("ACTUAL")
for r in rows:
    print(r["date"], r["port_pct"], r["value"], r["cum_pct"], "SPY", r["spy_day_pct"], r["spy_cum_pct"], "excess", r["excess_cum_pts"], "missing", r["missing"])

# 2. One-day counterfactual: keep the previous session's order for the fill day only
print("\nONE-DAY: change vs keeping the previous order on its fill day")
one = []
for d in DAYS[1:]:
    pd = PREV[d]
    a, _, m1 = session(O[pd], O[d], d)
    b, _, m2 = session(O[pd], O[pd], d)
    one.append((d, a, b, a - b, m1 + m2))
    print(d, f"actual {a:+.4f}  prev-order {b:+.4f}  effect {a-b:+.4f}  missing {m1+m2}")
print("sum 13-15 Oct:", round(sum(x[3] for x in one if x[0] in ("2026-10-13", "2026-10-14", "2026-10-15")), 4))
print("sum 12-16 Oct:", round(sum(x[3] for x in one), 4))

# 3. Each change against its replaced order held for up to five sessions (both from the fill)
print("\nFIVE-SESSION: each change vs the order it replaced, held fixed from the fill, to 16 Oct (max 5 sessions)")
for i, d in enumerate(DAYS[1:], 1):
    pd = DAYS[i - 1]
    span = DAYS[i:i + 5]
    va = vb = 1.0
    prev_a = prev_b = O[pd]
    miss = []
    for k, s in enumerate(span):
        new_a = O[d] if k == 0 else O[d]       # the new order held fixed
        a, _, m1 = session(prev_a, new_a, s); prev_a = new_a
        b, _, m2 = session(prev_b, O[pd], s); prev_b = O[pd]
        va *= 1 + a / 100; vb *= 1 + b / 100; miss += m1 + m2
    print(d, f"sessions {len(span)}  new {100*(va-1):+.3f}%  replaced {100*(vb-1):+.3f}%  effect {100*(va-vb):+.3f} pts  missing {sorted(set(miss))}")

# 4. Standstills over the whole record
def hold(order, start):
    return lambda d: (O[d] if d < start else order)

for label, f in [("Inception order held (9 Oct order, 25% cash), 9-16 Oct", lambda d: O["2026-10-09"]),
                 ("Inception order, cash spread pro rata (fully invested), 9-16 Oct",
                  lambda d: {t: w / 0.75 for t, w in O["2026-10-09"].items()}),
                 ("12 Oct order held from 12 Oct (actual 9 Oct before)", hold(O["2026-10-12"], "2026-10-12")),
                 ("13 Oct order held from 13 Oct", hold(O["2026-10-13"], "2026-10-13"))]:
    p = path(f)
    miss = sorted({m for x in p for m in x[3]})
    print(f"\n{label}: final {p[-1][2]:.2f} ({(p[-1][2]/1e5-1)*100:+.3f}%) missing {miss}")
    print("   ", [(x[0][5:], round(x[1], 3)) for x in p])

print(f"\nActual final {actual[-1][2]:.2f} ({(actual[-1][2]/1e5-1)*100:+.3f}%)")
print(f"SPY from 9 Oct open: {(bar('SPY','2026-10-16')['close']/spy0-1)*100:+.3f}%")
# Equal-weight SPY-like baseline not computed: no index constituents stored.
