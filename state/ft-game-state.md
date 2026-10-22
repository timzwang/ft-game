# FT Stock Picking Game: state and log

Last updated: Thu 22 Oct 2026, about 21:45 UK (evening review, a change evening: for Fri 23 Oct, AMD, Shopify and Datadog sold on the endgame exit rule after heavy-volume closes below their opens; Nvidia 20 added; ServiceNow 10 to 20, Palantir 15 to 20, Arm Holdings 10 to 15; message sent about 21:42 UK). Western Digital had no after-hours price when the review read it, so order B stayed the base (core part D). Day -1.75% against SPY -1.18%, the first session of the endgame book. Before that, Wed 21 Oct about 22:55 UK (hand-run session with Tim: playbook 6.13, the endgame stance, and the switch to order B for Thu 22 Oct). Earlier entries: see the review log (section 6).

This doc is the narrative record for Tim's entry, "Seeking Beta". The procedure for every run is in `claude/ft-game-playbook.md` (the core doc) and the docs its routing table names. The numbers (prices, scores, daily performance, contributions, ratings and their outcomes, the full calendar, analyst changes, alerts, the panel test, the drift record) live in the data files behind Tim's page and the panel file, and are produced by the pipeline script; this doc carries the decisions and the reasons.

Messages: from 10 Oct Tim is sent a message only when there is something for him to enter or answer (playbook part I, "When Tim is told"). Quiet runs update the page and this doc and send nothing.

Scheduled runs: evening review 21:30 UK Sun to Thu; morning check 06:36 UK Mon to Fri; price refresh 16:45 UK and late price refresh 19:22 UK Mon to Fri; results-day refresh 14:50 UK Mon to Fri (acts only on results days); weekly performance review Sat 09:12 UK; weekend news check Sat and Sun 20:20 UK; midday check 12:40 UK Mon to Fri (switched off, see section 8).

**Cut-off: until Tim decides otherwise, every order must be entered before 07:00 UK (playbook part C, from 17 Oct; FT Customer Care told Tim on 21 Oct the cut-off stays 08:00 UK local time all year).**

## 1. Status

