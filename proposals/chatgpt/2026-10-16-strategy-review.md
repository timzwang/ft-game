FT Stock Picking Game — Independent Strategy Review

Your system has the foundations of a sophisticated quantitative research workflow. The strongest parts are the disciplined record-keeping, event-driven monitoring, reproducible pipeline and recognition that a convincing backtest is not necessarily evidence of a genuine trading advantage.

However, I agree with Claude’s conclusion: the sophistication of the infrastructure currently exceeds the evidence that its signals can select outperforming stocks.

My main recommendation is to shift development towards three things:

* Finding measurable predictive advantages rather than introducing more indicators.
* Improving portfolio decisions by comparing the expected benefit of competing trades.
* Making the dashboard an investment decision terminal, not simply a collection of charts and statistics.

There are also some weaknesses in your testing design and risk rules that I would address before changing the scoring weights.

First: an important eligibility issue

I checked the FT’s official 2026 competition terms. They specify that entrants must be FT subscribers aged 18 or over.

As you’re under 18, you should clarify eligibility directly with the FT before treating any leaderboard result as an official competition achievement for your CV. Your analysis system can still be documented as an independent quantitative investment research and virtual portfolio project, but you should not claim an officially eligible placement without confirmation.

That doesn’t change the technical feedback below, which applies equally to a simulation or an authorised competition portfolio.

1. Highest-priority improvements

I would prioritise the following changes, based on their likely contribution to decision quality rather than how impressive they sound.

Priority	Improvement	Expected benefit	Effort
P0	Properly validate the scoring model	Very high	Medium
P0	Reproduce FT fills and performance exactly	Very high	Medium
P1	Build a portfolio replacement engine	High	Medium
P1	Improve earnings-event analysis	High	Medium
P1	Benchmark against simpler strategies	High	Low
P1	Separate evidence from AI judgement	High	Low
P2	Expand the investable-universe scanner	Medium–high	Medium
P2	Redesign the decision dashboard	Medium	Medium
P3	Add more macro indicators and complex forecasts	Uncertain	High

These are my qualitative assessments, not measured estimates of additional returns.

A. Fix the panel test before changing weights

This is my biggest concern.

You currently have 15 of 30 stocks loaded, an information coefficient (IC) of +0.028 and a t-statistic of +0.5.

That result doesn’t establish an edge. However, completing the remaining 15 stocks on Saturday will not automatically produce a statistically reliable conclusion.

There are three problems.

1. Overlapping returns

Suppose you calculate a stock’s next five-day return every trading day.

The return measured on Monday and the return measured on Tuesday share four trading days. They are not independent observations.

Naively treating these outcomes as independent can seriously exaggerate statistical significance.

2. Survivorship and selection bias

Selecting stocks based on their market capitalisation in October 2026, then testing their price histories going back two years, uses today’s universe to analyse yesterday’s opportunities.

Companies that declined, disappeared or fell outside the current top 150 can be omitted.

3. Your test doesn’t directly measure the competition objective

An IC measures the relationship between scores and subsequent returns. But you aren’t attempting to trade all 30 stocks in a diversified factor portfolio.

You’re selecting roughly six to ten holdings in a concentrated, long-only portfolio.

The relevant question is whether high-scoring stocks outperform alternatives over the actual holding period, using the game’s execution rules.

My recommended validation design

Research and validation workflow

Historical data available at decision time

Point-in-time universe, timestamps, verified closes

Model portfolio

Frozen scoring rules and constrained allocations

Control portfolios

Equal weight, simple momentum, buy and hold

Walk-forward simulation

Next-eligible-open fills, no future information, identical constraints

Out-of-sample evaluation

Excess return, rank IC, drawdown, hit rate and robustness

I would use:

* Walk-forward evaluation: freeze rules using historical data, then evaluate on subsequent unseen periods.
* Non-overlapping five-session tests, supplemented by overlapping tests with autocorrelation-robust inference.
* Matched-sector excess returns: determine whether a stock is outperforming its own sector, rather than simply benefiting from an industry rally.
* Top-five and top-ten portfolio tests: measure the actual outcome of selecting the model’s highest-ranked stocks.
* Bootstrap confidence intervals: assess how sensitive results are to the chosen market periods, preserving time dependence.

