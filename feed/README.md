# Price feed

Roadmap item 59, built 21 Oct 2026 (playbook 6.12, pipeline 7.7). A GitHub Actions job (`.github/workflows/feed.yml`) reads the day's prices, yields and coin prices straight from their sources and writes them here. Claude's scheduled runs read them with git and pass them to the pipeline's `feed` command, in place of fetching one price page per stock.

## Why

On Tue 20 Oct the evening review's fetch tool refused every address it had not first seen in a search result, so the clock-suffixed quote pages, the Treasury file, Coinbase's candles and the market data service could not be reached, and nine rows went missing (Marathon Petroleum, Humana, Valero, Phillips 66, the oil fund, the US lines of Shell and BP, the Ether fund and RTX). A GitHub runner has open internet and needs no fetch tool, so the feed does not depend on any of that.

## Files

| File | Written by | What it is |
|---|---|---|
| `latest.json` | close mode, after the US close | For every ticker the runs may need: the last ten completed sessions (open, high, low, close, volume), the 52-week high and low, a check against the stored prices, and about two years of daily bars for any ticker with fewer than 200 stored rows (or a panel stock with fewer than 480 closes); the Treasury's 2, 10 and 30-year yields (latest six days); Coinbase's Bitcoin, Ether, Solana and XRP prices at the hour before the US close; front-month Brent, WTI, natural gas and gold futures (a fallback only) |
| `latest.md` | close mode | The same, for reading, with the check for every ticker |
| `live.json` | live mode, on request during the US session | The latest price, previous close, open, high, low and volume for the list and the price store, when the feed read them, Coinbase's live Bitcoin and Ether and the futures |
| `log-close.txt`, `log-live.txt` | each mode | The last run's log (the Actions logs are not readable from Claude's sessions) |
| `request.txt` | the runs | Pushing a changed line forces a run (see below) |
| `feed.py` | | The script |

## Which tickers

Every stock in `data/stocks.json`, every ticker in `data/history.json` (stocks that left the list but are still being settled, the first order's stocks, SPY, and the series `OIL` from the BNO fund, `SHEL-US` and `BP-US` from the US-listed shares, `IBIT` and `ETHA`), the 30 panel stocks in `data/panel.json`, and any ticker named on a line `tickers: A B C` among the last 20 lines of `request.txt` (London tickers end in `.L`). So a stock added to the list one night is in the next night's feed by itself; a reporter the evening review wants tonight is added with a `tickers:` line.

## Prices

Yahoo Finance daily bars through the `yfinance` library, with dividend adjustment off, so a price is the price traded that day (adjusted only for splits, like stockanalysis.com's history pages). London prices are in pence, as in the price store. Bars are dated in the exchange's own zone. A US bar counts as final from 16:15 New York (13:15 on 27 Nov), a London bar from 16:45 UK.

First run (21 Oct 2026, 984 overlapping sessions across 41 tickers): Yahoo's close matched the stored close to the cent in 973; the largest gap was 0.42%, on one close-only row from September. 837 of 858 opens were within 0.05%; the six beyond 0.2% were mostly 19 Oct rows taken that night from Cboe's delayed quotes. The rows that first looked like disagreements were old close-only rows (open, high and low set to the close), which are now compared on the close only.

## The check

Every ticker's last 25 feed sessions are compared with the stored rows for the same sessions (for a panel stock, with the panel's closes). A close more than 0.5% away, or an open, high or low more than 1.5% away on a row with a traded open, marks the ticker as disagreeing. That catches the wrong listing, pence against pounds or a split, not the small differences between vendors. The pipeline's `feed` command repeats the check against the live store before it uses a row and refuses a disagreeing ticker (FEED REFUSED), so nothing here is trusted blindly.

## Timing and requests

- Close mode is scheduled at 20:16 and 21:16 UTC on weekdays (16:16 New York before and after the US clock change on 1 Nov); a slot that finds the session already written does nothing. GitHub often starts scheduled jobs 20 to 40 minutes late.
- So the runs ask for a run when they need one: a commit to `main` that changes `feed/request.txt` or `scan/request.txt` starts the job at once. A commit message starting `Feed request: live` runs live mode; anything else runs close mode, forced. The evening review's "Scan request" commit (data doc G7) therefore refreshes the feed as well.
- A run takes about a minute after the runner starts.

## Rules

- The feed writes only in `feed/`. It never decides anything: what the runs do with it is in the playbook (data doc G8).
- The script, the tolerances and the ticker list change only in a session with Tim.
- No key, token or account detail is needed or kept: every source here is public.
