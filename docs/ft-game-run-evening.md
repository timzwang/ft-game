# FT Stock Picking Game: evening review (H1)

Part H1 of the playbook (version 6.11, 19 Oct 2026: `order_expected` with every change of order, step 6, and the EXPECTED BENEFIT line, output item 15; version 6.10, 19 Oct 2026: the results budget by date and `RESULTS MISSING`, step 10; version 6.4, 17 Oct 2026: the 07:00 UK cut-off, the results total, rows for sold stocks; version 6.3, 16 Oct 2026: the broad scan, G7). Runs at 21:30 UK, Sunday to Thursday. Read with the core playbook (`claude/ft-game-playbook.md`, parts A to D and I to K), the rules (`claude/ft-game-rules.md`, part E), the data doc (`claude/ft-game-data.md`, parts F and G) and the state doc.

This review runs every evening and may change the order on any of them. Tim is sent a message only when there is something for him to enter (part I, "When Tim is told"). On a change evening he enters the order before 07:00 UK on the next trading day (part C); on a quiet evening the page and the state doc are updated and he hears nothing.

## Steps

1. Read the state doc. If it cannot be read, say so first and do not invent a portfolio. Assume the last recommended order was entered unless the doc or Tim says otherwise. If the state doc shows Tim's FT figures waiting to be stored, put them in `reported`. On a Sunday, start from the "Weekend log" in section 7 of the state doc, which the weekend news checks wrote (H7): confirm each item rated A or B from a current source, then build it into the regime read, the day call and the order.
2. Fetch the files (G1, the panel file included) and write the template with `--panel`. Note the stocks it lists under "Averages still needed", any stock behind SPY, and the open drift rows.
3. Collect data, pacing stockanalysis.com requests as part F says:
   - Every holding and watchlist stock: its quote page with a clock suffix (today's row, 52-week range, target, results date, headlines). Add the statistics page only for stocks under "Averages still needed", and the history page only if the store is missing a recent session for that stock.
   - UK stocks: the lse.co.uk quote; the quote pages of the US-listed lines (`/stocks/shel/`, `/stocks/bp/`) for their rows.
   - SPY's quote page; the BNO quote page for the `OIL` row; the S&P 500 list page for breadth and the 15 largest gainers and losers.
   - Macro: the Treasury page, the tradingeconomics bond page and commodity page (three fetches).
   - Crypto: the four Coinbase rows for the session, and the IBIT and ETHA quote pages for their rows (part F). If any fails, leave that figure out: the script carries the last one and says so.
   - The one-year feed (part F) for the US stocks the template lists under "Averages still needed", holdings first and then the highest scores. With the market data key in this run's instructions: every one of them, up to ten a night, five calls at a time; tonight's new candidates are done after step 4 names them. Without the key: at most four, one at a time with `sleep 170` between, and none on a night when any stockanalysis.com page has been refused. Pass each reply to `closes`. BAE Systems has no feed: skip it.
   - The panel is not topped up in the evening; the weekly review does it.
   - Stocks the template names as sold in the last five sessions and no longer on the list, and reporters on a DRIFT NEEDS line: one history page each, the session's row (and for DRIFT NEEDS the named session's full row) under `extra_history` (G3). These pages count towards the pacing rule.
   - Apply the freshness rules in part F to every page, and build today's session rows as G3 describes. On a Sunday the last session is Friday's.
