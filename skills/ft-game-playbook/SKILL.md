---
name: "ft-game-playbook"
description: "Rules, timing, risk limits and review steps for Tim's FT Stock Picking Game entry. Use for any review, order change, watchlist update or question about the FT game portfolio."
---

# FT Stock Picking Game playbook

Tim runs an entry ("Seeking Beta") in the FT Stock Picking Game (5 Oct to 27 Nov 2026, virtual 100,000 credits). Claude researches and recommends; Tim enters every order himself.

The full procedure is kept in one place so that every scheduled run and every chat works from the same rules: the project doc `claude/ft-game-playbook.md` in the "FT Stock Picking Game" project. **Read that doc first** (Projects tool, `project_read`) and follow the part that matches the job. This skill is the short version for when the doc cannot be reached, plus a map of where things are.

## Where things live

| Thing | Where |
|---|---|
| Procedure | Project doc `claude/ft-game-playbook.md` |
| Working record | Project doc `claude/ft-game-state.md`: status, portfolio, pending order, watchlist, trade log, review log, open questions, worked examples |
| Roadmap | Project doc `claude/ft-game-roadmap.md` |
| Tim's page | Dashboard artifact https://claude.ai/artifact/8P8UwQsb4QsbZMsKNYKrUJ, with tabs Today, Macro, Performance, Risk, Calendar and Log |
| Page data | Four JSON files attached to that artifact through `datasets/stocks`, `datasets/ledger`, `datasets/history` and `datasets/macro` |
| Scripts | Two assets on the same artifact: the pipeline (`ft_pipeline`) and the screening script (`ft_score`). Their asset ids and sha256 hashes are in part B of the procedure doc |

Which part of the procedure doc to use:

| Job | Part |
|---|---|
| Full review and next order | H1 Evening review |
| Pre-open check, or a change before 08:00 UK | H2 Morning check |
| Refresh prices on the page | H3 Price refresh |
| A stock has just reported | H4 Results-day refresh |
| How the week went | H5 Weekly performance review |
| A US-only change before the US open | H6 Midday check (switched off) |
| Score or screen stocks | The `stock-score` skill and part E |
| Change what the page shows or how a run behaves | Edit the procedure doc, the page, or the script, with Tim |

Scheduled tasks: evening review (21:30 UK, Sun to Thu), morning check (07:26 UK, Mon to Fri), price refreshes (16:45 and 19:22 UK, Mon to Fri), results-day refresh (14:50 UK, Mon to Fri, acts only on results days), weekly performance review (Sat 09:12 UK), midday check (12:40 UK, switched off: the game's rules rule out same-day changes).

## Hard limits

- Never sign in to, open or operate the FT game site or any account. Tim submits orders. The FT site blocks page fetching.
- It is a virtual game. Give analysis and a clear view, with numbers.
- After 27 November 2026 the game is over: say so and stop.
- Take the date and time from the system clock (`date -u`), then convert to UK time. Never guess a timestamp.
- Never state a price, date or figure not seen in a source for the current session. Check the year on every source.
- Never delete the two script assets on the artifact, and never edit the page's own documents during a routine run.
- Never build or upload the page's data files by hand. They are written only by the pipeline script, as part G of the procedure doc describes; a hand-made file would break the page's log.

## The game in brief

- 5 to 20 stocks, each 5% to 25%. Up to 25% cash, earning nothing. No shorting, no leverage, no trading costs, unlimited changes.
- About 1,610 eligible stocks from the LSE, Nasdaq, NYSE and main European listings. The list cannot be seen from here: prefer large listings and name a substitute for each new stock.
- An order is a set of target weights. Changes fill at the next trading day's opening price: London at 08:00 UK, US stocks at the US open. Weights reset to target at each close.
- **Performance is weighted**: the portfolio's return is the sum of each holding's weight times its return. A 15% position rising 2% adds 0.30 points; a 5% position rising 5% adds 0.25. Size and explain positions on that basis.
- An order never fills before a gap. For US results after the close on day D, order before 08:00 UK on D. For US results before the open on D, the stock must be held or sold by the open of D-1. After any report the earliest exit is the next open.
- US session is 14:30 to 21:00 UK, except 13:30 to 20:00 in the week of 26 Oct. US markets are closed on 26 Nov and close early on 27 Nov.

## Objective and guardrails in brief

- Target: roughly the top 2% of players, not first place. No lottery-ticket bets, but the portfolio must differ from the index.
- 6 to 10 holdings; largest normally 20% or less; one theme no more than about 45%; cash 0% to 25% by regime; no position above its volatility cap; results-only and momentum positions capped at 10%.
- A new core position needs a score of 60 or more and no "downtrend" or "below 50-day average" flag. A holding below 45, or in a downtrend, is replaced unless a dated catalyst inside five trading days justifies 5% or less.
- News momentum: enter at 5% to 10% only after follow-through (a close above the open, in the upper half of the range, on heavy volume). Exit on the first heavy-volume close below the open.
- Results ahead: weight times the options-implied move stays at or below 0.6 points of the portfolio.
- Every recommendation carries a confidence rating from 1 to 100: the estimated chance the position beats the S&P 500 over the five trading days after its fill. Start from the script's anchor and move at most 5 points with a stated reason.
- From 13 Nov: if Tim's rank is inside the target, cut volatility; if outside, keep risk on.
- Watchlist: five to ten new candidates every evening, with the weakest leaving so the list stays at about 20. Each stock has a strength band: strong (score 60 or more, above its 50-day average, no downtrend), weak (score under 45 or a downtrend), middling otherwise.
- Macro: every review reads government bond yields (US 2-year, 10-year and 30-year; UK, German and Japanese 10-year) and Brent, and weighs the day's news against them. Rising yields hurt shares, growth most; rising oil helps energy holdings and hurts most else.
- Day call: each evening gives a bull case, a bear case and the estimated chance that the next session closes up, for the S&P 500 and for the portfolio, from similar past days. It is logged and scored. A day's direction is close to a coin flip, so the call never changes the order by itself.

## Output style

- Start with "Tim,". British English, no em-dashes, UK times, concise, tables where they help.
- Lead with the verdict and the full order table (Stock, Weight, Score, Confidence, Change, Reason, with cash as a row), then what changed in the order and the watchlist.
- Explain results as weighted contributions, not raw moves.
- Be direct. If Tim's idea does not hold up, say so and show the numbers.
- End with sources as markdown links.

## What only Tim can supply

- Portfolio value, leaderboard position and number of players, ideally after each Friday's close, and the return of the player on the top 2% line if shown.
- Whether an order was entered and when, and any stock missing from the game's list.