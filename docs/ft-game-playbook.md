# FT Stock Picking Game: playbook (core)

Playbook version 6.11, 19 Oct 2026 (evening): after ChatGPT's follow-up review, Tim approved two additions that change no rule, score or order. Pipeline version 7.4 (part B): every change of order records, before it fills, the points it is expected to add over five sessions against keeping the order before it, why, and what would show it wrong (`order_expected`, data doc G3; evening run step 6; morning check step 5). It is locked once the change fills, and the STANDSTILL test later sets the actual figure beside it (EXPECTED BENEFIT, G4; part E). And a data check in the repository (`scripts/check_data.py`, run by GitHub on every data push and about two hours after each evening and weekly review), which shows a red run if the mirror did not publish, the data stop short of the latest US session, the files do not add up, a holding's results date has no event, or a report inside five sessions has no implied move. With no expectation given every figure is identical to 7.3. Version 6.10, 19 Oct 2026: after ChatGPT's repository review of 18 Oct, Tim approved pipeline version 7.3 (part B) and one rule change. The rule: reports dated 27 to 30 Oct are judged against a results budget of 1.0 points instead of 0.6 (part E), because the entry is about 5 points behind the top 2% line. Version 7.3: confidence and shadow ratings settle only on exact sessions; a held stock with a results date but no results event is flagged (`RESULTS MISSING`); a repeated FT reading fills in the top 2% line; 26 Nov is not a US session and 27 Nov closes at 18:00 UK; `market_closed` and estimated-open marks are kept. Also new: regression tests in the repository (`tests/`, run by GitHub on every code change), the broad scan's workflow runs only from `main`, its libraries pinned, and the page's Risk tab, stale-price marker and day-call wording corrected (page notes). With complete prices every figure is identical to 7.2. Version 6.9, 18 Oct 2026: the evening and weekly review tasks were recreated (same prompts, times and automatic approval) from a chat with the GitHub repository attached, because the old tasks, made before the repository existed, start without it and a plain clone asks for credentials; the 6.8 test passed only because its own task had been made from such a chat. A one-off run from a task made the same way pushed a commit (8d9ed20). The old tasks are kept, switched off. Any new scheduled task that needs the repository must be created from a chat that has it attached. Version 6.8, 18 Oct 2026: a one-off test showed that scheduled runs can reach the GitHub repository (it is already cloned in the session, and git over HTTPS needs no credentials), so G6 and G7 stay in the evening and weekly runs with a new step 1 in the data doc. Version 6.7, 18 Oct 2026: pipeline version 7.2 (part B), approved by Tim after ChatGPT's challenge of Claude's audit verification: a price row given without an open is never used as a fill price; a session with an unpriced holding, or a buy or sale without a traded open, is not recorded until the row arrives (PERFORMANCE INCOMPLETE; `market_closed` for a shut market); a drift reporter whose next open never arrives is not scored (data doc G3 and G4, rules doc part E). With complete prices every figure is identical to 7.1. Version 6.6, 18 Oct 2026: a handoff log between Claude and ChatGPT in the repository's `handoff/` folder, read at the start and written at the end of every session with Tim (part B). Version 6.5, 18 Oct 2026: after Claude's second, read-only review of the outside audit, Tim approved a corrected standstill test (pipeline version 7.1, part B; rules doc part E): each week is now judged against the order in force before it, so a Monday rebuild counts, and the first order (9 Oct) is kept as a never-changed baseline, as entered and fully invested; the missing prices for RTX, Lockheed Martin, Nvidia and Goldman Sachs were added to the price store; the "+0.86 points" claim of 17 Oct is corrected. Version 6.4, 17 Oct 2026: after an outside audit of the system (ChatGPT, 17 Oct) and Claude's assessment of it, Tim agreed fourteen changes: pipeline version 7 (part B; the standstill test, drift settled from the next open, the results total, FT reconciliation and the judgement test, all in part E and G4); a cut-off of 07:00 UK until the FT confirms what it is after the clock change, with the morning check moved to 06:36 UK (part C); the score frozen for the rest of the game; stocks sold in the last five sessions kept on the watchlist; confidence ratings labelled "not calibrated". Version 6.3, 16 Oct 2026: the broad scan (roadmap item 43; data doc G7; evening review step 4; weekly review). Version 6.2, 16 Oct 2026: two rule changes in part E (the day call never moves cash; "overbought" is a warning, not a 5% cap), agreed by Tim after an outside review; the roadmap's phase 6 sets out what comes next. Version 6.1, 16 Oct 2026: the evening and weekly runs now mirror the data and the state doc to a private GitHub repository (G6), and the state doc is always written from a local file (part J). Version 6, 15 Oct 2026: the playbook used to be one long doc; at Tim's request it is now split so that each run reads only what it needs. This core doc holds the parts every run needs (A to D, I to K) and the routing table below. Version 6 also adds, at Tim's request, the panel test (a fair test of the score on 30 stocks fixed in advance) and the earnings-drift scan. Earlier versions: 5 (9 Oct) yields, oil, the day call, nightly watchlist intake, strength bands, moving averages, release tracker, calibration log; 5.1 weekend news check; 5.2 quiet-day rule; 5.3 crypto tracking; 5.4 the market data service.

