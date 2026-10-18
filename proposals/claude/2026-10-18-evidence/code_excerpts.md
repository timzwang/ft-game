# Code excerpts (line-numbered)

Live pipeline v7: artifact asset fdfb8e108f26b962b62a9ca0a9909846 = repo scripts/ft_pipeline.py at main 4699b8a1, sha256 23e9c9fe7645ed4df2b66d5b8263378c983ed7c9c47e1bf0ef07531dca1867b1. v6: repo commit 9bd42e3 scripts/ft_pipeline.py, sha256 ea0433f2...c43414.

## Performance accounting: update_performance (v7 lines 545-600)
```python
 545  def update_performance(ledger, hist, bench, today_date):
 546      meta = {r["name"]: r for r in ledger if r["table"] == "meta"}
 547      start_date = meta["start_date"]["text"]
 548      start_value = num(meta["start_value"]["value"])
 549      spy_base = num(meta["spy_base"]["value"])
 550      brow = {r["date"]: r for r in series(hist, bench)}
 551      sessions = sorted(d for d in brow if start_date <= d <= today_date)
 552      done = {r["date"] for r in ledger if r["table"] == "perf" and r["value_est"] is not None}
 553      perf_rows = sorted((r for r in ledger if r["table"] == "perf" and r["value_est"] is not None), key=lambda r: r["date"])
 554      value = perf_rows[-1]["value_est"] if perf_rows else start_value
 555      added = []
 556      fills = {(r["name"], r["effective"]): num(r["value"]) for r in ledger if r["table"] == "position" and num(r["value"])}
 557      all_dates = sorted(brow)
 558      for d in sessions:
 559          if d in done:
 560              continue
 561          i = all_dates.index(d)
 562          dprev = all_dates[i - 1] if i > 0 else None
 563          w_new = live_weights(ledger, d)
 564          w_prev = live_weights(ledger, dprev) if (dprev and dprev >= start_date) else {}
 565          day = 0.0
 566          for name in sorted(set(w_new) | set(w_prev)):
 567              wn, tick = w_new.get(name, (0.0, None))
 568              wp, tick2 = w_prev.get(name, (0.0, None))
 569              tick = tick or tick2
 570              cur = hist.get((tick, d))
 571              prv = None
 572              if cur:
 573                  cutoff = dprev or ""
 574                  earlier = [r for r in series(hist, tick) if r["date"] <= cutoff]
 575                  prv = earlier[-1] if earlier else None
 576              if not cur:
 577                  warn(f"{name} {d}: no price row for this session, so its move was not counted (fine if that market was closed)")
 578                  continue
 579              kept, added_w, sold = min(wp, wn), max(wn - wp, 0.0), max(wp - wn, 0.0)
 580              contrib = 0.0
 581              if kept and prv:
 582                  contrib += kept * (cur["close"] / prv["close"] - 1.0)
 583              if added_w:
 584                  contrib += added_w * (cur["close"] / (fills.get((name, d)) or cur["open"]) - 1.0)   # bought at the open, or at a stated fill price
 585              if sold and prv:
 586                  contrib += sold * (cur["open"] / prv["close"] - 1.0)          # sold at the open
 587              if kept and not prv:
 588                  warn(f"{name} {d}: no earlier close in the history store; move not counted")
 589              day += contrib
 590              if wn or wp:
 591                  ledger.append(lrow("contrib", date=d, name=name, ticker=tick, weight=wn,
 592                                     ret_pct=r2(contrib / (wn or wp) * 100.0), contrib_pts=r2(contrib, 3)))
 593          value = value * (1.0 + day / 100.0)
 594          spx = pct(brow[d]["close"], spy_base)
 595          ledger.append(lrow("perf", date=d, value_est=r2(value), day_pct=r2(day, 3),
 596                             cum_pct=r2(pct(value, start_value), 3), spx_cum_pct=r2(spx, 3)))
 597          added.append(d)
 598      return added
 599  
 600  
```

## Order checks: check_order (no theme/risk limits enforced) (v7 lines 462-481)
```python
 462  def check_order(order):
 463      errs = []
 464      names = [o["name"] for o in order]
 465      if len(set(names)) != len(names):
 466          errs.append("a stock appears twice in the order")
 467      ws = [num(o.get("weight")) or 0 for o in order]
 468      if len([w for w in ws if w > 0]) < 5:
 469          errs.append("fewer than 5 stocks")
 470      if len(ws) > 20:
 471          errs.append("more than 20 stocks")
 472      for o, w in zip(order, ws):
 473          if w and not (5 <= w <= 25):
 474              errs.append(f"{o['name']} weight {w} is outside 5 to 25")
 475      cash = 100 - sum(ws)
 476      if cash < -1e-9:
 477          errs.append(f"weights total {sum(ws)}, above 100")
 478      if cash > 25 + 1e-9:
 479          errs.append(f"cash would be {cash}, above the 25 maximum")
 480      return errs, round(cash, 4)
 481  
```

