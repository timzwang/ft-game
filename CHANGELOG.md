# Changelog

Versions of the system behind Tim's FT Stock Picking Game entry ("Seeking Beta"). The version number is the playbook's (`docs/ft-game-playbook.md`); the pipeline script and the page are noted where they changed. Newest first. Times are UK.

Before 16 Oct 2026 the system lived only in Claude, so those versions have no commits here. Their dates come from the Project docs, the scheduled tasks and the dashboard artifact's files. Version 6.0 is the first one with a snapshot in this repository: commit `9d3ce05` (the first full export, made on 16 Oct from the 6.0 files).

How a new version is recorded is set out at the end.

## 6.4 (Sun 18 Oct 2026, about 00:30)

After an outside audit (ChatGPT, 17 Oct) that Claude checked against the live Project, artifact, scheduled tasks and code. Tim approved fourteen changes. Pipeline version 7 (uploaded 17 Oct, asset `fdfb8e108f26b962b62a9ca0a9909846`, sha256 `23e9c9fe7645ed4df2b66d5b8263378c983ed7c9c47e1bf0ef07531dca1867b1`).

- Cut-off: the FT's terms quote BST even for November, so from 17 Oct every order is to be entered before 07:00 UK until the FT confirms the cut-off after the clock change (part C). Morning check moved from 07:26 to 06:36 UK (scheduled task changed). A one-point Exxon and Chevron test at about 07:15 on Mon 26 Oct settles it. A question to FT help is drafted.
- GitHub access: the 17 Oct weekly run had no repository tool, so G6 and G7 failed. A one-off scheduled test at 10:07 UK on 18 Oct decides whether they stay in scheduled runs or become hand-run only.
- Pipeline 7: drift results settled from the next session's open (the old close-based figure kept beside it); STANDSTILL (each change against the order it replaced, five sessions; each week against its first-session order); RESULTS TOTAL (weight times implied move added up over five and ten sessions); RECONCILE (each FT figure against the estimate at the same close, flagging reads before the US close); JUDGEMENT TEST (shadow ratings now store the 60 price and session points and the 40 judgement points). The template names stocks sold in the last five sessions that left the list. Tested against the live files: stocks, history, macro and panel byte for byte the same as version 6.
- Rules (part E): implied moves for holdings reporting inside ten sessions; results total quoted; sold stocks stay on the watchlist five sessions; score, anchor and panel rule frozen for the game (Marsh & McLennan swap agreed); confidence labelled "not calibrated" in order tables.
- Weekly review: reconciliation, standstill and judgement sections; FT value to be read after the US close.
- Broad scan: slots 20:20 and 21:20 UTC (from 20:10 and 21:05), a US bar final from 16:15 New York, and stocks that cannot be measured are logged (the 867 of 868 on 16 Oct).
- Data: Tim's 16 Oct FT figures (101,402, rank 3,269 of 13,918) recorded in the state doc for the Sunday review; 35 credits below the estimate, so the 144-credit gap on 13 Oct was the reading time.
- This repository refreshed by hand: data to the Fri 16 Oct close, state, docs, pipeline 7, scheduled tasks copy.
- No change to the order, the page or any data file.

## 6.3 (Fri 16 Oct 2026, about 09:10)

The broad scan (roadmap item 43).

- New GitHub Actions job (`.github/workflows/scan.yml`, `scan/scan.py`, rules in `scan/README.md`): after every US close it scans 868 stocks (S&P 500, the rest of the Nasdaq-100, FTSE 100, FTSE 250) from a bulk Yahoo Finance download and writes two lists to `scan/`: Leaders (12-month trend excluding the last month, near the 52-week high, above both averages) and Events (a 3% gap that held, on 1.5 times volume). Rules version 1, fixed before any result was seen.
- The top 10 of each list is settled five sessions later, close to close and from the next open, in `scan/record.csv`. First rows: Fri 16 Oct.
- Data doc: new G7 (reading the scan, forcing a run through `scan/request.txt` if the scheduled one is late, and how the lists feed the intake). G6 reuses G7's clone. Part F: the scan's Events lead the search for reporters.
- Evening review (H1 step 4) reads the scan first; weekly review (H5) quotes its record. Rules (part E): the intake draws at least half its names from the scan when enough pass a first look.
- Scan figures never enter today.json or the score; every name is checked from part F's sources.
- Tested on synthetic prices and in eight live runs on 16 Oct. Yahoo's London stock data was missing 15 Oct that morning, so London is first tested in Friday evening's run. Stooq, the planned fallback, refuses GitHub's servers.
- No change to the scheduled tasks, the pipeline, the page or the portfolio.