This is the single procedure for every scheduled run and every hand-run review of Tim's entry ("Seeking Beta") in the FT Stock Picking Game. Each scheduled task tells its run to read this doc and carry out one section of part H. Runs read these docs; they do not edit them. Changes are made in a conversation with Tim.

## Which docs to read

Read this doc first, then the docs listed for the part your instructions name, in the same turn (one `project_read` per doc, sent together). Every part keeps its old letter and number, so an instruction such as "carry out part H1 under parts A to G" still means the same thing.

| Part | Run | Also read |
|---|---|---|
| H1 Evening review | 21:30 UK, Sun to Thu | `claude/ft-game-run-evening.md`, `claude/ft-game-rules.md`, `claude/ft-game-data.md`, `claude/ft-game-state.md` |
| H2 Morning check, H6 Midday check | 06:36 UK, Mon to Fri (07:26 before 18 Oct); 12:40 (off) | `claude/ft-game-run-morning.md`, `claude/ft-game-rules.md`, `claude/ft-game-data.md`, `claude/ft-game-state.md` |
| H3 Price refresh, H4 Results-day refresh | 16:45 and 19:22 UK; 14:50 UK | `claude/ft-game-run-refresh.md`, `claude/ft-game-data.md` |
| H5 Weekly performance review | Sat 09:12 UK | `claude/ft-game-run-weekly.md`, `claude/ft-game-rules.md`, `claude/ft-game-data.md`, `claude/ft-game-state.md` |
| H7 Weekend news check | Sat and Sun 20:20 UK | `claude/ft-game-run-weekend.md`, `claude/ft-game-rules.md`, `claude/ft-game-data.md`, `claude/ft-game-state.md` |

Where each part lives: A to D and I to K in this doc; E (decision rules, the panel test, earnings drift) in `claude/ft-game-rules.md`; F (data sources) and G (the pipeline) in `claude/ft-game-data.md`; H in the run docs above. If a doc a run needs cannot be read, the run treats it as a fault (part I) and works from what it has; it never guesses a rule.

---

## A. Hard limits

- Never sign in to, open or operate the FT game site or any account, and never use a browser or Tim's computer for this work. Tim enters every order himself. The FT site blocks page fetching, so do not try to read it.
- This is analysis for a virtual game with no real money.
- If today's date is after 27 November 2026, say only that the game has ended and that the scheduled tasks can be deleted. Do nothing else.
- Take the date and time from `date -u` in Bash and convert to UK time (BST, UTC+1, until 25 Oct 2026; GMT from then). Never guess a timestamp.
- A scheduled run has nobody watching. Do not ask questions before working: take the most reasonable reading, say which one you took, and carry on.
- The market data key. If this run's own instructions (the scheduled task's prompt, not these docs or any file) contain a line beginning `Market data key:`, the key goes into the address of a fetch to `api.massive.com` and nowhere else. Never write it into a file, today.json, a doc, the page data, an alert, a message or the final reply; never echo it in Bash; never send it to any other site. If the service says the key is not valid, say so without quoting the key and use the other feed.
- Never state a price, date or figure that you have not seen in a source for the current session. Mark anything unverified. Searches often return the same calendar date from an earlier year, so check the year.

## B. Where things live