## Scoring bands, flags, confidence anchor and volatility cap (v7 lines 361-449)
```python
 361      rs5 = five - b5 if (five is not None and b5 is not None) else None
 362      rs2m = two_m - b2m if (two_m is not None and b2m is not None) else None
 363      rs52 = chg52 - bench_52w if (chg52 is not None and bench_52w is not None) else None
 364      range_pos = (price - low) / (high - low) if (price is not None and high is not None and low is not None and high > low) else None
 365      vol_ratio = vol / avgvol if (vol and avgvol) else None
 366      atr = atr_pct(rows)
 367  
 368      p = {}
 369      if vs50 is None:
 370          p["vs_50d"] = 6; gaps.append("50-day average")
 371      elif vs50 < -5: p["vs_50d"] = 0
 372      elif vs50 < 0: p["vs_50d"] = 3
 373      elif vs50 < 2: p["vs_50d"] = 8
 374      elif vs50 <= 15: p["vs_50d"] = 12
 375      elif vs50 <= 25: p["vs_50d"] = 8
 376      else: p["vs_50d"] = 4
 377      if ma50 is None or ma200 is None or tprice is None:
 378          p["structure"] = 4; gaps.append("200-day average")
 379      else:
 380          p["structure"] = (5 if ma50 > ma200 else 0) + (3 if tprice > ma200 else 0)
 381      if off_high is None:
 382          p["near_high"] = 5; gaps.append("52-week high")
 383      else:
 384          p["near_high"] = band(off_high, [(-3, 10), (-8, 7), (-15, 4), (-25, 2)])
 385      if rs52 is None:
 386          p["rs_52w"] = 2; gaps.append("52-week change")
 387      else:
 388          p["rs_52w"] = band(rs52, [(30, 4), (10, 3), (0, 1)])
 389      if rs2m is None:
 390          p["rs_2m"] = 1; gaps.append("two-month return")
 391      else:
 392          p["rs_2m"] = band(rs2m, [(5, 2), (0, 1)])
 393      if rsi is None:
 394          p["rsi"] = 2; gaps.append("RSI")
 395      elif rsi > 80: p["rsi"] = 0
 396      elif rsi >= 70: p["rsi"] = 2
 397      elif rsi >= 50: p["rsi"] = 4
 398      elif rsi >= 40: p["rsi"] = 2
 399      else: p["rsi"] = 0
 400      trend = p["vs_50d"] + p["structure"] + p["near_high"] + p["rs_52w"] + p["rs_2m"] + p["rsi"]
 401  
 402      if rs5 is None:
 403          p["rs_5d"] = 4; gaps.append("5-day return")
 404      else:
 405          p["rs_5d"] = band(rs5, [(3, 8), (1, 6), (0, 4), (-2, 2)])
 406      if from_open is None or range_pos is None:
 407          p["session"] = 3; gaps.append("open, high or low")
 408      else:
 409          p["session"] = (3 if from_open > 0 else 0) + (3 if range_pos >= 0.5 else 0)
 410      if day_pct is None or vol_ratio is None:
 411          p["volume"] = 3; gaps.append("volume")
 412      elif day_pct > 0:
 413          p["volume"] = 6 if vol_ratio >= 1.3 else 4 if vol_ratio >= 0.8 else 2
 414      else:
 415          p["volume"] = 0 if vol_ratio >= 1.3 else 2
 416      short = p["rs_5d"] + p["session"] + p["volume"]
 417  
 418      cat, rev = num(s.get("catalyst_pts")), num(s.get("revisions_pts"))
 419      if cat is None:
 420          cat = 6; gaps.append("catalyst not rated")
 421      if rev is None:
 422          rev = 8; gaps.append("revisions not rated")
 423      cat, rev = max(0, min(20, cat)), max(0, min(20, rev))
 424      score = int(round(trend + short + cat + rev))
 425  
 426      if vs50 is not None and vs50 < 0: flags.append("below 50-day average")
 427      if ma50 is not None and ma200 is not None and ma50 < ma200: flags.append("downtrend: 50-day below 200-day")
 428      if vs50 is not None and vs50 > 15: flags.append("extended: more than 15% above 50-day")
 429      if rsi is not None and rsi > 75: flags.append("overbought: RSI above 75")
 430      if rsi is not None and rsi < 35: flags.append("oversold: RSI below 35")
 431      if day_pct is not None and vol_ratio is not None and day_pct < 0 and vol_ratio >= 1.3: flags.append("heavy-volume down day")
 432      if gap_pct is not None and from_open is not None and gap_pct > 1 and from_open < 0: flags.append("faded gap")
 433      if off_high is not None and off_high >= -0.5: flags.append("at 52-week high")
 434      if ind["cross"]: flags.append(ind["cross"])
 435      if rsi_from_history: gaps.append("RSI worked out from stored prices, not a published figure")
 436  
 437      conf = 50 + 0.35 * (score - 40)   # a score of 40 is treated as a coin flip; an unvalidated starting assumption
 438      if regime == "risk-off":
 439          conf -= 3
 440      conf = int(round(max(40, min(68, conf))))
 441      cap = int(max(5, min(20, round(30.0 / atr / 5.0) * 5))) if atr else None
 442      target = num(q.get("target"))
 443      return {
 444          "price": price, "day_chg": (price - prev) if (price is not None and prev is not None) else None,
 445          "day_pct": day_pct, "gap_pct": gap_pct, "from_open_pct": from_open, "five_day_pct": five, "month_pct": month,
 446          "score": score, "confidence_anchor": conf, "trend_pts": trend, "short_pts": short, "catalyst_pts": cat,
 447          "revisions_pts": rev, "parts": p, "vs_20d_pct": vs20, "vs_50d_pct": vs50, "vs_200d_pct": vs200,
 448          "off_high_pct": off_high, "rsi": rsi, "atr_pct": atr, "weight_cap_pct": cap, "rs_5d_pp": rs5, "rs_2m_pp": rs2m,
 449          "rs_52w_pp": rs52, "vol_ratio": vol_ratio, "range_pos": range_pos, "flags": flags, "data_gaps": gaps,
```

