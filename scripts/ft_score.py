#!/usr/bin/env python3
"""ft_score.py: technical metrics and a composite score (0 to 100) for stock candidates.

Usage: python3 ft_score.py input.json [output.json]

Input JSON:
{
  "as_of": "Thu 8 Oct close",
  "regime": "mixed",                      # "risk-on", "mixed" or "risk-off"
  "benchmark": {"name": "SPY", "change_52w_pct": 16.85, "five_day_pct": 1.30},
  "stocks": [{
    "name": "Exxon Mobil", "ticker": "XOM",
    "price": 168.50, "prev_close": 164.05, "open": 167.11, "high": 169.19, "low": 166.71,
    "volume": 13285721, "avg_vol_20d": 12737628,
    "ma50": 161.59, "ma200": 150.33, "rsi": 65.6,
    "week52_high": 176.41, "week52_low": 110.39, "change_52w_pct": 48.97,
    "five_day_pct": 2.86,                 # or "closes": [oldest ... newest] with at least 6 values
    "trend_price": null,                  # optional: price in the same currency as ma50/ma200 (use for
                                          # London stocks whose averages come from the US-listed ADR)
    "catalyst_pts": 10, "catalyst_note": "Results 30 Oct",
    "revisions_pts": 12, "revisions_note": "UBS target raise 8 Oct"
  }]
}
Every numeric field may be null. Missing inputs earn half marks for that item and are listed in data_gaps.

Score = trend (40) + short term (20) + catalyst (20) + revisions (20).
"""
import json
import sys


def num(x):
    try:
        if x is None or x == "":
            return None
        v = float(x)
        return None if v != v else v
    except (TypeError, ValueError):
        return None


def pct(a, b):
    if a is None or b is None or b == 0:
        return None
    return (a / b - 1.0) * 100.0


def band(value, steps, default=0):
    """steps: list of (threshold, points), checked in order; first threshold the value meets wins."""
    for threshold, points in steps:
        if value >= threshold:
            return points
    return default


