"""UK and US market calendars through the end of the game (Claude, 19 Oct 2026 evening, Tim's review brief priority A).

Ten scenarios on deterministic synthetic prices for 20 to 27 Nov 2026, the one stretch of the game where London and New
York trade on different days (26 Nov: Thanksgiving, US shut, London open; 27 Nov: US closes at 13:00 New York), plus
the week of 26 Oct, when UK clocks have gone back and US clocks have not.

Rules taken as given (playbook part C, from the FT's terms; not re-verified here because the FT site cannot be read):
  R1  an order is a set of target weights; changes fill at the next trading day's open, London at 08:00 UK and US
      stocks at the US open;
  R2  weights are reset to target at each close;
  R3  a day's return is the sum of weight x return: kept weight close over previous close, added weight close over
      the fill (the open), sold weight the open over the previous close;
  R4  final values use the official closes of 27 Nov.
Modelling assumptions, NOT established by FT documentation (each test that relies on one says so):
  M1  on 26 Nov a US holding is unchanged in value (its market is shut) while a London holding moves;
  M2  an order entered before the cut-off on 26 Nov fills its London legs at the 26 Nov London open and its US legs
      at the next US open, 27 Nov (R1 applied market by market). The FT could instead hold the whole order; ask them;
  M3  whether the FT resets weights at the 26 Nov close, when only London has traded, is unknown. The pipeline keeps
      no 26 Nov performance line, so over 26 and 27 Nov it is exactly a buy and hold of the 25 Nov weights. The test
      measures the gap to the reset version, a second-order term.

Each test states the expected outcome before comparing it with the code. Expected figures are computed here by hand
from the prices, never by calling the pipeline's own valuation.
"""
import copy

import pytest

from conftest import bar

V0 = 100000.0
US = ["2026-11-20", "2026-11-23", "2026-11-24", "2026-11-25", "2026-11-27"]
UK = ["2026-11-20", "2026-11-23", "2026-11-24", "2026-11-25", "2026-11-26", "2026-11-27"]
# (open, close) by date. US stocks have no 26 Nov row; London stocks do.
P = {
    "SPY": {"2026-11-20": (100, 100), "2026-11-23": (100, 101), "2026-11-24": (101, 102), "2026-11-25": (102, 103), "2026-11-27": (103, 104)},
    "USA": {"2026-11-20": (50, 50), "2026-11-23": (50, 51), "2026-11-24": (51, 52), "2026-11-25": (52, 53), "2026-11-27": (54, 55)},
    "USB": {"2026-11-20": (200, 200), "2026-11-23": (200, 198), "2026-11-24": (198, 196), "2026-11-25": (196, 194), "2026-11-27": (195, 197)},
    "UKA": {"2026-11-20": (1000, 1000), "2026-11-23": (1000, 1010), "2026-11-24": (1010, 1020), "2026-11-25": (1020, 1030),
            "2026-11-26": (1040, 1060), "2026-11-27": (1070, 1080)},
    "UKB": {"2026-11-20": (500, 500), "2026-11-23": (500, 495), "2026-11-24": (495, 490), "2026-11-25": (490, 485),
            "2026-11-26": (480, 470), "2026-11-27": (465, 460)},
}
NAME = {"USA": "US One", "USB": "US Two", "UKA": "UK One", "UKB": "UK Two"}


def o(t, d):
    return P[t][d][0]


def c(t, d):
    return P[t][d][1]


def history(drop=()):
    h = {}
    for t, rows in P.items():
        for d, (op, cl) in rows.items():
            if (t, d) in drop:
                continue
            r = bar(t, d, cl)
            r.update({"open": op, "high": max(op, cl) + 1, "low": min(op, cl) - 1})
            h[(t, d)] = r
    return h


