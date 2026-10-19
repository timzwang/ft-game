# Independent review of Claude's completed improvement work, 19 October 2026

Reviewed main at d52dbcb6d7b8c4a336c37b7160b0902e3e934966, including merged PR #4 (merged 19 October at 20:41 UK), the three 19 October Claude handoffs, the latest ChatGPT handoff and review on still-open PR #3, current source, state, changelog, data and Actions logs. This review was completed before the first recreated evening task was due to publish.

## Assessment

Claude has made useful, substantive improvements and its principal test claims reproduce. All 94 tests pass locally and in the merge commit's GitHub Action. Its 17 calendar cases give exactly three failures against 7.4 and all pass against 7.5. A separate arithmetic reconstruction matches all six stored portfolio values to the penny, ending at 101,435.76 credits.

I would accept the frozen fixtures, clearer confidence wording, decision gate and portfolio-fit context. I would not treat the holiday-fill correction as complete, or a green data-check as proof that every earnings input and every file is correct. There are reproducible gaps below, including an after-the-event expectation accepted by the reorder command. None demonstrates that a past FT score was wrong.

The repository contains prepared pipeline 7.5. The recorded live release remains playbook 6.11 / pipeline 7.4, and a merge does not deploy to Claude. Deployment of 7.5 is **unverified**, not assumed from PR #4's merge.

## Findings, ordered by action priority

### 1. P1: complete and accept tonight's actual earnings-data mirror

The merge commit's [data-check run](https://github.com/timzwang/ft-game/actions/runs/39313136551) fails for the same reason as a local run: AbbVie's 30 October results event is absent. All six other held events have no implied move. Three last-order deadlines still say 08:00; the other three are absent. Adding only AbbVie makes integrity exit successfully, with the remaining problems merely warnings at the stored 16 October horizon. A green run alone is therefore insufficient acceptance tonight.

The state already identifies the required corrections. Acceptance means inspecting the new commit and its data: all seven correctly dated events; implied moves or meaningful recorded reasons for their absence; usable 07:00 deadlines; the results-budget metadata; the top-2% observation enrichment; and matching nightly hashes. The current ledger still lacks the results-budget meta row and the 6.5 top-2% value.

This is outstanding planned work at the review time, not evidence that tonight's task failed. The latest sync is explicitly a hand-run session at 19:58 UK, and market data still end on 16 October. The recreated evening task is due around 21:30 UK; weekly acceptance separately falls on 24 October. Do not convert a hand-run timestamp or a code-test pass into acceptance of either scheduled run.

