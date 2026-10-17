# FT Stock Picking Game: state and log

Last updated: Sun 18 Oct 2026, about 00:30 UK (hand-run session with Tim: playbook version 6.4 and pipeline version 7 after the outside audit of 17 Oct; Tim's FT figures for Fri 16 Oct recorded below for Sunday's review to store; order unchanged. Before that: Sat 17 Oct about 20:25 UK weekend news check; about 09:50 UK weekly review: Fri 16 Oct session logged, panel topped up to 28 of 30 members with two years, files published; Fri 16 Oct about 09:10 UK, hand-run session with Tim, broad scan built and playbook version 6.3)

This doc is the narrative record for Tim's entry, "Seeking Beta". The procedure for every run is in `claude/ft-game-playbook.md` (the core doc) and the docs its routing table names. The numbers (prices, scores, daily performance, contributions, ratings and their outcomes, the full calendar, analyst changes, alerts, the panel test, the drift record) live in the data files behind Tim's page and the panel file, and are produced by the pipeline script; this doc carries the decisions and the reasons.

Messages: from 10 Oct Tim is sent a message only when there is something for him to enter or answer (playbook part I, "When Tim is told"). Quiet runs update the page and this doc and send nothing.

Scheduled runs: evening review 21:30 UK Sun to Thu; morning check 06:36 UK Mon to Fri (07:26 until 17 Oct); price refresh 16:45 UK and late price refresh 19:22 UK Mon to Fri; results-day refresh 14:50 UK Mon to Fri (acts only on results days); weekly performance review Sat 09:12 UK; weekend news check Sat and Sun 20:20 UK; midday check 12:40 UK Mon to Fri (switched off, see section 8). One-off: GitHub access test Sun 18 Oct 10:07 UK.

**Cut-off: until the FT confirms it, every order must be entered before 07:00 UK (playbook part C, from 17 Oct).**

## 1. Status

