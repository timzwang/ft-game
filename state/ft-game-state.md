# FT Stock Picking Game: state and log

Last updated: Thu 5 Nov 2026, about 22:15 UK (session with Tim: Roblox is not in the game, replaced by Netflix). Before that, Thu 5 Nov 2026, about 21:50 UK (evening review, a change evening for Fri 6 Nov's open). Before that, Wed 4 Nov 2026, about 21:45 UK (evening review, a change evening). Before that, Tue 3 Nov 2026, about 23:30 UK (session with Tim: FT figures for the 2 Nov close stored; order unchanged). Before that, Tue 3 Nov 2026, about 21:45 UK (evening review, a quiet evening: no change for Wed 4 Nov's open). Before that, Mon 2 Nov 2026, about 21:45 UK (evening review, a change evening). Earlier entries: see the review log (section 6).

This doc is the narrative record for Tim's entry, "Seeking Beta". The procedure for every run is in `claude/ft-game-playbook.md` (the core doc) and the docs its routing table names. The numbers (prices, scores, daily performance, contributions, ratings and their outcomes, the full calendar, analyst changes, alerts, the panel test, the drift record) live in the data files behind Tim's page and the panel file, and are produced by the pipeline script; this doc carries the decisions and the reasons.

Messages: from 10 Oct Tim is sent a message only when there is something for him to enter or answer (playbook part I, "When Tim is told"), and always when there is an issue (part I, "Issues: flag and fix", from 26 Oct). Quiet runs update the page and this doc and send nothing.

Scheduled runs: evening review 21:30 UK Sun to Thu; morning check 07:26 UK Mon to Fri (from Tue 27 Oct; 06:36 from 18 to 26 Oct; playbook 6.14); price refresh 17:04 UK (from 4 Nov; 16:45 until 3 Nov) and late price refresh 19:22 UK Mon to Fri; results-day refresh 14:50 UK Mon to Fri (acts only on results days); weekly performance review Sat 09:12 UK; weekend news check Sat and Sun 20:20 UK; nightly watchdog 22:47 UK every day (from 26 Oct); midday check 12:40 UK Mon to Fri (stops at once by its own instructions; Tim to switch the task off, roadmap item 68).

**Cut-off: every order must be entered before 08:00 UK, UK local time all year (FT Customer Care to Tim, 21 Oct; Tim approved the move back the same night; playbook 6.14 and pipeline 7.8 from 26 Oct). 07:00 UK was used as a safety margin from 17 to 26 Oct.**

## 1. Status

