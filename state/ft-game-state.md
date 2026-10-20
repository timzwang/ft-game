# FT Stock Picking Game: state and log

Last updated: Tue 20 Oct 2026, about 22:05 UK (evening review, a quiet evening: no change for Wed 21 Oct; day +0.62% against SPY +0.34%, Eli Lilly +0.52 points at a record; Hasbro passed all six drift tests and joined the watchlist, not bought; WebFetch refused every page address it had not first seen in a search result, so pages were reached through searches and several watchlist rows are missing). Before that, Mon 19 Oct about 22:25 UK (hand-run session with Tim: playbook 6.11.1, the 26 Oct 07:15 UK cut-off test removed; pipeline 7.6 prepared for review, not deployed, 7.4 stays live). Before that, about 22:15 UK (evening review, quiet; AbbVie's results event added; implied moves stored for five holdings). Earlier entries: see the review log (section 6).

This doc is the narrative record for Tim's entry, "Seeking Beta". The procedure for every run is in `claude/ft-game-playbook.md` (the core doc) and the docs its routing table names. The numbers (prices, scores, daily performance, contributions, ratings and their outcomes, the full calendar, analyst changes, alerts, the panel test, the drift record) live in the data files behind Tim's page and the panel file, and are produced by the pipeline script; this doc carries the decisions and the reasons.

Messages: from 10 Oct Tim is sent a message only when there is something for him to enter or answer (playbook part I, "When Tim is told"). Quiet runs update the page and this doc and send nothing.

Scheduled runs: evening review 21:30 UK Sun to Thu; morning check 06:36 UK Mon to Fri; price refresh 16:45 UK and late price refresh 19:22 UK Mon to Fri; results-day refresh 14:50 UK Mon to Fri (acts only on results days); weekly performance review Sat 09:12 UK; weekend news check Sat and Sun 20:20 UK; midday check 12:40 UK Mon to Fri (switched off, see section 8).

**Cut-off: until the FT confirms it, every order must be entered before 07:00 UK (playbook part C, from 17 Oct).**

## 1. Status

- **Playbook version 6.11.1** (6.11.1, 19 Oct late evening: the 26 Oct cut-off test removed at Tim's request; 6.11, 19 Oct evening: pipeline 7.4, `order_expected` with every change of order, and the repository's data check; 6.10, 19 Oct: pipeline 7.3 and a results budget of 1.0 points for reports dated 27 to 30 Oct; 6.9, 18 Oct: evening and weekly review tasks recreated with the repository attached; 6.8: G6 and G7 step 1; 6.7: pipeline 7.2, stricter price handling; 6.6: the handoff log; 6.5: the standstill test corrected; 6.4: after the outside audit, pipeline 7, 07:00 UK cut-off, score frozen; 6.3: the broad scan; 6.2: the day call never moves cash, "overbought" is a warning only; 6: split docs, panel test, earnings-drift scan). **Pipeline script version 7.4** (part B holds the asset id and hash).
- **Estimated value at Tue 20 Oct close: 101,725, +1.73% since the start, against -0.93% for the S&P 500 fund (gap +2.65 points).** Tue 20 Oct +0.62% against SPY +0.34%: Eli Lilly +0.52 points (+3.5% to a record), AbbVie +0.23, Chevron +0.06, Coca-Cola +0.02; Shell -0.12, Microsoft -0.05, Exxon -0.03. Health care made a record; energy was the weakest sector. Mon 19 Oct: 101,097.
- **Last FT figures: Fri 16 Oct after the close, 101,402 (+1.40%), rank 3,269 of 13,918 (top 23.5%).** RECONCILE -34 credits (-0.03%). Top 2% line about +6.5% (Tim's screenshots of 18 Oct; stored as `top2_return_pct` 6.5); gap to the line now roughly 4.8 points on the estimate.
- **Standstill (20 Oct run):** change for 13 Oct +0.61 (complete); 14 Oct -0.48 (complete); 15 Oct +0.63 (four sessions); 16 Oct -0.07 (three); 19 Oct -0.02 (two). Week of 12 Oct +0.12; week of 19 Oct -0.02 so far. Inception priced to 19 Oct only (RTX's 20 Oct row missing): -0.30 as entered, -0.77 fully invested. No evidence either way.
- **Panel test (unchanged):** history verdict "no evidence": average rank correlation +0.042 (t +1.1) over 49 dates; top third minus bottom third +0.25 points (t +0.4). Live: no complete window yet. 24 members behind (15 Oct); MRSH and HPE swap at the weekly review of 24 Oct. The score is frozen for the rest of the game.
- **Order in force (filled Mon 19 Oct's open; unchanged for Wed 21 Oct):** Coca-Cola 20, Exxon Mobil 15, Shell 15, Microsoft 15, Eli Lilly 15, Chevron 10, AbbVie 10, cash 0.
- Day call for Wed 21 Oct: S&P 500 green 55% (usual 55%); portfolio green 55% (usual 56%); no adjustment: close to a coin flip. Record (S&P 500): 3 right of 6. Tue 20 Oct: both green calls right (S&P 500 +0.34%, portfolio +0.62%).
- Macro at Tue 20 Oct: US yields carried from 19 Oct (2-year 4.77%, 10-year 5.15%, 30-year 5.48%: the Treasury had not published 20 Oct's row when the run read it; tradingeconomics showed the 10-year near 5.11% live). Gilt 5.42%, German 3.42%, French 4.92%, Italian 4.54%, Japanese 2.90%. Brent $108.91 (-0.3%; +2.2% over five; touched about $111, a five-month high, then fell on an unconfirmed Qatar and Pakistan framework for US-Iran talks), WTI $98.07 (the -5.6% day figure reflects the November contract's expiry, not a crash), gold $4,122. Backdrop label: neutral.
- Crypto: no Coinbase rows tonight (addresses not reachable); Bitcoin carried at $81,772 (19 Oct). Trend up (IBIT 1.0% below its 20-day, 4.9% above its 50-day). Ether mixed, -5.0% over five sessions through ETHA (19 Oct). Reports put Bitcoin near $83,000 on 20 Oct (not stored). No holding is crypto-linked.
- Regime: mixed. Tue 20 Oct: S&P 500 about +0.2% to +0.3% (SPY +0.34%), Dow about +1%, Nasdaq flat, Russell 2000 about +1.7%; rotation from tech into value, health care at a record, financials +1.2%, energy weakest. Advancers about 2.5 to 1 on the NYSE. Housing starts 1.221M against 1.30M forecast (-5.2%, a four-month low). Netflix fell about 4% after hours on a weaker advertising outlook. What would make it risk-off: the 10-year back above 5.25% with the S&P 500 below its 20-day, or a hike on 28 Oct priced above 70%.

## 2. Current portfolio

The order in force (filled Mon 19 Oct's open, unchanged for Wed 21 Oct). Scores and bands from the pipeline at the Tue 20 Oct close; confidence ratings as given on 18 Oct.

| Stock | Weight | Cap | Confidence (18 Oct, not calibrated) | Score | Band | Flags | Next results | Substitute if missing |
|---|---|---|---|---|---|---|---|---|
| Coca-Cola | 20% | 20% | 59 | 74 | Strong | none | 27 Oct, before US open (implied 4.2%) | PepsiCo (downtrend: cash instead) |
| Exxon Mobil | 15% | 15% | 60 | 84 | Strong | none; three target raises in a week | 30 Oct, before US open (implied n/a, 6% used) | ConocoPhillips |
| Shell | 15% | 15% | 59 | 70 | Strong | none | 29 Oct, 07:00 UK (implied n/a, 6% used) | BP |
| Microsoft | 15% | 15% | 57 | 66 | Strong | none; BMO target $600 from $515 (20 Oct) | 28 Oct, after US close (implied 6.0%) | Alphabet (not scored) |
| Eli Lilly | 15% | 15% | 59 | 79 | Strong | record high 20 Oct; Goldman $1,413, BofA $1,397 | 29 Oct, before US open (implied 7.9%: above budget at 15%) | Merck |
| Chevron | 10% | 15% | 59 | 75 | Strong | none | 30 Oct, before US open (implied 5.8%) | ConocoPhillips |
| AbbVie | 10% | 15% | 60 | 82 | Strong | none | 30 Oct, before US open, confirmed (implied 6.4%) | Amgen |
| Cash | 0% | | | | | | | |

Ratings were moved down from the anchors (60 to 65) by up to 5 points each: the panel test finds no evidence that a high score is an edge, so ratings stay near 55 to 60.

Points for the coming reviews:

- Themes: Energy 40%, Health care 25%, Consumer staples 20%, Software 15%. Risk shares: Exxon 21.6%, Coca-Cola 20.1%, Shell 16.9%, Chevron 13.8%, Eli Lilly 13.2%, AbbVie 12.1%, Microsoft 2.3% (oil names 52%). Worst scenario: ceasefire or Hormuz reopening -1.78%. Tuesday's peace report is a live version of that scenario: watch whether Qatar or either government confirms it.
- **Results cluster:** weight times implied move against the 1.0 budget for 27 to 30 Oct: Coca-Cola 0.84, Microsoft 0.90, Shell 0.90 (6% used), **Eli Lilly 1.19 (above budget)**, Exxon 0.90 (6% used), Chevron 0.58, AbbVie 0.64. RESULTS TOTAL next 10 sessions 5.95 points across seven reports, deliberate (the entry needs variance), but all in one week with oil names 2.4 points of it. Implied moves are earnings-watcher's of 16 Oct, not refreshed tonight. **Eli Lilly: trim to 12% or less in the order before 07:00 UK Wed 28 Oct unless its implied move falls below about 6.7%**; decide by the Sunday 25 Oct review. Last orders: Coca-Cola before 07:00 UK Mon 26 Oct; Shell, Eli Lilly and Microsoft before 07:00 UK Wed 28 Oct; Exxon, Chevron and AbbVie before 07:00 UK Thu 29 Oct.
- **Hasbro (drift ENTER, 20 Oct):** all six tests passed (EPS $2.90 against $1.86, revenue $1.59bn against $1.48bn, 2026 outlook raised; +11.2% on 3.5 times average volume, closed near the high, above a rising 50-day). Limit 5% (18% above its 50-day, RSI 83). Not bought tonight: expected benefit about +0.05 to +0.08 points, and funding it meant cutting Lilly at a record a week before its planned trim or Coca-Cola before its report. If Wed 21 Oct closes above its open in the upper half of its range, the Wednesday review may add it at 5%, funded from the Lilly trim. Exit rules from part E apply from any fill.
- Keep TSMC on the list until Fri 23 Oct and Palantir until Mon 26 Oct (standstill test), then they may be removed. Walmart is a ROTATE OUT candidate (downtrend flag) from Wed 21 Oct, its third session on the list.
- Walmart's statistics page now fetched (50-day 109.15, 200-day 118.33): its 200-day is below; score 60, band weak.
- Shadow ratings still open for stocks off the list: Constellation Energy, CrowdStrike, Lumentum, Marvell (the weekly review gives their rows).

## 3. Pending order

**No change for Wed 21 Oct (20 Oct evening review, quiet; nothing sent).** Last change: for Mon 19 Oct's open, message sent about 21:47 UK on Sun 18 Oct; entered, confirmed by Tim about 22:00 UK; filled 19 Oct.

Coca-Cola 20, Exxon Mobil 15, Shell 15, Microsoft 15, Eli Lilly 15, Chevron 10, AbbVie 10, cash 0.

Changes at the last change: sell Palantir 5 (momentum exit); Chevron 15 to 10 (oil concentration); add AbbVie 10.

## 4. Watchlist

Scores and bands at the Tue 20 Oct close. 19 names. Added Hasbro (drift ENTER). No removals. Rows missing tonight (scores use 19 Oct prices): Marathon Petroleum, Humana, Valero, Phillips 66 (their pages served 19 Oct copies).

| Name | Band | Status | Score | Flags | Next results | Promote if |
|---|---|---|---|---|---|---|
| Visa | Strong | Watching | 80 | overbought; at 52-week high | 27 Oct, after US close (est.) | Steady name if a holding weakens; not held through results above 10% |
| ConocoPhillips | Strong | Watching | 78 | faded gap | 5 Nov (est.) | Swap for Exxon or Chevron before their 30 Oct results if a report needs dodging |
| Phillips 66 | Strong | Watching | 77 | none (19 Oct prices) | 28 Oct, before US open | Only in place of an oil major |
| Mastercard | Strong | Watching | 77 | overbought | 29 Oct (est.) | Alternative to Visa, not both |
| Hasbro | Strong | Drift: day 1 (added 20 Oct) | 75 | extended; overbought; at 52-week high | Feb 2027 (est.) | 5% after a second session closing above its open in the upper half of its range |
| Valero Energy | Strong | Results ahead | 73 | EMAs mixed (19 Oct prices) | 22 Oct (time est.) | Not before results; drift tests after |
| Marathon Petroleum | Strong | Watching | 72 | extended (19 Oct prices) | 3 Nov | 5% at most while extended |
| Humana | Strong | Ready | 71 | none (19 Oct prices) | 6 Nov | 5% (cap) if a holding weakens |
| UnitedHealth | Strong | Ready | 69 | EMAs mixed | Jan 2027 (est.) | Up to 10% if a holding weakens |
| Amgen | Strong | Watching | 68 | none | 3 Nov, after US close | Steady name (cap 15%) |
| Merck | Strong | Watching | 66 | none | 29 Oct | Substitute for Lilly; back near its high |
| BP | Strong | Watching | 65 | none | 30 Oct (est.) | Substitute for Shell |
| Palantir | Middling | Watching (sold 19 Oct) | 59 | EMAs mixed | 2 Nov | Keep until 26 Oct (standstill test) |
| Meta Platforms | Middling | Results ahead | 53 | golden cross 6 Oct | 21 Oct, after US close | Drift tests on 22 Oct's session; not held through the report |
| Strategy (crypto tracker) | Middling | Watching | 52 | golden cross 19 Oct; moves with Bitcoin | 29 Oct (est.) | Kept whatever it scores |
| TSMC | Middling | Watching | 50 | below 50-day | Jan 2027 | Keep until Fri 23 Oct (left the order 16 Oct), then remove |
| Procter & Gamble | Weak | Results ahead | 64 | downtrend | 22 Oct (est.) | Not while in a downtrend |
| Walmart | Weak | Watching | 60 | downtrend; faded gap | 19 Nov | ROTATE OUT from 21 Oct unless the trend repairs |
| Coinbase (crypto tracker) | Weak | Watching | 35 | downtrend; below 50-day | 29 Oct, after US close | Kept whatever it scores |

Intake tonight: one addition (Hasbro), fewer than five, because only stock pages that had appeared in a search result could be fetched. Candidates from the 20 Oct broad scan not yet checked: Cardinal Health, Centene (its quote pages could not be reached tonight), Charles River Laboratories, Biogen, Viatris, Targa Resources, Ross Stores, Standard Life, Tate & Lyle. Equifax (drift FAIL: guidance lowered, 50-day below 200-day) not added.

## 5. Trade log

| Date entered | Effective (open of) | Order / change | Reason |
|---|---|---|---|
| Thu 8 Oct, about 23:55 | Fri 9 Oct | Account created with the game's "choose for me" button: Mobimo Holding 20, PACCAR 20, Monolithic Power Systems 20, Sunrise Communications 20, Monks Investment Trust 20 | Not a decision. Needed only to open the account |
| Fri 9 Oct, about 00:00 | Fri 9 Oct | First chosen order: Exxon Mobil 15, Chevron 15, Shell 10, RTX 10, Lockheed Martin 5, TSMC 10, Nvidia 10; cash 25 | Energy and defence led on 8 Oct; AI as a counterweight |
| Sun 11 Oct (entered, confirmed 12 Oct) | Mon 12 Oct | Sell RTX and Lockheed; add Microsoft 15, Coca-Cola 15, Palantir 5, Goldman Sachs 5; cash 25 to 0 | Trend filter; fully invested at Tim's request |
| Mon 12 Oct, 18:21 UK (confirmed) | Tue 13 Oct | Sell Nvidia 10; Shell 10 to 15; Coca-Cola 15 to 20 | Nvidia faded from its open four sessions running |
| Tue 13 Oct, 21:52 UK (confirmed 22:29 UK) | Wed 14 Oct | Sell Goldman Sachs 5; add Meta Platforms 5 | Goldman faded after its beat; Meta passed the momentum test |
| Wed 14 Oct, about 21:44 UK (confirmed 15 Oct 22:00 UK) | Thu 15 Oct | Sell Meta 5; Microsoft 15 to 10; add Eli Lilly 10 | Meta's momentum exit; tech trimmed after the hot CPI; Lilly score 77, small range |
| Thu 15 Oct, about 21:51 UK (correction message; confirmed 22:00 UK) | Fri 16 Oct | Sell TSMC 10; Microsoft 10 to 15; Eli Lilly 10 to 15 | TSMC score 43 after results; the two top scores with small ranges back to their caps |
| Sun 18 Oct, about 21:47 UK (entered, confirmed by Tim about 22:00 UK) | Mon 19 Oct | Sell Palantir 5; Chevron 15 to 10; add AbbVie 10 | Palantir's heavy-volume exit signal; oil names carried 64% of risk with Exxon and Chevron correlated 0.94; AbbVie score 82 with six target raises |

## 6. Review log (newest first, keep the latest 15)

- Tue 20 Oct 2026 (about 22:05): Evening review, quiet: no change for Wed 21 Oct. Day +0.62% against SPY +0.34% (Lilly +0.52 points at a record; health care led, energy lagged). Drift scan: Hasbro ENTER (not bought: expected benefit about +0.05 to +0.08 points, extended; watchlist "Drift: day 1"), Equifax FAIL. Meta's 13 Oct rating (57) settled: lagged. WebFetch refused every address that had not first appeared in a search result (permission requests withdrawn), so pages were found by searches without clock suffixes; holdings all priced from "At close" pages; MPC, HUM, VLO, PSX, SHEL-US, BP-US, OIL (BNO), ETHA, RTX rows and the Coinbase coin rows missing; US yields carried (Treasury row not yet out). Broad scan requested and read (20 Oct). Files published.
- Mon 19 Oct 2026 (about 22:25): Hand-run session with Tim. The Mon 26 Oct 07:15 UK cut-off test removed (playbook 6.11.1, part C). ChatGPT's review of pipeline 7.5 (PR #5) checked; pipeline 7.6 prepared on a branch, not deployed; 7.4 stays live.
- Mon 19 Oct 2026 (about 22:15): Evening review, quiet: no change for Tue 20 Oct. Day -0.33% against SPY +0.42%. AbbVie results event added; implied moves stored for five holdings. stockanalysis.com refused 8 pages; rows from Cboe's delayed quotes. Files published.
- Mon 19 Oct 2026 (about 20:40): Hand-run session with Tim after ChatGPT's follow-up review (PR #3): pipeline 7.4 (`order_expected`) and the repository data check; playbook 6.11.
- Mon 19 Oct 2026 (about 00:35): Hand-run session with Tim after ChatGPT's repository review of 18 Oct: pipeline 7.3 and a results budget of 1.0 points for 27 to 30 Oct; playbook 6.10.
- Sun 18 Oct 2026 (about 22:05): Tim confirmed the Mon 19 Oct order is entered; the top 2% line is about +6.5%, about 5 points above Tim.
- Sun 18 Oct 2026 (about 21:50): Evening review, a change evening for Mon 19 Oct (Palantir out; Chevron 15 to 10; AbbVie 10). Tim's 16 Oct FT figures stored (-34 credits against the estimate). Four watchlist additions (Visa, Mastercard, ConocoPhillips, Walmart); Marvell, CrowdStrike, Constellation Energy removed.
- Sun 18 Oct 2026 (about 20:25): Weekend news check (H7, Sunday). No A item. Order unchanged.
- Sun 18 Oct 2026 (about 10:50): Follow-up approved by Tim. GitHub access test passed. Playbook 6.8.
- Sun 18 Oct 2026 (about 01:20): Hand-run session with Tim. Playbook 6.6: the handoff log.
- Sun 18 Oct 2026 (about 01:00): Hand-run session with Tim. Playbook 6.5 and pipeline 7.1, the corrected standstill test.
- Sun 18 Oct 2026 (about 00:30): Hand-run session with Tim after the outside audit by ChatGPT. Playbook 6.4 and pipeline 7; morning check 06:36 UK and a 07:00 UK cut-off; score frozen.
- Sat 17 Oct 2026 (about 20:25): Weekend news check (H7). No A item. Order unchanged.
- Sat 17 Oct 2026 (about 09:50): Weekly review. Fri 16 Oct logged: +0.64%; week +1.51% against -1.97%. Panel topped up to 28 members.
- Fri 16 Oct 2026 (about 09:10): Hand-run session with Tim. Broad scan built (playbook 6.3).

## 7. Market regime notes

Label: Mixed (rotation out of tech into health care, staples, value and energy; yields above 5%; oil near five-month highs with a peace-talk tail risk).

Tue 20 Oct: S&P 500 up about 0.2% to 0.3% (SPY +0.34% to 769.05), Dow about +1% (+492 points), Nasdaq flat, Russell 2000 about +1.7%. Health care at a record (Lilly +3.5% to a record; Merck, Amgen, UnitedHealth +3%; Moderna +6%); financials +1.2%; energy the weakest sector; Meta -1.6% (policy chief Joel Kaplan leaving). Breadth strong. Earnings: RTX beat and raised (EPS $2.26 against $1.78; revenue $25.0bn against $24.09bn; record $340bn backlog), 3M raised its forecast (+4%), Equifax +11% (beat, 2026 revenue outlook cut), Hasbro +11% (beat and raise), GM -7% to -7.5% (commodity costs, truck sales), GE Aerospace -3.8%. Netflix after the close: EPS $0.87 against $0.82, revenue $12.87bn in line, ad outlook lowered, shares about -4% after hours; 6% job cuts. Housing starts 1.221M against 1.30M (a four-month low). Oil: Brent above $111 early (Houthi attacks on Saudi sites, at least 18 vessels attacked in the Gulf in two weeks), then down about 1% to 3% intraday on an unconfirmed report (Al-Araby Al-Jadeed) of a Qatar and Pakistan framework: interest on $6bn of frozen Iranian funds, a confidential IAEA visit; closed near $108.9. A third US aircraft carrier is heading to the region.

Mon 19 Oct: S&P 500 +0.41% (about 7,690), Nasdaq +1.11%, Dow -0.07%; chips ended an eight-day losing streak; NAHB 29 (lowest since 2012); 10-year +6bp to 5.15%.

Week to Fri 16 Oct: S&P 500 7,659.44 (-1.95% on the week), Nasdaq -4.48%, Dow +0.67%, Russell -3.05%; VIX 20.16; SOXX -12% on the week. Brent $109.86. Fed: September minutes backed a 25bp hike; December hike odds about 74%, October about 25% to 30% (19 Oct).

Weekend log (weekend of 17 and 18 Oct): confirmed by the Sunday evening review. No A item. B: Hormuz (Araghchi's offer "still on the table"; Trump could "soon finish the job"); Russia sanctions waiver. Earlier weekend (10 and 11 Oct): no A item.

Near calendar (the full calendar to 27 Nov is on the page and in the ledger):
- Wed 21 Oct: Meta and Tesla results after the US close; EIA oil stocks 15:30 UK; 20-year bond auction 18:00 UK.
- Thu 22 Oct: Valero, Procter & Gamble, Lockheed Martin; jobless claims 13:30 UK (forecast 200,000); Conference Board leading index.
- Fri 23 Oct: flash PMIs; Michigan sentiment final.
- Sun 25 Oct: UK clocks go back; the US session is 13:30 to 20:00 UK in the week of 26 Oct. The evening review sets the order for Coca-Cola's results and the Lilly trim call.
- Mon 26 Oct: Coca-Cola's last order, before 07:00 UK.
- Tue 27 Oct: Coca-Cola; Visa (after the close, est.). Wed 28 Oct: Fed decision 18:00 UK; Microsoft; Phillips 66. Thu 29 Oct: Shell; Eli Lilly; Merck; Mastercard; Coinbase. Fri 30 Oct: Exxon Mobil, Chevron, AbbVie. Tue 3 Nov: US midterms; Amgen. Thu 5 Nov: ConocoPhillips.

## 8. Open questions for Tim

Answered: an order entered before 08:00 UK counted for that day up to 23 Oct (from 17 Oct treat 07:00 UK as the cut-off); the midday check stays off; the leaderboard shows only the top 10; Shell filled at its 08:00 open on 9 Oct; Microsoft, Coca-Cola, Palantir, Goldman Sachs, Meta Platforms and Eli Lilly are in the game's list; the orders for 13 to 16 Oct were entered; value, rank and players after Fri 16 Oct's close; the Marsh & McLennan panel swap; GitHub access from scheduled runs; the top 2% line (about +6.5%, 18 Oct); the evening run's repository (tasks recreated 18 Oct).

Still open:
1. Is AbbVie in the game's list? Assumed yes (large NYSE listing); substitute Amgen. Tim to say if it was missing.
2. Are Strategy and Coinbase in the game's list? Not needed until one is close to being bought.
3. The cut-off after the clock change: 07:00 or 08:00 UK. Tim asked FT help on 18 Oct. No test order (removed 19 Oct): 07:00 UK stays until the FT answers.
4. Does the game convert US stocks' returns into pounds? In the draft to FT help; the closing gap has stayed under 0.05%.
5. New on 20 Oct: the scheduled evening run's WebFetch refused every address it had not first seen in a search result ("permission request not answered"), so clock-suffixed quote pages, Cboe's quotes, Coinbase's candles and the market data service could not be reached. Searches found most stock pages, but several watchlist rows, the oil and Ether fund rows, the US-listed Shell and BP lines and the coin prices were missing. Worth a look in the next session with Tim (fetch permissions for the scheduled task).

## 9. Game rules

Summarised in part C of the playbook. Key facts: 5 Oct to 27 Nov 2026; 5 to 20 stocks, each 5% to 25%; cash up to 25%; no shorting or leverage; changes fill at the next open; weights reset to target at each close; performance is weight times return; final values on 27 Nov closes; one portfolio, no reset; entry is for FT subscribers aged 18 and over.

## 10. News momentum and trend: worked examples

In this game an order fills at the open, so the gap on the news day cannot be captured; only moves from the fill onwards count. Prices from stockanalysis.com daily history.

**Vistra, DOE nuclear loan (continuation that was capturable, then an abrupt reversal)**

| Date | Open | Close | Gap vs prior close | Open to close | Close position in day's range |
|---|---|---|---|---|---|
| Fri 2 Oct | 142.05 | 140.02 | n/a | -1.43% | news reported this day |
| Mon 5 Oct | 144.04 | 144.89 | +2.87% | +0.59% | upper half |
| Tue 6 Oct | 151.47 | 160.50 | +4.54% | +5.96% | near the high, volume 18.0m |
| Wed 7 Oct | 154.77 | 166.72 | -3.57% | +7.72% | near the high |
| Thu 8 Oct | 165.81 | 156.14 | -0.55% | -5.83% | near the low |

- Lesson: follow-through after strong news is real and tradeable here. It ends without warning, so size at 10% or less and exit on the first heavy-volume close below the open.

**Palantir, Goldman Sachs upgrade (a gap with no follow-through on day one, then confirmation)**

| Date | Open | High | Low | Close | Gap vs prior close | Open to close |
|---|---|---|---|---|---|---|
| Thu 8 Oct | 199.00 | 204.44 | 195.65 | 198.78 | +2.51% | -0.11% |
| Fri 9 Oct | 201.48 | 209.58 | 198.30 | 209.05 | +1.36% | +3.76% |

- Lesson: an upgrade from a major bank is a real event. The entry test is follow-through after the gap.
- Sequel: no new high after 12 Oct (212.94); on Fri 16 Oct it opened at 201.79 and closed at 186.03 on 33.2m shares, the first heavy-volume close below its open, so it was sold at Mon 19 Oct's open. Held at 5% it cost about -0.56 points to 16 Oct. Lesson: a high-range stock at 5% can still cost half a point in a week.

**RTX and Lockheed Martin, 8 Oct (a one-day bounce inside a downtrend)**

- Lesson: a strong day says nothing about the trend. Check the 50-day and 200-day averages before buying on a headline.

**Humana, 9 and 12 Oct (large gaps that faded, even with upgrades)**

- Lesson: the bigger the gap, the more of the news is already in the fill price.

**Goldman Sachs, 13 Oct (a results beat inside a downtrend)**

- Lesson: a big beat does not lift a stock in a downtrend. A results position needs the trend filter too.

**Meta Platforms, 12 to 15 Oct (follow-through entry, then a quick exit)**

- Bought for 14 Oct at 5%; on 14 Oct it closed 3.0% below its open. Sold at the 15 Oct open (726.56); it closed at 709.33 on 16 Oct and 694.25 on 20 Oct. Its rating of 57 settled on 20 Oct: lagged the index by about 8 points.
- Lesson: a momentum entry after a two-day run can reverse at once. The give-back rule cut the cost.

**TSMC, 15 Oct (held through results in a sector sell-off)**

- Gapped down 3.4% on 15 Oct after a beat with lower margins. Sold at the 16 Oct open (421.22).
- Lesson: when the score has slipped below 50 before a report, cut the hold to 5% or exit, whatever the implied move.

**Judging changes: one day against several (17 Oct)**

- Lesson: judge a change over the five sessions it was meant for (the STANDSTILL block), not its first day, and judge the process against the first order never changed.

## 11. Confidence ratings, shadow ratings, the panel test and the day call

- Confidence ratings (not calibrated): 12 resolved by 20 Oct. Latest: Meta 57 (13 Oct) lagged. Earlier: RTX 60 beat, Lockheed 55 beat, Nvidia 50 lagged, Shell 59 beat, TSMC 53 lagged, Coca-Cola 55 beat, Goldman 54 beat, Microsoft 58 beat, Palantir 58 lagged. Far too few to judge. Ratings of 18 Oct for the order in force: Exxon 60, AbbVie 60, Coca-Cola 59, Shell 59, Chevron 59, Eli Lilly 59, Microsoft 57.
- Shadow ratings: 184 logged, 60 settled. Live: score 70 and above, 17 cases, 76% beat the index (+1.73 points); 60 to 69, 17 cases, 41% (-3.60); 45 to 59, 13 cases, 23% (-3.09); below 45, 13 cases, 85% (+2.58). Weak evidence. Judgement test: no settled dates yet.
- Panel test: see section 1. Old backtest (hindsight) correlation -0.12.
- Drift record: first two entries logged 20 Oct (Hasbro ENTER, Equifax FAIL); settle five sessions after 20 Oct. Meta (21 Oct), Valero and Procter & Gamble (22 Oct) are the next likely entries. RTX (beat and raise, 20 Oct) not scanned: its closing row was not reachable.
- Day call record (S&P 500): 3 right of 6. 20 Oct: S&P 500 green called and right; portfolio green called and right.

## 12. Tools

- Tim's page: https://claude.ai/artifact/8P8UwQsb4QsbZMsKNYKrUJ, pinned in his Claude sidebar, with tabs Today, Macro, Performance, Risk, Calendar and Log. It reads four data files (`stocks`, `ledger`, `history`, `macro`) and a fifth dataset, `logos`, that no run touches. The Order panel reads the latest alert whose `stock` is "Order"; its "Enter before" bar uses a 07:00 UK cut-off.
- Playbook docs (version 6.11.1): `claude/ft-game-playbook.md` (core, with the routing table), `claude/ft-game-rules.md`, `claude/ft-game-data.md`, and the run docs `claude/ft-game-run-evening.md`, `-morning`, `-refresh`, `-weekly`, `-weekend`.
- Panel file: `panel.json` on the same artifact, named by the document `store/panel`.
- Scripts: the pipeline (version 7.4) and the screening script are assets on that artifact. Their ids and hashes are in part B of the playbook, the only place they are kept.
- Leftover assets: the four files the 14 Oct run uploaded are superseded but kept.
- Fetching assets: read each asset with a single `path`.
- Rate limits and access: on 20 Oct WebFetch accepted only addresses that had appeared in a search result; a search limited to stockanalysis.com with "<name> <ticker> stock price quote" usually surfaced the quote or history page. Pages fetched without a clock suffix were often "At close" for the session (holdings, most of the list), but some history pages and the BNO, ETHA and RTX pages were stale copies. No 429 refusals in groups of four with pauses of 40 to 60 seconds.
- Market data service: massive.com, free plan, on an account opened by Tim's father. The key is in the evening and weekly review tasks and is never written into this project's docs, the page data, alerts or messages. Not used on 20 Oct (no year of closes was needed beyond Walmart, whose statistics page was read).
- Cboe's delayed quotes: used on 19 Oct for 23 session rows; not reachable on 20 Oct. Not yet in part F: for Tim to decide whether to add it.
- Coin prices: Coinbase's public candle and ticker pages (not reachable on 20 Oct).
- Sources that did not work: CNN article pages, CNBC's oil page and live-updates page (fetch error 20 Oct), Detroit News (robots); US News world article (18 Oct).
- GitHub mirror: private repository `timzwang/ft-game` (part B and G6), reached by scheduled runs from 19 Oct.
- Two saved skills, `ft-game-playbook` and `stock-score`, load in scheduled runs; the project docs win where they differ.
