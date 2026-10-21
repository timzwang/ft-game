"""How the price feed's run of 21 Oct 2026 (GitHub, 11:48 UTC, session 20 Oct) compares with the stored prices, from
the feed's own check blocks: each ticker's last 25 sessions against data/history.json at main 323663b (or, for a panel
stock, against data/panel.json). A stored close-only row is compared on the close alone.

    python3 proposals/claude/2026-10-21-evidence/feed_check_against_store.py <feed latest.json> <history.json>
"""
import json
import sys

F = json.load(open(sys.argv[1]))
stored = {r["ticker"] for r in json.load(open(sys.argv[2]))}
for label, keep in (("price store (data/history.json)", lambda t: t in stored), ("panel only (data/panel.json)", lambda t: t not in stored)):
    closes, opens, bigc, bigo = [], [], [], []
    for t, e in sorted(F["tickers"].items()):
        if not keep(t):
            continue
        for x in e["check"]["rows"]:
            closes.append(abs(x["close"]))
            if abs(x["close"]) > 0.01:
                bigc.append(f"{t} {x['date']} {x['close']:+.3f}%")
            if x.get("open") is not None:
                opens.append(abs(x["open"]))
                if abs(x["open"]) > 0.2:
                    bigo.append(f"{t} {x['date']} {x['open']:+.3f}%")
    n_t = sum(1 for t in F["tickers"] if keep(t))
    print(f"{label}: {n_t} tickers")
    print(f"  closes compared: {len(closes)}; within 0.01%: {sum(1 for c in closes if c <= 0.01)}; largest gap {max(closes or [0]):.3f}%")
    print(f"  opens compared (stored rows with a traded open): {len(opens)}; within 0.05%: {sum(1 for o in opens if o <= 0.05)}; beyond 0.2%: {len(bigo)}")
    print("  closes beyond 0.01%: " + ("; ".join(bigc) or "none"))
    print("  opens beyond 0.2%: " + ("; ".join(bigo) or "none"))
print("disagreeing tickers (close beyond 0.5%, or open, high, low beyond 1.5%): " + (", ".join(F["meta"]["mismatched"]) or "none"))
