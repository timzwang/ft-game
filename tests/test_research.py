"""Version 7.8 (prepared 21 Oct 2026, for deployment after the 27 to 30 Oct results cluster): the read-only `research`
command, the top-five panel test (roadmap item 39) and the overbought split of the shadow ratings (item 42). Nothing here
is wired into `run`, `refresh` or `reorder`, so the files those commands write are unchanged."""
import json
import subprocess
import sys

from conftest import REPO


def obs_row(date, ticker, pts, ex, ex_late=None):
    return {"date": date, "ticker": ticker, "pts": pts, "parts": {}, "ex": ex, "ex_late": ex_late, "live": False}


def panel_day(date, top_ret, rest_ret, n=10):
    """n members: five with high points returning top_ret, the rest with low points returning rest_ret."""
    return ([obs_row(date, f"T{i}", 40 - i, top_ret) for i in range(5)]
            + [obs_row(date, f"R{i}", 10 - i, rest_ret) for i in range(n - 5)])


def test_topfive_by_hand(pl):
    obs = panel_day("2026-01-05", 2.0, 0.0) + panel_day("2026-01-12", -1.0, 1.0)
    r = pl.panel_topfive(obs)
    assert r["dates"] == 2
    # day 1: top five +2.0, panel average +1.0 -> +1.0; day 2: top five -1.0, panel average 0.0 -> -1.0
    assert abs(r["vs_panel"]["mean"] - 0.0) < 1e-12
    assert abs(r["vs_index"]["mean"] - 0.5) < 1e-12
    assert r["vs_panel"]["pos"] == 50.0


def test_topfive_skips_thin_dates_and_missing_returns(pl):
    thin = panel_day("2026-01-05", 2.0, 0.0, n=9)                       # below PANEL_MIN_STOCKS
    late = panel_day("2026-01-12", 2.0, 0.0)
    assert pl.panel_topfive(thin)["dates"] == 0
    assert pl.panel_topfive(late, ret="ex_late")["dates"] == 0          # no ex_late values given


def test_topfive_ties_broken_by_ticker(pl):
    obs = [obs_row("2026-01-05", f"S{i:02d}", 20, float(i)) for i in range(12)]   # every member on the same points
    r = pl.panel_topfive(obs)
    # S00..S04 are chosen, returning 0..4 (mean 2.0); the panel mean is 5.5
    assert abs(r["vs_index"]["mean"] - 2.0) < 1e-12 and abs(r["vs_panel"]["mean"] - (2.0 - 5.5)) < 1e-12


def test_bootstrap_is_deterministic_and_brackets_the_mean(pl):
    vals = [0.5, -0.2, 1.1, 0.3, -0.7, 0.9, 0.0, 0.4]
    a, b = pl._block_boot(vals), pl._block_boot(vals)
    assert a == b
    m = sum(vals) / len(vals)
    assert a[0] <= m <= a[1]
    assert pl._block_boot([1.0]) == (None, None)


def shadow(pl, score, beat, ret, spx, flags=""):
    r = pl.lrow("shadow", date="2026-10-01", name="X", ticker="X", score=score, text=flags)
    r.update(beat=beat, ret_pct=ret, spx_ret_pct=spx)
    return r


def test_overbought_split_by_hand(pl):
    L = [shadow(pl, 70, "no", -2.0, 1.0, "overbought: RSI above 75"),
         shadow(pl, 50, "yes", 3.0, 1.0, "overbought: RSI above 75; extended"),
         shadow(pl, 65, "yes", 2.0, 0.0),
         shadow(pl, 40, "no", -1.0, 0.0),
         shadow(pl, 80, None, None, None, "overbought: RSI above 75")]           # not settled: left out
    s = pl.overbought_split(L)
    assert s["overbought"]["n"] == 2 and s["overbought"]["hit"] == 50.0 and abs(s["overbought"]["gap"] - (-3.0 + 2.0) / 2) < 1e-12
    assert s["not overbought"]["n"] == 2 and abs(s["not overbought"]["gap"] - 0.5) < 1e-12
    hi = pl.overbought_split(L, min_score=60)
    assert hi["overbought"]["n"] == 1 and hi["not overbought"]["n"] == 1


def test_research_command_writes_nothing(repo, tmp_path):
    before = {p.name: p.read_bytes() for p in (repo / "data").iterdir()}
    out = subprocess.run([sys.executable, "-I", str(REPO / "scripts" / "ft_pipeline.py"), "research",
                          "--history", str(repo / "data" / "history.json"), "--ledger", str(repo / "data" / "ledger.json"),
                          "--panel", str(repo / "data" / "panel.json")],
                         capture_output=True, text=True, cwd=tmp_path, check=True).stdout
    assert "TOP-FIVE PANEL history, close to close:" in out and "OVERBOUGHT SPLIT (all scores):" in out
    assert {p.name: p.read_bytes() for p in (repo / "data").iterdir()} == before
    assert not any(tmp_path.iterdir())
