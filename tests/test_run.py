"""End-to-end: template, then run, on the stored files, re-running the last stored session (Fri 16 Oct).

Checks that a complete run leaves every stored figure where it was and exercises the 7.3 run-level changes:
the FT reading update, the results budget record, the missing-results warning and the kept market_closed list.
"""
import contextlib
import io
import json

import pytest

from conftest import perf_rows


def build_today(pl, repo, tmp_path, stored):
    tpl = tmp_path / "today.json"
    with contextlib.redirect_stdout(io.StringIO()):
        pl.cmd_template({"stocks": str(repo / "data/stocks.json"), "ledger": str(repo / "data/ledger.json"),
                         "history": str(repo / "data/history.json"), "panel": str(repo / "data/panel.json"), "out": str(tpl)})
    today = json.loads(tpl.read_text(encoding="utf-8"))
    session = max(r["date"] for r in stored["ledger"] if r["table"] == "perf")
    today.update({"date": session, "prices_as_of": "stored close", "order_for": "next open"})
    hist = stored["hist"]
    stocks = {r["ticker"]: r for r in stored["stocks"]}
    for s in today["stocks"]:
        b = hist.get((s["ticker"], session))
        if b:
            s["quote"].update({k: b[k] for k in ("open", "high", "low", "volume")})
            s["quote"]["price"] = b["close"]
            before = sorted((r for (t, d), r in hist.items() if t == s["ticker"] and d < session), key=lambda r: r["date"])
            s["quote"]["prev_close"] = before[-1]["close"] if before else None
        for k in ("week52_high", "week52_low", "target"):
            s["quote"][k] = (stocks.get(s["ticker"]) or {}).get(k)
    return today, session


def run(pl, repo, tmp_path, today, ledger_path=None, name="out"):
    tf = tmp_path / f"{name}-today.json"
    tf.write_text(json.dumps(today), encoding="utf-8")
    out = tmp_path / name
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        pl.cmd_run({"today": str(tf), "ledger": str(ledger_path or repo / "data/ledger.json"), "history": str(repo / "data/history.json"),
                    "macro": str(repo / "data/macro.json"), "panel": str(repo / "data/panel.json"), "out": str(out)})
    return json.loads((out / "ledger.json").read_text(encoding="utf-8")), buf.getvalue(), out


def test_full_run_keeps_figures_and_applies_73(pl, repo, tmp_path, stored):
    today, session = build_today(pl, repo, tmp_path, stored)
    last = [r for r in stored["ledger"] if r["table"] == "reported"][-1]
    today["reported"] = {"date": last["date"], "time_uk": last["time_uk"], "value": last["value_reported"],
                         "rank": last["rank"], "players": last["players"], "top2_return_pct": 6.5}
    today["market_closed"] = [{"ticker": "TEST", "date": "2026-11-26"}]
    led, out, _ = run(pl, repo, tmp_path, today)

    assert out.startswith("Pipeline version 7.5")
    assert perf_rows(led) == perf_rows(stored["ledger"])
    assert not pl.INCOMPLETE

    rep = [r for r in led if r["table"] == "reported" and r["date"] == last["date"] and r["rank"] == last["rank"]]
    assert len(rep) == 1 and rep[0]["value"] == 6.5                 # the repeat filled in the top 2% line

    rb = next(r for r in led if r["table"] == "meta" and r["name"] == "results_budget")
    rule = json.loads(rb["text"])
    assert rule["default"] == 0.6 and rule["windows"][0]["from"] == "2026-10-27" and rule["windows"][0]["budget"] == 1.0
    assert rb["id"]                                                 # saved with an id like every ledger row

    mc = next(r for r in led if r["table"] == "meta" and r["name"] == "market_closed")
    assert json.loads(mc["text"]) == [["TEST", "2026-11-26"]]

    held = {r["name"] for r in stored["stocks"] if r["group"] == "Portfolio" and (r["weight"] or 0) > 0}
    has_abbvie_event = any(r["table"] == "event" and r["kind"] == "results" and r["stock"] == "AbbVie" for r in stored["ledger"])
    if "AbbVie" in held and not has_abbvie_event:
        assert "RESULTS MISSING AbbVie" in out

    # A second run with no market_closed keeps the stored list, and no row is duplicated.
    lp = tmp_path / "ledger-after.json"
    lp.write_text(json.dumps(led), encoding="utf-8")
    today.pop("market_closed")
    led2, _, _ = run(pl, repo, tmp_path, today, ledger_path=lp, name="out2")
    mc2 = [r for r in led2 if r["table"] == "meta" and r["name"] == "market_closed"]
    assert len(mc2) == 1 and json.loads(mc2[0]["text"]) == [["TEST", "2026-11-26"]]
    assert len([r for r in led2 if r["table"] == "meta" and r["name"] == "results_budget"]) == 1
    assert len([r for r in led2 if r["table"] == "reported"]) == len([r for r in led if r["table"] == "reported"])
    assert perf_rows(led2) == perf_rows(stored["ledger"])


def test_results_lines_use_the_window_budget(pl, repo, tmp_path, stored):
    today, session = build_today(pl, repo, tmp_path, stored)
    today["events"] = [{"date": "2026-10-27", "name": "Coca-Cola results", "stock": "Coca-Cola", "kind": "results", "implied_pct": 4.0}]
    led, out, _ = run(pl, repo, tmp_path, today)
    line = next(l for l in out.splitlines() if "RESULTS Coca-Cola 2026-10-27" in l)
    assert "0.80 points" in line and "within the 1 budget" in line   # 20% x 4% = 0.8, inside the cluster's 1.0


def test_run_prints_portfolio_fit_and_changes_no_file(pl, repo, tmp_path, stored):
    """7.5: the strong watchlist names get a fit line; BP moves with Shell (0.90 on the snapshot), so it is a swap."""
    today, _ = build_today(pl, repo, tmp_path, stored)
    led, out, _ = run(pl, repo, tmp_path, today)
    assert "PORTFOLIO FIT of the strong names" in out
    bp = next(l for l in out.splitlines() if l.strip().startswith("BP ") and "correlation with the order" in l)
    assert "highest +0.90 with Shell" in bp and "a swap, not an addition" in bp
    assert perf_rows(led) == perf_rows(stored["ledger"])
