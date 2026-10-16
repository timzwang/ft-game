# FT Stock Picking Game: state and log

Last updated: Fri 16 Oct 2026, about 09:10 UK (hand-run session with Tim: the broad scan built and tested, playbook version 6.3; nothing about the portfolio changed. Before that, about 01:30 UK: after an outside review by ChatGPT, playbook version 6.2 published (the day call no longer moves cash; "overbought" is a warning, not a cap) and roadmap phase 6 added (counterfactual portfolios, a top-five panel test, a test of the judgement points, weights fixed for the game, a broad scanner on GitHub); earlier the same session the GitHub mirror was set up and playbook 6.1 published; nothing about the portfolio changed. Before that, Thu 15 Oct 22:20 UK: playbook version 6 published, with the split docs, the panel test and the earnings-drift scan. Earlier: 22:00 Tim confirmed he entered the Wed 14 Oct order and the corrected Fri 16 Oct order; 21:55 evening review, a change evening: TSMC out; Microsoft and Eli Lilly each 10 to 15 for Fri 16 Oct)

This doc is the narrative record for Tim's entry, "Seeking Beta". The procedure for every run is in `claude/ft-game-playbook.md` (the core doc) and the docs its routing table names. The numbers (prices, scores, daily performance, contributions, ratings and their outcomes, the full calendar, analyst changes, alerts, the panel test, the drift record) live in the data files behind Tim's page and the panel file, and are produced by the pipeline script; this doc carries the decisions and the reasons.

Messages: from 10 Oct Tim is sent a message only when there is something for him to enter or answer (playbook part I, "When Tim is told"). Quiet runs update the page and this doc and send nothing.

Scheduled runs: evening review 21:30 UK Sun to Thu; morning check 07:26 UK Mon to Fri; price refresh 16:45 UK and late price refresh 19:22 UK Mon to Fri; results-day refresh 14:50 UK Mon to Fri (acts only on results days); weekly performance review Sat 09:12 UK; weekend news check Sat and Sun 20:20 UK; midday check 12:40 UK Mon to Fri (switched off, see section 8).

## 1. Status