## 6.2 (Fri 16 Oct 2026, about 01:30, later)

After ChatGPT's strategy review.

- Rules (part E): the day call is a research record only and never moves cash; it may become a cash input again only after beating always-green over at least 20 settled calls, with Tim's agreement.
- Rules (part E): "overbought" (RSI) is a warning, no longer a 5% cap. "Extended" still caps a new position at 5%.
- Roadmap phase 6 (items 38 to 43): counterfactual portfolios (standstill, previous order, price-only and full-score top five), a top-five panel test, a test of the 40 judgement points, score weights fixed for the game unless Saturday's 30-stock verdict is decisive, and a design for a broad scanner of about 900 US and London stocks on GitHub Actions. Items 38 to 40 wait for pipeline version 7; the scanner waits for Tim's agreement that runs may read `scan/` from this repository.
- G6 and part B: runs may read the repository's `scan/` folder to find candidates once the broad scan is built (agreed by Tim). Scan figures never enter today.json.
- Open question added: whether the game's 08:00 cut-off means BST after the clock change on 25 Oct.
- ChatGPT's review saved as `proposals/chatgpt/2026-10-16-strategy-review.md`.
- No change to the scheduled tasks, the pipeline, the page or the portfolio.

## 6.1 (Fri 16 Oct 2026, about 01:30)

GitHub mirror. Commits `bfd5b15` (playbook) and `8459eae` (this changelog).

- New private repository `timzwang/ft-game`, shared by Claude and ChatGPT. Tested end to end: a push from a chat, a push from a one-off scheduled cloud session with nobody present, and a ChatGPT branch and pull request merged by Tim.
- First full export: docs, state, scripts, data, page, skills, and the scheduled tasks with the market data key redacted. Scripts and data byte-identical to the artifact.
- G6 (data doc): the evening and weekly reviews mirror the data files and the state doc to GitHub as their last step, best effort, with a check for keys before every commit.
- Part J (core playbook): the state doc is always written to a local file first and uploaded from that file, so the Project and GitHub copies are identical.
- Evening and weekly run docs: new last step, G6.
- Versioning: every new version gets an entry here, the README's version line, and a release and repository description that Tim sets on GitHub from text Claude supplies.
- No change to the scheduled tasks, the pipeline, the page or the portfolio.

## 6.0 (Thu 15 Oct 2026, 22:20)

Split playbook, a fair test of the score, results season. Pipeline version 6 (uploaded 21:13).

- The playbook split into a core doc (parts A to D, I to K, with a routing table), a rules doc (E), a data doc (F, G) and one doc per run (H1 to H7), so each run reads only what it needs. Part letters unchanged.
- Panel test: 30 stocks fixed in advance by rank alone (every fifth of the 150 largest in the S&P 500), with the measure and pass mark fixed before any data was seen. First result on 15 members: no evidence the price points rank stocks (+0.028, t +0.5, 48 dates).
- Earnings-drift scan: six tests on each day's reporters (beat, raised guidance, reaction, held, volume, trend), with verdicts enter, watch or fail, each settled after five sessions.
- Pipeline: `panel` command, `--panel` on `template` and `run`, drift entries, the panel file outside the page's data.
- Confidence ratings kept close to 50 to 60 until the score shows an edge.
- Earlier the same evening (about 20:35): the instructions in all eight scheduled tasks rewritten to about half their length.

## 5.4 (Sun 11 Oct 2026, 23:10)

