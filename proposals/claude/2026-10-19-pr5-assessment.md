# ChatGPT's review of 7.5 (PR #5): Claude's verdicts, the 7.6 fixes and tonight's mirror

Claude, Mon 19 Oct 2026, about 21:55 to 23:00 UK. Tim asked for the planned 6.12 / pipeline 7.5 deployment to wait on ChatGPT's independent review (PR #5), for each finding to be reproduced independently, for focused fixes on a separate branch, for tonight's real mirror to be checked from its commit, and for the 26 Oct cut-off experiment to be removed. Nothing here is deployed.

Evidence: `proposals/claude/2026-10-19-evidence-4/` (scripts and their outputs). British English, UK times.

## 1. What was reviewed, and what is live

| Item | State |
|---|---|
| Repository reviewed | `main` at `1b89752` (PR #4's merge `d52dbcb` plus two scan commits), then tonight's mirror `0d3c4e8`; PR #5 at `d036867` |
| Pipeline on `main` | 7.5, sha256 `244a8af9...346f`: **merged, not deployed** |
| Pipeline live | 7.4: artifact asset `30bd733ca18434b8f577f2d57c3813e3`, sha256 `5adc3093...055e`, matching part B of the live playbook. No 7.5 asset was ever uploaded |
| Page live | `files/app.js` version 3, sha256 `0cb594a8...0d95`, identical to the 6.11 file (`f9241ee`); the 7.5 wording on `main` (`1583ef5d...cc73`) is not live |
| Project docs live | 6.11 text (7.5's doc edits were never uploaded); from tonight 6.11.1 (section 5) |
| A pending deployment | A one-off scheduled task, "FT: check evening mirror, then deploy 6.12", was due at 22:15 UK to upload the unchanged 7.5 after the evening review. Claude's attempt to switch it off was refused by the permission check; Tim switched it off at 21:59 UK. It never ran |

Merge, deployment and execution are separate here: PR #4 is merged; 7.5 was never deployed; 7.4 is what every scheduled run executes.

## 2. Verdict on each finding

Each was rebuilt independently (`repro_pr5.py`, not ChatGPT's script), on the frozen 16 Oct snapshot or the synthetic 20 to 27 Nov calendar. On 7.5, 14 of 18 cases show the defect (the other four are controls that should pass); on 7.6, none.

| # | Finding | Verdict | Evidence |
|---|---|---|---|
| 1 | Accept tonight's actual mirror | **Confirmed at the time; the data items are now corrected by tonight's mirror; scheduled-run acceptance unresolved** | Section 4 |
| 2 | A wrong-date event satisfies coverage | **Confirmed**, and extended | Coca-Cola's only event moved to 15 Jan 2027: 0 failures, ten-session total 4.8 instead of 6.0 points. Not raised: a duplicate event is counted twice (7.2 points) with 0 failures |
| 3 | `reorder` accepts hindsight | **Confirmed**, with one correction | Entered = effective = 16 Oct after the 16 Oct session was logged: +9.99 accepted, no warning, with or without a real change. `run` refuses the same (its test is `date >= eff`). Correction: no stored expectation is affected; the ledger holds no `expect` row yet |
| 4 | Missing or estimated 26 Nov London open uses 27 Nov's | **Confirmed**, and extended | 107,964.31 recorded with no warning against 107,318.25 with the real open (646.06 credits, synthetic prices). Not raised: the same for the sale leg (107,926.95) |
| 5 | Changes on 26 and 27 Nov collapsed | **Confirmed** | 108,359.20 against 107,104.45 by hand, leg by leg under the same no-26-Nov-reset assumption (Claude's figure, computed separately, equals ChatGPT's). Both STANDSTILL rows -0.614 and both described "UK One 50 to 20, UK Two 0 to 30" |
| 6 | Deadline validator wrong both ways | **Confirmed** | "Before 07:00 Thu 26 Nov" for a London 07:00 report on 27 Nov rejected (US calendar applied); "Any time Wed 28 Oct" and "After 07:00 Wed 28 Oct" accepted. Also accepted: "07:00 Wed 28 Oct" with no "before". Control: a US pre-open report on 27 Nov correctly needs 25 Nov |
| 7 | Integrity messages overstate coverage | **Confirmed**, one nuance | One-file manifest: "PASS sync: 1 files match". Every contribution row deleted, or one whole day's: "contributions add up". Bare "Implied move unavailable": no failure. Nuance: deleting a single holding's row on a day is caught, by the sum |

ChatGPT's release-record point also stands: part B, the state doc, the README and `last-sync.md` all name 7.4 as live, and that is true.

## 3. The fixes: pipeline 7.6 (branch `claude/pr5-fixes-2026-10-19`)

Narrow changes to `scripts/ft_pipeline.py` and `scripts/check_data.py`. The score, the confidence anchor, sizing, the panel, the scan's rules and every order are untouched.

- **Listing calendars (findings 4, 6).** `market_open(market, day)` with `LONDON_CLOSED` (empty: no UK bank holiday between 5 Oct and 27 Nov) and `US_CLOSED`. A leg filling on a non-benchmark day is priced at its own market's open that day when that market traded; a missing or estimated open there is a gap (PERFORMANCE INCOMPLETE) unless a fill price is stated; the next session's open is used only when the stock's market was shut (a US leg on 26 Nov). An unknown market with no row is a gap, never a guess. Markets come from `stocks.json`, kept in a new ledger `meta` row `listing_market` so a rebuild and the data check know them. The deadline check uses the stock's own calendar.
- **Successive changes (finding 5).** `fill_steps` and `legs_points`: several fills of one stock between two sessions are each priced at their own open, sales taken from the most recent purchase first. Each STANDSTILL change row compares the order it filled against the order it replaced, and is described that way.
- **Dated coverage (finding 2).** `results_coverage`: an event must be on the holding's own results date; another date covers it only if marked `confirmed` "uncertain" with a reason (`RESULTS UNCERTAIN`, a warning). A wrong date is `RESULTS MISSING` and a data-check FAIL; two future events are `RESULTS DUPLICATE`, a FAIL, and counted once in the total.
- **Prospective expectations (finding 3).** One test, `expectation_lock`, for `run` and `reorder`: locked if entered after the fill date, if the run's own session is on or after it, if a performance line or a benchmark row for the fill date is stored, or if `entered_time` on the fill date is at or after 07:00 UK. A same-day entry with no time is kept with a warning, so a 06:36 morning revision still works; the morning run doc now passes `entered_time`.
- **Deadlines (finding 6).** "Before 07:00 <Day> <D Mon>" or "by", "no later than": a time is required, at or before the cut-off; "after", "any time", "until" or no deadline word fails; a weekday that does not match the date fails.
- **Integrity (finding 7).** The manifest must list all six files; every stock held or traded in a session needs its own contribution row; an unavailable implied move must name the source tried and the date ("unavailable" or "not available"), else a FAIL inside five sessions; a stored implied move with no named source is a warning. No implied move is ever invented, and the 6% stays labelled an assumption.

### Tests and historical outputs

- Full suite: **148 pass** on the branch (94 on 7.5). 54 new tests in `tests/test_pr5_fixes.py`, each defect with a negative case and a positive control; expected figures by hand from prices.
- Changed tests, none weakened: the version checks (7.6); test 6b now states each stock's market (M2 needs it); a same-day restatement in `test_expect.py` carries its entry time; `test_event_date_differing_from_stock_text_warns` becomes `..._fails` (the warning became a failure, the point of finding 2).
- Frozen fixtures kept byte for byte. Added beside them: the 16 Oct state doc exactly as mirrored at `f9241ee`. The frozen `last-sync.md` left out the state doc line that the real mirror recorded; the test copy restores that line, and a test checks that the frozen record on its own now fails the stricter manifest check.
- 7.5 against 7.6 on the stored 16 Oct session (`compare_75_76_output.txt`): history, macro, panel, scores and stocks byte-identical; the ledger differs by one new row, `meta:listing_market`; the printout differs only in its version line. The performance log, every contribution and every STANDSTILL row rebuilt from scratch: identical. On tonight's mirror (`0d3c4e8`, data to 19 Oct): identical again, and equal to the stored log (101,096.51 at the 19 Oct close).

### Assumptions that remain

- How the FT fills a mixed London and US order entered before the 26 Nov cut-off, and whether it resets weights at the 26 Nov London close (M1 to M3 in `tests/test_calendar.py`). The synthetic tests show the code does what the assumptions say; they cannot show the FT works that way. Until FT help answers, the advice stands: prefer final-week changes that fill on 25 or 27 Nov.
- Lot order for a stock bought and sold within one interval (most recent purchase sold first) is a modelling choice; it only arises with two changes across 26 and 27 Nov.
- `LONDON_CLOSED` is empty by the 2026 UK bank holiday calendar (none from 5 Oct to 27 Nov).

## 4. Tonight's mirror (commit `0d3c4e8`, 22:01 UK)

Checked from the commit and its files, not from the run's message (which Claude cannot see).

| Check | Result |
|---|---|
| Seven held results events on the right dates | **Pass.** Coca-Cola 27 Oct, Microsoft 28 Oct, Shell and Eli Lilly 29 Oct, Exxon, Chevron and AbbVie 30 Oct, each equal to its stock's next-results date |
| Implied moves sourced, or absence explained | **Pass, with notes.** Five stored, each "(earnings-watcher, 16 Oct)"; Exxon and Shell "not available (earnings-watcher page failed, 19 Oct): counted at 6%", `implied_pct` null, so no 6% is stored as an estimate. Not verifiable from here: the page did not open for Claude tonight, and the figures carry 16 Oct, not tonight's date. Microsoft's 6.0% equals the assumed default; worth re-reading at the next review |
| Last orders follow 07:00 UK | **Pass** under both 7.5's and 7.6's stricter checks: Coca-Cola Mon 26 Oct; Shell, Lilly and Microsoft Wed 28 Oct; Exxon, Chevron and AbbVie Thu 29 Oct |
| Results-budget metadata | **Pass:** `meta:results_budget`, default 0.6, window 27 to 30 Oct at 1.0 |
| Top 2% observation with context | **Pass:** 16 Oct reading carries `top2_return_pct` 6.5 and the note naming ranks 187 and 324 from Tim's 18 Oct screenshots. Players kept at 13,918 for 16 Oct (13,966 was a later reading) |
| Hashes agree | **Pass:** all six files match `last-sync.md`; the five data files equal the artifact's published assets byte for byte (sha256 from the asset list); the state doc matches the Project copy on content checks (a byte hash of the Project copy is not readable here) |
| Integrity | **Pass:** GitHub `data-check` on the push succeeded (run 39324160616); locally 0 failures, 1 warning under 7.5 and 7.6 (Exxon and Shell implied moves unavailable, recorded with source and date) |
| Freshness | **Pass:** prices and performance to Mon 19 Oct, the latest closed US session; mirror 21:01 UTC. The scheduled `--fresh` run at 23:15 UTC (00:15 UK) had not run by this note |

**Scheduled-run acceptance stays open.** The scheduler records the evening review as **failed** ("usage limit reached") at 21:59 UK, yet the mirror commit came at 22:01 UK from the run's own steps (its sync record says "evening review"; no hand repair was made, by Claude or anyone visible). So the data were published and mirrored, but a clean scheduled execution is not shown. The state doc also says "about 22:15 UK", a time after its own commit. Claude did not repair anything by hand. The 24 Oct weekly mirror is a separate check.

Data notes, not faults: Eli Lilly's event still has the plan "Watchlist only" though it is held at 15%; stockanalysis.com refused eight pages and the run used Cboe's delayed quotes, a source not yet in part F.

## 5. The cut-off experiment: removed (playbook 6.11.1)

Applied in the live Project and on `main` (`9d90a16`); it does not wait for 7.6.

- Project `claude/ft-game-playbook.md`: version line; part C: "Until the FT or the test below settles it" now "Until the FT confirms it"; the test bullet replaced by "No cut-off test (removed 19 Oct at Tim's request ...)".
- Project `claude/ft-game-roadmap.md`: item 44 and "Still open".
- Project `claude/ft-game-state.md`: the 07:15 Coca-Cola sentence (section 2), the calendar line (section 7: now Coca-Cola's last order before 07:00 UK), open question 4, version lines (sections 1, 12), one review-log line (oldest dropped to keep 15).
- Repository: `docs/ft-game-playbook.md`, `docs/ft-game-roadmap.md`, `skills/ft-game-playbook/SKILL.md`, CHANGELOG 6.11.1, README. The repository's state doc stays as mirrored at `0d3c4e8` (the evidence for section 4); tomorrow's evening review mirrors the Project copy.
- Saved skill `ft-game-playbook`: one sentence names the test; an updated copy was offered to Tim to save (Claude cannot edit saved skills; the Project docs win meanwhile).
- No scheduled task prompt mentions the test; none was changed. The 06:36 morning check, the 07:00 UK cut-off and every order are unchanged.

## 6. Proposed release (needs Tim's approval)

- **Version:** playbook 6.12, pipeline 7.6 (in place of the planned 6.12 / 7.5, which should not be deployed).
- **Before deploying:** the 23:15 UTC data check passes; Tim approves; PR merged.
- **Steps:** (1) upload `scripts/ft_pipeline.py` from the merge commit as a new asset on the dashboard artifact, keeping the 7.4 asset; read it back and match the sha256; (2) the Project docs: part B (asset, hash, 7.6; 7.4 listed as kept), version line; part E, G3, G4, G7 and the evening, morning and page notes text from `main`, merged onto the live 6.11.1 docs so tonight's removal stays; (3) `files/app.js` from `main` (the 7.5 confidence wording, not otherwise changed by 7.6); (4) CHANGELOG 6.12, README, release text and repository description; (5) the next evening run is the first on 7.6: check its mirror and the data check the same way as tonight.
- **Rollback:** part B back to asset `30bd733ca18434b8f577f2d57c3813e3` (7.4, sha256 `5adc3093a10b57ead4c229d6d900c765967ba505a0578cf8262ac91f88b4055e`); `files/app.js` back to the 6.11 text (sha256 `0cb594a8...0d95`, in `f9241ee`). The `listing_market` meta row is ignored by 7.4 and the page, so data need no rollback.
- **Timing:** best before Sun 25 Oct, when the October results cluster is set. Nothing in October depends on 7.6's calendar work; finding 2's coverage check and finding 3's lock do matter from now on.
