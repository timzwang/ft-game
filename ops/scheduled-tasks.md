# Scheduled tasks

The schedule and instructions of the Claude scheduled tasks that run this system, copied on Fri 16 Oct 2026 at about 01:15 UK; the morning check updated on Sat 17 Oct 2026. All run in Anthropic's cloud (not on anyone's computer), with automatic approval, on model `claude-opus-5-5`. Times are UK local (`CRON_TZ=Europe/London`).

**Redacted:** the evening and weekly review prompts contain a market data API key in a line beginning `Market data key:`. It is replaced below by `<REDACTED: held only in the scheduled task>`. The key must never be written into this repository.

This file is a copy for reading. Changing it changes nothing: the live tasks are edited only in Claude, with Tim's approval.

| Task | Schedule (UK) | Cron | Playbook part |
|---|---|---|---|
| FT game evening review | 21:30 Sun to Thu | `30 21 * * 0-4` | H1 |
| FT game morning check | 06:36 Mon to Fri (07:26 until 17 Oct) | `36 6 * * 1-5` | H2 |
| FT game price refresh | 16:45 Mon to Fri | `45 16 * * 1-5` | H3 |
| FT game late price refresh | 19:22 Mon to Fri | `22 19 * * 1-5` | H3 |
| FT game results-day refresh | 14:50 Mon to Fri | `50 14 * * 1-5` | H4 |
| FT game weekly review | 09:12 Sat | `12 9 * * 6` | H5 |
| FT game midday check | 12:40 Mon to Fri (exits at once: switched off by its own instructions) | `40 12 * * 1-5` | H6 |
| FT game weekend news check | 20:20 Sat and Sun | `20 20 * * 6,0` | H7 |

## Evening review

```
FT Stock Picking Game, EVENING REVIEW for Tim. Unattended: never ask questions; take the most reasonable reading and state it. Virtual game. Never open or operate the FT site, any account, a browser or the user's computer. After 27 Nov 2026: reply only that the game has ended. Time from `date -u`, shown as UK time.

Read `claude/ft-game-playbook.md` and `claude/ft-game-state.md` together (Projects tool). The playbook is the procedure: carry out part H1 in full under parts A to G, output per part I, record-keeping per part J. Check the script's sha256 against part B before running it; on a mismatch do not run it and say so.

Priorities: the order first (5 to 20 stocks, each 5% to 25%, cash at most 25%, total 100%, a 1 to 100 confidence rating on every position; size by weight times return). Follow part F's freshness and pacing rules; never re-request a refused page and name it.
- Change evening: send verdict, full order table and order and watchlist changes through SendUserMessage BEFORE publishing data; final message starts "Tim,".
- Quiet evening: no SendUserMessage; final message starts exactly "No change tonight. Nothing to enter." (part I, at most nine lines).
- Fault before the order is checked: say so in line one, say the order in force stands, send through SendUserMessage.
- If the playbook cannot be read: treat as a fault, work from the state doc and current sources, deliver verdict, order table, changes, short market read and the next three trading days; do not touch the page.
British English, no em-dashes, UK times, sources as links.

Market data key: <REDACTED: held only in the scheduled task>
Tim's father's massive.com key, stored at the family's request. Use it only in fetches to api.massive.com as playbook parts A and F say. Never write it into any file, doc, data, alert, message or reply, nor echo it. If rejected, say so without quoting it and use the free feed.
```

## Morning check

Changed 17 Oct 2026 (playbook 6.4): 06:36 UK, cut-off 07:00 UK.

```
FT Stock Picking Game, MORNING CHECK for Tim (06:36 UK). Unattended: never ask questions. Finish within about ten minutes: Tim must enter any change before 07:00 UK, the cut-off until the FT confirms it after the clock change (playbook part C). Virtual game. Never open or operate the FT site, any account, a browser or the user's computer. After 27 Nov 2026: reply only that the game has ended. Time from `date -u`, shown as UK time.

Read `claude/ft-game-playbook.md` and `claude/ft-game-state.md` together and carry out part H2 under parts A to E, output per part I. Confirm last night's order unless something material and new changes it; 10 to 15 fetches and searches sent together. Check the script's sha256 against part B before running it.
- Order revised: send verdict and full order table (Stock, Weight, Confidence (not calibrated), Change, with cash) through SendUserMessage FIRST, saying "enter before 07:00 UK", then record it (H2 step 5) and update the state doc. Final message starts "Tim," (part I format).
- Order stands: no SendUserMessage, leave the state doc alone, final message exactly "No change this morning. Nothing to enter." plus at most one line for tonight.
- Then H2 step 6 (overnight yields, oil, Bitcoin, day-call revision); never let it delay an order.
Any order: 5 to 20 stocks, 5% to 25% each, cash at most 25%, total 100%, a confidence rating on each. Pre-open news is already in the opening price. If the playbook cannot be read, work from the state doc and do not touch the page. British English, no em-dashes.
```