## Tier (strength band) (v7 lines 764-790)
```python
 764  def tier_of(score, flags):
 765      """Strength band tied to the decision rules: strong can be bought as a core position, weak should be replaced."""
 766      if score is None:
 767          return ""
 768      if score < 45 or any(f.startswith("downtrend") for f in flags):
 769          return "weak"
 770      if score >= 60 and not any(f.startswith("below 50-day") for f in flags):
 771          return "strong"
 772      return "middling"
 773  
 774  
 775  # ---------------------------------------------------------------- macro: yields and oil
 776  MACRO_SERIES = [("us2y", "US 2-year yield", "yield"), ("us10y", "US 10-year yield", "yield"),
 777                  ("us30y", "US 30-year yield", "yield"), ("uk10y", "UK 10-year gilt yield", "yield"),
 778                  ("de10y", "German 10-year yield", "yield"), ("fr10y", "French 10-year yield", "yield"),
 779                  ("it10y", "Italian 10-year yield", "yield"), ("jp10y", "Japanese 10-year yield", "yield"),
 780                  ("brent", "Brent crude, $ a barrel", "commodity"), ("wti", "WTI crude, $ a barrel", "commodity"),
 781                  ("natgas", "US natural gas, $", "commodity"), ("gold", "Gold, $ an ounce", "commodity"),
 782                  ("btc", "Bitcoin, $", "crypto"), ("eth", "Ether, $", "crypto"), ("sol", "Solana, $", "crypto"),
 783                  ("xrp", "XRP, $", "crypto")]
 784  CRYPTO_PROXY = {"btc": "IBIT", "eth": "ETHA"}       # US-listed spot funds: their closes line up with stock sessions
 785  CRYPTO_NAME = {"btc": "Bitcoin", "eth": "Ether"}
 786  CRYPTO_SERIES = ("btc", "eth", "sol", "xrp")
 787  MACRO_SPREADS = [("us10y", "us2y", "US 10-year minus 2-year"), ("uk10y", "us10y", "UK minus US 10-year"),
 788                   ("it10y", "de10y", "Italy minus Germany 10-year")]
 789  
 790  
```