Market data service. Pipeline version 5.4 (uploaded 22:55).

- massive.com (formerly Polygon.io), free plan, on an account opened by Tim's father, for a year of daily closes per stock.
- A run fetches from it only when its own instructions carry the key, up to ten stocks a night; otherwise it falls back to the price site's rate-limited feed.
- New `closes` command lines the figures up with stored sessions and refuses them if they disagree.
- Mon 12 Oct, 13:10: the key added to the evening and weekly review tasks, and only there.

## 5.3 (Sun 11 Oct 2026, 22:30)

Crypto tracking.

- Bitcoin, Ether, Solana and XRP prices at every US close; Bitcoin's and Ether's trend from the IBIT and ETHA funds.
- Each stock's measured link to Bitcoin; crypto-linked stocks bought only while Bitcoin's trend is up, at 10% at most, 15% in all.
- Strategy and Coinbase on the watchlist as standing trackers; a "Bitcoin falls 15%" scenario; a Crypto block on the Macro tab.

## 5.2 (Sat 10 Oct 2026)

Quiet-day rule.

- The reviews still run every day, but Tim is messaged only when there is something to enter or a run has hit a fault. Price-refresh alerts and watchlist changes go on the page only.

## 5.1 (Sat 10 Oct 2026)

Weekend news check.

- New scheduled task, Saturday and Sunday at 20:20 (created 10 Oct, 00:16): the Iran war, oil supply, US policy and news on every holding, each item rated A, B or C for this portfolio.

## 5.0 (Fri 9 Oct 2026)

The full build: macro, the day call and calibration on top of phases 1 to 3. Playbook doc created 19:09.

- Accuracy: performance log (weight times return), price history store, calendar to 27 Nov, weekly review.
- Selection: indicators from stored prices, a score out of 100 (trend 40, short term 20, catalyst 20, revisions 20), analyst revision tracker, options-implied results moves with a 0.6-point budget, nightly watchlist intake with strength bands.
- Risk: volatility caps, risk shares and correlations, scenarios, rank-aware stance, post-mortems.
- Macro: US, UK, German, French, Italian and Japanese yields, Brent, WTI, gas and gold; a bull case, a bear case and a green-or-red call for the next session; an economic release tracker.
- Calibration: a shadow rating for every stock every evening.
- First pipeline uploaded 23:26. More scheduled tasks: midday check, results-day refresh and weekly review (19:24), late price refresh (19:54).

## Before 5.0 (Thu 8 to Fri 9 Oct 2026)

Setup. Version numbers before 5 were not recorded.

- Thu 8 Oct, 23:35: state doc created. 23:37: evening review and morning check created. About 23:55: game account opened.
- Fri 9 Oct, about 00:00: first chosen order (Exxon Mobil, Chevron, Shell, RTX, Lockheed Martin, TSMC, Nvidia, 25% cash). 00:08: price refresh created.

## The dashboard page

Not versioned with the playbook; its changes are listed here by date.

- Sat 10 Oct: two design rounds in the style of Trading 212 and TradingView.
- Mon 12 Oct, 01:40: denser rebuild, three-column layout on wide screens, company logos.
- Mon 12 Oct, about 18:30: one row per stock on phones, a one-column Order panel, shorter statuses.

## Recording a new version

Versions change only in a session with Tim; scheduled runs never change the version. For each new version, in the same session:

1. Raise the version line at the top of `docs/ft-game-playbook.md` and of each doc that changed, and upload those files to the Project from the repository files (part J).
2. Add an entry at the top of this file: version, UK date and time, a one-line title, the changes as bullets.
3. Update the "Current version" line at the top of `README.md`, then commit and push.
4. Give Tim, in the chat, two pieces of text to paste on GitHub: the release (tag `vX.Y` on `main`, title "Version X.Y: <title>", notes from the entry here), and a new repository description (the "About" text, at most 350 characters) naming the current version and its date, its changes in a few words, the version before it, and this file. Claude cannot do either itself: on 16 Oct the session's git proxy refused tag pushes and repository settings changes (HTTP 403).
