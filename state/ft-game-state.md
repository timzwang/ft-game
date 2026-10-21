# FT Stock Picking Game: state and log

Last updated: Wed 21 Oct 2026, about 22:50 UK (hand-run session with Tim: playbook 6.13, the endgame stance, approved by Tim at 22:38 UK; Thursday's evening review switches the book for Fri 23 Oct's open; the order for Thu 22 Oct is unchanged). Before that, about 21:45 UK (evening review, a change evening: for Thu 22 Oct, Hasbro 5% added as a drift position and Eli Lilly cut from 15% to 10%, message sent about 21:39 UK; day -0.34% against SPY +0.53%; five watchlist additions, Walmart removed; price feed and broad scan both current after a forced run). About 22:05 UK, at Tim's request: the feed fault that kept Analog Devices off the list was fixed (feed 1.1, playbook 6.12.1), the review re-run with it added and the files republished; order unchanged. Before that, Wed 21 Oct 2026, about 14:30 UK (hand-run session with Tim: playbook 6.12, the price feed on GitHub and pipeline 7.7). Earlier entries: see the review log (section 6).

This doc is the narrative record for Tim's entry, "Seeking Beta". The procedure for every run is in `claude/ft-game-playbook.md` (the core doc) and the docs its routing table names. The numbers (prices, scores, daily performance, contributions, ratings and their outcomes, the full calendar, analyst changes, alerts, the panel test, the drift record) live in the data files behind Tim's page and the panel file, and are produced by the pipeline script; this doc carries the decisions and the reasons.

Messages: from 10 Oct Tim is sent a message only when there is something for him to enter or answer (playbook part I, "When Tim is told"). Quiet runs update the page and this doc and send nothing.

Scheduled runs: evening review 21:30 UK Sun to Thu; morning check 06:36 UK Mon to Fri; price refresh 16:45 UK and late price refresh 19:22 UK Mon to Fri; results-day refresh 14:50 UK Mon to Fri (acts only on results days); weekly performance review Sat 09:12 UK; weekend news check Sat and Sun 20:20 UK; midday check 12:40 UK Mon to Fri (switched off, see section 8).

**Cut-off: until the FT confirms it, every order must be entered before 07:00 UK (playbook part C, from 17 Oct).**

## 1. Status

