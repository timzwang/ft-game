---
name: "stock-score"
description: "Score stocks out of 100 on trend, recent behaviour, catalyst and analyst revisions with tested scripts and free price pages. Use to screen, rank or compare stocks, size a position or anchor a confidence rating."
---

# Stock score

A repeatable way to rank stocks over a horizon of days to a few weeks. Numbers are collected from fixed pages, a tested script does the arithmetic, and two judgement inputs are scored against a written rubric. Never work the score out by hand.

Score = trend (40) + short term (20) + catalyst (20) + revisions (20). About 40 is neutral.

## 1. Two scripts

Both are stored as assets on Tim's watchlist artifact, https://claude.ai/artifact/8P8UwQsb4QsbZMsKNYKrUJ. Their asset ids and sha256 hashes are listed in part B of the project doc `claude/ft-game-playbook.md` ("FT Stock Picking Game" project). Fetch one with the Artifact tool (action "read", the artifact URL, `path` set to the asset id), check its hash, copy the saved `.txt` to a `.py` file in a folder of its own, and run it with `python3 -I`.

| Script | Use it for | Needs |
|---|---|---|
| `ft_pipeline` | Anything already in the game files: holdings and watchlist. It keeps a price history, so it also gives simple and exponential moving averages (10 to 200 days), average true range, a weight cap, about six weeks of relative strength, a strength band, risk shares and correlations | The four data files from the artifact and a `today.json`; see part G of the procedure doc |
| `ft_score` | A quick ranking of stocks that are not in the files yet: a screen of 25 to 40 candidates, or a one-off comparison | One `input.json`, described below |

The two give scores within a few points of each other. A stock that matters should end up in the files and be scored by the pipeline.

If neither script can be fetched, say so. Rebuild from the tables in section 5 only if Tim agrees, and say the rebuilt copy is untested.

## 2. Collect the inputs

Send the fetches together and ask each one for exact values as a fixed `field: value` list.

| Input | Source |
|---|---|
| price, open, prev_close, high, low, volume, week52_high, week52_low | `https://stockanalysis.com/stocks/<ticker>/` |
| ma50, ma200, rsi, change_52w_pct, avg_vol_20d | `https://stockanalysis.com/stocks/<ticker>/statistics/` |
| daily open, high, low, close, volume | `https://stockanalysis.com/stocks/<ticker>/history/` |
| benchmark change_52w_pct and recent closes | `https://stockanalysis.com/etf/spy/` (past-year return) and `/etf/spy/history/` |

- London stocks: daily history from `https://stockanalysis.com/quote/lon/<TICKER>/history/`, a live quote from `https://www.lse.co.uk/SharePrice.html?shareprice=<TICKER>`. Take the averages and RSI from the US-listed ADR's statistics page where one exists, and pass the ADR's own price as `trend_price`. Otherwise leave those inputs null.
- For a quick screen of many names, the quote and statistics pages are enough; the 5-day item then earns half marks.
- Any missing number is `null`. The script gives half marks for that item and lists it under data gaps.
- Yahoo Finance, Google Finance and Finviz do not work from here.

## 3. Rate the two judgement inputs

Give each a number and a one-line note.

**catalyst_pts (0 to 20)**

- 16 to 20: confirmed results or another dated event inside the next 10 trading days, with a supportive lead-in (peers beating, estimates rising, strong pre-announced numbers).
- 11 to 15: a dated catalyst inside 10 trading days with a neutral lead-in, or a theme tailwind with fresh confirming news this week.
- 6 to 10: a theme tailwind with no dated event, or an event more than 10 trading days away.
- 0 to 5: no catalyst, or a clear overhang.

**revisions_pts (0 to 20)**

- 16 to 20: an upgrade from a major bank in the last 7 days, or three or more target raises in the last three weeks.
- 11 to 15: one or two target or estimate raises in the last two weeks.
- 8: nothing notable.
- 0 to 5: downgrades or target cuts dominate.

## 4. Run the quick screen (`ft_score`)

Write `input.json`:

```json
{
  "as_of": "Thu 8 Oct close",
  "regime": "mixed",
  "benchmark": {"name": "SPY", "change_52w_pct": 16.85, "five_day_pct": 1.30},
  "stocks": [{
    "name": "Exxon Mobil", "ticker": "XOM",
    "price": 168.50, "prev_close": 164.05, "open": 167.11, "high": 169.19, "low": 166.71,
    "volume": 13285721, "avg_vol_20d": 12737628,
    "ma50": 161.59, "ma200": 150.33, "rsi": 65.6,
    "week52_high": 176.41, "week52_low": 110.39, "change_52w_pct": 48.97,
    "five_day_pct": 2.86,
    "trend_price": null,
    "catalyst_pts": 10, "catalyst_note": "Results 30 Oct",
    "revisions_pts": 8, "revisions_note": "No recent changes"
  }]
}
```