## Confidence settlement: resolve_confidence (no timeout for stocks whose prices stop) (v7 lines 601-622)
```python
 601  def resolve_confidence(ledger, hist, bench):
 602      bser = series(hist, bench)
 603      bdates = [r["date"] for r in bser]
 604      n = 0
 605      for r in ledger:
 606          if r["table"] != "confidence" or r["beat"] not in (None, "") or not r["effective"]:
 607              continue
 608          ser = series(hist, r["ticker"])
 609          after = [x for x in ser if x["date"] >= r["effective"]]
 610          bafter = [x for x in bser if x["date"] >= r["effective"]]
 611          if len(bafter) >= 5 and not r["window_end"]:
 612              r["window_end"] = bafter[4]["date"]
 613          if len(after) < 5 or len(bafter) < 5:
 614              continue
 615          s_ret = pct(after[4]["close"], after[0]["open"])
 616          b_ret = pct(bafter[4]["close"], bafter[0]["open"])
 617          r["ret_pct"], r["spx_ret_pct"] = r2(s_ret), r2(b_ret)
 618          r["beat"] = "yes" if s_ret > b_ret else "no"
 619          r["window_end"] = bafter[4]["date"]
 620          n += 1
 621      return n
 622  
```

## Shadow settlement: resolve_shadow (close-to-close from the rating evening) (v7 lines 1181-1209)
```python
1181  def resolve_shadow(ledger, hist, bench):
1182      bser = series(hist, bench)
1183      bidx = {r["date"]: i for i, r in enumerate(bser)}
1184      n = 0
1185      for r in ledger:
1186          if r["table"] != "shadow" or r["beat"] is not None or r["date"] not in bidx:
1187              continue
1188          i = bidx[r["date"]]
1189          if i + 5 >= len(bser):
1190              continue
1191          end = bser[i + 5]["date"]
1192          ser = series(hist, r["ticker"])
1193          start = next((x for x in ser if x["date"] == r["date"]), None)
1194          upto = [x for x in ser if x["date"] <= end]
1195          if not start or not upto or ser[-1]["date"] < end or upto[-1]["date"] <= r["date"]:
1196              if i + 15 < len(bser):
1197                  r["beat"], r["window_end"] = "n/a", end        # no prices arrived for three weeks: leave it out of the count
1198              continue                                   # the stock's prices do not reach the end of the window yet
1199          s_ret, b_ret = pct(upto[-1]["close"], start["close"]), pct(bser[i + 5]["close"], bser[i]["close"])
1200          r["window_end"], r["ret_pct"], r["spx_ret_pct"] = end, r2(s_ret), r2(b_ret)
1201          r["beat"] = "yes" if s_ret > b_ret else "no"
1202          n += 1
1203      return n
1204  
1205  
1206  PART_NAMES = [("vs_50d", "distance from the 50-day average"), ("structure", "50-day and 200-day order"),
1207                ("near_high", "closeness to the 52-week high"), ("rs_52w", "one-year return against the index"),
1208                ("rs_2m", "two-month return against the index"), ("rsi", "RSI band"), ("rs_5d", "five-day return against the index")]
1209  
```

## Drift settlement v7: real_open, resolve_drift (v7 lines 1495-1539)
```python
1495  def real_open(row):
1496      """True when a stored row carries a traded open. Rows added by `closes` hold only a close (open = high = low =
1497      close, no volume), so their open cannot be used as a fill price."""
1498      if not row:
1499          return False
1500      return not (row.get("volume") is None and row["open"] == row["close"] == row["high"] == row["low"])
1501  
1502  
1503  def resolve_drift(ledger, hist, bench):
1504      """The tradable result: bought at the open of the session after the reaction day (the first fill an order can get)
1505      and valued at the close five sessions after the reaction day, against the index over the same span (ret_pct,
1506      spx_ret_pct, beat). The version 6 figure, from the reaction day's close, is kept beside it (cum_pct, spx_cum_pct).
1507      If the next session's open never arrives, the row settles on the close basis after 15 sessions and says so (unit)."""
1508      bser = series(hist, bench)
1509      bidx = {r["date"]: i for i, r in enumerate(bser)}
1510      n = 0
1511      for r in ledger:
1512          if r["table"] != "drift" or r["beat"] is not None or r["date"] not in bidx:
1513              continue
1514          i = bidx[r["date"]]
1515          if i + 5 >= len(bser):
1516              continue
1517          end = bser[i + 5]["date"]
1518          ser = series(hist, r["ticker"])
1519          start = next((x for x in ser if x["date"] == r["date"]), None)
1520          fin = next((x for x in ser if x["date"] == end), None)
1521          nxt = next((x for x in ser if x["date"] == bser[i + 1]["date"]), None)
1522          if not start or not fin:
1523              if i + 15 < len(bser):
1524                  r["beat"], r["window_end"] = "n/a", end
1525              continue
1526          c_ret, cb_ret = pct(fin["close"], start["close"]), pct(bser[i + 5]["close"], bser[i]["close"])
1527          if real_open(nxt):
1528              s_ret, b_ret = pct(fin["close"], nxt["open"]), pct(bser[i + 5]["close"], bser[i + 1]["open"])
1529              basis = "from the next open"
1530          elif i + 15 < len(bser):
1531              s_ret, b_ret, basis = c_ret, cb_ret, "from the reaction close (next open never supplied)"
1532          else:
1533              continue                                    # wait for the next session's full row
1534          r["window_end"], r["ret_pct"], r["spx_ret_pct"] = end, r2(s_ret), r2(b_ret)
1535          r["cum_pct"], r["spx_cum_pct"], r["unit"] = r2(c_ret), r2(cb_ret), basis
1536          r["beat"] = "yes" if s_ret > b_ret else "no"
1537          n += 1
1538      return n
1539  
```