def ledger(pl, positions):
    """positions: [(effective, ticker, weight)]; the first order fills at the 20 Nov open."""
    L = [pl.lrow("meta", name="start_date", text="2026-11-20"), pl.lrow("meta", name="start_value", value=V0),
         pl.lrow("meta", name="spy_base", value=100.0)]
    for eff, t, w in positions:
        L.append(pl.lrow("position", effective=eff, name=NAME[t], ticker=t, weight=float(w)))
        L.append(pl.lrow("trade", date=eff, effective=eff, name=NAME[t], ticker=t, to_w=float(w)))
    return L


def perf(L):
    return {r["date"]: r for r in L if r["table"] == "perf"}


def kept(w, t, d0, d1):
    return w * (c(t, d1) / c(t, d0) - 1)


def chain(day_pts):
    v = V0
    for x in day_pts:
        v *= 1 + x / 100.0
    return v


FIRST_DAYS = ["2026-11-23", "2026-11-24", "2026-11-25"]


def first_days(w):
    """The three ordinary sessions after the 20 Nov fill (the fill day itself earns close over open = 0 here)."""
    out, prev = [], "2026-11-20"
    for d in FIRST_DAYS:
        out.append(sum(kept(x, t, prev, d) for t, x in w.items()))
        prev = d
    return out


# ------------------------------------------------------------------ 1 to 3: ordinary sessions

def test_1_us_only(pl):
    """Expected: each day the sum of weight x close-over-close; 27 Nov measured from the 25 Nov close (no US session
    on 26 Nov); no PERFORMANCE INCOMPLETE."""
    w = {"USA": 50, "USB": 50}
    L = ledger(pl, [("2026-11-20", t, x) for t, x in w.items()])
    pl.update_performance(L, history(), "SPY", "2026-11-27")
    days = [0.0] + first_days(w) + [sum(kept(x, t, "2026-11-25", "2026-11-27") for t, x in w.items())]
    assert not pl.INCOMPLETE
    assert sorted(perf(L)) == US
    assert perf(L)["2026-11-27"]["value_est"] == pytest.approx(chain(days), abs=0.01)


def test_2_uk_only(pl):
    """Expected: the same on London closes, with 26 and 27 Nov merged into one line measured from the 25 Nov close (M3,
    buy and hold over the two days). The reset version (R2 applied at the 26 Nov London close) differs by a cross term,
    printed here so its size is on record."""
    w = {"UKA": 50, "UKB": 50}
    L = ledger(pl, [("2026-11-20", t, x) for t, x in w.items()])
    pl.update_performance(L, history(), "SPY", "2026-11-27")
    base = chain([0.0] + first_days(w))
    buy_hold = base * (1 + sum(kept(x, t, "2026-11-25", "2026-11-27") for t, x in w.items()) / 100)
    reset = base * (1 + sum(kept(x, t, "2026-11-25", "2026-11-26") for t, x in w.items()) / 100) \
                 * (1 + sum(kept(x, t, "2026-11-26", "2026-11-27") for t, x in w.items()) / 100)
    assert not pl.INCOMPLETE
    assert perf(L)["2026-11-27"]["value_est"] == pytest.approx(buy_hold, abs=0.01)
    assert abs(buy_hold - reset) / V0 < 0.001          # under 0.1% even with these deliberately large opposite moves


def test_3_mixed(pl):
    """Expected: US and London holdings each valued on their own rows; 27 Nov from the 25 Nov close for both."""
    w = {"USA": 50, "UKA": 50}
    L = ledger(pl, [("2026-11-20", t, x) for t, x in w.items()])
    pl.update_performance(L, history(), "SPY", "2026-11-25")
    assert perf(L)["2026-11-25"]["value_est"] == pytest.approx(chain([0.0] + first_days(w)), abs=0.01)


# ------------------------------------------------------------------ 4 to 6: 26 Nov, US shut and London open

