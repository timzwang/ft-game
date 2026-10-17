# FT Stock Picking Game: weekly performance review (H5)

Part H5 of the playbook (version 6.4, 17 Oct 2026: reconciliation with the FT figure, the standstill and judgement tests, the panel swap Tim agreed; version 6.3, 16 Oct 2026: the broad scan's record in the review). Runs on Saturday at 09:12 UK. Read with the core playbook (`claude/ft-game-playbook.md`), the rules (`claude/ft-game-rules.md`), the data doc (`claude/ft-game-data.md`) and the state doc.

This run also keeps the panel test and the drift record supplied with prices. Both need the market data key in this run's instructions; without it, say so and skip those two steps.

## Steps

1. Read the state doc. Fetch the files (G1, the panel file included) and write the template with `--panel`. Note what it prints under "Panel" (members short of a two-year history, members behind SPY) and "Drift rows still open".
2. Look at the latest `perf` row in the fetched ledger. If its date is Friday's, the session is already in: skip the price fetches for list stocks. Otherwise bring the log up to Friday's close: fetch the quote page for every stock, for SPY, BNO and the US-listed lines, the statistics page for stocks under "Averages still needed", the macro pages, the four Coinbase rows for Friday's session and the IBIT and ETHA quote pages, applying the freshness and pacing rules in part F (on a Saturday a quote page should read "At close" for Friday; a history page may still lack Friday's row, in which case build it from the quote page as G3 describes). Fill today.json with `date` set to Friday's date, `effective` set to Monday's date, `next_session` set to Monday's, `entered` Friday's date, `prices_as_of` "Fri <date> close", `order_for` "Mon <date> open", and the order unchanged. Leave `daycall` blank: Sunday's review writes Monday's cases. Store the actual figure for any release that came out on Friday (the calendar page in part F). Leave each stock's status, note and judgement points as the template wrote them. Do not change the order or the watchlist in this run; the Sunday evening review does that.
3. Panel top-up (with the key). For every panel member the template names, one call to the market data service (part F), five at a time with `sleep 65` between groups:
   - A member short of a two-year history: `<from>` two years before SPY's last stored session plus two days (for example 2024-10-16 when SPY's last session is 2026-10-13), `<to>` SPY's last stored session.
   - A member that is behind: `<from>` the day after its last stored close, `<to>` SPY's last stored session.
   - Pass each reply to `closes` with `--panel panel.json`. A refused or short list may be fetched once more in this run if the rate allows; otherwise leave it for next Saturday and name it.
   - If a member's feed returns no data at all on two Saturdays running, or fewer than 400 sessions, replace it with the next position down in the S&P 500 list (part E), write the swap into the panel file's rule text by hand with Tim's agreement, and say so. Never swap for any other reason.
   - Agreed by Tim on 17 Oct: Marsh & McLennan (MRSH, 190 sessions) is replaced by the next position down, position 149 of stockanalysis.com's S&P 500 list by market cap. The list as read on 15 Oct was not saved, so read it on the day, take position 149 (or the first stock below it that is not already a member), and write into the rule text which stock it was, the date it was read and that the 15 Oct list was not kept. Load its two years like any other member. Hewlett Packard Enterprise (HPE) is also still to load.
4. Drift settlement (with the key). For each open drift row whose stock is not on the list and whose DRIFT WAITING line (or the template's "Drift rows still open" line) asks for prices: one call from its reaction date to SPY's last stored session, passed to `closes` (it lands in `extra_history`). Up to 20 a week, oldest first, in the same groups of five.
5. Run the pipeline with `--panel` (G4). If the run prints a SHADOW line, fetch the history page of each stock named, give the rows under `extra_history` with the stock's ticker, and run again so its ratings can settle. Run it even when no new session is due, whenever step 3 or 4 added closes, so the panel test and the drift record are brought up to date.
6. Run `report --ledger out/ledger.json --since <the Monday of the week just ended>`, and `panel --panel out/panel.json --history out/history.json` for the full panel list.
7. Publish the files that changed (G5).
8. Write the review:
   - The week and the game to date: estimated return against the S&P 500, and the value and rank Tim last reported with its date.
   - What each position contributed, in points (weight times return), best to worst, and what that says about sizing: was the weight in the right places?
   - Reconciliation: the RECONCILE lines, Tim's latest FT figure against the estimate for the same close. Say plainly whether the estimate is verified (a closing figure within about 0.2%) or not, and why.
   - The standstill test (part E): what the week's changes added against standing still, and each change's five-session verdict. Say when a row is not priced, and which prices it needs.
   - The judgement test (part E): the JUDGEMENT TEST lines once any dates have settled; until then one line saying how many ratings store both halves.
   - Confidence ratings: windows that closed, hit rate by band, and whether higher ratings beat the index more often. Say plainly when the sample is too small to judge.
   - The panel test: the history and live verdicts with their figures, how many members are loaded, each part's correlation, and a plain sentence on whether the score is earning its place. If the history verdict is settled on all 30 members, set out for Tim any change to the score that the parts point to, with the figures; never make the change in this run.
   - Calibration: the shadow ratings by score band and the old backtest, labelled as weaker evidence than the panel.
   - The earnings-drift record: settled cases by verdict (share that beat the index, average gap), any drift position held and how it went, and whether "enter" is doing better than "fail" yet. Say when the sample is too small.
   - The day call: how many were right against the bar of always saying green, and the Brier score.
   - The broad scan: clone the repository (G6 step 1) and quote the record table at the end of `scan/latest.md` (Leaders and Events, first appearances, share that beat the index and average excess from the next open), how many intake names came from the scan this week, and how those did. Say when the sample is too small. If the repository cannot be read, say so and skip this point.
   - Macro: the week's moves in the US and UK 10-year yields and in Brent, each release against its forecast with the market's reaction, and whether the scenario assumptions held.
   - Rules: which helped or hurt this week (the score filter, news momentum and drift entries and exits, results holds against implied moves), with the cases.
   - Closed positions and their lessons.
   - Risk now: the largest shares of risk, the most correlated pairs, the worst scenario (the report prints all three).
   - The rank stance from part D, and two or three specific changes for the coming week for the Sunday review to consider.
   - Ask Tim for his current value, rank and number of players, and for the return of the player on the top 2% line if the leaderboard shows it. Ask for the value after the US close (after 21:15 UK; 20:15 UK in the week of 26 Oct) or from the last point of the game's own value chart, with the time he read it (part K).
9. Add a line to the review log in the state doc and update its status section (including the panel test's latest line), writing the doc from a local file (part J). Send a five-line summary through SendUserMessage.
10. Mirror to GitHub (G6). Best effort: a failure goes under unverified items and changes nothing else.

## Output

Start "Tim,". Sections: week and game to date (two lines); contribution table; what worked; confidence, panel test, calibration, drift record and day-call checks; macro and risk; rank stance and Sunday changes; what is needed from Tim (value, rank, players, a top-of-leaderboard return); unverified items; sources as links.
