# FT Stock Picking Game: roadmap

Written Fri 9 Oct 2026; rebuilt the same evening after Tim asked for everything on it to be implemented, and extended later that night with the macro layer (phase 4). Phase 5 (a fair test, 15 Oct) and phase 6 (counterfactuals and the broad scan, 16 Oct) were added in later sessions with Tim. Status tags show where each item stands. What is left needs either time (data has to accumulate) or an answer from Tim.

## Guiding view

- Returns in this game will come from three things: being in the right themes, being positioned before catalysts (mainly Q3 earnings from 13 Oct to mid November), and cutting positions when momentum breaks. Features should serve those three.
- Performance is weighted. A position's effect on the portfolio is its weight times its return, so sizing matters as much as selection. Every portfolio figure is a sum of weight times return.
- Technical analysis is useful here as a trend filter and a risk tool, computed from price data by code. It is weak as a stand-alone predictor. The evidence over a one to seven week horizon favours relative strength, proximity to 52-week highs, volume-confirmed moves and earnings and analyst revision drift.
- Accuracy first: every number on the page or in a review comes from stored data and code, not from reading a page and typing.

## Phase 1: make it accurate

1. Check the plumbing. [Done 9 Oct: scheduled runs can read and write the project docs, use the page's tools and run Python; a rehearsal run fetched the files, ran the pipeline and republished the data. The game's cut-off times still need Tim's answer: see item 20.]
2. Performance log. [Done 9 Oct: the pipeline adds each completed session's weighted return, the estimated value, the return against the S&P 500 and every position's contribution. Values and ranks Tim reads off the FT site are stored beside the estimate. The FTSE 100 was dropped as a benchmark because no dependable source for it works from here. The first session, Fri 9 Oct, is added by the Saturday review.]
3. Price history store. [Done 9 Oct: 569 daily rows for 19 stocks and SPY back to late August, extended by every evening run. A corrected price triggers a recalculation of the log from that day.]
4. Earnings and events calendar for the whole game window. [Done 9 Oct: 34 events to 27 Nov, each with a UK time, confirmed or estimated, and the last moment to enter an order before it. Estimated dates need confirming as companies announce them; the evening review updates them.]
5. Weekly performance review. [Done 9 Oct: scheduled for Saturdays at 09:12 UK. First run 10 Oct.]

## Phase 2: find stocks that stand out

6. Technical indicators from the price store. [Done 9 Oct: price against 20-day and 50-day averages, structure against the 200-day, distance from the 52-week high, relative strength over five days, about six weeks and a year, RSI, volume ratio, and average true range for sizing. From the same night the 50-day and 200-day averages are worked out from stored prices for any stock with a year of closes: see item 27.]
7. Universe screen. [Changed 9 Oct at Tim's request: five to ten new candidates are added every evening and the weakest leave, keeping the list at about 20, in place of a Sunday pool of 25 to 40. First run 11 Oct.]
8. Composite score out of 100. [Done 9 Oct: trend 40, short term 20, catalyst 20, revisions 20. The link from score to confidence is an assumption that the confidence log will test.]
9. Analyst revision tracker. [Done 9 Oct: a running log of upgrades, downgrades and target changes, shown on the Log tab. 13 entries so far.]
10. Earnings playbook with options-implied moves. [Done 9 Oct: implied moves are stored on each results event, the pipeline prints weight times implied move against a budget of 0.6 points per report, and the Risk tab shows it for every holding. Seeded for TSMC (5.0%) and RTX (5.8%); others are added as their reports come inside five trading days. Source is a third-party page, earnings-watcher.com.]

## Phase 3: manage risk and rank

11. Sizing by volatility and correlation. [Done 9 Oct: a weight cap from each stock's daily range, each position's share of the portfolio's risk, and the most correlated pairs, from stored prices. First finding: energy is 40% of the portfolio and about 86% of its risk.]
12. Scenario table. [Done 9 Oct: six scenarios (ceasefire, oil spike, deeper AI sell-off, AI rebound, hot and cool CPI), each theme's weight times an assumed move. The assumed moves are judgement and should be revisited as events pass.]
13. Rank-aware strategy. [Done 9 Oct as rules: the stance depends on whether the latest reported rank is inside the top 2% and on the date, with an endgame plan from 13 Nov. Sharper once Tim can supply the return of the player on the top 2% line.]
14. Post-mortem on every closed position. [Done 9 Oct: the pipeline writes the return and weighted contribution of each closed position; the evening review adds the thesis and the lesson. Nothing has been sold yet.]

## Page

15. Portfolio value chart against the S&P 500, and a rank tracker. [Done 9 Oct: Performance tab. The lines start after the first completed session.]
16. A 20-day mini chart and trend marker on each tile. [Done 9 Oct, plus a longer price chart in each stock's details.]
17. Upcoming events calendar. [Done 9 Oct: Calendar tab, and the next five events on the Today tab.]
18. Alerts history, trade log and confidence scorecard. [Done 9 Oct: Log and Performance tabs.]
19. Score and technical columns. [Done 9 Oct.]

## Process

20. A midday review. [Built 9 Oct and switched off. The game's rules say a new order takes effect on the next trading day, so a midday change cannot fill the same day. It stays off unless Tim sees the game do otherwise.]
21. More frequent price refreshes. [Done 9 Oct: a second daily refresh at 19:22 UK catches the later US session, and a run at 14:50 UK acts only when a holding or watchlist stock has results that day.]
22. One set of instructions. [Done 9 Oct: every run reads `claude/ft-game-playbook.md`, so one edit changes them all. Split on 15 Oct (item 34). The two saved skills are for hand-run work in a chat.]

## Phase 4: macro, the day call and calibration (added 9 Oct at Tim's request)

23. Government bond yields and oil in every check. [Done 9 Oct: US 2-year, 10-year and 30-year yields back to June 2024, with UK, German, French, Italian and Japanese 10-year yields and Brent, WTI, gas and gold stored each evening from 9 Oct. The evening run prints each with its changes, a backdrop label and how the portfolio has moved with oil and yields; the morning check and both price refreshes store live readings.]
24. A bull case, a bear case and a green-or-red call for the next session. [Done 9 Oct: the chance of an up day for the S&P 500 and for the portfolio, from the 40 most similar past sessions out of about 550, pulled halfway back to the usual rate; the reviewer writes the two cases and may move the figure by up to 5 points. Every call is logged and settled. First call: Mon 12 Oct, green at 51% against a usual 55%. Expect it to stay close to a coin flip.]
25. Watchlist colours by strength. [Done 9 Oct: green, amber and red bands tied to the buying rules, on the tiles and in the table.]
26. Economic release tracker. [Done 9 Oct: forecast, previous and actual figures on each release, with what the S&P 500 and the 10-year yield did that day. Seeded with the 14 to 16 Oct releases.]
27. Moving averages from stored prices. [Done 9 Oct for the eleven stocks with a year of closes: 10, 20, 50, 100 and 200-day simple averages, 10, 20, 50 and 200-day exponential averages, their order, and golden and death crosses, with the 50-day and 200-day drawn on each stock's chart. Seven US stocks wait for their history: the price site limits its history feed, so the evening runs add two a night. BAE Systems has no source.]
28. Calibration. [Started 9 Oct: a shadow rating for every stock every evening, settled after five sessions and reported by score band; plus a backtest of the price-only part of the score. First settlements 15 Oct. The first backtest showed no positive link between points and the next five sessions, on a small sample chosen with hindsight.]

29. Weekend news check. [Done 10 Oct at Tim's request: Saturday and Sunday at 20:20 UK. It covers the Iran war, oil supply, US policy and news on every holding, rates each item for this portfolio (A changes Monday's plan, B watch, C noise), reads the few prices that trade at weekends, and logs the result for Sunday's review and Monday's morning check. First run Sat 10 Oct.]
30. A proper market data service. [Wired in on 11 Oct, waiting for the key. massive.com (the renamed Polygon.io), free plan, on an account opened by Tim's father. Used once by hand on 10 Oct for seven year-long histories, checked against stored prices. From playbook version 5.4 the evening and weekly runs fetch a year of closes from it for every stock that lacks one, up to ten a night, whenever their own instructions carry a line beginning "Market data key:"; a script command (`closes`) lines the figures up with stored sessions and refuses them if they disagree with stored closes. The key is kept only in those two scheduled tasks, never in the project's docs or on the page, and it is for Tim's father to put it there. Until then the runs use the price site's free feed, now four histories a night. The service has no London listings, no Brent and no intraday prices. No free feed with a year of history and no key was found.]

31. Quiet-day messages. [Done 10 Oct at Tim's request: the evening review and the morning check still run every day and may change the order on any of them, but Tim is sent a message only when there is something to enter (a changed order, a morning revision) or a run has hit a fault. Price refresh alerts and watchlist changes go on the page only. Playbook version 5.2, part I.]
32. Entering orders for Tim. [Asked for on 10 Oct and declined: the FT site blocks automated access, an unattended run would depend on his computer being on and signed in, and no one would check an order before it filled. Fixed order days were offered in its place and turned down: Tim wants the option to change on any day.]

33. Crypto tracking. [Done 11 Oct at Tim's request: Bitcoin, Ether, Solana and XRP prices at every US close (Coinbase), Bitcoin's trend read from a fund that trades in stock-market hours, and for every stock the move that has gone with a 1% move in Bitcoin. A stock that follows Bitcoin closely is marked, and is bought only while Bitcoin's trend is up, at 10% at most. Strategy and Coinbase are on the watchlist as standing trackers (first readings: 1.81% and 1.45% for each 1% in Bitcoin). A "Bitcoin falls 15%" scenario, a Crypto block on the Macro tab, and a live Bitcoin reading in the morning, weekend and price-refresh runs that gives the expected gap in any linked holding. Playbook version 5.3.]

## Phase 5: a fair test and results season (added 15 Oct at Tim's request)

34. Split the playbook. [Done 15 Oct, playbook version 6: a core doc (`claude/ft-game-playbook.md`: hard limits, where things live, the game, objective and rank, output style, the state doc) with a routing table, plus `claude/ft-game-rules.md` (part E), `claude/ft-game-data.md` (parts F and G) and one doc per run (`claude/ft-game-run-evening.md`, `-morning`, `-refresh`, `-weekly`, `-weekend`). Part letters are unchanged, so the scheduled tasks' instructions still work as written. A price refresh now reads about a third of what it did.]
35. A fair test of the score. [Built 15 Oct. A panel of 30 stocks fixed in advance by rank alone (every fifth of the 150 largest in the S&P 500), two years of closes each from the market data service, kept in a panel file outside the page's data. The pipeline ranks the panel by the 48 price-only points on every fifth session and checks the rank against the next five sessions' return against the index; the measure and the pass mark (+0.03 with t of 2 or more) were fixed before any data was seen. 15 of 30 loaded on 15 Oct; first result over 48 dates: +0.028 (t +0.5), no evidence that the points rank stocks. One-year and two-month strength lean positive, the five-day part leans negative. The other 15 load on Saturday 17 Oct; the panel is topped up every Saturday.]
36. Earnings-drift scan. [Built 15 Oct. Each evening the review finds the session's reporters (holdings and watchlist, the day's largest S&P 500 gainers, a search for beat-and-raise reports), up to six a night, and the pipeline runs six tests: beat, raised guidance, a reaction of 3% or more and 2 points over the index, a close at or above the open in the upper half of the range, volume 1.5 times average, and an intact trend. All six: may be bought at the next open at up to 10% (5% if extended). Beat, reaction and trend without the rest: watchlist, needing a second day. Every case is settled after five sessions so the record shows whether the tests work. No earnings calendar page with actual figures was readable from here, so reporters are found by search.]

37. A shared GitHub mirror for Claude and ChatGPT. [Done 16 Oct at Tim's request: private repository `timzwang/ft-game`, with the Claude GitHub App installed on that repository only. Tested end to end on 16 Oct: a push from a chat, a push from a one-off scheduled cloud session with nobody present, and a ChatGPT branch and pull request that Tim merged. First full export the same night (docs, state, scripts, data, page, skills, schedules with the key redacted; scripts and data byte-identical to the artifact). From playbook version 6.1 the evening and weekly runs mirror the data files and the state doc as their last step (G6), best effort, and the state doc is always written from a local file so the Project and GitHub copies match (part J). ChatGPT reads the repository and proposes changes through pull requests; Tim merges; a merged change reaches the live system only when applied in a session with Tim. First live mirror: Saturday 17 Oct's weekly review.]

## Phase 6: prove it beats something simpler, and look wider (added 16 Oct at Tim's request)

An outside review by ChatGPT on 16 Oct agreed that the system's machinery is ahead of the evidence that it picks better stocks. Tim agreed five changes from it and asked for a broad scanner. The question every item serves: did a decision put the portfolio in a better stock, at a price the game could actually fill, than it would otherwise have held?

38. Counterfactual portfolios. [Agreed 16 Oct; to build in pipeline version 7.] Four portfolios priced by the pipeline with the game's own arithmetic (weights reset at each close, changes fill at the next open), from prices already stored, so no new fetches:
    - Standstill: the order of Mon 12 Oct, never changed. The simplest control.
    - Previous order: for every order change, the order it replaced, carried five sessions. Each change gets a net effect in points, so the six changes in the first seven sessions get a verdict.
    - Price-only top five: every Monday open, the five list stocks with the most price-only points, 20% each.
    - Full-score top five: the same, ranked by the full score.
    The weekly review reports all four against the real portfolio and the S&P 500; the Performance tab gets a line for each. Stocks that leave the list keep their prices until every counterfactual using them has settled, as the shadow ratings already do. Limit: the two top-five portfolios draw on the watchlist, which was itself chosen by these rules; the broad scan (item 43) gives a fairer pool later.
39. Top-five panel test. [Agreed 16 Oct; pipeline version 7.] On each panel date, the five members with the most price-only points, equal weight, against the panel average and the S&P 500 over the next five sessions, also measured from the next open (the return an order could catch). Prints the average gap, the share of dates it was positive and a block-bootstrap interval. Supporting evidence only: the verdict stays the rank correlation fixed on 15 Oct, because adding a second pass mark after seeing the first result is testing until something passes.
40. Do the judgement points earn their place? [Agreed 16 Oct; pipeline version 7.] The 40 catalyst and revision points have never been tested. Two checks, both from records already kept: on settled shadow ratings, the rank correlation and hit rate of the full score against the price-only points (same stocks, same dates); and the full-score top five against the price-only top five (item 38). Too few settled ratings to judge before about 150, so reported weekly but not acted on until then. If the full score does no better, any change (for example an anchor built on price points only) goes to Tim.
41. Score weights stay fixed for the game. [Agreed 16 Oct.] The live panel gives about six dates by 27 Nov, too few to validate any new weighting. The weights change only if Saturday's 30-stock history verdict, by the rule fixed on 15 Oct, comes out "useful" or "the wrong way", and then only with Tim's agreement. Any change runs beside the original 40/20/20/20 score, which stays the control in the shadow ratings, and every live version is kept with its ratings.
42. Day call and "overbought". [Done 16 Oct, playbook version 6.2, part E.] The day call (1 right of 3) no longer moves cash in any case; it is logged and settled as a research record, and may come back as a cash input only after beating always-green over at least 20 settled calls, with Tim's agreement. "Overbought" (RSI) is a warning, no longer a 5% cap; "extended" (far above the 50-day) still caps a new position at 5%. Pipeline version 7 splits the shadow-rating record by the overbought flag, so the warning gets tested too.
43. Broad-universe scanner. [Built 16 Oct at Tim's request; first scheduled run Fri 16 Oct after the US close.] The nightly intake used to look at perhaps 40 names, because stockanalysis.com serves one page per stock and refuses bursts. The scan does the wide look on GitHub's servers instead, which have open internet.
    - Where: `.github/workflows/scan.yml` in `timzwang/ft-game`, running `scan/scan.py`. Rules and file list in `scan/README.md`. A run takes about four minutes, inside GitHub's free allowance.
    - Universe: 868 stocks: the S&P 500 (503), the Nasdaq-100's other members (15), the FTSE 100 and FTSE 250 (350), from Wikipedia (Nasdaq-100 from Slickcharts, since Wikipedia dropped its table), rebuilt weekly.
    - Data: about 15 months of daily bars for all of them from Yahoo Finance in one bulk download each run, US and London separately. A fresh download each night replaced the planned cache: it is quick, keeps the repository small for the evening review's clone, and picks up corrected bars. Stooq, the planned fallback, sends GitHub's servers a bot-check page and is of no use.
    - Timing: weekdays at 20:10 and 21:05 UTC, so 16:10 New York until 30 Oct and 16:05 New York from 2 Nov; a session already scanned is skipped. The evening review forces a run through `scan/request.txt` if the scheduled one is late (G7).
    - Lists (rules version 1, fixed 16 Oct before any result was seen): Leaders and Events, top 30 each, with a turnover floor ($25m a day US, £3m London). A stock missing one of the last three sessions in Yahoo's data stays eligible for Leaders but is kept out of Events.
    - Use: the evening review reads the lists first (data doc G7, H1 step 4): Events lead the search for reporters, both lists lead the intake. Scan figures never enter today.json or the score.
    - Record: the top 10 of each list is settled five sessions later, close to close and from the next open, in `scan/record.csv`, first appearances shown apart; the weekly review quotes it. The first rows are Friday 16 Oct's.
    - Tested 16 Oct: synthetic prices for the list rules and the settlement (checked by hand), then eight live runs on GitHub. US figures matched the stored closes for six of seven overlapping stocks exactly (Merck 0.09% off). Yahoo's London stock data was missing 15 Oct that morning while its FTSE 100 series was not, so London names were left out of those test runs; the first evening run is the first full London test.

## Still open

- **The broad scan's London data.** Yahoo skipped 15 Oct for London stocks on the morning of 16 Oct. If the gap persists, London names are kept out of Events (by rule) until it passes out of the last three sessions. Check `scan/latest.json` (`stale`, `holes`) after the first few evening runs.

- **Calibration.** The panel test (item 35) is now the main evidence. Once all 30 members are loaded (17 Oct), the history verdict is the fair answer on the price part of the score; the live part adds about one date a week. Any change to the score's weights goes to Tim with the figures. The shadow ratings keep running as a check on the full score, including the judgement points.
- **Earnings drift.** Needs about 30 settled "enter" and "watch" cases before the record says much; results season gives perhaps 5 to 15 a week.
- **The day call.** A research record only from 16 Oct (item 42). Needs at least 20 settled calls against the bar of always saying green, which is right about 55% of the time.
- **The order cut-off after the clock change.** The FT's 2026 terms state times in BST, including for November. If 08:00 means 08:00 BST after 25 Oct, the cut-off becomes 07:00 UK and the 07:26 morning check would miss it. Check the game's help page or ask the FT before Mon 26 Oct; if it is BST, move the morning check to about 06:30.
- **Page design pass.** Done 10 Oct in two rounds: the page now follows the look of Trading 212 and TradingView (own white or dark surface, order banner, value headline, one row per stock, a full screen per stock on a phone and a side-by-side view on a wide screen). It was checked on a local copy only; Tim is the one who sees the live page.
- **The top 2% line.** Needs leaderboard figures from Tim. Without them the stance rules work from rank alone.
- **Scenario assumptions.** Hand-set moves per theme. After a real event (CPI on 14 Oct, any ceasefire headline), compare what happened with what was assumed and adjust.
- **UK and European coverage.** Three UK names so far. BAE Systems has no published averages, so its score has gaps until the price store is long enough.
- **Crypto.** The link figures use 120 sessions that include one sharp rally (mid August to late September), so they describe how these stocks behave when Bitcoin moves a lot; in a quiet month the link is looser. Solana and XRP have no fund that lines up with stock sessions, so they are tracked as prices only.
- **Second benchmark.** A FTSE 100 line would need a dependable source for the index or a tracker fund.
- **Estimate against the FT site.** The estimated value should stay within a few tenths of a percent of the game's figure. A wider gap means a fill was assumed wrongly; the weekly review checks it.

## Limits to design around

- No streaming prices: the page updates when a scheduled run refreshes it.
- No access to the FT game site: value, rank and the leaderboard have to come from Tim.
- Data arrives one page per stock from here, so a wide universe cannot be scanned from Claude's workspace. The broad scan (item 43) does that work on GitHub's runners instead, and the workspace checks only the shortlist.
- Seven weeks is too short to prove any method works.