## Standstill v7: standstill_rows (week test skips the first session of each ISO week) (v7 lines 1603-1673)
```python
1603  def standstill_rows(ledger, hist, bench, date, horizon=5):
1604      """Two tests of whether changing the order paid, both from stored prices and the game's fill rules.
1605      change: for each effective date E, the new order and the order before it, each held fixed from E for up to
1606              `horizon` sessions (the new one filling at E's open); the gap is what the decision added.
1607      week:   for each week, the actual estimate against the order in force after the week's first session held fixed."""
1608      meta = {r["name"]: r for r in ledger if r["table"] == "meta"}
1609      start = (meta.get("start_date") or {}).get("text") or "0000-00-00"
1610      dates = [r["date"] for r in series(hist, bench) if start <= r["date"] <= date]
1611      tick_of = _tick_map(ledger)
1612      fills = {(r["name"], r["effective"]): num(r["value"]) for r in ledger if r["table"] == "position" and num(r["value"])}
1613      rows = []
1614      effs = sorted({r["effective"] for r in ledger if r["table"] == "trade" and r["effective"] in dates})
1615      for e in effs:
1616          i = dates.index(e)
1617          if i == 0:
1618              continue                                    # the first order replaced cash: nothing to compare
1619          dprev = dates[i - 1]
1620          w_old, w_new = _weights(ledger, dprev), _weights(ledger, e)
1621          if not w_old:
1622              continue
1623          span = dates[i:i + horizon]
1624          v_new = v_old = 1.0
1625          miss = set()
1626          prev_d = dprev
1627          for k, d in enumerate(span):
1628              a, m1 = port_day(w_old if k == 0 else w_new, w_new, d, prev_d, hist, tick_of, fills)
1629              b, m2 = port_day(w_old, w_old, d, prev_d, hist, tick_of, fills)
1630              miss |= m1 | m2
1631              v_new *= 1 + a / 100.0
1632              v_old *= 1 + b / 100.0
1633              prev_d = d
1634          eff_pts = (v_new - v_old) * 100.0
1635          changes = sorted(n for n in set(w_old) | set(w_new) if abs(w_old.get(n, 0) - w_new.get(n, 0)) > 1e-9)
1636          what = ", ".join(f"{n} {w_old.get(n, 0):g} to {w_new.get(n, 0):g}" for n in changes)
1637          rows.append(lrow("standstill", date=e, effective=e, kind="change", days=len(span),
1638                           ret_pct=None if miss else r2((v_new - 1) * 100.0, 3), spx_ret_pct=None if miss else r2((v_old - 1) * 100.0, 3),
1639                           value=None if miss else r2(eff_pts, 3),
1640                           confirmed="incomplete" if miss else ("complete" if len(span) == horizon else "running"),
1641                           window_end=span[-1], name=f"Change for {e}",
1642                           text=what + (f". Missing prices: {', '.join(sorted(miss))}" if miss else "")))
1643      perf = {r["date"]: num(r["day_pct"]) for r in ledger if r["table"] == "perf" and r["day_pct"] is not None}
1644      weeks = {}
1645      for d in dates:
1646          y, wk, _ = __import__("datetime").date.fromisoformat(d).isocalendar()
1647          weeks.setdefault((y, wk), []).append(d)
1648      for key in sorted(weeks):
1649          ds = weeks[key]
1650          if len(ds) < 2:
1651              continue
1652          w0 = _weights(ledger, ds[0])
1653          v_act = v_st = 1.0
1654          miss = set()
1655          prev_d = ds[0]
1656          for d in ds[1:]:
1657              if d not in perf:
1658                  miss.add("estimate for " + d)
1659                  continue
1660              v_act *= 1 + perf[d] / 100.0
1661              b, m = port_day(w0, w0, d, prev_d, hist, tick_of, fills)
1662              miss |= m
1663              v_st *= 1 + b / 100.0
1664              prev_d = d
1665          n_changes = len([e for e in effs if ds[0] < e <= ds[-1]])
1666          rows.append(lrow("standstill", date=ds[0], kind="week", days=len(ds) - 1, window_end=ds[-1],
1667                           ret_pct=None if miss else r2((v_act - 1) * 100.0, 3), spx_ret_pct=None if miss else r2((v_st - 1) * 100.0, 3),
1668                           value=None if miss else r2((v_act - v_st) * 100.0, 3), name=f"Week from {ds[0]}",
1669                           confirmed="incomplete" if miss else "complete",
1670                           text=f"{n_changes} change(s) after the first session; standstill = the order in force at the close of {ds[0]}"
1671                                + (f". Missing prices: {', '.join(sorted(miss))}" if miss else "")))
1672      return rows
1673  
```