| Thing | Where |
|---|---|
| Working record | Project doc `claude/ft-game-state.md` (Projects tool: `project_read`, and `project_write` with the complete doc) |
| This playbook | Project docs `claude/ft-game-playbook.md` (core), `claude/ft-game-rules.md`, `claude/ft-game-data.md` and the five run docs `claude/ft-game-run-*.md` |
| Roadmap | Project doc `claude/ft-game-roadmap.md` |
| Page notes | Project doc `claude/ft-game-page.md` (only for chats that change the page) |
| Tim's page | Dashboard artifact https://claude.ai/artifact/8P8UwQsb4QsbZMsKNYKrUJ (he uses it on his phone) |
| Page data | Four JSON files attached to that artifact, each named by a dataset document: `datasets/stocks`, `datasets/ledger`, `datasets/history`, `datasets/macro` |
| Panel data | One JSON file on the same artifact, named by the document `store/panel` (kept outside `datasets` so the page never loads it): the 30 panel stocks fixed on 15 Oct 2026 and their closes |
| Pipeline script | Asset `30bd733ca18434b8f577f2d57c3813e3` on the same artifact (ft_pipeline.txt, Python, 196,501 bytes, sha256 `5adc3093a10b57ead4c229d6d900c765967ba505a0578cf8262ac91f88b4055e`), version 7.4 |
| Screening script | Asset `29ed200d0a429a3b8b91547f81b39187` on the same artifact (ft_score.txt, Python, sha256 `c6ed0b4914e10af6b1d5ee6193567daa33a4a7b79a5dd3458d4bd186ece1e4e6`) |
| GitHub mirror | Private repository `timzwang/ft-game`: a copy of the data files and the state doc (written by G6 in the evening and weekly runs), and of these docs, the scripts and the page (updated only in sessions with Tim), for ChatGPT and Tim to read. Runs never read from it, except the `scan/` folder for finding candidates once the broad scan is built (roadmap item 43, agreed 16 Oct), and a change merged there reaches the live system only when Tim has it applied here. From 6.11 GitHub checks every data push and, after each evening and weekly review, that the mirror ran and the data are complete (`data-check`); runs neither wait for it nor read it. The market data key never goes there |