def test_4_uk_trades_while_us_shut(pl):
    """Expected (M1, M3): the US holding has no 26 Nov row and that is not a gap; the London holding's 26 Nov move is
    counted in the 27 Nov line; the value at the 27 Nov close equals holding the 25 Nov weights over both days. For a
    realistic case (a 15% London holding, +2% then +1%, the US half +1%) the reset version differs by under 0.001%."""
    w = {"USA": 50, "UKA": 50}
    L = ledger(pl, [("2026-11-20", t, x) for t, x in w.items()])
    pl.update_performance(L, history(), "SPY", "2026-11-27")
    v25 = chain([0.0] + first_days(w))
    want = v25 * (1 + (kept(50, "USA", "2026-11-25", "2026-11-27") + kept(50, "UKA", "2026-11-25", "2026-11-27")) / 100)
    assert not pl.INCOMPLETE
    assert perf(L)["2026-11-27"]["value_est"] == pytest.approx(want, abs=0.01)
    ws, r1, r2, rus = 0.15, 0.02, 0.01, 0.01                         # the size of the M3 cross term, realistic case
    assert abs(ws * r1 * (r2 * (1 - ws) - rus)) < 1e-5


def test_5_mixed_order_before_26_nov(pl):
    """Expected: an order entered on 24 Nov fills every leg at the 25 Nov opens (both markets open), by R3."""
    L = ledger(pl, [("2026-11-20", "USA", 50), ("2026-11-20", "UKA", 50),
                    ("2026-11-25", "USA", 30), ("2026-11-25", "USB", 20), ("2026-11-25", "UKA", 30), ("2026-11-25", "UKB", 20)])
    pl.update_performance(L, history(), "SPY", "2026-11-27")
    d1 = [0.0] + first_days({"USA": 50, "UKA": 50})[:2]
    d25 = (kept(30, "USA", "2026-11-24", "2026-11-25") + 20 * (o("USA", "2026-11-25") / c("USA", "2026-11-24") - 1)
           + 20 * (c("USB", "2026-11-25") / o("USB", "2026-11-25") - 1)
           + kept(30, "UKA", "2026-11-24", "2026-11-25") + 20 * (o("UKA", "2026-11-25") / c("UKA", "2026-11-24") - 1)
           + 20 * (c("UKB", "2026-11-25") / o("UKB", "2026-11-25") - 1))
    d27 = sum(kept(x, t, "2026-11-25", "2026-11-27") for t, x in {"USA": 30, "USB": 20, "UKA": 30, "UKB": 20}.items())
    assert not pl.INCOMPLETE
    assert perf(L)["2026-11-27"]["value_est"] == pytest.approx(chain(d1 + [d25, d27]), abs=0.01)


def london_change_on_26(pl, us_leg=False):
    pos = [("2026-11-20", "USA", 50), ("2026-11-20", "UKA", 50),
           ("2026-11-26", "UKA", 30), ("2026-11-26", "UKB", 20)]
    if us_leg:
        pos += [("2026-11-26", "USA", 40), ("2026-11-26", "USB", 10)]
    return ledger(pl, pos)


def test_6_uk_only_order_during_us_holiday(pl):
    """Expected (R1, R3): an order entered on the evening of 25 Nov, before the 26 Nov cut-off, sells 20 of UK One and
    buys 20 of UK Two at the 26 Nov London open. The 27 Nov line (which covers 26 and 27 Nov, M3) must use the
    26 Nov opens (1040 and 480) as the fill prices, not the 27 Nov opens (1070 and 465)."""
    L = london_change_on_26(pl)
    pl.update_performance(L, history(), "SPY", "2026-11-27")
    v25 = chain([0.0] + first_days({"USA": 50, "UKA": 50}))
    d27 = (kept(50, "USA", "2026-11-25", "2026-11-27") + kept(30, "UKA", "2026-11-25", "2026-11-27")
           + 20 * (o("UKA", "2026-11-26") / c("UKA", "2026-11-25") - 1)          # sold at the 26 Nov open
           + 20 * (c("UKB", "2026-11-27") / o("UKB", "2026-11-26") - 1))         # bought at the 26 Nov open
    assert not pl.INCOMPLETE
    assert perf(L)["2026-11-27"]["value_est"] == pytest.approx(v25 * (1 + d27 / 100), abs=0.01)