- **Playbook version 6.13** (6.13, 21 Oct late evening: the endgame stance in core part D, approved by Tim at 22:38 UK: score floor, trend tests, downtrend replacement, 10% caps, results budget, volatility caps and theme guide suspended for the rest of the game; the book is high-beta technology; exits only on a heavy-volume close below the open or a report that gaps down beyond its options move and closes in the lower half; every exit replaced from the swap column; 6.12.1: feed 1.1; 6.12: the price feed on GitHub and pipeline 7.7; 6.11.1: the 26 Oct cut-off test removed; 6.11: pipeline 7.4 and `order_expected`; 6.10: pipeline 7.3 and the 1.0 budget for 27 to 30 Oct; 6.9 to 6.5: repository tasks, handoff log, standstill test; 6.4: after the outside audit, pipeline 7, 07:00 UK cut-off, score frozen; 6.3: the broad scan; 6.2: day call never moves cash; 6: split docs, panel test, drift scan). **Pipeline script version 7.7** (part B holds the asset id and hash; hash checked and matched on 22 Oct).
- **Estimated value at Thu 22 Oct close: 99,610, -0.39% since the start, against -1.58% for the S&P 500 fund (gap +1.19 points).** Thu 22 Oct -1.75% against SPY -1.18%: Datadog -0.51 points, Shopify -0.48, AMD -0.46, Sandisk -0.43, Palantir -0.36, Arm -0.32, Robinhood -0.10; ServiceNow +0.18, Strategy +0.03; the sold holdings added +0.71 from their opens over Wednesday's closes (Coca-Cola +0.25, Exxon +0.15, Lilly +0.13, Shell +0.10, Chevron +0.09). Wed 21 Oct: 101,378.
- **Last FT figures: Wed 21 Oct after the close, 101,342 (+1.34%), rank 3,948 of 14,357 (top 27.5%; the top 2% is rank 287 or better).** RECONCILE -36 credits (-0.04%). Top 2% line +7.46% on 21 Oct (rank 274, stored as `top2_return_pct` 7.46).
- **Standstill (22 Oct run):** change for 14 Oct -0.48 (complete); 15 Oct +0.50 (complete); 16 Oct +0.21 (complete); 19 Oct -0.28 (four sessions); 22 Oct (the endgame switch) -2.35 after one session, expected 0.0. Week of 12 Oct +0.12; week of 19 Oct -2.63 so far. Inception (ten sessions): -1.96 as entered, -2.48 fully invested. Expected benefit: the change for 23 Oct carries 0.0 (waiting to fill).
- **Panel test:** history verdict "no evidence" (average rank correlation +0.050, t +1.3, 49 dates; one-year strength the strongest part, t +1.9). Live: one date (+0.37), too few to judge. The score is frozen.
- **Order for Fri 23 Oct's open (message sent about 21:42 UK on Thu 22 Oct):** Palantir 20, Nvidia 20, ServiceNow 20, Arm Holdings 15, Sandisk 10, Robinhood 10, Strategy 5, cash 0. Order in force until then (order B, filled Thu 22 Oct): AMD 15, Palantir 15, Shopify 15, Sandisk 10, Arm Holdings 10, Datadog 10, ServiceNow 10, Robinhood 10, Strategy 5.
- Day call for Fri 23 Oct: S&P 500 green 61% (usual 55%); portfolio green 55% (usual 54%, reviewer -3 for oil at May highs and the heavy-volume break in AI names). Record (S&P 500): 5 right of 8. Thu 22 Oct: the morning check had moved both calls to red; S&P 500 red called and right (-1.18%); portfolio red called and right (-1.75%).
- Macro at Thu 22 Oct: US 2-year 4.65% (-16bp), 10-year 4.96% (-17bp on the day, -25bp over five: a tailwind on the mechanical label), 30-year 5.29%. Gilt 5.33%, German 3.33%, French 5.08% (+11bp), Italian 4.60%, Japanese 2.88%. Brent $112.98 (+3.1%, +6.9% over five), WTI $99.27, natural gas $2.78, gold $4,039 (commodities from the futures fallback). Backdrop label: neutral (falling yields against rising oil).
- Crypto: Bitcoin $81,381 at the US close (-3.6% on the day, -0.4% over five); trend up, but IBIT 2.2% below its 20-day average (2.5% above its 50-day), so no new crypto-linked buy until it is back above the 20-day. Ether $2,384, trend mixed. Crypto-linked holdings 15% (Robinhood 10, Strategy 5), at the limit.
- Regime: mixed. Thu 22 Oct: S&P 500 -1.21% to 7,663, Nasdaq -2.60%, Dow +0.02%, Russell 2000 -0.20%. Chips led the fall on AI spending worries after Meta (-7.0%) and Tesla (-3.1%); Lam Research about -9%, AMD -8.1%, Sandisk -8.5%, Seagate -7.9%. Brent up to near $113 on US-Iran escalation fears (highest since May). What would make it risk-off: the 10-year back above 5.25% with the S&P 500 below its 20-day, a hike on 28 Oct priced above 70%, or Brent through its May high of $114.44 with tech still falling.

## 2. Current portfolio

The order for Fri 23 Oct's open (message sent about 21:42 UK). Scores and bands from the pipeline at the Thu 22 Oct close. Under the endgame stance (core part D) the score floor, trend tests, volatility caps, theme guide and results budget do not apply; the NOTE lines for them are expected.

| Stock | Weight | Confidence (not calibrated) | Score | Band | Flags | Next results (implied move) | Swap if missing or broken |
|---|---|---|---|---|---|---|---|
| Palantir | 20% | 55 | 61 | Strong | none | 2 Nov, after US close (12.2%) | ServiceNow |
| Nvidia | 20% | 52 | 37 | Weak | below 50-day | 18 Nov, after US close (est.; not yet checked) | AMD |
| ServiceNow | 20% | 55 | 68 | Strong | none; +2.5% on 1.6x volume 22 Oct | 28 Oct, after US close (11.0%) | Shopify |
| Arm Holdings | 15% | 50 | 30 | Weak | below 50-day; oversold | 4 Nov, after US close (14.2%) | Qualcomm |
| Sandisk | 10% | 50 | 35 | Weak | below 50-day; oversold | 29 Oct, after US close, confirmed (11.4%) | Micron |
| Robinhood | 10% | 50 | 34 | Weak | below 50-day; crypto-linked | 27 Oct, after US close (10.3%) | Coinbase |
| Strategy | 5% | 53 | 47 | Middling | crypto-linked (1.82% per 1% in Bitcoin) | 29 Oct, after US close, est. (9.2%) | Coinbase |
| Cash | 0% | | | | | | |