- **Playbook version 6.3 from Fri 16 Oct's runs** (6.3: the broad scan, G7; 6.2: the day call never moves cash, "overbought" is a warning only). The playbook is split (core doc plus rules, data and one doc per run), and two features are added: the panel test of the score and the earnings-drift scan (part E). Pipeline script version 6 (part B). The evening review now also scans the day's reporters and runs with `--panel`.
- **Panel test (first result, 15 Oct):** 15 of the 30 panel stocks loaded; over 48 non-overlapping five-session windows the price-only points show no evidence of ranking stocks: average rank correlation +0.028 (t +0.5), positive on 56% of dates; the 36 to 48 point band beat the index 49% of the time. One-year and two-month strength lean positive (t +1.3, +1.5), the five-day part leans negative (t -0.7). Saturday's weekly review loads the other 15 (Wells Fargo, Citigroup, Western Digital, Newmont, McKesson, Corning, Adobe, Quanta Services, Constellation Energy, Synopsys, PNC, Marsh & McLennan, Vertiv, Hewlett Packard Enterprise, and Valero's second year).
- **Wed 14 Oct evening review: partly lost.** It issued a change order for Thu 15 Oct (alert at 21:44 UK: Meta Platforms out, Microsoft 15 to 10, Eli Lilly in at 10; watchlist added Eli Lilly, Merck, AbbVie, Procter & Gamble, Constellation Energy and removed Goldman Sachs, ASML, Lumentum, Nvidia). It uploaded its four data files but never pointed the page at them and never wrote this doc. Tonight's run found those files and built tonight's files on them. **Tim confirmed at 22:00 UK on 15 Oct that he entered the 14 Oct order**, so the log is right and Eli Lilly is in the game's list.
- Estimated value at Thu 15 Oct close: 100,790, +0.79% since the start, against -0.57% for the S&P 500 fund. Wed 14 Oct +0.09% (Coca-Cola +0.37 points, Chevron +0.30; TSMC -0.34, Microsoft -0.27); Thu 15 Oct -0.38% (Eli Lilly +0.13, Microsoft +0.10; Exxon -0.20, Chevron -0.18, TSMC -0.18).
- Last FT figures: 13 Oct 20:59 UK, 100,931, rank 3,579 of 13,436 (stored). Top 2% line is rank 268, estimated +4% to +4.5%.
- Order for Fri 16 Oct (correction message sent about 21:51 UK; entered, confirmed by Tim at 22:00 UK): Coca-Cola 20, Exxon Mobil 15, Chevron 15, Shell 15, Microsoft 15, Eli Lilly 15, Palantir 5, cash 0. TSMC sold.
- Day call for Fri 16 Oct: S&P 500 green 56% (usual 55%, close to a coin flip); portfolio green 61% (usual 60%). No adjustment. Backdrop label: tailwind (10-year down 17bp in five sessions). The 15 Oct call (S&P 500 red 49%) was wrong (S&P +0.28%); record 1 right of 3.
- Macro at Thu 15 Oct close: US 2-year 4.77%, 10-year 5.10% (-9bp on the day by the Treasury), 30-year 5.43%. Gilt 5.37%, German 3.41%, French 4.79%, Italian 4.49%, Japanese 2.93%. Brent $105.73, WTI $97.59 (+2.6%, 8.6m barrel stock draw), gold $4,170. Note: the stored 14 Oct US yields are 13 Oct's carried forward (the 14 Oct run had no Treasury row), so the stored one-day changes for 15 Oct are against 13 Oct.
- Crypto: Bitcoin $82,299 at the US close, trend up (IBIT 1.8% below its 20-day, 6.1% above its 50-day). Ether, Solana and XRP down 9% to 12% over five sessions while Bitcoin held: risk appetite thinning at the edges. No holding is crypto-linked.
- Regime: mixed. Wed 14 Oct: hot CPI (3.7% a year, core 2.6%), S&P 500 -1.08%, its first 1% fall in 53 sessions; Anthropic's slower growth hit AI stocks. Thu 15 Oct: PPI +1.3% on the month (6.3% a year), retail sales +0.8%, yet the 10-year fell 9bp; S&P 500 7,744 (+0.33%), Dow +1.1%, Russell 2000 +1.4%, Nasdaq +0.1%, about 343 of 465 S&P stocks up; health care +1.9%, energy -1.6%, tech -0.7%. Korea's KOSPI -8% on memory chips. October hike odds roughly even. What would make it risk-off: the 10-year back above 5.25% with the S&P 500 below its 20-day, or a hike priced above 70%.

## 2. Current portfolio

The order for Fri 16 Oct's open (entered). Scores and bands from the pipeline at the Thu 15 Oct close.

| Stock | Weight | Cap | Confidence | Score | Band | Flags | Next results | Substitute if missing |
|---|---|---|---|---|---|---|---|---|
| Coca-Cola | 20% | 20% | 57 | 74 | Strong | faded gap | 27 Oct | PepsiCo (downtrend: cash instead) |
| Exxon Mobil | 15% | 15% | 62 | 76 | Strong | none | 30 Oct | ConocoPhillips |
| Chevron | 15% | 15% | 61 | 73 | Strong | none | 30 Oct | ConocoPhillips |
| Shell | 15% | 15% | 60 | 73 | Strong | overbought; heavy-volume down day; at 52-week high | 29 Oct | BP |
| Microsoft | 15% | 15% | 62 | 80 | Strong | none | 28 Oct | Alphabet (not scored) |
| Eli Lilly | 15% | 15% | 62 | 80 | Strong | none | 29 Oct | AbbVie |
| Palantir (momentum position) | 5% | 10% | 57 | 71 | Strong | none | 2 Nov (est.) | leave in cash |
| TSMC | 0% (sold for Fri 16 Oct) | 10% | exit 60 | 43 | Weak | below 50-day; heavy-volume down day | done 15 Oct | n/a |
| Cash | 0% | | | | | | | |