def score_stock(s, bench, regime):
    gaps, flags, warnings = [], [], []
    price = num(s.get("price"))
    tprice = num(s.get("trend_price")) or price
    prev, opn = num(s.get("prev_close")), num(s.get("open"))
    high, low = num(s.get("high")), num(s.get("low"))
    vol, avgvol = num(s.get("volume")), num(s.get("avg_vol_20d"))
    ma50, ma200, rsi = num(s.get("ma50")), num(s.get("ma200")), num(s.get("rsi"))
    hi52, lo52 = num(s.get("week52_high")), num(s.get("week52_low"))
    chg52 = num(s.get("change_52w_pct"))
    closes = [num(c) for c in (s.get("closes") or []) if num(c) is not None]

    # ---- sanity checks on the inputs -------------------------------------------------
    if price is not None and high is not None and low is not None:
        if not (low * 0.995 <= price <= high * 1.005):
            warnings.append("price outside the day's range")
        if high < low:
            warnings.append("day high below day low")
    if price is not None and hi52 is not None and price > hi52 * 1.001:
        hi52 = price  # a new high today
    if price is not None and lo52 is not None and price < lo52 * 0.999:
        lo52 = price
    if tprice is not None and ma50 is not None and not (0.5 <= tprice / ma50 <= 2.0):
        warnings.append("50-day average looks wrong for this price (check currency)")
    if rsi is not None and not (0 <= rsi <= 100):
        warnings.append("RSI out of range")
        rsi = None

    # ---- derived metrics -------------------------------------------------------------
    vs50, vs200 = pct(tprice, ma50), pct(tprice, ma200)
    off_high = pct(price, hi52)
    day_pct, gap_pct, from_open = pct(price, prev), pct(opn, prev), pct(price, opn)
    five = num(s.get("five_day_pct"))
    if five is None and len(closes) >= 6:
        five = pct(closes[-1], closes[-6])
    range_pos = None
    if price is not None and high is not None and low is not None and high > low:
        range_pos = (price - low) / (high - low)
    vol_ratio = vol / avgvol if (vol is not None and avgvol) else None
    avg_abs = None
    if len(closes) >= 4:
        moves = [abs(pct(closes[i], closes[i - 1])) for i in range(1, len(closes))]
        avg_abs = sum(moves) / len(moves)
    b52, b5 = num(bench.get("change_52w_pct")), num(bench.get("five_day_pct"))
    rs52 = chg52 - b52 if (chg52 is not None and b52 is not None) else None
    rs5 = five - b5 if (five is not None and b5 is not None) else None

    parts = {}

    # ---- trend: 40 points ------------------------------------------------------------
    if vs50 is None:
        parts["vs_50d"] = 6; gaps.append("50-day average")
    elif vs50 < -5: parts["vs_50d"] = 0
    elif vs50 < 0: parts["vs_50d"] = 3
    elif vs50 < 2: parts["vs_50d"] = 8
    elif vs50 <= 15: parts["vs_50d"] = 12
    elif vs50 <= 25: parts["vs_50d"] = 8
    else: parts["vs_50d"] = 4

    if ma50 is None or ma200 is None or tprice is None:
        parts["structure"] = 4; gaps.append("200-day average")
    else:
        parts["structure"] = (5 if ma50 > ma200 else 0) + (3 if tprice > ma200 else 0)

    if off_high is None:
        parts["near_high"] = 5; gaps.append("52-week high")
    else:
        parts["near_high"] = band(off_high, [(-3, 10), (-8, 7), (-15, 4), (-25, 2)])

    if rs52 is None:
        parts["rs_52w"] = 3; gaps.append("52-week change")
    else:
        parts["rs_52w"] = band(rs52, [(30, 6), (10, 4), (0, 2)])

    if rsi is None:
        parts["rsi"] = 2; gaps.append("RSI")
    elif rsi > 80: parts["rsi"] = 0
    elif rsi >= 70: parts["rsi"] = 2
    elif rsi >= 50: parts["rsi"] = 4
    elif rsi >= 40: parts["rsi"] = 2
    else: parts["rsi"] = 0
    trend = sum(parts[k] for k in ("vs_50d", "structure", "near_high", "rs_52w", "rsi"))

    # ---- short term: 20 points -------------------------------------------------------
    if rs5 is None:
        parts["rs_5d"] = 4; gaps.append("5-day return")
    else:
        parts["rs_5d"] = band(rs5, [(3, 8), (1, 6), (0, 4), (-2, 2)])

    if from_open is None or range_pos is None:
        parts["session"] = 3; gaps.append("open, high or low")
    else:
        parts["session"] = (3 if from_open > 0 else 0) + (3 if range_pos >= 0.5 else 0)

    if day_pct is None or vol_ratio is None:
        parts["volume"] = 3; gaps.append("volume")
    elif day_pct > 0:
        parts["volume"] = 6 if vol_ratio >= 1.3 else 4 if vol_ratio >= 0.8 else 2
    else:
        parts["volume"] = 0 if vol_ratio >= 1.3 else 2
    short = parts["rs_5d"] + parts["session"] + parts["volume"]

    # ---- judgement inputs: 20 points each --------------------------------------------
    cat = num(s.get("catalyst_pts"))
    if cat is None:
        cat = 6; gaps.append("catalyst not rated")
    rev = num(s.get("revisions_pts"))
    if rev is None:
        rev = 8; gaps.append("revisions not rated")
    cat, rev = max(0, min(20, cat)), max(0, min(20, rev))

    score = round(trend + short + cat + rev)

    # ---- flags -----------------------------------------------------------------------
    if vs50 is not None and vs50 < 0: flags.append("below 50-day average")
    if ma50 is not None and ma200 is not None and ma50 < ma200: flags.append("downtrend: 50-day below 200-day")
    if vs50 is not None and vs50 > 15: flags.append("extended: more than 15% above 50-day")
    if rsi is not None and rsi > 75: flags.append("overbought: RSI above 75")
    if rsi is not None and rsi < 35: flags.append("oversold: RSI below 35")
    if day_pct is not None and vol_ratio is not None and day_pct < 0 and vol_ratio >= 1.3:
        flags.append("heavy-volume down day")
    if gap_pct is not None and from_open is not None and gap_pct > 1 and from_open < 0:
        flags.append("faded gap")
    if off_high is not None and off_high >= -0.5: flags.append("at 52-week high")

    conf = 50 + 0.35 * (score - 40)  # a score of 40 is treated as a coin flip; unvalidated prior
    if regime == "risk-off":
        conf -= 3
    conf = int(round(max(40, min(68, conf))))

    weight_cap = None
    if avg_abs:
        weight_cap = int(max(5, min(20, round(30.0 / avg_abs / 5.0) * 5)))

    r2 = lambda v: None if v is None else round(v, 2)
    return {
        "name": s.get("name"), "ticker": s.get("ticker"),
        "score": score, "confidence_anchor": conf,
        "trend_pts": trend, "short_pts": short, "catalyst_pts": cat, "revisions_pts": rev,
        "parts": parts,
        "vs_50d_pct": r2(vs50), "vs_200d_pct": r2(vs200), "off_high_pct": r2(off_high),
        "rs_52w_pp": r2(rs52), "rs_5d_pp": r2(rs5), "rsi": r2(rsi),
        "day_pct": r2(day_pct), "gap_pct": r2(gap_pct), "from_open_pct": r2(from_open),
        "five_day_pct": r2(five), "range_pos": r2(range_pos), "vol_ratio": r2(vol_ratio),
        "avg_abs_move_pct": r2(avg_abs), "weight_cap_pct": weight_cap,
        "flags": flags, "data_gaps": gaps, "warnings": warnings,
        "catalyst_note": s.get("catalyst_note") or "", "revisions_note": s.get("revisions_note") or "",
    }


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    data = json.load(open(sys.argv[1]))
    bench = data.get("benchmark") or {}
    regime = data.get("regime") or "mixed"
    rows = [score_stock(s, bench, regime) for s in data.get("stocks", [])]
    rows.sort(key=lambda r: -r["score"])
    out = {"as_of": data.get("as_of"), "regime": regime, "benchmark": bench, "scores": rows}
    if len(sys.argv) > 2:
        json.dump(out, open(sys.argv[2], "w"), indent=1)
    f = lambda v, w=7: ("" if v is None else str(v)).rjust(w)
    print(f"As of {data.get('as_of')}; regime {regime}; benchmark {bench.get('name')}")
    print("Stock".ljust(18) + "Score Conf Trend Short  Cat  Rev  vs50d% offHigh%    RSI  5d-rs volR  Flags")
    for r in rows:
        print((r["name"] or "")[:17].ljust(18) + f(r["score"], 5) + f(r["confidence_anchor"], 5) + f(r["trend_pts"], 6)
              + f(r["short_pts"], 6) + f(int(r["catalyst_pts"]), 5) + f(int(r["revisions_pts"]), 5) + f(r["vs_50d_pct"])
              + f(r["off_high_pct"], 9) + f(r["rsi"]) + f(r["rs_5d_pp"]) + f(r["vol_ratio"], 5) + "  " + "; ".join(r["flags"]))
        if r["data_gaps"]:
            print("    data gaps: " + ", ".join(r["data_gaps"]))
        if r["warnings"]:
            print("    WARNING: " + "; ".join(r["warnings"]))


if __name__ == "__main__":
    main()
