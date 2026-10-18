# FT Stock Picking Game: repository review, 18 October 2026

Reviewed main at `25e8a93e52a956e4ca43f3544ddf77f2178d4a61`: playbook 6.9, pipeline 7.2, data published after the 18 October evening review, prices through 16 October. Review by ChatGPT, about 23:35 to 23:55 UK. Findings and recommendations only; Tim has not approved implementation.

The system has become a useful decision and risk process. Its accounting is reproducible, the recent corrections are substantive, and the evidence is much more candid. There is still no demonstrated stock-selection or trading edge. The best use of the remaining 29 US sessions is to make earnings decisions deliberate, keep the operational chain dependable and measure the existing process correctly. Extra indicators and a larger forecasting system have little prospect of earning their cost before 27 November.

## Scope and handoff

Read first: `handoff/README.md` and all four 18 October Claude notes, including the newest `-4` note. There is no ChatGPT handoff note on main or the only existing ChatGPT branch, `chatgpt/connection-test`; its sole PR is the merged connection test. Also read the earlier ChatGPT strategy proposal and Claude's audit verification and evidence. The linked ChatGPT conversation provided only the original review request, not a retrievable substantive answer.

Checked those claims against CHANGELOG, the state and sync records, current scripts, scanner configuration and workflow, dashboard source, playbook and run instructions, scheduled-task copy, JSON data, recent commits, branches, PRs and Actions history. These are the current repository files, not direct access to Claude's runtime. A note saying that a live deployment or task change happened remains a reported fact unless the repository offers independent evidence.

No live artifact, account, task or main branch was changed. Validation ran against a separate local snapshot with temporary outputs. No GitHub workflow was dispatched. This proposal and its evidence are the review deliverables.

## What works, and what is actually implemented

| Feature | Evidence and review result |
|---|---|
| Weighted performance, contributions and FT reconciliation | Full reconstruction of all six stored sessions matches exactly: 101,435.76 credits, +1.436%; FT closing figure 101,402, a 33.76-credit gap. See `scripts/ft_pipeline.py:572`, `:1839`, `:2790`, and evidence `complete_performance_rebuild`. |
| Corrected standstill controls, pipeline 7.1 | Reproduced: 12 October rebuild -0.748 points; inception as entered +0.115; inception fully invested -0.325; week of 12 October +0.115. The baseline before Monday's fill is present. `scripts/ft_pipeline.py:1652`, `:1700`, `:1731`. |
| Price integrity, pipeline 7.2 | A missing XOM row stops performance before 14 October; adding it resumes through 16 October. A missing open is marked and rejected for fills; drift with no tradable next open becomes n/a. `scripts/ft_pipeline.py:235`, `:618`, `:1539`, `:1576`. See qualifications below. |
| Holiday escape | Tested: an unchanged holding can be carried at zero on an explicitly closed market; the same exemption does not allow a trade without a price. `scripts/ft_pipeline.py:609`. Stopping at the first gap is correct for a chained portfolio value. |
| Broad scan | Present and working on complete synthetic US and UK fixtures: Leaders and Events produced, repeat run does not duplicate the record. Stored live run measured 867/868 on 16 October, no stale rows or recent holes, 30 Leaders and zero Events. `scan/scan.py:369`, `:504`; `scan/latest.json:1`. |
| Real Actions execution | 12 runs retrieved: 10 success, one failure, one cancelled. The latest two successful scheduled runs skipped the already scanned session. The last full scan was the forced 16 October run. Success therefore proves execution, not a fresh scan result. |
| Earnings drift and results totals | Six-test classifier, next-open settlement, n/a timeout, per-event output and five/ten-session totals exist. No drift cases are stored yet, so its real-world discovery and settlement chain is untested. `scripts/ft_pipeline.py:1468`, `:1549`, `:1809`. |
| Panel and judgement tests | Reproduced panel: 28/30 sufficiently loaded, 49 history dates, average rank correlation +0.042, t +1.1, no live windows. Shadow records store the two score parts; JUDGEMENT TEST exists, with no settled dates carrying those parts yet. `scripts/ft_pipeline.py:1218`, `:1337`, `:1856`. |
| Risk, macro, crypto and day call | Code and stored tables exist; present portfolio energy risk is about 54%, against 40% weight. The day call remains research only under the rules; index record 1/4, equal to always-green. `scripts/ft_pipeline.py:703`; `docs/ft-game-rules.md:100`; `state/ft-game-state.md:20`, `:45`. |
| Cut-off and dashboard | Current dashboard CUTOFF is 07:00; US opening time handles the October mismatch week. JavaScript syntax check passes. Source inspection does not establish visual correctness or live rendering. `page/app.js:146`. |
| Mirror repair, playbook 6.9 | History, ledger, stocks, macro and panel hashes match last-sync; pipeline matches the playbook hash; state matches the newer hash in last-sync's prose. The hand-run catch-up and actual one-off push `8d9ed20` are visible. The real recreated evening/weekly jobs have not yet supplied a nightly mirror. |

