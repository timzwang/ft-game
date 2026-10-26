# Changelog

Versions of the system behind Tim's FT Stock Picking Game entry ("Seeking Beta"). The version number is the playbook's (`docs/ft-game-playbook.md`); the pipeline script and the page are noted where they changed. Newest first. Times are UK.

Before 16 Oct 2026 the system lived only in Claude, so those versions have no commits here. Their dates come from the Project docs, the scheduled tasks and the dashboard artifact's files. Version 6.0 is the first one with a snapshot in this repository: commit `9d3ce05` (the first full export, made on 16 Oct from the 6.0 files).

How a new version is recorded is set out at the end.

## 6.14 (Mon 26 Oct 2026, late afternoon)

Tim asked "What's next to implement/improve? Work on it all now" (15:11 UK). No rule, score, sizing or order changed.

- Data check fixed: `data-check` had failed every run since 22 Oct ("2026-10-22: no contribution row for Hasbro") and nobody was told. The Hasbro order of 21 Oct was replaced before it filled, leaving a zero-weight position row for a stock never held, which the check counted as a trade. A zero row for a name not held the session before is no longer a trade (`scripts/check_data.py`, commit `0ac74b9`); two regression tests. Green from 15:16 UK.
- Cut-off 08:00 UK (approved by Tim on 21 Oct at 23:31 UK; that night's work was never pushed): FT Customer Care confirmed 08:00 UK local time all year. Pipeline 7.8 (commit `9760163`, sha256 `837ab0b9...d427`, also artifact asset `e3ca0a59...`) changes only `CUTOFF_UK`, the hindsight lock on `order_expected`, so a morning revision entered after 07:00 can record its expected benefit; the data check, the tests and the page's "Enter before" bar match; every deadline in the docs reads 08:00. Runs take 7.8 from commit `9760163` (data doc G1 step 3; core part B). 7.7 (asset `97024e28...`, commit `87d8f64`) is kept as the rollback.
- Morning check to 07:26 UK, prompt deadline 08:00: the first change that afternoon was refused by the session's permission check; made at 18:03 UK at Tim's direct request ("Do this for me"). First run at 07:26 on Tue 27 Oct.
- Nightly watchdog: a new scheduled task, "FT game nightly watchdog", at 22:47 UK every day (core part I). It checks every FT game task's last run, the review log, the page's publish and the repository's workflows, messages Tim only when something is wrong, and may re-fire a failed evening review once or push a scan request; nothing else.
- Sessions with Tim now also check the repository's workflow runs and the watchdog's messages (core part I).
- Docs: core playbook (version line, part B, part C, part D, part I), data doc (G1, G3, G4), rules doc, run docs (evening, morning, weekend), page notes, roadmap (phase 10), saved skill copy, ops record.

## 6.13.2 (Mon 26 Oct 2026, afternoon)

Tim's standing instruction ("From now on, if there are any issues in the automated runs, then you must flag them to me and fix them immediately", 13:29 UK). No rule, score, sizing, order, page, feed or scan changed. Pipeline still 7.7.

- Flag and fix (core part I, "Issues: flag and fix"): every run fixes what it can in the same run (retry once, the playbook's fallback, correct the input and run again, publish again), never by weakening a safeguard, then tells Tim about any issue through SendUserMessage, fixed or not. Its final reply starts "Tim, issue in the <run> at <HH:MM> UK:" instead of "No change", so the issue shows on his phone. Runs that write the state doc add an "ISSUE:" review-log line. This overrides the price refreshes' and results-day refresh's old "never message" rule and every fixed quiet reply.
- Sessions with Tim start by checking for open issues (the review log's ISSUE and FAULT lines, "System" alerts, each task's last run) and fix them first.
- Shallow-clone fix (data doc G1 step 3): a `--depth 1` clone does not hold commit `87d8f64`, so 6.13.1's `git show 87d8f64:scripts/ft_pipeline.py` fails there with "invalid object name" (tested 26 Oct). Runs now fetch the commit by its full hash when it is missing, then take the script; the hash is unchanged. Tested on a fresh shallow clone and on a full clone; the repository copy ran `template` on the 23 Oct data in the session with Tim (exit 0).
- Scheduled tasks: the prompts of all eight enabled tasks carry the issues clause and point at G1 step 3 for the script (evening review, morning check, midday check, price refresh, late price refresh, results-day refresh, weekly review, weekend news check). Times, models and approval settings unchanged.
- Docs: core playbook (version line, part I) and data doc (version line, G1 step 3), uploaded to the Project from these files.
- 6.13.1's entry: its approval time corrected to before 13:31 UK, the time of its commit (UK time is GMT from 25 Oct).

## 6.13.1 (Mon 26 Oct 2026, afternoon)

A fix for the pipeline script being refused, approved by Tim ("Yes do everything recommended", before 13:31 UK). No rule, score, sizing, order, page, feed, scan or scheduled task changed.

- Why: from Sat 24 Oct the session's permission check refused to run the pipeline script downloaded from the artifact asset. That stopped the weekend news checks of 24 and 25 Oct and the 25 Oct evening review, which sent a fault message and left the order in force.
- Fix: commit `87d8f64` holds `scripts/ft_pipeline.py` version 7.7 byte for byte (sha256 `abbb29c4...4bbd`, the hash in core part B). Runs now take the script with `git show 87d8f64:scripts/ft_pipeline.py` (data doc G1 step 3) and check the same hash. That copy ran on 26 Oct. The artifact asset stays as the fallback and the record.
- G6: push with `git push origin HEAD:main`, because the session's clone can sit on a detached HEAD (the 25 Oct push of `main` was refused).
- Docs: core playbook (version line, part B) and data doc (G1, G6), uploaded to the Project from these files.

## 6.13 (Wed 21 Oct 2026, late evening)

The endgame stance. Approved by Tim at 22:38 UK ("Yes", to suspending the guardrail rules for the rest of the game). No score, panel, pipeline, page, scan, feed or scheduled task changed. Pipeline still 7.7.

- Why: Claude's gap maths of 21 Oct (20,000 simulated paths of 26 sessions; each stock's return against SPY resampled from the last 250 sessions with its average set to zero, plus options-implied results moves) put the top 2% line about 14.5 points above the market by 27 Nov. The order in force had about a 1% chance of reaching it; a high-beta book pointed one way about 10% to 21%, with about a 50% chance of finishing below the market.
- Core playbook part D: a new "Endgame stance" block, which wins over anything in parts D and E that conflicts. Suspended: the score floor and trend tests for a new position, the downtrend replacement, the 10% caps on results, momentum and drift positions, the results budget, the volatility caps, the 45% theme guide and the 20% normal maximum. Kept: the game's rules, the 07:00 UK cut-off, confidence ratings, the trade decision gate and `order_expected`, the crypto rules, the exit rules (heavy-volume close below the open; a report gap down beyond its options move with a close in the lower half), every record and test.
- The switch: the 22 Oct evening review sells every holding and sets order A (memory-led: Sandisk 20, Micron 15, AMD 15, Palantir 15, Arm 15, Seagate 10, Western Digital 10) or order B (Sandisk 10, AMD 15, Palantir 15, Arm 10, Shopify 15, Datadog 10, ServiceNow 10, Robinhood 10, Strategy 5) for Fri 23 Oct's open, by Western Digital's after-hours reaction to its 22 Oct results. The watchlist cap of 25 is lifted until 30 Oct.
- Rules doc part E: a pointer to the stance at the top. State doc, roadmap (items 61 and 62).
- Also 21 Oct: PR #7 (not merged): the top-five panel test and the overbought split as a read-only `research` command, for after the results cluster.

## 6.12.1 (Wed 21 Oct 2026, late evening)

A price feed fix, asked for by Tim after the 21 Oct evening review ("Fix the issue and prevent anything similar occurring in future"). No rule, score, sizing, pipeline, page or order changed. Pipeline still 7.7.

- Why: the 21 Oct evening review named nine new tickers on a `tickers:` line. Analog Devices, a panel member not yet in the price store, came back with only ten rows: `feed.py` treated its close-only panel series as a stored history and sent no two-year series. Its score was unusable, so the run left it off the watchlist. AT&T, also a panel member, lost its drift entry's volume, 50-day and 200-day figures the same way.
- Feed version 1.1 (`feed/feed.py`, commit `2b276c4`): a new `wants_long` rule sends the two-year series to every list or requested stock outside the price store, panel members included. Panel-only members keep their ten rows, so the file does not grow each night. `meta.short_history` in `latest.json`, a line in `latest.md` and the job log name any list or requested stock still short of 200 sessions after the feed.
- A second fault of the same kind, found when the data check ran on the re-run: Yahoo's first bar after the close can have its open outside its own high and low. On 21 Oct this hit Charles River (open 313.83, low 315.825), whose row the pipeline skipped, and UnitedHealth (open 421.80, high 421.47; the later bar has 421.80), which failed the data check. Feed 1.1 now widens such a bar's high and low to include its own open and close, since both traded, and lists the bars it changed (`meta.ranges_widened`, also in `latest.md`). UnitedHealth's stored row was corrected the same way and history republished.
- Docs (uploaded to the Project from these files): the evening run doc, step 4, now checks each new candidate's history after `feed`; one still short is re-requested once before it is left out, and never scored on a short history. Data doc G8 step 2; core playbook version line.
- Tests: `test_feed_long_series_for_a_requested_panel_member` and `test_feed_widens_a_bar_that_excludes_its_own_open`, 160 in all, all passing.
- Applied the same evening: the forced feed run on 1.1 (20:58 UTC) gave ADI 551 rows and reported no short histories. The review was re-run from the same input files with Analog Devices added (score 64, strong) and AT&T's drift row completed (still FAIL: reaction, held and trend). Stocks, ledger, history and panel were republished (macro unchanged). The order for Thu 22 Oct is unchanged.

## 6.12 (Wed 21 Oct 2026, afternoon)

A price feed that does not depend on fetching pages, and pipeline 7.7 (7.6 plus a `feed` command) deployed. Approved by Tim on 21 Oct, 12:29 UK. No rule, score, sizing, panel rule, scan rule or order changed. Pipeline 7.7: asset `97024e28a7cbb015b5fdc48c6d4b68cf`, sha256 `abbb29c46723461bb44f83e15db8a4317e19daf3168d078daa5c8615abd74bbd`; 7.4 (asset `30bd733ca18434b8f577f2d57c3813e3`) kept as the rollback.

- Why: on Tue 20 Oct the scheduled evening review's fetch tool refused every address it had not first seen in a search result. Nine rows went missing (Marathon Petroleum, Humana, Valero, Phillips 66, the oil fund, the US lines of Shell and BP, the Ether fund, RTX), the Treasury row, the coin prices and the market data service could not be reached, and the inception standstill stopped at 19 Oct.
- The price feed (`feed/`, `.github/workflows/feed.yml`, `feed/README.md`; roadmap item 59). A GitHub job reads Yahoo Finance's daily bars (dividend adjustment off) for every list stock, SPY, every stored ticker and the 30 panel stocks (two years for any with a short store), the Treasury's 2, 10 and 30-year yields from its own file, Coinbase's Bitcoin, Ether, Solana and XRP at the hour before the US close, and front-month futures as a commodity fallback. It checks each ticker's last 25 sessions against the stored prices and writes `feed/latest.json` after the US close (20:16 and 21:16 UTC, and at once on a request line pushed by a run, since GitHub often starts scheduled jobs 20 to 40 minutes late) and `feed/live.json` on request during the session. First run (984 overlapping sessions, 41 tickers): closes equal to the cent in 973, largest gap 0.42% (one close-only row from September); 837 of 858 opens within 0.05%.
- Pipeline 7.7: `feed --feed latest.json --today today.json --history history.json --panel panel.json [--futures yes]` fills today.json after `template` (every missing row up to `date` for the list, SPY and stored tickers; two years for a stock short of 200 closes; empty quote fields and the 52-week range; empty Treasury and coin values; drift entries' price fields; the panel's missing closes). It re-checks each ticker against the live store and refuses one that disagrees (close beyond 0.5%, or open, high or low beyond 1.5%: the wrong listing, pence against pounds, a split), never replaces a stored row, never passes `date`, and is safe to repeat. `feed --live live.json --stocks stocks.json --out quotes.json` writes quotes.json for `refresh` and refuses a file read more than 90 minutes ago. Every other command is unchanged: `run` on the 16 Oct snapshot and on the 20 Oct mirror gives byte-identical files with 7.6 and 7.7 (`proposals/claude/2026-10-21-evidence/`).
- Pipeline 7.6 deployed (prepared 19 Oct after ChatGPT's review of 7.5, PR #6, merged now): listing calendars for 26 Nov fills, several fills between sessions priced leg by leg, results coverage by date, one hindsight lock for `run` and `reorder`, stricter data check. Re-checked before merging: 148 tests pass; the data check passes on the 20 Oct mirror.
- A dry run on the 20 Oct mirror: `feed` filled all nine missing rows, two years for Walmart, Hasbro, Shell and BP (so "Averages still needed" empties), RTX's row for the inception standstill, and the panel's missing closes (including HPE's two years).
- Docs: data doc part F (the feed first; in a scheduled run reach every page through a search), G2, G3, G4 and a new G8 (how runs read the feed); evening run doc (steps 2 to 4 and the quiet-evening line); weekly (steps 1 to 5: Friday's rows, the panel top-up and drift settlement from the feed; the Marsh & McLennan question); refresh (step 2: live quotes from the feed); morning (search first); core playbook (version line, part B); roadmap (items 58 to 60, phase 8, still open, limits); page notes. Uploaded to the Project from these files. The state doc (status, section 8 item 5, tools, one review-log line) was updated in the Project only: `state/` here stays as the 20 Oct evening review mirrored it (`323663b`), so `state/last-sync.md` stays true, until tonight's review mirrors the Project copy (as in 6.11.1).
- Held back since 19 Oct with 7.5, now live (Tim approved them with PR #4): rules doc part E (what a confidence rating means, portfolio fit, the trade decision gate before every change of order, now marked in force), the evening run's step 6 and playbook part I wording, and the page's conviction tooltip and calibration banner (`files/app.js` version 4, equal to `page/app.js`).
- Scheduled tasks: the 16:45, 19:22 and 14:50 UK refresh tasks recreated from a chat with the repository attached (they dated from 9 Oct and could not reach it), same schedule, notifications and prompts apart from the feed, automatic approval confirmed; the old ones switched off, not deleted. A one-off task created the same way pulled the repository, pushed a live request at 13:07 UK (`4d9dd99`) and had the live feed back two minutes later (`cc7f182`). Evening, weekly, morning and weekend tasks unchanged.
- Tests: 10 more (`tests/test_feed.py`), 158 in all; the tests workflow now also runs on changes to `feed/`.
- Open, for Tim: Marsh & McLennan. The panel swap agreed on 17 Oct rested on a 190-session feed; Yahoo has two years for it.

## 6.11.1 (Mon 19 Oct 2026, about 22:25)

The Mon 26 Oct cut-off experiment removed, at Tim's request (decided before this session; applied here). An operational change only: no pipeline, page, score, order or scheduled task changed, and it does not wait for the 7.5 review below.

- Removed: the one-point Exxon and Chevron test order planned for about 07:15 UK on Mon 26 Oct (playbook part C, agreed 17 Oct in 6.4). It would have fallen on Coca-Cola's last-order morning and could gain at most an hour that the 06:36 morning check does not need.
- Kept: the 06:36 UK morning check, the precautionary 07:00 UK cut-off until the FT confirms the cut-off after the clock change, and every order.
- Live (Claude Project, written from local files in the session): `claude/ft-game-playbook.md` (version line; part C: the test bullet replaced by a line saying no test order is made, and "Until the FT or the test below settles it" now "Until the FT confirms it"), `claude/ft-game-roadmap.md` (item 44 and "Still open"), `claude/ft-game-state.md` (sections 1, 2, 6, 7, 8 item 4 and 12; one review-log line added and the oldest dropped to keep 15). The saved `ft-game-playbook` skill names the test once ("A test on Mon 26 Oct settles it"); Claude cannot edit saved skills, so an updated copy is offered to Tim to save, and the Project docs win where they differ.
- Mirror: `docs/ft-game-playbook.md`, `docs/ft-game-roadmap.md`, `skills/ft-game-playbook/SKILL.md`, with the same wording. `state/ft-game-state.md` here is left as the 19 Oct evening review mirrored it (commit `0d3c4e8`), so that commit stays the untouched evidence for its acceptance check; the next evening review mirrors the Project copy, which carries the change. Note: `docs/` on `main` also carries the 7.5 wording merged in PR #4, which is prepared but not deployed; the Project docs do not.
- Script: `proposals/claude/2026-10-19-evidence-4/remove_cutoff_test.py` (on the 7.6 branch), each replacement matched exactly once.

## 6.11 (Mon 19 Oct 2026, about 20:40)

Expected benefit before every change, and a data check on every mirror, after ChatGPT's follow-up review of 19 Oct (`proposals/chatgpt/2026-10-19-follow-up-review.md`, branch `chatgpt/handoff-2026-10-19`, PR #3). Tim approved both. No rule, score, order or scheduled task changed. Pipeline version 7.4 (asset `30bd733ca18434b8f577f2d57c3813e3`, sha256 `5adc3093a10b57ead4c229d6d900c765967ba505a0578cf8262ac91f88b4055e`).

- Pipeline 7.4: `order_expected` in today.json and order.json, `{"pts", "thesis", "invalidation"}`: the points a change of order is expected to add over the five sessions from its fill against keeping the order in force, the same measure as its STANDSTILL change row. Stored as an `expect` ledger row; it can be restated until the change fills and is locked after (a first figure given after the fill is refused as hindsight). A change with no expectation draws a WARNING. STANDSTILL change rows carry it (`forecast`) and, once complete, actual minus expected (`surprise`); EXPECTED BENEFIT in `run` and `report` gives the totals and how often the sign was right. The template writes an empty `order_expected`. With none given every figure is identical to 7.3: the 16 Oct session re-run with both gives identical files (`proposals/claude/2026-10-19-evidence-2/compare_73_74_output.txt`).
- Data check: `scripts/check_data.py` and `.github/workflows/data-check.yml`. On every push that changes `data/` or `state/`: the files parse; ledger rows have exactly the pipeline's fields and unique ids; one price row per ticker and date with consistent prices; `stocks.json` matches the latest order and the game's rules; no benchmark session missing from the performance log, values compound and contributions add up to each day's return; every holding's results date has an event; no report inside five sessions without an implied move (inside ten: a warning); the files match `state/last-sync.md`. Sun to Thu 23:15 UTC and Sat 11:15 UTC, with `--fresh`: the mirror ran in the last six hours and prices and performance reach the latest closed US session. On the stored 16 Oct files it fails on one item, AbbVie's missing results event (the 19 Oct evening review adds it). Output: `proposals/claude/2026-10-19-evidence-2/check_data_on_16oct_files.txt`.
- Tests: 26 more (`tests/test_check_data.py`, `tests/test_expect.py`), 66 in all.
- Docs: core playbook (version line, part B), data (G3, G4, G6), rules (part E, standstill test), evening run doc (step 6, output items 3 and 15), morning run doc (step 5), roadmap (items 56 and 57), state doc; uploaded to the Project from these files. README.
- Not changed: the order, the data files, the score, the page, the scheduled tasks. The 7.3 asset is kept.

## 6.10 (Mon 19 Oct 2026, about 00:40)

Settlement, the calendar and a results budget for the October cluster, after ChatGPT's repository review of 18 Oct (`proposals/chatgpt/2026-10-18-repository-review.md`, on its branch and PR #2). Claude checked the findings against the same commit (`25e8a93`) first; Tim approved the fixes and one rule change. Pipeline version 7.3 (asset `f8ce759cc09d110095a10bbf712ae582`, sha256 `ca39efd22325da4c8ddb1158fe72ea64e39436d7b76434d4e8cd41727f9921b3`).

- Rule (part E): reports dated 27 to 30 Oct are judged against a results budget of 1.0 points instead of 0.6, because the entry is about 5 points behind the top 2% line and a results day is close to a fair bet. A ceiling, not a target: a holding that has weakened is still cut or exited before its report.
- Pipeline 7.3, review finding 1: `RESULTS MISSING` and a WARNING for a holding whose own next-results text names a date with no results event (AbbVie, 30 Oct, had none; the results total read 5.40 points instead of 6.00). The budget is applied by report date and written to a `meta` row for the page.
- Finding 2: a confidence rating settles over one window of five index sessions from its fill date, needing the stock's traded open on the fill date and its close on the fifth session; otherwise it waits and, after 15 sessions, settles as "n/a" with the reason. In 7.2 the stock's first five rows were used, so a missing day moved its window away from the index's, and an estimated open could be scored.
- Finding 3: shadow ratings need the stock's close on the exact end date. The broad scan settles on the benchmark's sessions and needs the stock's rows on them; a row closed with no figures counts in neither direction.
- Finding 5: an FT reading given again (same date, value and rank) fills in `top2_return_pct`, `players` and `note`; in 7.2 the repeat was dropped.
- Finding 6: 26 Nov is not a US session and 27 Nov closes at 13:00 New York (18:00 UK), in the pipeline (next session, sessions ahead, RECONCILE), the scan (bar finality) and the page (stale-price marker).
- Finding 7: a stored row marked as having no traded open keeps the mark when given back, and a change of mark alone counts as a correction; `market_closed` entries are kept in the ledger.
- Finding 8: the scan workflow runs only from `main` (a manual run on another branch could have pushed that branch to main).
- Finding 9: roadmap items 39 and 42 corrected (the top-five panel test and the overbought split were never built; deferred to after the game) and item 45 marked superseded; the page's day-call help text no longer says it nudges cash.
- Tests: `tests/`, 40 regression tests with real assertions, and `.github/workflows/tests.yml` running them on every change to the scripts, the page or the tests. Run against 7.2, 19 fail. Evidence: `proposals/claude/2026-10-19-evidence/` (7.2 against 7.3 on the 16 Oct session: identical files apart from one new `meta` row).
- Scan libraries pinned (`scan/requirements.txt`) except yfinance, which follows Yahoo's changes.
- Page: `files/app.js` version 3 (Risk tab budget by date, US calendar, day-call wording). Docs: core playbook (version line, part B, part D), rules (part E), data (G3, G4), evening run doc (step 10), roadmap (39, 42, 45, 53 to 55, the final week), page notes, state doc.
- Not changed: the order (Mon 19 Oct's, entered by Tim), the data files, the score, the scheduled tasks.

## 6.9 (Sun 18 Oct 2026, about 23:50)

Scheduled runs reach the repository, for real this time. Tim asked whether everything implemented was in the repository; the check found the 18 Oct evening review had not mirrored anything.

- Cause: the evening review run of 18 Oct (21:31 to 21:50 UK) found no clone at `/home/claude/ft-game`, and a plain HTTPS clone asked for credentials. A scheduled task's runs only start with the repository attached, and with git access, if the task was created from a chat that had the repository attached. The evening and weekly review tasks were created on 8 and 9 Oct, before the repository existed. The 6.8 test passed only because its own task was created on 17 Oct from such a chat. 6.8's conclusion was wrong.
- Fix, approved by Tim: new evening review and weekly review tasks created from a repo-attached chat, with the same prompts, schedules, notifications and automatic approval. The old two are switched off, not deleted (run history kept; switch them back on to undo).
- Test: a one-off task created the same way ran at 23:43 UK, found the clone, pushed commit `8d9ed20` (a line in `sync-test/hello.txt`) with plain git and reached the Project.
- Catch-up: the 18 Oct evening data files (byte for byte from the artifact) and the state doc (a text copy) pushed by hand, commits `1a0259e` and `a1f5232`. `skills/ft-game-playbook/SKILL.md` updated to the saved skill (6.4 version, 17 Oct).
- Docs: core playbook version line; state doc (status, section 8 item 5, section 12), uploaded to the Project from the repository file; README; `ops/scheduled-tasks.md`.
- Rule from now on: any new scheduled task that needs the repository is created from a chat with the repository attached.
- No change to the order, the pipeline, the page or any task prompt.

## 6.8 (Sun 18 Oct 2026, about 10:50)

GitHub access from scheduled runs (item 2 of the fourteen changes Tim approved on 17 Oct).

- A one-off scheduled test at 10:08 UK found `timzwang/ft-game` already cloned in the session at `/home/claude/ft-game`, cloned it again over HTTPS without credentials, read `scan/latest.json`, and passed a dry-run push. `add_repo` was not available to the scheduled run; the GitHub tools (`mcp__github__*`) were. Report: Project doc `claude/ft-game-diag-github.md` (deleted after this change; summary here).
- Data doc G6 step 1 and G7 step 1: use the session's clone if present, else a plain HTTPS clone; `add_repo` and then the GitHub tools as fall-backs (the tools can read the scan for G7; G6 needs git). The weekly task prompt carries one line saying the same. The evening task prompt was left as it was: the update was stopped by a safety check because that prompt holds the market data key. The evening run follows the data doc, which is enough.
- The first real push from a scheduled run will be tonight's evening review (G6, best effort).
- No change to the order, the pipeline, the page or any data file.

## 6.7 (Sun 18 Oct 2026, about 01:40)

Price integrity, after ChatGPT's challenge of Claude's audit verification (pasted into the project chat by Tim). Tim approved the three fixes Claude drafted and tested. Pipeline version 7.2 (asset `2726d826123a22d94290a175e5dab68e`, sha256 `1a46ea6fa8f406257b98ae02c78c84d4bb8adb621754733b5c1fc555ca8f36e4`).

- Open provenance (ChatGPT's H9): a price row given without an open is stored with the close in its place and marked `open_obs: false`, and is never used as a fill price. In 7.1 any row with a volume counted as having a traded open, so an invented open could be taken as a fill in the drift record and, a case ChatGPT did not raise, in the performance log's buys and sales.
- Strict performance (ChatGPT's H6): a session is recorded only when every stock held or traded that day is priced and every buy or sale has a traded open or a stated fill price. Otherwise it and every later session wait (PERFORMANCE INCOMPLETE plus a WARNING) and the next run with the rows adds them. `market_closed` in today.json covers a genuine holiday. In 7.1 the stock was skipped with a warning; on Exxon's 14 Oct row removed as a test, 7.1 logged that day at -0.16% instead of +0.09% and caught up the next session.
- Drift: a reporter whose next-session open never arrives is marked "n/a" after 15 sessions (close-basis figure kept) instead of a win or loss, so it stays out of the calibration.
- Tests (`proposals/claude/2026-10-18-evidence/v72_tests.py`): the 16 Oct session re-run end to end with 7.1 and 7.2 on the same files gives byte-identical stocks, ledger, history, macro and scores; ChatGPT's example row is no longer read as a traded open; with Exxon's 14 Oct row removed 7.2 stops before 14 Oct and matches the stored log once the row is restored.
- No stored row was affected. The one suspicious open in the game period (Shell, 13 Oct, 3,836, equal to the previous close) matches stockanalysis.com.
- Docs: core playbook (version line, part B), data doc (G3, G4), rules doc (part E, drift record), roadmap (item 52).
- No change to the order, the page, the scheduled tasks or any data file.

## 6.6 (Sun 18 Oct 2026, about 01:20)

A handoff log between Claude and ChatGPT, at Tim's request.

- New folder `handoff/` with a `README.md` setting the rule and format: read the newest notes before starting, write one at the end of any session that decided, changed or found something. Claude commits its notes to `main`; ChatGPT proposes its notes through pull requests that Tim merges. Notes record who said what; the live files win.
- Core playbook part B: Claude reads and writes the log in every session with Tim. Scheduled runs do not.
- First note: `handoff/2026-10-18-claude.md`. Claude's audit verification and its evidence added under `proposals/claude/`.
- README: the log added to "Start here" and the layout.
- No change to the order, the pipeline, the page, the scheduled tasks or any data file.

## 6.5 (Sun 18 Oct 2026, about 01:00)

The standstill test corrected, after Claude's second, read-only review of the outside audit (a handover report for ChatGPT). Tim approved this one change. Pipeline version 7.1 (asset `3e3904212ba88da023d24d244d6b1a15`, sha256 `367d303f0101eb48a8957e06d52d00b8f97f4ea0ff9b614c171149bbea8c2201`).

- Pipeline 7.1, STANDSTILL only: each week is judged against the order in force before it, so a change that fills on a Monday (a weekend rebuild) counts; version 7 used the order after Monday's fill, which left those changes out. New inception rows: the first order (9 Oct) never changed, as entered (with its 25% cash) and fully invested, against the actual estimate, priced to the last session with every price. STANDSTILL NEEDS and the template also name the first order's stocks that have left the list. A price row for a stock not held that day or the day before no longer makes the log recalculate.
- Price store (history dataset version 12): the missing rows for RTX, Lockheed Martin and Nvidia (14 to 16 Oct) and Goldman Sachs (15 and 16 Oct), from stockanalysis.com. No existing row changed. They also let four stuck confidence ratings settle.
- Corrected record to 16 Oct: +0.12 points against never changing the first order as entered, -0.32 against it fully invested, -0.75 for the 12 Oct rebuild alone; no evidence either way. The +0.86 points quoted on 17 Oct (rules doc, state doc, roadmap) measured only the week after the rebuild and is withdrawn.
- Docs: core playbook (version line, part B), rules (the standstill test), data doc (G3, G4), weekly run doc, roadmap (items 38 and 51), state doc.
- Tested by re-running the 16 Oct session with versions 7 and 7.1 on the same files: stocks, history, macro, panel and scores byte for byte the same; every ledger row the same except the standstill rows, whose figures match an independent reconstruction.
- No change to the order, the page, the scheduled tasks or any other data file.

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
- Sun 18 Oct: order cut-off shown as 07:00 UK (`app.js` version 2).
- Mon 19 Oct, about 00:30: results budget read from the ledger (1.0 for 27 to 30 Oct), US calendar for 26 and 27 Nov, day-call help text (`app.js` version 3).
- Wed 21 Oct, afternoon: conviction tooltip and calibration banner wording from 19 Oct deployed (`app.js` version 4).

## Recording a new version

Versions change only in a session with Tim; scheduled runs never change the version. For each new version, in the same session:

1. Raise the version line at the top of `docs/ft-game-playbook.md` and of each doc that changed, and upload those files to the Project from the repository files (part J).
2. Add an entry at the top of this file: version, UK date and time, a one-line title, the changes as bullets.
3. Update the "Current version" line at the top of `README.md`, then commit and push.
4. Give Tim, in the chat, everything to paste on GitHub, each piece in its own code block so it copies in one go (Tim's request, 19 Oct: never point him to a file instead): the release tag (`vX.Y`, on `main`), its title ("Version X.Y: <title>"), its notes (the full entry from this file, in the same markdown format, without the version heading), and a new repository description (the "About" text, at most 350 characters) naming the current version and its date, its changes in a few words, the version before it, and this file. Claude cannot do either itself: on 16 Oct the session's git proxy refused tag pushes and repository settings changes (HTTP 403).