- **Playbook version 6.15.1** (6.15.1, 3 Nov about 23:20: page only, hover details, calendar, log and tables; 6.15, 3 Nov late evening: results-day refresh only for stocks on the list, 17:04 UK price refresh, late refreshes not an issue, watchlist under the stance in core part D, page redesigned; 6.14.3, 29 Oct evening: runs no longer delete superseded data assets, data doc G5 step 4; G5 step 5 checks the store's size instead; 6.14.2, 27 Oct: feed 1.2.1 takes Japan's 10-year from CNBC first; 6.14.1, 26 Oct: the five non-US 10-year yields from the price feed; 6.14, 26 Oct: cut-off 08:00 UK, pipeline 7.8 from commit `9760163`, nightly watchdog 22:47 UK; 6.13.2: flag and fix every issue; 6.13.1: the script run from the repository; 6.13, 21 Oct: the endgame stance in core part D; earlier versions in the playbook header). **Pipeline script version 7.8** (part B holds the asset id, the run commit and the hash). The 5 Nov evening review ran it from commit `9760163` (hash matched part B).
- **Estimated value at Thu 5 Nov close: 76,478, -23.52% since the start, against -5.57% for the S&P 500 fund (gap -17.95 points).** Thu 5 Nov -13.25% against the S&P 500 -4.4% (AP): Sandisk -3.24 points, Western Digital -2.60, Seagate -2.44, ServiceNow -1.19, Micron -1.07 (sold at the open), AMD -1.06, NetApp -0.98, Monolithic Power -0.46 (sold at the open), Amazon -0.22.
- **Last FT figures: Mon 2 Nov close, 89,956 (-10.04%), rank 11,537 (number of players not recorded; the top 2% line is about rank 307).** Read off the FT site by Tim late on 3 Nov, before it updated. `reported` row with top2_return_pct 10.29 (Cautious, rank 316; Owen'sbigmoney, rank 195, at +11.64%). RECONCILE +142 credits (+0.16%). Previous: Mon 26 Oct close, 100,973, rank 3,994 of 14,736.
- **Standstill (5 Nov evening run):** change for 27 Oct +4.26, 30 Oct +0.61, both complete; 2 Nov -2.08 after four sessions; 3 Nov +1.00 after three; 5 Nov -1.31 after one. Week of 19 Oct -3.17; week of 26 Oct +5.58; week of 2 Nov -2.36 so far. Inception (20 sessions): -19.64 as entered, -18.32 fully invested. EXPECTED BENEFIT: four settled, expected 0.0, actual +2.34, sign right in 1 of 4.
- **Panel test (all 30 members loaded):** history verdict "no evidence" (average rank correlation +0.044, t +1.2, 58 dates). Live: three dates (-0.101), too few to judge. The score is frozen.
- **Order for Fri 6 Nov's open (set by the Thu 5 Nov evening review, message sent about 21:44 UK; corrected about 22:10 UK after Tim found Roblox is not in the game):** AppLovin 20, Meta Platforms 15, Qualcomm 15, Netflix 15, Salesforce 15, Spotify 10, NetApp 10, cash 0.
- Day call record (S&P 500): 11 right of 18; Brier in the ledger. Fri 6 Nov: S&P 500 Green 56% against a usual 55% (close to a coin flip); portfolio Red 48% against a usual 54%, reviewer -3 on both for forced selling and the jobs report.
- Macro at Thu 5 Nov: US 2-year 4.46% (-12bp; -15bp over five), 10-year 4.84% (-6bp; -14bp over five), 30-year 5.25%. UK 10-year 5.15% (-1bp; -14bp over five), Germany 3.24%, France 4.77%, Italy 4.36%, Japan 2.76% (all from the feed). Brent $98.63 (+3.8%; -11.6% over five), WTI $90.76, natural gas $2.94, gold $4,098.90 (futures fallback). Backdrop label: tailwind.
- Crypto: Bitcoin $76,085 at the US close (-5.0% on the day, -5.8% over five); trend **mixed** (IBIT 6.2% below its 50-day, 5.9% below its 20-day, 4.2% above its 200-day), so no crypto-linked buy. No crypto-linked holding.
- Regime: risk-off. Thu 5 Nov: S&P 500 -4.4% to 7,353.73 (worst day since April 2025), Dow -3.4% to 51,523.06, Nasdaq -5.5% to 24,315.00 (AP); Russell 2000 about -4.5% (late intraday, JournalArta); VIX about 27 late intraday (Yahoo). Chip index about -10.6% late intraday (Yahoo).

## 2. Current portfolio

The order for Fri 6 Nov's open. Scores and bands from the pipeline at the Thu 5 Nov close. Under the endgame stance (core part D) the score floor, trend tests, volatility caps, theme guide and results budget do not apply; the NOTE lines for them are expected.

| Stock | Weight | Confidence (not calibrated) | Score | Band | Flags | Next results (implied move) | Swap if missing or broken |
|---|---|---|---|---|---|---|---|
| AppLovin | 20% | 55 | 55 | Weak | downtrend (50-day below 200-day), extended | Reported 4 Nov; next Feb (est.) | Netflix |
| Meta Platforms | 15% | 50 | 32 | Weak | below 50-day, oversold | Late Jan (est.) | Spotify |
| Qualcomm | 15% | 50 | 25 | Weak | below 50-day, heavy-volume down day (closed above its open) | Reported 4 Nov; next Feb (est.) | Arm Holdings |
| Netflix | 15% | 50 | 26 | Weak | below 50-day, downtrend, faded gap | Jan (est., after the game) | IBM (20-day volume not checked) |
| Salesforce | 15% | 50 | 32 | Weak | below 50-day | Early Dec (est., after the game) | Spotify |
| Spotify | 10% | 50 | 54 | Middling | faded gap | Feb (est.) | Netflix |
| NetApp | 10% | 50 | 35 | Weak | below 50-day, oversold | 25 Nov, after US close (est.) | Spotify |
| Cash | 0% | | | | | | |

Themes: Software 75%, AI and chips 25%. Largest risk shares: AppLovin 44.8%, Qualcomm 17.1%, Meta 13.2%, Netflix 10.9%; estimated daily volatility 1.91% (2.32% with Roblox). Worst scenario: a deeper AI sell-off, -6.5%. The concentration is deliberate under the stance. The book's move from memory to software came from the exit rule, not from a view.

Points for the coming reviews:

- Tim was told tonight that the memory breakdown named in the stance has happened and that a change of direction is his call.
- Next-result dates of the six new names are estimates, not read tonight; analyst targets not read.
- Cloudflare reported after the 5 Nov close: revenue $782.5m, a beat, guidance lifted; StockStory reported +18.2% after hours. Reaction session Fri 6 Nov: add its drift row in the next review. Figures from search snippets; the release page failed.
- Fri 6 Nov: US jobs report, 13:30 UK, forecast +59K, unemployment 4.2% (Kiplinger).
- Sold and kept on the list five sessions: Sandisk, Seagate, Western Digital, AMD, ServiceNow, Amazon (to Thu 12 Nov); Micron, Monolithic Power (to Wed 11 Nov); Palantir (to Mon 9 Nov); Nvidia, Shopify, Arm, Datadog (to Fri 6 Nov).
- Iran: tankers hit in Hormuz again on 5 Nov (US News, Al Jazeera); Trump signalled a "heavy hit" (Gulf News). Brent near $98.
- Bitcoin's trend is mixed: no crypto-linked buy.

## 3. Pending order

**Change for Fri 6 Nov's open (Thursday 5 Nov evening review): sell Sandisk 20, ServiceNow 20, Seagate 15, Western Digital 15, AMD 10, Amazon 10; add AppLovin 20, Meta Platforms 15, Qualcomm 15, Netflix 15, Salesforce 15, Spotify 10.** Order: AppLovin 20, Meta Platforms 15, Qualcomm 15, Netflix 15, Salesforce 15, Spotify 10, NetApp 10, cash 0. Message sent about 21:44 UK on 5 Nov; Netflix replaced Roblox about 22:10 UK, Roblox not being in the game (Tim, 5 Nov); taken as entered unless Tim says otherwise.

## 4. Watchlist

22 names after tonight, above the 20 guide because six stocks just sold must stay listed. Scores and bands at the Thu 5 Nov close. Removed tonight: Texas Instruments, Bloom Energy, TSMC, Advanced Energy, Analog Devices (weak, rotated out). Added: none beyond the six bought.

| Name | Band | Status | Score | Note |
|---|---|---|---|---|
| Microsoft | Strong | Watching | 67 | Closed 3.42% below its open on 1.80 times volume. Promote on a close above its open. |
| Block | Strong | Watching | 62 | Reported 3 Nov, guide raised. Fell 4.1% on 1.55 times volume. |
| Apple | Strong | Watching | 60 | Fell 1.5% on 1.58 times volume after a record high. |
| Amazon | Middling | Exit signal (sold for 6 Nov) | 54 | Listed to Thu 12 Nov. |
| CDW | Middling | Watching | 53 | Scan Event on 4 Nov; fell 6.1%. |
| AMD | Weak | Exit signal (sold for 6 Nov) | 38 | Listed to Thu 12 Nov. |
| Datadog | Weak | Exit signal | 37 | Listed to Fri 6 Nov. |
| Seagate | Weak | Exit signal (sold for 6 Nov) | 36 | Listed to Thu 12 Nov. |
| Cloudflare | Weak | Exit signal | 33 | Reported after 5 Nov close, beat; earliest entry Mon 9 Nov on the drift test. |
| Palantir | Weak | Exit signal | 32 | Listed to Mon 9 Nov. |
| Shopify | Weak | Exit signal | 32 | Listed to Fri 6 Nov. |
| Sandisk | Weak | Exit signal (sold for 6 Nov) | 30 | Listed to Thu 12 Nov. |
| Coinbase | Weak | Watching | 28 | Crypto tracker. |
| ServiceNow | Weak | Exit signal (sold for 6 Nov) | 27 | Listed to Thu 12 Nov. |
| Micron | Weak | Exit signal | 26 | Listed to Wed 11 Nov. |
| Strategy | Weak | Exit signal | 25 | Crypto tracker. |
| Arm Holdings | Weak | Exit signal | 25 | Listed to Fri 6 Nov; swap for Qualcomm. |
| Western Digital | Weak | Exit signal (sold for 6 Nov) | 24 | Listed to Thu 12 Nov. |
| Alphabet | Weak | Watching | 24 | Fell 2.2% on 1.44 times volume. |
| Monolithic Power Systems | Weak | Exit signal | 23 | Listed to Wed 11 Nov. |
| Nvidia | Weak | Exit signal | 21 | Listed to Fri 6 Nov. Reports 18 Nov (est.). |
| Broadcom | Weak | Watching | 16 | Promote on a heavy-volume close above its open. |

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

- Thu 5 Nov 2026 (about 22:15): Session with Tim. Roblox is not in the game. AppLovin, its listed swap, is already at the 20% limit, so Netflix 15 took its place (fell 1.25% on 1.06 times volume; lower beta than Roblox). Pipeline re-run from the evening's inputs and files republished. Portfolio call now Red 48%.
- Thu 5 Nov 2026 (about 21:50): Evening review, a change evening for Fri 6 Nov (six rule exits; AppLovin 20, Meta 15, Qualcomm 15, Roblox 15 (replaced by Netflix at 22:10), Salesforce 15, Spotify 10 in, NetApp kept). 5 Nov -13.25% against the S&P 500 -4.4%, value 76,478. Pipeline 7.8 from commit `9760163`, hash matched. Price feed: forced (first read 4 Nov; forced run 21:32 UTC, again 21:41 UTC for 37 tech tickers), nothing refused or missing. Non-US yields from the feed; commodities from the futures fallback. Broad scan: forced (2 Events, 30 Leaders). Drift: AppLovin FAIL 5 of 6 (trend), Arm FAIL, Qualcomm FAIL. Order message sent about 21:44 UK; a first draft of the order held Oracle on a nine-session volume figure, corrected to Salesforce before the message when the 20-day figure read 1.30. Files published (no deletes; store 100 MB, 135 files). WARNINGs: FLEX 2026-05-06 and BE 2024-11-15 known; APP 2024-11-07 (+46.3%) from the feed's new two-year history, believed genuine, not re-checked. Research lighter than the usual 25 to 40 sources. Pages not read: KRMG, CNBC's live page and BoE page, Benzinga's memory page, StockTitan, Invezz, Stockhouse, FinancialContent (errors), 247wallst's Cloudflare page (permission request not answered), Investing.com (rate limited). Not read: Qualcomm's revenue against consensus, Arm's guidance, analyst changes, the new names' targets and next-result dates. No ISSUE this run.
- Wed 4 Nov 2026 (about 21:45): Evening review, a change evening for Thu 5 Nov (Micron, Monolithic Power out; Sandisk 20, AMD 10 in). 4 Nov -3.76% against SPY +1.65%, value 88,163. Pipeline 7.8 from commit `9760163`, hash matched. Price feed: forced (first read 3 Nov; forced run 21:33 UTC, again 21:36 UTC for XYZ, CDW, DASH, AVGO, GOOGL, AAPL), nothing refused or missing. Non-US yields from the feed; commodities from the futures fallback. Broad scan: forced (30 Events, 30 Leaders). Drift: AMD, Datadog, Block, CDW all FAIL (Block and CDW on a missing consensus, not read). Watchlist cleaned per 6.15. Order message sent about 21:39 UK. Files published (no deletes). WARNINGs for FLEX 2026-05-06 and BE 2024-11-15: known. Research lighter than the usual 25 to 40 sources. Pages not read: Benzinga's AMD page, Arm's newsroom, Invezz (client errors), FX Leaders (robots). VIX, Russell 2000 close and ISM forecast not read; analyst changes not read tonight. No ISSUE this run.
- Tue 3 Nov 2026 (about 23:30): Session with Tim. FT figures for the 2 Nov close stored in the ledger (89,956, rank 11,537). Order unchanged.
- Tue 3 Nov 2026 (about 23:20): Session with Tim. Playbook 6.15.1, page only: hover details, calendar, log and tables. Order unchanged.
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

## 7. Market regime notes

Label: Risk-off (Thu 5 Nov: the index followed chips lower on heavy volume). What would change it: to mixed, a session that holds its gains with chips no longer leading down; to risk-on, chips and memory closing above their opens on heavy volume for two sessions.

Thu 5 Nov: S&P 500 -4.4%, Dow -3.4%, Nasdaq -5.5% (AP). Reasons given: Democratic wins raising the chance of pauses on data-centre building, costlier borrowing and bubble talk (AP); Rep. Ansari's call for a pause on advanced AI (24/7 Wall St); UBS on nearly a third of 2028 US capacity at risk (Motley Fool). Vanda: largest retail net selling since 17 March 2020, with forced selling by systematic and leveraged strategies; Nomura: hedge funds locking in profits (Yahoo). Nvidia -9.3%, AMD -17.3%, AppLovin +31%. Brent +3.9% (AP); 10-year 4.84%. Bank of England raised to 4% from 3.75%, eight for a quarter point and one for a half (Euronews). Kospi -5.3%, Nikkei -1.8%, FTSE 100 -0.4% (AP). Hormuz: more tankers hit (US News). After the close: Cloudflare revenue $782.5m, a beat.

Wed 4 Nov: S&P 500 +1.58%, Dow +3.03%, Nasdaq +1.44% (TradingKey); chip index -3.13% (TradingKey) or -3.84% (Econcurrents). Democrats won both chambers. Brent about -9% (Reuters at midday, -8.9%). ADP +86k against +69k; ISM services 54.5 (September 54.9). Seagate -8.13%, Sandisk -7.91%, Micron -7.00%, WDC -6.77%, on a slower-AI-build read (TIKR), Kioxia's forecast and Texas data-centre moratorium fears (24/7 Wall St). Datadog -14.4% after a beat with an in-line Q4 guide. Block +15.3%, raised guide. After the close: Arm revenue $1.44bn against $1.38bn, EPS $0.52 against $0.47, -1.8%; Qualcomm EPS $2.17 against $2.16.

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
- Fri 6 Nov: US jobs report (13:30 UK), forecast 59K, unemployment 4.2%, previous 29K (Kiplinger). Tue 10 Nov: US CPI. Wed 18 Nov (est.): Nvidia. Wed 25 Nov (est.): NetApp. Thu 26 Nov: US closed. Fri 27 Nov: US closes 18:00 UK, game ends.

## 8. Open questions for Tim

Answered: an order entered before 08:00 UK counted for that day up to 23 Oct; the midday check stays off; the leaderboard shows only the top 10; Shell filled at its 08:00 open on 9 Oct; Microsoft, Coca-Cola, Palantir, Goldman Sachs, Meta Platforms and Eli Lilly are in the game's list; the orders for 13 to 16 Oct were entered; GitHub access from scheduled runs; the cut-off after the clock change (08:00 UK local time all year); the fetch tool refusing built addresses (answered by the price feed); Marsh & McLennan stays in the panel; order B entered (21 Oct); whether the 23 Oct order was entered as sent; the 27 Oct order entered (26 Oct, 22:52 UK).

Still open:
1. Are AppLovin, Qualcomm, Netflix, Salesforce and Spotify in the game's list? Assumed yes (Meta and NetApp were held earlier; Roblox is not in it: Tim, 5 Nov). Swaps if one is missing: Netflix for AppLovin and Spotify, Spotify for Meta and Salesforce, Arm for Qualcomm, IBM for Netflix (IBM's 20-day volume not checked).
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

