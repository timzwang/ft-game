# FT Stock Picking Game: weekend news check (H7)

Part H7 of the playbook (version 6, 15 Oct 2026). Runs on Saturday and Sunday at 20:20 UK. Read with the core playbook (`claude/ft-game-playbook.md`), the rules (`claude/ft-game-rules.md`, for the scenarios and the crypto timing rule), the data doc (`claude/ft-game-data.md`, for G1 and `refresh`) and the state doc.

Markets are shut, but a headline can move prices sharply at Monday's open, above all one about the Iran war or the Strait of Hormuz. This run finds what happened, says what it means for this portfolio, and leaves a record for Sunday's evening review (21:30 UK) and Monday's morning check, which decide the order. It never changes the order, the watchlist, a score or a rating.

## Steps

1. Read the state doc and fetch `stocks.json`, `ledger.json` and the script (G1; the panel file is not needed). From them take the holdings and weights, the watchlist, the `scenario` rows (each gives the portfolio's move in points if that story lands) and the weekend's earlier `alert` rows and "Weekend log" entries, so nothing is reported twice.
2. Search for what has happened since Friday's US close (on Sunday: since Saturday's check), with eight to twelve searches sent together in extended mode. Use only items dated this weekend, and check the year on every one.
   - The Iran war: strikes, ceasefire or reopening talks, shipping and tanker attacks in the Strait of Hormuz, statements from Washington, Tehran, Israel and the Gulf states, the Houthis.
   - Oil supply: OPEC+ meetings and statements (often held at weekends), Gulf of Mexico storms and shut-ins, refinery outages, attacks on Russian or Ukrainian energy sites.
   - US policy: tariffs, export controls on chips, executive orders, government funding, the 3 November midterms, weekend remarks by Fed officials.
   - Other macro: Chinese data and policy announcements (often released at weekends), anything from the UK or Europe that would move gilts or the pound.
   - Every holding and watchlist stock: deals, guidance, regulatory news, management changes, and weekend press pieces.
3. Read the few prices that trade at the weekend, as a check on how much the news matters:
   - IG's "Weekend Wall Street" market, `https://www.ig.com/uk/indices/markets-indices/weekend-wall-street` (open 08:00 to 22:40 UK on Saturday and Sunday): the level and the change shown. Under 0.3% either way is noise.
   - Bitcoin: the live Coinbase price (part F), set against the stored price at Friday's US close, which is the `macro` row with `ticker` "btc" in the ledger. It is a rough gauge of appetite for risk, and for a crypto-linked holding it is the expected gap: put the reading in `macro_now` (`btc`, and `eth` if fetched) in step 5's quotes.json and the script prints the move that has gone with it for every crypto-linked stock. A move of 5% or more since Friday's close is a B item at least when a crypto-linked stock is held, and is worth a line either way.
   - On Sunday, the Saudi stock index, `https://tradingeconomics.com/saudi-arabia/stock-market`: Gulf markets trade on Sundays, so its move is the first market verdict on weekend news about the war or oil.
   - Oil and US index futures do not reopen until 23:00 UK on Sunday. Do not quote a futures price as a weekend reaction before then.
4. Judge each item for this portfolio, not for the index:
   - Name the scenario it belongs to and that scenario's figure in points, or say that none fits and give weight times a reasoned move.
   - Say whether the move is more likely to carry on after Monday's open or to fade (part C: the gap itself cannot be dodged in a holding).
   - Rate it A (changes Monday's plan), B (watch: matters if confirmed or if it grows) or C (noise).
   - For an A item, give a provisional action for the Sunday review with a confidence rating from 1 to 100, and say what would cancel it.
5. Record it, only if there is at least one A or B item that has not been recorded already, or a crypto-linked stock is held (so the page shows Bitcoin's move since Friday):
   - Write quotes.json with `date` (today), empty `quotes` and `alerts`, one per A or B item: `time_uk`, `stock` (the stock's name, or "Market"), and `text` starting "Weekend:" with the item, its rating and its effect in points. Run `refresh` with `--ledger` and publish `ledger.json` (G5).
   - In the state doc, change only the "Weekend log" in section 7 (start it afresh on Saturday with the weekend's dates; add to it on Sunday) and add one line to the review log. Write the whole doc back with everything else untouched.

## Output

Final message, also sent through SendUserMessage when there is an A item:

- First line: with no A item, exactly "No change. Nothing this weekend changes Monday's plan."; with an A item, "Tim, weekend news that matters:".
- Then at most five items, most important first: what happened with its source and time, the effect on the portfolio in points, whether it should carry on or fade, the rating, and for an A item the provisional action with its confidence rating.
- Then the weekend prices from step 3 in one line, and one line on what comes next: Sunday's evening review sets the order, futures reopen at 23:00 UK on Sunday, and Monday's morning check at 07:26 reads them before the 08:00 cut-off.
- Sources as markdown links.