- **Playbook version 6.4** (6.4, 17 Oct: after the outside audit, pipeline version 7 with the standstill test, drift settled from the next open, the results total, FT reconciliation and the judgement test; 07:00 UK cut-off and 06:36 morning check; score frozen for the game; 6.3: the broad scan, G7; 6.2: the day call never moves cash, "overbought" is a warning only; 6: split docs, panel test, earnings-drift scan). **Pipeline script version 7** (part B: asset fdfb8e10..., sha256 23e9c9fe...), tested on 17 Oct against the live files: stocks, history, macro and panel came out byte for byte the same as version 6, and the new lines matched figures worked out by hand.
- **Estimated value at Fri 16 Oct close: 101,437, +1.44% since the start, against -1.67% for the S&P 500 fund (gap +3.11 points).** Week of 12 to 16 Oct: +1.51% against -1.97%. Fri 16 Oct +0.64% (Coca-Cola +0.41 points, Chevron +0.39, Exxon +0.37; Palantir -0.36, Microsoft -0.31).
- **Last FT figures: Fri 16 Oct after the close, 101,402 (+1.40%), rank 3,269 of 13,918 (top 23.5%).** Sent by Tim on Sat 17 Oct as a screenshot. Not yet in the ledger: the Sunday evening review puts them in `reported` (`date` 2026-10-16, `time_uk` "after close", `value` 101402, `rank` 3269, `players` 13918, `note` "Screenshot sent Sat 17 Oct; the game's chart shows the same closing value"). Against the estimate: -35 credits (-0.03%), so the estimate is verified at the close. The game's own chart puts its closes at about 100,565 (12 Oct), 101,060 (13 Oct), 101,190 (14 Oct) and 100,775 (15 Oct), each within about 40 credits of the estimate: the 144-credit gap on 13 Oct came from reading the figure at 20:59, during the US session. Top 2% line: rank 278 of 13,918; its return is not known (about +4% to +4.5% on 13 Oct, not verified since).
- **Standstill (first result, pipeline version 7, worked out on 17 Oct with Nvidia and Goldman Sachs closes fetched for the purpose):** the week from 12 Oct's four changes added about +0.86 points against keeping the Mon 12 Oct order (+0.83% against -0.02%), mostly from selling Nvidia (about +0.45) and TSMC (about +0.18). Each change's one-day effect looked negative for 13 and 14 Oct (-0.17, -0.14), which is why the outside audit read the changes as adverse; over several sessions they paid. Four days in one regime prove little.
- **Panel test (17 Oct, 28 of 30 members with two years):** history verdict still "no evidence": average rank correlation +0.042 (t +1.1) over 49 dates, positive on 61%; top third minus bottom third +0.25 points (t +0.4). Parts: one-year strength +0.087 (t +1.7), two-month +0.053 (t +1.4), five-day +0.007 (t +0.2). Live: no complete window yet. Not loaded: Marsh & McLennan (190 sessions; Tim agreed on 17 Oct to replace it with the next position down, for the weekly review of 24 Oct), Hewlett Packard Enterprise (left for 24 Oct). All members are one session behind (16 Oct). The score is frozen for the rest of the game (agreed 17 Oct).
- Order in force for Mon 19 Oct's open (unchanged; the Sunday review decides): Coca-Cola 20, Exxon Mobil 15, Chevron 15, Shell 15, Microsoft 15, Eli Lilly 15, Palantir 5, cash 0.
- **Palantir exit signal on Fri 16 Oct:** closed at 186.03, 7.8% below its open of 201.79, on heavy volume (33.2m), with no new high since 12 Oct (212.94); score 48, middling. Under the momentum rule it is sold at the next open: for the Sunday review.
- Day call: the run logged Mon 19 Oct's figures (S&P 500 green 53%, usual 55%; portfolio green 63%, usual 60%) with no cases; Sunday's review writes them. Record (S&P 500): 1 right of 4, the same as always saying green (1); Brier 0.266. Portfolio: 3 of 4, the same as always green; Brier 0.205.
- Macro at Fri 16 Oct close: US 2-year 4.74%, 10-year 5.09% (-15bp on the week), 30-year 5.43%. Gilt 5.38% (-4bp on the week), German 3.41%, French 4.79%, Italian 4.48%, Japanese 2.93% (tradingeconomics, read Saturday without a timestamp). Brent $109.86 (+3.7% on the day, +5.2% on the week), WTI $101.41, gold $4,166. Backdrop label: neutral (yields a tailwind, oil an inflation worry).
- Crypto: Bitcoin $81,477 at the US close (-0.9% on the week), trend up (IBIT 2.7% below its 20-day, 4.7% above its 50-day). Ether -2.6%, Solana -5.6%, XRP -6.0% over five sessions: appetite thinning at the edges. Strategy -9.6% and Coinbase -5.8% on Friday (MSCI exclusion reports). No holding is crypto-linked.
- Regime: mixed. Inflation ran hot all week (CPI core 2.6%, PPI +1.3% on the month, import prices +1.1%, industrial production +0.7% against 0.4%), yet the 10-year fell 15bp. Fri 16 Oct: S&P 500 -1.11% as investors rotated out of chips and AI (Palantir, CrowdStrike, Marvell, Meta all down 4% to 8%) into staples, payments and energy. What would make it risk-off: the 10-year back above 5.25% with the S&P 500 below its 20-day (it is now 1.0% below it), or a hike priced above 70%.

## 2. Current portfolio

The order in force for Mon 19 Oct's open. Scores and bands from the pipeline at the Fri 16 Oct close.

| Stock | Weight | Cap | Confidence (15 Oct, not calibrated) | Score | Band | Flags | Next results | Substitute if missing |
|---|---|---|---|---|---|---|---|---|
| Coca-Cola | 20% | 20% | 57 | 80 | Strong | at 52-week high | 27 Oct, before US open | PepsiCo (downtrend: cash instead) |
| Exxon Mobil | 15% | 15% | 62 | 82 | Strong | at 52-week high | 30 Oct, before US open | ConocoPhillips |
| Chevron | 15% | 15% | 61 | 80 | Strong | at 52-week high | 30 Oct | ConocoPhillips |
| Shell | 15% | 15% | 60 | 81 | Strong | overbought (warning only); at 52-week high | 29 Oct | BP |
| Microsoft | 15% | 15% | 62 | 65 | Strong | EMAs mixed; closed 2.3% below its open on 16 Oct | 28 Oct (time est.) | Alphabet (not scored) |
| Eli Lilly | 15% | 15% | 62 | 76 | Strong | none | 29 Oct | AbbVie |
| Palantir (momentum position) | 5% | 5% | 57 | 48 | Middling | heavy-volume down day: exit signal | 2 Nov | leave in cash |
| Cash | 0% | | | | | | | |

Points for the coming reviews:

- **For Sunday 18 Oct (agreed with Tim on 17 Oct):**
  - Palantir's exit signal (above).
  - Concentration. Exxon and Chevron correlate at 0.94 and together hold 30%, at the edge of the part D test; the three oil names carry about 64% of the portfolio's risk, above the 60% warning level in part D, and all three report on 29 and 30 Oct. Tim's view, agreed on 17 Oct as a view and not a rule: cut one of Exxon and Chevron to 10% before their 30 Oct results (last order before the cut-off on Thu 29 Oct), moving the weight to a strong non-energy name such as AbbVie (score 72, steady, first candidate for the Palantir slot) if it still passes the rules. The evening review decides the timing and size under parts D and E, with a confidence rating, and says why if it keeps the pair as is.
  - Shell's price rows. The stored 12 Oct row is a placeholder (open, high, low and close all 3,836). stockanalysis.com's London history (read 17 Oct) gives 12 Oct open 3,768, high 3,855, low 3,759.5, close 3,836, volume 5,002,093; and 9 Oct close 3,793.5 (stored 3,795.5), open 3,752.5 (stored 3,753). Check against lse.co.uk or the history page, and give the corrected 9 and 12 Oct rows in Shell's `history` (the script recalculates from 9 Oct; the effect is a few thousandths of a point).
  - The standstill test needs today's row for stocks sold in the last five sessions that are off the list (the template names them; on Sunday: Goldman Sachs, Lockheed Martin, Nvidia, RTX, Friday's rows from their history pages under `extra_history`). Goldman's stored 14 Oct open is 881.35 against 880.93 on stockanalysis.com: give the page's figure if it still says so.
  - Keep TSMC on the list until it has been off the order five sessions (sold 16 Oct; may be removed from Fri 23 Oct), under the new rule in part E.
- Themes: Energy 45% (at the guardrail), Consumer staples 20%, Software 20%, Health care 15%. Risk shares: Exxon 22.6%, Chevron 22.5%, Coca-Cola 19.6%, Shell 18.6%. Worst scenario: ceasefire or Hormuz reopening -2.02%.
- **Results cluster:** Coca-Cola 27 Oct, Microsoft 28 Oct, Shell and Eli Lilly 29 Oct, Exxon and Chevron 30 Oct: every core holding reports inside four sessions. Implied moves for all six are needed from the Mon 20 Oct evening review (part E now asks for them inside ten sessions). At the default 6% each, the RESULTS TOTAL for those reports is 5.7 points; each one is over the 0.6 budget on its own (Coca-Cola at 20% holds through only if its implied move is 3% or less). Coca-Cola reports before the US open on Tue 27 Oct, so its last order goes in before the cut-off on Mon 26 Oct, set by the Sunday 25 Oct evening review.
- TSMC post-mortem logged on 17 Oct (return -9.27% over five sessions, -0.96 points).

## 3. Pending order

No change since the Fri 16 Oct order. The weekly review does not change the order; the Sunday evening review does.

Coca-Cola 20, Exxon Mobil 15, Chevron 15, Shell 15, Microsoft 15, Eli Lilly 15, Palantir 5, cash 0. Last change: correction message about 21:51 UK on Thu 15 Oct, entered (Tim confirmed 22:00 UK). From 17 Oct every change message gives 07:00 UK as the deadline.

## 4. Watchlist

Scores and bands at the Fri 16 Oct close.

| Name | Band | Status | Score | Flags | Next results | Promote if |
|---|---|---|---|---|---|---|
| Phillips 66 | Strong | Watching | 83 | none | 28 Oct, before US open | Only in place of an oil major (energy at 45%) |
| Marathon Petroleum | Strong | Watching | 75 | extended | 3 Nov | 5% at most while extended; energy at 45% |
| Valero Energy | Strong | Results ahead | 73 | extended | 22 Oct (time est.) | Not before results; drift tests after |
| BP | Strong | Watching | 72 | none | 30 Oct (est.) | Substitute for Shell |
| AbbVie | Strong | Watching | 72 | none | 30 Oct | Steady name (cap 20%); first candidate for the Palantir slot and for weight taken from an oil major |
| Humana | Strong | Ready | 66 | none (fell 4.4% on 16 Oct) | 6 Nov | 5% (cap) if a holding weakens |
| UnitedHealth | Strong | Ready | 63 | EMAs mixed | Jan 2027 (est.) | Up to 10% if a holding weakens |
| Merck | Strong | Watching | 60 | faded gap | 29 Oct | Hold above its 50-day |
| Amgen | Middling | Watching | 59 | none | 3 Nov, after US close | Score 60+; steady name (cap 20%) |
| Meta Platforms | Middling | Results ahead | 56 | none | 21 Oct, after US close | Drift tests on 22 Oct's session; not held through the report |
| Procter & Gamble | Weak | Results ahead | 64 | downtrend | 22 Oct (est.) | Not while in a downtrend |
| Marvell | Weak | Watching | 42 | below 50-day | 1 Dec | Rotate-out candidate |
| CrowdStrike | Weak | Watching | 39 | below 50-day; heavy-volume down day | 1 Dec | Rotate-out candidate |
| Coinbase (crypto tracker) | Weak | Watching | 34 | downtrend | 29 Oct, after US close | Kept whatever it scores |
| Strategy (crypto tracker) | Weak | Watching | 33 | downtrend | 29 Oct (est.) | Kept whatever it scores |
| TSMC | Weak | Watching | 33 | below 50-day | Jan 2027 | Sold 16 Oct: keep until Fri 23 Oct (standstill test), then remove |
| Constellation Energy | Weak | Watching | 19 | downtrend | early Nov (est.) | Remove at the next evening run |