Crucially, keep the original 40/20/20/20 formula as a control. If you revise it after Saturday’s results, you need another untouched validation sample before claiming that the revision works.

Research on financial factor discovery warns that conventional significance thresholds can be inadequate after multiple strategies have been tested.

My verdict: do not immediately rebuild your score if Saturday produces another weak result. Treat the score as an unproven ranking hypothesis and investigate whether any individual component actually adds useful information.

B. Add a portfolio replacement engine

Your existing system evaluates stocks largely on their own merits.

What it really needs to evaluate is the opportunity cost of holding one stock instead of another.

For example, suppose a holding scores 64, and a candidate scores 81.

That alone doesn’t establish that replacing the holding improves the portfolio.

The candidate might have a worse upcoming earnings risk, duplicate an existing AI exposure, or have already experienced much of the move your signal is trying to capture.

I would create a new pipeline operation called compare.

It should evaluate:

Dimension	Current holding	Candidate
Forward catalyst	Existing thesis	New opportunity
Relative momentum	Sector-adjusted	Sector-adjusted
Expected five-session performance	Estimated	Estimated
Earnings gap exposure	Existing risk	New risk
Portfolio correlation	Current contribution	Post-swap contribution
Execution	No trade	Next eligible open
Evidence quality	Data coverage	Data coverage

The engine should produce one of three decisions:

REPLACE, HOLD, or REVIEW.

It should also explain what evidence would reverse the decision.

The key measure would be:

\Delta \widehat R =
\mathbb E\[R_{\\text{candidate}}-R_{\\text{holding}}\]

where both expected returns refer to the same achievable investment window, with uncertainty displayed separately.

Initially, I would use a relative opportunity ranking instead of pretending these expected returns can be estimated accurately. As your event and shadow records accumulate, you can test whether the rankings have predictive value.

This would improve your daily process more than adding another five technical indicators.

C. Improve post-earnings drift analysis

I agree with Claude that earnings drift is one of the more worthwhile strategies to investigate.

There is substantial academic evidence for post-earnings-announcement drift (PEAD), but its strength, explanation and tradability vary by market and period. It is not a guaranteed source of short-term returns.

Your current six-test system is a good screening tool, but some important dimensions are missing.

Existing test	Recommended improvement
Earnings beat	Measure surprise against the correct consensus, not simply whether EPS increased
Raised guidance	Capture the size and credibility of the guidance revision
Share-price reaction	Compare the move against both sector performance and the implied move
Held its opening price	Analyse first-day and second-day price acceptance
Volume above 1.5×	Use relative volume and flag abnormal liquidity
Intact trend	Evaluate pre-event trend separately from post-event behaviour

I would also track earnings revision persistence: whether analysts subsequently raise forward-year estimates, rather than focusing only on the initial quarterly announcement.

A 2025 research paper reported improved return forecasts when incorporating a company’s history of earnings surprises, rather than relying on just the latest quarter. That is an interesting hypothesis for your engine to test, not a reason to assume the published result will reproduce in this game.

The crucial execution distinction is between a share’s announcement-day return and its attainable return after your next eligible FT fill. If most of the gain happens before your order can execute, an attractive-looking event study may be practically useless.

D. Introduce strategy-level shadow portfolios

You have 109 shadow ratings, but I would expand testing from individual-stock predictions to whole portfolios.

Run four virtual strategies alongside your actual model:

Strategy	Purpose
Current model	Existing composite, catalysts and risk rules
Momentum-only	Tests whether judgement scores add value
Earnings-only	Isolates the post-results continuation hypothesis
Simple control	Fixed equal-weight selection or no-change portfolio

For each, reproduce the game’s allocation limits and next-opening-price execution.

Track performance from the same start date using the same valuation conventions, and show each strategy’s incremental return against the simple control.

This gives you direct evidence about whether complexity is worthwhile.

It may turn out that a simple momentum-based portfolio outperforms the elaborate model. If so, that is a valuable result, not a failure.

