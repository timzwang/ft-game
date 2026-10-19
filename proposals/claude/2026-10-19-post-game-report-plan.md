# Post-game research report: outline, data to capture, reproducibility plan

Claude, Mon 19 Oct 2026 evening, for Tim (review brief, priority E). A plan, not the report: the report is written after the final weekly review of Sat 28 Nov, from the files listed here. Nothing below claims a result.

## Ground rules for the final report

- Every figure comes from a file in this repository at a named commit, or from Tim's FT readings stored in the ledger (`reported` rows). No figure is typed by hand.
- Each claim says which of four kinds it is: **measured** (from stored prices and the game's arithmetic), **reported** (Tim's FT reading), **judgement** (a decision or rating made at the time), **assumption** (a modelling choice the FT has not confirmed, such as the 26 Nov fill split).
- Attribution is explicit, per section:
  - **Tim**: the objective, the rules he set or approved (fully invested on 12 Oct, the 1.0 results budget, the frozen score, the cut-off precaution, the GitHub mirror and the Claude/ChatGPT handoff), every order he entered, and every approval. Ideas he proposed (momentum after bank upgrades, macro checks, the dashboard design) are his.
  - **Claude**: the pipeline, scan, data check, tests, page and procedure docs, the nightly reviews and recommendations.
  - **ChatGPT**: the independent reviews (16, 17, 18 and 19 Oct) and the findings each one produced.
  - **Tested independently**: what one assistant built and the other verified, with the commit and test output.
- Statistical honesty: this entry spans 35 US sessions (9 Oct fill to 27 Nov). With overlapping five-session windows and correlated stocks, almost no signal test can reach significance. Report effect sizes with their sample sizes and distinct dates, and say "inconclusive" where that is the answer.
- Eligibility and placing: quote the FT rank exactly as the game showed it, with the date read. Before using the placing on a CV or application, Tim reads the game's own terms page and confirms the entry meets them. The state doc records the entry as "for FT subscribers aged 18 and over", which this review could not verify (ChatGPT's cited FT post does not state an age). If the terms are not met, describe the project and its measured results, not an official placing.

## Outline

**A. Objective.** The game's rules (part C of the playbook, with sources), 5 Oct to 27 Nov, 100,000 virtual credits, 5 to 20 stocks at 5% to 25%, cash to 25%, fills at the next open, weights reset at each close. Target: roughly the top 2% (rank line from `reported.players`), not first place. Constraints Tim set.

**B. System architecture.** One diagram: scheduled Claude runs (evening, morning, refreshes, weekly, weekend) reading the Project docs; the pipeline (`scripts/ft_pipeline.py`, standard library only) producing four data files; the dashboard artifact; the GitHub mirror with the broad scan (Actions), the regression tests and the data check; the handoff log. Version history from `CHANGELOG.md` (6.0 to the final version) with dates.

**C. Investment method.** The frozen 40/20/20/20 score; strength bands; news momentum and earnings drift rules; results budget; concentration and volatility caps; the macro backdrop; the day call (labelled research only); confidence ratings and why they are not probabilities; the trade decision gate (if approved).

**D. Validation method.** The panel test (rule fixed 15 Oct before data was seen); shadow ratings; confidence settlement on exact sessions (7.3); the drift record; the STANDSTILL and inception counterfactuals; the expected-benefit record (7.4); RECONCILE against FT readings; the regression suite and data check. For each: what it can and cannot show.

**E. Results.** Final estimated value and FT value (RECONCILE gap), FT rank and percentile with the date read, gap to the top 2% line over time, return against SPY, maximum drawdown of the estimate, contribution by holding and by theme (weight times return), the effect of every change (STANDSTILL rows), changes against the first order (inception rows, as entered and fully invested), turnover.

**F. Critical evaluation.** What worked, what did not, what is inconclusive. Known biases: the panel's survivorship (large today), overlapping windows, one market regime (an oil shock and a chip sell-off), decisions made by an AI with a human approving, multiple testing across many indicators.

**G. Engineering lessons.** Price provenance (7.2), exact-session settlement (7.3), the results-event gap (AbbVie), scheduled runs without repository access (6.8 to 6.9), tests coupled to live data (fixed 19 Oct evening), the calendar edge (26 Nov), cross-assistant review as a control.

**H. Future research.** A longer live panel test; calibrating ratings with non-overlapping windows over months; a cost-free turnover study; testing the judgement points separately.

## Data to capture from now until 27 November

| What | Where it lands | Who | When | Status on 19 Oct |
|---|---|---|---|---|
| FT value, rank, players, read after the US close | `reported` rows via the next run | Tim supplies, run stores | every Friday at least; also 26 Nov and 27 Nov | 16 Oct stored |
| Return of the player on the top 2% line (and the rank of that line) | `reported.value` (`top2_return_pct`) | Tim | every weekend | 16 Oct: about +6.5%, waiting to be attached by tonight's review |
| Screenshot of the final leaderboard page and the portfolio page | `proposals/claude/final/` (images) | Tim | 27 Nov after 18:15 UK, and 28 Nov | not started |
| Every order as entered, with entry time and the fill the game shows | `trade`/`position` rows, state doc section 3 | Tim confirms, run records | each change | done to 19 Oct |
| The decision record for each change (gate answers, `pts`, invalidation) | `expect` rows | evening review | before each fill | from 19 Oct |
| Changes considered and rejected, with the reason | state doc review log line | evening review | each evening | ad hoc so far |
| Nightly data snapshot | `data/` at each mirror commit | G6 | every evening and Saturday | first real run tonight |
| Prices for every stock ever held, to 27 Nov | `history.json` (`extra_history` for those off the list) | evening and weekly reviews | each session | RTX, LMT, NVDA, TSM via the template |
| Panel closes to 27 Nov | `panel.json` | weekly review | Saturdays | 28 of 30 members |
| Scan records | `scan/record.csv` | Actions | each session | from 16 Oct |
| Data-check results | Actions run history (export the list on 28 Nov: Actions logs expire) | Claude, by hand | 28 Nov | from tonight |
| Version history | `CHANGELOG.md`, tags | sessions with Tim | each version | 6.0 to 6.11 |
| Handoff notes and reviews | `handoff/`, `proposals/` | both assistants | each session | complete |

Two things the system does not keep and the report needs: an end-of-game export of the GitHub Actions run list (logs expire after 90 days), and Tim's screenshots of the final FT pages. Both are by hand on 27 and 28 Nov.

## Reproducibility plan

1. Tag the final state: `v-final` on the commit of the 28 Nov weekly mirror. Record its sha256 manifest (`state/last-sync.md`).
2. One script, `report/build.py` (written after the game, standard library only, reading only `data/` at the tag), produces every table and figure in sections E and F, writing them to `report/out/`. It reuses the pipeline's functions where they exist (`update_performance`, `standstill_rows`, `panel_stats`) and asserts that its recalculated values match the stored ones to the cent, as `scripts/check_data.py` does.
3. The frozen-snapshot test pattern (tests/fixtures) is applied to the final data: a test asserts the report's headline figures, so a later change cannot silently move them.
4. Windows that run past 27 Nov (confidence ratings, standstill rows, drift entries) are reported as truncated with their session count, never as complete.
5. The report states the commit, the pipeline version and the Python version used to build it, and anyone with the repository can rebuild it with one command.