ROTATE OUT candidates for Sunday: Marvell, CrowdStrike, Constellation Energy (TSMC from 23 Oct). The list is 17 names; Sunday's intake should add five to ten (the broad scan first, if the repository can be reached).

## 5. Trade log

| Date entered | Effective (open of) | Order / change | Reason |
|---|---|---|---|
| Thu 8 Oct, about 23:55 | Fri 9 Oct | Account created with the game's "choose for me" button: Mobimo Holding 20, PACCAR 20, Monolithic Power Systems 20, Sunrise Communications 20, Monks Investment Trust 20 | Not a decision. Needed only to open the account |
| Fri 9 Oct, about 00:00 | Fri 9 Oct | First chosen order: Exxon Mobil 15, Chevron 15, Shell 10, RTX 10, Lockheed Martin 5, TSMC 10, Nvidia 10; cash 25 | Energy and defence led on 8 Oct; AI as a counterweight |
| Sun 11 Oct (entered, confirmed 12 Oct) | Mon 12 Oct | Sell RTX and Lockheed; add Microsoft 15, Coca-Cola 15, Palantir 5, Goldman Sachs 5; cash 25 to 0 | Trend filter; fully invested at Tim's request |
| Mon 12 Oct, 18:21 UK (confirmed) | Tue 13 Oct | Sell Nvidia 10; Shell 10 to 15; Coca-Cola 15 to 20 | Nvidia faded from its open four sessions running |
| Tue 13 Oct, 21:52 UK (confirmed 22:29 UK) | Wed 14 Oct | Sell Goldman Sachs 5; add Meta Platforms 5 | Goldman faded after its beat; Meta passed the momentum test |
| Wed 14 Oct, about 21:44 UK (entered, confirmed by Tim 15 Oct 22:00 UK) | Thu 15 Oct | Sell Meta 5; Microsoft 15 to 10; add Eli Lilly 10 | Meta's momentum exit; tech trimmed after the hot CPI; Lilly score 77, small range |
| Thu 15 Oct, about 21:51 UK (correction message; entered, confirmed by Tim 22:00 UK) | Fri 16 Oct | Sell TSMC 10; Microsoft 10 to 15; Eli Lilly 10 to 15 | TSMC score 43 after results; the two top scores with small ranges back to their caps |

## 6. Review log (newest first, keep the latest 15)