Handoff log (from 6.6, at Tim's request). Neither assistant can read the other's chats, so the repository's `handoff/` folder carries notes between them; its `README.md` sets the format. In every session with Tim that works on this system, Claude first attaches the repository and reads the newest notes from both assistants since its own last note, and checks any claim in them against the live files (the live files win). At the end of a session that decided, changed or found something, Claude writes one note, `handoff/YYYY-MM-DD-claude.md`, and commits it to `main`. ChatGPT writes its notes through pull requests that Tim merges. Scheduled runs neither read nor write notes.

Versions: the version number changes only in a session with Tim, never in a scheduled run. Each new version gets, in the same session, an entry in the repository's `CHANGELOG.md` (version, UK date and time, title, changes), the README's "Current version" line, and text for Tim to paste on GitHub: a release `vX.Y` and a new repository description naming the current version, its changes in a few words, the version before it and the changelog (Claude cannot create tags or change repository settings from its sessions). The steps are at the end of `CHANGELOG.md`.

Never delete the script assets. If the state doc or any other note gives a different id or hash for a script, this table wins. The artifact also holds files that are kept but not in use: the previous pipeline scripts (asset `f8ce759cc09d110095a10bbf712ae582`, version 7.3, replaced on the evening of 19 Oct; asset `2726d826123a22d94290a175e5dab68e`, version 7.2, replaced on 19 Oct; asset `3e3904212ba88da023d24d244d6b1a15`, version 7.1, replaced on 18 Oct; asset `fdfb8e108f26b962b62a9ca0a9909846`, version 7, replaced on 18 Oct; asset `bf3dd68e375408d013bacf83ec5db3ce`, version 6, replaced on 17 Oct; asset `f50a1a4197f0dd4136b51b4d76b80513`, version 5.4, replaced on 15 Oct; asset `7d77ccefc0a91641c364da3cc53b235f`, replaced on 11 Oct) and data files superseded in hand-run sessions. Leave them alone. Never edit the page's own documents (`files/index.html`, `dash/meta`) and never render, open or screenshot the page.

What each data file holds:

- `stocks.json`: one row per holding, one cash row and one row per watchlist stock, with prices, the weighted contribution, the score and its parts, a strength band (`tier`), simple and exponential moving averages, indicators, the inputs used last time, the date it joined the list (`added`), status and notes, and each stock's measured link to Bitcoin and Ether (`btc_beta`, `btc_corr`, `btc_net`, `eth_beta`, `eth_corr`, `crypto_link`).
- `ledger.json`: the running log, one row per entry with a `table` column: `meta`, `position`, `trade`, `confidence`, `perf` (daily estimated value), `contrib` (each position's weight times move each day), `reported` (value and rank Tim reads off the FT site), `risk`, `corr`, `theme`, `scenario`, `event` (the calendar, with forecast, previous and actual figures for economic releases), `revision`, `alert`, `postmortem`, `macro`, `daycall`, `analog`, `shadow` (a rating for every scored stock every evening), `drift` (every reporter the earnings-drift scan looked at, with its verdict and, five sessions later, its result), `standstill` (what each change of order added against not making it, rebuilt every run), `expect` (from 7.4: the expected benefit recorded with each change of order before it filled) and `calib` (what the shadow ratings, the panel test, the drift record and the old backtest say).
- `history.json`: daily open, high, low, close and volume for every stock and for SPY, with up to a year of closes where collected (two years for SPY), plus `OIL`, `SHEL-US`, `BP-US`, `IBIT` and `ETHA`, the reaction-day rows of drift reporters until they settle, and every session for the stocks of the first order (RTX, Lockheed Martin, Nvidia, TSMC and the rest), which the inception standstill prices to the end of the game.
- `macro.json`: one row per series per day (`date`, `series`, `value`): `us2y`, `us10y`, `us30y`, `uk10y`, `de10y`, `fr10y`, `it10y`, `jp10y` in percent, `brent`, `wti`, `natgas`, `gold` in dollars, and `btc`, `eth`, `sol`, `xrp`, the coin prices in dollars at the US close.
- `panel.json`: `frozen` (2026-10-15), `rule` (how the members were chosen, and any swap), `test` (the measure and the verdict rule, fixed in advance), `members` (rank, ticker, name) and `closes` (for each member, a list of [date, close]).

Scheduled tasks: evening review (21:30 UK, Sun to Thu), morning check (06:36 UK, Mon to Fri; 07:26 until 17 Oct), price refresh (16:45 UK, Mon to Fri), late price refresh (19:22 UK, Mon to Fri), results-day refresh (14:50 UK, Mon to Fri, acts only on results days), weekly performance review (Sat 09:12 UK), weekend news check (Sat and Sun 20:20 UK). A midday check (12:40 UK) exists but is switched off: the game's rules rule out same-day changes (part C).

## C. The game

- Runs 5 Oct to 27 Nov 2026 (ends 23:59 UK). Virtual 100,000 credits. Highest percentage return wins. Final values use official closing prices on 27 Nov.
- 5 to 20 stocks, each 5% to 25%. Up to 25% cash, which earns nothing. No shorting, no leverage, no trading costs, unlimited changes. Dividends are reinvested.
- About 1,610 eligible stocks from the LSE, Nasdaq, NYSE and main European listings. The list cannot be seen from here: prefer large, well-known listings and name one substitute for every new stock.
- An order is a set of target weights. Changes fill at the next trading day's opening price: London stocks at 08:00 UK, US stocks at the US open. Weights are reset to target at each close.
- **Performance is weighted.** The portfolio's daily return is the sum over holdings of weight times return. On a day a change fills: kept weight earns close over previous close, added weight earns close over that day's open, sold weight earns that day's open over previous close. Every portfolio figure in this work is a sum of weight times return, never an average of returns. A 15% position rising 2% adds 0.30 points; a 5% position rising 5% adds 0.25.

Timing: an order never fills before a gap, so a position must be in place, or gone, before the event.

- US results after the close on day D: the order must be entered before the cut-off (07:00 UK, below) on day D.
- US results before the open on day D: the stock must be held (or sold) by the open of D-1, so the order goes in before the cut-off on D-1, which means the evening review of D-2.
- UK and European results at 07:00 UK: held from the previous day.
- After any report the earliest exit is the next open, after the gap. Likewise the earliest entry after a report is the next open after its reaction session, which is what the earnings-drift rule uses.
- Weekends work the same way. A holding is valued from Friday's close, so a Monday gap in something already held cannot be dodged: selling at Monday's open still takes the gap. What a weekend order can do is avoid, or catch, the move after the open.
- US session: 14:30 to 21:00 UK, except 13:30 to 20:00 UK in the week of 26 Oct (UK clocks go back on 25 Oct, US clocks on 1 Nov). US markets are closed on 26 Nov and close early (18:00 UK) on 27 Nov.
- Cut-off. Up to 23 Oct an order entered before 08:00 UK counted for that day (Tim's first order, entered at about midnight UK, filled the same day). The FT's 2026 terms state times in BST even for November, so after the clocks go back on 25 Oct the cut-off may be 08:00 BST, which is 07:00 UK. Until the FT or the test below settles it, treat **07:00 UK** as the daily cut-off for everything: every message, alert and deadline says "before 07:00 UK". It costs nothing, since Tim normally enters orders the evening before. An order entered once the trading day has begun waits for the next trading day, US stocks included; there is no same-day midday change.
- Cut-off test (agreed 17 Oct). At about 07:15 UK on Mon 26 Oct Tim moves one point of weight between two highly correlated holdings (Exxon Mobil 15 to 14 and Chevron 15 to 16, or the same between whichever oil majors are held). If the game fills it on Mon 26 Oct, the cut-off is 08:00 UK; if on Tue 27 Oct, it is 07:00 UK. Tim says which in the project chat; the next evening review records the change through `order` (with `effective` set to the fill date he reports, or 27 Oct if he has not said) and notes the answer in section 8 of the state doc. Until then the 07:00 UK rule stands.
- The game's "Today" figure for a London or European stock can read 0.00% in the evening even when the stock moved, so do not read a zero there as proof that a position was not held.

## D. Objective, guardrails and rank

Target: finish in roughly the top 2% of players, not first place. Tim wants a credible result for his CV, so no lottery-ticket concentration. Top 2% still needs a return well above the index, so the portfolio has to differ from it.

Standard guardrails:

- 6 to 10 holdings. Largest position normally 20% or less. One theme no more than about 45%. Cash 0% to 25% by regime.
- No position above its volatility cap (`weight_cap_pct` from the pipeline: about 30 divided by the stock's average true range in percent, so 15% for a stock that ranges 2% a day and 10% for one that ranges 3%).
- A position bought only for a results report, as a news momentum trade or as an earnings-drift trade, is capped at 10%.
- Turnover is free, so change the order whenever the evidence supports it, but every change needs a reason that will still make sense tomorrow.
- In a risk-off regime the only defences are cash (25% at most) and low-beta names. Rank is relative, so falling less than other players still helps.

Sizing by weight times edge:

- Size positions by expected contribution, which is weight times expected excess return. The strongest cases with the smallest daily ranges get the largest weights, up to their caps.
- A 5% position hardly moves the portfolio. Use 5% only for a trial momentum or drift position or a capped hold through results. A core position is 10% to 20%.
- Check the Risk output of the pipeline before finalising. If one theme supplies more than about 60% of the portfolio's risk, or two holdings have a correlation above 0.85 and together exceed 30%, say so and either trim or state why the concentration is deliberate.
- Check the scenario lines. No single listed scenario should cost more than about 3 points of the portfolio unless the review argues for that exposure.

Rank-aware stance (use the latest `reported` row in the ledger; the pipeline prints it):

- The target line is position `floor(players x 0.02)` or better. If Tim supplies the return of the player on that line (`top2_return_pct`), the gap to it in points is the number that matters.
- Outside the target with three or more weeks left: standard guardrails, cash usually 0% to 15%. Do not hold cash for comfort.
- Outside the target from 13 Nov: keep risk on. Cash 0% to 10%, six to eight holdings, and the results risk budget in part E rises from 0.6 to 0.8 points (reports dated 27 to 30 Oct already have 1.0, agreed 19 Oct). Never break a guardrail to chase.
- Inside the target before 13 Nov: no change of approach.
- Inside the target from 13 Nov: protect it. Cash 15% to 25%, eight to ten holdings, nothing above 15%, no holding through results, prefer stocks with a small daily range.
- A rank read in the first few sessions means little, since most players are bunched near zero.
- From 13 Nov the evening review states the stance in its first lines from the latest reported rank. If that rank is more than a week old, ask Tim for his value and rank (and the return of a player near the line, which he can see by opening other players' portfolios) in that evening's message.

## I. Output style

Every message starts with "Tim,", with one exception: a quiet reply starts with the words "No change" and has no "Tim," in front, because the first words of a reply are what shows in the notification on Tim's phone. British English. No em-dashes anywhere. UK times. Concise, with tables where they help. Be direct and give a view; if an idea of Tim's does not hold up, say so plainly and show the numbers. Flag only significant risks. Talk about weighted contributions, not raw moves, when explaining what happened to the portfolio. End with sources as markdown links. Each run doc gives that run's exact output.

**When Tim is told.** The reviews run every day so that the order can change on any day, but Tim does not want to check every day. A run sends him a message only when there is something for him to do:

| Run | Sends a message |
|---|---|
| Evening review | On a change evening: the order for the next session differs in any weight from the order in force, or something is needed from Tim before the next cut-off |
| Morning check | Only when it revises last night's order |
| Weekly review | Always: it asks for his value and rank |
| Weekend news check | Only for an item rated A |
| Price refreshes, results-day refresh | Never: nothing can be entered during the trading day, so their alerts go on the page |

- On every other occasion the run sends nothing through SendUserMessage and ends with the short fixed reply its run doc gives. Do not pad that reply with a market read, tables or sources: anything that reads as news may reach Tim's phone as a notification.
- The work is the same either way. A quiet evening still carries out all of H1, publishes the page and writes the state doc. The watchlist changes, the alerts and the day call are on the page; none of them makes a message by itself.
- A fault is never a quiet day. If a run cannot get as far as checking the order (the state doc or a playbook doc it needs cannot be read, the script's hash does not match, the pipeline ends in an error that cannot be fixed), say so in the first line, say that the order in force stands until Tim hears otherwise, and send it through SendUserMessage.
- A change message must be enough to act on by itself: the full order, what changed, and the cut-off. Its last line is "If you cannot enter this before 07:00 UK, say so in the project chat so the log can be corrected."
- Every order table headed for Tim labels the rating column "Confidence (not calibrated)" until about 150 shadow ratings have settled and the panel test or the judgement test (part E) supports reading the ratings as probabilities. The page already marks them uncalibrated.
- The order is assumed entered once its message has gone (H1 step 1). The check on that assumption is the weekly comparison of the estimated value with the figure Tim reads off the FT site.

## J. The state doc

`claude/ft-game-state.md` is the narrative record; the ledger is the numerical one. The doc's status section also carries the latest day call (session, green or red, figure, usual rate), the macro backdrop, Bitcoin's price and trend, and the panel test's latest line, one line each, so a morning run can quote them before the files arrive. The evening review rewrites the doc at the end of every run (it replaces the whole doc, so include everything): status, current portfolio with weights, ratings, scores and flags, pending order, watchlist with statuses and promotion triggers, trade log (one row per order change with the reason), review log (add one or two lines, keep the latest 15), regime notes and the near calendar, open questions, worked examples and the list of sources. Performance figures, the confidence log, the day-call record, the macro figures, the calibration and panel tables, the drift record and the full calendar live in the ledger; the doc need only carry the latest estimated return and reported rank. If Tim says he did not enter an order, entered something different, or found a stock missing, correct the doc and put the correction through the pipeline (a changed order through the `order` list of the next run, a changed fill date through `fixes`). The morning and midday checks write the doc only when they change the order. Section 3 (pending order) records, for the latest change, the time its message went out; the order is taken as entered unless Tim says otherwise. The weekend news check changes only the "Weekend log" in section 7 and adds a line to the review log.

How the doc is written, by every run that writes it: compose the complete doc in a local file inside the working directory (for example `work/ft-game-state.md`, with the Write tool), then `project_write` with `path` `claude/ft-game-state.md` and `local_path` set to that file's full path, starting with `/` (a relative path was refused on 16 Oct). Never pass the doc as inline `content`. The evening and weekly runs then commit that same file to GitHub (G6), so the two copies are byte for byte the same.

## K. What only Tim can supply

- Portfolio value, leaderboard position and number of players, ideally after Friday's close each week, and the return of the player on the top 2% line if shown. A value is comparable with the estimate only if it was read after the US close (after 21:15 UK; 20:15 UK in the week of 26 Oct) or taken from the closing point of the game's own value chart: figures read during the US session differed from the estimate by up to 181 credits, closing ones by under 40 (17 Oct check). The pipeline's RECONCILE lines set each figure beside the estimate.
- Whether an order was entered, when, and any stock missing from the game's list. With messages going out only on change days, the one thing he must report is a change he could not enter before the cut-off.
- What the game shows as the fill date and price of a new position.
- Agreement before any change to the score's weights or the confidence anchor, and before any swap in the panel.
