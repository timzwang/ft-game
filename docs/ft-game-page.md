# FT Stock Picking Game: page notes

Written Mon 12 Oct 2026, 01:40 UK, after the third design pass on Tim's page (https://claude.ai/artifact/8P8UwQsb4QsbZMsKNYKrUJ); updated Mon 12 Oct, about 18:30 UK, after a fourth, smaller pass on the watchlist and the order. Scheduled runs do not need this doc; it is for any chat that changes the page.

## What changed on 12 Oct (third pass, 01:40)

- The page was rebuilt at Tim's request to be denser and closer to Trading 212 and TradingView. Same six tabs (Today, Macro, Performance, Risk, Calendar, Log), same four data files, same figures.
- Layout: grey desk with white panels. One column on a phone, two on a tablet, three on a wide screen (list, chosen stock, order and events).
- Today: headline figures with a one-line market tape; an Order panel showing the full order with weights, "New" marks and the stocks to sell; a holdings map where area is weight and colour is the last session's move; the watchlist grouped by strength.
- Macro, Performance, Calendar and Log are split into short views chosen with buttons, so no view is a long scroll.
- No table is wider than the screen. Every table is a grid whose columns fit; long text drops to its own line.
- Text longer than one sentence is shown as bullets. Tim asked for bullets in place of blocks of text.
- Company logos sit beside every stock.

## What changed on 12 Oct (fourth pass, about 18:30)

