# FT Stock Picking Game: roadmap

Written Fri 9 Oct 2026; rebuilt the same evening after Tim asked for everything on it to be implemented, and extended later that night with the macro layer (phase 4). Status tags show where each item stands. What is left needs either time (data has to accumulate) or an answer from Tim.

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

## Still open

- **Calibration.** The panel test (item 35) is now the main evidence. Once all 30 members are loaded (17 Oct), the history verdict is the fair answer on the price part of the score; the live part adds about one date a week. Any change to the score's weights goes to Tim with the figures. The shadow ratings keep running as a check on the full score, including the judgement points.
- **Earnings drift.** Needs about 30 settled "enter" and "watch" cases before the record says much; results season gives perhaps 5 to 15 a week.
- **The day call.** Needs three to four weeks of settled calls before its record means anything. The bar is always saying green, which is right about 55% of the time.
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
- Data arrives one page per stock, so a wide universe can be scanned weekly, not daily.
- Seven weeks is too short to prove any method works.