RESULTS TOTAL next 5 sessions 4.83 points across four reports, next 10 sessions 9.40 points across six (deliberate: the stance needs variance). Themes: AI and chips 45%, Software 40%, Banks 10% (Robinhood), Crypto 5%. Largest risk shares: Arm 21.8%, Palantir 18.0%, ServiceNow 14.1%. Worst scenario: a deeper AI sell-off, -6.5%.

Points for the coming reviews:

- Exits under the stance: the next open after a heavy-volume close below the open (taken on 22 Oct as the pipeline's "heavy-volume down day" flag, 1.3x the 20-day average, with a close below the open), or after a report that gaps down beyond its options move and closes in the lower half of its range. Every exit is replaced from the swap column; when the swap has itself just given the exit signal (Cloudflare, 22 Oct), its weight goes to holdings already in the book.
- Robinhood reports Tue 27 Oct after the close: last order before 07:00 Tue 27 Oct. ServiceNow Wed 28 Oct (20%, 2.2 points at its implied move). Sandisk and Strategy Thu 29 Oct.
- Western Digital's report of 22 Oct: no after-hours price or results seen by 21:40 UK. The next review should read its reaction session (23 Oct) for the memory theme (the stance's invalidation test).
- Sold holdings stay listed for the standstill test: Coca-Cola, Exxon Mobil, Shell, Microsoft, Eli Lilly, Chevron, AbbVie to Thu 29 Oct; AMD, Shopify, Datadog to Fri 30 Oct. Hasbro stays as a drift row to settle.

## 3. Pending order

**Changed for Fri 23 Oct's open. Message sent about 21:42 UK on Thu 22 Oct; taken as entered unless Tim says otherwise.**

Palantir 20, Nvidia 20, ServiceNow 20, Arm Holdings 15, Sandisk 10, Robinhood 10, Strategy 5, cash 0.