E. Build a game-native performance reconciliation system

The FT rules confirm that changes take effect at the following trading day’s opening price, weights remain constant, and the platform uses Norkon market data. Official closes determine the end-of-day results.

I would add automated validation for exchange holidays, opening-price availability, share splits, dividend treatment, and currency conversion assumptions.

More importantly, compare your theoretical portfolio against the FT’s actual reported figures.

Proposed reconciliation report

FT reported value	Imported manually
Modelled value	Calculated
Difference	FT − model
Cause	Fill / FX / data / unknown
Verification	Matched / Review

I would reconcile every newly executed order and each completed trading day when the FT figures are available, rather than only during the weekly review.

Also verify the platform’s precise order cut-off. Its published 2026 terms repeatedly use BST, including for November, so the dashboard should not rely on interpreting that wording alone after the UK clock change.

2. Changes to the existing scoring and risk methods

A. Reduce the number of overlapping momentum indicators

Your scoring model contains several measurements of essentially the same underlying phenomenon:

* Moving-average relationships.
* Distance from the 52-week high.
* Relative strength.
* RSI.
* Recent price appreciation.

This creates a risk of counting one trend several times and interpreting the resulting score as stronger evidence than it actually is.

I would compare three simpler factor groups.

Factor	What it measures	Suggested test
Intermediate momentum	Sustained strength across months	Six-month and 12-month returns, excluding recent weeks
Near-term strength	Whether a trend is continuing	Five- and 20-session sector-relative performance
Catalyst quality	Whether new information supports continuation	Earnings, guidance and estimate revisions

AQR’s established momentum methodology ranks equities using the preceding 12 months while excluding the most recent month. That is a useful research baseline, although your much shorter competition horizon makes direct testing essential.

I would also stop treating RSI-based overbought status as an automatic reason to reduce a position to 5%. Strongly trending stocks can remain overbought for extended periods.

Instead, make it a warning whose usefulness is evaluated historically.

B. Separate model confidence from probability

Your current confidence formula is:

50+0.35(\text{score}-40)

with the result clipped to a range of 40–68.

This produces a numerical confidence rating, but not necessarily a meaningful estimate of the probability that a stock will rise.

I would introduce two distinct measures:

Research conviction: a qualitative assessment of the evidence, source reliability, catalyst and thesis.

Empirical probability: a calibrated estimate supported by enough completed, comparable historical predictions.

Until sufficient evidence exists, display Not calibrated rather than a misleading percentage.

The same principle applies to your day call. With just one correct prediction out of three, it should remain a research experiment and should not influence cash positioning.

C. Add a portfolio concentration and sensitivity optimiser

Your correlations and theme limits are helpful, but correlation alone is insufficient.

A portfolio containing three semiconductor stocks may have much greater exposure to an AI-capital-expenditure shock than its individual weights suggest.

I’d add a portfolio-level view measuring:

* Sector and shared business-driver exposure.
* Risk contribution using a covariance estimate, with appropriate shrinkage.
* Exposure to broad market, rates, oil and Bitcoin movements where relevant.
* Simultaneous earnings or macro-event exposure.
* Expected portfolio effect of replacing or resizing one holding.

For now, don’t treat the output as a precise forecast of losses. Historical relationships can change rapidly, particularly during market shocks.

I would also revisit the fixed 45% theme limit and 20% single-position limit. These are reasonable default guardrails, but you are participating in a short-horizon ranking exercise rather than managing a long-term pension fund. Different constraints should be evaluated through simulation, not loosened simply to pursue higher returns.

D. Introduce an evidence-based catalyst score

At present, 40 of your 100 score points come from judgement-based catalysts and revisions.

That may be appropriate, but I would make the judgement auditable.

Each catalyst should contain:

Field	Example of information captured
Event type	Guidance increase, contract, regulatory approval
First-publication time	When the information became available
Primary evidence	Company announcement or regulatory filing
Economic significance	Quantified effect, or explicitly unknown
Expectations	What the market appeared to anticipate
Price response	Market- and sector-adjusted
Thesis invalidation	What would contradict the bullish interpretation

