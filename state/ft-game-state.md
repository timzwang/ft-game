# FT Stock Picking Game: state and log

Last updated: Thu 12 Nov 2026, about 21:50 UK (evening review, a quiet evening: no change for Fri 13 Nov's open). Before that, Wed 11 Nov 2026, about 21:50 UK (evening review, quiet). Before that, Tue 10 Nov 2026, about 21:45 UK (evening review, quiet). Before that, Mon 9 Nov 2026, about 21:45 UK (evening review, quiet). Before that, Sat 7 Nov 2026, about 09:30 UK (weekly review). Earlier entries: see the review log (section 6).

This doc is the narrative record for Tim's entry, "Seeking Beta". The procedure for every run is in `claude/ft-game-playbook.md` (the core doc) and the docs its routing table names. The numbers (prices, scores, daily performance, contributions, ratings and their outcomes, the full calendar, analyst changes, alerts, the panel test, the drift record) live in the data files behind Tim's page and the panel file, and are produced by the pipeline script; this doc carries the decisions and the reasons.

Messages: from 10 Oct Tim is sent a message only when there is something for him to enter or answer (playbook part I, "When Tim is told"), and always when there is an issue (part I, "Issues: flag and fix", from 26 Oct). Quiet runs update the page and this doc and send nothing.

Scheduled runs: evening review 21:30 UK Sun to Thu; morning check 07:26 UK Mon to Fri (from Tue 27 Oct; 06:36 from 18 to 26 Oct; playbook 6.14); price refresh 17:04 UK (from 4 Nov; 16:45 until 3 Nov) and late price refresh 19:22 UK Mon to Fri; results-day refresh 14:50 UK Mon to Fri (acts only on results days); weekly performance review Sat 09:12 UK; weekend news check Sat and Sun 20:20 UK; nightly watchdog 22:47 UK every day (from 26 Oct); midday check 12:40 UK Mon to Fri (stops at once by its own instructions; Tim to switch the task off, roadmap item 68).

**Cut-off: every order must be entered before 08:00 UK, UK local time all year (FT Customer Care to Tim, 21 Oct; Tim approved the move back the same night; playbook 6.14 and pipeline 7.8 from 26 Oct). 07:00 UK was used as a safety margin from 17 to 26 Oct.**

## 1. Status

- **Playbook version 6.15.1** (6.15.1, 3 Nov about 23:20: page only, hover details, calendar, log and tables; 6.15, 3 Nov late evening: results-day refresh only for stocks on the list, 17:04 UK price refresh, late refreshes not an issue, watchlist under the stance in core part D, page redesigned; 6.14.3, 29 Oct evening: runs no longer delete superseded data assets, data doc G5 step 4; G5 step 5 checks the store's size instead; 6.14.2, 27 Oct: feed 1.2.1 takes Japan's 10-year from CNBC first; 6.14.1, 26 Oct: the five non-US 10-year yields from the price feed; 6.14, 26 Oct: cut-off 08:00 UK, pipeline 7.8 from commit `9760163`, nightly watchdog 22:47 UK; 6.13.2: flag and fix every issue; 6.13.1: the script run from the repository; 6.13, 21 Oct: the endgame stance in core part D; earlier versions in the playbook header). **Pipeline script version 7.8** (part B holds the asset id, the run commit and the hash). The 12 Nov evening review ran it from commit `9760163` (hash matched part B).
- **Estimated value at Thu 12 Nov close: 84,611, -15.39% since the start, against -2.46% for the S&P 500 fund (gap -12.93 points).** Thu 12 Nov -1.10% against SPY -0.35%: AppLovin -0.55 points, Netflix -0.43, Spotify -0.17, Meta -0.12, Salesforce -0.03, Qualcomm +0.05, NetApp +0.16. Wed 11 Nov +1.51%; Tue 10 Nov -0.84%; Mon 9 Nov +3.00%.
- **Last FT figures: Mon 2 Nov close, 89,956 (-10.04%), rank 11,537 (number of players not recorded; the top 2% line is about rank 307).** Read off the FT site by Tim late on 3 Nov, before it updated. `reported` row with top2_return_pct 10.29 (Cautious, rank 316; Owen'sbigmoney, rank 195, at +11.64%). RECONCILE +142 credits (+0.16%). The pipeline's RANK line still reads the 26 Oct row (3,994 of 14,736), since the 2 Nov row has no player count. From 13 Nov the rank is more than a week old: the Friday review asks Tim for value, rank and players (core part D). Outside the target: keep risk on.
- **Standstill (12 Nov evening review):** change for 30 Oct +0.61, 2 Nov -4.00, 3 Nov -0.45, 5 Nov -1.41, 6 Nov -2.65, all complete. Week of 26 Oct +5.58; week of 2 Nov +0.68; week of 9 Nov 0.00 (no change, four sessions). Inception (25 sessions): -12.94 as entered, -12.08 fully invested. EXPECTED BENEFIT: eight settled, expected 0.0, actual -6.16, sign right in 5 of 8.
- **Panel test (all 30 members loaded):** history verdict "no evidence" (average rank correlation +0.044, t +1.2, 58 dates). Live: four dates (-0.271, t -1.0), too few to judge. Strongest parts in history: one-year return against the index +0.095 (t +1.9), two-month +0.059 (t +1.8), neither at t 2. The score is frozen.
- **Order in force for Fri 13 Nov's open (unchanged by the Thu 12 Nov evening review, a quiet evening; set by the Thu 5 Nov evening review, corrected about 22:10 UK on 5 Nov when Roblox proved not to be in the game):** AppLovin 20, Meta Platforms 15, Qualcomm 15, Netflix 15, Salesforce 15, Spotify 10, NetApp 10, cash 0.
- Day call record (S&P 500): 15 right of 23. Fri 13 Nov's call (Thu 12 Nov review): S&P 500 Green 54% against a usual 55%, portfolio Green 52% against a usual 54%, no reviewer adjustment (yield and oil jumps have tended to precede up days, against PPI on Friday and the book closing near its lows). Close to a coin flip.
- Macro at Thu 12 Nov: US 2-year 4.86% (+13bp; +28bp over five), 10-year 5.10% (+12bp; +20bp over five), 30-year 5.43%. UK 10-year 5.28% (+5bp; +13bp over five), Germany 3.36%, France 4.84%, Italy 4.39%, Japan 2.79% (all from the feed). Brent $96.04 (+3.8%; -2.6% over five), WTI $88.96, natural gas $3.36, gold $3,877 (-2.9%) (futures fallback). Backdrop label: headwind (10-year up 20bp in five sessions).
- Crypto: Bitcoin $71,342 at the Thursday US close (-4.4% on the day, -6.2% over five). Trend **down** (IBIT 9.3% below its 20-day, 11.5% below its 50-day, 1.8% below its 200-day); Ether's trend down. No crypto-linked buy; no crypto-linked holding.
- Regime: mixed. Thu 12 Nov: S&P 500 -0.43% to 7,586.64, Nasdaq -0.61%, Dow -0.35% (24/7 Wall St); Russell 2000 about -1.7%. Jensen Huang resigned as Nvidia's CEO (CFO Colette Kress interim); Nvidia fell as much as 14% early, then closed -4.3% but 10.1% above its open on 4.6 times volume. Money rotated to other chipmakers: Broadcom +5.5%, AMD +5.9% (1.76 times volume), Arista +5.1%. Rate-hike odds weighed on growth (24/7 Wall St; SF Standard). After the close Cisco beat and raised.

## 2. Current portfolio

The order in force for Fri 13 Nov's open (unchanged since Fri 6 Nov). Scores and bands from the pipeline at the Thu 12 Nov close (12 Nov evening review). Under the endgame stance (core part D) the score floor, trend tests, volatility caps, theme guide and results budget do not apply; the NOTE lines for them are expected.

| Stock | Weight | Confidence (not calibrated) | Score | Band | Flags | Next results (implied move) | Swap if missing or broken |
|---|---|---|---|---|---|---|---|
| AppLovin | 20% | 55 | 41 | Weak | downtrend (50-day below 200-day), extended | Reported 4 Nov; next Feb (est.) | Netflix |
| Meta Platforms | 15% | 50 | 29 | Weak | below 50-day | Late Jan (est.) | Spotify |
| Qualcomm | 15% | 50 | 42 | Weak | below 50-day | Reported 4 Nov; next Feb (est.) | Arm Holdings |
| Netflix | 15% | 50 | 16 | Weak | below 50-day, downtrend | Jan (est., after the game) | IBM (20-day volume not checked) |
| Salesforce | 15% | 50 | 29 | Weak | below 50-day | Early Dec (est., after the game) | Spotify |
| Spotify | 10% | 50 | 46 | Middling | none | Feb (est.) | Netflix |
| NetApp | 10% | 50 | 53 | Middling | below 50-day | 25 Nov, after US close (est.; no implied move yet) | Spotify |
| Cash | 0% | | | | | | |

Exit check on Thu 12 Nov (20-day average volume from stored rows): no heavy-volume close below the open. Netflix closed 2.46% below its open on 0.67 times average volume, AppLovin 1.48% below on 0.52 times, Spotify 1.43% below on 0.51 times, Salesforce 0.44% below on 0.51 times, Meta 0.28% below on 0.43 times; NetApp +4.00% from its open, Qualcomm +1.15%. Five holdings closed in the bottom tenth of the day's range, all on light volume.

Themes: Software 75%, AI and chips 25%. Largest risk shares: AppLovin 47%, Qualcomm 18.4%, Meta 13.9%, Netflix 9.6%; estimated daily volatility 1.93%. Worst scenario: a deeper AI sell-off, -6.5%. The concentration is deliberate under the stance.

Points for the coming reviews:

- Still open from 5 Nov: the memory breakdown named in the stance has happened; a change of direction is Tim's call (question 1a). On 12 Nov chips other than Nvidia were bid again (AMD, Broadcom on 1.7 times volume; memory names closed well above their opens on ordinary volume) while the book's software and internet names closed near their lows on light volume. The regime test set on 11 Nov (chips and memory above their opens on heavy volume for a second session) was met only in part, so no change tonight.
- AppLovin: securities class action lead-plaintiff deadline 16 Nov and the SEC inquiry are named risks; watch for a heavy-volume close below the open.
- Netflix: score 16, closed near its low for a second day (light volume). An exit only on the rule.
- Fri 13 Nov: PPI 13:30 UK (+0.4% m/m forecast, core +0.3%). Cisco's reaction session (drift entry on Friday evening's review). Tue 17 Nov: retail sales. Wed 18 Nov: Fed minutes; Nvidia results (est.; one report says Tue 17 Nov, unverified).
- Analyst targets and next-result dates of the holdings were not refreshed on 8 to 12 Nov.
- Candidates if a holding exits: AMD (score 83, 1.76 times volume, third strong close), Arista (73, 6.98% above its open), Texas Instruments (71) and Analog Devices (69), both with low correlation to the order, Broadcom (scan Event).
- Bitcoin's trend is down: no crypto-linked buy.

## 3. Pending order

**Change for Fri 6 Nov's open (Thursday 5 Nov evening review): sell Sandisk 20, ServiceNow 20, Seagate 15, Western Digital 15, AMD 10, Amazon 10; add AppLovin 20, Meta Platforms 15, Qualcomm 15, Netflix 15, Salesforce 15, Spotify 10.** Order: AppLovin 20, Meta Platforms 15, Qualcomm 15, Netflix 15, Salesforce 15, Spotify 10, NetApp 10, cash 0. Message sent about 21:44 UK on 5 Nov; Netflix replaced Roblox about 22:10 UK, Roblox not being in the game (Tim, 5 Nov); Tim confirmed it entered ("Done", 22:09 UK).

## 4. Watchlist

21 names after tonight. Scores and bands at the Thu 12 Nov close. Added tonight: Texas Instruments and Analog Devices (scan Leaders, chips, two years of rows from a forced feed run) and Cisco (beat and raise after the close; drift entry on its reaction session, Fri 13 Nov). Removed: Western Digital and ServiceNow (weak, five sessions after their sale passed). Broadcom, a ROTATE OUT name, is kept as tonight's scan Event. The scan's other Leaders are health care, staples, energy, retail and London names the stance bars.

| Name | Band | Status | Score | Note |
|---|---|---|---|---|
| AMD | Strong | Watching | 83 | +5.86%, 2.81% above its open on 1.76 times volume: third strong close. First candidate if a holding exits. |
| Arista Networks | Strong | Watching | 73 | +5.06%, 6.98% above its open near the high on 1.08 times volume. Promote on a heavy-volume close above its open. |
| Texas Instruments | Strong | Watching (added 12 Nov) | 71 | Scan Leader; correlation with the order +0.08. |
| Analog Devices | Strong | Watching (added 12 Nov) | 69 | Scan Leader, panel member; results late Nov (est., not confirmed). |
| CDW | Strong | Watching | 68 | Extended (15% above its 50-day). |
| Cloudflare | Middling | Watching | 66 | +1.11%, 3.99% above its open on light volume. |
| Cisco | Middling | Drift: day 1 (added 12 Nov) | 61 | Beat and raise after the close (EPS $1.40 against $1.32, revenue $18.5bn against $18.11bn, FY guide raised; Investing.com). |
| Apple | Middling | Watching | 59 | Closed near its low. |
| Microsoft | Middling | Watching | 58 | Flat. |
| Block | Middling | Watching | 58 | -4.04%, near its low. |
| Amazon | Middling | Watching | 53 | Five sessions after its sale passed; kept as a stance name. |
| Palantir | Middling | Watching | 52 | Light volume. |
| Seagate | Middling | Watching | 52 | 2.86% above its open; five sessions after its sale passed. |
| Micron | Middling | Watching | 47 | 3.79% above its open near the high, 0.88 times volume. |
| Sandisk | Middling | Watching | 46 | 5.56% above its open on 1.13 times volume; five sessions after its sale passed. |
| Arm Holdings | Middling | Watching | 46 | 4.95% above its open on light volume. Swap for Qualcomm. |
| Broadcom | Weak | Needs follow-through | 56 | Scan Event: +5.5%, gap +3.4% that held on 1.68 times volume. Downtrend flag. |
| CoreWeave | Weak | Drift FAIL | 38 | -6.86% but 11.2% above its open on 1.43 times volume. Listed since 11 Nov. |
| Nvidia | Weak | Exit signal | 27 | Jensen Huang resigned; Colette Kress interim CEO; RBC target $230 from $330. Closed 10.1% above its open on 4.6 times volume. Reports 18 Nov (est.). |
| Strategy | Weak | Exit signal | 28 | Crypto tracker. |
| Coinbase | Weak | Watching | 28 | Crypto tracker. |

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
| Wed 4 Nov, about 21:39 UK (message sent) | Thu 5 Nov | Sell Micron 20, Monolithic Power 10; add Sandisk 20, AMD 10 | Endgame exit rule: both closed below their opens on 1.34 times average volume on 4 Nov. Micron's swap Sandisk took its weight; Monolithic's swap Analog Devices gave the same signal, so AMD. Expected 0.0 points |
| Thu 5 Nov, about 21:44 UK (message sent) | Fri 6 Nov | Sell Sandisk 20, ServiceNow 20, Seagate 15, Western Digital 15, AMD 10, Amazon 10; add AppLovin 20, Meta Platforms 15, Qualcomm 15, Netflix 15, Salesforce 15, Spotify 10 (Netflix replaced Roblox, not in the game, about 22:10 UK) | Endgame exit rule: all six closed below their opens on heavy volume on 5 Nov (1.33 to 3.30 times average). Nearly every swap and large tech name gave the same signal, so the weight went to high-beta names without one; Oracle passed over at 1.30 times. NetApp kept at 1.18 times. Expected 0.0 points |

## 6. Review log (newest first, keep the latest 15)

- Thu 12 Nov 2026 (about 21:50): Evening review, a quiet evening: no change for Fri 13 Nov's open (no holding closed below its open on heavy volume; Netflix -2.46% from its open on 0.67 times). 12 Nov -1.10% against SPY -0.35%, value 84,611. Started 21:31 UK, on time. Pipeline 7.8 from commit `9760163`, hash matched. Price feed: forced (scheduled run at 20:58 UTC still on 11 Nov; forced run generated 21:33 UTC, again 21:36 UTC for TXN, ADI, CSCO, two years each), nothing refused or missing. Non-US yields from the feed; commodities from the futures fallback. Broad scan: forced (3 Events, 30 Leaders). Drift: no reporter on the list tonight; Cisco and Applied Materials reported after the close (reaction session Friday). Added Texas Instruments, Analog Devices, Cisco; removed Western Digital, ServiceNow. Files published (store 172 MB, 195 files; no deletes). WARNINGs: APP 2024-11-07, CRWV 2025-04-01, known. Pages not read: Crypto Briefing (Applied Materials) and JournalArta (client errors). Research much lighter than the usual 25 to 40 sources (four pages and five searches); Applied Materials' figures, VIX close, jobless claims actual and holdings' targets not read. No ISSUE this run.
- Wed 11 Nov 2026 (about 21:50): Evening review, a quiet evening: no change for Thu 12 Nov's open (no holding closed below its open on heavy volume; Meta -2.78% from its open on 0.64 times). 11 Nov +1.51% against SPY +1.32%, value 85,548. Started 21:32 UK, on time. Pipeline 7.8 from commit `9760163`, hash matched. Price feed: current (generated 21:34 UTC), then forced at about 21:36 UTC for CRWV and ANET (409 and 551 rows), nothing refused or missing. US Treasury yields carried (bond market closed for Veterans Day). Non-US yields from the feed; commodities from the futures fallback. Broad scan: forced (1 Event, 30 Leaders). Drift: CoreWeave FAIL 5 of 6 (trend). Added CoreWeave, Arista Networks; removed Monolithic Power, Coherent, Shopify. Files published (store 160 MB, 185 files; no deletes). WARNINGs: APP 2024-11-07, BE 2024-11-15 known; CRWV 2025-04-01 (+41.8%, its post-IPO surge), believed genuine. Page not read: CNBC's CoreWeave article (client error). Research much lighter than the usual 25 to 40 sources (three pages and two searches); analyst changes beyond Nvidia's and holdings' targets not read; VIX not read. No ISSUE this run.
- Tue 10 Nov 2026 (about 21:45): Evening review, a quiet evening: no change for Wed 11 Nov's open (no holding closed below its open on heavy volume; AppLovin -2.49% from its open on 0.95 times). 10 Nov -0.84% against SPY -0.37%, value 84,275. Started 21:31 UK, on time. Pipeline 7.8 from commit `9760163`, hash matched. Price feed: forced (scheduled run still on 9 Nov; forced run generated 21:32 UTC, again 21:35 UTC for TTWO), nothing refused or missing. Non-US yields from the feed; commodities from the futures fallback. Broad scan: forced (1 Event, 30 Leaders). Drift: Take-Two FAIL (beat missing: bookings below consensus, EPS bases differ; guidance reaffirmed; below its 200-day). No additions or removals. CPI actual stored. Files published (store 149 MB, 175 files; no deletes). WARNINGs: APP 2024-11-07, FLEX 2026-05-06, BE 2024-11-15, known. Pages not read: StreetInsider (AppLovin), Benzinga (CoreWeave), Chartmill (Take-Two) (client errors). Research much lighter than the usual 25 to 40 sources (about eight pages and searches); analyst changes and holdings' targets not read; CoreWeave after-hours move not read. No ISSUE this run.
- Mon 9 Nov 2026 (about 21:45): Evening review, a quiet evening: no change for Tue 10 Nov's open (every holding closed above its open). 9 Nov +3.00% against SPY +2.37%, value 84,991. Started 21:32 UK, on time. Pipeline 7.8 from commit `9760163`, hash matched. Price feed: forced (scheduled run at 21:00 UTC still on 6 Nov; forced run generated 21:33 UTC), nothing refused or missing. Non-US yields from the feed; commodities from the futures fallback. Broad scan: forced (5 Events, 30 Leaders). Drift: no reporter on the list or among the stance-eligible Events tonight (Constellation Energy, Ferguson, Franklin Resources outside the stance), so no entries. Added Broadcom; no removals. Files published (store 138 MB, 165 files; no deletes). WARNINGs: APP 2024-11-07, FLEX 2026-05-06, BE 2024-11-15, known. Page not read: Benzinga's trending-stocks page (client error). Research much lighter than the usual 25 to 40 sources (four pages and searches); analyst changes beyond AMD's upgrade and holdings' targets not read; CoreWeave implied move not read. No ISSUE this run.
- Sun 8 Nov 2026 (about 21:45): Evening review, a quiet evening: no change for Mon 9 Nov's open (no holding closed below its open on heavy volume on 6 Nov; NetApp -3.31% from its open on 1.00 times volume). No new session (Friday logged by the weekly review). Started 21:33 UK, on time. Pipeline 7.8 from commit `9760163`, hash matched. Price feed: current (Fri 6 Nov), then forced at 21:35 UTC for Coherent (549 rows, two years), nothing refused or missing. Non-US yields from the feed; commodities from the futures fallback. Broad scan: current (4 Events, 30 Leaders). Drift: Cloudflare FAIL (held; volume and trend missing from the feed). Added Coherent; removed Datadog, Broadcom, Alphabet. Week's calendar stored (CPI and PPI forecasts, bond market closed 11 Nov, CoreWeave, Cisco, Applied Materials). Files published (store 126 MB, 155 files; no deletes). WARNINGs: APP 2024-11-07, FLEX 2026-05-06, BE 2024-11-15, known. Weekend B items confirmed from AND Magazine's 8 Nov brief (citing Al Jazeera, CENTCOM, CNN). Page not read: straits.live (client error). Research lighter than the usual 25 to 40 sources; analyst changes and holdings' targets not read. No ISSUE this run.
- Sun 8 Nov 2026 (about 20:30): Weekend news check (Sunday). No A item; one B item (Sunday escalation in Hormuz: the IRGC says three tankers caught fire, CENTCOM disabled the M/V Huda, the IRGC lifted its 2,000 km missile range limit, missiles over Riyadh and an Aramco office damaged; against that, Trump told CNN new strikes are "highly unlikely" if talks progress and Araghchi said Iran's Hormuz proposal stands). Saudi TASI -0.52%; IG Weekend Wall Street -0.1%. Pipeline 7.8 from commit `9760163`, hash matched; one alert added through `refresh`, ledger published (store 122 MB, 152 files; no deletes). Page not read: Al Arabiya (client error; the same story read on Gulf News). No ISSUE this run. Order unchanged.
- ISSUE (7 Nov weekend news check, about 20:24 UK; fixed): the first state doc write was refused, "project_write: local_path must be inside the working directory" (the file was in /home/claude/ft-game-work, outside the working directory /home/claude/ft-game). Fixed by writing from work/ft-game-state.md inside it.
- Sat 7 Nov 2026 (about 20:25): Weekend news check (Saturday). No A item; one B item (Trump confirmed "minor" US strikes on Qeshm Island and said Iran wants a deal; Iran's seven conditions for reopening Hormuz; CENTCOM's Task Force Iron Gate). Pipeline 7.8 from commit `9760163`, hash matched; one alert added through `refresh`, ledger published (store 120 MB, 151 files; no deletes). Pages not read: straits.live and iransitrep.com (client errors). One ISSUE (state doc write, fixed). Order unchanged.
- Sat 7 Nov 2026 (about 09:30): Weekly review. Fri 6 Nov logged from the price feed (current, generated 21:52 UTC 6 Nov; nothing refused or missing; panel topped up, all 30 members current): +7.89% against SPY +0.31%, value 82,513; week -12.11% against SPY -2.70%. Pipeline 7.8 from commit `9760163`, hash matched. Non-US yields from the feed; commodities from the futures fallback. Jobs report actual stored (165K, 4.1%). Files published (store 118 MB, 150 files; no deletes). WARNINGs: APP 2024-11-07, FLEX 2026-05-06, BE 2024-11-15, known. Not done here, for the Sunday review: Cloudflare's drift row (reaction day 6 Nov, +9.9%). Order unchanged; message to Tim with the review and a request for FT figures. No ISSUE this run.
- Thu 5 Nov 2026 (about 22:15): Session with Tim. Roblox is not in the game. AppLovin, its listed swap, is already at the 20% limit, so Netflix 15 took its place (fell 1.25% on 1.06 times volume; lower beta than Roblox). Pipeline re-run from the evening's inputs and files republished. Portfolio call now Red 48%. Tim confirmed the corrected order entered at 22:09 UK.
- Thu 5 Nov 2026 (about 21:50): Evening review, a change evening for Fri 6 Nov (six rule exits; AppLovin 20, Meta 15, Qualcomm 15, Roblox 15 (replaced by Netflix at 22:10), Salesforce 15, Spotify 10 in, NetApp kept). 5 Nov -13.25% against the S&P 500 -4.4%, value 76,478. Pipeline 7.8 from commit `9760163`, hash matched. Price feed: forced (first read 4 Nov; forced run 21:32 UTC, again 21:41 UTC for 37 tech tickers), nothing refused or missing. Non-US yields from the feed; commodities from the futures fallback. Broad scan: forced (2 Events, 30 Leaders). Drift: AppLovin FAIL 5 of 6 (trend), Arm FAIL, Qualcomm FAIL. Order message sent about 21:44 UK; a first draft of the order held Oracle on a nine-session volume figure, corrected to Salesforce before the message when the 20-day figure read 1.30. Files published (no deletes; store 100 MB, 135 files). WARNINGs: FLEX 2026-05-06 and BE 2024-11-15 known; APP 2024-11-07 (+46.3%) from the feed's new two-year history, believed genuine, not re-checked. Research lighter than the usual 25 to 40 sources. Pages not read: KRMG, CNBC's live page and BoE page, Benzinga's memory page, StockTitan, Invezz, Stockhouse, FinancialContent (errors), 247wallst's Cloudflare page (permission request not answered), Investing.com (rate limited). Not read: Qualcomm's revenue against consensus, Arm's guidance, analyst changes, the new names' targets and next-result dates. No ISSUE this run.
- Wed 4 Nov 2026 (about 21:45): Evening review, a change evening for Thu 5 Nov (Micron, Monolithic Power out; Sandisk 20, AMD 10 in). 4 Nov -3.76% against SPY +1.65%, value 88,163. Pipeline 7.8 from commit `9760163`, hash matched. Price feed: forced (first read 3 Nov; forced run 21:33 UTC, again 21:36 UTC for XYZ, CDW, DASH, AVGO, GOOGL, AAPL), nothing refused or missing. Non-US yields from the feed; commodities from the futures fallback. Broad scan: forced (30 Events, 30 Leaders). Drift: AMD, Datadog, Block, CDW all FAIL (Block and CDW on a missing consensus, not read). Watchlist cleaned per 6.15. Order message sent about 21:39 UK. Files published (no deletes). WARNINGs for FLEX 2026-05-06 and BE 2024-11-15: known. Research lighter than the usual 25 to 40 sources. Pages not read: Benzinga's AMD page, Arm's newsroom, Invezz (client errors), FX Leaders (robots). VIX, Russell 2000 close and ISM forecast not read; analyst changes not read tonight. No ISSUE this run.
- Tue 3 Nov 2026 (about 23:30): Session with Tim. FT figures for the 2 Nov close stored in the ledger (89,956, rank 11,537). Order unchanged.
- Tue 3 Nov 2026 (about 23:20): Session with Tim. Playbook 6.15.1, page only: hover details, calendar, log and tables. Order unchanged.
- Tue 3 Nov 2026 (about 23:00): Session with Tim. Playbook 6.15, page redesigned. Exit rule tested on stored prices: no change (roadmap item 69). Order unchanged. No open ISSUE; the midday task still to be switched off by Tim.

## 7. Market regime notes

Label: Mixed (Thu 12 Nov: Nvidia's CEO resigned and the 2-year jumped 13bp, but money rotated into other chipmakers on heavy volume; S&P 500 -0.43%). What would change it: to risk-on, a cool PPI and chips again closing above their opens on heavy volume; to risk-off, a hot PPI that lifts the 2-year towards 5%.

Thu 12 Nov: S&P 500 -0.43% to 7,586.64, Nasdaq -0.61%, Dow -0.35% (24/7 Wall St closing bell); rate-hike odds weighed on growth. Russell 2000 about -1.7%. Nvidia: Jensen Huang resigned after reports of affairs including one with a subordinate, following the board's investigation; CFO Colette Kress interim CEO; RBC cut its target to $230 from $330; shares down as much as 14% early, closed -4.3% (SF Standard, Forbes, CNBC headline). Broadcom +5.5%, AMD +5.3%, Arista +4.6% (24/7 Wall St). 2-year 4.86% (+13bp), 10-year 5.10% (+12bp) (Treasury via the feed). Brent $96.04 (+3.8%, futures). After the close: Cisco Q1 EPS $1.40 against $1.32, revenue $18.5bn (+24%) against $18.11bn, Q2 and FY27 guides above consensus, AI infrastructure revenue from hyperscalers raised to $9bn; shares up about 4% after hours (Investing.com). Applied Materials reported after the close (figures not read).

Wed 11 Nov: S&P 500 +1.29%, Nasdaq +1.55%, Dow +0.48% (24/7 Wall St closing bell; its ticker bar gave the S&P 500 at 7,628 and the Russell 2000 at 2,848, +0.79%). US bond market closed (Veterans Day). CoreWeave +24% to about $60.5: Q3 revenue $3.66bn (+168%) against $3.54bn, loss $1.27 a share against $1.55, FY26 revenue guide raised to $13.0bn to $13.3bn, adjusted operating income guide $1.275bn to $1.375bn against $1.07bn expected (TheStreet, Forbes, 24/7 Wall St). Sandisk +13.7%, Arm +12.1%, Micron +11.9%, Dell +11.9%, Bloom Energy +12.5% (24/7 Wall St). Nvidia +2.9%: Baird downgraded to Neutral and cut its target to $200 from $500; Morgan Stanley dropped it as a top pick (TheStreet). Fed: a December hike almost fully priced, a half point about 11% (TheStreet). Iran said it will not remove "a single particle" of enriched material; a tanker reportedly hit a mine in Hormuz (TheStreet). Brent $92.53 (futures).

Tue 10 Nov: S&P 500 -0.4% to 7,520, Nasdaq -0.7% to 25,065, Dow -0.3% to 52,231 (Kiplinger). October CPI +0.4% m/m against +0.3% forecast, core +0.3% against +0.2%; the BLS did not publish 12-month rates (HNGN). 10-year 4.98%, 2-year 4.73% (Treasury). CME FedWatch 90% for a December quarter-point hike, 10% for a half point; Waller floated a half point, Logan two more quarter points (Kiplinger, HNGN). Nvidia -5.5% on 3.1 times volume, down nearly 30% since early October, over the investigation of its chief executive; Anthropic's IPO pricing (825m shares at $70 to $78) weighed on tech (Kiplinger). Chips mixed: Broadcom +3.9%, Cloudflare +4.1%, Qualcomm +1.2%, AMD +1.3%. AppLovin -3.5% on profit-taking after a six-day 79% run (TradingKey, Trefis). Take-Two +8.3% on its GTA VI date (19 Nov) despite a bookings miss. Brent -0.9% to $91.98 (futures) as Trump held off new Iran strikes (TheStreet). After the close: CoreWeave beat and raised (24/7 Wall St).

Mon 9 Nov: S&P 500 +2.35% to 7,549.94, Nasdaq +2.74%, Dow +2.15% (+1,104 points), Russell 2000 +3.17%; VIX 20.02. First day since 5 April with all three indexes up 2% or more (Kiplinger). Dip buying after last week's rout; AMD +13.3% (Oppenheimer upgrade), Micron +6.3%, Sandisk +6.2%, Monolithic Power +16.6%, Coherent +16.8%, Constellation Energy +10.5%. Nvidia -4.3% on 3.9 times volume: its board opened an independent investigation of Jensen Huang over a relationship with an executive US officials link to Chinese intelligence; the board says it has no reason to believe secrets were compromised (TheStreet via Yahoo). Brent -5.2% to about $93 on Trump calling new strikes "highly unlikely" while talks progress, despite fresh shipping attacks (Reuters via GV Wire). Take-Two -3.5% before its results.

Fri 6 Nov: S&P 500 +0.31%, Nasdaq +1.09%, Dow -0.46% (The Closing Print). Chips rebounded (index +4.2%, AMD +11.0%, Nvidia +2.8%, Micron +5.1%) after Thursday's rout; jobs 165K against 59K pushed yields up 2bp; Cloudflare +9.9% on a beat and Q4 guide of $845m to $846m; Salesforce -3.9%. Week: S&P 500 -2.68%, Nasdaq -3.37%, WTI -13.2%.

Thu 5 Nov: S&P 500 -4.4%, Dow -3.4%, Nasdaq -5.5% (AP). Reasons given: Democratic wins raising the chance of pauses on data-centre building, costlier borrowing and bubble talk (AP); Rep. Ansari's call for a pause on advanced AI (24/7 Wall St); UBS on nearly a third of 2028 US capacity at risk (Motley Fool). Vanda: largest retail net selling since 17 March 2020, with forced selling by systematic and leveraged strategies; Nomura: hedge funds locking in profits (Yahoo). Nvidia -9.3%, AMD -17.3%, AppLovin +31%. Brent +3.9% (AP); 10-year 4.84%. Bank of England raised to 4% from 3.75%, eight for a quarter point and one for a half (Euronews). Kospi -5.3%, Nikkei -1.8%, FTSE 100 -0.4% (AP). Hormuz: more tankers hit (US News). After the close: Cloudflare revenue $782.5m, a beat.

Wed 4 Nov: S&P 500 +1.58%, Dow +3.03%, Nasdaq +1.44% (TradingKey); chip index -3.13% (TradingKey) or -3.84% (Econcurrents). Democrats won both chambers. Brent about -9% (Reuters at midday, -8.9%). ADP +86k against +69k; ISM services 54.5 (September 54.9). Seagate -8.13%, Sandisk -7.91%, Micron -7.00%, WDC -6.77%, on a slower-AI-build read (TIKR), Kioxia's forecast and Texas data-centre moratorium fears (24/7 Wall St). Datadog -14.4% after a beat with an in-line Q4 guide. Block +15.3%, raised guide. After the close: Arm revenue $1.44bn against $1.38bn, EPS $0.52 against $0.47, -1.8%; Qualcomm EPS $2.17 against $2.16.

Tue 3 Nov: S&P 500 about +0.36%, Nasdaq +0.83%, Dow -0.38%, Russell 2000 +0.24%; VIX 21.27 (Bank of Vol). Apple -4.4%: gross margin guide 45% to 46% against 47%, memory costs; its CEO called memory pricing "unprecedented" and rising beyond December. Palantir -1.65% (gap -5.70%). Shopify -8.74% (gap -12.67%): GMV $119.15bn against $120.08bn. Fiserv +12.5%. Bloom Energy on Barclays upgrade. AMD after the close: revenue about $13.4bn against $13.1bn, EPS about $2.10 against $1.95, Q4 guide about $17bn against $16.3bn, margin guide 55% against 55.5%. JOLTS little changed (forecast 7,164k; figure not read). A December Fed hike about 75% priced (Bank of Vol).

Mon 2 Nov: S&P 500 -0.51%, Nasdaq -1.07%, Dow +0.41%, Russell 2000 -0.21%. Kioxia guided December-quarter operating profit to 2 trillion yen, below estimates, blaming shipment timing, and said next year's output has sold out. Marvell -12.7% and Lumentum -18.6% on Marvell's $115bn all-stock deal, read by Citrini's Jukan as a sign of an AI collapse in two to three years; Oracle down on a $20bn capital raise. ISM manufacturing 55.5 (forecast 54.5), prices paid 75.2. Palantir after the close: revenue $2.31bn (+96%), FY guide about $8.53bn, contract value +6%. Idexx +21.9% on a beat and raise.

Fri 30 Oct: S&P 500 -1.83%, Nasdaq -2.84%, Dow -1.06%; SPY -1.77%; S&P 500 futures settled -1.8%, Nasdaq 100 futures -3.5% (Regards of Wall Street, last 6:40pm ET). Intel -29%; Dell -11% and HP lower on Intel's PC outlook (units -12% in 2026, -10% in 2027, blamed on memory shortages); Amazon EPS $1.89 and revenue $201.9bn, both below consensus, AWS +39%, opened about 5% down and closed -1.4%; Qualcomm -11%; Marvell -10%. Memory: Sandisk -13.5% (beat: revenue $11.03bn against $10.7bn, EPS $49.51 against $47.15; Q2 EPS guide $55 to 57 against $54.69; consumer revenue -29%), WDC -7.4%, Seagate -8.0%, Micron -5.3% (24/7 Wall St: profit-taking after a 460% year, Samsung -6% and Kospi -5%). Q3 employment cost index +0.8% (in line).

Thu 29 Oct: S&P 500 about -0.3%, Nasdaq about -1.4%. Q3 GDP 3.4% annualised; September PCE 3.6% on the year. Alphabet -12.6%, ServiceNow about -20%, Eli Lilly +6.4%.

Wed 28 Oct: S&P 500 +0.28% (a record). Fed held at 3.75% to 4.00%, 10-2. Tue 27 Oct: S&P 500 +0.60%. Mon 26 Oct: S&P 500 +0.70%.

Weekend log (weekend of 7 and 8 Nov): Sat 7 Nov (check at about 20:20 UK): no A item. B: Trump confirmed limited US strikes on an Iranian air-defence site on Qeshm Island, calling them "minor", and said Iran "desperately" wants a deal (RFE/RL, 7 Nov 13:26 CET); Iran's army set seven conditions (sanctions lifted, assets released, reparations) before Hormuz reopens, the IRGC Navy says the strait stays closed; CENTCOM formed Task Force Iron Gate to reinforce the blockade (RFE/RL, 7 Nov 15:47 CET). Two-sided: scenario "Oil spike on escalation" -2.0 points, "Ceasefire or Hormuz reopening" +2.0. C: Brent settled $98.32 on Fri, -16% on the week. Prices: IG Weekend Wall Street +0.01%, noise; Bitcoin about $76,040.
Sun 8 Nov (check at about 20:20 UK): no A item. B: Sunday escalation in Hormuz against talk of a deal. The IRGC said three tankers caught fire in the strait (UKMTO: one 8 nm NW of Khasab); CENTCOM disabled the M/V Huda at the blockade; the IRGC lifted its 2,000 km missile range limit; missiles intercepted over Riyadh, an Aramco office damaged by debris (Gulf News, Iran International, ABC, 8 Nov). Against that, Trump told CNN fresh strikes are "highly unlikely" if the two sides sign a strong deal (Reuters via Daily Maverick) and Araghchi said Iran's Hormuz reopening proposal stays on the table (AzerNews). TASI -0.52%; IG Weekend Wall Street -0.1%, Weekend US Tech 100 -0.2%. US CPI Tue 10 Nov the week's main event.
Confirmed by the 8 Nov evening review (AND Magazine brief, 8 Nov 17:34 UTC, citing Al Jazeera, CENTCOM, CNN and Khaleej Times): Task Force Iron Gate, the M/V Huda, the IRGC's tanker claims, the missile range remark (dated 7 Nov) and the Riyadh interceptions; Qatar's mediation continues with no breakthrough, Iran's proposal via Pakistan sets the nuclear issue aside and the US wants it included. Built into the read as two-sided; no reviewer adjustment to the day call. No Sunday oil futures price seen at review time (they reopen at 23:00 UK).
Earlier weekends: 31 Oct and 1 Nov, no A item (B items on US strike threats against Iran, Hormuz tanker attacks and the Doha talks); 24 and 25 Oct, no A item; 17 and 18 Oct, no A item.

Near calendar (the full calendar to 27 Nov is on the page and in the ledger):
- Thu 12 Nov: Nvidia CEO resigned; Cisco beat and raised after the close. Fri 13 Nov: PPI 13:30 UK (+0.4% m/m forecast, core +0.3%). Tue 17 Nov: retail sales. Wed 18 Nov: Fed minutes; Nvidia (est.). Wed 25 Nov: GDP and PCE; NetApp (est.). Thu 26 Nov: US closed. Fri 27 Nov: US closes 18:00 UK, game ends.

## 8. Open questions for Tim

Answered: an order entered before 08:00 UK counted for that day up to 23 Oct; the midday check stays off; the leaderboard shows only the top 10; Shell filled at its 08:00 open on 9 Oct; Microsoft, Coca-Cola, Palantir, Goldman Sachs, Meta Platforms and Eli Lilly are in the game's list; the orders for 13 to 16 Oct were entered; GitHub access from scheduled runs; the cut-off after the clock change (08:00 UK local time all year); the fetch tool refusing built addresses (answered by the price feed); Marsh & McLennan stays in the panel; order B entered (21 Oct); whether the 23 Oct order was entered as sent; the 27 Oct order entered (26 Oct, 22:52 UK).

Still open:
1. Roblox is not in the game's list (Tim, 5 Nov). The order for 6 Nov was entered with AppLovin, Meta, Qualcomm, Netflix, Salesforce, Spotify and NetApp, so taken as all in the list.
1a. Whether to stay on the memory-led stance now that its stated breakdown has happened (raised in tonight's message; the exit rule has already moved the book out of memory).
2. How a mixed London and US order entered for 26 Nov fills: Tim to ask FT help. Only matters if a London stock is bought: the book is all US.
3. Does the game convert US stocks' returns into pounds? The closing gap has stayed under 0.1%.
4. FT value, rank and players at the latest close: the 2 Nov figures are stored without the number of players; a fresh set after a US close, with the players, is still wanted.

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

**The rout of 5 Nov (the book as it was bought)**

- Sandisk, rebought at the open as Micron's swap, closed 16.19% below that open: -3.24 points in one session. Lesson: a swap in the same theme is not an exit from the theme's risk. Whether this rule helps on sector-wide days is for a session with Tim to look at, from the 2 Nov, 5 Nov and 6 Nov change rows.

## 11. Confidence ratings, shadow ratings, the panel test and the day call

- Confidence ratings (not calibrated): 39 of 42 settled (six more on 12 Nov; figures below from 11 Nov), few distinct dates: below 55, 6 of 19 beat the index (32%); 55 to 59, 6 of 9 (67%); 60 and above, 4 of 5 (80%, all from the 9 to 15 Oct energy book). Far too few to judge. Ratings for the order for 6 Nov: AppLovin 55; Meta, Qualcomm, Netflix, Salesforce, Spotify, NetApp 50.
- Shadow ratings: 727 logged. Live: score 70 and above, 195 cases, 52% beat the index (-1.31 points); 60 to 69, 128, 41% (-3.76); 45 to 59, 110, 27% (-5.49); below 45, 149, 34% (-3.61). Not ordered by score. Judgement test: three dates, too few (price and session points +0.155, t +2.2; judgement points -0.045).
- Panel test: see section 1. Old backtest (hindsight) correlation +0.008.
- Drift record: ENTER 2 settled (100% beat the index, +5.55 points); WATCH 1 settled (-3.62); FAIL 31 settled (48%, +0.21 points), 3 open.
- Day call record (S&P 500): 15 right of 23. Twenty-three calls have now settled; whether that beats always saying green is for the weekly review to report, and any use needs Tim's agreement.
- Broad scan record (scan/latest.md, 6 Nov): Leaders, 110 settled, 35% beat the index, -3.81 close to close, -3.67 from the next open (first appearances 34, 32%, -3.81); Events, 29 settled, 69%, +1.34 and +0.76 (first appearances 28, 71%, +1.31 from the next open); 70 open. Previous (30 Oct): Leaders, 60 settled, 40% beat the index, mean excess -1.81 points close to close and -1.89 from the next open; Events, 9 settled, 56%, -1.31 and -1.44; 70 rows open.

## 12. Tools

- Tim's page: https://claude.ai/artifact/8P8UwQsb4QsbZMsKNYKrUJ, pinned in his Claude sidebar, with tabs Today, Macro, Performance, Risk, Calendar and Log. It reads four data files (`stocks`, `ledger`, `history`, `macro`) and a fifth dataset, `logos`, that no run touches. The Order panel reads the latest alert whose `stock` is "Order"; its "Enter before" bar uses the 08:00 UK cut-off.
- Playbook docs (version 6.15.1): `claude/ft-game-playbook.md` (core, with the routing table), `claude/ft-game-rules.md`, `claude/ft-game-data.md`, and the run docs `claude/ft-game-run-evening.md`, `-morning`, `-refresh`, `-weekly`, `-weekend`.
- Panel file: `panel.json` on the same artifact, named by the document `store/panel`.
- Scripts: the pipeline (version 7.8; runs take it from the repository at the commit in data doc G1) and the screening script are assets on that artifact. Their ids and hashes are in part B of the playbook, the only place they are kept.
- Price feed (data doc G8): `feed/latest.json` and `feed/live.json` in the repository, with the non-US 10-year yields under `macro.intl_yields`. 1 Nov: current for Fri 30 Oct, then a forced run at 21:35 UTC for 17 tickers (two years each for the two new holdings). It refused Palantir on a revised low; the stockanalysis.com history page confirmed the revision.
- Pages reached through searches on 12 Nov: 24/7 Wall St (closing bell), SF Standard (Nvidia), Investing.com (Cisco), 5paisa (oil). Refused or failed: Crypto Briefing (Applied Materials), JournalArta (client errors).
- Pages reached through searches on 11 Nov: TheStreet (live blog), 24/7 Wall St (closing bell), Forbes (CoreWeave). Refused or failed: CNBC's CoreWeave article (client error).
- Pages reached through searches on 10 Nov: Kiplinger, HNGN, TheStreet (live blog), TradingKey (AppLovin), 24/7 Wall St (CoreWeave card), Yahoo Finance (Take-Two). Refused or failed: StreetInsider, Benzinga, Chartmill (client errors).
- Pages reached through searches on 9 Nov: Kiplinger, Yahoo Finance (TheStreet market article), 24/7 Wall St, GV Wire (Reuters oil). Refused or failed: Benzinga (client error).
- Pages reached through searches on 8 Nov: Cloudflare's release, 24/7 Wall St (Cloudflare card; Coherent), Trefis (Coherent), Vanderbilt Report and FXEmpire (week ahead), AND Magazine (weekend brief). Refused or failed: straits.live (client error).
- Pages reached through searches on 5 Nov: AP via VIN News, Yahoo Finance live page, 24/7 Wall St (memory), Kiplinger, Euronews, Motley Fool, JournalArta, TokenPost, StockStory (AppLovin). Search snippets only: US News, Al Jazeera, Gulf News, tech-insider, Cryptobriefing and StockStory (Cloudflare). Refused or failed: KRMG, CNBC, Benzinga, StockTitan, Invezz, Stockhouse, FinancialContent, Futu (no content), 247wallst's Cloudflare page, Investing.com (rate limited).
- Pages reached through searches on 4 Nov: TradingKey, Econcurrents, TheStreet, TIKR, 24/7 Wall St, Star-Advertiser (Reuters), KFGO (Reuters), StockStory, StockTitan, Seeking Alpha, SEC (CDW 8-K), forexfundamentals, financecalendar. Refused or failed: Benzinga's AMD page, Arm's newsroom, Invezz (client errors), FX Leaders (robots).
- Pages reached through searches on 3 Nov: TheStreet (closes), Yahoo Finance live page, ZeroHedge, Bank of Vol, investingLive (AMD), SEC (Fiserv 8-K), Grafa and StockStory (Shopify, Advanced Energy), MarketBeat (Bloom), 24/7 Wall St (memory), TIKR (Seagate). Refused or failed: CNBC article pages (site errors); investing.com and 24/7 Wall St's AMD live page (rate limited).
- Market data service: massive.com, free plan, on an account opened by Tim's father. The key is in the evening and weekly review tasks and is never written into this project's docs, the page data, alerts or messages. Not used on 3 Nov (the feed covered every price).
- Sources that did not work: Alphastreet, Chartmill and Rolling Out article pages (29 Oct); Benzinga article pages (28 Oct); CNBC article pages; gurufocus news pages and EBC; CNN article pages; Detroit News; Fortune's Bitcoin price page; capital.com news pages. tradingeconomics' news pages carry no statistics table.
- Artifact leftovers: superseded data assets stay in the store (playbook 6.14.3). 12 Nov evening: 172 MB of 1 GB used, 195 files.
- GitHub mirror: private repository `timzwang/ft-game` (part B and G6).
- Two saved skills, `ft-game-playbook` and `stock-score`, load in scheduled runs; the project docs win where they differ.