Changes against the order in force (order B, filled 22 Oct): sell AMD 15, Shopify 15, Datadog 10; buy Nvidia 20; ServiceNow 10 to 20, Palantir 15 to 20, Arm 10 to 15. Rule exit (endgame part D): AMD (-3.1% open to close, 1.4x volume), Shopify (-3.2%, 1.3x) and Datadog (-5.1%, 1.3x) closed below their opens on heavy volume. Swaps: Nvidia for AMD, ServiceNow for Shopify; Cloudflare (Datadog's swap) gave the same signal, so its 10% went to Palantir and Arm. Expected benefit recorded: 0.0 points. What would show it wrong: AMD, Shopify and Datadog recovering more than Nvidia, ServiceNow, Palantir and Arm over five sessions.

## 4. Watchlist

27 names (the cap of 25 is lifted until Fri 30 Oct for the standstill test). Scores and bands at the Thu 22 Oct close.

Tonight: added Nvidia (into the order) and Cloudflare (Watching: Datadog's swap; closed below its open on heavy volume with a faded gap on 22 Oct; promote on a session closing above its open in the upper half of its range). Removed Analog Devices and Meta Platforms (weak, fit neither endgame order, not held in the last five sessions). AMD, Shopify, Datadog: "Exit signal", kept five sessions.

| Name | Band | Status | Score | Note |
|---|---|---|---|---|
| Exxon Mobil | Strong | Watching (sold 22 Oct) | 84 | Kept to 29 Oct; not to be re-bought under the stance |
| AbbVie | Strong | Watching (sold 22 Oct) | 82 | As above |
| Eli Lilly | Strong | Watching (sold 22 Oct) | 80 | As above |
| Coca-Cola | Strong | Watching (sold 22 Oct) | 77 | As above |
| Centene | Strong | Watching | 77 | Results 28 Oct (est.); fits neither order |
| ConocoPhillips | Strong | Watching | 76 | Fits neither order |
| Chevron | Strong | Watching (sold 22 Oct) | 75 | Kept to 29 Oct |
| Humana | Strong | Ready | 71 | Fits neither order |
| Hasbro | Strong | Watching (drift row) | 71 | Drift row settles 27 Oct |
| Charles River Laboratories | Strong | Needs follow-through | 70 | Extended; heavy-volume down day 22 Oct |
| Valero Energy | Strong | Watching | 69 | Reported 22 Oct: drift FAIL |
| Shell | Strong | Watching (sold 22 Oct) | 68 | Kept to 29 Oct |
| Phillips 66 | Strong | Results ahead | 68 | 28 Oct, before US open |
| Marathon Petroleum | Strong | Watching | 65 | Fits neither order |
| BP | Strong | Watching | 65 | Fits neither order |
| Datadog | Strong | Exit signal (sold for 23 Oct) | 63 | Kept to 30 Oct |
| Microsoft | Strong | Watching (sold 22 Oct) | 61 | Results 28 Oct; kept to 29 Oct |
| NetApp | Strong | Watching | 60 | Tech; correlation 0.44 with AMD |
| Targa Resources | Middling | Watching | 55 | Fits neither order |
| Shopify | Middling | Exit signal (sold for 23 Oct) | 53 | Kept to 30 Oct |
| Cloudflare | Middling | Watching (added 22 Oct) | 45 | Datadog's swap; results 5 Nov |
| AMD | Weak | Exit signal (sold for 23 Oct) | 42 | Kept to 30 Oct; Nvidia's swap |
| Seagate | Weak | Results ahead | 38 | 27 Oct after close; swap for Western Digital |
| TSMC | Weak | Watching | 35 | First order stock; remove after Fri 23 Oct |
| Western Digital | Weak | Watching | 35 | Reported 22 Oct after the close; swap for Seagate |
| Micron | Weak | Watching | 31 | Sandisk's swap; oversold |
| Coinbase (crypto tracker) | Weak | Watching | 27 | Kept whatever it scores; swap for Robinhood and Strategy |

Names that fit neither endgame order and were not held in the last five sessions may be removed without the three-session wait (part D); the strong energy and health care names are kept for now only because the list cap is lifted and they cost nothing. Intake tonight: no new candidates beyond the two swaps; the broad scan was current but its names were not checked, because the endgame book takes new names only from the swap column.

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
| Sun 18 Oct, about 21:47 UK (entered, confirmed about 22:00 UK) | Mon 19 Oct | Sell Palantir 5; Chevron 15 to 10; add AbbVie 10 | Palantir's heavy-volume exit signal; oil names carried 64% of risk; AbbVie score 82 |
| Wed 21 Oct, about 21:39 UK (replaced at 22:50 before it filled) | Thu 22 Oct | Add Hasbro 5; Eli Lilly 15 to 10 | Hasbro drift entry; Lilly results-budget trim. Expected +0.05 |
| Wed 21 Oct, about 22:50 UK (confirmed 22:55 UK) | Thu 22 Oct | Endgame switch, order B: sell all seven holdings; AMD 15, Palantir 15, Shopify 15, Sandisk 10, Arm Holdings 10, Datadog 10, ServiceNow 10, Robinhood 10, Strategy 5 | Endgame stance (playbook 6.13). Expected 0.0 points (variance, not edge) |
| Thu 22 Oct, about 21:42 UK (message sent) | Fri 23 Oct | Sell AMD 15, Shopify 15, Datadog 10; add Nvidia 20; ServiceNow 10 to 20, Palantir 15 to 20, Arm 10 to 15 | Endgame exit rule: heavy-volume closes below the open on 22 Oct; swaps from the column (Cloudflare skipped: same signal). Expected 0.0 points |

## 6. Review log (newest first, keep the latest 15)

- Thu 22 Oct 2026 (about 21:45): Evening review, a change evening for Fri 23 Oct (rule exits of AMD, Shopify and Datadog; Nvidia 20; ServiceNow, Palantir and Arm raised). Day -1.75% against SPY -1.18% on a Nasdaq -2.6% AI sell-off. Western Digital: no after-hours price found by about 21:40 UK (several searches; only older quarters' articles surfaced), so order B stayed the base. Drift scan: Valero, Procter & Gamble, Meta all FAIL. Watchlist: added Nvidia, Cloudflare; removed Analog Devices, Meta. Price feed: forced (request pushed 21:33 UK; second run for NET and NVDA at about 21:37 UK); broad scan: forced. Commodities from the futures fallback. Files published.
- Wed 21 Oct 2026 (about 23:12): Tim relayed FT Customer Care's answer: the order cut-off stays 08:00 UK local time all year. Recorded; the 07:00 working cut-off stays until Tim decides.
- Wed 21 Oct 2026 (about 23:02): Tim sent the top 2% line (rank 274, +7.46%); stored; gap maths re-run.
- Wed 21 Oct 2026 (about 22:58): Tim confirmed order B entered and gave the FT figures (101,342, rank 3,948 of 14,357); RECONCILE -36 credits.
- Wed 21 Oct 2026 (about 22:55): Hand-run session with Tim: ten new stocks added from the feed, results events with implied moves, order B for Thu 22 Oct (message 22:50 UK).
- Wed 21 Oct 2026 (about 22:50): Hand-run session with Tim. Playbook 6.13: the endgame stance (core part D).
- Wed 21 Oct 2026 (about 22:30): Tim's answers recorded (Marsh & McLennan stays in the panel; PRs #3 and #5 merged). Research checks on PR #7, not deployed.
- Wed 21 Oct 2026 (about 22:10): Feed 1.1 and playbook 6.12.1; review re-run with Analog Devices added.
- Wed 21 Oct 2026 (about 21:45): Evening review, a change evening for Thu 22 Oct (Hasbro 5; Lilly 15 to 10), later replaced by order B.
- Wed 21 Oct 2026 (about 14:30): Hand-run session with Tim. Playbook 6.12: the price feed; pipeline 7.7.
- Tue 20 Oct 2026 (about 22:05): Evening review, quiet. Day +0.62% against SPY +0.34%.
- Mon 19 Oct 2026 (about 22:25): The Mon 26 Oct cut-off test removed (playbook 6.11.1).
- Mon 19 Oct 2026 (about 22:15): Evening review, quiet. Day -0.33% against SPY +0.42%.
- Mon 19 Oct 2026 (about 20:40): Pipeline 7.4 (`order_expected`) and the repository data check; playbook 6.11.
- Mon 19 Oct 2026 (about 00:35): Pipeline 7.3 and a results budget of 1.0 points for 27 to 30 Oct; playbook 6.10.

## 7. Market regime notes

Label: Mixed (an AI and chip sell-off on spending worries after Meta's results; oil at its highest since May on US-Iran escalation fears; Treasury yields falling sharply, which supports growth stocks if the sell-off steadies).

Thu 22 Oct: S&P 500 -1.21% (7,663.45), Nasdaq -2.60% (26,008.86), Dow +0.02%, Russell 2000 -0.20%. Meta -7.0% after its results ($64.6bn revenue, a beat, but a $9.9bn legal charge and higher spending), Tesla -3.1%. Chips drove the fall (Lam Research about -9%, Applied Materials and KLA about -6%, AMD -8.1%, Sandisk -8.5%, Nvidia -2.4%). ServiceNow +2.5%. Procter & Gamble rose after a beat with guidance kept; Valero beat (EPS $23.90 against $21.17) but fell. Brent near $113 (+3% to 4%) on reports of planned US and Israeli strikes after the midterms, a drone attack on the Shaybah oilfield and US staff leaving Saudi Arabia; WTI about $99. US 10-year 4.96% (-17bp). Western Digital reported after the close; no reaction seen by the review.

Wed 21 Oct: S&P 500 +0.5% (fourth straight gain), Nasdaq +0.9%; Meta beat after the close. Tue 20 Oct: S&P 500 +0.3%, health care at a record. Mon 19 Oct: S&P 500 +0.41%, Nasdaq +1.11%. Week to Fri 16 Oct: S&P 500 -1.95%, Nasdaq -4.48%.

Weekend log (weekend of 17 and 18 Oct): no A item. B: Hormuz; Russia sanctions waiver.

Near calendar (the full calendar to 27 Nov is on the page and in the ledger):
- Fri 23 Oct: the new order fills at the US open; Western Digital's reaction session; flash PMIs; Michigan sentiment final. TSMC may leave the list after this session.
- Sun 25 Oct: UK clocks go back; the US session is 13:30 to 20:00 UK in the week of 26 Oct.
- Mon 26 Oct: Robinhood's last order before its report, before 07:00 UK Tue 27 Oct.
- Tue 27 Oct: Robinhood and Seagate (after the close); Coca-Cola; Visa. Wed 28 Oct: Fed decision 18:00 UK; ServiceNow and Microsoft (after the close); Phillips 66. Thu 29 Oct: Sandisk and Strategy (after the close); Shell; Eli Lilly; Coinbase. Fri 30 Oct: Exxon Mobil, Chevron, AbbVie. Mon 2 Nov: Palantir. Tue 3 Nov: US midterms. Wed 4 Nov: Arm. Thu 5 Nov: Cloudflare. Wed 18 Nov (est.): Nvidia.

## 8. Open questions for Tim

Answered: an order entered before 08:00 UK counted for that day up to 23 Oct (from 17 Oct treat 07:00 UK as the cut-off); the midday check stays off; the leaderboard shows only the top 10; Shell filled at its 08:00 open on 9 Oct; Microsoft, Coca-Cola, Palantir, Goldman Sachs, Meta Platforms and Eli Lilly are in the game's list; the orders for 13 to 16 Oct were entered; GitHub access from scheduled runs; the cut-off after the clock change (FT Customer Care, 21 Oct: 08:00 UK local time all year; whether runs move back to it is Tim's call); the fetch tool refusing built addresses (answered by the price feed); Marsh & McLennan stays in the panel; order B entered (21 Oct, 22:55 UK).

Still open:
1. Is Nvidia in the game's list? Assumed yes (it was in the first order on 9 Oct, so it is). Are ServiceNow, Arm, Sandisk, Robinhood, Strategy and Palantir in it? Palantir yes; the rest assumed yes since order B was entered without a report of a missing stock.
2. Is Hasbro in the game's list? No longer needed (never filled).
3. How a mixed London and US order entered for 26 Nov fills: Tim to ask FT help.
4. Does the game convert US stocks' returns into pounds? The closing gap has stayed under 0.05%.
5. Tim's FT value and rank after Thu 22 Oct or Fri 23 Oct's close (asked by the weekly review on Saturday).

## 9. Game rules

Summarised in part C of the playbook. Key facts: 5 Oct to 27 Nov 2026; 5 to 20 stocks, each 5% to 25%; cash up to 25%; no shorting or leverage; changes fill at the next open; weights reset to target at each close; performance is weight times return; final values on 27 Nov closes; one portfolio, no reset; entry is for FT subscribers aged 18 and over.

## 10. News momentum and trend: worked examples

In this game an order fills at the open, so the gap on the news day cannot be captured; only moves from the fill onwards count. Prices from stockanalysis.com daily history and, from 21 Oct, the price feed.

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
- Sequel: on Fri 16 Oct it opened at 201.79 and closed at 186.03 on 33.2m shares, the first heavy-volume close below its open, so it was sold at Mon 19 Oct's open. Lesson: a high-range stock at 5% can still cost half a point in a week.

**RTX and Lockheed Martin, 8 Oct (a one-day bounce inside a downtrend)**

- Lesson: a strong day says nothing about the trend. Check the 50-day and 200-day averages before buying on a headline.

**Humana, 9 and 12 Oct (large gaps that faded, even with upgrades)**

- Lesson: the bigger the gap, the more of the news is already in the fill price.

**Goldman Sachs, 13 Oct (a results beat inside a downtrend)**

- Lesson: a big beat does not lift a stock in a downtrend. A results position needs the trend filter too.

**Meta Platforms, 12 to 15 Oct (follow-through entry, then a quick exit)**

- Bought for 14 Oct at 5%; sold at the 15 Oct open (726.56) after a close 3.0% below its open. It closed at 648.85 on 22 Oct after its results. Lesson: a momentum entry after a two-day run can reverse at once; the give-back rule cut the cost.

**TSMC, 15 Oct (held through results in a sector sell-off)**

- Lesson: when the score has slipped below 50 before a report, cut the hold to 5% or exit, whatever the implied move.

**Judging changes: one day against several (17 Oct)**

- Lesson: judge a change over the five sessions it was meant for (the STANDSTILL block), not its first day, and judge the process against the first order never changed.

**Hasbro, 20 and 21 Oct (a drift entry bought on its second session, never filled)**

| Date | Open | High | Low | Close | Volume |
|---|---|---|---|---|---|
| Tue 20 Oct (reaction day) | 102.40 | n/a | n/a | 109.52 | 7.3m |
| Wed 21 Oct | 110.27 | 114.05 | 109.60 | 114.00 | 5.2m (2.8 times average) |

- The order was replaced by the endgame switch before it filled; Hasbro closed at 117.23 on 22 Oct (open 113.85). Its drift row settles on 27 Oct.

**The endgame switch, 22 Oct (first session of a one-way book)**

- The high-beta book filled at the 22 Oct open into an AI sell-off (Nasdaq -2.6%): -1.75% on the day against SPY -1.18%, and -2.35 points against the old defensive book, which rose. Three holdings gave the exit signal on day one. Lesson: a one-way book doubles both the bad and the good days; one session says nothing about the stance, and the exit rule will churn a high-beta book on broad sell-off days, which is the price of keeping it.

## 11. Confidence ratings, shadow ratings, the panel test and the day call

- Confidence ratings (not calibrated): 13 resolved by 21 Oct; far too few to judge. Ratings for the order of 23 Oct: Palantir 55, ServiceNow 55, Strategy 53, Nvidia 52, Arm 50, Sandisk 50, Robinhood 50 (the case rests on variance, not picks).
- Shadow ratings: 258 logged. Live: score 70 and above, 39 cases, 64% beat the index (+0.88 points); 60 to 69, 34 cases, 44% (-2.78); 45 to 59, 19 cases, 16% (-2.89); below 45, 17 cases, 76% (+2.19). Weak evidence, few dates. Judgement test: no settled dates yet.
- Panel test: see section 1. Old backtest (hindsight) correlation +0.01.
- Drift record: Hasbro ENTER and Equifax FAIL (20 Oct); Elevance, AT&T, Netflix FAIL (21 Oct); Valero (beat, no guidance, fell), Procter & Gamble (guidance kept; consensus not confirmed) and Meta (fell 7%) FAIL (22 Oct). None settled yet.
- Day call record (S&P 500): 5 right of 8. 22 Oct: red called (after the morning check's -3) and right.

## 12. Tools

- Tim's page: https://claude.ai/artifact/8P8UwQsb4QsbZMsKNYKrUJ, pinned in his Claude sidebar, with tabs Today, Macro, Performance, Risk, Calendar and Log. It reads four data files (`stocks`, `ledger`, `history`, `macro`) and a fifth dataset, `logos`, that no run touches. The Order panel reads the latest alert whose `stock` is "Order"; its "Enter before" bar uses a 07:00 UK cut-off.
- Playbook docs (version 6.13): `claude/ft-game-playbook.md` (core, with the routing table), `claude/ft-game-rules.md`, `claude/ft-game-data.md`, and the run docs `claude/ft-game-run-evening.md`, `-morning`, `-refresh`, `-weekly`, `-weekend`.
- Panel file: `panel.json` on the same artifact, named by the document `store/panel`.
- Scripts: the pipeline (version 7.7) and the screening script are assets on that artifact. Their ids and hashes are in part B of the playbook, the only place they are kept.
- Price feed (data doc G8): `feed/latest.json` and `feed/live.json` in the repository. 22 Oct: the close run had not yet run at 21:32 UK; a pushed request forced it within about a minute, and a `tickers: NET NVDA` line was served within a minute (Cloudflare got 551 rows). Every list stock, SPY, the extra rows, the panel, the US yields and the coins came from it; nothing missing or refused. Four bars widened by the feed (Chevron, Corning, McKesson, Valero). The feed carries no after-hours prices.
- Pages reached through searches on 22 Oct: tradingeconomics' UK bond page (non-US yields; its commodity page did not surface, so commodities came from `feed --futures yes`), Yahoo Finance's live market page (index closes), stockanalysis.com's Cloudflare quote page, MarketBeat (Valero), StockTitan (P&G release). stockanalysis.com's Western Digital history page served a copy from 10:12 EDT; no Western Digital after-hours price or result was found.
- Market data service: massive.com, free plan, on an account opened by Tim's father. The key is in the evening and weekly review tasks and is never written into this project's docs, the page data, alerts or messages. Not used on 22 Oct (the feed covered every price).
- Sources that did not work: CNBC article pages (P&G, 22 Oct: client error); Chartmill news pages; CNN article pages; Detroit News.
- GitHub mirror: private repository `timzwang/ft-game` (part B and G6). On 22 Oct the session's clone was on a detached HEAD at the start; the run checked out `main` and fast-forwarded before pushing.
- Two saved skills, `ft-game-playbook` and `stock-score`, load in scheduled runs; the project docs win where they differ.
