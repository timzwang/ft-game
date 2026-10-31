# FT Stock Picking Game: state and log

Last updated: Sat 31 Oct 2026, about 09:30 UK (weekly review: Fri 30 Oct logged, -7.14%; order unchanged). Before that, Thu 29 Oct 2026, about 21:45 UK (evening review, a change evening: Datadog out on the endgame exit rule, Cloudflare in at 5% for Fri 30 Oct's open; order message sent about 21:34 UK). Before that, Thu 29 Oct 2026, about 19:45 UK (session with Tim: issue scan; playbook 6.14.3, runs no longer delete superseded data assets; order unchanged). Before that, Wed 28 Oct 2026, about 21:40 UK (evening review, a quiet evening). Earlier entries: see the review log (section 6).

This doc is the narrative record for Tim's entry, "Seeking Beta". The procedure for every run is in `claude/ft-game-playbook.md` (the core doc) and the docs its routing table names. The numbers (prices, scores, daily performance, contributions, ratings and their outcomes, the full calendar, analyst changes, alerts, the panel test, the drift record) live in the data files behind Tim's page and the panel file, and are produced by the pipeline script; this doc carries the decisions and the reasons.

Messages: from 10 Oct Tim is sent a message only when there is something for him to enter or answer (playbook part I, "When Tim is told"), and always when there is an issue (part I, "Issues: flag and fix", from 26 Oct). Quiet runs update the page and this doc and send nothing.

Scheduled runs: evening review 21:30 UK Sun to Thu; morning check 07:26 UK Mon to Fri (from Tue 27 Oct; 06:36 from 18 to 26 Oct; playbook 6.14); price refresh 16:45 UK and late price refresh 19:22 UK Mon to Fri; results-day refresh 14:50 UK Mon to Fri (acts only on results days); weekly performance review Sat 09:12 UK; weekend news check Sat and Sun 20:20 UK; nightly watchdog 22:47 UK every day (from 26 Oct); midday check 12:40 UK Mon to Fri (switched off, see section 8).

**Cut-off: every order must be entered before 08:00 UK, UK local time all year (FT Customer Care to Tim, 21 Oct; Tim approved the move back the same night; playbook 6.14 and pipeline 7.8 from 26 Oct). 07:00 UK was used as a safety margin from 17 to 26 Oct.**

## 1. Status

- **Playbook version 6.14.3** (6.14.3, 29 Oct evening: runs no longer delete superseded data assets, data doc G5 step 4; G5 step 5 checks the store's size instead; 6.14.2, 27 Oct: feed 1.2.1 takes Japan's 10-year from CNBC first; 6.14.1, 26 Oct: the five non-US 10-year yields from the price feed; 6.14, 26 Oct: cut-off 08:00 UK, pipeline 7.8 from commit `9760163`, nightly watchdog 22:47 UK; 6.13.2: flag and fix every issue; 6.13.1: the script run from the repository; 6.13, 21 Oct: the endgame stance in core part D (score floor, trend tests, downtrend replacement, 10% caps, results budget, volatility caps and theme guide suspended; the book is high-beta technology; exits only on a heavy-volume close below the open or a report that gaps down beyond its options move and closes in the lower half; every exit replaced from the swap column); earlier versions in the playbook header). **Pipeline script version 7.8** (part B holds the asset id, the run commit and the hash). The 31 Oct weekly review ran it from commit `9760163` (hash matched part B).
- **Estimated value at Fri 30 Oct close: 93,877, -6.12% since the start, against -2.64% for the S&P 500 fund (gap -3.48 points).** Fri 30 Oct -7.14% against SPY -1.77%: Arm -1.50 points, Sandisk -1.35, Palantir -1.25, Shopify -1.13, Nvidia -0.84, Micron -0.53, Cloudflare -0.32, Datadog (sold at the open) -0.23. Week of 26 Oct: -5.81% against SPY -0.56%. Thu 29 Oct -2.07%; Wed 28 Oct +1.79%; Tue 27 Oct +0.54%; Mon 26 Oct +1.22%. Week of 19 Oct: -1.74% against SPY -0.43%.
- **Last FT figures: Mon 26 Oct close, 100,973 (+0.97%), rank 3,994 of 14,736 (top 27.1%; the top 2% is rank 294 or better).** `reported` row with top2_return_pct 8.14 (a player at rank 330). RECONCILE +94 credits (+0.09%). On the estimate the gap to the 26 Oct line is about 14 points with 19 sessions left (the line itself has probably moved since; not verified). New FT figures asked for in the 31 Oct weekly review.
- **Standstill (31 Oct weekly run):** change for 19 Oct -0.42, 22 Oct (endgame switch) +1.67, 23 Oct (rule exits) -4.20, all complete; 27 Oct (rule exits) +5.48 after four sessions; 30 Oct (Datadog to Cloudflare) +0.03 after one; both expected 0.0. Week of 12 Oct +0.12; week of 19 Oct -3.17; week of 26 Oct +5.58 (complete). Inception (16 sessions): -9.63 as entered, -10.82 fully invested (the first, energy and defence order would stand at +3.51%). EXPECTED BENEFIT: two settled, expected 0.0, actual -2.53, sign right in 1 of 2.
- **Panel test (31 Oct, all 30 members loaded, at least 511 closes each):** history verdict "no evidence" (average rank correlation +0.039, t +1.1, 58 dates; one-year strength the strongest part, t +1.9; two-month t +1.8). Live: two dates (-0.130), too few to judge. The score is frozen.
- **Order in force for Mon 2 Nov's open (unchanged since the 29 Oct evening review, which set it for Fri 30 Oct):** Palantir 20, Nvidia 20, Shopify 20, Arm Holdings 15, Sandisk 10, Micron 10, Cloudflare 5, cash 0. The Sun 1 Nov evening review decides Monday's order: five holdings (Shopify, Cloudflare, Arm, Sandisk, Nvidia) closed below their opens on heavy volume on 30 Oct.
- Day call record (S&P 500): 9 right of 14 against 7 for always saying green; Brier 0.245. Portfolio: 10 of 14 against 8; Brier 0.226. Fri 30 Oct: S&P 500 -1.77% (call red 48%: right); portfolio -7.14% (call red 41%: right). Mon 2 Nov: model S&P 500 green 59%, portfolio green 58%; the Sun 1 Nov review writes the cases.
- Macro at Fri 30 Oct: US 2-year 4.56% (-5bp; -13bp over five), 10-year 4.94% (-4bp; -6bp over five), 30-year 5.31%. UK 10-year 5.29% (flat; -4bp over five), Germany 3.32%, France 4.97% (+7bp), Italy 4.49%, Japan 2.78% (all from the feed). Brent $112.24, WTI $102.92, natural gas $2.88, gold $3,884 (-3.8%) (futures fallback; Brent's December contract expired 30 Oct, so the front month is uncertain). Backdrop label: neutral. Q3 employment cost index +0.8%, in line.
- Crypto: Bitcoin $76,715 at the US close (-5.0% on the day, -5.5% over five); trend **mixed** (IBIT 5.5% below its 50-day, 6.7% below its 20-day, 4.5% above its 200-day), so no crypto-linked buy. No crypto-linked holding.
- Regime: risk-off (label set by the 31 Oct weekly review). Fri 30 Oct: S&P 500 -1.83% (7,578.97), Nasdaq -2.84% (25,442.31), Dow -1.06% (TheStreet's close). Intel -29% (weak guide; its worst day since 1974), Reddit -29%, Amazon lower after EPS of $1.89 against $1.96 and a twelve-month free cash outflow of $42.4bn; Sandisk -13.5% after a beat and raise, on worries that memory prices are near a peak. Bitcoin -5%, gold -3.8%.

## 2. Current portfolio

The order for Fri 30 Oct's open. Scores and bands from the pipeline at the Thu 29 Oct close. Under the endgame stance (core part D) the score floor, trend tests, volatility caps, theme guide and results budget do not apply; the NOTE lines for them are expected.

| Stock | Weight | Confidence (not calibrated) | Score | Band | Flags | Next results (implied move) | Swap if missing or broken |
|---|---|---|---|---|---|---|---|
| Palantir | 20% | 55 | 64 | Strong | none | 2 Nov, after US close (12.2%) | ServiceNow |
| Nvidia | 20% | 52 | 37 | Weak | below 50-day | 18 Nov, after US close (est.; not yet checked) | AMD |
| Shopify | 20% | 54 | 60 | Strong | none | 3 Nov, before US open (14.6%) | ServiceNow |
| Arm Holdings | 15% | 50 | 49 | Middling | below 50-day | 4 Nov, after US close (14.2%) | Qualcomm |
| Sandisk | 10% | 50 | 45 | Middling | below 50-day | Reported 29 Oct after the close (9.7% implied); reaction session Fri 30 Oct | Micron |
| Micron | 10% | 52 | 44 | Weak | below 50-day | December (after the game) | Sandisk |
| Cloudflare | 5% | 52 | 56 | Middling | below 50-day | 5 Nov, after US close (13.9%, earnings-watcher 28 Oct) | Datadog |
| Cash | 0% | | | | | | |

RESULTS TOTAL next 5 sessions 8.18 points across four reports (Palantir 2.44, Shopify 2.92, Arm 2.13, Cloudflare 0.69): deliberate, the stance needs variance. Themes: AI and chips 55%, Software 45%. Largest risk shares: Arm 27.7%, Shopify 16.3%, Palantir 14.6%. Worst scenario: a deeper AI sell-off, -7.1%.

Points for the coming reviews:

- Datadog gave the exit signal on 29 Oct (close 1.38% below its open on 1.38 times its 20-day volume, a day the software sleeve sold off on ServiceNow's guide); replaced by its swap, Cloudflare, which gapped down but closed 1.9% above its open. Same pattern as the 23 Oct exits (a sector-wide down day): the 30 Oct change row will show whether that matters.
- Sandisk reported on 29 Oct after the close: revenue $11.03bn (+378%), non-GAAP EPS $49.51; Q2 guide revenue $12.2bn to 12.6bn, EPS $55 to 57; 8-for-1 split (split-adjusted trading from 20 Nov). Up about 2% to 3% after hours after a 5.3% fall in the session. Exit test on Fri 30 Oct: a gap down beyond 9.7% with a close in the lower half; acted on by the Sun 1 Nov review for Mon 2 Nov. Its drift entry is logged on Sunday (reaction session Fri 30 Oct).
- Shopify reports Tue 3 Nov before the open: the order to hold or exit must go in before 08:00 UK Mon 2 Nov (decided by the Sun 1 Nov evening review). Palantir Mon 2 Nov after the close; Arm Wed 4 Nov after the close; Cloudflare Thu 5 Nov after the close.
- Intel about -17.6% and Amazon about -6.7% after hours on 29 Oct: read-across risk for chips and AI spending at Friday's open. No rule acts on a peer's report.
- Bitcoin's trend has turned mixed (IBIT just below its 50-day): no crypto-linked buy.
- Sold holdings stay listed for the standstill test: AMD to Fri 30 Oct; ServiceNow, Robinhood, Strategy to Mon 2 Nov; Datadog to Fri 6 Nov.

## 3. Pending order

**Changed for Fri 30 Oct's open (Thursday 29 Oct evening review; message sent about 21:34 UK):** Palantir 20, Nvidia 20, Shopify 20, Arm Holdings 15, Sandisk 10, Micron 10, Cloudflare 5, cash 0. Change: Datadog 5 out (endgame exit rule), Cloudflare 5 in (swap column). Expected 0.0 points (`order_expected` recorded). Taken as entered unless Tim says otherwise.

## 4. Watchlist

32 names (the cap of 25 is lifted until Fri 30 Oct for the standstill test; the Fri 30 Oct review brings it back down). Scores and bands at the Thu 29 Oct close. No additions or removals tonight (reason in the review log).

| Name | Band | Status | Score | Note |
|---|---|---|---|---|
| Exxon Mobil | Strong | Watching (sold 22 Oct) | 84 | Five sessions done; not to be re-bought under the stance; results 30 Oct; can be removed from 30 Oct |
| Shell | Strong | Watching (sold 22 Oct) | 80 | Reported 29 Oct (beat, $5bn buyback): drift FAIL; can be removed from 30 Oct |
| Labcorp | Strong | Drift: enter (not taken) (added 28 Oct) | 80 | Health care barred by the stance; overbought |
| AbbVie | Strong | Watching (sold 22 Oct) | 79 | Results 30 Oct; can be removed from 30 Oct |
| Chevron | Strong | Watching (sold 22 Oct) | 77 | Results 30 Oct; can be removed from 30 Oct |
| Eli Lilly | Strong | Watching (sold 22 Oct) | 77 | Beat and raise 29 Oct, +6.4%: drift FAIL (beat and volume missing); health care barred |
| Johnson Controls | Strong | Drift: needs 2nd day | 77 | Drift WATCH 27 Oct |
| Analog Devices | Strong | Watching | 75 | Broad scan leader; correlation 0.61 with Arm |
| AMD | Strong | Watching (sold 23 Oct) | 73 | Kept to 30 Oct; Nvidia's swap; results 3 Nov; correlation 0.78 with Arm |
| Coca-Cola | Strong | Watching (sold 22 Oct) | 71 | Can be removed from 30 Oct |
| Datadog | Strong | Exit signal (sold for 30 Oct) | 69 | Kept to 6 Nov; results 4 Nov |
| Texas Instruments | Strong | Watching | 69 | Broad scan leader |
| Illumina | Strong | Watching (added 28 Oct) | 67 | Broad scan Leader #1; extended; health care |
| CrowdStrike | Strong | Watching | 66 | Broad scan leader |
| Microsoft | Strong | Watching (sold 22 Oct) | 64 | Beat 28 Oct; heavy-volume down day 29 Oct: drift FAIL |
| NetApp | Strong | Watching | 63 | Tech |
| Palo Alto Networks | Strong | Watching | 63 | Panel member |
| Quanta Services | Strong | Watching (added 28 Oct) | 63 | Power |
| Seagate | Middling | Watching | 59 | Memory |
| TSMC | Middling | Watching | 53 | First order stock |
| Valero Energy | Middling | Results ahead | 51 | Drift row open |
| Flex | Middling | Watching | 50 | Drift FAIL 28 Oct |
| Western Digital | Middling | Watching | 49 | Memory swap |
| Aon | Weak | Watching (added 28 Oct) | 54 | Downtrend flag; rotate out from 2 Nov |
| Pentair | Weak | Watching | 48 | Rotate out from 30 Oct |
| Robinhood | Weak | Watching (sold for 27 Oct) | 39 | Kept to 2 Nov |
| Fortinet | Weak | Watching | 38 | Reaction day 29 Oct (beat and raise, gapped down, closed near the high): drift FAIL; rotate out 30 Oct |
| Strategy (crypto tracker) | Weak | Watching (sold for 27 Oct) | 38 | Tracker, stays |
| Coinbase (crypto tracker) | Weak | Watching | 35 | Tracker |
| F5 | Weak | Watching | 35 | Rotate out from 30 Oct |
| Comfort Systems USA | Weak | Watching (added 28 Oct) | 30 | Rotate out from 2 Nov |
| ServiceNow | Weak | Watching (sold for 27 Oct) | 25 | Kept to 2 Nov; about -20% on 29 Oct after its guide: drift FAIL |

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
| Mon 26 Oct, about 21:34 UK (message sent) | Tue 27 Oct | Sell ServiceNow 20, Robinhood 10, Strategy 5; add Shopify 20, Micron 10, Datadog 5 | Rule exits: ServiceNow's heavy-volume close below its open, swap Shopify; IBIT closed below its 50-day (crypto exit rule), swap Coinbase barred, so Micron and Datadog. Expected 0.0 points |
| Thu 29 Oct, about 21:34 UK (message sent) | Fri 30 Oct | Sell Datadog 5; add Cloudflare 5 | Endgame exit rule: Datadog closed 1.38% below its open on 1.38 times average volume; swap Cloudflare (closed above its open). Expected 0.0 points |

## 6. Review log (newest first, keep the latest 15)

- Sat 31 Oct 2026 (about 09:30): Weekly review. Pipeline 7.8 from commit `9760163`, hash matched. Fri 30 Oct logged from the price feed (current, generated 20:51 UTC; every list stock, SPY, extra rows and all 30 panel closes): -7.14% against SPY -1.77%, value 93,877; week -5.81% against SPY -0.56%; game -6.12% against -2.64%. Non-US yields from the feed; commodities from the futures fallback. ECI stored (0.8%, in line; Seeking Alpha's page refused by robots, figure from Reuters via Idaho Business Review). WARNINGs for FLEX 2026-05-06 (+39.7%) and CNC 2025-07-02 (-40.4%) checked against the stored rows: genuine moves on heavy volume that held, not typos. Files published (store 44 MB, 78 files; no deletes). Order unchanged; message to Tim with the review and a request for FT figures. No ISSUE this run. The week's issues (26 Oct live yields; 27 Oct morning push 403; 28 and 29 Oct asset deletes refused; 29 Oct state doc path) are all fixed.
- Thu 29 Oct 2026 (about 21:45): Evening review, a change evening for Fri 30 Oct (Datadog out on the endgame exit rule, Cloudflare 5 in from the swap column). Pipeline 7.8 from commit `9760163`, hash matched; 29 Oct logged: -2.07% against SPY -0.38%, value 101,099. Order message sent about 21:34 UK. Price feed: used (current, generated 20:54 UTC; every list stock, SPY, extra rows and panel). Non-US yields from the feed (all five dated 29 Oct). Commodities from the futures fallback (tradingeconomics' commodity page not found through a search). Broad scan: current (10 Events, 30 Leaders). Drift: Microsoft, ServiceNow, Fortinet, Shell, Eli Lilly all FAIL (50-day, 200-day and 20-day volume worked out from stored rows; Lilly's volume missing). Intake: none tonight: the list is at 32 against the cap of 25 that returns on Fri 30 Oct, the scan's Events (Carvana, Norwegian Cruise, Huntington Ingalls, Textron and others) fall outside the stance's high-beta technology book, and its tech leaders are already listed. Removals deferred to Fri 30 Oct (Fortinet, Pentair, F5 and the sold names whose five sessions ended 29 Oct). Files published (store 34 MB, 66 files; no deletes, as G5 step 4 says). Pages refused: Alphastreet's Datadog page, Chartmill's and Rolling Out's Lilly pages (client errors).
- ISSUE (29 Oct evening review, about 21:40 UK; fixed): the first state doc write was refused, "project_write: local_path must be inside the working directory" (the local file was in a folder outside the session's working directory). Fixed by writing from the repository copy `state/ft-game-state.md`, which is inside it; no effect on the order or the page.
- Thu 29 Oct 2026 (about 19:45): Session with Tim ("Scan everything again and ensure that no issues will ever arise again"). Every FT game task's last run SUCCEEDED; every repository workflow green since 26 Oct 23:08 UK. The recurring issue (the permission check refusing the delete of superseded data assets on 24, 26, 28 and 29 Oct) fixed by playbook 6.14.3: runs no longer delete them. ISSUE: fixed. Order unchanged.
- Wed 28 Oct 2026 (about 21:40): Evening review, a quiet evening (no change for Thu 29 Oct). Pipeline 7.8, hash matched; 28 Oct +1.79% against SPY +0.34%, value 103,232. Feed used; non-US yields from the feed; commodities from the futures fallback; broad scan current. Drift: Labcorp ENTER (not taken), Flex FAIL, Phillips 66 FAIL. Intake: Labcorp, Quanta Services, Comfort Systems USA, Aon, Illumina; removed Phillips 66, Centene, Charles River Laboratories. No message.
- Tue 27 Oct 2026 (about 21:45): Evening review, a quiet evening (no change for Wed 28 Oct). 27 Oct +0.54% against SPY +0.56%, value 101,419. Tim's 26 Oct FT figures stored (RECONCILE +94 credits). Intake: Texas Instruments, F5, Flex, Johnson Controls, Pentair. No message.
- Mon 26 Oct 2026 (about 23:25): Hand-run session with Tim. FT figures for the 26 Oct close (100,973, rank 3,994 of 14,736); playbook 6.14.1 and feed 1.2 (non-US yields). ISSUE: fixed.
- Mon 26 Oct 2026 (about 21:45): Evening review, a change evening for Tue 27 Oct (ServiceNow, Robinhood, Strategy out; Shopify 20, Micron 10, Datadog 5 in). Mon +1.22% against SPY +0.71%. Order message sent about 21:34 UK.
- ISSUE (26 Oct evening review; fixed at about 23:20 UK the same night, playbook 6.14.1, feed 1.2): non-US 10-year yields not refreshed. Confirmed fixed on 27, 28 and 29 Oct.
- Mon 26 Oct 2026 (about 17:15): Hand-run session with Tim. Data check false failure fixed (ISSUE: fixed). Playbook 6.14: cut-off 08:00 UK, pipeline 7.8, nightly watchdog. Order unchanged.
- Sun 25 Oct 2026 (about 21:50): Evening review, FAULT: running the script refused by the session's permission check; nothing published. Order for Mon 26 Oct stood.
- Sun 25 Oct 2026 (about 20:30): Weekend news check (Sunday). No A item. Script refused; Weekend log updated only.
- Sat 24 Oct 2026 (about 20:30): Weekend news check (Saturday). No A item. Script refused; Weekend log updated only.
- Sat 24 Oct 2026 (about 09:35): Weekly review. Week -1.74% against SPY -0.43%. Files published; two old data assets could not be deleted.
- Thu 22 Oct 2026 (about 21:45): Evening review, a change evening for Fri 23 Oct (rule exits of AMD, Shopify and Datadog; Nvidia 20). Day -1.75% against SPY -1.18%.

## 7. Market regime notes

Label: Risk-off (Fri 30 Oct: Intel's and Amazon's reports hit tech, Nasdaq -2.8%, Bitcoin -5%; Sandisk fell 13.5% on a beat and raise; yields lower; Brent about $112).

Fri 30 Oct: S&P 500 -1.83%, Nasdaq -2.84%, Dow -1.06% (TheStreet); SPY -1.77%. October's last session. Intel -29%, Reddit -29%, Amazon lower (EPS $1.89 against $1.96). Memory: Sandisk -13.5% (open -8.6%, inside its 9.7% implied move, closed in the lower half), Micron -5.3%. Q3 employment cost index +0.8% (in line; Q2 0.9%), 3.4% on the year. US 10-year 4.94% (-4bp).

Thu 29 Oct: S&P 500 about -0.3% (SPY -0.38%), ending a three-day run; Nasdaq about -1.4%. Q3 GDP 3.4% annualised (Q2 2.2%); September PCE +0.5% on the month, 3.6% on the year (August 3.4%), described as in line; CME FedWatch about 81% for a 25bp hike in December. Alphabet -12.6% (negative free cash flow of $9.1bn on AI spending), Marvell -13.2%, ServiceNow about -20% on its Q4 guide, Fortinet gapped down after a beat and raise and closed near its high, Eli Lilly +6.4% (beat and raise), Shell beat with a $5bn buyback. Memory fell before Sandisk's report: Sandisk -5.3%, Micron -5.0%. After hours: Intel about -17.6%, Amazon about -6.7%, Sandisk about +2% to +3% (revenue +378%, 8-for-1 split).

Wed 28 Oct: S&P 500 +0.28% (7,743.98, a record), Nasdaq +0.27%, SOX +1.75% on SK Hynix's results. Fed held at 3.75% to 4.00%, 10-2 (Cook and Hammack for a hike). After hours: Microsoft about +4%, Alphabet about -8%, ServiceNow about -16%.

Tue 27 Oct: S&P 500 +0.60%, Nasdaq +1.18%. Mon 26 Oct: S&P 500 +0.70%. Fri 23 Oct: S&P 500 -0.52%. Thu 22 Oct: S&P 500 -1.21%, Nasdaq -2.60%.

Weekend log (weekend of 24 and 25 Oct): no A item on either day. B: Iran (Trump: no strike before the 3 Nov midterms) and Houthi attacks on Saudi Arabia. C: Bitcoin -0.6% (Sat) and -0.9% (Sun) from Friday's close.
Weekend of 17 and 18 Oct: no A item. B: Hormuz; Russia sanctions waiver.

Near calendar (the full calendar to 27 Nov is on the page and in the ledger):
- Fri 30 Oct: Exxon Mobil, Chevron, AbbVie (before the open); BP (07:00 UK); Sandisk's reaction session. Employment cost index, Chicago PMI. US session 13:30 to 20:00 UK this week.
- Sun 1 Nov: US clocks go back. Mon 2 Nov: Palantir (after the close); US session back to 14:30 to 21:00 UK. Tue 3 Nov: Shopify (before the open; order before 08:00 UK Mon 2 Nov), AMD (after the close), JOLTS; US midterms. Wed 4 Nov: Datadog (before the open), Arm (after the close). Thu 5 Nov: Cloudflare (after the close). Wed 18 Nov (est.): Nvidia.

## 8. Open questions for Tim

Answered: an order entered before 08:00 UK counted for that day up to 23 Oct; the midday check stays off; the leaderboard shows only the top 10; Shell filled at its 08:00 open on 9 Oct; Microsoft, Coca-Cola, Palantir, Goldman Sachs, Meta Platforms and Eli Lilly are in the game's list; the orders for 13 to 16 Oct were entered; GitHub access from scheduled runs; the cut-off after the clock change (08:00 UK local time all year); the fetch tool refusing built addresses (answered by the price feed); Marsh & McLennan stays in the panel; order B entered (21 Oct); whether the 23 Oct order was entered as sent; the 27 Oct order entered (26 Oct, 22:52 UK).

Still open:
1. Are Nvidia, Shopify, Arm, Sandisk, Micron and Cloudflare in the game's list? Assumed yes (large Nasdaq or NYSE listings).
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

- The order was replaced by the endgame switch before it filled; its drift row settled on 27 Oct (+7.51 points against the index).

**The endgame switch, 22 Oct (first session of a one-way book)**

- The high-beta book filled at the 22 Oct open into an AI sell-off: -1.75% on the day against SPY -1.18%. Lesson: a one-way book doubles both the bad and the good days. Sequel: the switch's five-session row completed on 28 Oct at +1.67 points against the old defensive book.

**The rule exits of 23 Oct (AMD, Shopify, Datadog, sold after one session)**

- After its five sessions the change cost 4.20 points against keeping order B (complete on 29 Oct). Lesson: an exit signal on a day when the whole sector sold off on volume is weaker evidence than one on a quiet day; the 27 Oct and 30 Oct rows will show whether the pattern repeats before any rule change is put to Tim.

**The exits of 27 Oct (ServiceNow on a marginal signal; the crypto pair on IBIT's 50-day)**

- ServiceNow closed 0.23% below its open on exactly the 1.3 times volume threshold, two days before results; after three sessions the change stands +6.20 points, with ServiceNow about -20% on 29 Oct after its guide. Lesson to test: whether edge-of-threshold signals cost more than clear ones; the five-session row will say.

**Datadog, 29 Oct (an exit on a sector-wide software sell-off)**

- Closed 1.38% below its open on 1.38 times average volume, the day ServiceNow and Fortinet's reports hit software; swap Cloudflare gapped down on the same news but closed 1.9% above its open. Lesson to test: whether exits on peer-driven sector days cost more than exits on stock-specific days (23 Oct cost 4.20 points).

**Coca-Cola, 27 Oct (a beat and raise that fell)**

- Comparable EPS $0.91 against $0.88, revenue $13.4bn against $12.93bn, guidance raised, and the stock fell 1.6% on the day: drift FAIL. Lesson: in a growth rebound, a defensive beat-and-raise does not draw buyers; the reaction test exists for this.

## 11. Confidence ratings, shadow ratings, the panel test and the day call

- Confidence ratings (not calibrated): 24 of 28 settled, few distinct dates: below 55, 5 of 11 beat the index (45%); 55 to 59, 6 of 9 (67%); 60 and above, 4 of 4 (100%, all from the 9 to 15 Oct energy book). Ordered by rating, but far too few to judge. Ratings for the order in force: Palantir 55, Shopify 54, Nvidia 52, Micron 52, Cloudflare 52, Arm 50, Sandisk 50.
- Shadow ratings: 484 logged, 292 settled. Live: score 70 and above, 116 cases, 63% beat the index (+0.64 points); 60 to 69, 84, 48% (-2.09); 45 to 59, 42, 31% (-2.34); below 45, 50, 66% (+1.43). Not ordered by score; few distinct dates. Judgement test: two dates (full score +0.113, price and session +0.160, judgement -0.039): too few.
- Panel test: see section 1. Old backtest (hindsight) correlation +0.008.
- Drift record: ENTER 1 settled (Hasbro, +7.51 points against the index), 1 open (Labcorp, not taken); WATCH Johnson Controls open; FAIL 7 settled (14% beat the index, -5.07 points), 9 open (including Microsoft, ServiceNow, Fortinet, Shell, Eli Lilly from 29 Oct).
- Day call record (S&P 500): 9 right of 14 (always green: 7); Brier 0.245. Below the 20 settled calls needed before it could be considered.
- Broad scan record (scan/latest.md, 30 Oct): Leaders, 60 settled, 40% beat the index, mean excess -1.81 points close to close and -1.89 from the next open (first appearances 21, 38%, -1.91); Events, 9 settled, 56%, -1.31 and -1.44; 70 rows open. About 12 of the week's intake came from the scan; from their add-date close to 30 Oct, 7 of 12 trailed the index (worst F5 -24.5 and Illumina -16.1 points; best Pentair +8.2).

## 12. Tools

- Tim's page: https://claude.ai/artifact/8P8UwQsb4QsbZMsKNYKrUJ, pinned in his Claude sidebar, with tabs Today, Macro, Performance, Risk, Calendar and Log. It reads four data files (`stocks`, `ledger`, `history`, `macro`) and a fifth dataset, `logos`, that no run touches. The Order panel reads the latest alert whose `stock` is "Order"; its "Enter before" bar uses the 08:00 UK cut-off.
- Playbook docs (version 6.14.3): `claude/ft-game-playbook.md` (core, with the routing table), `claude/ft-game-rules.md`, `claude/ft-game-data.md`, and the run docs `claude/ft-game-run-evening.md`, `-morning`, `-refresh`, `-weekly`, `-weekend`.
- Panel file: `panel.json` on the same artifact, named by the document `store/panel`.
- Scripts: the pipeline (version 7.8; runs take it from the repository at the commit in data doc G1) and the screening script are assets on that artifact. Their ids and hashes are in part B of the playbook, the only place they are kept.
- Price feed (data doc G8): `feed/latest.json` and `feed/live.json` in the repository, with the non-US 10-year yields under `macro.intl_yields`. 29 Oct: the scheduled close run (generated 20:54 UTC) covered every list stock, SPY, the extra rows, the panel, US and non-US yields and coins. Nothing missing or refused.
- Pages reached through searches on 29 Oct: MoneyCheck (Sandisk results), Stock Titan (market wrap, movers), Upstox (PCE, FedWatch odds), earnings-watcher (Cloudflare implied move), Zacks via Yahoo Finance (Fortinet), Investing.com (Shell), TradingView headline (Eli Lilly). Refused: Alphastreet's Datadog page, Chartmill's and Rolling Out's Lilly pages (client errors). tradingeconomics' commodity page did not come up in a search; commodities from `feed --futures yes`.
- Market data service: massive.com, free plan, on an account opened by Tim's father. The key is in the evening and weekly review tasks and is never written into this project's docs, the page data, alerts or messages. Not used on 29 Oct (the feed covered every price).
- Sources that did not work: Alphastreet, Chartmill and Rolling Out article pages (29 Oct); Benzinga article pages (28 Oct); CNBC article pages; gurufocus news pages and EBC; CNN article pages; Detroit News; Fortune's Bitcoin price page; capital.com news pages. tradingeconomics' news pages carry no statistics table.
- Artifact leftovers: deletes of old data assets refused on 24 and 26 Oct and partly on 29 Oct left unnamed files in the store; from playbook 6.14.3 runs no longer delete superseded data assets (data doc G5 step 4), so they accumulate as expected leftovers. 29 Oct evening: 34 MB of 1 GB used, 66 files.
- GitHub mirror: private repository `timzwang/ft-game` (part B and G6).
- Two saved skills, `ft-game-playbook` and `stock-score`, load in scheduled runs; the project docs win where they differ.