- `regime` is "risk-on", "mixed" or "risk-off". Give either `five_day_pct` or `closes` (at least six, oldest first).
- Run `python3 -I ft_score.py input.json scores.json`. It prints a ranked table and writes the detail to `scores.json`.
- A `WARNING` line means an input is probably mistyped (wrong currency, price outside the day's range). Recheck that stock against its source and rerun.
- Test case: the example above scores 71 with a confidence anchor of 61.

For the pipeline, follow part G of the procedure doc: `template` writes the input skeleton, `run` scores everything and prints the table.

## 5. How the points are awarded

**Trend, 40**

| Item | Quick screen | Pipeline |
|---|---|---|
| Price versus 50-day average | below -5%: 0; -5% to 0: 3; 0 to 2%: 8; 2% to 15%: 12; 15% to 25%: 8; above 25%: 4 | the same |
| Structure | 50-day above 200-day: 5; price above 200-day: 3 | the same |
| Distance from 52-week high | within 3%: 10; within 8%: 7; within 15%: 4; within 25%: 2; further: 0 | the same |
| 52-week change minus benchmark | 30 points or more: 6; 10 or more: 4; 0 or more: 2 | 30 or more: 4; 10 or more: 3; 0 or more: 1 |
| About six weeks' return minus benchmark | not used | 5 points or more: 2; 0 or more: 1 |
| RSI | 50 to 70: 4; 70 to 80: 2; 40 to 50: 2; above 80 or below 40: 0 | the same |

**Short term, 20**

| Item | Points |
|---|---|
| 5-day return minus benchmark | 3 points or more: 8; 1 or more: 6; 0 or more: 4; -2 or more: 2; worse: 0 |
| Last session | closed above its open: 3; closed in the upper half of its range: 3 |
| Volume (the session versus the 20-day average) | up day at 1.3x or more: 6; up day at 0.8x or more: 4; up day on less: 2; down day below 1.3x: 2; down day at 1.3x or more: 0 |

**Catalyst, 20** and **Revisions, 20**: the judgement inputs. Unrated defaults are 6 and 8.

**Confidence anchor** = 50 + 0.35 x (score - 40), held between 40 and 68, minus 3 in a risk-off regime. It is the estimated chance the stock beats the S&P 500 over the next five trading days. The mapping is a starting assumption; the game's ledger records every rating and its outcome so it can be checked.

**Weight cap.** Quick screen: 30 divided by the average absolute daily move over the supplied closes. Pipeline: 30 divided by the 14-day average true range in percent. Both rounded to the nearest 5 and held between 5% and 20%. A stock that ranges 2% a day is capped at 15%; one that ranges 3% at 10%.

**Flags**: below 50-day average; downtrend (50-day below 200-day); extended (more than 15% above 50-day); overbought (RSI above 75); oversold (RSI below 35); heavy-volume down day; faded gap (gapped up more than 1%, then closed below its open); at 52-week high.

## 6. Reading the result

- 70 and above: strong trend with support from news. Check the flags before sizing: "extended" and "overbought" argue for a small first position.
- 55 to 69: acceptable. Usually needs a catalyst or revisions to earn a place.
- 45 to 54: neutral. Hold only for balance or a dated catalyst.
- Below 45, or flagged "downtrend": avoid or replace. A strong single day does not change this.
- The pipeline's strength band puts this in one word: strong (60 or more, above the 50-day average, no downtrend), weak (under 45 or a downtrend), middling otherwise.
- A position's effect on a portfolio is its weight times its return, so a high score matters most where the weight is. Use the weight cap, and check how much of the portfolio's risk a new name would add if it moves with what is already held.
- Report the score with its four parts, the flags, any data gaps and the time the data was taken. Do not present the confidence anchor as a forecast.

## Limits

- The scripts only rank what they are given. A screen is as good as the candidate pool, so build the pool from several places: index leaders, the day's large-cap movers, recent upgrades, and upcoming results.
- The quick screen takes the 50-day and 200-day averages and RSI from a published page. The pipeline works them out from stored closes once a stock has 200 of them, and uses the published figures until then.
- The game's ledger logs a rating for every scored stock every evening and checks it five sessions later. A first backtest of the price-only points (9 Oct 2026, nine stocks) showed no positive link with the next five sessions. Treat the score as a way to rank and to filter out weak trends, not as a forecast.
- stockanalysis.com refuses requests that arrive too fast: send its pages in groups of at most eight with a pause between groups, and do not ask again for a page that was refused.
- Catalyst and revisions are judgement. Keep the notes specific so they can be checked later.
- Trend following loses at turning points. In a risk-off regime, favour cash and low-beta names over high scores.