- Confidence ratings (not calibrated): 28 of 42 settled, few distinct dates: below 55, 5 of 14 beat the index (36%); 55 to 59, 6 of 9 (67%); 60 and above, 4 of 5 (80%, all from the 9 to 15 Oct energy book). Far too few to judge. Ratings for the order for 6 Nov: AppLovin 55; Meta, Qualcomm, Netflix, Salesforce, Spotify, NetApp 50.
- Shadow ratings: 611 logged. Live: score 70 and above, 173 cases, 54% beat the index (-1.21 points); 60 to 69, 113, 42% (-3.81); 45 to 59, 84, 24% (-6.42); below 45, 75, 45% (-1.99). Not ordered by score. Judgement test: two dates, too few.
- Panel test: see section 1. Old backtest (hindsight) correlation +0.008.
- Drift record: ENTER 2 settled (100% beat the index, +5.55 points); WATCH 1 settled (-3.62); FAIL 16 settled (25%, -2.76 points), 15 open.
- Day call record (S&P 500): 11 right of 18. Below the 20 settled calls needed before it could be considered.
- Broad scan record (scan/latest.md, 30 Oct): Leaders, 60 settled, 40% beat the index, mean excess -1.81 points close to close and -1.89 from the next open; Events, 9 settled, 56%, -1.31 and -1.44; 70 rows open.