def test_6b_mixed_order_entered_for_26_nov(pl):
    """Expected (M2): the same order with US legs too (US One 50 to 40, US Two 0 to 10), all given the fill date of
    26 Nov: the London legs fill at the 26 Nov London open, the US legs at the 27 Nov US open, the next US session."""
    L = london_change_on_26(pl, us_leg=True)
    pl.update_performance(L, history(), "SPY", "2026-11-27")
    v25 = chain([0.0] + first_days({"USA": 50, "UKA": 50}))
    d27 = (kept(40, "USA", "2026-11-25", "2026-11-27") + 10 * (o("USA", "2026-11-27") / c("USA", "2026-11-25") - 1)
           + 10 * (c("USB", "2026-11-27") / o("USB", "2026-11-27") - 1)
           + kept(30, "UKA", "2026-11-25", "2026-11-27") + 20 * (o("UKA", "2026-11-26") / c("UKA", "2026-11-25") - 1)
           + 20 * (c("UKB", "2026-11-27") / o("UKB", "2026-11-26") - 1))
    assert not pl.INCOMPLETE
    assert perf(L)["2026-11-27"]["value_est"] == pytest.approx(v25 * (1 + d27 / 100), abs=0.01)


def test_6c_standstill_judges_a_26_nov_change(pl):
    """Expected: the STANDSTILL test has a change row for a change that fills on 26 Nov, priced with the same fills
    as the performance log (the change against keeping the 25 Nov order, over the sessions from 27 Nov)."""
    L = london_change_on_26(pl)
    rows = {r["name"]: r for r in pl.standstill_rows(L, history(), "SPY", "2026-11-27") if r["kind"] == "change"}
    assert "Change for 2026-11-26" in rows
    r = rows["Change for 2026-11-26"]
    new = (kept(30, "UKA", "2026-11-25", "2026-11-27") + 20 * (o("UKA", "2026-11-26") / c("UKA", "2026-11-25") - 1)
           + 20 * (c("UKB", "2026-11-27") / o("UKB", "2026-11-26") - 1))
    old = kept(50, "UKA", "2026-11-25", "2026-11-27")
    assert r["value"] == pytest.approx(new - old, abs=0.002)                # the US half is the same in both


# ------------------------------------------------------------------ 7: the early close on 27 Nov

def test_7_early_close(pl):
    """Expected: 27 Nov is a US session closing at 13:00 New York, 18:00 UK; the session after 25 Nov is 27 Nov; an FT
    value read at 17:45 UK on 27 Nov is flagged as read before the close and one read at 18:30 is not."""
    assert pl.us_close_uk("2026-11-27") == "18:00"
    assert pl.next_weekday("2026-11-25") == "2026-11-27"
    assert pl._sessions_ahead("2026-11-24", 3) == ["2026-11-25", "2026-11-27", "2026-11-30"]
    L = ledger(pl, [("2026-11-20", "USA", 50), ("2026-11-20", "USB", 50)])
    pl.update_performance(L, history(), "SPY", "2026-11-27")
    L += [pl.lrow("reported", date="2026-11-27", time_uk="17:45", value_reported=101000.0),
          pl.lrow("reported", date="2026-11-27", time_uk="18:30", value_reported=101000.0)]
    flags = {r["time_uk"]: early for r, _e, _g, early in pl.reconcile(L)}
    assert flags == {"17:45": True, "18:30": False}


# ------------------------------------------------------------------ 8 and 9: a missing quote against a shut market