Claude can analyse and summarise this evidence, but should not fabricate numerical precision from qualitative descriptions.

You could then test whether adding judgement-derived points improves selections relative to the price-only baseline.

3. Optimisations to the scheduled runs

I wouldn’t add many more scheduled runs. You have enough monitoring frequency already.

Instead, I would improve the purpose, reliability and outputs of the existing runs.

Run	My recommended change
Evening, 21:30	Focus on candidate ranking, replacement comparisons, catalyst quality and the next eligible execution
Morning, 07:26	Make this the authoritative confirmation step, with stronger source freshness and event-timing checks
Price refreshes	Reduce unnecessary repeated analysis; prioritise price moves that alter a thesis or next-order decision
Results-day refresh	Explicitly distinguish event reaction from the return still available at the next eligible opening
Saturday review	Add shadow-portfolio comparisons, calibration, model changes and reconciliation
Weekend news	Summarise only developments that alter a defined exposure or investment thesis

Two run-level features I would add

1. A decision-change detector

Instead of reanalysing the whole portfolio at the same depth each time, record changes since the last validated run.

For example, detect whether a catalyst has occurred, estimates have materially changed, relative momentum has reversed, or a candidate has overtaken a holding.

Prioritise deeper research on these changes. That reduces wasted analysis and makes the reasons for each decision easier to audit.

2. A data-quality gate

Your documentation, hashes and idempotent runs are good foundations.

Add explicit statuses for:

* Verified data.
* Delayed but usable data.
* Partially missing data.
* Conflicting sources.
* Execution-critical data unavailable.

If a recommended order depends on missing or conflicting critical information, the pipeline should flag it for manual review rather than confidently recommending the change.

Also make publishing the dashboard and state files an atomic operation where possible, so an interrupted run cannot leave inconsistent versions displayed.

What I would stop developing for now

I would temporarily deprioritise refinements to the daily market-direction forecast, more scenario narratives, additional macro series and new short-term technical indicators.

They might become useful. But each new input creates more opportunities for noise, spurious relationships and data errors.

Your development effort would be better spent measuring the contribution of existing signals.

4. Redesigning the Watchlist dashboard

Based on your description, the dashboard sounds functionally comprehensive, but possibly too focused on displaying all the data you’ve collected.

I would move towards an institutional equity research terminal, closer to the information hierarchy of a Bloomberg workspace, FactSet or a well-designed professional portfolio management system.

The objective isn’t to imitate those platforms visually. It’s to make important decisions easy to identify and investigate.

Recommended information hierarchy

SEEKING BETA / RESEARCH TERMINAL

Portfolio overview

Illustrative layout

Portfolio value

—

Competition rank

—

5-day return

—

Action queue

Next eligible opening

Pending portfolio changes

Not shown

Order status, evidence and latest verification belong here.

Research watchlist

Ranked by actionable opportunity

Symbol	Signal	Catalyst	Action
STOCK A	Momentum	Earnings	Review
STOCK B	Revision	Guidance	Watch
STOCK C	Unconfirmed	Pending	Research

Example structure only. No live portfolio values, stock ratings or recommendations are represented.

The biggest improvement is bringing the order queue, portfolio changes and candidate comparisons ahead of secondary statistics.

I would specifically add a Why this stock? detail panel. Clicking a watchlist entry should reveal its thesis, supporting evidence, disconfirming evidence, next catalyst, execution constraints and alternatives within the same sector.

A prompt you can paste into Claude

Redesign my existing FT Stock Picking Game watchlist dashboard so that it looks and functions like a professional institutional equity research and portfolio management terminal, rather than a generic AI-generated dashboard.

Overall design direction

Take inspiration from Bloomberg, FactSet, Koyfin and well-designed institutional portfolio management software, but do not copy their proprietary interfaces.

The visual style should be restrained, information-dense, precise and editorial. Prioritise usability and analytical clarity over decoration.

Visual design requirements

