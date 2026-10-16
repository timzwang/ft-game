# Broad scan

Roadmap item 43, built 16 Oct 2026. A GitHub Actions job (`.github/workflows/scan.yml`) scans about 900 US and London stocks after every US close and writes two lists here. The evening review reads them to choose which stocks to look at (data doc, G7). The scan finds stocks; it never scores them, and none of its figures go into the pipeline: every shortlisted name is fetched again from the playbook's own sources (part F).

## Files

| File | What it is |
|---|---|
| `latest.md` | The night's two lists and the record, for reading |
| `latest.csv` | The same lists, one row per stock, for the evening review |
| `latest.json` | Which session was scanned, when, how many stocks were measured, which had no prices |
| `record.csv` | Every top-10 entry since 16 Oct, settled five sessions later |
| `universe.csv` | The stocks scanned and their index, rebuilt weekly |
| `log.txt` | The last run's log (the Actions logs are not readable from Claude's sessions) |
| `request.txt` | Pushing a changed line here starts a forced run |
| `scan.py`, `requirements.txt` | The script |

## Universe

The S&P 500, the Nasdaq-100, the FTSE 100 and the FTSE 250, from the constituent tables on Wikipedia, rebuilt when the file is more than seven days old. If any of the four sources fails, the previous file is kept. US and London listings only, because those are the ones the playbook's sources can verify.

## Prices

A bulk download of about 15 months of daily bars from Yahoo Finance (the `yfinance` library), adjusted for splits and dividends, fresh each run. Stocks Yahoo does not return are tried on Stooq. London prices are in pence and are converted to pounds for turnover only. Benchmarks: SPY for US stocks, the FTSE 100 index for London stocks. A stock whose last bar is not the scanned session (suspended, delisted or late) is left out and listed as stale in `latest.json`.

## The two lists (rules version 1, fixed 16 Oct 2026 before any result was seen)

A **turnover floor** applies to both: a median daily turnover over 20 sessions of at least $25m (US) or £3m (London).

**Leaders.** The stock closed above its 50-day and its 200-day average, is within 10% of its 52-week high, and has at least 253 sessions of history. Ranked by the 12-month return excluding the latest month (closes 252 and 21 sessions back), less the benchmark's over the same span. Top 30.

**Events.** The stock opened at least 3% above the previous close, closed at or above its open, closed in the upper half of the day's range, on volume at least 1.5 times the average of the previous 20 sessions. Ranked by the day's return less the benchmark's. Top 30. Many of these will be earnings reactions; the evening review checks the headlines and runs the full six-test drift scan on any that are.

The rules change only in a session with Tim, with a new rules version, and the record keeps the version each row was made under.

## The record

The top 10 of each list is written to `record.csv` once per session, with a flag for a stock that was not in that list's top 10 the session before. Five sessions later each row is settled against its benchmark two ways: close to close from the scan session, and from the next session's open (the price an order entered that evening would get). `latest.md` reports, for each list, the share that beat the index and the average excess, over all rows and over first appearances only. Rows on consecutive nights overlap, so the first-appearance figures are the fairer ones.

## Timing

Scheduled at 20:10 and 21:05 UTC on weekdays. Until 30 Oct the first slot is 16:10 New York; from 2 Nov (after the US clock change) the second slot is 16:05 New York. The script works out the latest US session whose bar is final and does nothing if that session is already in `latest.json`. GitHub can start scheduled jobs late, sometimes by 15 minutes or more, so the evening review checks the session date and, if it is behind, pushes a line to `request.txt` to force a run.