4. Earnings-drift scan and watchlist intake (part E):
   - First read the broad scan (G7): its Events list leads the search for reporters and its two lists lead the intake.
   - Find the session's reporters (part F, "The day's reporters"): the scan's Events; holdings and watchlist stocks with a results event on this session or the evening before; any of the 15 largest S&P 500 gainers whose quote page headlines show results; and large US or FTSE 100 names from a search for the day's beat-and-raise reports. Keep large, well-known listings only.
   - Take up to six: holdings and watchlist reporters first, then the largest day moves. For each, fetch its quote page (the reaction session's row, reading "At close") and statistics page, and find its earnings and revenue against the consensus and what it said about guidance from the company's release or a report that gives both figures. Add each as a `drift` entry (G3). On a Sunday the scan covers Friday's session.
   - Then pick five to ten new watchlist candidates, "enter" and "watch" verdicts from tonight's scan first once the run has printed them, and fetch each one's quote page, statistics page and history page (up to 50 rows). Decide removals after the first pipeline run, when the scores are known.
5. Research, aiming for 25 to 40 distinct current sources beyond the price pages, with independent searches sent together and extended search mode for anything from the last 48 hours:
   - Market regime: closes and moves for the S&P 500, Nasdaq, Dow, Russell 2000, FTSE 100 and STOXX 600; VIX; the US 2-year, 10-year and 30-year yields and the UK, German and Japanese 10-year yields; Brent and WTI; gold; the dollar; sector performance; breadth; where the S&P 500 and Nasdaq sit against their 20-day and 50-day averages. Label it risk-on, mixed or risk-off and say what would change the label. Weigh the day's bullish news against the macro backdrop as part E describes. Tim's view on 8 Oct was that the market is strongly bearish; test that against the data each day without assuming either way.
   - Economic releases: today's actual figures against forecast, and the forecast and previous figure for anything due in the next five sessions (part E).
   - Macro and events: the Fed, inflation and jobs data, Treasury auctions, oil and geopolitics (the Iran war and the Strait of Hormuz in particular), and regulatory news touching holdings. Flag market-moving or regulatory items even when they are not about a holding.
   - Every holding and watchlist stock: the move and its reason, news, the next results date and time, and every rating or target change in the last 7 days with the bank and the old and new rating and target.
   - News momentum scan: the day's notable upgrades from major banks, large contracts, financings, government deals and guidance raises across large US, UK and European stocks, plus the largest movers on the S&P 500 list page.
   - Results ahead (part E) for anything reporting inside five trading days, and the implied move for every holding reporting inside ten (from Mon 20 Oct: Coca-Cola 27 Oct, Microsoft 28 Oct, Shell and Eli Lilly 29 Oct, Exxon Mobil and Chevron 30 Oct), stored as `implied_pct` on each results event.
   - The next three trading days, positioned with the timing rules in part C.
   - The bear case: the strongest argument against the current portfolio, from a source that disagrees with it.
6. Fill today.json (G3) and run the pipeline with `--panel` (G4). Then, from its output: decide the order using parts D and E, with a score and a confidence rating on every position; act on the DRIFT SCAN verdicts (part E, "Earnings drift"); apply the crypto rules of part E to any crypto-linked stock that is held or being considered, reading Bitcoin's trend from the CRYPTO block; settle the watchlist removals; write the bull case, the bear case and any adjustment into `daycall`. Decide whether this is a change evening or a quiet evening (part I): compare the final `order`, weight by weight, with the one the template wrote into today.json, which is the order in force. Before calling it a change evening, put every proposed change through the trade decision gate (part E): why change, why the replacement is better (with its PORTFOLIO FIT line), why not keep the order in force, and what it does for the top 2% target. If the four answers are not convincing, keep the order: a quiet evening is a good outcome. On a change evening fill `order_expected` (G3) before the final run, with the four answers, what would show the change wrong, and the subjective `pts`. It is the record the STANDSTILL test will judge the change against, so write it honestly and before the message; never inflate `pts`, and never cite it as the reason for the change. Add two rows to `alerts` so the page says which it is, each with today's UK date as `date` and the UK time now as `time_uk` (the page's banner works out the 08:00 cut-off from them): one with `stock` "Order", reading "Changed for <order_for>: enter before 07:00 UK. <the changes in a few words>" or "No change for <order_for>: nothing to enter."; and one with `stock` "Watchlist" naming the stocks added and removed tonight (leave it out if there were none). Run again. The run is safe to repeat.
7. On a change evening, send the order first: items 1 to 3 of the change-evening output through SendUserMessage if that tool is available. On a quiet evening send nothing through SendUserMessage.
8. Publish the files that changed (G5).
9. Write the state doc back (part J), from a local file.
10. Mirror to GitHub (G6), reusing G7's clone. Best effort: a failure costs one line in the final message and nothing else.
11. Final message: the change-evening output or the quiet-evening output below, whichever applies.

Sunday also scans the coming week's results and economic calendars and updates the events list, with the forecast and previous figure for each release. Its intake may draw on the whole week's movers and upgrades rather than one day's. The screening script (part B) is kept for ranking a long list quickly by hand; the nightly intake does not need it. If there is no portfolio at all, this run builds the first one with deeper work on at least 15 candidates.

## Output

Quiet evening. Nothing through SendUserMessage. The final message is at most nine short lines:

1. Exactly "No change tonight. Nothing to enter."
2. The order in force on one line, for example "Exxon 15, Chevron 15, Shell 10, cash 25".
3. The last session, weighted: the portfolio's move, the S&P 500's, and the largest contribution either way.
4. Tomorrow's call for the portfolio with its figure and the usual rate.
5. Watchlist: the names added and removed, on one line, with any drift verdict of "enter" or "watch".
6. Up to three lines on what tomorrow's review is watching: a result due, an exit signal, a stock close to promotion, a release.
7. Any page that was refused, the broad scan's status (G7: current, one session old, forced, or not used with the reason) and G6's line if the GitHub mirror failed, on one line.

Change evening, in this order:

1. Verdict line: "Change the order: enter before 07:00 UK on <day>", plus the regime in a few words.
2. The order to enter before 07:00 UK on the next trading day, restated in full every time: Stock | Weight | Score | Confidence (not calibrated) | Change versus current | One-line reason, with cash as a row. Check before sending: at least 5 stocks, each 5% to 25%, cash at most 25%, total exactly 100%.
3. What changed and why, covering the order and the watchlist: the four gate answers in a line each, what would show the change wrong, and the review's own estimate ("subjective estimate: +0.2 points over five sessions", never a probability); every stock added to or removed from the watchlist and every status change, or "No watchlist changes".
4. Yesterday's result, weighted: the portfolio's move, the S&P 500's, and the three largest contributions either way as weight times return.
5. Market read, short, with the macro block: a small table of the US 2-year and 10-year, the UK 10-year gilt, Brent and Bitcoin (level, one-day and five-day change), the backdrop label, Bitcoin's trend in a few words, and one sentence on which way it cuts for this portfolio.
6. Tomorrow: the bull case, the bear case, and the call for the S&P 500 and for the portfolio, each as "Green" or "Red" with its figure and the usual rate, then one sentence on what the similar-day evidence showed. Say so when it is a coin flip.
7. Holdings table: move, score, band and flags, news, next results, consensus target, rating changes.
8. Watchlist: the additions and removals table (stock, added or removed, score, band, reason), then the list by band with scores, each promotion with a confidence rating.
9. Earnings drift: each reporter scanned with its verdict and the tests it failed, and the record so far.
10. Results ahead: implied move, past reactions, weight times implied move against the budget for its date (1.0 for 27 to 30 Oct, otherwise 0.6; part E), and the hold, trim or exit call with the last order time; any `RESULTS MISSING` line fixed by adding the event; the RESULTS TOTAL lines and whether that concentration is deliberate.
11. News momentum: qualifying events, gap versus open-to-close, and whether each passes the entry test.
12. Risk check: theme weights, the largest shares of risk, the worst scenario, and any NOTE lines from the pipeline with what was done about them.
13. Coming up: the next three trading days in UK time, with the forecast for each economic release.
14. Bear case against the portfolio.
15. Checks: confidence ratings whose window closed, yesterday's day call against what happened, any shadow ratings or drift windows that settled, the panel test's latest line, and the STANDSTILL line for the latest change, with the EXPECTED BENEFIT line once any change carries an expectation.
16. Assumptions, unverified items (including any page that was refused, and G6's line if it failed), and anything needed from Tim. On Sundays ask for his value, rank and number of players.
17. Sources.
