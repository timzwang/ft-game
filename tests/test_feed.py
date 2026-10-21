"""The price feed (feed/feed.py) and the pipeline's `feed` command (version 7.7, 21 Oct 2026).

Offline: the feed files here are built from the frozen 16 Oct snapshot plus one synthetic session (Mon 19 Oct), so no
network is used. They check that the command adds only new sessions, never replaces a stored row, refuses a ticker
whose rows disagree with the store (the wrong listing, pence against pounds, a split), fills only empty fields, leaves
`run` able to record the new session, and that the live form builds quotes.json for `refresh` and refuses a stale file.
"""
import contextlib
import datetime
import importlib.util
import io
import json

import pytest

from conftest import DATES, REPO

SESSION = DATES[0]          # Mon 19 Oct, the first session after the snapshot's last (Fri 16 Oct)


def _feed_mod():
    spec = importlib.util.spec_from_file_location("feed_under_test", REPO / "feed" / "feed.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def quiet(fn, *a):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(*a)
    return buf.getvalue()


def make_feed(stored, session=SESSION, scale=None, drop=(), long_for=()):
    """A close feed for `session`: each stored ticker's last five stored rows unchanged, plus a new row for `session`
    one per cent above the last close. `scale` multiplies one ticker's prices (to fake a wrong listing)."""
    hist = stored["hist"]
    by = {}
    for (t, d), r in hist.items():
        by.setdefault(t, []).append(r)
    tickers = {}
    for t, rows in by.items():
        if t in drop:
            continue
        rows = sorted(rows, key=lambda r: r["date"])
        last = rows[-1]["close"]
        new = {"date": session, "open": round(last * 1.002, 4), "high": round(last * 1.02, 4), "low": round(last * 0.995, 4),
               "close": round(last * 1.01, 4), "volume": 1000}
        feed_rows = [{k: r.get(k) for k in ("date", "open", "high", "low", "close", "volume")} for r in rows[-5:]] + [new]
        if scale and t in scale:
            feed_rows = [{**r, **{k: r[k] * scale[t] for k in ("open", "high", "low", "close") if r[k] is not None}} for r in feed_rows]
        e = {"yahoo": t, "market": "US", "session": session, "last_bar": session, "complete": True, "rows": feed_rows,
             "week52_high": 999.0, "week52_low": 1.0, "sessions_available": 300, "stored_rows": len(rows),
             "check": {"status": "agrees"}}
        if t in long_for:
            e["long"] = [{**r, "date": d} for r, d in zip([feed_rows[0]] * 3, ["2025-01-02", "2025-01-03", "2025-01-06"])] + feed_rows
        tickers[t] = e
    return {"meta": {"feed_version": "test", "mode": "close", "generated_utc": "2026-10-19T20:30:00+00:00",
                     "session_us": session, "session_uk": session, "stale": [], "missing": [], "mismatched": []},
            "tickers": tickers,
            "macro": {"treasury": [{"date": session, "us2y": 4.77, "us10y": 5.15, "us30y": 5.48}],
                      "coins": {"btc": {"price": 81772.5}, "eth": {"price": 2401.1}, "sol": {"price": 101.2}, "xrp": {"price": 1.31}},
                      "futures": {"brent": {"symbol": "BZ=F", "date": session, "close": 109.1}}}}


@pytest.fixture()
def today_file(pl, repo, tmp_path):
    tpl = tmp_path / "today.json"
    quiet(pl.cmd_template, {"stocks": str(repo / "data/stocks.json"), "ledger": str(repo / "data/ledger.json"),
                            "history": str(repo / "data/history.json"), "panel": str(repo / "data/panel.json"), "out": str(tpl)})
    return tpl


def run_feed(pl, repo, tmp_path, today_file, feed, **extra):
    ff = tmp_path / "latest.json"
    ff.write_text(json.dumps(feed), encoding="utf-8")
    out = quiet(pl.cmd_feed, {"feed": str(ff), "today": str(today_file), "history": str(repo / "data/history.json"), **extra})
    return json.loads(today_file.read_text(encoding="utf-8")), out


def test_feed_check_limits(pl):
    stored = {"2026-10-16": {"open": 100.0, "high": 101.0, "low": 99.0, "close": 100.0, "volume": 5},
              "2026-10-15": {"open": 98.0, "high": 98.0, "low": 98.0, "close": 98.0, "volume": None}}   # close-only, old style
    ok = [{"date": "2026-10-15", "open": 97.0, "high": 99.0, "low": 96.0, "close": 98.1},              # close-only: close only
          {"date": "2026-10-16", "open": 101.2, "high": 101.5, "low": 99.2, "close": 100.4}]
    assert pl.feed_check(ok, stored) == (2, [])
    n, bad = pl.feed_check([{**ok[1], "close": 100.6}], stored)
    assert n == 1 and "close" in bad[0]
    n, bad = pl.feed_check([{**ok[1], "open": 98.0}], stored)
    assert "open" in bad[0]
    assert pl.feed_check([{"date": "2026-10-19", "close": 5.0}], stored) == (0, [])


def test_feed_fills_new_session_only(pl, repo, tmp_path, today_file, stored):
    feed = make_feed(stored)
    today, out = run_feed(pl, repo, tmp_path, today_file, feed)
    assert today["date"] == SESSION                                   # was empty: set from the feed
    for s in today["stocks"]:
        dates = [r["date"] for r in s["history"]]
        assert dates == [SESSION], (s["ticker"], dates)               # only the new session: stored rows are never re-sent
        assert s["quote"]["price"] == s["history"][0]["close"] and s["quote"]["open"] == s["history"][0]["open"]
        assert s["quote"]["week52_high"] == 999.0
    assert [r["date"] for r in today["benchmark"]["history"]] == [SESSION]
    for t in ("OIL", "IBIT", "ETHA"):
        assert [r["date"] for r in today["extra_history"][t]] == [SESSION]
    mv = today["macro"]["values"]
    assert (mv["us2y"], mv["us10y"], mv["us30y"], mv["btc"], mv["xrp"]) == (4.77, 5.15, 5.48, 81772.5, 1.31)
    assert mv["brent"] is None                                        # futures only when asked
    assert "FEED ADDED" in out and "FEED REFUSED" not in out
    again, out2 = run_feed(pl, repo, tmp_path, today_file, feed, futures="yes")
    assert all(len(s["history"]) == 1 for s in again["stocks"])       # safe to repeat: nothing added twice
    assert again["macro"]["values"]["brent"] == 109.1


def test_feed_keeps_what_the_run_already_set(pl, repo, tmp_path, today_file, stored):
    today = json.loads(today_file.read_text(encoding="utf-8"))
    today["date"] = SESSION
    today["stocks"][0]["quote"]["price"] = 123.45
    today["macro"]["values"]["us10y"] = 5.2
    today_file.write_text(json.dumps(today), encoding="utf-8")
    today, _ = run_feed(pl, repo, tmp_path, today_file, make_feed(stored))
    assert today["stocks"][0]["quote"]["price"] == 123.45
    assert today["macro"]["values"]["us10y"] == 5.2 and today["macro"]["values"]["us2y"] == 4.77


def test_feed_refuses_wrong_listing_and_names_missing(pl, repo, tmp_path, today_file, stored):
    uk = next(s["ticker"] for s in stored["stocks"] if s.get("market") == "UK")
    us = next(s["ticker"] for s in stored["stocks"] if s.get("market") == "US" and s["group"] != "Cash")
    feed = make_feed(stored, scale={uk: 0.01}, drop=(us,))             # pence read as pounds; one stock missing
    today, out = run_feed(pl, repo, tmp_path, today_file, feed)
    by = {s["ticker"]: s for s in today["stocks"]}
    assert by[uk]["history"] == [] and by[uk]["quote"]["price"] is None
    assert by[us]["history"] == []
    assert f"FEED REFUSED" in out and uk in out.split("FEED REFUSED")[1]
    assert "FEED MISSING" in out and us in out.split("FEED MISSING")[1]
    assert pl.WARN                                                    # a refusal is a warning the run must read


def test_feed_does_not_pass_the_date(pl, repo, tmp_path, today_file, stored):
    today = json.loads(today_file.read_text(encoding="utf-8"))
    today["date"] = "2026-10-16"                                      # re-running the stored session
    today_file.write_text(json.dumps(today), encoding="utf-8")
    today, out = run_feed(pl, repo, tmp_path, today_file, make_feed(stored))
    assert all(r["date"] <= "2026-10-16" for s in today["stocks"] for r in s["history"])
    assert "nothing after 2026-10-16 is used" in out


def test_feed_backfills_a_short_store(pl, repo, tmp_path, today_file, stored):
    counts = {}
    for (t, _d) in stored["hist"]:
        counts[t] = counts.get(t, 0) + 1
    short = next(s["ticker"] for s in stored["stocks"] if s["group"] != "Cash" and counts.get(s["ticker"], 0) < 200)
    today, _ = run_feed(pl, repo, tmp_path, today_file, make_feed(stored, long_for=(short,)))
    rows = next(s for s in today["stocks"] if s["ticker"] == short)["history"]
    assert [r["date"] for r in rows][:3] == ["2025-01-02", "2025-01-03", "2025-01-06"] and rows[-1]["date"] == SESSION


def test_run_records_the_session_after_feed(pl, repo, tmp_path, today_file, stored):
    today, _ = run_feed(pl, repo, tmp_path, today_file, make_feed(stored))
    today.update({"next_session": DATES[1], "prices_as_of": "Mon 19 Oct close", "order_for": "Tue 20 Oct open",
                  "effective": DATES[1], "entered": SESSION})
    tf = tmp_path / "run-today.json"
    tf.write_text(json.dumps(today), encoding="utf-8")
    out = tmp_path / "out"
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        pl.cmd_run({"today": str(tf), "ledger": str(repo / "data/ledger.json"), "history": str(repo / "data/history.json"),
                    "macro": str(repo / "data/macro.json"), "panel": str(repo / "data/panel.json"), "out": str(out)})
    led = json.loads((out / "ledger.json").read_text(encoding="utf-8"))
    assert any(r["table"] == "perf" and r["date"] == SESSION for r in led), buf.getvalue()[-2000:]
    assert not pl.INCOMPLETE


def test_feed_live_builds_quotes(pl, repo, tmp_path, stored):
    now = datetime.datetime.now(datetime.timezone.utc)
    q = {s["ticker"]: {"price": 10.0, "prev_close": 9.9, "open": 9.95, "high": 10.1, "low": 9.8, "volume": 5, "bar_date": SESSION}
         for s in stored["stocks"] if s["group"] != "Cash"}
    q["SPY"] = {"price": 700.0, "prev_close": 699.0, "open": 699.5, "high": 701.0, "low": 698.0, "volume": 9, "bar_date": SESSION}
    live = {"meta": {"mode": "live", "read_utc": now.isoformat(timespec="seconds"), "read_uk": "16:31", "quotes": len(q)},
            "quotes": q, "macro_now": {"coins": {"btc": {"price": 82000.0}}, "futures": {"brent": {"price": 108.0}}}}
    lf, qf = tmp_path / "live.json", tmp_path / "quotes.json"
    lf.write_text(json.dumps(live), encoding="utf-8")
    quiet(pl.cmd_feed, {"live": str(lf), "stocks": str(repo / "data/stocks.json"), "out": str(qf)})
    got = json.loads(qf.read_text(encoding="utf-8"))
    assert got["date"] == SESSION and len(got["quotes"]) == len(q) - 1
    assert got["macro_now"]["values"] == {"btc": 82000.0, "brent": 108.0}
    live["meta"]["read_utc"] = (now - datetime.timedelta(hours=3)).isoformat(timespec="seconds")
    lf.write_text(json.dumps(live), encoding="utf-8")
    with pytest.raises(SystemExit):
        quiet(pl.cmd_feed, {"live": str(lf), "stocks": str(repo / "data/stocks.json"), "out": str(tmp_path / "q2.json")})


def test_feed_script_helpers(tmp_path):
    pytest.importorskip("pandas")
    f = _feed_mod()
    assert f.yahoo_symbol("SHEL", "UK") == "SHEL.L" and f.yahoo_symbol("BP.", "UK") == "BP.L"
    assert f.yahoo_symbol("OIL", "US") == "BNO" and f.yahoo_symbol("SHEL-US", "US") == "SHEL" and f.yahoo_symbol("BRK.B", "US") == "BRK-B"
    assert f.market_of("SHEL", {}) == "UK" and f.market_of("SHEL-US", {"SHEL-US": "UK"}) == "US" and f.market_of("XOM", {}) == "US"
    assert f.close_hour_utc("2026-10-20") == "2026-10-20T19:00:00Z"        # data doc part F: 19 to 30 Oct
    assert f.close_hour_utc("2026-11-02") == "2026-11-02T20:00:00Z"        # 20 from 2 Nov
    assert f.close_hour_utc("2026-11-27") == "2026-11-27T17:00:00Z"        # 17 on the early close
    (tmp_path / "request.txt").write_text("2026-10-21 21:40 evening review\ntickers: has, rr.l EFX\n", encoding="utf-8")
    assert f.requested_tickers(str(tmp_path / "request.txt")) == {"HAS": "US", "RR": "UK", "EFX": "US"}
    stored = {"2026-10-15": {"open": 98.0, "high": 98.0, "low": 98.0, "close": 98.0, "volume": None},
              "2026-10-16": {"open": 100.0, "high": 101.0, "low": 99.0, "close": 100.0, "volume": 5}}
    chk = f.compare([{"date": "2026-10-15", "open": 90.0, "high": 99.0, "low": 89.0, "close": 98.0, "volume": 3},
                     {"date": "2026-10-16", "open": 100.0, "high": 101.0, "low": 99.0, "close": 100.0, "volume": 5}], stored)
    assert chk["status"] == "agrees" and chk["sessions_compared"] == 2
    chk = f.compare([{"date": "2026-10-16", "open": 1.0, "high": 1.01, "low": 0.99, "close": 1.0, "volume": 5}], stored)
    assert chk["status"] == "mismatch"


def test_feed_tops_up_the_panel(pl, repo, tmp_path, today_file, stored):
    panel = json.loads((repo / "data/panel.json").read_text(encoding="utf-8"))
    members = [m["ticker"] for m in panel["members"]]
    t_ok, t_bad = members[0], members[1]
    feed = make_feed(stored)
    for t, k in ((t_ok, 1.0), (t_bad, 1.5)):                 # the second member's closes are 50% off: refused
        closes = (panel.get("closes") or {}).get(t, [])[-3:]
        rows = [{"date": d, "open": c * k, "high": c * k, "low": c * k, "close": c * k, "volume": 1} for d, c in closes]
        rows.append({"date": SESSION, "open": 10.0, "high": 11.0, "low": 9.0, "close": 10.5, "volume": 1})
        feed["tickers"][t] = {"yahoo": t, "market": "US", "rows": rows, "sessions_available": 300, "check": {"status": "agrees"}}
    today, out = run_feed(pl, repo, tmp_path, today_file, feed, panel=str(repo / "data/panel.json"))
    assert today["panel_history"][t_ok] == [{"date": SESSION, "close": 10.5}]
    assert t_bad not in today["panel_history"]
    assert "FEED PANEL REFUSED" in out and t_bad in out
    again, _ = run_feed(pl, repo, tmp_path, today_file, feed, panel=str(repo / "data/panel.json"))
    assert again["panel_history"][t_ok] == [{"date": SESSION, "close": 10.5}]     # not added twice


def test_feed_long_series_for_a_requested_panel_member(tmp_path):
    """Feed 1.1 (21 Oct 2026): a panel member requested as a candidate, with no rows in the price store, gets the
    long series. Panel closes carry no open, high, low or volume and never reach history.json, so they cannot stand
    in for a stored history (Analog Devices got ten rows on 21 Oct and could not be scored)."""
    f = _feed_mod()
    full_panel = {f"2025-{i:04d}": {} for i in range(500)}           # 500 panel closes: the panel needs no top-up
    stored = {"XOM": {f"d{i}": {} for i in range(250)}, "NEW": {f"d{i}": {} for i in range(30)}}
    panel = {"ADI": full_panel, "HPE": {}}
    assert f.wants_long("ADI", stored, panel, wanted={"ADI"})          # requested: the bug case
    assert not f.wants_long("ADI", stored, panel, wanted=set())        # panel only, not scored: ten rows are enough
    assert f.wants_long("HPE", stored, panel, wanted=set())            # a panel member short of two years
    assert f.wants_long("NEW", stored, panel, wanted={"NEW"})          # a list stock short of 200 stored rows
    assert not f.wants_long("XOM", stored, panel, wanted={"XOM"})      # a full store
    assert f.wants_long("CRL", stored, panel, wanted=set())            # not stored, not in the panel
    (tmp_path / "data").mkdir()
    (tmp_path / "feed").mkdir()
    (tmp_path / "data" / "stocks.json").write_text(json.dumps([{"ticker": "XOM"}, {"ticker": "CASH", "group": "Cash"}]))
    (tmp_path / "feed" / "request.txt").write_text("tickers: ADI\n")
    assert f.wanted_tickers(str(tmp_path)) == {"XOM", "ADI"}