Points for the coming reviews:

- Themes: Energy 45% (at the guardrail), Consumer staples 20%, Software 20%, Health care 15%. Risk shares: Exxon 22%, Chevron 22%, Coca-Cola 19%, Shell 19%. Worst scenario: ceasefire or Hormuz reopening -2.02%.
- Palantir: no new high since 12 Oct (212.94). Exit after about five sessions without one (around Mon 19 Oct) or on a heavy-volume close below its open.
- Results inside ten sessions: Coca-Cola 27 Oct, Microsoft 28 Oct, Shell and Eli Lilly 29 Oct, Exxon and Chevron 30 Oct. Implied moves are needed from about 20 Oct for the hold, trim or exit calls (budget 0.6 points each). After each report the drift tests apply to the holding too (part E).
- Meta post-mortem logged. TSMC's post-mortem goes in with the next run: thesis "AI chip leader held through results at 10% inside the 0.6 point budget"; lesson "Holding through results in a sector sell-off cost about 0.5 points over two sessions; the score had slipped below 50 before the report and the hold should have been cut to 5%."
- Confidence ratings: the panel test has so far found no edge in the price part of the score, so keep ratings close to 50 to 60 and do not raise one because a score is high (part E).

## 3. Pending order

Order for Fri 16 Oct's open, issued by the 21:30 evening review on Thu 15 Oct.

- A first message at 21:46 UK used a base that ignored the 14 Oct order. A correction message at about 21:51 UK replaced it.
- **Entered: Tim confirmed at 22:00 UK that the corrected order is fully in.** No log correction needed.

Coca-Cola 20, Exxon Mobil 15, Chevron 15, Shell 15, Microsoft 15, Eli Lilly 15, Palantir 5, cash 0. Sold: TSMC (was 10). Raised: Microsoft 10 to 15, Eli Lilly 10 to 15.

Order in force on Thu 15 Oct (from the 14 Oct message, entered, confirmed by Tim): Coca-Cola 20, Exxon 15, Chevron 15, Shell 15, Microsoft 10, Eli Lilly 10, TSMC 10, Palantir 5.

## 4. Watchlist

Scores and bands at the Thu 15 Oct close.

| Name | Band | Status | Score | Flags | Next results | Promote if |
|---|---|---|---|---|---|---|
| Humana | Strong | Ready | 83 | none (15 Oct row missing: page refused) | 6 Nov | 5% (cap) if a holding weakens |
| UnitedHealth | Strong | Ready | 69 | EMAs mixed | Jan 2027 (est.) | Up to 10% if a holding weakens |
| Marathon Petroleum | Strong | Watching | 75 | extended | 3 Nov | 5% at most while extended; energy at 45% |
| Phillips 66 | Strong | Watching | 75 | none | 28 Oct | Only in place of an oil major (three target raises 12 to 14 Oct) |
| Valero Energy | Strong | Results ahead | 69 | extended | 22 Oct (est.) | Not before results; drift tests after |
| Meta Platforms | Strong | Results ahead | 67 | none | 21 Oct, after US close | Drift tests on 22 Oct's session; not held through the report |
| AbbVie | Strong | Watching | 66 | faded gap; at 52-week high | late Oct (est.) | A close above its open; steady name (cap 20%) |
| BP | Strong | Watching | 63 | none | 30 Oct (est.) | Substitute for Shell |
| Amgen (new) | Strong | Watching | 61 | faded gap | 3 Nov | Close above its open, score 60+; target cuts weigh; steady name (cap 20%) |
| CrowdStrike | Strong | Needs follow-through | 60 | none | 1 Dec | A close above its open in the upper half of its range |
| Merck | Strong | Watching | 60 | faded gap | late Oct (est.) | Hold above its 50-day |
| Marvell | Middling | Watching | 57 | none | none dated | Score 60+ |
| Procter & Gamble | Weak | Results ahead | 64 | downtrend (15 Oct row missing) | 22 Oct | Not while in a downtrend |
| Coinbase (crypto tracker) | Weak | Watching | 62 | downtrend | 29 Oct, after US close | Kept whatever it scores |
| Strategy (crypto tracker) | Weak | Watching | 53 | downtrend | 29 Oct (est.) | Kept whatever it scores |
| TSMC | Weak | Watching | 43 | below 50-day | Jan 2027 | Kept one night to collect its 16 Oct sale price; remove at the next run |
| Constellation Energy | Weak | Watching | 25 | downtrend (15 Oct row missing) | early Nov (est.) | Rotate out once listed three sessions (added 14 Oct) |

