# FT Stock Picking Game: state and log

Last updated: Mon 19 Oct 2026, about 22:15 UK (evening review, a quiet evening: no change for Tue 20 Oct; AbbVie's results event added, implied moves stored for five holdings, the 16 Oct FT reading given again with the top 2% line; stockanalysis.com refused most pages, so most session rows came from Cboe's delayed quotes. Before that, about 20:40 UK: hand-run session with Tim: playbook 6.11 and pipeline 7.4, the expected benefit recorded with every change of order and a data check in the repository, after ChatGPT's follow-up review; no order, data file or scheduled task changed. Before that, about 00:35 UK: hand-run session with Tim: playbook 6.10 and pipeline 7.3 after ChatGPT's repository review of 18 Oct; results budget 1.0 points for reports dated 27 to 30 Oct; no order changed. Before that, about 00:05 UK: the review checked against commit 25e8a93 and AbbVie's missing results event noted. Before that, Sun 18 Oct about 23:50 UK: hand-run session with Tim: playbook 6.9, the evening and weekly review tasks recreated so their runs reach the GitHub repository. Before that, about 22:05 UK: Tim confirmed the Mon 19 Oct order is entered (the game shows "Pending reweight") and sent portfolios near the top 2% line. Before that, about 21:50 UK: evening review, a change evening: Palantir out, Chevron 15 to 10, AbbVie 10 in, for Mon 19 Oct's open; message sent about 21:47 UK. Before that: about 20:25 UK weekend news check; about 10:50 UK follow-up approved by Tim (GitHub access test passed, playbook version 6.8); about 01:00 and 00:30 UK hand-run sessions with Tim (playbook 6.4 and 6.5, pipeline 7 and 7.1, after the outside audit))

This doc is the narrative record for Tim's entry, "Seeking Beta". The procedure for every run is in `claude/ft-game-playbook.md` (the core doc) and the docs its routing table names. The numbers (prices, scores, daily performance, contributions, ratings and their outcomes, the full calendar, analyst changes, alerts, the panel test, the drift record) live in the data files behind Tim's page and the panel file, and are produced by the pipeline script; this doc carries the decisions and the reasons.

Messages: from 10 Oct Tim is sent a message only when there is something for him to enter or answer (playbook part I, "When Tim is told"). Quiet runs update the page and this doc and send nothing.

Scheduled runs: evening review 21:30 UK Sun to Thu; morning check 06:36 UK Mon to Fri; price refresh 16:45 UK and late price refresh 19:22 UK Mon to Fri; results-day refresh 14:50 UK Mon to Fri (acts only on results days); weekly performance review Sat 09:12 UK; weekend news check Sat and Sun 20:20 UK; midday check 12:40 UK Mon to Fri (switched off, see section 8).

**Cut-off: until the FT confirms it, every order must be entered before 07:00 UK (playbook part C, from 17 Oct).**

## 1. Status