## Results total v7 (v7 lines 1700-1716)
```python
1700  def results_total(ledger, weights, date, default_move=6.0):
1701      """Holdings reporting inside the next 5 and 10 sessions: weight x implied move added up (a missing implied move
1702      counts at default_move). Returns {5: (points, reports, missing), 10: (...)}."""
1703      out = {}
1704      for n in (5, 10):
1705          ahead = set(_sessions_ahead(date, n))
1706          pts, k, missing = 0.0, 0, []
1707          for e in ledger:
1708              if e["table"] == "event" and e["kind"] == "results" and e["stock"] in weights and (e["date"] or "") in ahead and weights[e["stock"]] > 0:
1709                  mv = num(e["implied_pct"])
1710                  if mv is None:
1711                      missing.append(e["stock"])
1712                      mv = default_move
1713                  pts += weights[e["stock"]] * mv / 100.0
1714                  k += 1
1715          out[n] = (pts, k, missing)
1716      return out
```

## Reconcile v7 (v7 lines 1730-1745)
```python
1730  def reconcile(ledger):
1731      """Sets value_est on every `reported` row to the estimate at the close of the last session on or before its date,
1732      and returns (row, estimate, gap, read_before_close) for each."""
1733      perf = sorted((r for r in ledger if r["table"] == "perf" and r["value_est"] is not None), key=lambda r: r["date"])
1734      out = []
1735      for r in sorted((r for r in ledger if r["table"] == "reported"), key=lambda r: (r["date"] or "", r["time_uk"] or "")):
1736          p = [x for x in perf if x["date"] <= (r["date"] or "")]
1737          if not p or r["value_reported"] is None:
1738              continue
1739          est = p[-1]["value_est"]
1740          r["value_est"] = est
1741          t = (r["time_uk"] or "").strip()
1742          early = p[-1]["date"] == r["date"] and len(t) == 5 and t[2] == ":" and t < us_close_uk(r["date"])
1743          out.append((r, est, num(r["value_reported"]) - est, early))
1744      return out
1745  
```

## Panel test: price_parts and panel_obs (v7 lines 1211-1233)
```python
1211  def price_parts(c, b):
1212      """The part of the score that needs only closing prices (48 of the 100 points), split into its seven parts, for a
1213      stock's closes c and the benchmark's closes b over the same dates, both ending on the day being scored. The bands
1214      are the ones score_stock uses."""
1215      price, ma50, ma200 = c[-1], sma(c, 50), sma(c, 200)
1216      vs50 = pct(price, ma50)
1217      p = {}
1218      p["vs_50d"] = 0 if vs50 < -5 else 3 if vs50 < 0 else 8 if vs50 < 2 else 12 if vs50 <= 15 else 8 if vs50 <= 25 else 4
1219      p["structure"] = (5 if ma50 > ma200 else 0) + (3 if price > ma200 else 0)
1220      p["near_high"] = band(pct(price, max(c[-252:])), [(-3, 10), (-8, 7), (-15, 4), (-25, 2)])
1221      span = min(251, len(c) - 1)
1222      p["rs_52w"] = band(pct(c[-1], c[-1 - span]) - pct(b[-1], b[-1 - span]), [(30, 4), (10, 3), (0, 1)])
1223      p["rs_2m"] = band(pct(c[-1], c[-43]) - pct(b[-1], b[-43]), [(5, 2), (0, 1)])
1224      rsi = rsi_wilder(c)
1225      p["rsi"] = 0 if rsi > 80 else 2 if rsi >= 70 else 4 if rsi >= 50 else 2 if rsi >= 40 else 0
1226      p["rs_5d"] = band(pct(c[-1], c[-6]) - pct(b[-1], b[-6]), [(3, 8), (1, 6), (0, 4), (-2, 2)])
1227      return p
1228  
1229  
1230  def price_points(c, b):
1231      return sum(price_parts(c, b).values())
1232  
1233  
```

