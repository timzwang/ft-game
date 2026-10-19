# FT Stock Picking Game: 19 October follow-up review

Review of repository `timzwang/ft-game` at main commit `5af524f4ba28b726077aaf8ce679154778051d25`, Monday 19 October 2026 around midday UK. Read-only assessment of the live main files. The only repository writes are this proposal and the required handoff note on a separate ChatGPT branch and pull request. No changes to the live Claude artifact, orders, tasks, data, code, or main.

## Verified progress since the 18 October review

- Playbook 6.10 and pipeline 7.3 are present in source and documentation: exact-session confidence and shadow settlement, scan settlement fixes, missing-results warning, FT observation enrichment, results-budget override, a US Thanksgiving/final-day calendar and persisted provenance and closed-market data.
- Forty regression cases are documented under `tests/`. The new tests workflow succeeded on commit `e999cfe3f3170dee283757cfffc009104d479abf`: https://github.com/timzwang/ft-game/actions/runs/39176413134. This is a genuine first green CI run, not proof that future nightly data updates are sound.
- The scan workflow is main-only, the page has the event-date budget rule, and the roadmap no longer claims that top-five and overbought tests have been built.
- The branch contains the mirror of source and saved data, not a direct view into Claude's running tasks or dashboard artifact. Deployment statements in the handoff remain reported statements.

## P0: immediate operational checks

1. **19 October evening acceptance:** check that the next evening review actually updates `data/`, `state/ft-game-state.md`, `state/last-sync.md` and its hashes. The latest published data, report and scan currently end on 16 October. This is correct at Monday midday; the first real recreated nightly run has not yet occurred. The Saturday 24 October weekly task needs its own acceptance check.
2. **Complete the earnings inputs:** all seven currently held names have results dated 27 to 30 October and together comprise 100% of the current allocation. The stored ledger has six of those events but **no AbbVie event**, although a 7.3 warning now detects it. As of this snapshot, **zero of the seven held results events contains an options-implied percentage**. The state already instructs the 19 October review to add AbbVie, source the seven implied moves, confirm estimated timestamps and replace the lingering 08:00 deadlines with the current 07:00 UK precaution. Also enrich the stored 16 October FT observation with the approximate top-2% line. Inspect the resulting data, not just the review's message.
3. **Decision calendar:** by Sunday 25 October evening, record a specific hold/trim/exit stance for each of the seven reports, including the last actionable order. Coca-Cola's pre-open 27 October release makes Monday 26 October's early cut-off decisive. Do not let the 07:15 cut-off experiment accidentally replace or undo the entire Coca-Cola weight in the full portfolio order.

## P1: small, worthwhile improvements

4. **Add a nightly data-integrity gate.** `.github/workflows/tests.yml` runs on code, scanner configuration and page changes, but excludes ordinary `data/**` commits. Add a cheap, independent post-mirror check, or extend CI paths if affordable, checking freshness, sha256 manifest correspondence, unique ledger identities, weighted position sum, monotonic settled sessions, no performance gaps, and exact-dated results events for held names. Distinguish failed validation from a stale but previously passing run.
5. **Tighten the permissive calendar regression.** `tests/test_pipeline.py:test_stored_holdings_results_events` currently permits `missing <= {AbbVie}` on actual stored data. This was a reasonable transition fixture, but after the evening adds the event it should assert *no missing held results events*, with a date-horizon rule so stale far-future estimates do not cause false alarms. Also verify the new `results_budget` meta row actually appears in the published ledger.
6. **Assess earnings risk jointly, not only by per-stock budget.** The 1.0-point event ceiling is a policy reference, not an enforceable worst-case loss. Current risk is concentrated: 40% energy, including a very correlated Exxon/Chevron pair. The printed fallback 6.0-point aggregate exposure is the sum of weight times assumed moves, not a maximum or an expected loss. Add a one-page downside scenario for correlated negative reactions and a plan for what to do if the stock gaps beyond the cap.
7. **Make the scan freshness decision explicit before 2 November.** A successful scheduled Action can produce no newly scanned session. The evening review should say whether it used the latest, prior-session, forced or unavailable scan, and should never block order publication on GitHub queue timings.
8. **Check game eligibility for any personal CV claim.** The FT's 21 September 2026 public statement specifies 18+ and an active FT subscription for entrants (https://bsky.app/profile/financialtimes.com/post/3mvzn64izqx2k). Verify the named entrant is eligible. Project-building and analytical work can still be described accurately regardless, but an account's official placing should not be attributed to a different person.

## Investment assessment

The latest confirmed FT reading is for **Friday 16 October**: 101,402 credits, +1.40%, rank 3,269 of 13,918 (top 23.5%). The top-2% return inferred from a pair of published portfolios was about +6.5% on 18 October and is not a live, exact threshold. The estimated model value was 101,435.76, a 33.76-credit difference.

The system has earned confidence for basic reproducible accounting, not yet for signal alpha. Cumulative changes added +0.12 points against the inception portfolio as actually entered (and lost 0.33 versus the same initial names fully invested). The historical price-only panel rank correlation is +0.042 (t +1.1) on 49 overlapping measurement dates, no reliable positive edge. Most of the outperformance to date comes from energy exposure. Do not treat uncalibrated confidence 57-60 as observed win probabilities.

Recommended approach: retain the frozen 40/20/20/20 score for continuity; use a lightweight pre-decision record for every change (timestamp, thesis, expected five-session benefit, invalidation, next-open price, comparator and five-session follow-up), keep simple inception, previous-order and S&P baselines, and focus the remaining game on source freshness, dated catalysts, execution, concentration and weekly rank. Do not build the deferred top-five panel, overbought split or new predictive model during the game.

## Dates and acceptance evidence

- **19 Oct after evening review:** new file commits and hashes, seven earnings events (including AbbVie), implied-move inputs or transparent unavailable flags, results-budget meta, enriched FT threshold.
- **24-26 Oct:** weekly mirror accepted, earnings actions locked in by 25 Oct, cut-off test executes only as an intentional full-weight order on 26 Oct.
- **2 Nov:** late scan fallback verified against actual Action queue timings.
- **13 Nov onward:** rank stance from an updated FT reading, not the 16 October snapshot or SPY alone.
- **26-28 Nov:** reconcile the US holiday, early Friday close, London-specific fills and final FT ranking; avoid claiming results for windows extending beyond the game.

No order changes, score adjustments or code deployments are recommended without Tim's explicit approval.
