# FT Stock Picking Game: state and log

Last updated: Thu 29 Oct 2026, about 19:45 UK (session with Tim: issue scan; playbook 6.14.3, runs no longer delete superseded data assets; order unchanged). Before that, Wed 28 Oct 2026, about 21:40 UK (evening review, a quiet evening: no change for Thu 29 Oct; no exit signal on any holding; Sandisk held through its report on Thu 29 Oct after the close). Before that, Tue 27 Oct 2026, about 21:45 UK (evening review, a quiet evening; Tim's FT figures for the 26 Oct close stored under `reported`). Before that, Mon 26 Oct 2026, about 23:25 UK (hand-run session with Tim: playbook 6.14.1 and feed 1.2). Earlier entries: see the review log (section 6).

This doc is the narrative record for Tim's entry, "Seeking Beta". The procedure for every run is in `claude/ft-game-playbook.md` (the core doc) and the docs its routing table names. The numbers (prices, scores, daily performance, contributions, ratings and their outcomes, the full calendar, analyst changes, alerts, the panel test, the drift record) live in the data files behind Tim's page and the panel file, and are produced by the pipeline script; this doc carries the decisions and the reasons.

Messages: from 10 Oct Tim is sent a message only when there is something for him to enter or answer (playbook part I, "When Tim is told"), and always when there is an issue (part I, "Issues: flag and fix", from 26 Oct). Quiet runs update the page and this doc and send nothing.

Scheduled runs: evening review 21:30 UK Sun to Thu; morning check 07:26 UK Mon to Fri (from Tue 27 Oct; 06:36 from 18 to 26 Oct; playbook 6.14); price refresh 16:45 UK and late price refresh 19:22 UK Mon to Fri; results-day refresh 14:50 UK Mon to Fri (acts only on results days); weekly performance review Sat 09:12 UK; weekend news check Sat and Sun 20:20 UK; nightly watchdog 22:47 UK every day (from 26 Oct); midday check 12:40 UK Mon to Fri (switched off, see section 8).

**Cut-off: every order must be entered before 08:00 UK, UK local time all year (FT Customer Care to Tim, 21 Oct; Tim approved the move back the same night; playbook 6.14 and pipeline 7.8 from 26 Oct). 07:00 UK was used as a safety margin from 17 to 26 Oct.**

## 1. Status

- **Playbook version 6.14.3** (6.14.3, 29 Oct evening: runs no longer delete superseded data assets, data doc G5 step 4, after the permission check refused the delete five times from 24 to 29 Oct; G5 step 5 checks the store's size instead; 6.14.2, 27 Oct late evening: feed 1.2.1 takes Japan's 10-year from CNBC first; 6.14.1, 26 Oct late evening: the UK, German, French, Italian and Japanese 10-year yields from the price feed, tradingeconomics only as the fallback; 6.14, 26 Oct afternoon: cut-off 08:00 UK, pipeline 7.8 from commit `9760163`, nightly watchdog at 22:47 UK, data check false failure fixed; 6.13.2, 26 Oct: flag and fix every issue; 6.13.1, 26 Oct: the script run from the repository; 6.13, 21 Oct late evening: the endgame stance in core part D, approved by Tim at 22:38 UK: score floor, trend tests, downtrend replacement, 10% caps, results budget, volatility caps and theme guide suspended for the rest of the game; the book is high-beta technology; exits only on a heavy-volume close below the open or a report that gaps down beyond its options move and closes in the lower half; every exit replaced from the swap column; 6.12.1: feed 1.1; 6.12: the price feed on GitHub and pipeline 7.7; 6.11.1: the 26 Oct cut-off test removed; 6.11: pipeline 7.4 and `order_expected`; 6.10: pipeline 7.3 and the 1.0 budget for 27 to 30 Oct; 6.9 to 6.5: repository tasks, handoff log, standstill test; 6.4: after the outside audit, pipeline 7, 07:00 UK cut-off, score frozen; 6.3: the broad scan; 6.2: day call never moves cash; 6: split docs, panel test, drift scan). **Pipeline script version 7.8** (part B holds the asset id, the run commit and the hash). The 28 Oct evening review ran it from commit `9760163` (hash matched part B).
- **Estimated value at Wed 28 Oct close: 103,232, +3.23% since the start, against -0.51% for the S&P 500 fund (gap +3.74 points).** Wed 28 Oct +1.79% against SPY +0.34%: Sandisk +0.77 points, Arm +0.62, Micron +0.59, Shopify +0.29; Nvidia -0.24, Palantir -0.19, Datadog -0.04. Tue 27 Oct +0.54% against SPY +0.56%. Week of 19 Oct: -1.74% against SPY -0.43%.
- **Last FT figures: Mon 26 Oct close, 100,973 (+0.97%), rank 3,994 of 14,736 (top 27.1%; the top 2% is rank 294 or better).** Stored in the ledger on 27 Oct (`reported`, with top2_return_pct 8.14: a player at rank 330 stood at +8.14%, so the line is a little above that). RECONCILE: +94 credits (+0.09%) against the estimate. On the estimate the gap to the line is now at least about 4.9 points with 21 sessions left.
- **Standstill (28 Oct run):** change for 16 Oct +0.21, 19 Oct -0.42 (complete); 22 Oct (the endgame switch) +1.67, complete, expected 0.0; 23 Oct (rule exits) -2.12 after four sessions, expected 0.0; 27 Oct (rule exits) +1.59 after two sessions, expected 0.0. Week of 12 Oct +0.12; week of 19 Oct -3.17; week of 26 Oct +1.61 so far. Inception (14 sessions): -0.25 as entered, -1.42 fully invested. EXPECTED BENEFIT: one settled (22 Oct), expected 0.0, actual +1.67.
- **Panel test:** history verdict "no evidence" (average rank correlation +0.039, t +1.1, 58 dates; one-year strength the strongest part, t +1.9). Live: one date (+0.37), too few to judge. All 30 members up to date. The score is frozen.
- **Order in force for Thu 29 Oct's open (unchanged tonight):** Palantir 20, Nvidia 20, Shopify 20, Arm Holdings 15, Sandisk 10, Micron 10, Datadog 5, cash 0.
- Day call record (S&P 500): 8 right of 12. Wed 28 Oct: S&P 500 rose 0.28% (call was green 51%: right). Thu 29 Oct call: S&P 500 Green 54% against a usual 55%; portfolio Green 54% against a usual 56% (reviewer -2 for ServiceNow's and Alphabet's after-hours falls): both close to a coin flip.
- Macro at Wed 28 Oct: US 2-year 4.67% (-3bp), 10-year 5.05% (+6bp on the day, -8bp over five), 30-year 5.37%. UK 10-year 5.35% (flat), Germany 3.36%, France 4.92%, Italy 4.51%, Japan 2.83% (all from the feed; Japan is CNBC's previous close). Brent $110.44, WTI $101.94, natural gas $3.03, gold $4,081 (futures fallback). Backdrop label: neutral.
- Crypto: Bitcoin $81,502 at the US close (+1.0% on the day, -3.5% over five); trend **up**: IBIT 0.9% above its 50-day, 11.0% above its 200-day, but 1.4% below its 20-day, so no crypto-linked buy yet. No crypto-linked holding.
- Regime: mixed. Wed 28 Oct: Fed held at 3.75% to 4.00% by 10-2 (Cook and Hammack for a hike; "inflation remains elevated"); S&P 500 +0.28% to a record 7,743.98, Nasdaq +0.27% (26,549.85), Dow +0.19%, SOX +1.75% on SK Hynix's results (DRAM prices up nearly 30%, NAND about 25% in the quarter). After hours: Microsoft about +4% (beat), Alphabet about -8% (EPS miss, negative free cash flow on AI spending), ServiceNow about -16% (EPS miss, Q4 guide below consensus on longer sales cycles), KLA about +3%.

## 2. Current portfolio

The order in force for Thu 29 Oct's open. Scores and bands from the pipeline at the Wed 28 Oct close. Under the endgame stance (core part D) the score floor, trend tests, volatility caps, theme guide and results budget do not apply; the NOTE lines for them are expected.

| Stock | Weight | Confidence (not calibrated) | Score | Band | Flags | Next results (implied move) | Swap if missing or broken |
|---|---|---|---|---|---|---|---|
| Palantir | 20% | 55 | 62 | Strong | none | 2 Nov, after US close (12.2%) | ServiceNow |
| Nvidia | 20% | 52 | 35 | Weak | below 50-day | 18 Nov, after US close (est.; not yet checked) | AMD |
| Shopify | 20% | 54 | 61 | Strong | none | 3 Nov, before US open (14.6%) | ServiceNow |
| Arm Holdings | 15% | 50 | 51 | Middling | below 50-day | 4 Nov, after US close (14.2%) | Qualcomm |
| Sandisk | 10% | 50 | 51 | Middling | below 50-day | 29 Oct, after US close, confirmed (9.7%, earnings-watcher 27 Oct) | Micron |
| Micron | 10% | 52 | 63 | Strong | none | December (after the game) | Sandisk |
| Datadog | 5% | 61 | 76 | Strong | none | 4 Nov, before US open (15%) | Cloudflare |
| Cash | 0% | | | | | | |

RESULTS TOTAL next 5 sessions 9.21 points across five reports (Sandisk 0.97 against its 1.0 budget, Palantir 2.44, Shopify 2.92, Arm 2.13, Datadog 0.75): deliberate, the stance needs variance. Themes: AI and chips 55%, Software 45%. Largest risk shares: Arm 27.5%, Shopify 16.1%, Palantir 14.9%. Worst scenario: a deeper AI sell-off, -7.1%.

Points for the coming reviews:

- No holding gave the exit signal on 28 Oct: Nvidia closed 2.06% below its open on 0.90 times average volume, Datadog 0.51% below on 0.91 times, Palantir 0.10% below on 0.93 times (the rule needs heavy volume). Nvidia's score fell to 35 (weak); the downtrend replacement is suspended under the stance, and its rating of 52 stays as the AI leader of the one-way book. US DOJ inquiry into its Hugging Face acquisition reported 28 Oct.
- ServiceNow (sold for 27 Oct) fell about 16% after hours on a weak Q4 guide citing longer enterprise sales cycles: a read-across risk for Palantir, Shopify and Datadog (45%) at Thursday's open. No rule acts on a peer's report and the stance holds through.
- Sandisk reports Thu 29 Oct after the close (10%, 0.97 points at its 9.7% implied move), held through at full weight; its exit test is the report rule (gap down beyond 9.7% and a close in the lower half) on Fri 30 Oct, acted on by that evening's review for Mon 2 Nov.
- Shopify reports Tue 3 Nov before the open: the order to hold or exit must go in before 08:00 UK Mon 2 Nov (decided by the Sun 1 Nov evening review). Palantir Mon 2 Nov after the close; Arm Wed 4 Nov after the close; Datadog Wed 4 Nov before the open.
- Coinbase and any crypto-linked buy: Bitcoin's trend is up; the remaining test is IBIT closing above its 20-day (1.4% below on 28 Oct).
- Sold holdings stay listed for the standstill test: Coca-Cola, Exxon Mobil, Shell, Microsoft, Eli Lilly, Chevron, AbbVie to Thu 29 Oct; AMD to Fri 30 Oct; ServiceNow, Robinhood, Strategy to Mon 2 Nov.

## 3. Pending order

**No change for Thu 29 Oct's open (Wednesday 28 Oct evening review; no message).** The order for Tue 27 Oct (Monday 26 Oct evening review; message sent about 21:34 UK; seen entered on Tim's FT page at 22:52 UK) stays in force: Palantir 20, Nvidia 20, Shopify 20, Arm Holdings 15, Sandisk 10, Micron 10, Datadog 5, cash 0.

## 4. Watchlist

32 names (the cap of 25 is lifted until Fri 30 Oct for the standstill test). Scores and bands at the Wed 28 Oct close.

| Name | Band | Status | Score | Note |
|---|---|---|---|---|
| Exxon Mobil | Strong | Watching (sold 22 Oct) | 87 | Kept to 29 Oct; not to be re-bought under the stance; results 30 Oct |
| Eli Lilly | Strong | Watching (sold 22 Oct) | 81 | Kept to 29 Oct; results 29 Oct |
| AbbVie | Strong | Watching (sold 22 Oct) | 80 | Kept to 29 Oct; results 30 Oct |
| Labcorp | Strong | Drift: enter (not taken) (added 28 Oct) | 79 | Drift ENTER 28 Oct (beat and raise); health care barred by the stance; overbought |
| Shell | Strong | Watching (sold 22 Oct) | 78 | Kept to 29 Oct; results 29 Oct |
| AMD | Strong | Watching (sold 23 Oct) | 78 | Kept to 30 Oct; Nvidia's swap; results 3 Nov; correlation 0.77 with Arm |
| Chevron | Strong | Watching (sold 22 Oct) | 77 | Kept to 29 Oct; results 30 Oct |
| Johnson Controls | Strong | Drift: needs 2nd day | 73 | Drift WATCH 27 Oct; faded gap 28 Oct |
| Analog Devices | Strong | Watching | 72 | Broad scan leader; correlation 0.62 with Arm |
| Coca-Cola | Strong | Watching (sold 22 Oct) | 70 | Kept to 29 Oct |
| Texas Instruments | Strong | Watching | 69 | Broad scan leader; a swap for Arm, not an addition |
| NetApp | Strong | Watching | 68 | Tech |
| Microsoft | Strong | Watching (sold 22 Oct) | 65 | Beat 28 Oct, about +4% after hours |
| Illumina | Strong | Watching (added 28 Oct) | 65 | Broad scan Leader #1; extended; health care |
| CrowdStrike | Strong | Watching | 63 | Broad scan leader |
| TSMC | Strong | Watching | 62 | First order stock |
| Palo Alto Networks | Strong | Watching | 61 | Panel member |
| Seagate | Middling | Watching | 57 | Recovered 28 Oct (+7.9% from its open) |
| Cloudflare | Middling | Watching | 57 | Datadog's swap; results 5 Nov |
| Valero Energy | Middling | Watching | 56 | Drift row open to 29 Oct |
| Quanta Services | Middling | Watching (added 28 Oct) | 54 | Scan Event 28 Oct; results figures not verified |
| Flex | Middling | Watching | 53 | Drift FAIL 28 Oct on trend only (beat and raise, +11.6%) |
| Fortinet | Middling | Watching | 51 | Heavy-volume down day 28 Oct; fell after hours |
| Western Digital | Middling | Watching | 49 | Memory swap |
| ServiceNow | Middling | Watching (sold for 27 Oct) | 49 | Kept to 2 Nov; about -16% after hours on results |
| Strategy (crypto tracker) | Middling | Watching (sold for 27 Oct) | 46 | Tracker, stays; results 29 Oct |
| Aon | Weak | Watching (added 28 Oct) | 56 | Scan Event 28 Oct; downtrend flag |
| Pentair | Weak | Watching | 51 | Rotate out from 30 Oct |
| Coinbase (crypto tracker) | Weak | Watching | 38 | Tracker; results 29 Oct |
| Robinhood | Weak | Watching (sold for 27 Oct) | 35 | Kept to 2 Nov |
| Comfort Systems USA | Weak | Watching (added 28 Oct) | 34 | Scan Event 28 Oct; death cross 26 Oct; rotate out from 2 Nov |
| F5 | Weak | Watching | 29 | Rotate out from 30 Oct (fell 19.8% on 28 Oct) |

Removed 28 Oct (fit neither order under the endgame stance; not held in the last five sessions): Phillips 66 (reported 28 Oct, drift FAIL), Centene, Charles River Laboratories.

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

- Thu 29 Oct 2026 (about 19:45): Session with Tim ("Scan everything again and ensure that no issues will ever arise again"). Issue check: every FT game task's last run SUCCEEDED (results-day refresh fired 15:10 UK, 20 minutes after its 14:50 slot: the scheduler, inside the 30-minute limit); the old duplicate morning check and weekend news check are switched off; every repository workflow run green since 26 Oct 23:08 UK; feed and scan current; ledger and stocks published 19:26 UK. The one recurring issue: the permission check refusing the delete of a superseded data asset ("Irreversible Deletion") on 24, 26 and 28 Oct and twice on 29 Oct (15:15 UK, leftover `6ba7bd723d82aeda5a05459d5c046f1d`; 19:25 UK, retry worked). Fixed by playbook 6.14.3: runs no longer delete old data assets (store 30 MB of 1 GB, 63 of 5,000 files); G5 step 5 flags the store above 700 MB or 4,000 files. ISSUE: fixed. Order unchanged.
- Wed 28 Oct 2026 (about 21:40): Evening review, a quiet evening (no change for Thu 29 Oct; no holding gave an exit signal; ServiceNow's and Alphabet's after-hours falls noted for the software sleeve but no rule acts on a peer's report). Pipeline 7.8 from commit `9760163`, hash matched; 28 Oct logged: +1.79% against SPY +0.34%, value 103,232. Price feed: used (current; forced run at 21:33 UTC for the intake tickers, two years each, none short). Non-US yields from the feed (all five dated 28 Oct). Commodities from the futures fallback (tradingeconomics' English commodity page not found through a search). Broad scan: current (5 Events, 30 Leaders). Drift: Labcorp ENTER (not taken: health care barred by the stance), Flex FAIL (trend), Phillips 66 FAIL; Flex's and Phillips 66's 50-day, 200-day and 20-day volume worked out from stored closes. Intake: Labcorp, Quanta Services, Comfort Systems USA, Aon, Illumina; removed Phillips 66, Centene, Charles River Laboratories. Sandisk's implied move updated to 9.7% (earnings-watcher, 27 Oct). History WARNINGs for Flex (6 May 2026) and Centene (2 Jul 2025) are the known real moves checked on 27 Oct. Files published and the five superseded data assets deleted. Benzinga's ServiceNow page and two Investing.com pages were refused or rate limited (one Investing.com page read on retry). No message.
- Tue 27 Oct 2026 (about 21:45): Evening review, a quiet evening (no change for Wed 28 Oct; no holding gave an exit signal). Pipeline 7.8 from commit `9760163`, hash matched; 27 Oct logged: +0.54% against SPY +0.56%, value 101,419. Tim's 26 Oct FT figures stored under `reported` (RECONCILE +94 credits). Price feed: used. Non-US yields from the feed. Commodities from the futures fallback. Broad scan: current. Drift: Coca-Cola FAIL, Pentair FAIL, Johnson Controls WATCH. Intake: Texas Instruments, F5, Flex, Johnson Controls, Pentair; removed ConocoPhillips, Marathon Petroleum, Targa Resources, Humana, BP, Hasbro. Files published. No message.
- Mon 26 Oct 2026 (about 23:25): Hand-run session with Tim ("Anything else?", then "Do it now"). Issue check first: every run today finished; one open ISSUE (non-US yields, below). Tim gave the FT figures for the 26 Oct close (100,973, rank 3,994 of 14,736; RECONCILE +94 credits against the estimate) and a player at rank 330 at +8.14%; the 27 Oct order shows as entered. Playbook 6.14.1 and feed 1.2 (`feed/feed.py`): the five non-US 10-year yields from CNBC's quote service. ISSUE: fixed.
- Mon 26 Oct 2026 (about 21:45): Evening review, a change evening for Tue 27 Oct (ServiceNow, Robinhood, Strategy out on rule exits; Shopify 20, Micron 10, Datadog 5 in). Pipeline 7.8 ran from commit `9760163`, hash matched; Mon +1.22% against SPY +0.71%, value 100,879. Order message sent about 21:34 UK.
- ISSUE (26 Oct evening review; fixed at about 23:20 UK the same night, playbook 6.14.1, feed 1.2): non-US 10-year yields not refreshed (tradingeconomics page gave no figure dated 26 Oct). No effect on the order. Confirmed fixed on 27 and 28 Oct: all five came from the feed.
- Mon 26 Oct 2026 (about 17:15): Hand-run session with Tim. Issue check first: the repository's data check had been red every run since 22 Oct on a false failure (Hasbro); fixed and green (ISSUE: fixed). Playbook 6.14: cut-off 08:00 UK, pipeline 7.8 from commit `9760163`, page bar 08:00, nightly watchdog 22:47 UK. Morning check task moved to 07:26 UK at 18:03 UK at Tim's request. Order unchanged.
- Sun 25 Oct 2026 (about 21:50): Evening review, FAULT. Script hash matched part B, but running it was refused by the session's permission check (the third run in a row); nothing published. Order in force for Mon 26 Oct stood. Fault message sent about 21:45 UK.
- Sun 25 Oct 2026 (about 20:30): Weekend news check (Sunday). No A item. B: Houthi attacks on Saudi Arabia; TASI -2.65%; Trump: no strike on Iran before the 3 Nov midterms. C: Bitcoin -0.9% since Friday's close. Script refused; Weekend log updated only.
- Sat 24 Oct 2026 (about 20:30): Weekend news check (Saturday). No A item. B: possible US strike on Iran. C: Bitcoin -0.6%. Script refused; Weekend log updated only.
- Sat 24 Oct 2026 (about 09:35): Weekly review. Week -1.74% against SPY -0.43%; game -0.33% against -2.10%. Post-mortems for AMD, Datadog, Shopify. Files published; two old data assets could not be deleted. Broad scan: current.
- Thu 22 Oct 2026 (about 21:45): Evening review, a change evening for Fri 23 Oct (rule exits of AMD, Shopify and Datadog; Nvidia 20; ServiceNow, Palantir and Arm raised). Day -1.75% against SPY -1.18%. Drift: Valero, Procter & Gamble, Meta all FAIL.
- Wed 21 Oct 2026 (about 23:12): Tim relayed FT Customer Care's answer: the order cut-off stays 08:00 UK local time all year.
- Wed 21 Oct 2026 (about 23:02): Tim sent the top 2% line (rank 274, +7.46%); stored; gap maths re-run.
- Wed 21 Oct 2026 (about 22:58): Tim confirmed order B entered and gave the FT figures (101,342, rank 3,948 of 14,357); RECONCILE -36 credits.

## 7. Market regime notes

Label: Mixed (a hawkish Fed hold with two dissents for a hike; the S&P 500 at a record on chips; the 10-year back up to 5.05%; software hit after hours by ServiceNow and Alphabet; Brent near $110; Bitcoin's trend up, still below its 20-day).

Wed 28 Oct: S&P 500 +0.28% (7,743.98, a record), Nasdaq +0.27% (26,549.85), Dow +0.19% (52,475.10), SOX +1.75%. Fed held at 3.75% to 4.00%, 10-2 (Cook and Hammack for a 25bp hike); statement: economy "expanding at a strong pace", inflation "remains elevated"; Goldman Sachs Asset Management sees a December hike possible. Memory and AI hardware led: SK Hynix's US line +13% (DRAM prices up nearly 30% in the quarter), Vertiv +17%, Flex +11.6% (beat and raise), Sandisk +7.7%, Seagate +7.9% from its open after Tuesday's after-hours fall, Micron +5.9%, Oracle +10.6%. F5 -19.8%, Enphase -17%. After hours: Microsoft about +4% (EPS $4.89 vs $4.72, revenue $92.28bn vs $90.61bn), KLA +3%, Alphabet about -8% (EPS $2.12 vs $3.02, negative free cash flow on AI spending), ServiceNow about -16% (EPS $1.00 vs $1.02, Q4 guide $4.25 to 4.26bn vs $4.36bn), Fortinet lower.

Tue 27 Oct: S&P 500 +0.60% (7,722.60), Nasdaq +1.18%; tech up on Anthropic's listing filing; Conference Board confidence 91.7 against about 81 expected. Mon 26 Oct: S&P 500 +0.70%. Fri 23 Oct: S&P 500 -0.52%. Thu 22 Oct: S&P 500 -1.21%, Nasdaq -2.60%. Week to Fri 23 Oct: S&P 500 -0.43% (SPY).

Weekend log (weekend of 24 and 25 Oct): no A item on either day. B: Iran (Trump: no strike before the 3 Nov midterms) and Houthi attacks on Saudi Arabia (TASI -2.65% on Sunday). C: Bitcoin -0.6% (Sat) and -0.9% (Sun) from Friday's close. Monday's open took none of it badly: S&P 500 +0.70%.
Weekend of 17 and 18 Oct: no A item. B: Hormuz; Russia sanctions waiver.

Near calendar (the full calendar to 27 Nov is on the page and in the ledger):
- Thu 29 Oct: Shell (07:00 UK); Eli Lilly and Mastercard (11:30 UK); Q3 GDP (advance), September PCE and core PCE, jobless claims (12:30 UK); Sandisk (after the close, about 20:05 UK; implied 9.7%), Coinbase, Strategy (after the close). US session 13:30 to 20:00 UK this week.
- Fri 30 Oct: Exxon Mobil, Chevron, AbbVie (before the open); BP (07:00 UK). Employment cost index, Chicago PMI.
- Mon 2 Nov: Palantir (after the close); US session back to 14:30 to 21:00 UK. Tue 3 Nov: Shopify (before the open; order before 08:00 UK Mon 2 Nov), AMD; US midterms. Wed 4 Nov: Datadog (before the open), Arm (after the close). Thu 5 Nov: Cloudflare. Wed 18 Nov (est.): Nvidia.

## 8. Open questions for Tim

Answered: an order entered before 08:00 UK counted for that day up to 23 Oct; the midday check stays off; the leaderboard shows only the top 10; Shell filled at its 08:00 open on 9 Oct; Microsoft, Coca-Cola, Palantir, Goldman Sachs, Meta Platforms and Eli Lilly are in the game's list; the orders for 13 to 16 Oct were entered; GitHub access from scheduled runs; the cut-off after the clock change (08:00 UK local time all year); the fetch tool refusing built addresses (answered by the price feed); Marsh & McLennan stays in the panel; order B entered (21 Oct, 22:55 UK); whether the 23 Oct order was entered as sent (26 Oct FT figure within 0.09% of the estimate); the 27 Oct order entered (26 Oct, 22:52 UK).

Still open:
1. Are Nvidia, Shopify, Arm, Sandisk, Micron and Datadog in the game's list? Assumed yes (large Nasdaq listings; the 27 Oct order showed as a pending reweight on the FT page).
2. How a mixed London and US order entered for 26 Nov fills: Tim to ask FT help.
3. Does the game convert US stocks' returns into pounds? The closing gap has stayed under 0.1%.

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

- The order was replaced by the endgame switch before it filled; Hasbro closed at 117.23 on 22 Oct (open 113.85). Its drift row settled on 27 Oct (the ENTER record: one settled, +7.51 points against the index).

**The endgame switch, 22 Oct (first session of a one-way book)**

- The high-beta book filled at the 22 Oct open into an AI sell-off (Nasdaq -2.6%): -1.75% on the day against SPY -1.18%. Three holdings gave the exit signal on day one. Lesson: a one-way book doubles both the bad and the good days; one session says nothing about the stance. Sequel: the switch's five-session row completed on 28 Oct at +1.67 points against the old defensive book.

**The rule exits of 23 Oct (AMD, Shopify, Datadog, sold after one session)**

- On the session after the sale Datadog rose 4.6% and AMD 1.7%, while Nvidia (AMD's swap) was flat. On 27 Oct AMD rose another 5.5% against Nvidia's 0.9%. After four sessions the change has cost 2.12 points against keeping order B. Lesson: an exit signal on a day when the whole sector sold off on volume is weaker evidence than one on a quiet day; judge it on its five-session row before changing the rule.

**The exits of 27 Oct (ServiceNow on a marginal signal; the crypto pair on IBIT's 50-day)**

- ServiceNow closed 0.23% below its open on exactly the 1.3 times volume threshold, on an up day, two days before results; Robinhood and Strategy left because IBIT closed 0.2% below its 50-day. After two sessions the change stands +1.59 points, and ServiceNow then fell about 16% after hours on its 28 Oct report. Lesson to test: whether edge-of-threshold signals cost more than clear ones; the five-session row for 27 Oct will say.

**Coca-Cola, 27 Oct (a beat and raise that fell)**

- Comparable EPS $0.91 against $0.88, revenue $13.4bn against $12.93bn, guidance raised for the third time, and the stock fell 1.6% on the day: drift FAIL. Lesson: in a growth rebound, a defensive beat-and-raise does not draw buyers; the reaction test exists for this.

## 11. Confidence ratings, shadow ratings, the panel test and the day call

- Confidence ratings (not calibrated): nine more settled on 28 Oct; still too few distinct dates to judge. Ratings for the order in force: Datadog 61, Palantir 55, Shopify 54, Nvidia 52, Micron 52, Arm 50, Sandisk 50 (the case rests on variance, not picks).
- Shadow ratings: 406 logged. Live: score 70 and above, 91 cases, 63% beat the index (+0.74 points); 60 to 69, 66 cases, 48% (-1.33); 45 to 59, 35 cases, 31% (-2.49); below 45, 32 cases, 72% (+1.53). Not ordered by score; few distinct dates. Judgement test: one date (full score -0.07, price points +0.04, judgement points -0.26): too few.
- Panel test: see section 1. Old backtest (hindsight) correlation +0.011.
- Drift record: ENTER 1 settled (Hasbro, +7.51 points against the index), 1 open (Labcorp, 28 Oct, not taken); WATCH Johnson Controls (27 Oct) open; FAIL 4 settled (25% beat the index, -4.30 points); FAIL rows open include Valero, Procter & Gamble, Meta (22 Oct), Coca-Cola, Pentair (27 Oct), Flex, Phillips 66 (28 Oct).
- Day call record (S&P 500): 8 right of 12.
- Broad scan record (scan/latest.md, 28 Oct): Leaders, 40 settled, 38% beat the index, mean excess -2.12 points close to close and -2.13 from the next open; Events, 4 settled, 50%, +1.35 and +1.54; 63 rows open.

## 12. Tools

- Tim's page: https://claude.ai/artifact/8P8UwQsb4QsbZMsKNYKrUJ, pinned in his Claude sidebar, with tabs Today, Macro, Performance, Risk, Calendar and Log. It reads four data files (`stocks`, `ledger`, `history`, `macro`) and a fifth dataset, `logos`, that no run touches. The Order panel reads the latest alert whose `stock` is "Order"; its "Enter before" bar uses the 08:00 UK cut-off.
- Playbook docs (version 6.14.3): `claude/ft-game-playbook.md` (core, with the routing table), `claude/ft-game-rules.md`, `claude/ft-game-data.md`, and the run docs `claude/ft-game-run-evening.md`, `-morning`, `-refresh`, `-weekly`, `-weekend`.
- Panel file: `panel.json` on the same artifact, named by the document `store/panel`.
- Scripts: the pipeline (version 7.8; runs take it from the repository at the commit in data doc G1) and the screening script are assets on that artifact. Their ids and hashes are in part B of the playbook, the only place they are kept.
- Price feed (data doc G8): `feed/latest.json` and `feed/live.json` in the repository, with the non-US 10-year yields under `macro.intl_yields`. 28 Oct: the scheduled close run (generated 20:52 UTC) covered every list stock, SPY, the extra rows, the panel, US and non-US yields and coins; a forced run at 21:33 UTC added Labcorp, Quanta Services, Comfort Systems USA, Aon and Illumina (two years each). Nothing missing or refused.
- Pages reached through searches on 28 Oct: tradingkey (index closes, SK Hynix, Fed), Stock Titan (Fed details, movers), Investing.com (after-hours movers), finchannel (ServiceNow), StockStory via FinancialContent (Flex), 24/7 Wall St (Labcorp), BOE Report (Phillips 66), earnings-watcher (Sandisk). Benzinga's ServiceNow page failed (client error); two Investing.com pages were rate limited (one read on retry; the Quanta preview not read). tradingeconomics' English commodity page did not come up in a search; commodities from `feed --futures yes`.
- Market data service: massive.com, free plan, on an account opened by Tim's father. The key is in the evening and weekly review tasks and is never written into this project's docs, the page data, alerts or messages. Not used on 28 Oct (the feed covered every price).
- Sources that did not work: Benzinga article pages (28 Oct); CNBC article pages; gurufocus news pages and EBC (fetch errors, 27 Oct); Chartmill news pages; CNN article pages; Detroit News; Fortune's Bitcoin price page and Morningstar's Fed preview (fetch errors, 26 Oct); capital.com news pages. tradingeconomics' news pages carry no statistics table.
- Artifact leftovers: the deletes of old data assets were refused by the permission check on 24 Oct (`98e54fb763c6e44126cc66fa4a35f64e`, `aff39fd7453cd4385d3cda52f7a0d81e`) and on 26 Oct (`35c94361e87930f39b568ba631794c95`, `d7c7c7506edbff99e053e2ac356962f5`, `49268bf02547924685207f3bf12af412`, `935d70426e320bac747af3fb7812abce`, `4ae4e0bf4affb8d8ee3860ac2621b535`); no document names them, so they are harmless leftovers. On 27 and 28 Oct the five superseded data assets were deleted without refusal; on 29 Oct the delete was refused at 15:15 UK (`6ba7bd723d82aeda5a05459d5c046f1d` left) and once at 19:25 UK (the retry worked). From playbook 6.14.3 runs no longer delete superseded data assets (data doc G5 step 4), so they accumulate as expected leftovers; 29 Oct: 30 MB of 1 GB used.
- GitHub mirror: private repository `timzwang/ft-game` (part B and G6).
- Two saved skills, `ft-game-playbook` and `stock-score`, load in scheduled runs; the project docs win where they differ.