* Use a sophisticated neutral palette: near-white or charcoal backgrounds, subtle grey borders, muted text and restrained financial red/green accents.
* Avoid purple gradients, glowing elements, glassmorphism, oversized rounded cards, emojis, generic AI graphics and excessive shadows.
* Use a clear professional sans-serif font such as Inter or IBM Plex Sans, with tabular numerals for financial data.
* Establish a consistent type scale, spacing system and alignment grid.
* Prefer compact tables, sparklines and restrained data visualisations to large decorative dashboard cards.
* Use minimal border radii and thin separators.
* Maintain excellent readability in both light and dark modes.
* Do not overuse coloured status badges. Colour must communicate something useful.
* Make the interface feel like serious financial software, not a startup landing page.

Information architecture

Preserve the existing Today, Macro, Performance, Risk, Calendar and Log tabs, but improve their hierarchy.

The Today tab should prioritise:

1. Portfolio value, return, rank and distance to the target percentile where verified data exists.
2. A clear order queue distinguishing proposed, pending, submitted and confirmed positions.
3. Portfolio holdings with weights, daily performance, risk contribution and approaching catalysts.
4. A ranked research watchlist with filters, sorting, signal changes and upcoming events.
5. A compact, timestamped market context section.

The watchlist should support sorting and filtering by score, sector-relative momentum, upcoming catalysts, earnings risk, conviction and current portfolio status.

Selecting a stock should open a detailed research view showing its thesis, supporting and contradictory evidence, catalyst timeline, technical conditions, relative performance, risk, source timestamps and comparison with existing holdings.

Interaction requirements

* Prioritise desktop analytical workflows while maintaining a usable mobile layout.
* Use dense tables on desktop and intelligently collapsed rows or cards on mobile.
* Add useful hover states, expandable detail panels and contextual tooltips.
* Use skeleton or neutral loading states rather than invented values.
* Display explicit stale-data, unavailable-data and uncalibrated-model states.
* Make order-related actions visually distinct from informational alerts.
* Show source and last-updated timestamps wherever data freshness matters.
* Use text labels as well as colours to communicate status.
* Ensure keyboard accessibility and adequate colour contrast.

Charts and performance

Use restrained line charts, clearly labelled axes, consistent date windows and minimal chart clutter.

Highlight portfolio performance against appropriate benchmarks, contribution by holding, drawdowns, sector exposure and historical rank.

Prefer charts that answer an investment question. Remove charts that duplicate information or serve only a decorative purpose.

Implementation constraints

Preserve the existing data sources, calculations, logs, order validation, trading rules and underlying application functionality. Refactor presentation components where necessary without changing investment decisions or historical records.

Do not add fake sample stock data, fabricated prices, fictional performance figures or uncalibrated probabilities.

Do not introduce unnecessary dependencies or large animation libraries.

Quality standard

The finished dashboard should resemble a credible internal investment research tool that a professional analyst could use every day.

Before implementation, audit the current interface, identify its five most important usability and visual weaknesses, then redesign it systematically.

After implementation, verify all existing functionality and review the finished interface at desktop, tablet and mobile sizes.

Optimise for decision-making speed, information trustworthiness and professional visual consistency—not visual novelty.

I would run this as a focused redesign task, separate from changing your investment models. That will make regressions much easier to identify.

5. Additional features worth building

Here are four additional features I think offer particularly good value.

A. Continuous opportunity discovery

Your current intake of five to ten new names a night may be too dependent on which companies happen to attract attention.

Build a two-stage screening system:

Stage 1: Broad screening

Scan as much of the FT-eligible stock universe as your data budget permits, using inexpensive price and event signals.

Stage 2: Candidate shortlist

Select stocks with exceptional relative strength, material catalysts or unusually favourable price reactions.

Stage 3: Deep research

Only investigate the highest-potential candidates using slower fundamental, analyst and event research.

This is also an API efficiency improvement: cache historical prices and append new completed sessions rather than repeatedly downloading full histories.

Importantly, the 30-stock statistical panel should remain separate from your actual discovery universe.

B. A rejected-opportunity tracker

You already record decisions for positions you buy or sell. I would additionally record significant candidates you choose not to buy.