Evidence: [state, including tonight's list](https://github.com/timzwang/ft-game/blob/d52dbcb6d7b8c4a336c37b7160b0902e3e934966/state/ft-game-state.md#L45), [last sync](https://github.com/timzwang/ft-game/blob/d52dbcb6d7b8c4a336c37b7160b0902e3e934966/state/last-sync.md#L3), and the Action above.

### 2. P1: the earnings invariant accepts an event on the wrong date

The missing-event function checks whether the stock has any future results event, not one matching its next-results date. The new checker warns on a mismatch but still prints that every holding has an event and exits successfully.

Reproduction: on a temporary copy with AbbVie added, move Coca-Cola's sole event from 27 October to 15 January 2027. Integrity has zero failures; the ten-session fallback exposure falls from 6.0 to 4.8 points and Coca-Cola disappears from that calculation. This defeats the promised dated coverage even though a warning is present. It is a remaining 7.3 detector gap exposed by the new 7.5 validation, not a new regression in historical prices.

Require matching stock/date coverage for confirmed held reports in the game horizon; route genuinely disputed dates to an explicit unresolved state. Test both wrong-date and duplicate-event cases.

Evidence: [missing_results_events](https://github.com/timzwang/ft-game/blob/d52dbcb6d7b8c4a336c37b7160b0902e3e934966/scripts/ft_pipeline.py#L2062), [date-mismatch handling](https://github.com/timzwang/ft-game/blob/d52dbcb6d7b8c4a336c37b7160b0902e3e934966/scripts/check_data.py#L315), reproduction held_event_on_wrong_date.

### 3. P1: the expected-benefit record can still accept hindsight

The 7.4 reorder command decides that a change has filled only if entered is strictly later than effective. Both fields are dates. On the fill date itself it permits an expectation even when the ledger already contains the completed performance session.

Reproduction: use the stored 16 October close and its existing order, submit effective = entered = 2026-10-16 through cmd_reorder with a new expectation of +9.99 points. The output ledger accepts it without warning, despite having that day's completed performance. No wall-clock ambiguity remains once the completed session is in the data. The normal evening run uses a different, stricter date test, so the two entry paths disagree.

Use completed-fill/session evidence, plus a real timestamp for same-day submissions, consistently across both commands. Preserve a legitimate pre-open morning update while refusing after-open or after-close rewrites. This is a weakness already present in 7.4, not introduced by PR #4. It undermines the assertion that every stored expectation is prospective.

Evidence: [reorder caller](https://github.com/timzwang/ft-game/blob/d52dbcb6d7b8c4a336c37b7160b0902e3e934966/scripts/ft_pipeline.py#L2900), [record_expectation](https://github.com/timzwang/ft-game/blob/d52dbcb6d7b8c4a336c37b7160b0902e3e934966/scripts/ft_pipeline.py#L634), reproduction same_day_after_close_expectation.

### 4. P2: 7.5 silently falls back to the wrong day's London open

The new fill_row correctly selects a real 26 November London open when present. If that row is missing, or marked open_obs=false, it silently selects the 27 November open instead. It cannot distinguish an unpriced London fill from a US market holiday.

Using Claude's synthetic calendar prices, the valid London change ends at 107,318.25 credits. Remove the new London holding's 26 November row, or mark its open unobserved: 7.5 records 107,964.31, with no warning and no incomplete-performance marker. The synthetic difference is 646.06 credits; it is not a claim about the current real portfolio.

The missing-row case should wait for the actual fill, or an explicit supported fill price. The holiday fallback must depend on the listing's market calendar rather than absence of a quote. Add both negative tests before relying on 7.5 for 26 November. This is an incomplete fix of the older calendar defect, not proof that ordinary October provenance checks regressed.

Evidence: [fill_row](https://github.com/timzwang/ft-game/blob/d52dbcb6d7b8c4a336c37b7160b0902e3e934966/scripts/ft_pipeline.py#L704), [valuation caller](https://github.com/timzwang/ft-game/blob/d52dbcb6d7b8c4a336c37b7160b0902e3e934966/scripts/ft_pipeline.py#L762), reproductions missing_26_open and imputed_26_open.

### 5. P2: two London changes across 26 and 27 November are collapsed

fill_days keeps only the latest effective row per name between benchmark sessions. Performance compares the 25 November weights directly with the 27 November weights. It loses intermediate trades if the same name changes on both days. STANDSTILL also maps both decisions to the same before/after orders.

Reproduction: extend the calendar fixture's 26 November UK One 50 to 30 / UK Two 0 to 20 change with another on 27 November to 20 / 30. Source gives 108,359.20 credits; pricing the two sets of legs separately under the same no-26-Nov-reset assumption gives 107,104.45. Both STANDSTILL decisions receive the identical combined -0.614-point result and identical descriptions.

Preserve each fill separately and judge each decision against the order it actually replaces. A documented operational restriction on changes for those dates could reduce exposure until corrected, but should not be presented as a mathematical fix. The FT's mixed-market fill/reset rules still require confirmation, as Claude correctly labels in M1 to M3.

Evidence: [fill_days](https://github.com/timzwang/ft-game/blob/d52dbcb6d7b8c4a336c37b7160b0902e3e934966/scripts/ft_pipeline.py#L692), [STANDSTILL mapping](https://github.com/timzwang/ft-game/blob/d52dbcb6d7b8c4a336c37b7160b0902e3e934966/scripts/ft_pipeline.py#L1867), reproduction changes_on_both_26_and_27.

### 6. P2: the new deadline validator both rejects and accepts the wrong cases

The London holiday false alarm Claude asked ChatGPT to check is real. A London report at 07:00 on Friday 27 November with a last order before 07:00 Thursday 26 November is rejected as needing Wednesday 25 November, because the helper applies the US holiday calendar to every stock.

Conversely, “Any time Wed 28 Oct” and “After 07:00 Wed 28 Oct” are accepted for an after-close 28 October report. A readable date and absence of a time later than 07:00 do not establish a valid before-cut-off deadline.

Use the stock's relevant market/session calendar and require a readable deadline with an explicit before/no-later-than meaning. Retain conservative guidance as guidance, rather than making an assumed US calendar a hard data failure for London.

Evidence: [deadline parser](https://github.com/timzwang/ft-game/blob/d52dbcb6d7b8c4a336c37b7160b0902e3e934966/scripts/check_data.py#L68), reproduction last_order_parser.

### 7. P2: some data-integrity success messages overstate coverage

Two independent temporary-copy checks return zero failures after AbbVie's event is supplied:

- Replace last-sync's six-file list with only a correct stocks.json hash: “PASS sync: 1 files match”. The other five required files are never required to appear.
- Delete every contrib row, rewrite the hash honestly: “PASS performance ... contributions add up”. The sum is checked only for dates that have contribution rows.

Also, the new “unavailable with a reason” policy is implemented as a substring test. A bare “Implied move unavailable”, with no reason, avoids the near-term missing-move failure. This is not a reason to invent a market estimate; retain transparent unavailable states and validate their explanation.

Require all five datasets and the state doc in the manifest, require the expected contribution coverage, and validate a non-empty reason. Recalculation using the pipeline is useful for detecting changed inputs, but cannot independently detect a valuation bug shared with that pipeline. The separate arithmetic check in this review addresses the stored October sessions only.

Evidence: [contribution check](https://github.com/timzwang/ft-game/blob/d52dbcb6d7b8c4a336c37b7160b0902e3e934966/scripts/check_data.py#L266), [absence check](https://github.com/timzwang/ft-game/blob/d52dbcb6d7b8c4a336c37b7160b0902e3e934966/scripts/check_data.py#L329), [manifest check](https://github.com/timzwang/ft-game/blob/d52dbcb6d7b8c4a336c37b7160b0902e3e934966/scripts/check_data.py#L355), reproductions in the evidence.

## What Claude implemented successfully

| Requested area | Independent result |
|---|---|
| UK/US calendar | The three stated 7.4 failures reproduce; 17 of 17 supplied cases pass on 7.5. Remaining cases are findings 4 to 6 above. M1 to M3 are labelled assumptions, as requested. |
| Confidence | Source banner no longer hides itself at 150; the anchor tooltip and rules explicitly reject a probability reading. The 47-shadow-rating, two-overlapping-window calculation reproduces: Brier about 0.250, date-level rank correlations -0.03 and +0.01. This supports caution, not proof the score is useless. |
| Changes earning their place | The qualitative four-question gate is in the rules. Per-change attribution and first-order buy-and-hold figures reproduce. The +0.115 / -0.325 daily-reset comparisons and -0.024 / -0.511 buy-and-hold comparisons use different counterfactuals; that difference is explained, not a contradiction. The same-day expectation hole remains. |
| Scanner concentration | Portfolio-fit printouts and the assumed-6% wording are present. The 7.4/7.5 rerun has identical output datasets and ledger rows. Correlation context is descriptive, not a diversification guarantee; the existing 45% theme guide still permits a 5-point energy addition from 40%. |
| Post-game report | A useful plan exists, including attribution, snapshots, final screenshots, truncated windows and a future build script. It is a plan, not a completed reporting feature. Preserve price history for departed names; earlier handoffs acknowledge 14 shadow settlements cannot currently be reconstructed. |
| Test/data separation | Frozen compressed fixtures genuinely decouple code regression tests from nightly mutable data. Tests still deliberately detect the known AbbVie gap in the old snapshot; the live data checker has no AbbVie exception. |

## Release and workflow evidence

- [Merge tests](https://github.com/timzwang/ft-game/actions/runs/39313136426): success, 94 passed, page syntax success. Local Python 3.13 on Windows also passes 94; GitHub used Python 3.12 on Ubuntu.
- [Merge data-check](https://github.com/timzwang/ft-game/actions/runs/39313136551): failure on AbbVie, with implied-move and deadline warnings. No scheduled freshness acceptance was yet visible at the review time.
- 7.4 against 7.5 on the stored 16 October inputs: history, macro, panel, scores and stocks are byte-identical; the two generated ledgers both have 542 rows with no row differences. Source changes only the stated extra printouts on that input.
- 72 downloaded blobs, including production data, scripts, tests and frozen fixtures, were verified against GitHub's Git blob hashes. This is a pinned review of main, not an assessment based on the older local mirror.
- The repository's 7.5 script SHA-256 is 244a8af943f9efe36380ff4c3713a370b8358979b63e56ebcdd9aefbca29346f. Part B and last-sync still identify live 7.4 as 5adc3093a10b57ead4c229d6d900c765967ba505a0578cf8262ac91f88b4055e. The current release record therefore does not substantiate deployment of 7.5 or of the page/doc edits.
- The data-check schedule intentionally follows the Sun-to-Thu evening reviews and Saturday weekly review. It does not itself prove the recreated Claude tasks can mirror. The main branch is reported unprotected by GitHub, so a red data check is a signal, not a merge block.

## Recommended sequence

1. Accept the actual 19 October mirror from commits and files, then separately accept the 24 October weekly mirror. Read warnings as well as the exit code.
2. Make dated held-event coverage and the prospective expectation lock reliable. Keep the score, anchor and sizing unchanged.
3. Correct or explicitly fence the remaining holiday cases before any final-week order depends on them; reconcile the actual FT mixed-market rules.
4. By the 25 October review, record one joint plan for the seven-stock results cluster and decide whether to move/drop the 26 October 07:15 cut-off experiment. The experiment is still present in the recorded operating instructions. No trade change is proposed here.
5. Record an explicit merge-versus-deployment handoff with the final asset/hash and page/doc state once Claude applies any approved release.

There is no basis here to declare the FT age/subscription terms resolved: the prior ChatGPT citation was disputed, and the official terms have not been independently retrieved in this review. No inference about the entrant's eligibility is made.

## Reproducible evidence and limits

The adjacent evidence folder contains review_checks.py, results.json and validation.txt. Run review_checks.py with --repo pointing to a checkout of the pinned commit; pytest is needed because it imports the synthetic calendar fixture. It writes only temporary copies unless --out is explicitly supplied. The JSON records both successful controls and observed defects, so script completion does not mean the defects are fixed.

This session had direct access to GitHub and local copies, not Claude's current artifact, Project documents or scheduler. Claude's statements about those surfaces remain reported claims. No workflow was dispatched or rerun. No live order, game, source, data, page, task or main branch was changed by this review; only this review and its handoff are proposed through a separate PR.