The other two claimed research additions remain absent: the top-five panel/portfolio comparison with bootstrap interval (roadmap 39 and parts of 38/40), and the overbought split of shadow outcomes (roadmap 42). This was already conceded in Claude's first handoff and audit. It is still not corrected in the roadmap. Source: `docs/ft-game-roadmap.md:78`, `:84`, `:87`; `proposals/claude/2026-10-18-audit-verification.md:345`. I would correct the claims and defer substantial implementation until after the game.

## Findings in priority order

### 1. P1: AbbVie's earnings are absent from the actual risk calendar

All seven current holdings have results dated 27 to 30 October in the state/stock records. AbbVie is 10%, but there is no corresponding results event in the ledger. The aggregate function and dashboard read events, not the stock's free-text next-results field. Consequently AbbVie disappears from both views.

Reproduction using the current order and the 16 October session date: ten-session risk is 5.40 points across six reports; adding the state doc's 30 October AbbVie event gives 6.00 across seven. These figures use the documented 6% fallback, not options quotes or a forecast loss. The statement that AbbVie is simply outside the window is wrong.

Evidence: `state/ft-game-state.md:38`, `:46`; `scripts/ft_pipeline.py:1809`; `page/app.js:83`; `data/ledger.json:1`; evidence `missing_abbvie_event`.

Next action: confirm the date/time from company investor relations, add the event in a normal authorised Claude run, obtain implied moves or disclose the fallback for every holding, and make hold/trim/exit decisions with explicit last-order times. Add a completeness check that every holding's upcoming results has a dated event. The October cluster needs decisions before it needs more dashboard features.

### 2. P1: confidence settlement still accepts invented opens and different windows

`resolve_confidence` takes the first five available stock rows after the effective date, independently of the first five benchmark rows. It never calls `real_open`.

Synthetic reproduction: remove the stock's 19 October entry row; the function scores 20 to 26 October against the benchmark's 19 to 23 October, labels the result 23 October and awards a win. With a present entry row marked `open_obs: false`, it still scores the placeholder open. Thus 7.2's fill protection covers portfolio performance and drift but does not cover confidence calibration.

Evidence: `scripts/ft_pipeline.py:645`, especially `:653` and `:659`; evidence `confidence_missing_entry_session`, `confidence_imputed_entry_open`.

Next action: define one benchmark session window, require the exact stock entry open and end close, apply open provenance checks, and time out missing cases as n/a with a reason. This is a demonstrated failure mode, not evidence that the 11 currently resolved ratings are wrong.

### 3. P2: shadow and scanner outcomes can silently move their horizons

Shadow settlement allows a missing exact end-date close when a later row exists. With 26 October missing but 27 October present, it uses the 23 October close and labels the result 26 October. The scanner uses positional stock rows: deleting 20 October moves entry from 20 to 21 October and the fifth-session end from 26 to 27 October.

Evidence: `scripts/ft_pipeline.py:1235`; `scan/scan.py:435`, especially `:445` and `:452`; evidence `shadow_missing_end_session`, `scan_missing_session`.

Next action: anchor both to benchmark session dates and require the precise entry and end rows. Keep shadow's current close-based ranking test clearly labelled; if a tradable version is added, store next-open results alongside it and benchmark both over identical dates. A close-based predictive test can be useful, but it is not an attainable trading return.

### 4. P1 operational check: the actual scheduled mirror still needs acceptance

Claude's newest note explicitly retracts the 6.8 access conclusion for the real tasks. The current data is caught up by hand; a newly attached one-off job really pushed. That is stronger evidence than a dry run, but it does not complete the real evening/weekly acceptance test.

Evidence: `handoff/2026-10-18-claude-4.md:7`; `CHANGELOG.md:9`; `state/last-sync.md:3`; `ops/scheduled-tasks.md:20`.

Next action: inspect the Monday 19 October nightly commit and last-sync against that run's published files, then the Saturday 24 October weekly run. A successful Claude session without an updated mirror is a partial failure. Report freshness and affected stage, not simply job success. No monitor or task was created in this review.

From 2 November the useful scan slot is 21:20 UTC and the evening review starts 21:30 UK, leaving ten minutes before the review even begins. Historical Actions runs started about 26 minutes late on 16 October relative to that revision's 20:10/21:05 cron slots. Queueing plus download time makes same-session availability uncertain. G7 can force and wait ten minutes, then use the previous session when allowed. Agree a non-blocking freshness policy before 2 November; do not depend on a precisely timed GitHub start.

