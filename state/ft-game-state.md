# FT Stock Picking Game: state and log

Last updated: Mon 26 Oct 2026, about 23:25 UK (hand-run session with Tim: his FT figures for the 26 Oct close recorded; the 27 Oct order seen entered on the FT page; playbook 6.14.1 and feed 1.2: the non-US 10-year yields now come from the price feed, which fixes the evening review's open ISSUE). Before that, Mon 26 Oct 2026, about 21:45 UK (evening review, a change evening for Tue 27 Oct: ServiceNow sold on the endgame exit rule, Robinhood and Strategy sold because IBIT closed below its 50-day average; Shopify 20, Micron 10, Datadog 5 added; message sent about 21:34 UK). Before that, Mon 26 Oct about 18:05 UK (hand-run session with Tim, playbook 6.14; morning check moved to 07:26 UK at 18:03: the 08:00 UK cut-off and pipeline 7.8, a nightly watchdog, the data check fixed; no change to the order). Before that, Sun 25 Oct 2026, about 21:50 UK (evening review, FAULT: running the script was refused; the order in force for Mon 26 Oct stood). Earlier entries: see the review log (section 6).

This doc is the narrative record for Tim's entry, "Seeking Beta". The procedure for every run is in `claude/ft-game-playbook.md` (the core doc) and the docs its routing table names. The numbers (prices, scores, daily performance, contributions, ratings and their outcomes, the full calendar, analyst changes, alerts, the panel test, the drift record) live in the data files behind Tim's page and the panel file, and are produced by the pipeline script; this doc carries the decisions and the reasons.

Messages: from 10 Oct Tim is sent a message only when there is something for him to enter or answer (playbook part I, "When Tim is told"), and always when there is an issue (part I, "Issues: flag and fix", from 26 Oct). Quiet runs update the page and this doc and send nothing.

Scheduled runs: evening review 21:30 UK Sun to Thu; morning check 07:26 UK Mon to Fri (from Tue 27 Oct; 06:36 from 18 to 26 Oct; playbook 6.14); price refresh 16:45 UK and late price refresh 19:22 UK Mon to Fri; results-day refresh 14:50 UK Mon to Fri (acts only on results days); weekly performance review Sat 09:12 UK; weekend news check Sat and Sun 20:20 UK; nightly watchdog 22:47 UK every day (from 26 Oct); midday check 12:40 UK Mon to Fri (switched off, see section 8).

**Cut-off: every order must be entered before 08:00 UK, UK local time all year (FT Customer Care to Tim, 21 Oct; Tim approved the move back the same night; playbook 6.14 and pipeline 7.8 from 26 Oct). 07:00 UK was used as a safety margin from 17 to 26 Oct.**

## 1. Status

- **Playbook version 6.14.1** (6.14.1, 26 Oct late evening, hand-run with Tim: the UK, German, French, Italian and Japanese 10-year yields from the price feed, feed 1.2, tradingeconomics only as the fallback; 6.14, 26 Oct afternoon, hand-run with Tim: cut-off 08:00 UK, pipeline 7.8 from commit `9760163`, nightly watchdog at 22:47 UK, data check false failure fixed; 6.13.2, 26 Oct: flag and fix every issue; 6.13.1, 26 Oct: the script run from the repository; 6.13, 21 Oct late evening: the endgame stance in core part D, approved by Tim at 22:38 UK: score floor, trend tests, downtrend replacement, 10% caps, results budget, volatility caps and theme guide suspended for the rest of the game; the book is high-beta technology; exits only on a heavy-volume close below the open or a report that gaps down beyond its options move and closes in the lower half; every exit replaced from the swap column; 6.12.1: feed 1.1; 6.12: the price feed on GitHub and pipeline 7.7; 6.11.1: the 26 Oct cut-off test removed; 6.11: pipeline 7.4 and `order_expected`; 6.10: pipeline 7.3 and the 1.0 budget for 27 to 30 Oct; 6.9 to 6.5: repository tasks, handoff log, standstill test; 6.4: after the outside audit, pipeline 7, 07:00 UK cut-off, score frozen; 6.3: the broad scan; 6.2: day call never moves cash; 6: split docs, panel test, drift scan). **Pipeline script version 7.8** (from 26 Oct: only the cut-off constant changed; part B holds the asset id, the run commit and the hash). The 26 Oct evening review ran it from commit `9760163` (hash matched part B): the first full pipeline run since 24 Oct.
- **Estimated value at Mon 26 Oct close: 100,879, +0.88% since the start, against -1.40% for the S&P 500 fund (gap +2.28 points).** Mon 26 Oct +1.22% against SPY +0.71%: Arm +0.93 points, Nvidia +0.48, Palantir +0.21, Sandisk +0.14; ServiceNow -0.10, Strategy -0.21, Robinhood -0.24. Week of 19 Oct: -1.74% against SPY -0.43%.
- **Last FT figures: Mon 26 Oct close, 100,973 (+0.97%), rank 3,994 of 14,736 (top 27.1%; the top 2% is rank 294 or better).** Read by Tim at 22:52 UK from the FT page, its value timed 19:59 UK (the US closed at 20:00). Against the estimate of 100,879: +94 credits (+0.09%), inside the 0.2% check. A player at rank 330 stood at 108,141 (+8.14%), so the top 2% line was a little above +8.14%: the gap is at least 7.2 points with 23 sessions left. **Not yet in the ledger: the next evening review gives it under `reported` (date 2026-10-26, time_uk "after close", value 100973, rank 3994, players 14736, top2_return_pct 8.14, note "rank 330 at +8.14%; the line is rank 294, so a little higher").** Before that: Wed 21 Oct after the close, 101,342 (+1.34%), rank 3,948 of 14,357; top 2% line +7.46% (rank 274).
- **Standstill (26 Oct run):** change for 15 Oct +0.50, 16 Oct +0.21, 19 Oct -0.42 (all complete); 22 Oct (the endgame switch) -1.34 after three sessions, expected 0.0; 23 Oct (rule exits) -0.49 after two sessions, expected 0.0; 27 Oct (rule exits) waiting to fill, expected 0.0. Week of 12 Oct +0.12; week of 19 Oct -3.17. Inception (twelve sessions): -2.90 as entered, -4.18 fully invested.
- **Panel test:** history verdict "no evidence" (average rank correlation +0.050, t +1.3, 49 dates; one-year strength the strongest part, t +1.9). Live: one date (+0.37), too few to judge. All 30 members up to date. The score is frozen.
- **Order for Tue 27 Oct's open (changed tonight):** Palantir 20, Nvidia 20, Shopify 20, Arm Holdings 15, Sandisk 10, Micron 10, Datadog 5, cash 0.
- Day call record (S&P 500): 6 right of 10. Mon 26 Oct: S&P 500 rose 0.71%. Tue 27 Oct call: S&P 500 Green 51% against a usual 55%; portfolio (new order) Green 54% against a usual 55%: both close to a coin flip.
- Macro at Mon 26 Oct: US 2-year 4.68%, 10-year 5.00% (0bp on the day, -9bp over five), 30-year 5.31%. Non-US 10-year yields not refreshed by the review (tradingeconomics page showed no figure dated 26 Oct; carried from 22 and 23 Oct). Fixed for the coming runs (feed 1.2): the feed gave the 26 Oct closes as UK 5.35, Germany 3.37, France 4.90, Italy 4.50, Japan 2.79 (not in the ledger, whose 26 Oct row was written before; France 4.92 to 4.93 and Germany 3.37 on two other pages). Brent $110.14, WTI $101.27, natural gas $3.04, gold $4,027 (all from the futures fallback). Backdrop label: neutral. VIX 18.39 (-5.5%).
- Crypto: Bitcoin $79,875 at the US close (-1.6% on the day, -2.0% over five); trend mixed: IBIT 0.2% below its 50-day, 3.6% below its 20-day, 8.6% above its 200-day. The IBIT close below its 50-day forced Robinhood and Strategy out for 27 Oct. No crypto-linked holding from 27 Oct; Coinbase cannot be bought until Bitcoin's trend is up and IBIT is above its 20-day.
- Regime: mixed. Mon 26 Oct: S&P 500 +0.70% to 7,676.8, Nasdaq +0.82%, Dow +0.28%, Russell 2000 +0.4%; Anthropic's public listing filing revived the AI trade (chips led); oil eased on US-Iran hopes; Fed meets 27 and 28 Oct (hold about 88% priced).

## 2. Current portfolio

The order for Tue 27 Oct's open. Scores and bands from the pipeline at the Mon 26 Oct close. Under the endgame stance (core part D) the score floor, trend tests, volatility caps, theme guide and results budget do not apply; the NOTE lines for them are expected.

| Stock | Weight | Confidence (not calibrated) | Score | Band | Flags | Next results (implied move) | Swap if missing or broken |
|---|---|---|---|---|---|---|---|
| Palantir | 20% | 55 | 71 | Strong | none | 2 Nov, after US close (12.2%) | ServiceNow |
| Nvidia | 20% | 52 | 47 | Middling | below 50-day | 18 Nov, after US close (est.; not yet checked) | AMD |
| Shopify | 20% | 54 | 57 | Middling | none | 3 Nov, before US open (14.6%) | ServiceNow |
| Arm Holdings | 15% | 50 | 40 | Weak | below 50-day | 4 Nov, after US close (14.2%) | Qualcomm |
| Sandisk | 10% | 50 | 40 | Weak | below 50-day; oversold | 29 Oct, after US close, confirmed (11.4%) | Micron |
| Micron | 10% | 52 | 45 | Middling | below 50-day | December (after the game) | Sandisk |
| Datadog | 5% | 61 | 86 | Strong | none | 4 Nov, before US open (15%) | Cloudflare |
| Cash | 0% | | | | | | |

RESULTS TOTAL next 5 sessions 3.58 points across two reports (Sandisk 1.14, Palantir 2.44), next 10 sessions 9.38 points across five (deliberate: the stance needs variance). Themes: AI and chips 55%, Software 45%. Largest risk shares: Arm 26.6%, Shopify 17.0%, Palantir 15.8%. Worst scenario: a deeper AI sell-off, -7.1%; Fed hike with hawkish guidance -3.0%.

Points for the coming reviews:

- ServiceNow's exit signal on 26 Oct was borderline (close 0.23% below its open on 1.30 times average volume, upper part of the range, on an up day); its 28 Oct results will show whether the exit helped. The 23 Oct exits have cost 0.49 points so far.
- Sandisk reports Thu 29 Oct after the close (10%, 1.14 points at its implied move). Palantir Mon 2 Nov; Shopify Tue 3 Nov before the open (the order to hold or exit must go in before 08:00 UK Mon 2 Nov); Arm and Datadog Wed 4 Nov.
- Coinbase and any crypto-linked buy wait for Bitcoin's trend to turn up and IBIT to close above its 20-day.
- Sold holdings stay listed for the standstill test: Coca-Cola, Exxon Mobil, Shell, Microsoft, Eli Lilly, Chevron, AbbVie to Thu 29 Oct; AMD, Shopify (now bought back), Datadog (bought back) to Fri 30 Oct; ServiceNow, Robinhood, Strategy to Mon 2 Nov. Hasbro stays as a drift row to settle.

## 3. Pending order

**Changed for Tue 27 Oct's open (Monday 26 Oct evening review; message sent about 21:34 UK).** Palantir 20, Nvidia 20, Shopify 20, Arm Holdings 15, Sandisk 10, Micron 10, Datadog 5, cash 0. Seen entered: Tim's FT page showed "Pending reweight" at 22:52 UK.

## 4. Watchlist

31 names (the cap of 25 is lifted until Fri 30 Oct for the standstill test). Scores and bands at the Mon 26 Oct close.

| Name | Band | Status | Score | Note |
|---|---|---|---|---|
| Exxon Mobil | Strong | Watching (sold 22 Oct) | 87 | Kept to 29 Oct; not to be re-bought under the stance |
| Charles River Laboratories | Strong | Needs follow-through | 83 | Extended |
| ConocoPhillips | Strong | Watching | 81 | Fits neither order |
| Cloudflare | Strong | Watching | 77 | Datadog's swap; results 5 Nov |
| Valero Energy | Strong | Watching | 76 | Drift FAIL 22 Oct |
| Phillips 66 | Strong | Results ahead | 76 | 28 Oct, before US open |
| AbbVie | Strong | Watching (sold 22 Oct) | 76 | Kept to 29 Oct |
| NetApp | Strong | Watching | 76 | Tech |
| Chevron | Strong | Watching (sold 22 Oct) | 75 | Kept to 29 Oct |
| Marathon Petroleum | Strong | Watching | 75 | Fits neither order |
| Fortinet | Strong | Watching (added 26 Oct) | 75 | Broad scan leader; correlation 0.63 with Datadog |
| Eli Lilly | Strong | Watching (sold 22 Oct) | 74 | Kept to 29 Oct |
| Shell | Strong | Watching (sold 22 Oct) | 73 | Kept to 29 Oct |
| Microsoft | Strong | Watching (sold 22 Oct) | 71 | Results 28 Oct |
| Targa Resources | Strong | Watching | 71 | Fits neither order |
| Humana | Strong | Ready | 70 | Fits neither order |
| BP | Strong | Watching | 70 | Fits neither order |
| Hasbro | Strong | Watching (drift row) | 70 | Drift row settles 27 Oct |
| Coca-Cola | Strong | Watching (sold 22 Oct) | 69 | Results 27 Oct before open |
| Palo Alto Networks | Strong | Watching (added 26 Oct) | 69 | Broad scan leader; panel member |
| Analog Devices | Strong | Watching (added 26 Oct) | 69 | Broad scan leader; correlation 0.67 with Arm |
| CrowdStrike | Strong | Watching (added 26 Oct) | 68 | Broad scan leader |
| Centene | Middling | Watching | 59 | Results 28 Oct (est.) |
| AMD | Middling | Watching (sold 23 Oct) | 59 | Kept to 30 Oct; Nvidia's swap; results 3 Nov |
| ServiceNow | Middling | Exit signal (sold for 27 Oct) | 59 | Kept to 2 Nov; results 28 Oct |
| TSMC | Middling | Watching | 57 | First order stock |
| Seagate | Middling | Results ahead | 46 | 27 Oct after close |
| Western Digital | Middling | Watching | 45 | Memory swap |
| Strategy (crypto tracker) | Weak | Exit signal (sold for 27 Oct) | 41 | Tracker, stays |
| Robinhood | Weak | Exit signal (sold for 27 Oct) | 31 | Kept to 2 Nov; results 27 Oct |
| Coinbase (crypto tracker) | Weak | Watching | 28 | Tracker; results 29 Oct |

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
| Mon 26 Oct, about 21:34 UK (message sent) | Tue 27 Oct | Sell ServiceNow 20, Robinhood 10, Strategy 5; add Shopify 20, Micron 10, Datadog 5 | Rule exits: ServiceNow's heavy-volume close below its open (endgame exit rule), swap Shopify; IBIT closed below its 50-day (crypto exit rule), swap Coinbase barred while Bitcoin's trend is not up, so Micron (order A's memory lead) and Datadog (score 86). Expected 0.0 points |

## 6. Review log (newest first, keep the latest 15)

- Mon 26 Oct 2026 (about 23:25): Hand-run session with Tim ("Anything else?", then "Do it now"). Issue check first: every run today finished; one open ISSUE (non-US yields, below). Tim gave the FT figures for the 26 Oct close (100,973, rank 3,994 of 14,736; RECONCILE +94 credits against the estimate) and a player at rank 330 at +8.14%; the 27 Oct order shows as entered. Playbook 6.14.1 and feed 1.2 (`feed/feed.py`): the five non-US 10-year yields from CNBC's quote service (Japan: the Ministry of Finance's file first, else CNBC's previous close once Tokyo has moved on), in `feed/latest.json` `macro.intl_yields` and `feed/live.json`; tested with two forced feed runs (all five dated 26 Oct; stooq refused GitHub and was dropped); 170 tests pass. Docs: core, data doc (F, G8), evening, refresh and morning run docs. ISSUE: fixed.
- Mon 26 Oct 2026 (about 21:45): Evening review, a change evening for Tue 27 Oct (ServiceNow, Robinhood, Strategy out on rule exits; Shopify 20, Micron 10, Datadog 5 in). Pipeline 7.8 ran from commit `9760163`, hash matched; Fri 23 to Mon 26 Oct logged: Mon +1.22% against SPY +0.71%, value 100,879. Price feed: used (current, every row and quote from it; second forced run for the intake tickers). Broad scan: current (0 Events, 30 Leaders). Intake: Fortinet, CrowdStrike, Palo Alto Networks, Analog Devices added from the scan; no removals. No drift reporters on 26 Oct (no list stock reported; scan had no Events). Commodities from the futures fallback. Files published; the delete of the old data assets was refused by the permission check (harmless leftovers). Order message sent about 21:34 UK.
- ISSUE (26 Oct evening review; fixed at about 23:20 UK the same night, playbook 6.14.1, feed 1.2): non-US 10-year yields (UK, German, French, Italian, Japanese) not refreshed: the tradingeconomics page reached through a search gave no figure dated 26 Oct (its only date was 23 Oct), so the stored figures from 22 and 23 Oct were carried. No effect on the order.
- Mon 26 Oct 2026 (about 17:15): Hand-run session with Tim ("What's next to implement/improve? Work on it all now"). Issue check first: the repository's data check had been red every run since 22 Oct on a false failure ("2026-10-22: no contribution row for Hasbro", the Hasbro order replaced before it filled) and nobody was told; fixed and green (ISSUE: fixed). The morning check of 26 Oct ran 55 seconds, probably the same script refusal (covered by 6.13.2). Playbook 6.14: cut-off 08:00 UK (approved 21 Oct, never deployed until now), pipeline 7.8 from commit `9760163` (asset `e3ca0a59...`), page bar 08:00, nightly watchdog 22:47 UK. Morning check task moved to 07:26 UK with an 08:00 prompt at 18:03 UK at Tim's request (the first attempt that afternoon was refused by the permission check). Order unchanged.
- Sun 25 Oct 2026 (about 21:50): Evening review, FAULT. Script hash matched part B, but running it was refused by the session's permission check (the third run in a row), so no template, feed, scores, drift scan, intake, day call or ledger rows; nothing published; GitHub data unchanged. Order in force for Mon 26 Oct confirmed by hand and stood. Fault message sent about 21:45 UK.
- Sun 25 Oct 2026 (about 20:30): Weekend news check (Sunday). No A item. B: Houthi missiles and drones at Saudi Arabia; Saudi TASI -2.65% on Sunday; Trump: "There will not be a strike today", none before the 3 Nov midterms. C: Bitcoin -0.9% since Friday's close (about -0.17 points). Weekend Wall Street -0.06%. Script refused; state doc Weekend log updated only.
- Sat 24 Oct 2026 (about 20:30): Weekend news check (Saturday). No A item. B: possible US strike on Iran this weekend. C: Bitcoin -0.6% since Friday's close; Canada tariff shuffle. Script refused; state doc Weekend log updated only.
- Sat 24 Oct 2026 (about 09:35): Weekly review. Fri 23 Oct logged from the price feed; commodities from the futures fallback; gilt from the tradingeconomics news stream; other non-US yields not read. Week -1.74% against SPY -0.43%; game -0.33% against -2.10%. Post-mortems written for AMD, Datadog, Shopify. Files published; two old data assets could not be deleted (permission refused). Broad scan read: current.
- Thu 22 Oct 2026 (about 21:45): Evening review, a change evening for Fri 23 Oct (rule exits of AMD, Shopify and Datadog; Nvidia 20; ServiceNow, Palantir and Arm raised). Day -1.75% against SPY -1.18% on a Nasdaq -2.6% AI sell-off. Drift scan: Valero, Procter & Gamble, Meta all FAIL. Watchlist: added Nvidia, Cloudflare; removed Analog Devices, Meta. Price feed and broad scan: forced. Files published.
- Wed 21 Oct 2026 (about 23:12): Tim relayed FT Customer Care's answer: the order cut-off stays 08:00 UK local time all year.
- Wed 21 Oct 2026 (about 23:02): Tim sent the top 2% line (rank 274, +7.46%); stored; gap maths re-run.
- Wed 21 Oct 2026 (about 22:58): Tim confirmed order B entered and gave the FT figures (101,342, rank 3,948 of 14,357); RECONCILE -36 credits.
- Wed 21 Oct 2026 (about 22:55): Hand-run session with Tim: ten new stocks added from the feed, results events with implied moves, order B for Thu 22 Oct (message 22:50 UK).
- Wed 21 Oct 2026 (about 22:50): Hand-run session with Tim. Playbook 6.13: the endgame stance (core part D).
- Wed 21 Oct 2026 (about 22:30): Tim's answers recorded (Marsh & McLennan stays in the panel; PRs #3 and #5 merged). Research checks on PR #7, not deployed.
- Wed 21 Oct 2026 (about 22:10): Feed 1.1 and playbook 6.12.1; review re-run with Analog Devices added.

## 7. Market regime notes

Label: Mixed (an AI rebound on Monday after two weekly losses, led by chips on Anthropic's listing filing; the Fed meets 27 and 28 Oct with a hawkish hold expected; the 10-year at 5.00%; Brent above $110; Bitcoin below its 50-day trend).

Mon 26 Oct: S&P 500 +0.70% (7,676.8), Nasdaq +0.82% (26,169.4), Dow +0.28% (52,361.5), Russell 2000 +0.4%; VIX 18.39 (-5.5%). Anthropic filed publicly to list on the Nasdaq (ticker ANT); chips rose (Arm +6.2%, Micron +3.0%, Nvidia +2.4%, AMD +2.8%). Tesla +6% on a Barclays upgrade; EQT to buy Range Resources; Brazilian stocks fell sharply after the presidential runoff (XP about -50%, Nu about -20%); Meta plans to raise about $95bn in stock; Microsoft offering voluntary buyouts to about 60,000 staff. Oil eased on US-Iran hopes after a Saudi defence minister visited Tehran. Fed: hold about 88% priced (CME FedWatch via Kiplinger); a December hike is the market's base case.

Fri 23 Oct: S&P 500 -0.52% (7,623.68), Nasdaq -0.21%, Dow -1.23%; cybersecurity rallied; Brent at a six-month high. Thu 22 Oct: S&P 500 -1.21%, Nasdaq -2.60%. Week to Fri 23 Oct: S&P 500 -0.43% (SPY). Week to Fri 16 Oct: S&P 500 -1.95%, Nasdaq -4.48%.

Weekend log (weekend of 24 and 25 Oct): no A item on either day. B: Iran (Trump: no strike before the 3 Nov midterms) and Houthi attacks on Saudi Arabia (TASI -2.65% on Sunday). C: Bitcoin -0.6% (Sat) and -0.9% (Sun) from Friday's close. Weekend Wall Street about -0.05%. Ledger alerts not written either day (script refused). Monday's open took none of it badly: S&P 500 +0.70%.
Weekend of 17 and 18 Oct: no A item. B: Hormuz; Russia sanctions waiver.

Near calendar (the full calendar to 27 Nov is on the page and in the ledger):
- Tue 27 Oct: Robinhood and Seagate results (after the close); Coca-Cola (before the open); Visa. Durable goods (13:30 UK), Conference Board consumer confidence and new home sales (15:00 UK). Fed meeting day 1. US session 13:30 to 20:00 UK this week.
- Wed 28 Oct: Fed decision 18:00 UK, Warsh press conference 18:30 UK; ServiceNow and Microsoft (after the close); Phillips 66 (before the open); trade balance.
- Thu 29 Oct: Sandisk and Strategy (after the close); Shell; Eli Lilly; Coinbase; Mastercard. Q3 GDP, September PCE and core PCE, jobless claims (12:30 UK).
- Fri 30 Oct: Exxon Mobil, Chevron, AbbVie. Employment cost index, Chicago PMI.
- Mon 2 Nov: Palantir. Tue 3 Nov: Shopify (before the open), AMD; US midterms. Wed 4 Nov: Arm, Datadog (before the open). Thu 5 Nov: Cloudflare. Wed 18 Nov (est.): Nvidia.

## 8. Open questions for Tim

Answered: an order entered before 08:00 UK counted for that day up to 23 Oct; the midday check stays off; the leaderboard shows only the top 10; Shell filled at its 08:00 open on 9 Oct; Microsoft, Coca-Cola, Palantir, Goldman Sachs, Meta Platforms and Eli Lilly are in the game's list; the orders for 13 to 16 Oct were entered; GitHub access from scheduled runs; the cut-off after the clock change (FT Customer Care, 21 Oct: 08:00 UK local time all year; runs moved back to it in playbook 6.14); the fetch tool refusing built addresses (answered by the price feed); Marsh & McLennan stays in the panel; order B entered (21 Oct, 22:55 UK).

Still open:
1. Are Nvidia, Shopify, Arm, Sandisk, Micron and Datadog in the game's list? Assumed yes (large Nasdaq listings; Nvidia was in the first order; Shopify, Arm, Sandisk and Datadog in order B).
2. How a mixed London and US order entered for 26 Nov fills: Tim to ask FT help.
3. Does the game convert US stocks' returns into pounds? The closing gap has stayed under 0.05%.
4. Whether the 23 Oct order was entered as sent (the 26 Oct FT figure is within 0.09% of the estimate, which suggests it was). Answered 26 Oct: FT figures for the 26 Oct close; the 27 Oct order entered.

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

- The high-beta book filled at the 22 Oct open into an AI sell-off (Nasdaq -2.6%): -1.75% on the day against SPY -1.18%, and -2.35 points against the old defensive book, which rose. Three holdings gave the exit signal on day one. Lesson: a one-way book doubles both the bad and the good days; one session says nothing about the stance, and the exit rule will churn a high-beta book on broad sell-off days, which is the price of keeping it. Sequel: on 26 Oct the same book rose 1.22% against SPY +0.71%.

**The rule exits of 23 Oct (AMD, Shopify, Datadog, sold after one session)**

- On the session after the sale Datadog rose 4.6% and AMD 1.7%, while Nvidia (AMD's swap) was flat; ServiceNow (Shopify's swap) rose 1.3% against Shopify's -0.1%. On 26 Oct Datadog rose another 3.9% and AMD 2.8% against Nvidia's 2.4%. The change has cost 0.49 points over two sessions against keeping order B. Lesson: an exit signal on a day when the whole sector sold off on volume is weaker evidence than one on a quiet day; judge it on its five-session row before changing the rule.

**The exits of 27 Oct (ServiceNow on a marginal signal; the crypto pair on IBIT's 50-day)**

- ServiceNow closed 0.23% below its open on exactly the 1.3 times volume threshold, on an up day, two days before results; Robinhood and Strategy left because IBIT closed 0.2% below its 50-day. Both are mechanical exits at the edge of their thresholds. Lesson to test: whether edge-of-threshold signals cost more than clear ones; the five-session row for 27 Oct will say.

## 11. Confidence ratings, shadow ratings, the panel test and the day call

- Confidence ratings (not calibrated): from about four fill dates; higher bands did better so far, but far too few to judge. Ratings for the order for 27 Oct: Datadog 61, Palantir 55, Shopify 54, Nvidia 52, Micron 52, Arm 50, Sandisk 50 (the case rests on variance, not picks; Datadog's leans on its score, which the panel test has not shown to rank stocks).
- Shadow ratings: 326 logged. Live: score 70 and above, 68 cases, 65% beat the index (+0.92 points); 60 to 69, 43 cases, 51% (-1.81); 45 to 59, 25 cases, 24% (-2.53); below 45, 26 cases, 73% (+1.88). Not ordered by score; few distinct dates. Judgement test: one date (full score -0.07, price points +0.04, judgement points -0.26): too few.
- Panel test: see section 1. Old backtest (hindsight) correlation +0.01.
- Drift record: Hasbro ENTER and Equifax FAIL (20 Oct); Elevance, AT&T, Netflix FAIL (21 Oct); Valero, Procter & Gamble, Meta FAIL (22 Oct). None settled yet. No reporters scanned on 26 Oct.
- Day call record (S&P 500): 6 right of 10.
- Broad scan record (scan/latest.md, 26 Oct): Leaders, 20 settled, 40% beat the index, mean excess -0.70 points close to close and -0.53 from the next open; Events, none settled; 59 rows open.

## 12. Tools

- Tim's page: https://claude.ai/artifact/8P8UwQsb4QsbZMsKNYKrUJ, pinned in his Claude sidebar, with tabs Today, Macro, Performance, Risk, Calendar and Log. It reads four data files (`stocks`, `ledger`, `history`, `macro`) and a fifth dataset, `logos`, that no run touches. The Order panel reads the latest alert whose `stock` is "Order"; its "Enter before" bar uses the 08:00 UK cut-off (07:00 from 18 to 26 Oct).
- Playbook docs (version 6.14): `claude/ft-game-playbook.md` (core, with the routing table), `claude/ft-game-rules.md`, `claude/ft-game-data.md`, and the run docs `claude/ft-game-run-evening.md`, `-morning`, `-refresh`, `-weekly`, `-weekend`.
- Panel file: `panel.json` on the same artifact, named by the document `store/panel`.
- Scripts: the pipeline (version 7.8 from 26 Oct; runs take it from the repository at the commit in data doc G1) and the screening script are assets on that artifact. Their ids and hashes are in part B of the playbook, the only place they are kept.
- Price feed (data doc G8): `feed/latest.json` and `feed/live.json` in the repository. From feed 1.2 (26 Oct, late evening) they also carry the UK, German, French, Italian and Japanese 10-year yields (`macro.intl_yields`, with source and time) and, live, the US 10-year. 26 Oct: the scheduled close run (generated 20:46 UTC) covered every list stock, SPY, the extra rows, the panel, US yields and coins; a forced run at 21:34 UTC added Fortinet, CrowdStrike, Palo Alto Networks (two years each) and Analog Devices. Nothing missing or refused.
- Pages reached through searches on 26 Oct: TheStreet and Yahoo Finance's live market pages (index closes, VIX, drivers), TradingKey (Arm), Kiplinger (week's calendar, FedWatch), Motley Fool (memory bear case). tradingeconomics' German bond page gave no figure dated 26 Oct. Commodities from `feed --futures yes`.
- Market data service: massive.com, free plan, on an account opened by Tim's father. The key is in the evening and weekly review tasks and is never written into this project's docs, the page data, alerts or messages. Not used on 26 Oct (the feed covered every price).
- Sources that did not work: CNBC article pages; Chartmill news pages; CNN article pages; Detroit News; Fortune's Bitcoin price page and Morningstar's Fed preview (fetch errors, 26 Oct); capital.com news pages. tradingeconomics' news pages carry no statistics table.
- Artifact leftovers: the deletes of old data assets were refused by the permission check on 24 Oct (`98e54fb763c6e44126cc66fa4a35f64e`, `aff39fd7453cd4385d3cda52f7a0d81e`) and on 26 Oct (`35c94361e87930f39b568ba631794c95`, `d7c7c7506edbff99e053e2ac356962f5`, `49268bf02547924685207f3bf12af412`, `935d70426e320bac747af3fb7812abce`, `4ae4e0bf4affb8d8ee3860ac2621b535`); no document names them, so they are harmless leftovers.
- GitHub mirror: private repository `timzwang/ft-game` (part B and G6).
- Two saved skills, `ft-game-playbook` and `stock-score`, load in scheduled runs; the project docs win where they differ.