def test_8_missing_quote_on_an_open_market(pl):
    """Expected: London is open on 24 Nov, so a held London stock without a 24 Nov row stops the log before 24 Nov
    (PERFORMANCE INCOMPLETE) and nothing later is chained over the gap; given the row, the log matches full data."""
    L0 = ledger(pl, [("2026-11-20", "USA", 50), ("2026-11-20", "UKA", 50)])
    L = copy.deepcopy(L0)
    pl.update_performance(L, history(drop={("UKA", "2026-11-24")}), "SPY", "2026-11-27")
    assert max(perf(L)) == "2026-11-23" and pl.INCOMPLETE
    pl.INCOMPLETE.clear()
    pl.update_performance(L, history(), "SPY", "2026-11-27")
    full = copy.deepcopy(L0)
    pl.update_performance(full, history(), "SPY", "2026-11-27")
    assert perf(L)["2026-11-27"]["value_est"] == pytest.approx(perf(full)["2026-11-27"]["value_est"], abs=0.02)


def test_9_genuine_holiday(pl):
    """Expected: (a) a London holiday on a US session, declared under market_closed, leaves the London holding unchanged
    that day and the next day is measured from the last London close; (b) the same gap undeclared stops the log; (c) a
    buy of a stock on its own market's declared holiday also stops the log, since it cannot fill. (The US holiday on
    26 Nov needs no declaration: it is not a session, tests 1 and 4.)"""
    hist = history(drop={("UKA", "2026-11-24")})
    L = ledger(pl, [("2026-11-20", "USA", 50), ("2026-11-20", "UKA", 50)])
    pl.update_performance(L, hist, "SPY", "2026-11-25", closed={("UKA", "2026-11-24")})
    days = [0.0, kept(50, "USA", "2026-11-20", "2026-11-23") + kept(50, "UKA", "2026-11-20", "2026-11-23"),
            kept(50, "USA", "2026-11-23", "2026-11-24"),
            kept(50, "USA", "2026-11-24", "2026-11-25") + kept(50, "UKA", "2026-11-23", "2026-11-25")]
    assert not pl.INCOMPLETE
    assert perf(L)["2026-11-25"]["value_est"] == pytest.approx(chain(days), abs=0.01)
    L = ledger(pl, [("2026-11-20", "USA", 50), ("2026-11-20", "UKA", 50)])
    pl.update_performance(L, hist, "SPY", "2026-11-25")
    assert max(perf(L)) == "2026-11-23" and pl.INCOMPLETE
    pl.INCOMPLETE.clear()
    L = ledger(pl, [("2026-11-20", "USA", 50), ("2026-11-20", "UKB", 50), ("2026-11-24", "UKB", 30), ("2026-11-24", "UKA", 20)])
    pl.update_performance(L, hist, "SPY", "2026-11-25", closed={("UKA", "2026-11-24")})
    assert max(perf(L)) == "2026-11-23" and pl.INCOMPLETE


# ------------------------------------------------------------------ 10: the week the clocks disagree

@pytest.mark.parametrize("day,close_uk", [("2026-10-23", "21:00"), ("2026-10-27", "20:00"), ("2026-10-30", "20:00"),
                                          ("2026-11-02", "21:00"), ("2026-11-27", "18:00")])
def test_10_us_close_in_uk_time(pl, day, close_uk):
    """Expected: UK clocks go back on 25 Oct and US clocks on 1 Nov, so in the week of 26 Oct the US closes at 20:00 UK."""
    assert pl.us_close_uk(day) == close_uk


def test_10_reconcile_in_the_misaligned_week(pl):
    """Expected: a reading at 20:30 UK on Tue 27 Oct is after that day's close (20:00 UK); the same time on Mon 2 Nov is
    before it (21:00 UK). Nothing in the valuation itself depends on clock times."""
    dates = ["2026-10-27", "2026-11-02"]
    L = [pl.lrow("perf", date=d, value_est=V0, day_pct=0.0) for d in dates]
    L += [pl.lrow("reported", date=d, time_uk="20:30", value_reported=V0) for d in dates]
    flags = {r["date"]: early for r, _e, _g, early in pl.reconcile(L)}
    assert flags == {"2026-10-27": False, "2026-11-02": True}