## One-off: GitHub access test (Sun 18 Oct 2026, 10:07 UK)

Created 17 Oct with Tim's approval; ran at 10:08 UK on 18 Oct and passed (read, dry-run push). Result in `CHANGELOG.md`, 6.8. The weekly review's prompt gained a GitHub line on 18 Oct.

## Price refresh (16:45)

```
FT Stock Picking Game, PRICE REFRESH (16:45 UK). Unattended: never ask questions. Virtual game. Never open or operate the FT site, any account, a browser or the user's computer. After 27 Nov 2026: reply only that the game has ended. Time from `date -u`, shown as UK time.

project_read `claude/ft-game-playbook.md` and carry out part H3 using parts F and G. Check the script's sha256 against part B before running it. Follow part F's freshness (clock suffix) and pacing rules; never re-request a refused page. Never change the order, watchlist, scores or ratings. Never call SendUserMessage.
Final reply, one line: "No change. Prices refreshed at <time>, <n> alerts on the page." or "No change. Prices refreshed at <time>, no alerts.", plus one line naming any failed step or refused page. If the playbook cannot be read: "No change. The price refresh could not read its instructions, so the page was not refreshed." British English, no em-dashes.
```

## Late price refresh (19:22)

```
FT Stock Picking Game, LATE PRICE REFRESH (19:22 UK). Unattended: never ask questions. Virtual game. Never open or operate the FT site, any account, a browser or the user's computer. After 27 Nov 2026: reply only that the game has ended. Time from `date -u`, shown as UK time.

project_read `claude/ft-game-playbook.md` and carry out part H3 using parts F and G. Check the script's sha256 against part B before running it. Follow part F's freshness and pacing rules; never re-request a refused page. Do not repeat today's earlier alerts unless the picture changed; add any results reaction per part H4 step 2. In the week of 26 Oct the US closes at 20:00 UK: say so in `prices_as_of`. Never change the order, watchlist, scores or ratings. Never call SendUserMessage.
Final reply, one line: "No change. Prices refreshed at <time>, <n> alerts on the page." or "No change. Prices refreshed at <time>, no alerts.", plus one line naming any failed step or refused page. If the playbook cannot be read: "No change. The price refresh could not read its instructions, so the page was not refreshed." British English, no em-dashes.
```

## Results-day refresh

```
FT Stock Picking Game, RESULTS-DAY REFRESH (14:50 UK). Unattended: never ask questions. Virtual game. Never open or operate the FT site, any account, a browser or the user's computer. After 27 Nov 2026: reply only that the game has ended. Time from `date -u`, shown as UK time.

Step 1, before anything else: ArtifactData `get` collection `datasets`, doc `ledger` on https://claude.ai/artifact/8P8UwQsb4QsbZMsKNYKrUJ; read the asset after `/_blob/` with Artifact `read`. Act only if a `table`="event", `kind`="results" row is dated today, or dated the previous trading day with `time_uk` after the US close. If none, reply exactly "No change. No results today." and stop.
Step 2: project_read `claude/ft-game-playbook.md` and carry out part H4 (built on H3). Check the script's sha256 against part B. For each reporter, log an alert: headline numbers against expectations, the move from the previous close and from the open against `implied_pct`, and for a holding the exit-rule verdict and weight times move. Never call SendUserMessage.
Final reply, one line: "No change. Results-day refresh at <time>, <n> alerts on the page.", plus one line naming any failed step. British English, no em-dashes.
```

## Weekly review