## 12. Tools

- Tim's page: https://claude.ai/artifact/8P8UwQsb4QsbZMsKNYKrUJ, pinned in his Claude sidebar, with tabs Today, Macro, Performance, Risk, Calendar and Log. It reads four data files (`stocks`, `ledger`, `history`, `macro`) and a fifth dataset, `logos`, that no run touches. The Order panel reads the latest alert whose `stock` is "Order"; its "Enter before" bar uses the 08:00 UK cut-off.
- Playbook docs (version 6.15.1): `claude/ft-game-playbook.md` (core, with the routing table), `claude/ft-game-rules.md`, `claude/ft-game-data.md`, and the run docs `claude/ft-game-run-evening.md`, `-morning`, `-refresh`, `-weekly`, `-weekend`.
- Panel file: `panel.json` on the same artifact, named by the document `store/panel`.
- Scripts: the pipeline (version 7.8; runs take it from the repository at the commit in data doc G1) and the screening script are assets on that artifact. Their ids and hashes are in part B of the playbook, the only place they are kept.
- Price feed (data doc G8): `feed/latest.json` and `feed/live.json` in the repository, with the non-US 10-year yields under `macro.intl_yields`. 1 Nov: current for Fri 30 Oct, then a forced run at 21:35 UTC for 17 tickers (two years each for the two new holdings). It refused Palantir on a revised low; the stockanalysis.com history page confirmed the revision.
- Pages reached through searches on 5 Nov: AP via VIN News, Yahoo Finance live page, 24/7 Wall St (memory), Kiplinger, Euronews, Motley Fool, JournalArta, TokenPost, StockStory (AppLovin). Search snippets only: US News, Al Jazeera, Gulf News, tech-insider, Cryptobriefing and StockStory (Cloudflare). Refused or failed: KRMG, CNBC, Benzinga, StockTitan, Invezz, Stockhouse, FinancialContent, Futu (no content), 247wallst's Cloudflare page, Investing.com (rate limited).
- Pages reached through searches on 4 Nov: TradingKey, Econcurrents, TheStreet, TIKR, 24/7 Wall St, Star-Advertiser (Reuters), KFGO (Reuters), StockStory, StockTitan, Seeking Alpha, SEC (CDW 8-K), forexfundamentals, financecalendar. Refused or failed: Benzinga's AMD page, Arm's newsroom, Invezz (client errors), FX Leaders (robots).
- Pages reached through searches on 3 Nov: TheStreet (closes), Yahoo Finance live page, ZeroHedge, Bank of Vol, investingLive (AMD), SEC (Fiserv 8-K), Grafa and StockStory (Shopify, Advanced Energy), MarketBeat (Bloom), 24/7 Wall St (memory), TIKR (Seagate). Refused or failed: CNBC article pages (site errors); investing.com and 24/7 Wall St's AMD live page (rate limited).
- Market data service: massive.com, free plan, on an account opened by Tim's father. The key is in the evening and weekly review tasks and is never written into this project's docs, the page data, alerts or messages. Not used on 3 Nov (the feed covered every price).
- Sources that did not work: Alphastreet, Chartmill and Rolling Out article pages (29 Oct); Benzinga article pages (28 Oct); CNBC article pages; gurufocus news pages and EBC; CNN article pages; Detroit News; Fortune's Bitcoin price page; capital.com news pages. tradingeconomics' news pages carry no statistics table.
- Artifact leftovers: superseded data assets stay in the store (playbook 6.14.3). 5 Nov evening: 100 MB of 1 GB used, 135 files.
- GitHub mirror: private repository `timzwang/ft-game` (part B and G6).
- Two saved skills, `ft-game-playbook` and `stock-score`, load in scheduled runs; the project docs win where they differ.
