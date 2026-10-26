"""Tests for scripts/check_data.py (19 Oct 2026, playbook 6.11). Each test copies the frozen 16 Oct snapshot
(tests/fixtures, see conftest) into a temporary folder, breaks one thing and checks that the right check fails; nothing
in the checkout is changed. The snapshot really did lack AbbVie's results event, so on it the check must fail on that
one item: a regression test of the detector. The live data/ files carry no such exception: the data-check workflow
runs check_data.py on them and fails on any missing event."""
import datetime as dt
import importlib.util
import json
import shutil

import pytest

from conftest import REPO


@pytest.fixture(scope="module")
def cd():
    spec = importlib.util.spec_from_file_location("check_data_under_test", REPO / "scripts" / "check_data.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def pl(cd):
    return cd.load_pipeline()


@pytest.fixture()
def tmp_repo(tmp_path, repo):
    for d in ("data", "state"):
        shutil.copytree(repo / d, tmp_path / d)
    return tmp_path


def utc(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)


def run(cd, pl, repo, now="2026-10-17T12:00:00Z", fresh=False):
    rep = cd.check(repo, utc(now), fresh, pl)
    return [l for l in rep.lines if l.startswith("FAIL")], rep


def edit(repo, name, fn):
    p = repo / "data" / f"{name}.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d = fn(d) or d
    p.write_text(json.dumps(d), encoding="utf-8")


def resync(cd, repo):
    """Rewrite last-sync's hashes, as the nightly mirror does after copying files in."""
    p = repo / "state" / "last-sync.md"
    text = p.read_text(encoding="utf-8")
    for f in ("data/stocks.json", "data/ledger.json", "data/history.json", "data/macro.json", "data/panel.json"):
        text = __import__("re").sub(r"^[0-9a-f]{64}(\s+" + f.replace(".", r"\.") + r")$", cd.sha256(repo / f) + r"\1", text, flags=__import__("re").M)
    p.write_text(text, encoding="utf-8")


def test_snapshot_fails_only_on_abbvie(cd, pl, tmp_repo):
    """The frozen 16 Oct files: their one real gap was AbbVie's missing results event."""
    fails, _ = run(cd, pl, tmp_repo)
    assert len(fails) == 1 and "results" in fails[0] and "AbbVie" in fails[0]


def test_duplicate_history_row_fails(cd, pl, tmp_repo):
    edit(tmp_repo, "history", lambda h: h + [dict(h[0])])
    resync(cd, tmp_repo)
    fails, _ = run(cd, pl, tmp_repo)
    assert any(f.startswith("FAIL history") and "duplicate" in f for f in fails)


def test_bad_range_fails(cd, pl, tmp_repo):
    def f(h):
        h[5]["close"] = h[5]["high"] * 1.1
    edit(tmp_repo, "history", f)
    resync(cd, tmp_repo)
    fails, _ = run(cd, pl, tmp_repo)
    assert any(f.startswith("FAIL history") and "range" in f for f in fails)


def test_weights_not_matching_order_fail(cd, pl, tmp_repo):
    def f(s):
        for r in s:
            if r["name"] == "Coca-Cola":
                r["weight"] = 15.0
            if r["group"] == "Cash":
                r["weight"] = 5.0
    edit(tmp_repo, "stocks", f)
    resync(cd, tmp_repo)
    fails, _ = run(cd, pl, tmp_repo)
    assert any(f.startswith("FAIL order") and "latest order" in f for f in fails)


def test_missing_performance_session_fails(cd, pl, tmp_repo):
    edit(tmp_repo, "ledger", lambda L: [r for r in L if not (r["table"] == "perf" and r["date"] == "2026-10-14")])
    resync(cd, tmp_repo)
    fails, _ = run(cd, pl, tmp_repo)
    assert any(f.startswith("FAIL performance") and "2026-10-14" in f for f in fails)


def test_contributions_must_add_up(cd, pl, tmp_repo):
    def f(L):
        r = next(r for r in L if r["table"] == "contrib" and r["date"] == "2026-10-15")
        r["contrib_pts"] = (r["contrib_pts"] or 0) + 0.2
    edit(tmp_repo, "ledger", f)
    resync(cd, tmp_repo)
    fails, _ = run(cd, pl, tmp_repo)
    assert any(f.startswith("FAIL performance") and "contributions" in f for f in fails)


def test_file_changed_after_sync_fails(cd, pl, tmp_repo):
    edit(tmp_repo, "macro", lambda m: m[:-1])
    fails, _ = run(cd, pl, tmp_repo)
    assert any(f.startswith("FAIL sync") and "data/macro.json differs" in f for f in fails)


def test_implied_move_inside_five_sessions_fails(cd, pl, tmp_repo):
    def f(L):
        for r in L:
            if r["table"] == "event" and r["kind"] == "results" and r["stock"] == "Coca-Cola":
                r["date"] = "2026-10-21"
    edit(tmp_repo, "ledger", f)
    resync(cd, tmp_repo)
    fails, _ = run(cd, pl, tmp_repo)
    assert any("no implied move for a report inside five sessions: Coca-Cola" in f for f in fails)


def set_run(repo, when):
    p = repo / "state" / "last-sync.md"
    p.write_text(__import__("re").sub(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", when, p.read_text(encoding="utf-8"), count=1), encoding="utf-8")


def test_fresh_needs_a_recent_mirror_and_the_latest_session(cd, pl, tmp_repo):
    set_run(tmp_repo, "2026-10-18T22:00:00Z")                                    # the stored files: data to Fri 16 Oct
    fails, _ = run(cd, pl, tmp_repo, now="2026-10-19T23:15:00Z", fresh=True)
    assert any("FAIL fresh: the last mirror ran" in f for f in fails)
    assert any("latest closed US session is 2026-10-19" in f for f in fails)
    fails, _ = run(cd, pl, tmp_repo, now="2026-10-18T23:30:00Z", fresh=True)     # Sunday night: Friday is the latest
    assert not any(f.startswith("FAIL fresh") for f in fails)


@pytest.mark.parametrize("now,expected", [
    ("2026-10-19T20:40:00Z", "2026-10-19"),      # Mon, 16:40 New York (BST, US on EDT)
    ("2026-10-19T20:20:00Z", "2026-10-16"),      # Mon before the close has settled: Friday
    ("2026-10-24T11:15:00Z", "2026-10-23"),      # Saturday
    ("2026-10-27T20:45:00Z", "2026-10-27"),      # week of 26 Oct: UK on GMT, US still on EDT
    ("2026-11-26T23:15:00Z", "2026-11-25"),      # Thanksgiving: no session
    ("2026-11-27T18:40:00Z", "2026-11-27"),      # half day: 13:00 New York close
])
def test_expected_session(cd, pl, now, expected):
    assert cd.expected_session(utc(now), pl) == expected


def test_cli_exit_code(cd, tmp_repo):
    assert cd.main(["--repo", str(tmp_repo), "--now", "2026-10-17T12:00:00Z"]) == 1     # AbbVie, as above (frozen snapshot)


# ----------------------------------------------------------------- added 19 Oct evening (recalculation, deadlines, absence)

def test_snapshot_recalculates_exactly(cd, pl, tmp_repo):
    _, rep = run(cd, pl, tmp_repo)
    assert any(l.startswith("PASS recalc: 6 stored values") for l in rep.lines)


def test_changed_price_fails_recalculation(cd, pl, tmp_repo):
    """A held stock's close quietly changed after the session was logged: the ranges still look fine, the compounding
    and the contributions still add up, but the stored values no longer follow from the prices."""
    def f(h):
        r = next(r for r in h if r["ticker"] == "XOM" and r["date"] == "2026-10-15")
        r["close"] = round((r["high"] + r["low"]) / 2 + 0.01, 2)
    edit(tmp_repo, "history", f)
    resync(cd, tmp_repo)
    fails, _ = run(cd, pl, tmp_repo)
    assert [f for f in fails if f.startswith("FAIL recalc")] and not [f for f in fails if f.startswith("FAIL history")]


def move_ko(L, **kw):
    for r in L:
        if r["table"] == "event" and r["kind"] == "results" and r["stock"] == "Coca-Cola":
            r.update({"date": "2026-10-21", "time_uk": "before US open"}, **kw)


def test_documented_absence_of_implied_move_is_a_warning(cd, pl, tmp_repo):
    edit(tmp_repo, "ledger", lambda L: move_ko(L, text="Implied move unavailable: no options page readable on 20 Oct",
                                               last_order="Before 07:00 Tue 20 Oct"))
    resync(cd, tmp_repo)
    fails, rep = run(cd, pl, tmp_repo)
    assert not any("implied move for a report inside five sessions" in f for f in fails)
    assert any(l.startswith("WARN results: implied move recorded as unavailable") and "Coca-Cola" in l for l in rep.lines)


@pytest.mark.parametrize("last_order,bad", [("Before 07:00 Tue 20 Oct", None),
                                            ("Before 07:00 Wed 21 Oct", "later than the last possible order day, 2026-10-20"),
                                            ("Before 09:00 Tue 20 Oct", "after the 08:00 UK cut-off"),
                                            ("", "none recorded")])
def test_last_order_inside_five_sessions(cd, pl, tmp_repo, last_order, bad):
    """Coca-Cola reporting before the US open on Wed 21 Oct: the last order is before 07:00 UK on Tue 20 Oct."""
    edit(tmp_repo, "ledger", lambda L: move_ko(L, implied_pct=3.0, last_order=last_order))
    resync(cd, tmp_repo)
    fails, _ = run(cd, pl, tmp_repo)
    hit = [f for f in fails if f.startswith("FAIL results: last order")]
    assert (not hit) if bad is None else (hit and bad in hit[0])


def test_after_close_report_allows_an_order_that_morning(cd, pl):
    ev = {"date": "2026-10-28", "time_uk": "after US close (est.)", "last_order": "Before 07:00 Wed 28 Oct"}
    assert cd.last_order_problem(ev, pl) is None
    ev = {"date": "2026-10-29", "time_uk": "11:30", "last_order": "Before 07:00 Wed 28 Oct"}     # Lilly: before the open
    assert cd.last_order_problem(ev, pl) is None
    ev = {"date": "2026-10-29", "time_uk": "11:30", "last_order": "Before 07:00 Thu 29 Oct"}
    assert "later than" in cd.last_order_problem(ev, pl)
    ev = {"date": "2026-11-27", "time_uk": "before US open", "last_order": "Before 07:00 Wed 25 Nov"}   # 26 Nov: no US session
    assert cd.last_order_problem(ev, pl) is None


def test_event_on_another_date_fails(cd, pl, tmp_repo):
    """7.6 (was a WARN in 7.5, ChatGPT's PR #5 finding 2): a holding's only results event on a date other than its stock
    data's no longer counts as coverage; it is a FAIL until the date is corrected or the event is marked uncertain."""
    def f(s):
        for r in s:
            if r["name"] == "Coca-Cola":
                r["next_results"] = "28 Oct, before US open"
    edit(tmp_repo, "stocks", f)
    resync(cd, tmp_repo)
    fails, _ = run(cd, pl, tmp_repo)
    assert any(f.startswith("FAIL results: holding(s) whose results event is not on the date") and "Coca-Cola" in f for f in fails)


def test_order_replaced_before_it_filled_is_no_trade(cd, pl, tmp_repo):
    """26 Oct: an order replaced before it filled leaves a zero row for a name never held (Hasbro, 22 Oct). That is no
    trade, so it needs no contribution row; before the fix the data check failed every night on it."""
    def f(L):
        r = dict(next(r for r in L if r["table"] == "position" and r["effective"] == "2026-10-15"))
        r.update(id="position:2026-10-15:Hasbro", name="Hasbro", ticker="HAS", weight=0.0)
        L.append(r)
    edit(tmp_repo, "ledger", f)
    resync(cd, tmp_repo)
    fails, _ = run(cd, pl, tmp_repo)
    assert len(fails) == 1 and "AbbVie" in fails[0]


def test_held_name_without_contribution_still_fails(cd, pl, tmp_repo):
    """The 26 Oct fix must not hide a real gap: a name held that session with no contribution row still fails."""
    def f(L):
        L.remove(next(r for r in L if r["table"] == "contrib" and r["date"] == "2026-10-15"))
    edit(tmp_repo, "ledger", f)
    resync(cd, tmp_repo)
    fails, _ = run(cd, pl, tmp_repo)
    assert any(f.startswith("FAIL performance") and "no contribution row" in f for f in fails)
