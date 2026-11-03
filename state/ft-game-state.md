# FT Stock Picking Game: state and log

Last updated: Tue 3 Nov 2026, about 23:00 UK (session with Tim, playbook 6.15; order unchanged). Before that, Tue 3 Nov 2026, about 21:45 UK (evening review, a quiet evening: no change for Wed 4 Nov's open). Before that, Mon 2 Nov 2026, about 21:45 UK (evening review, a change evening). Earlier entries: see the review log (section 6).

This doc is the narrative record for Tim's entry, "Seeking Beta". The procedure for every run is in `claude/ft-game-playbook.md` (the core doc) and the docs its routing table names. The numbers (prices, scores, daily performance, contributions, ratings and their outcomes, the full calendar, analyst changes, alerts, the panel test, the drift record) live in the data files behind Tim's page and the panel file, and are produced by the pipeline script; this doc carries the decisions and the reasons.

Messages: from 10 Oct Tim is sent a message only when there is something for him to enter or answer (playbook part I, "When Tim is told"), and always when there is an issue (part I, "Issues: flag and fix", from 26 Oct). Quiet runs update the page and this doc and send nothing.

Scheduled runs: evening review 21:30 UK Sun to Thu; morning check 07:26 UK Mon to Fri (from Tue 27 Oct; 06:36 from 18 to 26 Oct; playbook 6.14); price refresh 17:04 UK (from 4 Nov; 16:45 until 3 Nov) and late price refresh 19:22 UK Mon to Fri; results-day refresh 14:50 UK Mon to Fri (acts only on results days); weekly performance review Sat 09:12 UK; weekend news check Sat and Sun 20:20 UK; nightly watchdog 22:47 UK every day (from 26 Oct); midday check 12:40 UK Mon to Fri (stops at once by its own instructions; Tim to switch the task off, roadmap item 68).

**Cut-off: every order must be entered before 08:00 UK, UK local time all year (FT Customer Care to Tim, 21 Oct; Tim approved the move back the same night; playbook 6.14 and pipeline 7.8 from 26 Oct). 07:00 UK was used as a safety margin from 17 to 26 Oct.**

## 1. Status

- **Playbook version 6.15** (6.15, 3 Nov late evening: results-day refresh only for stocks on the list, 17:04 UK price refresh, late refreshes not an issue, watchlist under the stance in core part D, page redesigned; 6.14.3, 29 Oct evening: runs no longer delete superseded data assets, data doc G5 step 4; G5 step 5 checks the store's size instead; 6.14.2, 27 Oct: feed 1.2.1 takes Japan's 10-year from CNBC first; 6.14.1, 26 Oct: the five non-US 10-year yields from the price feed; 6.14, 26 Oct: cut-off 08:00 UK, pipeline 7.8 from commit `9760163`, nightly watchdog 22:47 UK; 6.13.2: flag and fix every issue; 6.13.1: the script run from the repository; 6.13, 21 Oct: the endgame stance in core part D; earlier versions in the playbook header). **Pipeline script version 7.8** (part B holds the asset id, the run commit and the hash). The 3 Nov evening review ran it from commit `9760163` (hash matched part B).
- **Estimated value at Tue 3 Nov close: 91,605, -8.40% since the start, against -2.82% for the S&P 500 fund (gap -5.58 points).** Tue 3 Nov +1.99% against SPY +0.30%: ServiceNow +0.73 points, Monolithic Power +0.68, Micron +0.52, Western Digital +0.39, Seagate +0.32, NetApp +0.30, Amazon +0.21, Palantir (sold at the open, -5.70% gap) -1.14.
- **Last FT figures: Mon 26 Oct close, 100,973 (+0.97%), rank 3,994 of 14,736 (top 27.1%; the top 2% is rank 294 or better).** `reported` row with top2_return_pct 8.14 (a player at rank 330). RECONCILE +94 credits (+0.09%). Asked for on 31 Oct and 1 Nov; not yet received.
- **Standstill (3 Nov evening run):** change for 22 Oct +1.67, 23 Oct -4.20, 27 Oct +4.26, all complete; 30 Oct +0.20 after three sessions; 2 Nov +1.16 after two; 3 Nov -0.08 after one. Week of 19 Oct -3.17; week of 26 Oct +5.58; week of 2 Nov +1.08 so far. Inception (18 sessions): -10.26 as entered, -10.87 fully invested. EXPECTED BENEFIT: three settled, expected 0.0, actual +1.73, sign right in 1 of 3.
- **Panel test (all 30 members loaded):** history verdict "no evidence" (average rank correlation +0.042, t +1.1, 58 dates). Live: two dates (-0.130), too few to judge. The score is frozen.
- **Order in force, unchanged for Wed 4 Nov's open (set by the Mon 2 Nov evening review; message sent about 21:39 UK that night):** ServiceNow 20, Micron 20, Seagate 15, Western Digital 15, Monolithic Power Systems 10, NetApp 10, Amazon 10, cash 0.
- Day call record (S&P 500): 10 right of 16; Brier in the ledger. Wed 4 Nov: S&P 500 Green 56% against a usual 55%; portfolio Green 58% against a usual 56%; reviewer +1 and +2 for AMD's after-hours rise and guide.
- Macro at Tue 3 Nov: US 2-year 4.61% (+2bp; -9bp over five), 10-year 4.95% (+4bp; -4bp over five), 30-year 5.32%. UK 10-year 5.25% (+5bp; -10bp over five), Germany 3.33%, France 4.95%, Italy 4.47%, Japan 2.77% (all from the feed). Brent $104.51 (+0.3%; -4.8% over five), WTI $96.90, natural gas $2.91, gold $3,934.50 (futures fallback). Backdrop label: neutral.
- Crypto: Bitcoin $77,784 at the US close (+1.5% on the day, -3.6% over five); trend **mixed** (IBIT 4.0% below its 50-day, 4.2% below its 20-day, 6.5% above its 200-day), so no crypto-linked buy. No crypto-linked holding. Binance hack of about $6.3bn, attributed by the FBI to North Korea (Yahoo).
- Regime: mixed. Tue 3 Nov: S&P 500 about +0.36%, Nasdaq about +0.83%, Dow about -0.38%, Russell 2000 about +0.24% (TheStreet, closing wrap; levels not read). Chips rebounded after a Monday that left the semiconductor index in a bear market; Apple -4.4% on a margin guide cut by memory costs; US strike on Qeshm Island, Iran calls itself "in a state of war".

## 2. Current portfolio

The order for Wed 4 Nov's open (unchanged). Scores and bands from the pipeline at the Tue 3 Nov close. Under the endgame stance (core part D) the score floor, trend tests, volatility caps, theme guide and results budget do not apply; the NOTE lines for them are expected.

| Stock | Weight | Confidence (not calibrated) | Score | Band | Flags | Next results (implied move) | Swap if missing or broken |
|---|---|---|---|---|---|---|---|
| ServiceNow | 20% | 50 | 33 | Weak | below 50-day, oversold | Reported 28 Oct; next late Jan (est.) | Shopify |
| Micron | 20% | 52 | 33 | Weak | below 50-day, faded gap | December (after the game) | Sandisk |
| Seagate | 15% | 50 | 40 | Weak | below 50-day, oversold, faded gap | Reported 27 Oct | Western Digital |
| Western Digital | 15% | 50 | 28 | Weak | below 50-day, downtrend, faded gap, death cross 2 Nov | Reported 22 Oct | Seagate |
| Monolithic Power Systems | 10% | 54 | 66 | Weak | downtrend, death cross 19 Oct | Reported 29 Oct; next Feb | Analog Devices |
| NetApp | 10% | 50 | 45 | Middling | below 50-day | 25 Nov, after US close (est.) | Seagate |
| Amazon | 10% | 52 | 49 | Middling | below 50-day | Late Jan (after the game) | Microsoft |
| Cash | 0% | | | | | | |

Themes: AI and chips 70%, Software 30%. Memory and storage (Micron, Seagate, WDC, NetApp) 60%. Largest risk shares: Micron 23%, Western Digital 19.7%, Seagate 19.3%, ServiceNow 18%; estimated daily volatility 2.58%. Worst scenario: a deeper AI sell-off, -7.4%. The concentration is deliberate under the stance. No holding reports inside ten sessions.

Points for the coming reviews:

- Watchlist clean-up due in the 4 Nov evening review (core part D, playbook 6.15): remove the names in barred themes (Exxon Mobil, Chevron, Shell, Eli Lilly, Coca-Cola, Labcorp, Valero Energy, Johnson Controls), refresh stale notes (TSMC's, for example), and rebuild towards about 20 buyable high-beta names. A dry run on 3 Nov left every figure unchanged.
- Memory bounced on 3 Nov but Micron, Seagate and Western Digital all closed below their opens (faded gaps), on 0.77, 0.85 and 0.59 times average volume, under the 1.3 heavy-volume line, so no exit signal. A repeat on heavy volume would be one. The stance names the memory theme breaking down as what would show it wrong; Tim was told on 2 Nov that a change of direction is his call.
- Palantir sold at the 3 Nov open, -5.70% from the previous close (cost -1.14 points), then rose 4.29% open to close on 2.2 times volume. Drift FAIL.
- AMD reported after the 3 Nov close: beat, Q4 guide about $17bn against about $16.3bn, up after hours. Reaction session is 4 Nov: add its drift row in that review. It closed above its open on 3 Nov, so the swap column is open if a holding signals.
- Sold and kept on the list five sessions for the standstill test: Palantir (to Mon 9 Nov); Nvidia, Shopify, Arm, Sandisk, Cloudflare, Datadog (to Fri 6 Nov).
- Iran: US struck Qeshm Island ("small-scale", "defensive"); Iran says it is "in a state of war"; a senior official says a deal is out of reach. Scenario "Oil spike on escalation" -2.0 points.
- Midterm count overnight: Democrats about 76% to win both chambers on Polymarket (Yahoo).
- Bitcoin's trend is mixed: no crypto-linked buy.

## 3. Pending order

**No change for Wed 4 Nov's open (Tuesday 3 Nov evening review).** Order in force: ServiceNow 20, Micron 20, Seagate 15, Western Digital 15, Monolithic Power Systems 10, NetApp 10, Amazon 10, cash 0. Last changed for Tue 3 Nov's open (message sent 2 Nov about 21:39 UK); taken as entered unless Tim says otherwise.

## 4. Watchlist

27 names after tonight (above the cap of 25 because the sold holdings, the first order's stocks and the open drift rows must stay listed). Scores and bands at the Tue 3 Nov close. Removed tonight: Robinhood, Pentair. Added: Advanced Energy (drift FAIL on trend only), Bloom Energy (Barclays upgrade). Fewer than five added: the scan's Events (Fiserv, DuPont, Drax) and Leaders are outside the stance.

| Name | Band | Status | Score | Note |
|---|---|---|---|---|
| Exxon Mobil | Strong | Watching | 74 | Sold in the endgame switch (22 Oct open); kept five sessions for the standstill test. |
| Eli Lilly | Strong | Watching | 74 | Sold in the endgame switch (22 Oct open); kept five sessions for the standstill test. |
| Labcorp | Strong | Drift: enter (not taken) | 73 | Drift scan 28 Oct: ENTER, all six tests passed (beat and raise, +8.8% on 2.8x volume, above its 50-day). Not b |
| Coca-Cola | Strong | Watching | 72 | Sold in the endgame switch (22 Oct open); kept five sessions for the standstill test. |
| Texas Instruments | Strong | Watching | 71 | Broad scan leader #12 (27 Oct): analog chips, +54.5% against the index over 12 months. Correlated with Analog  |
| Chevron | Strong | Watching | 70 | Sold in the endgame switch (22 Oct open); kept five sessions for the standstill test. |
| Quanta Services | Strong | Watching | 70 | Scan Event #3 28 Oct (+4.8%, gap +3.7%, 1.8x volume) on results day; AI power infrastructure. Results figures  |
| Shell | Strong | Watching | 67 | Sold in the endgame switch (22 Oct open); kept five sessions for the standstill test. |
| Valero Energy | Middling | Results ahead | 67 | Refiner at a 52-week high with record crack spreads; closed 1.5% below its open on Friday after a new high. Ex |
| Microsoft | Strong | Watching | 66 | Sold 22 Oct. Reported 28 Oct after the close: EPS $4.89 vs $4.72, revenue $92.28bn vs $90.61bn; about +4% afte |
| Analog Devices | Strong | Watching | 62 | Broad scan leader #16 (26 Oct), +4.3% on 26 Oct. Chip name with a smaller range than the memory names; panel m |
| Johnson Controls | Strong | Watching | 62 | Scan Event 27 Oct (+5.7%, 1.7x volume) on a results beat and a record $23bn backlog led by data-centre cooling |
| Datadog | Middling | Exit signal (sold for 30 Oct) | 56 | Sold for 30 Oct on the endgame exit rule (heavy-volume close below its open on 29 Oct); kept listed five sessi |
| AMD | Middling | Exit signal | 49 | Reported 3 Nov after the close: beat, Q4 guide $17bn against about $16.3bn; shares up after hours. Reaction se |
| Bloom Energy | Middling | Watching | 48 | Barclays upgrade on 3 Nov; AI power demand. Promote only on follow-through: a further close above its open. |
| Flex | Middling | Watching | 45 | Drift scan 28 Oct: FAIL on trend only (beat and raise, +11.6% on 2.5x volume, but 13% below its 50-day). Fits  |
| Cloudflare | Weak | Exit signal | 43 | Sold for Mon 2 Nov: heavy-volume close below its open on 30 Oct (endgame exit rule); kept on the list five ses |
| Advanced Energy | Weak | Watching | 43 | Drift candidate: beat and strong guide on 2 Nov after the close; high-beta AI power supplies. Promote on the d |
| Palantir | Weak | Exit signal | 40 | Exit signal: sold at the 3 Nov open, -5.70% from the previous close, then +4.29% open to close on 2.2 times vo |
| Coinbase | Weak | Watching | 38 | Crypto tracker: kept on the list whatever its score. It earns its money from coin trading, so it follows Bitco |
| Sandisk | Weak | Exit signal | 37 | Sold for Mon 2 Nov: heavy-volume close below its open on 30 Oct (endgame exit rule); kept on the list five ses |
| Shopify | Weak | Exit signal | 37 | Sold for 2 Nov, avoiding a report that fell 8.7%. Kept to 6 Nov for the standstill test. |
| Strategy | Weak | Exit signal (sold for 27 Oct) | 36 | Crypto tracker: sold for 27 Oct, IBIT closed below its 50-day average (crypto exit rule). Stays on the list as |
| TSMC | Weak | Watching | 34 | Left the order 16 Oct; kept until Fri 23 Oct for the standstill test, then removed. |
| Fortinet | Weak | Watching | 33 | Reaction day 29 Oct: gapped down after a beat and raise, closed near the high; logged in the drift scan, rotat |
| Arm Holdings | Weak | Exit signal | 31 | Sold for Mon 2 Nov: heavy-volume close below its open on 30 Oct (endgame exit rule); kept on the list five ses |
| Nvidia | Weak | Exit signal | 30 | Sold for Mon 2 Nov: heavy-volume close below its open on 30 Oct (endgame exit rule); kept on the list five ses |

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
| Sun 1 Nov, about 21:40 UK (message sent) | Mon 2 Nov | Sell Nvidia 20, Shopify 20, Arm 15, Sandisk 10, Cloudflare 5; Micron 10 to 20; add Seagate 15, Western Digital 15, Monolithic Power Systems 10, NetApp 10, Amazon 10 | Endgame exit rule: all five closed below their opens on heavy volume on 30 Oct (Nvidia 1.69, Shopify 1.36, Arm 2.26, Sandisk 2.14, Cloudflare 1.64 times average). Their swaps gave the same signal (AMD, ServiceNow, Qualcomm, Datadog) except Micron, so Micron to 20 and the weight to the swap column's clean names and three clean high-beta tech names to keep seven holdings. Expected 0.0 points |
| Mon 2 Nov, about 21:39 UK (message sent) | Tue 3 Nov | Sell Palantir 20; add ServiceNow 20 | Endgame exit rule: Palantir closed 4.39% below its open on 1.44 times average volume on 2 Nov, before its report; swap ServiceNow closed 1.11% above its open. Expected 0.0 points |

## 6. Review log (newest first, keep the latest 15)

- Tue 3 Nov 2026 (about 23:00): Session with Tim. Playbook 6.15, page redesigned. Exit rule tested on stored prices: no change (roadmap item 69). Order unchanged. No open ISSUE; the midday task still to be switched off by Tim.
- Tue 3 Nov 2026 (about 21:45): Evening review, a quiet evening: no holding gave an exit signal (Micron, Seagate, WDC closed below their opens on volume under 1.3 times). 3 Nov +1.99% against SPY +0.30%, value 91,605. Pipeline 7.8 from commit `9760163`, hash matched. Price feed: forced (first read 2 Nov; forced run generated 21:34 UTC, again 21:38 UTC for FISV, DD, AEIS, BE), nothing refused or missing. Non-US yields from the feed; commodities from the futures fallback. Broad scan: forced (3 Events, 30 Leaders). Drift: Palantir, Shopify, Fiserv, Advanced Energy all FAIL; DuPont left out (its results page was rate limited). Added Advanced Energy, Bloom Energy; removed Robinhood, Pentair. Files published (no deletes). WARNINGs: FLEX 2026-05-06 and CNC 2025-07-02 known genuine; BE 2024-11-15 (+59.2%) from the feed's new two-year history, believed genuine (AEP deal), not re-checked. Pages not read: CNBC article pages (site errors), investing.com and 24/7 Wall St's AMD live page (rate limited, not re-requested). JOLTS exact figure and Fiserv's consensus revenue not read. No ISSUE this run.
- Mon 2 Nov 2026 (about 21:45): Evening review, a change evening for Tue 3 Nov (Palantir out, ServiceNow in). 2 Nov -4.33% against SPY -0.48%, value 89,814. Pipeline 7.8 from commit `9760163`, hash matched. Price feed: forced (first read 30 Oct; forced run generated 21:32 UTC, again 21:37 UTC for IDXX), nothing refused or missing. Non-US yields from the feed; commodities from the futures fallback (no current tradingeconomics page came through the search). Broad scan: forced (1 Event, 30 Leaders). Drift: Idexx FAIL on trend, not taken. Removed CrowdStrike; no additions. Order message sent about 21:39 UK. Files published (no deletes). WARNINGs for FLEX 2026-05-06 and CNC 2025-07-02: known genuine moves. Pages not read: Benzinga's Palantir article, CNBC's oil article, Seeking Alpha, Archynewsy (site errors), investingLive's ISM page (server error), BusinessWire's Palantir release (address too long). Apple's results and Palantir's later after-hours price not found at review time. No ISSUE this run.
- Sun 1 Nov 2026 (about 21:45): Evening review, a change evening for Mon 2 Nov (five rule exits; Micron 20, Seagate 15, Western Digital 15, Monolithic Power 10, NetApp 10, Amazon 10 in). Pipeline 7.8 from commit `9760163`, hash matched. No new session (Friday logged by the weekly review). Price feed: current (Fri 30 Oct, generated 20:51 UTC), then forced at 21:35 UTC for 17 candidate tickers. Feed REFUSED Palantir on its second run (Yahoo's revised 30 Oct low 180.81 against the stored 183.68): checked on stockanalysis.com (low 180.81, "At close: Oct 30") and the corrected row given; RECALCULATED, value unchanged. Non-US yields from the feed; commodities from the futures fallback. Broad scan: current (2 Events, 30 Leaders, all outside the stance except TXN and ADI, both already listed and both with the exit signal). Drift: Sandisk, Monolithic Power, Amazon all FAIL. Intake: two (Monolithic Power, Amazon, both bought), fewer than five because nearly every high-beta tech name closed below its open on heavy volume on 30 Oct. Removed Aon, Palo Alto Networks, Illumina, Comfort Systems USA, F5, AbbVie. NetApp results event (25 Nov, est.) added. Order message sent about 21:40 UK. Files published (store 51 MB, 84 files; no deletes). No ISSUE this run.
- Sun 1 Nov 2026 (about 20:30): Weekend news check (Sunday). No A item; three B items (Axios: Netanyahu pressing for a strike on Iran right after the 3 Nov midterms, Trump wants more time; new Hormuz shipping incidents, Saudi TASI -0.84%; Doha talks in a third day, no deal). Ledger published. No ISSUE this run. Order unchanged.
- Sat 31 Oct 2026 (about 20:25): Weekend news check (Saturday). No A item; two B items (US strikes on Iran reported as possible from 4 Nov; Doha talks on reopening Hormuz). No ISSUE this run.
- Sat 31 Oct 2026 (about 09:30): Weekly review. Fri 30 Oct logged from the price feed: -7.14% against SPY -1.77%, value 93,877; week -5.81% against SPY -0.56%. WARNINGs for FLEX 2026-05-06 and CNC 2025-07-02 checked: genuine moves. Order unchanged; message to Tim with the review and a request for FT figures. No ISSUE this run.
- Thu 29 Oct 2026 (about 21:45): Evening review, a change evening for Fri 30 Oct (Datadog out on the endgame exit rule, Cloudflare 5 in). 29 Oct -2.07% against SPY -0.38%. Order message sent about 21:34 UK. Drift: Microsoft, ServiceNow, Fortinet, Shell, Eli Lilly all FAIL. Pages refused: Alphastreet's Datadog page, Chartmill's and Rolling Out's Lilly pages.
- ISSUE (29 Oct evening review, about 21:40 UK; fixed): the first state doc write was refused, "project_write: local_path must be inside the working directory". Fixed by writing from the repository copy `state/ft-game-state.md`.
- Thu 29 Oct 2026 (about 19:45): Session with Tim. Playbook 6.14.3: runs no longer delete superseded data assets. ISSUE: fixed. Order unchanged.
- Wed 28 Oct 2026 (about 21:40): Evening review, a quiet evening. 28 Oct +1.79% against SPY +0.34%. Drift: Labcorp ENTER (not taken), Flex FAIL, Phillips 66 FAIL. No message.
- Tue 27 Oct 2026 (about 21:45): Evening review, a quiet evening. 27 Oct +0.54% against SPY +0.56%. Tim's 26 Oct FT figures stored. No message.
- Mon 26 Oct 2026 (about 23:25): Hand-run session with Tim. FT figures for the 26 Oct close (100,973, rank 3,994 of 14,736); playbook 6.14.1 and feed 1.2. ISSUE: fixed.
- Mon 26 Oct 2026 (about 21:45): Evening review, a change evening for Tue 27 Oct (ServiceNow, Robinhood, Strategy out; Shopify 20, Micron 10, Datadog 5 in).
- ISSUE (26 Oct evening review; fixed the same night, playbook 6.14.1, feed 1.2): non-US 10-year yields not refreshed.
- Mon 26 Oct 2026 (about 17:15): Hand-run session with Tim. Playbook 6.14: cut-off 08:00 UK, pipeline 7.8, nightly watchdog. Order unchanged.

## 7. Market regime notes

Label: Mixed (Tue 3 Nov: Nasdaq +0.8%, Dow -0.4%; chip bounce on light volume after the semiconductor index entered a bear market on Monday). What would change it: to risk-on, a Nasdaq close back above its 20-day average; to risk-off, a heavy-volume reversal in chips after AMD.

Tue 3 Nov: S&P 500 about +0.36%, Nasdaq +0.83%, Dow -0.38%, Russell 2000 +0.24%; VIX 21.27 (Bank of Vol). Apple -4.4%: gross margin guide 45% to 46% against 47%, memory costs; its CEO called memory pricing "unprecedented" and rising beyond December. Palantir -1.65% (gap -5.70%). Shopify -8.74% (gap -12.67%): GMV $119.15bn against $120.08bn. Fiserv +12.5%. Bloom Energy on Barclays upgrade. AMD after the close: revenue about $13.4bn against $13.1bn, EPS about $2.10 against $1.95, Q4 guide about $17bn against $16.3bn, margin guide 55% against 55.5%. JOLTS little changed (forecast 7,164k; figure not read). A December Fed hike about 75% priced (Bank of Vol).

Mon 2 Nov: S&P 500 -0.51%, Nasdaq -1.07%, Dow +0.41%, Russell 2000 -0.21%. Kioxia guided December-quarter operating profit to 2 trillion yen, below estimates, blaming shipment timing, and said next year's output has sold out. Marvell -12.7% and Lumentum -18.6% on Marvell's $115bn all-stock deal, read by Citrini's Jukan as a sign of an AI collapse in two to three years; Oracle down on a $20bn capital raise. ISM manufacturing 55.5 (forecast 54.5), prices paid 75.2. Palantir after the close: revenue $2.31bn (+96%), FY guide about $8.53bn, contract value +6%. Idexx +21.9% on a beat and raise.

Fri 30 Oct: S&P 500 -1.83%, Nasdaq -2.84%, Dow -1.06%; SPY -1.77%; S&P 500 futures settled -1.8%, Nasdaq 100 futures -3.5% (Regards of Wall Street, last 6:40pm ET). Intel -29%; Dell -11% and HP lower on Intel's PC outlook (units -12% in 2026, -10% in 2027, blamed on memory shortages); Amazon EPS $1.89 and revenue $201.9bn, both below consensus, AWS +39%, opened about 5% down and closed -1.4%; Qualcomm -11%; Marvell -10%. Memory: Sandisk -13.5% (beat: revenue $11.03bn against $10.7bn, EPS $49.51 against $47.15; Q2 EPS guide $55 to 57 against $54.69; consumer revenue -29%), WDC -7.4%, Seagate -8.0%, Micron -5.3% (24/7 Wall St: profit-taking after a 460% year, Samsung -6% and Kospi -5%). Q3 employment cost index +0.8% (in line).

Thu 29 Oct: S&P 500 about -0.3%, Nasdaq about -1.4%. Q3 GDP 3.4% annualised; September PCE 3.6% on the year. Alphabet -12.6%, ServiceNow about -20%, Eli Lilly +6.4%.

Wed 28 Oct: S&P 500 +0.28% (a record). Fed held at 3.75% to 4.00%, 10-2. Tue 27 Oct: S&P 500 +0.60%. Mon 26 Oct: S&P 500 +0.70%.

Weekend log (weekend of 31 Oct and 1 Nov): Sat 31 Oct (check at about 20:25 UK): no A item. B: MS NOW (Fri 30 Oct, after the US close) says the US told Gulf allies to prepare for strikes on Iran from Wed 4 Nov; Khamenei promised an unrestricted response; Rubio: no decision yet; scenario "Oil spike on escalation" -2.0 points. B: Iranian delegation in Doha; Araghchi said a proposal cuts the Hormuz reopening period from five days to two. C: China's October manufacturing PMI 49.3; Bitcoin about $77,500 midday Sat; IG Weekend Wall Street -0.09%.
Sun 1 Nov (check at about 20:25 UK): no A item. B: Axios (via Iran International) says Netanyahu is pressing Trump to strike Iran right after Tuesday's midterms while Trump wants more time; Fox: strikes stay on the table, not likely before the midterms. B: Hormuz shipping: UKMTO reports a vessel hit; the IRGC claims tankers hit mines on Fri 30 Oct; Saudi TASI -0.84% on Sunday. B: Doha talks in a third day; Trump: talks "going fine". C: OPEC+ kept December targets; Binance hack report (one source, not verified); Bitcoin $77,827 Sun morning; IG Weekend Wall Street -0.08%.
Confirmed by the 1 Nov evening review (Al Jazeera, 1 Nov): Trump said on 31 Oct the US still had "one or two sites" to handle; Iran says it may strike pre-emptively; Qatar-mediated talks in Tehran (30 Oct) and Qatar (31 Oct); at least four tankers reported hit on 30 and 31 Oct; Iran has cut the period before a partial Hormuz reopening from seven days to two, on conditions (blockade lifted, sanctions waivers, assets unfrozen).
Weekend of 24 and 25 Oct: no A item. Weekend of 17 and 18 Oct: no A item.

Near calendar (the full calendar to 27 Nov is on the page and in the ledger):
- Wed 4 Nov: ADP (13:15 UK), ISM services (15:00 UK), midterm count; Datadog (before the open); Arm and Qualcomm (after the close; Qualcomm's date from its own release); AMD's reaction session.
- Thu 5 Nov: Bank of England (12:00 UK); Cloudflare (after the close). Fri 6 Nov: US jobs report (13:30 UK), forecast 55K. Tue 10 Nov: US CPI. Wed 18 Nov (est.): Nvidia. Wed 25 Nov (est.): NetApp. Thu 26 Nov: US closed. Fri 27 Nov: US closes 18:00 UK, game ends.

## 8. Open questions for Tim

Answered: an order entered before 08:00 UK counted for that day up to 23 Oct; the midday check stays off; the leaderboard shows only the top 10; Shell filled at its 08:00 open on 9 Oct; Microsoft, Coca-Cola, Palantir, Goldman Sachs, Meta Platforms and Eli Lilly are in the game's list; the orders for 13 to 16 Oct were entered; GitHub access from scheduled runs; the cut-off after the clock change (08:00 UK local time all year); the fetch tool refusing built addresses (answered by the price feed); Marsh & McLennan stays in the panel; order B entered (21 Oct); whether the 23 Oct order was entered as sent; the 27 Oct order entered (26 Oct, 22:52 UK).

Still open:
1. Are Micron, Seagate, Western Digital, Monolithic Power Systems, NetApp, Amazon and ServiceNow in the game's list? Assumed yes. Swaps if one is missing: Seagate and Western Digital for each other, Analog Devices for Monolithic Power, Seagate for NetApp, Microsoft for Amazon, Shopify for ServiceNow.
2. How a mixed London and US order entered for 26 Nov fills: Tim to ask FT help. Only matters if a London stock is bought: the book is all US.
3. Does the game convert US stocks' returns into pounds? The closing gap has stayed under 0.1%.
4. FT value, rank and players at the latest close (asked 31 Oct and 1 Nov; still needed).

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

- Bought for 14 Oct at 5%; sold at the 15 Oct open (726.56) after a close 3.0% below its open. Lesson: a momentum entry after a two-day run can reverse at once; the give-back rule cut the cost.

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

- Lesson: a one-way book doubles both the bad and the good days. Sequel: the switch's five-session row completed on 28 Oct at +1.67 points against the old defensive book.

**The rule exits of 23 Oct (AMD, Shopify, Datadog, sold after one session)**

- After its five sessions the change cost 4.20 points against keeping order B. Lesson: an exit signal on a day when the whole sector sold off on volume is weaker evidence than one on a quiet day; the 27 Oct, 30 Oct and 2 Nov rows will show whether the pattern repeats before any rule change is put to Tim.

**The exits of 27 Oct (ServiceNow on a marginal signal; the crypto pair on IBIT's 50-day)**

- After four sessions the change stands +5.48 points, with ServiceNow about -20% on 29 Oct after its guide. Lesson to test: whether edge-of-threshold signals cost more than clear ones.

**Datadog, 29 Oct (an exit on a sector-wide software sell-off)**

- Closed 1.38% below its open on 1.38 times average volume; swap Cloudflare gapped down on the same news but closed above its open, then gave its own exit signal the next day. Lesson: swaps taken on sector sell-off days inherit the same risk.

**Palantir, 2 Nov (a rule exit the session before a beat and raise)**

- Closed 4.39% below its open on 1.44 times average volume in an AI sell-off, then beat after the close. Sold at the 3 Nov open, so it keeps the gap and gives up any drift; Sequel: it opened -5.70% from its close (-1.14 points at 20%), then rose 4.29% open to close on 2.2 times volume, while ServiceNow rose 3.64% from the same open: the swap cost 0.08 points on day one.

**The five exits of 2 Nov (Nvidia, Shopify, Arm, Sandisk, Cloudflare)**

- On 30 Oct nearly every high-beta tech name on the list, and 10 of 17 large tech names checked through the feed, closed below its open on heavy volume. The rule emptied most of the swap column; the book moved to the few that did not signal (memory and storage, Monolithic Power, Amazon). The 2 Nov change row is the largest test yet of sector-day exits.

**Sandisk, 30 Oct (a beat and raise that fell 13.5%)**

- After a 460% year the bar was too high: revenue and guidance beat, consumer revenue fell 29%, and memory sold off worldwide. Lesson: after a parabolic run, results are a sell-the-news event whatever the figures.

**Coca-Cola, 27 Oct (a beat and raise that fell)**

- Lesson: in a growth rebound, a defensive beat-and-raise does not draw buyers; the reaction test exists for this.

## 11. Confidence ratings, shadow ratings, the panel test and the day call

- Confidence ratings (not calibrated): 24 of 28 settled, few distinct dates: below 55, 5 of 11 beat the index (45%); 55 to 59, 6 of 9 (67%); 60 and above, 4 of 4 (100%, all from the 9 to 15 Oct energy book). Far too few to judge. Ratings for the order in force: Monolithic Power 54, Micron 52, Amazon 52, ServiceNow 50, Seagate 50, Western Digital 50, NetApp 50.
- Shadow ratings: 554 logged, 367 settled. Live: score 70 and above, 152 cases, 56% beat the index (-0.77 points); 60 to 69, 93, 48% (-2.10); 45 to 59, 61, 26% (-3.93); below 45, 61, 56% (-0.10). Not ordered by score. Judgement test: two dates, too few.
- Panel test: see section 1. Old backtest (hindsight) correlation +0.008.
- Drift record: ENTER 1 settled (Hasbro, +7.51 points), 1 open (Labcorp, not taken); WATCH 1 settled (-3.62); FAIL 9 settled (33% beat the index, -1.73 points), 15 open (including Palantir, Shopify, Fiserv, Advanced Energy from 3 Nov).
- Day call record (S&P 500): 10 right of 16. Below the 20 settled calls needed before it could be considered.
- Broad scan record (scan/latest.md, 30 Oct): Leaders, 60 settled, 40% beat the index, mean excess -1.81 points close to close and -1.89 from the next open; Events, 9 settled, 56%, -1.31 and -1.44; 70 rows open.

## 12. Tools

- Tim's page: https://claude.ai/artifact/8P8UwQsb4QsbZMsKNYKrUJ, pinned in his Claude sidebar, with tabs Today, Macro, Performance, Risk, Calendar and Log. It reads four data files (`stocks`, `ledger`, `history`, `macro`) and a fifth dataset, `logos`, that no run touches. The Order panel reads the latest alert whose `stock` is "Order"; its "Enter before" bar uses the 08:00 UK cut-off.
- Playbook docs (version 6.15): `claude/ft-game-playbook.md` (core, with the routing table), `claude/ft-game-rules.md`, `claude/ft-game-data.md`, and the run docs `claude/ft-game-run-evening.md`, `-morning`, `-refresh`, `-weekly`, `-weekend`.
- Panel file: `panel.json` on the same artifact, named by the document `store/panel`.
- Scripts: the pipeline (version 7.8; runs take it from the repository at the commit in data doc G1) and the screening script are assets on that artifact. Their ids and hashes are in part B of the playbook, the only place they are kept.
- Price feed (data doc G8): `feed/latest.json` and `feed/live.json` in the repository, with the non-US 10-year yields under `macro.intl_yields`. 1 Nov: current for Fri 30 Oct, then a forced run at 21:35 UTC for 17 tickers (two years each for the two new holdings). It refused Palantir on a revised low; the stockanalysis.com history page confirmed the revision.
- Pages reached through searches on 3 Nov: TheStreet (closes), Yahoo Finance live page, ZeroHedge, Bank of Vol, investingLive (AMD), SEC (Fiserv 8-K), Grafa and StockStory (Shopify, Advanced Energy), MarketBeat (Bloom), 24/7 Wall St (memory), TIKR (Seagate). Refused or failed: CNBC article pages (site errors); investing.com and 24/7 Wall St's AMD live page (rate limited).
- Market data service: massive.com, free plan, on an account opened by Tim's father. The key is in the evening and weekly review tasks and is never written into this project's docs, the page data, alerts or messages. Not used on 3 Nov (the feed covered every price).
- Sources that did not work: Alphastreet, Chartmill and Rolling Out article pages (29 Oct); Benzinga article pages (28 Oct); CNBC article pages; gurufocus news pages and EBC; CNN article pages; Detroit News; Fortune's Bitcoin price page; capital.com news pages. tradingeconomics' news pages carry no statistics table.
- Artifact leftovers: superseded data assets stay in the store (playbook 6.14.3). 1 Nov evening: 51 MB of 1 GB used, 84 files.
- GitHub mirror: private repository `timzwang/ft-game` (part B and G6).
- Two saved skills, `ft-game-playbook` and `stock-score`, load in scheduled runs; the project docs win where they differ.