- **Playbook version 6.13** (6.13, 21 Oct late evening: the endgame stance in core part D, approved by Tim at 22:38 UK: the score floor, trend tests, downtrend replacement, 10% caps on results, momentum and drift positions, results budget, volatility caps and theme guide suspended for the rest of the game; the book switches to high-beta technology at the 22 Oct evening review, order A or B by Western Digital's after-hours reaction; 6.12.1, 21 Oct late evening: feed 1.1 sends two years to every list or requested stock outside the price store, panel members included, and names any still short; the evening run re-requests a short candidate once before leaving it out; 6.12, 21 Oct afternoon: the price feed, a GitHub job whose `feed/latest.json` and `feed/live.json` the evening and weekly reviews and the price refreshes read first (data doc G8), pipeline 7.7 (7.6 plus the `feed` command) deployed, every page in a scheduled run reached through a search, the refresh tasks recreated with the repository; 6.11.1, 19 Oct late evening: the 26 Oct cut-off test removed at Tim's request; 6.11, 19 Oct evening: pipeline 7.4, `order_expected` with every change of order, and the repository's data check; 6.10, 19 Oct: pipeline 7.3 and a results budget of 1.0 points for reports dated 27 to 30 Oct; 6.9, 18 Oct: evening and weekly review tasks recreated with the repository attached; 6.8: G6 and G7 step 1; 6.7: pipeline 7.2, stricter price handling; 6.6: the handoff log; 6.5: the standstill test corrected; 6.4: after the outside audit, pipeline 7, 07:00 UK cut-off, score frozen; 6.3: the broad scan; 6.2: the day call never moves cash, "overbought" is a warning only; 6: split docs, panel test, earnings-drift scan). **Pipeline script version 7.7** (part B holds the asset id and hash).
- **Estimated value at Wed 21 Oct close: 101,378, +1.38% since the start, against -0.41% for the S&P 500 fund (gap +1.78 points).** Wed 21 Oct -0.34% against SPY +0.53%: Coca-Cola -0.17 points, Eli Lilly -0.15, AbbVie -0.15; Chevron +0.05, Shell +0.04, Microsoft +0.03, Exxon +0.02. Tech led, defensives and health care lagged (Tuesday's rotation reversed). Tue 20 Oct: 101,725.
- **Last FT figures: Fri 16 Oct after the close, 101,402 (+1.40%), rank 3,269 of 13,918 (top 23.5%).** RECONCILE -34 credits (-0.03%). Top 2% line about +6.5% (Tim's screenshots of 18 Oct; stored as `top2_return_pct` 6.5); gap to the line now roughly 5.1 points on the estimate.
- **Standstill (21 Oct run):** change for 13 Oct +0.61 (complete); 14 Oct -0.48 (complete); 15 Oct +0.50 (complete); 16 Oct -0.27 (four sessions); 19 Oct -0.43 (three). Week of 12 Oct +0.12; week of 19 Oct -0.43 so far. Inception (now fully priced, nine sessions): -0.62 as entered, -1.30 fully invested: the first order, never changed, would have done better so far. Expected benefit: the change for 22 Oct carries +0.05 (waiting to fill).
- **Panel test:** all 30 members now loaded (the feed added HPE's two years and MRSH's longer run, 21 Oct). History verdict "no evidence": average rank correlation +0.050 (t +1.3) over 49 dates; top third minus bottom third +0.46 points (t +0.8); one-year strength the strongest part (t +1.9). Live: no complete window yet. The score is frozen for the rest of the game.
- **Order for Thu 22 Oct's open (changed 21 Oct, message sent about 21:39 UK):** Coca-Cola 20, Exxon Mobil 15, Shell 15, Microsoft 15, Eli Lilly 10, Chevron 10, AbbVie 10, Hasbro 5, cash 0. Order in force until then (filled Mon 19 Oct): the same with Eli Lilly 15 and no Hasbro.
- Day call for Thu 22 Oct: S&P 500 red 46% (usual 55%); portfolio green 63% (usual 60%); no adjustment (Meta's after-hours reaction mixed). Record (S&P 500): 4 right of 7. Wed 21 Oct: S&P 500 green called and right (+0.53%); portfolio green called and wrong (-0.34%).
- Macro at Wed 21 Oct: US 2-year 4.81%, 10-year 5.13% (-11bp over five sessions: a tailwind on the mechanical label), 30-year 5.42%. Gilt 5.38%, German 3.41%, French 4.97%, Italian 4.56%, Japanese 2.90%. Brent $109.60 (+0.6%), WTI $97.75, natural gas $2.77, gold $4,134. UK CPI 3.5% in September against 3.4% expected; a Bank of England hike in November is being priced. Backdrop label: tailwind.
- Crypto: Bitcoin $84,436 at the US close (+3.3% on the day, +1.5% over five); trend up (IBIT 1.4% above its 20-day, 6.9% above its 50-day). Ether $2,493 (+4.2%), trend up. No holding is crypto-linked.
- Regime: mixed. Wed 21 Oct: S&P 500 +0.5% (SPY +0.53% to 773.09), a fourth straight gain, Nasdaq about +0.9% (tech and SpaceX led), defensives trailed cyclicals. Earnings: Elevance beat and raised (shares only modestly up), AT&T beat and raised its EPS guide but fell, Netflix fell sharply on its tax hit and ad outlook. Meta beat on revenue after the close with strong guidance; shares reported lower after hours. What would make it risk-off: the 10-year back above 5.25% with the S&P 500 below its 20-day, or a hike on 28 Oct priced above 70%.

## 2. Current portfolio

The order for Thu 22 Oct's open (assumed entered from the 21 Oct message). Scores and bands from the pipeline at the Wed 21 Oct close; confidence ratings as given on 18 Oct, Hasbro's on 21 Oct.

| Stock | Weight | Cap | Confidence (not calibrated) | Score | Band | Flags | Next results | Substitute if missing |
|---|---|---|---|---|---|---|---|---|
| Coca-Cola | 20% | 20% | 59 | 67 | Strong | none | 27 Oct, before US open (implied 4.2%) | PepsiCo (downtrend: cash instead) |
| Exxon Mobil | 15% | 15% | 60 | 83 | Strong | none | 30 Oct, before US open (implied n/a, 6% used) | ConocoPhillips |
| Shell | 15% | 15% | 59 | 66 | Strong | none | 29 Oct, 07:00 UK (implied n/a, 6% used) | BP |
| Microsoft | 15% | 15% | 57 | 69 | Strong | none | 28 Oct, after US close (implied 6.0%) | Alphabet (not scored) |
| Eli Lilly | 10% | 15% | 59 | 79 | Strong | none; Barclays $1,400 kept (21 Oct) | 29 Oct, before US open (implied 7.9%) | Merck |
| Chevron | 10% | 15% | 59 | 78 | Strong | none | 30 Oct, before US open (implied 5.8%) | ConocoPhillips |
| AbbVie | 10% | 15% | 60 | 72 | Strong | none | 30 Oct, before US open, confirmed (implied 6.4%) | Amgen |
| Hasbro | 5% | 10% | 57 | 75 | Strong | Drift position; extended (23% above 50-day); overbought (RSI 86); at 52-week high | Feb 2027 (est.) | Mattel (not scored) |
| Cash | 0% | | | | | | | |

Ratings stay near 55 to 60: the panel test finds no evidence that a high score is an edge. Hasbro's 57 is its anchor (62) less 5 for the extension.

Points for the coming reviews:

- Themes: Energy 40%, Consumer staples 20%, Health care 20%, Software 15%, Media 5%. Risk shares: Exxon 22.4%, Coca-Cola 20.0%, Shell 17.7%, Chevron 13.2%, AbbVie 11.5%, Eli Lilly 9.7%, Hasbro 5.9%, Microsoft -0.3% (oil names 53%). Worst scenario: ceasefire or Hormuz reopening -1.75%.
- **Results cluster:** weight times implied move against the 1.0 budget for 27 to 30 Oct: Coca-Cola 0.84, Microsoft 0.90, Shell 0.90 (6% used), Eli Lilly 0.79 (trimmed tonight, now within budget), Exxon 0.90 (6% used), Chevron 0.58, AbbVie 0.64. RESULTS TOTAL next 10 sessions 5.55 points across seven reports, deliberate (the entry needs variance), oil names 2.4 points of it. Implied moves are earnings-watcher's of 16 Oct; Exxon's and Shell's pages were not found by search tonight. Last orders: Coca-Cola before 07:00 UK Mon 26 Oct; Shell, Eli Lilly and Microsoft before 07:00 UK Wed 28 Oct; Exxon, Chevron and AbbVie before 07:00 UK Thu 29 Oct. The Sunday 25 Oct review should refresh every implied move.
- **Hasbro (drift position from 22 Oct's open):** exit at the next open after a heavy-volume close below its open, a close below 104.01 (midpoint of 98.49 and 109.52), five sessions without a new high (high so far 114.05, 21 Oct), or after ten sessions (by the 3 Nov close). Never average up.
- Keep TSMC on the list until Fri 23 Oct and Palantir until Mon 26 Oct (standstill test), then they may be removed.
- Shadow ratings still open for stocks off the list: Constellation Energy, CrowdStrike, Marvell (the weekly review gives their rows).

## 3. Pending order

**The switch (approved by Tim, Wed 21 Oct 22:38 UK; core playbook part D, endgame stance).** Thu 22 Oct's evening review sells every holding and sets order A or order B (part D's table) for Fri 23 Oct's open, by Western Digital's after-hours reaction to its results. The order for Thu 22 Oct below is unchanged.

**Changed for Thu 22 Oct's open (21 Oct evening review). Message sent about 21:39 UK on Wed 21 Oct; taken as entered unless Tim says otherwise.**

Coca-Cola 20, Exxon Mobil 15, Shell 15, Microsoft 15, Eli Lilly 10, Chevron 10, AbbVie 10, Hasbro 5, cash 0.

Changes: add Hasbro 5 (drift position, second-session test passed); Eli Lilly 15 to 10 (results-budget trim due before 28 Oct, done now). Expected benefit recorded: +0.05 points over five sessions (subjective). What would show it wrong: Hasbro closes below its open on heavy volume or below 104.01 within five sessions, or Lilly outruns Hasbro by more than 1.5 points into its report.

## 4. Watchlist

Scores and bands at the Wed 21 Oct close. 23 names. Added Charles River Laboratories, Centene, Targa Resources, Analog Devices, NetApp. Removed Walmart (rotate out). Hasbro moved into the order.

| Name | Band | Status | Score | Flags | Next results | Promote if |
|---|---|---|---|---|---|---|
| Charles River Laboratories | Strong | Needs follow-through (added 21 Oct) | 85 | extended; overbought | 4 Nov (est.) | 5% after a second session closing above its open in the upper half of its range |
| Visa | Strong | Watching | 80 | overbought; at 52-week high | 27 Oct, after US close (est.) | Steady name if a holding weakens; not held through results above 10% |
| Mastercard | Strong | Watching | 78 | overbought; at 52-week high | 29 Oct (est.) | Alternative to Visa, not both |
| Valero Energy | Strong | Results ahead | 77 | none | 22 Oct (time est.) | Not before results; drift tests after |
| ConocoPhillips | Strong | Watching | 74 | none; 0.83 with Exxon | 5 Nov (est.) | Swap for Exxon or Chevron before their 30 Oct results if a report needs dodging |
| Phillips 66 | Strong | Watching | 72 | none | 28 Oct, before US open | Only in place of an oil major |
| Humana | Strong | Ready | 70 | none | 6 Nov | 5% (cap) if a holding weakens |
| Palantir | Strong | Watching (sold 19 Oct) | 69 | none | 2 Nov | Keep until 26 Oct (standstill test) |
| BP | Strong | Watching | 69 | faded gap; 0.87 with Shell | 30 Oct (est.) | Substitute for Shell |
| Merck | Strong | Watching | 68 | none | 29 Oct | Substitute for Lilly |
| Targa Resources | Strong | Watching (added 21 Oct) | 67 | none | 5 Nov (est.) | Midstream alternative to an oil major |
| Centene | Strong | Watching (added 21 Oct) | 65 | none (a -40% day in July 2025 is in its history) | 28 Oct (est.) | Not before results; managed care read from Elevance |
| UnitedHealth | Strong | Ready | 64 | none | Jan 2027 (est.) | Up to 10% if a holding weakens |
| Marathon Petroleum | Strong | Watching | 63 | extended | 3 Nov | 5% at most while extended |
| Analog Devices | Strong | Watching (added 21 Oct) | 64 | none | 25 Nov (est.) | Chip exposure if the tech rebound holds (correlation -0.37 with the order) |
| NetApp | Strong | Watching (added 21 Oct) | 63 | none | 25 Nov (est.) | Tech exposure if the rebound holds; cap 5% |
| Strategy (crypto tracker) | Strong | Watching | 62 | golden cross 19 Oct; moves with Bitcoin | 29 Oct (est.) | Kept whatever it scores |
| Amgen | Strong | Watching | 62 | none | 3 Nov, after US close | Steady name (cap 20%) |
| Procter & Gamble | Weak | Results ahead | 54 | downtrend | 22 Oct (est.) | Not while in a downtrend |
| TSMC | Middling | Watching | 50 | below 50-day; faded gap | Jan 2027 | Keep until Fri 23 Oct, then remove |
| Meta Platforms | Middling | Results ahead | 50 | golden cross 6 Oct | reported 21 Oct, after US close | Drift tests on 22 Oct's session |
| Coinbase (crypto tracker) | Weak | Watching | 44 | downtrend; below 50-day | 29 Oct, after US close | Kept whatever it scores |

Intake tonight: five additions. Analog Devices was first left out because the feed gave it only 10 rows (a feed fault, fixed the same evening in feed 1.1) and was added on the re-run with two years of rows. Consensus targets for the four came from Benzinga pages that were days or weeks old, so targets were left empty for Charles River, Centene and Targa. Candidates not yet checked: Viatris, Biogen, Illumina, Devon Energy, Ross Stores, Tate & Lyle, Rotork.

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
| Wed 21 Oct, about 21:39 UK (message sent; assumed entered) | Thu 22 Oct | Add Hasbro 5; Eli Lilly 15 to 10 | Hasbro's drift entry confirmed by a second session (+4.1% on 2.8 times volume, closed at the high); Lilly's results-budget trim (7.9% implied, 1.19 points at 15%) done now. Expected +0.05 points (subjective) |

## 6. Review log (newest first, keep the latest 15)

- Wed 21 Oct 2026 (about 22:50): Hand-run session with Tim. Playbook 6.13: Tim approved the endgame stance (core part D) after the gap maths gave the order in force about a 1% chance of the top 2%; rules suspended for the rest of the game as listed there; the switch to a high-beta book is set for Thursday's evening review (order A or B). Order for Thu 22 Oct unchanged.
- Wed 21 Oct 2026 (about 22:30): Tim's answers recorded: Marsh & McLennan stays in the panel (no swap on 24 Oct); he deleted the `claude/feed-test` branch and merged PRs #3 and #5; he will ask FT help how a mixed London and US order fills on 26 Nov. Research checks (top-five panel test, overbought split) prepared on a branch, PR #7, not deployed. Order, rules and data unchanged.
- Wed 21 Oct 2026 (about 22:10): At Tim's request after the evening review: feed 1.1 (`2b276c4`; a panel member requested as a candidate had been sent only 10 rows), playbook 6.12.1 (evening run step 4, data doc G8), feed 1.1 also widens Yahoo bars whose open lies outside their range (UnitedHealth's 21 Oct high corrected to 421.80); two regression tests (160 pass). Review re-run with Analog Devices added (score 64, strong); AT&T's drift row completed (still FAIL); stocks, ledger, history and panel files republished. Order unchanged.
- Wed 21 Oct 2026 (about 21:45): Evening review, a change evening for Thu 22 Oct (Hasbro 5 added as a drift position; Eli Lilly 15 to 10). Day -0.34% against SPY +0.53% (Coca-Cola, Lilly, AbbVie -0.15 to -0.17 points each as tech led and defensives lagged). Drift scan: Elevance, AT&T, Netflix all FAIL. Watchlist: added Charles River Laboratories, Centene, Targa Resources, NetApp; removed Walmart. Price feed: forced (request pushed 21:32 UK, close run at 21:32 UK, second run for nine new tickers at 21:36 UK); broad scan: forced. Charles River's 21 Oct row from the feed had its open below its low (Yahoo); the low was set to the open (313.83, which matches the range StocksToTrade reported). Files published.
- Wed 21 Oct 2026 (about 14:30): Hand-run session with Tim. Playbook 6.12: the price feed on GitHub (`feed/`, data doc G8) after the 20 Oct fetch refusals; pipeline 7.7 (7.6 from PR #6 plus the `feed` command) deployed, byte-identical to 7.6 on the snapshot and the 20 Oct mirror; page wording from 19 Oct deployed; refresh tasks recreated with the repository. Order, watchlist, score and rules unchanged.
- Tue 20 Oct 2026 (about 22:05): Evening review, quiet: no change for Wed 21 Oct. Day +0.62% against SPY +0.34% (Lilly +0.52 points at a record). Drift scan: Hasbro ENTER (not bought: watchlist "Drift: day 1"), Equifax FAIL. WebFetch refused every address that had not first appeared in a search result. Files published.
- Mon 19 Oct 2026 (about 22:25): Hand-run session with Tim. The Mon 26 Oct 07:15 UK cut-off test removed (playbook 6.11.1, part C). Pipeline 7.6 prepared on a branch, not deployed.
- Mon 19 Oct 2026 (about 22:15): Evening review, quiet: no change for Tue 20 Oct. Day -0.33% against SPY +0.42%. AbbVie results event added; implied moves stored for five holdings. Files published.
- Mon 19 Oct 2026 (about 20:40): Hand-run session with Tim after ChatGPT's follow-up review (PR #3): pipeline 7.4 (`order_expected`) and the repository data check; playbook 6.11.
- Mon 19 Oct 2026 (about 00:35): Hand-run session with Tim after ChatGPT's repository review of 18 Oct: pipeline 7.3 and a results budget of 1.0 points for 27 to 30 Oct; playbook 6.10.
- Sun 18 Oct 2026 (about 22:05): Tim confirmed the Mon 19 Oct order is entered; the top 2% line is about +6.5%, about 5 points above Tim.
- Sun 18 Oct 2026 (about 21:50): Evening review, a change evening for Mon 19 Oct (Palantir out; Chevron 15 to 10; AbbVie 10). Tim's 16 Oct FT figures stored (-34 credits against the estimate). Four watchlist additions; three removals.
- Sun 18 Oct 2026 (about 20:25): Weekend news check (H7, Sunday). No A item. Order unchanged.
- Sun 18 Oct 2026 (about 10:50): Follow-up approved by Tim. GitHub access test passed. Playbook 6.8.
- Sun 18 Oct 2026 (about 01:20): Hand-run session with Tim. Playbook 6.6: the handoff log.

## 7. Market regime notes

Label: Mixed (tech rebounding after its October sell-off while health care, staples and energy, the portfolio's core, paused; yields above 5% but falling over the week; oil near five-month highs with a peace-talk tail risk).

Wed 21 Oct: S&P 500 about +0.5% (SPY +0.53% to 773.09), a fourth straight gain; Nasdaq about +0.9%; tech led (SpaceX about +8%, chips up), defensives trailed. Elevance beat and raised (EPS $6.99 against $4.70; 2026 guide at least $29); AT&T beat and raised its EPS guide to about $2.40 but fell; Netflix fell sharply (tax hit, ad outlook). Charles River Laboratories +9% on its investor day and a UBS upgrade. Meta after the close: revenue beat and strong guidance, shares reported lower after hours; Tesla and IBM also reported. Brent about $109.6 after trading either side of $108 to $110 (Hormuz flows against attack worries; a US crude stock draw). UK CPI 3.5% against 3.4% expected; gilts near 5.4%. 20-year bond auction in line (reported).

Tue 20 Oct: S&P 500 about +0.3%, Dow about +1%, Nasdaq flat; health care at a record; Housing starts 1.221M against 1.30M. Brent touched about $111, then eased on an unconfirmed Qatar and Pakistan framework for US-Iran talks.

Mon 19 Oct: S&P 500 +0.41%, Nasdaq +1.11%; NAHB 29 (lowest since 2012); 10-year +6bp to 5.15%.

Week to Fri 16 Oct: S&P 500 -1.95% on the week, Nasdaq -4.48%; VIX 20.16. Fed: September minutes backed a 25bp hike; December hike odds about 74%, October about 25% to 30% (19 Oct).

Weekend log (weekend of 17 and 18 Oct): confirmed by the Sunday evening review. No A item. B: Hormuz (Araghchi's offer "still on the table"); Russia sanctions waiver. Earlier weekend (10 and 11 Oct): no A item.

Near calendar (the full calendar to 27 Nov is on the page and in the ledger):
- Thu 22 Oct: Valero, Procter & Gamble, Lockheed Martin before the open; Meta's reaction session (drift tests); jobless claims 13:30 UK (forecast about 200,000); Conference Board leading index. Hasbro fills at the open.
- Fri 23 Oct: flash PMIs; Michigan sentiment final. TSMC may leave the list after this session.
- Sun 25 Oct: UK clocks go back; the US session is 13:30 to 20:00 UK in the week of 26 Oct. The evening review sets the order for Coca-Cola's results and refreshes every implied move.
- Mon 26 Oct: Coca-Cola's last order, before 07:00 UK.
- Tue 27 Oct: Coca-Cola; Visa (after the close, est.). Wed 28 Oct: Fed decision 18:00 UK; Microsoft; Phillips 66; Centene (est.). Thu 29 Oct: Shell; Eli Lilly; Merck; Mastercard; Coinbase. Fri 30 Oct: Exxon Mobil, Chevron, AbbVie. Tue 3 Nov: US midterms; Amgen. Wed 4 Nov: Charles River (est.). Thu 5 Nov: ConocoPhillips; Targa (est.).

## 8. Open questions for Tim

Answered: an order entered before 08:00 UK counted for that day up to 23 Oct (from 17 Oct treat 07:00 UK as the cut-off); the midday check stays off; the leaderboard shows only the top 10; Shell filled at its 08:00 open on 9 Oct; Microsoft, Coca-Cola, Palantir, Goldman Sachs, Meta Platforms and Eli Lilly are in the game's list; the orders for 13 to 16 Oct were entered; value, rank and players after Fri 16 Oct's close; the Marsh & McLennan panel swap; GitHub access from scheduled runs; the top 2% line (about +6.5%, 18 Oct); the evening run's repository (tasks recreated 18 Oct); the fetch tool refusing built addresses in scheduled runs (answered 21 Oct by the price feed, playbook 6.12); Marsh & McLennan stays in the panel (Tim, 21 Oct about 21:44 UK: the panel stays exactly as fixed on 15 Oct, so the weekly review of 24 Oct does not swap it).

Still open:
1. Is AbbVie in the game's list? Assumed yes (large NYSE listing); substitute Amgen. Tim to say if it was missing.
2. New on 21 Oct: is Hasbro in the game's list? Assumed yes (large Nasdaq listing); if missing, leave the 5% with Eli Lilly (15%) for that day and say so.
3. Are Strategy and Coinbase in the game's list? Not needed until one is close to being bought.
4. The cut-off after the clock change: 07:00 or 08:00 UK. Tim asked FT help on 18 Oct. 07:00 UK stays until the FT answers. Tim will also ask how a mixed London and US order entered for 26 Nov (US closed) fills (21 Oct).
5. Does the game convert US stocks' returns into pounds? In the draft to FT help; the closing gap has stayed under 0.05%.

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

- Lesson: judge a change over the five sessions it was meant for (the STANDSTILL block), not its first day, and judge the process against the first order never changed. On 21 Oct, with nine sessions priced, the first order never changed was ahead by 0.62 points as entered.

**Hasbro, 20 and 21 Oct (a drift entry bought on its second session)**

| Date | Open | High | Low | Close | Volume |
|---|---|---|---|---|---|
| Tue 20 Oct (reaction day) | 102.40 | n/a | n/a | 109.52 | 7.3m |
| Wed 21 Oct | 110.27 | 114.05 | 109.60 | 114.00 | 5.2m (2.8 times average) |

- Bought for 22 Oct at 5% (extended). The outcome is the test of buying drift on day two rather than day one.

## 11. Confidence ratings, shadow ratings, the panel test and the day call

- Confidence ratings (not calibrated): 13 resolved by 21 Oct. Latest: Eli Lilly (14 Oct) beat. Earlier: Meta 57 lagged, RTX 60 beat, Lockheed 55 beat, Nvidia 50 lagged, Shell 59 beat, TSMC 53 lagged, Coca-Cola 55 beat, Goldman 54 beat, Microsoft 58 beat, Palantir 58 lagged. Far too few to judge. Ratings for the order of 22 Oct: Exxon 60, AbbVie 60, Coca-Cola 59, Shell 59, Chevron 59, Eli Lilly 59, Microsoft 57, Hasbro 57.
- Shadow ratings: 213 logged, 88 settled. Live: score 70 and above, 30 cases, 67% beat the index (+0.77 points); 60 to 69, 25 cases, 40% (-3.47); 45 to 59, 17 cases, 18% (-2.70); below 45, 16 cases, 81% (+2.41). Weak evidence, few dates. Judgement test: no settled dates yet.
- Panel test: see section 1. Old backtest (hindsight) correlation -0.09.
- Drift record: Hasbro ENTER and Equifax FAIL (20 Oct); Elevance, AT&T and Netflix FAIL (21 Oct; AT&T's revenue consensus missing; its volume and trend figures, first missing through the feed fault, were filled on the re-run: trend fails). All settle five sessions after their reaction days. Meta (22 Oct), Valero and Procter & Gamble (22 Oct) are the next likely entries.
- Day call record (S&P 500): 4 right of 7. 21 Oct: S&P 500 green called and right; portfolio green called and wrong.

## 12. Tools

- Tim's page: https://claude.ai/artifact/8P8UwQsb4QsbZMsKNYKrUJ, pinned in his Claude sidebar, with tabs Today, Macro, Performance, Risk, Calendar and Log. It reads four data files (`stocks`, `ledger`, `history`, `macro`) and a fifth dataset, `logos`, that no run touches. The Order panel reads the latest alert whose `stock` is "Order"; its "Enter before" bar uses a 07:00 UK cut-off.
- Playbook docs (version 6.13): `claude/ft-game-playbook.md` (core, with the routing table), `claude/ft-game-rules.md`, `claude/ft-game-data.md`, and the run docs `claude/ft-game-run-evening.md`, `-morning`, `-refresh`, `-weekly`, `-weekend`.
- Panel file: `panel.json` on the same artifact, named by the document `store/panel`.
- Scripts: the pipeline (version 7.7) and the screening script are assets on that artifact. Their ids and hashes are in part B of the playbook, the only place they are kept.
- Leftover assets: the four files the 14 Oct run uploaded are superseded but kept.
- Fetching assets: read each asset with a single `path`.
- Price feed (from 21 Oct, data doc G8): `feed/latest.json` and `feed/live.json` in the repository. First evening use 21 Oct: the scheduled close run had not yet run at 21:31 UK, so a pushed request forced it (about one minute); a `tickers:` line for nine new names was served within about a minute too. Every list stock, SPY, the extra rows, the panel and the US yields and coins came from it; nothing was missing or refused. Two caveats: a panel member requested as a candidate (Analog Devices) came back with only 10 rows, a feed fault fixed in feed 1.1 the same evening (`meta.short_history` now names any list or requested stock still short of 200 sessions); and two Yahoo bars (Charles River and UnitedHealth, 21 Oct) had their open outside their own range: corrected by hand on 21 Oct, and feed 1.1 now widens such bars itself (`meta.ranges_widened`).
- Pages reached through searches on 21 Oct: tradingeconomics' commodity and UK bond pages (non-US yields, Brent, WTI, gas, gold), news articles. Benzinga quote pages served copies days or weeks old (targets not used). earnings-watcher pages were not surfaced by search, so implied moves were not refreshed.
- Market data service: massive.com, free plan, on an account opened by Tim's father. The key is in the evening and weekly review tasks and is never written into this project's docs, the page data, alerts or messages. Not used on 21 Oct (the feed covered every price).
- Cboe's delayed quotes: used on 19 Oct; not yet in part F: for Tim to decide whether to add it.
- Sources that did not work: Chartmill news pages (need JavaScript, 21 Oct); CNN article pages, CNBC's oil page and live-updates page (fetch error 20 Oct), Detroit News (robots); US News world article (18 Oct).
- GitHub mirror: private repository `timzwang/ft-game` (part B and G6), reached by scheduled runs from 19 Oct.
- Two saved skills, `ft-game-playbook` and `stock-score`, load in scheduled runs; the project docs win where they differ.