Evidence: `.github/workflows/scan.yml:12`; `docs/ft-game-data.md:155`; [first scheduled run](https://github.com/timzwang/ft-game/actions/runs/38963490871); [second scheduled run](https://github.com/timzwang/ft-game/actions/runs/38969990868); old workflow at `9bd42e3`.

### 5. P2: the new top-2% observation cannot update its existing reported row

The state explicitly asks the next review to store `top2_return_pct: 6.5` on the existing 16 October FT reading. The deduplication key is just date, value and rank. Resubmitting those with the added threshold is discarded; stored `value` remains null. The full local template/run reproduction confirms it.

Evidence: `state/ft-game-state.md:17`; `scripts/ft_pipeline.py:2143`; evidence `top2_existing_report_update`.

Next action: update allowed fields on an existing matching observation, keeping source time and provenance. Show the gap to the latest threshold, its age and uncertainty. The +6.5% line is a rough estimate bracketed by two portfolios, not an exact stationary target. The actual objective is beating roughly 98% of players, not beating SPY.

### 6. P2: final-day timing is documented correctly but not encoded consistently

The playbook correctly says US markets close on Thanksgiving and close at 18:00 UK on 27 November. The US-close helper nevertheless returns 21:00 for 27 November; it will incorrectly label a final FT reading between 18:00 and 21:00 as pre-close. The page's expected-session function assumes every weekday becomes final at 21:15, and `next_weekday` does not exclude Thanksgiving. The scan also assumes 16:15 New York finality even on a half-day, delaying the final result rather than recognising the early close.

Evidence: `docs/ft-game-playbook.md:79`; `scripts/ft_pipeline.py:1140`, `:1828`; `page/app.js:138`; `scan/scan.py:482`; evidence `us_close_27_nov`.

Next action: one explicit game-window session calendar, tested for 26 to 30 October, 2 November, Thanksgiving and the final half-day. Decide how London-only 26 November and final valuations are represented. Plan the final Friday capture and Saturday reconciliation. The weekly prompt already explicitly keeps 28 November as the final review (`ops/scheduled-tasks.md:89`), which is correct; verify that it captures the final early-close prices and FT result.

The half-day and holiday are independently confirmed by [NYSE's calendar](https://www.nyse.com/trade/hours-calendars) and [Nasdaq's calendar](https://www.nasdaqtrader.com/trader.aspx?id=Calendar). UK clocks change on 25 October per [GOV.UK](https://www.gov.uk/when-do-the-clocks-change). These external checks confirm exchange/time facts, not the FT's unresolved order cut-off.

### 7. P2: provenance can be lost when a stored row is re-imported

`merge_history` infers provenance only from whether the input open is null. Passing back a stored row that contains numeric open 105 and `open_obs: false` removes the flag; `real_open` then returns true. Reproduced with non-zero volume. No occurrence in the current game ledger was established.

Evidence: `scripts/ft_pipeline.py:246`, `:259`; evidence `provenance_round_trip`.

Next action: preserve explicit provenance and make provenance-only changes trigger dependent recalculation. Also retain closed-market explanations for historical rebuilds: `market_closed` currently arrives only in today's input and is not stored as a durable calendar fact. Do not allow the escape to suppress a genuinely missing quote.

### 8. P2: manual workflow dispatch can carry a branch into main

The scanner workflow permits manual dispatch on a selected branch, checks out that branch by default and eventually runs `git push origin HEAD:main`. After a successful rebase, this can publish the dispatched branch's commits to main. Main is currently unprotected. This matters especially when ChatGPT branches are meant to remain proposals.

Evidence: `.github/workflows/scan.yml:17`, `:35`, `:57`; repository main-branch API returned `protected: false`.

Next action: require main as the execution ref and constrain the write-back path; discuss branch protection compatible with the authorised nightly bot. This review did not dispatch the workflow or change repository settings.

### 9. P3: documentation and tests still overstate completeness

Roadmap 39 and the overbought claim in 42 remain inaccurate; item 45 still calls the superseded 6.8 experiment done. SYNC is explicitly the original export, while last-sync is newer, but the latter's hash block contains an older state hash and a prose override. Several future event deadlines still say 08:00 while current policy says 07:00. Dashboard copy still says the day call nudges cash (`page/app.js:507`) contrary to policy.

The only workflow is the scanner, with no PR regression job. The published v72 test file hard-codes `/home/claude/ft-game` and treats whatever is there as v7.1; it is now 7.2. Its print-based checks do not fail on false results. Portably rerunning it with a real v7.1 snapshot reproduces the advertised fixes, but its exact backfill-equality print is false on today's data: 15 October differs by 0.01 credit from rounding, while the final value is equal. This is immaterial financially, but not byte-identical.

Evidence: `docs/ft-game-roadmap.md:84`, `:87`, `:103`; `state/last-sync.md:5`; `proposals/claude/2026-10-18-evidence/v72_tests.py:5`; evidence `missing_holding_and_backfill`.

Next action: a small portable regression suite with explicit versioned fixtures and meaningful assertions; run it for script changes before Claude deployment. Correct claims instead of building features merely to make the roadmap true. Pin scanner dependencies to a reviewed set when next changing it, rather than allowing fresh library upgrades on every job.

## Decisions for the remaining game

| When | Highest-value action | Completion evidence |
|---|---|---|
| 19 October | Confirm AbbVie was eligible and the pending order filled as intended; accept the first real scheduled mirror; complete all seven earnings events and implied-move inputs. | FT confirmation, nightly data/state commit and matching hashes; no unrepresented holding in the calendar. |
| By 25 October evening | Decide the 27 to 30 October cluster stock by stock. Coca-Cola's pre-open 27 October report requires exposure established or removed at 26 October's open under the playbook. Later pre-open reports also need exits the prior session. | Full order and last-order times; explicit aggregate event exposure. Default total is 6.0 points, not a probability or maximum loss. |
| Before the 26 October test | Keep 07:00 until FT confirmation or the already approved small test resolves it. Log actual fill date and only then revise the calendar/page/tasks through the normal approval process. | Written FT answer or observed fill and corrected effective date. |
| This week | Repair settlement date/open integrity and the reported-observation update. Add regression checks; correct the roadmap. | Missing-row cases wait or become n/a; replay uses identical dates; existing FT row accepts the new threshold. |
| By 2 November | Agree the late-scan fallback and verify it in a scheduled run; maintain the panel and existing records. | Intake states session used and age; order publication does not depend on a fresh scan arriving on time. |
| From 13 November | Use fresh FT rank and a near-threshold portfolio to choose the documented protect/chase stance. | Current rank, players and threshold timestamp. Do not infer competition position from SPY outperformance. |
| Before final week | Rehearse Thanksgiving and the final early close, capture final FT value/rank, finish unsettled evidence with explicit censoring, then arrange the post-game review and task retirement. | Final snapshot and reconciliation from the explicitly retained 28 November final review, with no invented outcomes for windows that run past the game. |

There are 29 US trading sessions from 19 October through 27 November, and 30 London weekdays. Current FT return is +1.40%, rank top 23.5%; the rough target line is +6.5%. That is about five initial-portfolio percentage points behind a moving line. Energy has contributed +2.561 points to a total +1.436%, so the rest of the book collectively detracted; this is mainly a successful theme exposure so far. It does not establish that the score picked superior stocks. The concentration trim is sensible as a deliberate risk decision, not a statistically demonstrated return improvement.

Freeze the existing score as agreed. Keep the panel as an honest check: 49 historical dates from today's large-cap universe are neither 1,372 independent trials nor a historical investable-universe test; the direction of selection bias is not established. Only about six new non-overlapping live windows can mature before the finish, below the code's eight-date minimum for a live verdict. Likewise 47 settled shadow rows, 11 confidence outcomes and zero drift cases cannot validate calibrated probabilities. Do not turn weak evidence into higher confidence simply because the deadline is near.

## Validation and reproducibility

[Review checks](2026-10-18-review-evidence/review_checks.py) and [captured output](2026-10-18-review-evidence/results.json) accompany this report. The output explicitly distinguishes expected behaviour from reproduced defects; successful execution is not a claim that the defects passed a correctness test.

Run from a repository checkout with scanner dependencies installed:

~~~text
python proposals/chatgpt/2026-10-18-review-evidence/review_checks.py --repo .
python -I scripts/ft_pipeline.py report --ledger data/ledger.json
python -I scripts/ft_pipeline.py panel --panel data/panel.json --history data/history.json
node --check page/app.js
~~~

Python 3.13 used locally; third-party scanner dependencies installed in an isolated validation folder. The review checks generate synthetic fixtures and output only in a temporary directory. They test a full template/run with current stored data, both market branches of an offline scan, repeat-scan record preservation, portfolio replay and gap repair, holiday handling, standstill, drift timeout, the new threshold update and the defects above. They make no price-feed requests.

Original file content hashes were checked after excluding the local snapshot writer's one added terminal newline. All five data hashes, pipeline hash and the newer state hash match the repository manifest. The older state hash in the manifest's code block is superseded by its prose, not silently accepted as matching.

Limits: did not inspect live Claude task registry, read private FT pages, confirm current options quotes or company earnings dates externally, render the dashboard, or run a live Yahoo download. Consequently this review separates repository observations, synthetic reproductions, Claude's reported deployments and proposed future actions.