## Panel test: panel_obs (v7 lines 1293-1322)
```python
1293  def panel_obs(panel, hist, bench):
1294      """One observation per panel stock per signal date: the price-only points and their parts on that date, and the
1295      stock's return minus the index's over the next five sessions (and, as a check, over five sessions starting a day
1296      later, which leaves out the first night's gap that an order filling at the next open cannot catch). Signal dates
1297      are every fifth benchmark session counted from the date the panel was fixed, so no two windows of one stock overlap."""
1298      bser = series(hist, bench)
1299      bd = [r["date"] for r in bser]
1300      bc = [r["close"] for r in bser]
1301      frozen = panel.get("frozen") or "9999-12-31"
1302      anchor = next((i for i, d in enumerate(bd) if d >= frozen), len(bd))
1303      sigs = [i for i in range(len(bd)) if (i - anchor) % PANEL_STEP == 0]
1304      obs = []
1305      for t, closes in panel_series(panel, hist).items():
1306          idx = [i for i, d in enumerate(bd) if d in closes]           # benchmark sessions this stock has a close for
1307          if len(idx) < PANEL_MIN_CLOSES:
1308              continue
1309          pos = {i: k for k, i in enumerate(idx)}
1310          c = [closes[bd[i]] for i in idx]
1311          b = [bc[i] for i in idx]
1312          for i in sigs:
1313              k = pos.get(i)
1314              if k is None or k + 1 < PANEL_MIN_CLOSES or k + 5 >= len(idx) or idx[k + 5] != i + 5:
1315                  continue                                              # not enough history, or the window is not complete
1316              parts = price_parts(c[:k + 1], b[:k + 1])
1317              ex = pct(c[k + 5], c[k]) - pct(b[k + 5], b[k])
1318              ex_late = (pct(c[k + 6], c[k + 1]) - pct(b[k + 6], b[k + 1])) if (k + 6 < len(idx) and idx[k + 6] == i + 6) else None
1319              obs.append({"date": bd[i], "ticker": t, "pts": sum(parts.values()), "parts": parts, "ex": ex, "ex_late": ex_late,
1320                          "live": bd[i] >= frozen})
1321      return obs
1322  
```

## Risk tables (40 common sessions) (v7 lines 659-690)
```python
 659  def risk_tables(order, stocks_by_name, hist, scenarios, links=None):
 660      held = [(o["name"], num(o["weight"]) or 0.0) for o in order if (num(o.get("weight")) or 0) > 0]
 661      rets = {}
 662      for name, _ in held:
 663          tick = stocks_by_name[name]["ticker"]
 664          rets[name] = daily_returns(series(hist, tick))
 665      dates = None
 666      for name in rets:
 667          ds = set(rets[name])
 668          dates = ds if dates is None else dates & ds
 669      dates = sorted(dates or [])[-40:]
 670      rows, corr_rows = [], []
 671      port_vol = None
 672      if len(dates) >= 15:
 673          m = {n: [rets[n][d] * 100.0 for d in dates] for n, _ in held}
 674          mean = {n: sum(v) / len(v) for n, v in m.items()}
 675          def cov(a, b):
 676              return sum((x - mean[a]) * (y - mean[b]) for x, y in zip(m[a], m[b])) / (len(dates) - 1)
 677          names = [n for n, _ in held]
 678          w = dict(held)
 679          c = {(a, b): cov(a, b) for a in names for b in names}
 680          var = sum(w[a] / 100 * w[b] / 100 * c[(a, b)] for a in names for b in names)
 681          port_vol = math.sqrt(var) if var > 0 else 0.0
 682          for a in names:
 683              marg = sum(w[b] / 100 * c[(a, b)] for b in names)
 684              share = (w[a] / 100 * marg / var * 100.0) if var > 0 else None
 685              rows.append(lrow("risk", name=a, weight=w[a], theme=stocks_by_name[a].get("theme"),
 686                               vol_pct=r2(math.sqrt(c[(a, a)])), risk_share_pct=r2(share, 1)))
 687          for i, a in enumerate(names):
 688              for b in names[i + 1:]:
 689                  den = math.sqrt(c[(a, a)] * c[(b, b)])
 690                  if den > 0:
```