- **Playbook version 6.11** (6.11, 19 Oct evening: pipeline 7.4, `order_expected` with every change of order, and the repository's data check, approved by Tim after ChatGPT's follow-up review; 6.10, 19 Oct: pipeline 7.3 and a results budget of 1.0 points for reports dated 27 to 30 Oct, approved by Tim after ChatGPT's repository review; 6.9, 18 Oct: evening and weekly review tasks recreated with the repository attached; 6.8, 18 Oct: G6 and G7 step 1, finding the repository in a scheduled run; 6.7, 18 Oct: pipeline version 7.2, stricter price handling; 6.6: the handoff log; 6.5: the standstill test corrected; 6.4: after the outside audit, pipeline version 7, 07:00 UK cut-off, score frozen; 6.3: the broad scan; 6.2: the day call never moves cash, "overbought" is a warning only; 6: split docs, panel test, earnings-drift scan). **Pipeline script version 7.4** (19 Oct evening; part B holds the asset id and hash).
- **Estimated value at Mon 19 Oct close: 101,097, +1.10% since the start, against -1.26% for the S&P 500 fund (gap +2.35 points).** Mon 19 Oct -0.33% against SPY +0.42%: Microsoft +0.13 points, Palantir (sold at the open) +0.03; Eli Lilly -0.20, Coca-Cola -0.10, Exxon -0.06, AbbVie -0.06 (bought at the open), Chevron -0.05. Tech rebounded, staples and health care lagged. Fri 16 Oct: 101,436.
- **Last FT figures: Fri 16 Oct after the close, 101,402 (+1.40%), rank 3,269 of 13,918 (top 23.5%).** Stored in `reported` on 18 Oct. RECONCILE: -34 credits (-0.03%) against the estimate: verified at the close. Top 2% line: rank 279 of 13,969 (game page on 18 Oct). Tim's screenshots of 18 Oct put the line at about +6.5%: "contrarian cy" rank 187, 107,332 (+7.33%; holds Mastercard, Visa, Home Depot, Uber, Otis); "Abi's Portfolio" rank 324, 106,462 (+6.46%). Gap to the line about 5 points. Stored on 19 Oct: `top2_return_pct` 6.5 on the 2026-10-16 row (players kept at 13,918; Tim's own page showed 13,966). Also seen: "Intense" rank 2,807 at 101,877 (+1.88%), so the middle of the field is bunched within half a point of Tim.
- **Standstill (19 Oct run):** against never changing the first order (9 Oct), the changes now cost **-0.30 points** as entered and **-0.77** against the same stocks fully invested (RTX, Lockheed and Nvidia held up on 19 Oct). Change for 13 Oct +0.61 over five sessions (complete); 14 Oct -0.34 (four); 15 Oct +0.19 (three); 16 Oct -0.12 (two); 19 Oct -0.26 (one). Week of 12 to 16 Oct +0.12. No evidence either way.
- **Panel test (18 Oct, 28 of 30 members with two years):** history verdict "no evidence": average rank correlation +0.042 (t +1.1) over 49 dates; top third minus bottom third +0.25 points (t +0.4). Parts: one-year strength +0.087 (t +1.7), two-month +0.053 (t +1.4), five-day +0.007 (t +0.2). Live: no complete window yet. Marsh & McLennan to be replaced by the next position down and HPE loaded at the weekly review of 24 Oct. 23 members one session behind (15 Oct). The score is frozen for the rest of the game.
- **Order in force (filled Mon 19 Oct's open; unchanged for Tue 20 Oct):** Coca-Cola 20, Exxon Mobil 15, Shell 15, Microsoft 15, Eli Lilly 15, Chevron 10, AbbVie 10, cash 0.
- Day call for Tue 20 Oct: S&P 500 green 51% (usual 55%); portfolio green 53% (usual 56%); no adjustment: a coin flip. Record (S&P 500): 2 right of 5. Mon 19 Oct: S&P 500 rose (green right), portfolio fell (green wrong).
- Macro at Mon 19 Oct close: US 2-year 4.77% (+3bp), 10-year 5.15% (+6bp; -7bp over five sessions), 30-year 5.48%. Gilt 5.39%, German 3.43%, French 4.89% (+10bp), Italian 4.54%, Japanese 2.91%. Brent $109.29 (-0.5%; +4.7% over five), WTI $103.84, gold $4,138. VIX about 18.4 (midday). Backdrop label: neutral. October 28 hike odds about 25% to 30% (CME FedWatch reports, 19 Oct), down from 42% on 14 Oct.
- Crypto: Bitcoin $81,772 at the US close (-0.6% over five sessions), trend up (IBIT 2.1% below its 20-day, 4.5% above its 50-day). Ether -3.3%, Solana -4.1%, XRP -6.0% over five sessions; Ether's trend mixed. No holding is crypto-linked.
- Regime: mixed. Mon 19 Oct: S&P 500 +0.41% to about 7,690, Nasdaq +1.11%, Dow -0.07%, Russell +0.25%; chips ended an eight-day losing streak; consumer discretionary and tech led, staples, real estate and utilities lagged; NAHB 29 (forecast 31), lowest since 2012. Week to 16 Oct: S&P 500 -1.95% to 7,659 (0.6% below its 50-day, 1.0% below its 20-day), Nasdaq -4.48%, Dow +0.67%, Russell -3.05%; chips -12% on the week. Energy, utilities and staples led on Friday. What would make it risk-off: the 10-year back above 5.25% with the S&P 500 below its 20-day, or a hike at the next meeting priced above 70% (read as the 28 Oct meeting; the December figure is already above 70%).

## 2. Current portfolio

The order in force (filled Mon 19 Oct's open, unchanged for Tue 20 Oct). Scores and bands from the pipeline at the Mon 19 Oct close; confidence ratings as given on 18 Oct.

| Stock | Weight | Cap | Confidence (18 Oct, not calibrated) | Score | Band | Flags | Next results | Substitute if missing |
|---|---|---|---|---|---|---|---|---|
| Coca-Cola | 20% | 20% | 59 | 75 | Strong | none | 27 Oct, before US open (implied 4.2%) | PepsiCo (downtrend: cash instead) |
| Exxon Mobil | 15% | 15% | 60 | 82 | Strong | none; three target raises in a week | 30 Oct, before US open (implied n/a, 6% used) | ConocoPhillips |
| Shell | 15% | 15% | 59 | 72 | Strong | none | 29 Oct, 07:00 UK (implied n/a, 6% used) | BP |
| Microsoft | 15% | 15% | 57 | 71 | Strong | none | 28 Oct, after US close (implied 6.0%) | Alphabet (not scored) |
| Eli Lilly | 15% | 15% | 59 | 71 | Strong | none | 29 Oct, before US open (implied 7.9%: above budget at 15%) | Merck |
| Chevron | 10% | 15% | 59 | 77 | Strong | none | 30 Oct, before US open (implied 5.8%) | ConocoPhillips |
| AbbVie | 10% | 20% | 60 | 74 | Strong | none | 30 Oct, before US open, confirmed (implied 6.4%) | Amgen |
| Cash | 0% | | | | | | | |

Ratings were moved down from the anchors (60 to 65) by up to 5 points each: the panel test finds no evidence that a high score is an edge, so ratings stay near 55 to 60. Palantir's exit carries a rating of 58 (the chance it lags the index over five sessions).

Points for the coming reviews:

- Every change of order carries `order_expected` (data doc G3, from 6.11). None tonight (no change).
- Themes: Energy 40%, Health care 25%, Consumer staples 20%, Software 15%. Risk shares: Exxon 21.9%, Coca-Cola 20.3%, Shell 17.5%, Chevron 13.8%, Eli Lilly 12.2%, AbbVie 11.8%, Microsoft 2.5% (oil names 53%). Worst scenario: ceasefire or Hormuz reopening -1.78%.
- **Results cluster (events now complete; AbbVie's added 19 Oct):** weight times implied move against the 1.0 budget for 27 to 30 Oct: Coca-Cola 0.84, Microsoft 0.90, Shell 0.90 (6% used), **Eli Lilly 1.19 (above budget)**, Exxon 0.90 (6% used), Chevron 0.58, AbbVie 0.64. RESULTS TOTAL next 10 sessions **5.95 points** across seven reports, deliberate in the sense agreed on 19 Oct (the entry needs variance), but it is all in one week and oil names make up 2.4 points of it. Implied moves are earnings-watcher's of 16 Oct; Exxon's and Shell's pages failed tonight. Chevron's 5.8% and AbbVie's 6.4% are well above their recent reports (2% to 5%). **Eli Lilly: trim to 12% or less in the order before 07:00 UK Wed 28 Oct unless its implied move falls below about 6.7%**; decide by the Sunday 25 Oct review. Last orders: Coca-Cola before 07:00 UK Mon 26 Oct; Shell, Eli Lilly and Microsoft before 07:00 UK Wed 28 Oct; Exxon, Chevron and AbbVie before 07:00 UK Thu 29 Oct. The Mon 26 Oct cut-off test order (07:15 UK) must carry the same Coca-Cola weight as that morning's 07:00 order. Each report gets its own hold, trim or exit call by the Sunday 25 Oct review at the latest (Coca-Cola's is that night).
- Palantir post-mortem row written by the 19 Oct run.
- Keep TSMC on the list until Fri 23 Oct and Palantir until Mon 26 Oct (standstill test), then they may be removed.
- Walmart has only 51 stored sessions on the list (its year of closes went to the panel): its 200-day figures are missing until the list history catches up; its statistics page could not be fetched on 19 Oct.
- Shadow ratings still open for stocks off the list: Constellation Energy, CrowdStrike, Lumentum, Marvell (the weekly review gives their rows).

## 3. Pending order

**No change for Tue 20 Oct (19 Oct evening review, quiet; nothing sent).** Last change: for Mon 19 Oct's open, message sent about 21:47 UK on Sun 18 Oct; entered, confirmed by Tim about 22:00 UK (screenshot shows "Pending reweight"); filled 19 Oct.

Coca-Cola 20, Exxon Mobil 15, Shell 15, Microsoft 15, Eli Lilly 15, Chevron 10, AbbVie 10, cash 0.

Changes: sell Palantir 5 (momentum exit); Chevron 15 to 10 (oil concentration); add AbbVie 10.

## 4. Watchlist

Scores and bands at the Mon 19 Oct close. 18 names. No additions or removals on 19 Oct: stockanalysis.com refused its pages after the first ten, so no candidate could be given full data, and the broad scan had not yet run for 19 Oct.

| Name | Band | Status | Score | Flags | Next results | Promote if |
|---|---|---|---|---|---|---|
| Visa | Strong | Watching | 80 | at 52-week high | 27 Oct, after US close (est.) | Steady name if a holding weakens; not held through results above 10% |
| Mastercard | Strong | Watching | 78 | none | 29 Oct (est.) | Alternative to Visa, not both |
| Phillips 66 | Strong | Watching | 77 | none | 28 Oct, before US open | Only in place of an oil major |
| Valero Energy | Strong | Results ahead | 73 | EMAs mixed | 22 Oct (time est.) | Not before results; drift tests after |
| ConocoPhillips | Strong | Watching | 73 | none | 5 Nov (est.) | Swap for Exxon or Chevron before their 30 Oct results if a report needs dodging |
| Marathon Petroleum | Strong | Watching | 72 | extended | 3 Nov | 5% at most while extended |
| Humana | Strong | Ready | 71 | none | 6 Nov | 5% (cap) if a holding weakens |
| UnitedHealth | Strong | Ready | 70 | EMAs mixed | Jan 2027 (est.) | Up to 10% if a holding weakens |
| BP | Strong | Watching | 69 | none | 30 Oct (est.) | Substitute for Shell |
| Walmart | Strong | Watching | 69 | 200-day not yet stored on the list | 19 Nov | Core candidate once its stored trend is complete |
| Palantir | Strong | Watching (sold 19 Oct) | 64 | EMAs mixed | 2 Nov | Keep until 26 Oct (standstill test) |
| Amgen | Middling | Watching | 57 | none | 3 Nov, after US close | Score 60+; steady name (cap 20%) |
| Meta Platforms | Middling | Results ahead | 53 | golden cross 6 Oct | 21 Oct, after US close | Drift tests on 22 Oct's session; not held through the report |
| Merck | Middling | Watching | 46 | below 50-day | 29 Oct | Back above its 50-day |
| Procter & Gamble | Weak | Results ahead | 63 | downtrend | 22 Oct (est.) | Not while in a downtrend |
| TSMC | Weak | Watching | 42 | below 50-day; faded gap | Jan 2027 | ROTATE OUT candidate; keep until Fri 23 Oct (left the order 16 Oct), then remove |
| Strategy (crypto tracker) | Weak | Watching | 40 | faded gap; golden cross 19 Oct | 29 Oct (est.) | Kept whatever it scores |
| Coinbase (crypto tracker) | Weak | Watching | 29 | downtrend | 29 Oct, after US close | Kept whatever it scores |

Tuesday's intake should add five to ten, including two or three FTSE 100 names. Candidates noted from the 16 Oct broad scan's Leaders, not yet checked: Cardinal Health, Travelers, Ross Stores, Targa Resources, Centene, Standard Life, Hiscox.

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
| Sun 18 Oct, about 21:47 UK (entered, confirmed by Tim about 22:00 UK) | Mon 19 Oct | Sell Palantir 5; Chevron 15 to 10; add AbbVie 10 | Palantir's heavy-volume exit signal; oil names carried 64% of risk with Exxon and Chevron correlated 0.94 (Tim's view of 17 Oct, acted on now); AbbVie score 82 with six target raises |

## 6. Review log (newest first, keep the latest 15)

- Mon 19 Oct 2026 (about 22:15): Evening review, quiet: no change for Tue 20 Oct. Day -0.33% against SPY +0.42% (tech rebound; Lilly -0.20 points). AbbVie results event added; implied moves stored for Coca-Cola, Microsoft, Eli Lilly, Chevron, AbbVie (Lilly 1.19 points against the 1.0 budget: trim by 28 Oct unless the move falls). stockanalysis.com refused 8 pages (BNO, ETHA, BP, Palantir, Marathon, Humana, Valero, Phillips 66) and the run stopped asking; those rows and the rest of the list came from Cboe's delayed quotes (`cdn-api.cboe.com`, read with a clock suffix, all at 16:00 EDT 19 Oct). No watchlist changes. Broad scan behind (16 Oct); a request was pushed. Files published.
- Mon 19 Oct 2026 (about 20:40): Hand-run session with Tim after ChatGPT's follow-up review (PR #3). Tim approved two additions: pipeline 7.4 (`order_expected`: every change of order records, before it fills, its expected benefit in points over five sessions against keeping the order in force, the thesis and what would show it wrong; locked once filled; EXPECTED BENEFIT beside the STANDSTILL change rows) and a data check in the repository (`scripts/check_data.py`, workflow `data-check`, on every data push and after each evening and weekly review). Playbook 6.11. 7.3 against 7.4 on the 16 Oct session: identical files. The check on the stored files fails on one item, AbbVie's missing results event, which tonight's review adds. No order, data file or scheduled task changed.
- Mon 19 Oct 2026 (about 00:35): Hand-run session with Tim after ChatGPT's repository review of 18 Oct (checked against commit 25e8a93 first: findings 1 to 3 and 5 to 8 confirmed in the code). Tim approved pipeline 7.3 and a results budget of 1.0 points for reports dated 27 to 30 Oct. Playbook 6.10. Pipeline 7.3 deployed (asset and hash in part B); page script updated (Risk tab budget, US calendar, day-call wording); regression tests and a test workflow in the repository; scan workflow main-only; scan libraries pinned. 16 Oct re-run with 7.2 and 7.3: identical files apart from one new meta row. AbbVie's results date confirmed (30 Oct, before US open). No order, data file or scheduled task changed.
- Sun 18 Oct 2026 (about 22:05): Tim confirmed the Mon 19 Oct order is entered and sent three portfolios near the top: the top 2% line is about +6.5%, about 5 points above Tim. Order unchanged.
- Sun 18 Oct 2026 (about 21:50): Evening review, a change evening for Mon 19 Oct (Palantir out; Chevron 15 to 10; AbbVie 10). Weekend B items confirmed (Araghchi's six-day offer "still on the table", Trump says the US could "soon finish the job"; no deal). Tim's 16 Oct FT figures stored (-34 credits against the estimate). Shell 9 and 12 Oct rows and Goldman's 14 Oct open corrected from stockanalysis.com (log recalculated, one credit). Four watchlist additions (Visa, Mastercard, ConocoPhillips, Walmart, with a year of closes from the market data service; key worked); Marvell, CrowdStrike, Constellation Energy removed. Broad scan and GitHub mirror not available (the repository was not cloned in this session and a fresh clone asked for credentials). No page refused. Files published.
- Sun 18 Oct 2026 (about 20:25): Weekend news check (H7, Sunday). No A item. One B item: Araghchi says Iran's Hormuz reopening conditions stand; Trump says the war will end "very quickly". Escalation continued (Houthi strikes on Saudi Arabia, a tug struck near Hormuz): C. Saudi index +0.82%; Bitcoin $81,018. Order unchanged.
- Sun 18 Oct 2026 (about 10:50): Follow-up approved by Tim. The one-off GitHub access test passed. Playbook version 6.8: data doc G6 and G7 step 1. No order, data file or page changed.
- Sun 18 Oct 2026 (about 01:20): Hand-run session with Tim. Playbook version 6.6: a handoff log between Claude and ChatGPT in the repository's `handoff/` folder. No order, data file or scheduled task changed.
- Sun 18 Oct 2026 (about 01:00): Hand-run session with Tim. Playbook version 6.5 and pipeline version 7.1, the corrected standstill test. Missing rows for RTX, Lockheed Martin, Nvidia and Goldman Sachs added. Corrected record: +0.12 points against the first order as entered, -0.32 fully invested, -0.75 for the 12 Oct rebuild.
- Sun 18 Oct 2026 (about 00:30): Hand-run session with Tim after the outside audit by ChatGPT. Fourteen changes approved: playbook 6.4 and pipeline 7; morning check 06:36 UK and a 07:00 UK cut-off; the Mon 26 Oct cut-off test; score frozen. No order changed.
- Sat 17 Oct 2026 (about 20:25): Weekend news check (H7). No A item. B items: IRGC supertanker mine claims; Trump's Russia sanctions waiver. Order unchanged.
- Sat 17 Oct 2026 (about 09:50): Weekly review. Fri 16 Oct logged: +0.64%; week +1.51% against -1.97%. Panel topped up to 28 members. Order unchanged; Palantir exit signal for Sunday.
- Fri 16 Oct 2026 (about 09:10): Hand-run session with Tim. Broad scan built (playbook 6.3).
- Fri 16 Oct 2026 (about 01:30, later): Hand-run session with Tim after an outside review. Playbook version 6.2.
- Fri 16 Oct 2026 (about 01:30): Hand-run session with Tim. GitHub repository `timzwang/ft-game` set up as a shared mirror; playbook 6.1.

## 7. Market regime notes

Label: Mixed (an AI and chip sell-off and a VIX above 20, offset by falling yields and rotation into energy, staples, payments and pharma).

Mon 19 Oct: S&P 500 +0.41% (about 7,690), Nasdaq +1.11%, Dow -0.07%, Russell +0.25%. Semiconductors ended an eight-day losing streak (Sandisk +7%, Micron +5%); Intel upgraded at JPMorgan; CoreWeave upgraded at Goldman. Staples, real estate and utilities lagged. 10-year +6bp to 5.15%. NAHB 29 against 31 forecast (lowest since June 2012). Brent eased to about $109 on profit-taking; WTI rose. Hormuz: Iranian attacks on at least 15 container ships in ten days (Guardian via straits.live); Araghchi's seven-day plan "remains on the table"; Macron on a Gulf tour; no deal. KBW bank index down six weeks running. Black Monday anniversary pieces everywhere.

Week to Fri 16 Oct:
- S&P 500 7,659.44 (-1.09% Friday, -1.95% on the week), 0.6% below its 50-day and 5.3% above its 200-day; Nasdaq 26,140 (-2.15%, -4.48%), below its 21-day and 50-day; Dow 52,002 (+0.67% on the week); Russell 2,721 (-3.05%). VIX 20.16. SOXX -4.1% Friday, -12% on the week. Energy +2.5%, utilities +1.4%, staples +1.1% on Friday. S&P 500 breadth on Friday roughly even (about 237 up, 227 down on stockanalysis.com's list). Largest gainers: Targa, Diamondback, EOG, Kinder Morgan, Northrop, RTX, Lockheed (+3.6% to +4.4%); losers: Twilio, Super Micro, Flex, Moderna, Palo Alto, Seagate, Palantir (-7% to -11%).
- Coca-Cola, Visa and Mastercard at records (Barron's). Exxon +2.5% after preliminary Q3 figures; Chevron +2.6%.
- Oil: Brent $109.86 (+3.7% Friday), highest since 19 May; ING says crude prices a significant risk premium.
- Fed: September minutes backed a 25bp hike to 3.75% to 4.00%; December hike odds about 74%, October about 42% (14 Oct).

Weekend log (weekend of 17 and 18 Oct): confirmed by the Sunday evening review.
- No A item.
- B: Hormuz. IRGC mine claims (Sat); Araghchi in Baghdad on Sunday: the seven-day offer "is still on the table", reopening within six days if the US accepts Iran's conditions (Fox News live, about 15:00 EDT). Trump on Truth Social: Washington could "soon finish the job". Rezaei: Iran has a plan "more devastating" than earlier wars. Fox reports the strait open to ships other than Iran's. No step towards a deal: the ceasefire scenario (-1.78 points on the new order) stays a tail risk.
- B: Russia. Trump's waiver of Graham Act sanctions and a Russian diesel licence; Energy Secretary Wright called it a "carrot" (Sunday). Bearish at the margin for refiners.
- C: Houthi strikes on Saudi Arabia; a tug struck off Khor Fakkan (UKMTO). Continuation of the pattern.
- Prices: Saudi index +0.82% Sunday; Bitcoin about $81,000. Oil and US futures reopen at 23:00 UK.
Earlier weekend (10 and 11 Oct): no A item.

Near calendar (the full calendar to 27 Nov is on the page and in the ledger):
- Tue 20 Oct: RTX results before the US open (watchlist off); housing starts and permits 13:30 UK (starts forecast 1.30M); Netflix after the close.
- Wed 21 Oct: Meta and Tesla results after the US close; EIA oil stocks 15:30 UK; 20-year bond auction 18:00 UK.
- Thu 22 Oct: Valero, Procter & Gamble, Lockheed Martin; jobless claims 13:30 UK (forecast 200,000); Conference Board leading index.
- Fri 23 Oct: flash PMIs; Michigan sentiment final.
- Sun 25 Oct: UK clocks go back; the US session is 13:30 to 20:00 UK in the week of 26 Oct. The evening review sets the order for Coca-Cola's results.
- Mon 26 Oct: cut-off test at about 07:15 UK (part C).
- Tue 27 Oct: Coca-Cola; Visa (after the close, est.). Wed 28 Oct: Fed decision 18:00 UK; Microsoft; Phillips 66. Thu 29 Oct: Shell; Eli Lilly; Merck; Mastercard; Coinbase. Fri 30 Oct: Exxon Mobil, Chevron, AbbVie. Tue 3 Nov: US midterms; Amgen. Thu 5 Nov: ConocoPhillips.

## 8. Open questions for Tim

Answered: an order entered before 08:00 UK counted for that day up to 23 Oct (from 17 Oct treat 07:00 UK as the cut-off); the midday check stays off; the leaderboard shows only the top 10; Shell filled at its 08:00 open on 9 Oct; Microsoft, Coca-Cola, Palantir, Goldman Sachs, Meta Platforms and Eli Lilly are in the game's list; the orders for 13 to 16 Oct were entered; value, rank and players after Fri 16 Oct's close; the Marsh & McLennan panel swap; GitHub access from scheduled runs (test of 18 Oct passed).

Still open:
1. Is AbbVie in the game's list? Assumed yes (large NYSE listing); substitute Amgen. Tim to say if it was missing.
2. Are Strategy and Coinbase in the game's list? Not needed until one is close to being bought.
3. Answered 18 Oct: the top 2% line is about +6.5% (ranks 187 and 324 at +7.33% and +6.46%). Updated figures welcome each weekend.
4. The cut-off after the clock change: 07:00 or 08:00 UK. Tim asked FT help on 18 Oct; the one-point Exxon and Chevron test at about 07:15 UK on Mon 26 Oct settles it (with Chevron now at 10%, the test is Exxon 15 to 14 and Chevron 10 to 11). Until then 07:00 UK.
5. Answered 18 Oct (about 23:50): the evening run had no repository because its task was created on 8 Oct, before the repository existed. The evening and weekly review tasks were recreated from a chat with the repository attached (playbook 6.9); a test run from a task made that way found the clone and pushed. The old two are kept, switched off. The mirror was caught up by hand for 18 Oct.
6. Does the game convert US stocks' returns into pounds? In the draft to FT help; the closing gap has stayed under 0.05%.

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
- Sequel: no new high after 12 Oct (212.94); on Fri 16 Oct it opened at 201.79 and closed at 186.03 on 33.2m shares, the first heavy-volume close below its open, so it is sold at Mon 19 Oct's open. Held at 5% it cost about -0.56 points to 16 Oct. Lesson: a high-range stock (daily range about 4%) at 5% can still cost half a point in a week; the 5% cap limits, but does not remove, the damage.

**RTX and Lockheed Martin, 8 Oct (a one-day bounce inside a downtrend)**

- Lesson: a strong day says nothing about the trend. Check the 50-day and 200-day averages before buying on a headline.

**Humana, 9 and 12 Oct (large gaps that faded, even with upgrades)**

- Lesson: the bigger the gap, the more of the news is already in the fill price.

**Goldman Sachs, 13 Oct (a results beat inside a downtrend)**

- Lesson: a big beat does not lift a stock in a downtrend. A results position needs the trend filter too.

**Meta Platforms, 12 to 15 Oct (follow-through entry, then a quick exit)**

- Bought for 14 Oct at 5%; on 14 Oct it closed 3.0% below its open. Sold at the 15 Oct open (726.56); it closed at 709.33 on 16 Oct, so the exit saved about a further 0.12 points.
- Lesson: a momentum entry after a two-day run can reverse at once. The give-back rule cut the cost.

**TSMC, 15 Oct (held through results in a sector sell-off)**

- Fell 3.4% on 14 Oct ahead of the report; gapped down 3.4% on 15 Oct after a beat with lower margins. Sold at the 16 Oct open (421.22); it closed at 412.61.
- Lesson: when the score has slipped below 50 before a report, cut the hold to 5% or exit, whatever the implied move. Total cost over the game -0.96 points.

**Judging changes: one day against several (17 Oct)**

- The 13 and 14 Oct changes each looked worse than standing still on their fill day, but over its sessions the 13 Oct change has added +0.78, because Nvidia kept falling. The 12 Oct rebuild looked good on its first day (+0.33) and cost 0.75 over five sessions. All changes together: +0.12 points against never changing the first order.
- Lesson: judge a change over the five sessions it was meant for (the STANDSTILL block), not its first day, and judge the process against the first order never changed.

## 11. Confidence ratings, shadow ratings, the panel test and the day call

- Confidence ratings (not calibrated): 11 resolved by 18 Oct (RTX, Lockheed Martin, Nvidia and Goldman Sachs settled once their rows were stored). Latest: RTX 60 beat, Lockheed 55 beat, Nvidia 50 lagged, Shell 59 beat, TSMC 53 lagged, Coca-Cola 55 beat, Goldman 54 beat (by 0.08 points), Microsoft 58 beat, Palantir 58 lagged. Far too few to judge. Ratings of 18 Oct for the order in force: Exxon 60, AbbVie 60, Coca-Cola 59, Shell 59, Chevron 59, Eli Lilly 59, Microsoft 57.
- Shadow ratings: 162 logged. Live: score 70 and above, 11 cases, 82% beat the index (+3.00 points); 60 to 69, 14 cases, 43% (-4.41); 45 to 59, 10 cases, 20% (-4.34); below 45, 12 cases, 83% (+2.76). Weak evidence until about 150 have settled. Judgement test: no settled dates yet (builds from 18 Oct).
- Panel test: see section 1. The main evidence on the score. Old backtest (hindsight) correlation -0.13.
- Drift record: no reporters scanned yet (Friday's session had no large reporters among the holdings or watchlist, and the broad scan was unavailable on 18 Oct). Meta (21 Oct), Valero and Procter & Gamble (22 Oct) are the first likely entries.
- Day call record (S&P 500): 2 right of 5. 19 Oct: S&P 500 green called and right; portfolio green called and wrong.

## 12. Tools

- Tim's page: https://claude.ai/artifact/8P8UwQsb4QsbZMsKNYKrUJ, pinned in his Claude sidebar, with tabs Today, Macro, Performance, Risk, Calendar and Log. It reads four data files (`stocks`, `ledger`, `history`, `macro`) and a fifth dataset, `logos`, that no run touches. The Order panel reads the latest alert whose `stock` is "Order"; its "Enter before" bar uses a 07:00 UK cut-off (`CUTOFF`; page notes in `claude/ft-game-page.md`).
- Playbook docs (version 6.11): `claude/ft-game-playbook.md` (core, with the routing table), `claude/ft-game-rules.md`, `claude/ft-game-data.md`, and the run docs `claude/ft-game-run-evening.md`, `-morning`, `-refresh`, `-weekly`, `-weekend`.
- Panel file: `panel.json` on the same artifact, named by the document `store/panel`. The evening and weekly runs read and publish it (G1, G5).
- Scripts: the pipeline (version 7.4) and the screening script are assets on that artifact. Their ids and hashes are in part B of the playbook, the only place they are kept.
- Leftover assets: the four files the 14 Oct run uploaded (stocks 272fe63f..., ledger e4b81f05..., history 448fb462..., macro e67fb2ac...) are superseded but kept.
- Check before trusting the base: if the latest assets are newer than the dataset documents' `updated` time, an earlier run uploaded but did not finish publishing.
- Fetching assets: read each asset with a single `path`.
- Rate limits: on 18 Oct stockanalysis.com refused nothing in groups of four with 60-second pauses; on 19 Oct it refused 8 of the first 18 pages even in groups of two or three. tradingeconomics' US calendar showed "actual" figures for 19 to 22 Oct on 18 Oct (impossible): only its forecasts were used, and those should be checked against a second source.
- Market data service: massive.com, free plan, on an account opened by Tim's father. The key is in the evening and weekly review tasks and is never written into this project's docs, the page data, alerts or messages. Ask in halves of 125 and check three elements by index (done on 18 Oct for Visa, Mastercard, ConocoPhillips, Walmart: all matched). A panel stock's closes go to `panel_history`, not to its list history.
- No earnings calendar with actual figures is readable; the drift scan finds reporters by search (part F).
- Cboe's delayed quotes (`https://cdn-api.cboe.com/api/global/delayed_quotes/quotes/<TICKER>.json?r=<clock suffix>`): used on 19 Oct for 23 session rows when stockanalysis.com refused. Without a suffix it served a copy from the morning (16 Oct data); with one, fresh at 16:00 EDT. It gives open, high, low, close, previous close and volume, but no 52-week range, target or results date. Not yet in part F: for Tim to decide whether to add it.
- Coin prices: Coinbase's public candle and ticker pages.
- Sources that did not work: CNN article pages, CNBC's oil page; US News world article (fetch error, 18 Oct).
- GitHub mirror: private repository `timzwang/ft-game` (part B and G6). Reached by scheduled runs from 19 Oct: the evening and weekly review tasks were recreated on 18 Oct from a chat with the repository attached (section 8, item 5).
- Two saved skills, `ft-game-playbook` and `stock-score`, load in scheduled runs; the project docs win where they differ.