- Phone watchlist and holdings list: one stock per row (logo, ticker with score, name or status, 20-day line, price, and the day's move in a green or red pill), in place of the two-column tiles where the score badge ran into the day's move and names were cut off. Below about 350px wide the 20-day line is dropped.
- Statuses are shorter and "Watching" is no longer printed, so only stocks with something to note carry a status ("Needs follow-through" now reads "Needs 2nd day").
- Order panel: always one column, so names are never cut to two letters on a phone; weights slightly larger.
- Phone header: the price time sits on its own line instead of running into the title; tabs fit without being clipped.
- Tablet: the portfolio value takes its own row above the four headline figures, so their labels no longer wrap.
- Holdings map: a tile's weight and points line is shown only where it fits.
- Checked on a local copy at 375, 390, 820 and 1440px wide, in light and dark, with the live data files; no horizontal scroll at any width.
- The page as it was before this pass is kept on the artifact as the asset `9ab128e46f7aecc2db12b8d65c8b041a` (page_before_watchlist_pass_2026-10-12.txt). To go back, write its text to `files/index.html`.

## What changed on 18 Oct (cut-off)

- The order cut-off on the page moved from 08:00 to 07:00 UK (playbook 6.4): one constant, `CUTOFF`, next to `usOpenUk` in `files/app.js`, sets the Order panel's "Proposed" state, its countdown, its call to action and the step label; the help text in `files/index.html` says the same. If the FT confirms 08:00, change that one constant and the help sentence back. Only the two page documents changed (app.js version 2, index.html version 13).

## What changed on 19 Oct (playbook 6.10, pipeline 7.3)

- Risk tab, results table: the budget per report now comes from the ledger's `meta` row `results_budget`, which pipeline 7.3 writes on every run (`{"default", "windows": [{"from", "to", "budget", "why"}]}`). Reports dated 27 to 30 Oct show "Within 1.0" or "Over 1.0"; others 0.6. Until the first 7.3 run publishes that row, every report shows 0.6, as before.
- Stale-price marker and FT reading age: a US session counts as complete 15 minutes after its close (21:15 UK, 20:15 UK in the week of 26 Oct, 18:15 UK on 27 Nov), and 26 Nov is not counted as a session (`US_CLOSED`, `usFinalUk`, `isUsSession` in `files/app.js`). Before, every weekday counted and the 21:15 rule applied all year, so 26 Nov would have shown the page a session behind.
- The day call's help text no longer says it "nudges cash": it reads "A research record only: it never changes the order or the cash level" (part E since 16 Oct).
- Only `files/app.js` changed (version 3). Checked with `node --check` and by running the changed functions in Node on sample data; the page was not rendered.

## What changed on 21 Oct (playbook 6.12)

- Deployed the wording merged with pipeline 7.5 on 19 Oct (PR #4, approved by Tim) but never published: the watchlist's "Conviction" tooltip now says the anchor is the score rescaled (50 + 0.35 x (score - 40), held between 40 and 68), a ranking and not a measured chance of beating the S&P 500; the calibration banner no longer hides itself at 150 settled ratings and says the count is a minimum before a test, not proof. Only `files/app.js` changed (version 4, equal to the repository's `page/app.js`, sha256 `1583ef5d...1cc3`). Checked with `node --check`; the page was not rendered.

## What changed on 26 Oct (playbook 6.14)

- The order cut-off on the page moved back from 07:00 to 08:00 UK, the cut-off FT Customer Care confirmed to Tim on 21 Oct (UK local time all year): the constant `CUTOFF` in `files/app.js` and the "Order states" help sentence in `files/index.html`. Nothing else changed. Checked with `node --check`; the live files matched the repository's `page/` copies byte for byte before the change.

## What changed on 3 Nov (playbook 6.15): Liquid Glass

Tim asked for the page to look like Apple's Liquid Glass and Apple's own dashboards, as clean as possible, with the important information clear and no captions under numbers. `files/index.html` (version 15) and `files/app.js` (version 6) were rewritten; the data files and the pipeline did not change.

- Look: translucent panels with a bright rim over a soft fixed wallpaper, capsule controls, a sliding lens under the selected tab, the system font (San Francisco on Apple devices), system green, red and blue, Apple Stocks style solid day pills. Light and dark. `prefers-reduced-transparency` falls back to solid panels. The IBM Plex font file (`files/fonts.css`) is no longer linked.
- Today: portfolio value, return and chart first; four tiles (against the S&P 500, last session, rank, gap to the top 2%); the Order card beside them (all target weights, "Nothing to enter" or a blue "Enter before 08:00 UK"). Then holdings, a two-column watchlist (top ten and "Show all" on a phone; score badge coloured by strength), and Markets, Coming up and Alerts.
- Removed: captions under figures, the four-step order tracker, the watchlist's held/all and toggle filters, source lines, per-chart subtitles, the theme limit line and the results budget column (both suspended by the endgame stance), wording that quoted suspended rules, and the "Last run" and "Stale" columns. The next-session call now lives only on the Macro tab: it never changes the order.
- New logic: `standing` adds the gap to the top 2% (the latest `reported` row's `value`, the return of the player nearest the line, minus the estimated return); results events for stocks off the list are hidden (`relevantEvent`); events that have already happened today are dropped from Coming up (`eventPassed`); a non-held stock shows "Sold <date>" instead of an old "Exit signal"; the Alerts card shows only the holdings, Portfolio, Market and System, two lines each (everything is in Log).
- Rounding: figures round half away from zero, so the page shows -8.40% where the reviews do.
- The tab labelled Returns is still `performance` in the code.
- Checked on a local copy with the live data files at 390, 834 and 1440px, light and dark, all tabs, with a changed order simulated; no horizontal scroll at any width. The old page, both files, is kept on the artifact as asset `53081510b3a7830082995aec759e3ce3` (page_before_glass_2026-11-03.txt). To go back, split it at the `=== app.js ===` line and write each part to its file.

## Things a later chat must keep

- The Order card reads the latest alert whose `stock` is "Order", exactly as the old banner did: text starting "Changed" or "Revised" shows the blue "Enter before <cut-off>" capsule until the cut-off on the effective day (the cut-off is the constant `CUTOFF` in `files/app.js`, 08:00 UK from 26 Oct (07:00 from 18 to 26 Oct), playbook part C; London fills still show 08:00, the LSE open); "No change" shows "Nothing to enter". The blue "new" dots and the Sell line come from the `trade` rows with the latest `effective` date, until that date's US open.
- Logos are a fifth dataset, `datasets/logos`, a JSON file of rows `{key, src}` with keys like `US:XOM` and `UK:SHEL` (UK keys use the ticker as it appears in stocks.json, for example `UK:BP.`). About 550 names. A stock with no logo shows its initials. To add one, rebuild the file and update that dataset; the pipeline never touches it.
- The page before the third pass is kept on the artifact as the asset `c2263c65f6b1c81a12ccd051709c0630` (page_before_redesign_2026-10-11.txt).
- Superdesign was asked for but is not signed in for this account, so it was not used in either pass.