After five sessions, compare their outcomes with the stocks selected instead.

This could help answer questions such as:

* Are you avoiding volatile stocks that subsequently outperform?
* Do you buy strong companies too late?
* Are the judgement-based catalyst scores adding or destroying value?
* Do your guardrails exclude unusually profitable opportunities?

This is potentially more informative than traditional trade post-mortems because it measures the opportunity cost of decisions.

C. Attribution by decision type

For every change, tag its primary motivation:

MOMENTUM, EARNINGS_DRIFT, ANALYST_REVISION, NEWS_CATALYST, RISK_REDUCTION, or MACRO.

Then evaluate each category’s contribution and record the counterfactual outcome of retaining the previous position.

Be careful not to treat categories as independent when multiple signals drive the same trade.

Over time, you can identify which methods actually help, rather than judging the overall strategy based on a handful of unusually successful stocks.

D. Rank-aware simulation

The current plan switches to an endgame approach on 13 November.

I would make that transition more responsive to your actual competitive position.

Useful inputs are the latest verified rank, the portfolio return at approximately the top-2% boundary, the remaining trading sessions and the uncertainty in future returns.

For example, the dashboard could show:

Metric	Why it matters
Return needed to reach the current top-2% boundary	Quantifies the immediate shortfall
Return buffer above that boundary	Measures how exposed an existing placement is
Sessions remaining	Defines the time available
Portfolio volatility	Describes potential movement in either direction
Historical rank movement	Shows how unstable the boundary has been

These figures would not establish your probability of finishing in the top 2%, because other competitors’ portfolios will also move.

However, they would provide a more disciplined basis for altering risk than a calendar-date switch.

6. What I would implement next

You have approximately six weeks remaining until the scheduled 27 November finish. I would avoid a major overhaul of the entire system.

When	Priority	Deliverable
16–17 Oct	Validate panel methodology and actual FT fill calculations	A trustworthy testing baseline
17–18 Oct	Finish the 30-stock panel without immediately refitting weights	Recorded statistical findings
19–23 Oct	Add replacement comparisons and shadow portfolios	Direct evidence about alternative trades
24–25 Oct	Test UK clock changes and redesign the dashboard	More reliable execution and clearer UI
26 Oct–6 Nov	Expand candidate discovery and earnings evaluation	Stronger opportunity identification
7–12 Nov	Review performance by signal and assess any justified model changes	Evidence-based strategy review
13–27 Nov	Prioritise execution, verified rank information and risk management	Preserve operational reliability

One additional safeguard: preserve every live model version and its predictions. Avoid repeatedly changing a model after observing which approach would have won the preceding week.

7. Making the project valuable for your CV

Even aside from competition performance, you have the basis of a substantial independent research project.

For a finance-oriented CV, I would eventually document three things: the system you engineered, the analytical methods you tested, and the actual results—including unsuccessful hypotheses.

If the FT confirms you are eligible, a verified high placement would be an additional achievement. Otherwise, focus on the independent research and simulation rather than presenting an ineligible leaderboard result as an official competition award.

A concise project report with an architecture diagram, testing methodology, portfolio results, benchmark comparisons and lessons learned would give interviewers something concrete to discuss.

My overall assessment

Engineering and automation

9/10

Documentation and reproducibility

9/10

Portfolio risk framework

7.5/10

Stock-selection methodology

6.5/10

Statistical validation

4/10

Demonstrated predictive edge

2/10

Subjective assessment based solely on Claude’s summary, not an audit of the code, calculations or actual portfolio performance. A low score for demonstrated edge means there is insufficient evidence, not that the strategy has been proven ineffective.

I think the biggest risk now is spending the remainder of the competition perfecting an already elaborate infrastructure while not discovering whether it makes better decisions than a simple alternative.

Your strongest next step is to turn the system into a process that can answer:

“Did this information cause me to choose a better stock, at an achievable entry price, than I would otherwise have held?”

If you can answer that consistently and quantitatively, you’ll have built something much more convincing than a dashboard full of indicators—and something worth discussing in a future investment banking or quantitative finance interview.