Tonight: Amgen added. Walmart, ServiceNow and GE Vernova were candidates, but their quote pages were refused, so they were left out. No FTSE 100 names screened (rate limits). Steady names on the list: AbbVie, Amgen. From 16 Oct the intake draws first on the drift scan's "enter" and "watch" verdicts.

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

- Fri 16 Oct 2026 (about 09:10): Hand-run session with Tim. Broad scan built (roadmap item 43, playbook 6.3): a GitHub Actions job scans 868 US and London stocks after each US close and writes Leaders and Events lists to the repository's `scan/` folder; the evening review reads them first for reporters and intake (data doc G7), and the weekly review quotes their five-session record. Tested on synthetic prices and in eight live runs; US closes matched the stored ones. Yahoo's London stock data was missing 15 Oct that morning, so London is first tested in Friday evening's run. No scheduled task, pipeline script or data file was changed.
- Fri 16 Oct 2026 (about 01:30, later): Hand-run session with Tim, after an outside review of the system by ChatGPT. Playbook version 6.2: the day call is a research record only and never moves cash; "overbought" is a warning, not a 5% cap ("extended" still caps at 5%). Roadmap phase 6 (items 38 to 43): counterfactual portfolios, a top-five panel test and a test of the judgement points for pipeline version 7; score weights fixed for the game unless Saturday's verdict is decisive; a broad scanner of about 900 US and London stocks designed to run on GitHub, Tim agreed that runs may read `scan/` from the repository, so it is ready to build. Releases, tags and the repository description cannot be set from Claude's sessions (refused by policy on retry); Tim sets them. Open: whether the FT's 08:00 cut-off means BST after 25 Oct. No scheduled task, script or data file was changed.
- Fri 16 Oct 2026 (about 01:30): Hand-run session with Tim. Private GitHub repository `timzwang/ft-game` set up as a shared mirror for Claude and ChatGPT and tested end to end (push from a chat, push from a scheduled cloud session, ChatGPT pull request merged by Tim); first full export pushed. Playbook version 6.1: G6 (mirror data and this doc to GitHub, last step of the evening and weekly runs, best effort) and part J (this doc always written from a local file). No scheduled task was changed.
- Thu 15 Oct 2026 (22:20): Hand-run session with Tim. Playbook version 6 published after the evening review finished: the playbook split into a core doc, a rules doc, a data doc and five run docs; pipeline version 6 (panel test, drift scan, `panel` command); the panel file (30 stocks fixed by rank, 15 loaded) in `store/panel`. First panel result: no evidence the price points rank stocks (+0.028, t +0.5, 48 dates).
- Thu 15 Oct 2026 (22:00): Tim confirmed he entered the Wed 14 Oct order (Eli Lilly is in the game's list) and the corrected Fri 16 Oct order in full.
- Thu 15 Oct 2026 (21:55): Evening review, a change evening. TSMC out; Microsoft and Eli Lilly to 15%. Found that the 14 Oct evening run had issued an order (Lilly in, Meta out, Microsoft 10) and uploaded files but never published them or wrote this doc; rebuilt on its files and sent a correction to a first message that had used the 13 Oct base. Pipeline hash matched. Refused pages (429): Humana, Walmart, ServiceNow and GE Vernova quote pages. Market data key worked (Amgen, Eli Lilly years). Watchlist: Amgen in.
- Wed 14 Oct 2026 (about 21:44): Evening review, a change evening for Thu 15 Oct (Meta out, Microsoft 15 to 10, Eli Lilly 10). Its files were uploaded but not registered, and this doc was not written; the run hit the account's usage limit. Reconstructed on 15 Oct.
- Tue 13 Oct 2026 (22:35): Tim confirmed the Wed 14 Oct order is entered. Sent rank 1,683 ("Deerino", +2.15%) as the nearest portfolio to the top 2% line.
- Tue 13 Oct 2026 (22:30): Tim sent FT screenshots at 20:59 UK: 100,931, rank 3,579 of 13,436.
- Tue 13 Oct 2026 (22:00): Evening review, a change evening: Goldman Sachs out, Meta in at 5% for Wed 14 Oct. stockanalysis.com refused 11 pages.
- Mon 12 Oct 2026 (21:50): Evening review, a quiet evening. The session refused to run the pipeline script.
- Mon 12 Oct 2026 (21:20): Tim sent FT screenshots: 100,414, rank 4,178 of 13,212.
- Mon 12 Oct 2026 (18:30): Review run by hand. Order for Tue 13 Oct changed: Nvidia sold, Shell 15, Coca-Cola 20.
- Mon 12 Oct 2026 (13:10): Market data key added to the evening and weekly review tasks at the family's request.
- Sun 11 Oct 2026 (23:10): Market data service wired in (playbook 5.4), with the `closes` command.

## 7. Market regime notes

Label: Mixed (hot inflation and an AI sell-off, offset by falling yields and a broad rotation into health care, staples, financials and small caps).

Thu 15 Oct:
- S&P 500 7,744 (+0.33%), Dow 52,178 (+1.08%), Nasdaq 26,713 (+0.08%), Russell 2000 2,767 (+1.38%); VIX about 16.8 intraday. About seven in ten S&P stocks rose.
- Data: PPI +1.3% on the month, 6.3% a year (forecast 0.5%, 5.3%); core +0.7%, 5.0% a year; retail sales +0.8% (0.3% forecast); claims 199,000. Yields fell anyway: 10-year 5.10%, 2-year 4.77%.
- AI: Anthropic told investors Q3 revenue was $16.8bn, growth slowing to 45% from about 147%. KOSPI -8% (Samsung -9%, SK Hynix -11%), Nikkei -5%. Dell, HPE, Arista, Applied Materials and Lam Research fell 3% to 7%. Software rallied (Intuit, ServiceNow, Autodesk +6%).
- TSMC: Q3 revenue $46.7bn, above its $44.6bn to $45.8bn guidance; gross margin 66.4% (down 130bp); Q4 guide $52.3bn to $54.3bn. Opened 3.4% lower, closed 1.7% above its open.
- Oil and Iran: two ships sunk near Hormuz, including Singapore's GFS Pride; Iran says the strait stays closed without coordination; Gulf tanker rates at records. Brent $105.73, WTI $97.59 after an 8.6m barrel stock draw. Energy shares fell 1.6% despite this: the oil trade may be crowded.
- UK: FTSE 100 +1.1% to 10,840 (low tech exposure); gilt 5.37%, a three-week low; August GDP +0.1%.
- Wed 14 Oct: CPI 3.7% a year (0.6% on the month), core 2.6% (0.3%); gasoline +9.1% on the month. S&P 500 -1.08%. October hike odds about 50%.

Weekend log (weekend of 10 and 11 Oct): no A item; B items on Riyadh's airport attacks, Iran's reply on Hormuz, tanker strikes and Hurricane Isaias.

Near calendar (the full calendar to 27 Nov is on the page and in the ledger):
- Fri 16 Oct: Fed Chair Warsh speaks 04:30 UK; industrial production 14:15 UK (forecast +0.4%); import prices; monthly options expiry.
- Sat 17 Oct: weekly review loads the other 15 panel stocks.
- Mon 19 Oct: Palantir's five-session test for a new high.
- Tue 20 Oct: RTX results (watchlist only).
- Wed 21 Oct: Meta results after the US close (watchlist).
- Thu 22 Oct: Valero, Procter & Gamble, Lockheed Martin.
- Sun 25 Oct: UK clocks go back; the US session is 13:30 to 20:00 UK in the week of 26 Oct.
- Tue 27 Oct: Coca-Cola. Wed 28 Oct: Fed decision 18:00 UK; Microsoft; Phillips 66. Thu 29 Oct: Shell; Eli Lilly; Coinbase. Fri 30 Oct: Exxon Mobil and Chevron. Tue 3 Nov: US midterms; Amgen.

## 8. Open questions for Tim

Answered: an order entered before 08:00 UK counts for that day; the midday check stays off; the leaderboard shows only the top 10, though Tim can open other players' portfolios; Shell filled at its 08:00 open on 9 Oct; Microsoft, Coca-Cola, Palantir, Goldman Sachs, Meta Platforms and Eli Lilly are in the game's list; the orders for Tue 13 Oct, Wed 14 Oct, Thu 15 Oct and Fri 16 Oct (the correction) were entered.

Still open:
1. Portfolio value, rank and number of players after each Friday's close.
2. Are Strategy and Coinbase in the game's list? Not needed until one is close to being bought.
3. The value of a player nearer rank 268 (the top 2% line), if Tim comes across one.
4. Once all 30 panel stocks are loaded: weights change only if the history verdict is "useful" or "the wrong way" (roadmap item 41), and then only with Tim's agreement.
5. Does the game's 08:00 cut-off mean BST after the clock change on 25 Oct? If so it becomes 07:00 UK and the morning check must move earlier.

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

**RTX and Lockheed Martin, 8 Oct (a one-day bounce inside a downtrend)**

- Lesson: a strong day says nothing about the trend. Check the 50-day and 200-day averages before buying on a headline.

**Humana, 9 and 12 Oct (large gaps that faded, even with upgrades)**

- Lesson: the bigger the gap, the more of the news is already in the fill price.

**Goldman Sachs, 13 Oct (a results beat inside a downtrend)**

- Lesson: a big beat does not lift a stock in a downtrend. A results position needs the trend filter too. Run through the drift tests on 15 Oct as a check, it fails four of six (no raise, no reaction, did not hold its open, below its 50-day).

**Meta Platforms, 12 to 15 Oct (follow-through entry, then a quick exit)**

- 12 Oct: open 728.50, close 742.96. 13 Oct: open 735.99, close 762.50, volume 22.6m. Bought for 14 Oct at 5%.
- 14 Oct: opened 760.75 and closed 737.54, 3.0% below its open, giving back more than all of 13 Oct's gain. Goldman cut its target to $762. Sold at the 15 Oct open (726.56).
- Lesson: a momentum entry after a two-day run can reverse at once. The give-back rule cut the cost to about 0.23 points.

**TSMC, 15 Oct (held through results in a sector sell-off)**

- Fell 3.4% on 14 Oct ahead of the report, as Korean memory stocks and Anthropic's slowing growth hit AI shares. After a beat with lower margins it gapped down 3.4% on 15 Oct, then closed 1.7% above its open.
- Lesson: when the score has slipped below 50 before a report, cut the hold to 5% or exit, whatever the implied move.

## 11. Confidence ratings, shadow ratings, the panel test and the day call

- Confidence ratings are logged and resolved in the ledger; the first windows closed on 15 Oct (the weekly review reports the hit rate). Ratings of 15 Oct for the Fri 16 Oct order: Exxon 62, Microsoft 62, Eli Lilly 62, Chevron 61, Shell 60, Coca-Cola 57, Palantir 57; TSMC exit 60.
- Shadow ratings: 109 logged. Live so far: score 70 and above, 5 of 5 beat the index; 60 to 69, 1 of 3. Far too few to judge.
- Panel test (part E): the main evidence on the score from now on. First result on 15 of 30 stocks: no evidence (see section 1). The old backtest on list stocks (picked with hindsight) still shows no positive link and is now labelled as such.
- Drift record: starts with the 16 Oct evening review's scan; settled five sessions after each reaction day.
- Day call record (S&P 500): 1 right of 3. Fri 16 Oct: S&P 500 green 56% (usual 55%), portfolio green 61% (usual 60%).

## 12. Tools

- Tim's page: https://claude.ai/artifact/8P8UwQsb4QsbZMsKNYKrUJ, pinned in his Claude sidebar, with tabs Today, Macro, Performance, Risk, Calendar and Log. It reads four data files (`stocks`, `ledger`, `history`, `macro`) and a fifth dataset, `logos`, that no run touches. The Order panel reads the latest alert whose `stock` is "Order". Notes for anyone changing the page are in `claude/ft-game-page.md`.
- Playbook docs (version 6): `claude/ft-game-playbook.md` (core, with the routing table), `claude/ft-game-rules.md`, `claude/ft-game-data.md`, and the run docs `claude/ft-game-run-evening.md`, `-morning`, `-refresh`, `-weekly`, `-weekend`.
- Panel file: `panel.json` on the same artifact, named by the document `store/panel` (outside `datasets`, so the page never loads it). The evening and weekly runs read and publish it (G1, G5).
- Scripts: the pipeline and the screening script are assets on that artifact. Their ids and hashes are in part B of the playbook, which is the only place they are kept. The pipeline uploaded at 21:13 UK on 15 Oct (154 KB) is version 6 and is now the one in part B; the panel JSON uploaded at the same time is the panel file.
- **Leftover assets:** the four files the 14 Oct run uploaded (stocks 272fe63f..., ledger e4b81f05..., history 448fb462..., macro e67fb2ac...) are superseded but kept.
- **Check before trusting the base:** if the latest assets are newer than the dataset documents' `updated` time, an earlier run uploaded but did not finish publishing. Read its stocks file and its `alert` rows for an Order change before deciding what order is in force. On 15 Oct the first message went out before this was found.
- Fetching assets: read each asset with a single `path`.
- Rate limits: on 15 Oct stockanalysis.com refused 4 of about 45 pages, all quote pages in the later groups. History pages read "At close" by about 21:35 UK and carry two sessions; some still showed a mid-session status, and a quote page with a clock suffix fixed those.
- Market data service: massive.com, free plan, on an account opened by Tim's father. The key is in the evening and weekly review tasks and is never written into this project's docs, the page data, alerts or messages. Its data runs to the previous session. Long replies get truncated or come back short, so ask for the closes in two halves from the same address (part F). `closes` needs the count to match SPY's stored sessions: end the range at SPY's last stored session. SPY is stored back to July 2024, so two-year panel ranges line up.
- No earnings calendar with actual figures was readable on 15 Oct (stockanalysis.com and MarketBeat served stale copies; Nasdaq refuses automated reading); the drift scan finds reporters by search (part F).
- A free price feed found on 11 Oct, not yet used: Cboe's delayed quotes (`https://cdn-api.cboe.com/api/global/delayed_quotes/quotes/<TICKER>.json`).
- Coin prices: Coinbase's public candle and ticker pages.
- Sources that did not work: CNN article pages (robots), the US News CPI article, CNBC's oil page (fetch errors on 15 Oct).
- GitHub mirror: private repository `timzwang/ft-game` (playbook part B and G6). The evening and weekly runs commit the data files and this doc as their last step; docs, scripts and the page are updated there only in sessions with Tim. ChatGPT reads it and proposes changes through pull requests, which Tim merges; nothing merged there reaches the live system until it is applied here. `state/last-sync.md` there shows the last mirror's time and file hashes.
- Two saved skills, `ft-game-playbook` and `stock-score`, load in scheduled runs; the `ft-game-playbook` skill still describes the single playbook; it still works, because it sends a run to `claude/ft-game-playbook.md`, whose routing table names the other docs. An update to the skill could not be proposed from the 15 Oct session.