- Sun 18 Oct 2026 (about 00:30): Hand-run session with Tim, after an outside audit by ChatGPT (17 Oct) that Claude checked against the live files, the scheduled tasks and the code. Tim approved fourteen changes. Playbook version 6.4 and pipeline version 7 (standstill test, drift from the next open, results total, reconciliation, judgement test), tested against the live files. Morning check moved to 06:36 UK and the cut-off treated as 07:00 UK until the FT confirms it; a one-point Exxon and Chevron test on Mon 26 Oct to settle it; a draft question to FT help in Tim's Gmail drafts. One-off GitHub access test scheduled for 10:07 UK on 18 Oct. Broad scan: slots moved to 20:20 and 21:20 UTC and unmeasurable stocks now logged. Tim's 16 Oct FT figures recorded for Sunday (101,402, rank 3,269 of 13,918; 35 credits below the estimate). Repository mirror refreshed by hand. Page: the Order panel's cut-off set to 07:00 UK. Updated `ft-game-playbook` skill offered to Tim. No order or data file changed.
- Sat 17 Oct 2026 (about 20:25): Weekend news check (H7). No A item. Two B items: the IRGC says two supertankers hit mines (Fri evening and Sat) and calls Hormuz closed (fits "Oil spike on escalation", +1.4 points, partial carry likely); Trump's Fri 16 Oct order waiving the Graham Act Russia sanctions, with a Russian diesel licence (about -0.45 points on energy if it bites, likely to fade). Weekend Wall Street -0.13%, Bitcoin $81,429 (-0.06% since Friday's close). Script hash matched; two alerts added and ledger.json published. Order unchanged.
- Sat 17 Oct 2026 (about 09:50): Weekly review. Fri 16 Oct logged: +0.64%, estimate 101,437 (+1.44% against -1.67% for the S&P 500); week +1.51% against -1.97%. Panel topped up: 13 members loaded with two years (Wells Fargo, Citigroup, Western Digital, Newmont, McKesson, Corning, Adobe, Quanta, Constellation, Synopsys, PNC, Vertiv, Valero's second year), 14 brought up to 15 Oct; Marsh & McLennan has only 190 sessions and HPE was left out; history verdict still no evidence (+0.042, t +1.1). Eight leavers' shadow ratings settled. Market data key worked. stockanalysis.com served 16 Sep copies of the Microsoft and Eli Lilly pages once (rejected; fresh copies on the second ask); no page refused. GitHub mirror and broad scan not available (no repository tool in this run). Order unchanged; Palantir exit signal for Sunday.
- Fri 16 Oct 2026 (about 09:10): Hand-run session with Tim. Broad scan built (roadmap item 43, playbook 6.3): a GitHub Actions job scans 868 US and London stocks after each US close and writes Leaders and Events lists to the repository's `scan/` folder; the evening review reads them first for reporters and intake (data doc G7), and the weekly review quotes their five-session record. No scheduled task, pipeline script or data file was changed.
- Fri 16 Oct 2026 (about 01:30, later): Hand-run session with Tim, after an outside review by ChatGPT. Playbook version 6.2: the day call is a research record only and never moves cash; "overbought" is a warning, not a 5% cap ("extended" still caps at 5%). Roadmap phase 6 (items 38 to 43). Open: whether the FT's 08:00 cut-off means BST after 25 Oct.
- Fri 16 Oct 2026 (about 01:30): Hand-run session with Tim. Private GitHub repository `timzwang/ft-game` set up as a shared mirror; playbook version 6.1 (G6 and part J).
- Thu 15 Oct 2026 (22:20): Hand-run session with Tim. Playbook version 6 published: split docs; pipeline version 6 (panel test, drift scan, `panel` command); the panel file in `store/panel`. First panel result: no evidence (+0.028, t +0.5, 48 dates).
- Thu 15 Oct 2026 (22:00): Tim confirmed he entered the Wed 14 Oct order and the corrected Fri 16 Oct order in full.
- Thu 15 Oct 2026 (21:55): Evening review, a change evening. TSMC out; Microsoft and Eli Lilly to 15%. Rebuilt on the 14 Oct run's files and sent a correction to a first message that had used the 13 Oct base.
- Wed 14 Oct 2026 (about 21:44): Evening review, a change evening for Thu 15 Oct (Meta out, Microsoft 15 to 10, Eli Lilly 10). Files uploaded but not registered; this doc not written (usage limit). Reconstructed on 15 Oct.
- Tue 13 Oct 2026 (22:35): Tim confirmed the Wed 14 Oct order is entered. Sent rank 1,683 ("Deerino", +2.15%) as the nearest portfolio to the top 2% line.
- Tue 13 Oct 2026 (22:30): Tim sent FT screenshots at 20:59 UK: 100,931, rank 3,579 of 13,436.
- Tue 13 Oct 2026 (22:00): Evening review, a change evening: Goldman Sachs out, Meta in at 5% for Wed 14 Oct. stockanalysis.com refused 11 pages.
- Mon 12 Oct 2026 (21:50): Evening review, a quiet evening. The session refused to run the pipeline script.
- Mon 12 Oct 2026 (21:20): Tim sent FT screenshots: 100,414, rank 4,178 of 13,212.

## 7. Market regime notes

Label: Mixed (hot inflation and an AI and chip sell-off, offset by falling yields and rotation into staples, health care and energy).

Fri 16 Oct:
- SPY 763.25 (-1.11%), 1.0% below its 20-day average; down 1.97% on the week. Chips and AI sold again (Marvell -5.6%, CrowdStrike -7.0%, Palantir -7.2%, Meta -3.7%, Microsoft -1.9%); Coca-Cola, Visa and Mastercard at records (Barron's headline on the KO quote page).
- Coca-Cola +2.1% to a record: KFC switched its drinks deal from PepsiCo; Barclays target $98 from $93.
- Exxon +2.5% to a 52-week high after preliminary Q3 figures (an 8-K) and reports of a large Iran-war profit boost; Chevron +2.6%; Morgan Stanley Chevron target $226.
- Data: industrial production +0.7% (0.4% forecast), capacity use 76.9%; import prices +1.1% (0.8%); NY Fed services -20.7. 10-year -1bp.
- Oil: Brent $109.86 (+3.7%), above $110 intraday, +5.2% on the week; Hormuz flows cut to about 11.6m barrels a day (tradingeconomics); US crude stocks -8.6m barrels.
- Strategy -9.6% on MSCI exclusion reports; Coinbase -5.8%; Bitcoin -1.0%.

Thu 15 Oct and earlier in the week:
- Thu 15 Oct: PPI +1.3% on the month (6.3% a year), retail sales +0.8%, yet the 10-year fell to 5.10%; S&P 500 +0.33%; Anthropic's slower growth; KOSPI -8% on memory chips; TSMC beat with lower margins.
- Wed 14 Oct: CPI 3.7% a year, core 2.6%; S&P 500 -1.08%. October hike odds about even.
- UK: gilt 5.38%, a three-week low on 15 Oct; FTSE 100 10,840 on 15 Oct.

Weekend log (weekend of 17 and 18 Oct; Saturday check at 20:20 UK):
- No A item.
- B: Hormuz escalation. The IRGC says a supertanker with over 2m barrels hit a mine on Fri evening and a second on Sat (Tasnim, 16:33 Tehran time; Al Jazeera, 17 Oct), and that the strait is closed to all vessels (Gulf News live, 14:20). A tanker was hit by an RPG from a small boat 78nm north-east of Jubail on Sat. CENTCOM says about 400 ships transited last week and that mines have been cleared; no talks breakthrough expected; Trump has reportedly told the military to be ready for larger strikes after 3 Nov. Fits "Oil spike on escalation" (+1.4 points); attacks were already at a record and Brent at $110 on Friday, so a partial carry at most. Supports the energy holdings (45%); argues against the ceasefire scenario (-2.02) in the near term.
- B: Russia. Trump signed an order on Fri 16 Oct (reported Sat) waiving the Graham Act sanctions and tariffs on Russian energy, plus a Treasury licence to April for Russian diesel imports (ABC News, 17 Oct). Bearish at the margin for diesel and refining margins: energy 45% x about -1% is roughly -0.45 points if it bites; likely to fade behind the Hormuz news. Most relevant to the refiners on the watchlist (Phillips 66, Valero, Marathon) and Exxon's refining lift.
- C: Saudi-led coalition intercepts of a missile aimed at Yanbu, cruise missiles and drones over Riyadh and the Eastern region (Gulf News live, 01:13 and 18:23). Continuation of the pattern.
- C: no weekend company news found on the holdings; Palantir's exit signal stands for Sunday's review.
- Prices: IG Weekend Wall Street 51,884 to 51,939, -0.13% (noise); Bitcoin $81,429 at 20:22 UK, -0.06% since Friday's US close. No crypto-linked holding.
Earlier weekend (10 and 11 Oct): no A item; B items on Riyadh's airport attacks, Iran's reply on Hormuz, tanker strikes and Hurricane Isaias.

Near calendar (the full calendar to 27 Nov is on the page and in the ledger):
- Sun 18 Oct: evening review writes Monday's order (Palantir exit signal; the oil-pair view above).
- Mon 19 Oct: NAHB housing index (31 forecast).
- Tue 20 Oct: RTX results (watchlist only); housing starts.
- Wed 21 Oct: Meta results after the US close (watchlist); EIA oil stocks; 20-year bond auction.
- Thu 22 Oct: Valero, Procter & Gamble, Lockheed Martin; jobless claims.
- Fri 23 Oct: flash PMIs; Michigan sentiment final.
- Sun 25 Oct: UK clocks go back; the US session is 13:30 to 20:00 UK in the week of 26 Oct. The evening review sets the order for Coca-Cola's results.
- Mon 26 Oct: cut-off test at about 07:15 UK (part C).
- Tue 27 Oct: Coca-Cola. Wed 28 Oct: Fed decision 18:00 UK; Microsoft; Phillips 66. Thu 29 Oct: Shell; Eli Lilly; Merck; Coinbase. Fri 30 Oct: Exxon Mobil, Chevron, AbbVie. Tue 3 Nov: US midterms; Amgen.

## 8. Open questions for Tim

Answered: an order entered before 08:00 UK counted for that day up to 23 Oct (from 17 Oct treat 07:00 UK as the cut-off, part C); the midday check stays off; the leaderboard shows only the top 10, though Tim can open other players' portfolios; Shell filled at its 08:00 open on 9 Oct; Microsoft, Coca-Cola, Palantir, Goldman Sachs, Meta Platforms and Eli Lilly are in the game's list; the orders for Tue 13 Oct to Fri 16 Oct were entered; value, rank and players after Fri 16 Oct's close (101,402, 3,269 of 13,918, sent 17 Oct); the Marsh & McLennan panel swap (agreed 17 Oct: next position down, for the weekly review of 24 Oct).

Still open:
1. Are Strategy and Coinbase in the game's list? Not needed until one is close to being bought.
2. The value of a player nearer rank 278 (the top 2% line), if Tim comes across one.
3. The cut-off after the clock change: 07:00 or 08:00 UK. A question to FT help is in Tim's Gmail drafts (for him to check the address and send), and the one-point Exxon and Chevron test at about 07:15 UK on Mon 26 Oct settles it: Tim reports which day it filled. Until then 07:00 UK.
4. GitHub access from scheduled runs: the 17 Oct weekly run had no repository tool, so the mirror and the broad scan's record were skipped. A one-off test runs at 10:07 UK on Sun 18 Oct; the result decides whether G6 and G7 stay in the scheduled runs or become hand-run only.
5. Does the game convert US stocks' returns into pounds? If it does, the estimate would drift from the FT figure with the dollar; so far the closing gap has stayed under 0.05%. In the same draft to FT help.

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
- Sequel: no new high after 12 Oct (212.94); on Fri 16 Oct it opened at 201.79 and closed at 186.03 on 33.2m shares, the first heavy-volume close below its open, so the exit falls at Mon 19 Oct's open (the five-session test was due the same day). Held at 5% it cost -0.56 points over the game. Lesson: a high-range stock (daily range about 4%) at 5% can still cost half a point in a week; the 5% cap limits, but does not remove, the damage.

**RTX and Lockheed Martin, 8 Oct (a one-day bounce inside a downtrend)**

- Lesson: a strong day says nothing about the trend. Check the 50-day and 200-day averages before buying on a headline.

**Humana, 9 and 12 Oct (large gaps that faded, even with upgrades)**

- Lesson: the bigger the gap, the more of the news is already in the fill price.

**Goldman Sachs, 13 Oct (a results beat inside a downtrend)**

- Lesson: a big beat does not lift a stock in a downtrend. A results position needs the trend filter too.

**Meta Platforms, 12 to 15 Oct (follow-through entry, then a quick exit)**

- Bought for 14 Oct at 5%; on 14 Oct it closed 3.0% below its open, giving back all of 13 Oct's gain. Sold at the 15 Oct open (726.56). It closed at 709.33 on 16 Oct, so the exit saved about a further 0.12 points.
- Lesson: a momentum entry after a two-day run can reverse at once. The give-back rule cut the cost.

**TSMC, 15 Oct (held through results in a sector sell-off)**

- Fell 3.4% on 14 Oct ahead of the report; after a beat with lower margins it gapped down 3.4% on 15 Oct, then closed 1.7% above its open. Sold at the 16 Oct open (421.22); it closed at 412.61.
- Lesson: when the score has slipped below 50 before a report, cut the hold to 5% or exit, whatever the implied move. Total cost over the game -0.96 points.

**Judging changes: one day against several (17 Oct)**

- The 13 and 14 Oct changes each looked worse than standing still on their fill day (-0.17 and -0.14 points), but over the week the four changes added about +0.86 points, because Nvidia (-6% after the sale) and TSMC kept falling.
- Lesson: judge a change over the five sessions it was meant for (the STANDSTILL block), not its first day.

## 11. Confidence ratings, shadow ratings, the panel test and the day call

- Confidence ratings (not calibrated): 7 of 13 resolved. Below 55: 0 of 1 beat the index; 55 to 59: 4 of 5; 60 and above: 1 of 1. Far too few to judge. Ratings of 15 Oct for the order in force: Exxon 62, Microsoft 62, Eli Lilly 62, Chevron 61, Shell 60, Coca-Cola 57, Palantir 57.
- Shadow ratings: 40 of 133 settled. Live: score 70 and above, 11 cases, 82% beat the index (+3.00 points); 60 to 69, 14 cases, 43% (-4.41); 45 to 59, 8 cases, 25% (-4.16); below 45, 7 cases, 71% (+1.34). Weak evidence until about 150 have settled. From 18 Oct each rating also stores its 60 price and session points and its 40 judgement points, for the judgement test (part E).
- Panel test: see section 1. The main evidence on the score. Old backtest (hindsight) correlation -0.12.
- Drift record: no reporters scanned yet (the first scan falls to Sunday's evening review, as there was no Friday evening run). From pipeline version 7 drift results run from the next session's open.
- Day call record (S&P 500): 1 right of 4, the same as always saying green; Brier 0.266. Portfolio: 3 of 4, the same as always green; Brier 0.205.

## 12. Tools

- Tim's page: https://claude.ai/artifact/8P8UwQsb4QsbZMsKNYKrUJ, pinned in his Claude sidebar, with tabs Today, Macro, Performance, Risk, Calendar and Log. It reads four data files (`stocks`, `ledger`, `history`, `macro`) and a fifth dataset, `logos`, that no run touches. The Order panel reads the latest alert whose `stock` is "Order"; its "Enter before" bar uses a 07:00 UK cut-off from 18 Oct (one constant in the page, `CUTOFF`; page notes). Notes for anyone changing the page are in `claude/ft-game-page.md`.
- Playbook docs (version 6.4): `claude/ft-game-playbook.md` (core, with the routing table), `claude/ft-game-rules.md`, `claude/ft-game-data.md`, and the run docs `claude/ft-game-run-evening.md`, `-morning`, `-refresh`, `-weekly`, `-weekend`.
- Panel file: `panel.json` on the same artifact, named by the document `store/panel` (outside `datasets`, so the page never loads it). The evening and weekly runs read and publish it (G1, G5).
- Scripts: the pipeline (version 7 from 17 Oct) and the screening script are assets on that artifact. Their ids and hashes are in part B of the playbook, which is the only place they are kept. Version 6 is kept on the artifact, not in use.
- Leftover assets: the four files the 14 Oct run uploaded (stocks 272fe63f..., ledger e4b81f05..., history 448fb462..., macro e67fb2ac...) are superseded but kept.
- Check before trusting the base: if the latest assets are newer than the dataset documents' `updated` time, an earlier run uploaded but did not finish publishing. Read its stocks file and its `alert` rows for an Order change before deciding what order is in force.
- Fetching assets: read each asset with a single `path`.
- Rate limits: on 17 Oct stockanalysis.com refused nothing in groups of four with 60-second pauses; it twice served a copy a month old (Microsoft and Eli Lilly, dated 16 Sep), caught by the status text. The Treasury CSV first served a copy without 16 Oct's row; a throwaway suffix fetched the current one.
- Market data service: massive.com, free plan, on an account opened by Tim's father. The key is in the evening and weekly review tasks and is never written into this project's docs, the page data, alerts or messages. Its data runs to the previous session. Long replies get transcribed wrongly: on 17 Oct a 250-value half for Synopsys dropped three values inside the list and padded the end (caught by checking elements 100, 200 and 250 by index), and HPE's check disagreed. Ask in halves of 125 and check three elements by index before passing a list to `closes`. `closes` needs the count to match SPY's stored sessions.
- No earnings calendar with actual figures was readable on 15 Oct; the drift scan finds reporters by search (part F).
- A free price feed found on 11 Oct, not yet used: Cboe's delayed quotes (`https://cdn-api.cboe.com/api/global/delayed_quotes/quotes/<TICKER>.json`).
- Coin prices: Coinbase's public candle and ticker pages.
- Sources that did not work: CNN article pages (robots), the US News CPI article, CNBC's oil page (fetch errors on 15 Oct).
- GitHub mirror: private repository `timzwang/ft-game` (playbook part B and G6). The 17 Oct weekly run could not reach it: `git clone` asked for credentials and the session had no repository tool; the mirror was skipped. Refreshed by hand on 18 Oct (data to the Fri 16 Oct close, docs 6.4, pipeline 7). The broad scan's slots are 20:20 and 21:20 UTC from 17 Oct.
- Two saved skills, `ft-game-playbook` and `stock-score`, load in scheduled runs. An updated `ft-game-playbook` skill (playbook 6.4 times and rules) was offered to Tim on 18 Oct; until he saves it the old one shows 07:26 and 08:00, but it sends every run to the project docs, which win.