```
FT Stock Picking Game, WEEKLY REVIEW (Saturday) for Tim. Unattended: never ask questions; state any assumption. Virtual game. Never open or operate the FT site, any account, a browser or the user's computer. After 28 Nov 2026: reply only that the game has ended (28 Nov itself is the final review). Time from `date -u`, shown as UK time.

Read `claude/ft-game-playbook.md` and `claude/ft-game-state.md` together and carry out part H5 in full using parts D, F and G. Check the script's sha256 against part B before running it; on a mismatch, review from the state doc and current prices. If Friday's session is already logged (H5 step 2), do not fetch prices again. Follow part F's freshness and pacing rules; never re-request a refused page.

The review must: report weighted contributions (weight times return, points) for the week and the game, and what they say about sizing; give the estimated Friday-close value to the nearest credit against Tim's last FT figure; report confidence hit rates by band, calibration, the day-call record against always-green, and the week's yields, oil, Bitcoin and releases against forecast, each with a plain verdict and saying when samples are too small; name rules that helped or hurt with cases; give two or three changes for Sunday; state the gap to the top 2% honestly.

GitHub (broad scan record and G6, best effort): find the repository as data doc G6 step 1 says: first the existing clone at /home/claude/ft-game (check its origin is timzwang/ft-game; never reset or clean it), else `git clone` over HTTPS; only if git is refused, ToolSearch "select:mcp__claude-code-remote__add_repo", then the mcp__github__* tools (ToolSearch "github") to read the scan.

Output: start "Tim,". Sections: week and game to date (two lines); contribution table; what worked; confidence, calibration and day-call checks; macro and risk; rank stance and Sunday changes; what is needed from Tim (value, rank, players, a top-of-leaderboard return); unverified items; sources as links. Send a five-line summary through SendUserMessage. British English, no em-dashes, UK times.

Market data key: <REDACTED: held only in the scheduled task>
Tim's father's massive.com key, stored at the family's request. Use it only in fetches to api.massive.com as playbook parts A and F say. Never write it into any file, doc, data, alert, message or reply, nor echo it. If rejected, say so without quoting it and use the free feed.
```

## Midday check (switched off)

```
FT Stock Picking Game, MIDDAY CHECK for Tim. Unattended: never ask questions. Virtual game. Never open or operate the FT site, any account, a browser or the user's computer. After 27 Nov 2026: reply only that the game has ended. Time from `date -u`, shown as UK time.

1. project_read `claude/ft-game-state.md`, sections 1 and 8 only. Unless it says Tim has seen a US order entered after 08:00 UK fill at that day's US open, reply exactly "No change. Midday check is off until the US cut-off is confirmed." and stop: no other calls, no SendUserMessage.
2. Otherwise project_read `claude/ft-game-playbook.md` and carry out part H6 under parts A to E. Check the script's sha256 against part B before running it. If nothing qualifies, reply exactly "No change. No midday change." If something does, send the full order through SendUserMessage first, starting "Tim,", with the entry deadline.
British English, no em-dashes.
```

## Weekend news check

```
FT Stock Picking Game, WEEKEND NEWS CHECK (Sat and Sun 20:20 UK) for Tim. Unattended: never ask questions; state any assumption. Virtual game. Never open or operate the FT site, any account, a browser or the user's computer. After 27 Nov 2026: reply only that the game has ended. Time from `date -u`, shown as UK time. Never change the order, watchlist, scores or ratings.

Read `claude/ft-game-playbook.md` and `claude/ft-game-state.md` together and carry out part H7 under parts A, C, D and E, using F and G. Check the script's sha256 against part B before running it; on a mismatch skip the script but still deliver the check and update the state doc. Only this weekend's news counts: check date and year, give source and time for each item, and judge each in points of Tim's portfolio (weight times move), whether it carries on after Monday's open or fades, and a rating A, B or C. Change only the state doc's Weekend log plus one review-log line.

Output, British English, no em-dashes, UK times:
- No A item: final message starts exactly "No change. Nothing this weekend changes Monday's plan."; no SendUserMessage.
- An A item: start "Tim, weekend news that matters:" and send through SendUserMessage, with a provisional action, a 1 to 100 confidence rating and what would cancel it.
Then at most five items, weekend prices in one line, one line on what comes next, sources as links. If the playbook cannot be read, say so first, give a news check from the state doc, and do not touch the page, data or state doc.
```