## History merge (fills a missing open with the close: placeholder bars) (v7 lines 215-240)
```python
 215  def merge_history(hist, ticker, rows):
 216      """hist: dict (ticker, date) -> row. New rows replace old ones for the same day.
 217      Returns the dates whose row is new or whose stored open or close changed by more than 0.01%."""
 218      changed = []
 219      for r in rows or []:
 220          d = str(r.get("date") or "")[:10]
 221          o, h, l, c = num(r.get("open")), num(r.get("high")), num(r.get("low")), num(r.get("close"))
 222          v = num(r.get("volume"))
 223          if len(d) != 10 or c is None or c <= 0:
 224              warn(f"{ticker} {d}: row skipped (no date or close)")
 225              continue
 226          if o is None:
 227              o = c
 228          if h is None:
 229              h = max(o, c)
 230          if l is None:
 231              l = min(o, c)
 232          if h < l or not (l * 0.995 <= c <= h * 1.005) or not (l * 0.995 <= o <= h * 1.005):
 233              warn(f"{ticker} {d}: row skipped (open/high/low/close inconsistent: {o}, {h}, {l}, {c})")
 234              continue
 235          old = hist.get((ticker, d))
 236          if old is None or abs(old["close"] / c - 1) > 1e-4 or abs(old["open"] / o - 1) > 1e-4:
 237              changed.append(d)             # new for that day, or corrected
 238          hist[(ticker, d)] = {"ticker": ticker, "date": d, "open": o, "high": h, "low": l, "close": c, "volume": v}
 239      return changed
 240  
```

## Recalculation after a price correction (v7 lines 1912-1924)
```python
1912      ever_held = {r["ticker"] for r in ledger if r["table"] == "position"} | {bench}
1913      revised = {d_: [t_ for t_ in ts_ if t_ in ever_held] for d_, ts_ in revised.items()}
1914      revised = {d_: ts_ for d_, ts_ in revised.items() if ts_}
1915      stale = sorted(d_ for d_ in revised if d_ in done_perf)
1916      if stale:                       # a stored price was corrected after that session was logged: redo from there
1917          cut = stale[0]
1918          for r in ledger:
1919              if r["table"] == "postmortem" and r["date"] and r["date"] >= cut:
1920                  kept_notes[r["name"]] = {"name": r["name"], "text": r["text"], "lesson": r["lesson"]}
1921              if r["table"] == "confidence" and r["window_end"] and r["window_end"] >= cut:
1922                  r["window_end"] = r["beat"] = r["ret_pct"] = r["spx_ret_pct"] = None
1923          ledger = [r for r in ledger if not (r["table"] in ("perf", "contrib", "postmortem") and r["date"] and r["date"] >= cut)]
1924          print(f"RECALCULATED from {cut}: prices arrived late or were corrected for " + ", ".join(f"{d_} ({', '.join(sorted(set(t_)))})" for d_, t_ in sorted(revised.items()) if d_ in done_perf))
```

## v6 resolve_drift (repo commit 9bd42e3, lines 1476-1499)
```python
1476  def resolve_drift(ledger, hist, bench):
1477      """Five sessions from the close of the reaction day, against the index over the same sessions."""
1478      bser = series(hist, bench)
1479      bidx = {r["date"]: i for i, r in enumerate(bser)}
1480      n = 0
1481      for r in ledger:
1482          if r["table"] != "drift" or r["beat"] is not None or r["date"] not in bidx:
1483              continue
1484          i = bidx[r["date"]]
1485          if i + 5 >= len(bser):
1486              continue
1487          end = bser[i + 5]["date"]
1488          ser = series(hist, r["ticker"])
1489          start = next((x for x in ser if x["date"] == r["date"]), None)
1490          fin = next((x for x in ser if x["date"] == end), None)
1491          if not start or not fin:
1492              if i + 15 < len(bser):
1493                  r["beat"], r["window_end"] = "n/a", end
1494              continue
1495          s_ret, b_ret = pct(fin["close"], start["close"]), pct(bser[i + 5]["close"], bser[i]["close"])
1496          r["window_end"], r["ret_pct"], r["spx_ret_pct"] = end, r2(s_ret), r2(b_ret)
1497          r["beat"] = "yes" if s_ret > b_ret else "no"
1498          n += 1
1499      return n
```
