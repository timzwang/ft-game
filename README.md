# ft-game

[![data-check](https://github.com/timzwang/ft-game/actions/workflows/data-check.yml/badge.svg)](https://github.com/timzwang/ft-game/actions/workflows/data-check.yml) [![tests](https://github.com/timzwang/ft-game/actions/workflows/tests.yml/badge.svg)](https://github.com/timzwang/ft-game/actions/workflows/tests.yml)

Tim's entry ("Seeking Beta") in the FT Stock Picking Game, 5 Oct to 27 Nov 2026: a virtual 100,000-credit portfolio of 5 to 20 stocks. The aim is a finish in roughly the top 2% of players. No real money is involved.

**Current version: 6.14.2 (27 Oct 2026, late evening): feed 1.2.1 takes the Japanese 10-year from CNBC's benchmark figure first and the Ministry of Finance's constant-maturity figure only as the fallback, so the series uses one measure. Previous: 6.14.1 (26 Oct 2026, late evening): the UK, German, French, Italian and Japanese 10-year yields come from the price feed (feed 1.2: CNBC, and the Japanese Ministry of Finance for Japan), tradingeconomics only as the fallback. Previous: 6.14 (26 Oct 2026, late afternoon): the order cut-off is 08:00 UK as the FT confirmed (pipeline 7.8, run from commit `9760163`), a nightly watchdog checks every run at 22:47 UK, and the data check's false failure since 22 Oct is fixed. Previous: 6.13.2 (26 Oct 2026, afternoon): every run fixes what it can and tells Tim about any issue, fixed or not, even on a quiet day; sessions with Tim check for open issues first; runs fetch the pinned script commit when their clone is shallow. Previous: 6.13.1 (26 Oct 2026, afternoon): runs take the pipeline script (7.7, same hash) from this repository at commit `87d8f64`, because the session's permission check refused the artifact copy; the mirror pushes `HEAD:main`. Previous: 6.13 (21 Oct 2026, late evening): the endgame stance, approved by Tim: the guardrails that kept the book defensive are suspended to the end of the game, and the 22 Oct evening review switches to a high-beta technology book (order A or B, core playbook part D). Previous: 6.12.1 (21 Oct 2026, late evening): price feed 1.1 sends two years of rows to every list or requested stock not yet stored (a panel member requested as a candidate had been given ten), names any still short, and the evening review re-requests a short candidate once before leaving it out. Previous: 6.12 (21 Oct 2026, afternoon): a price feed on GitHub (`feed/`) that the evening and weekly reviews and the price refreshes read first, so they no longer depend on fetching one page per stock, and pipeline 7.7 (7.6, after ChatGPT's review of 7.5, plus a `feed` command) deployed. Previous: 6.11.1 (19 Oct 2026, late evening): the Mon 26 Oct 07:15 UK cut-off test removed at Tim's request. Before that 6.11 (19 Oct 2026, evening): pipeline 7.4 (every change of order records its expected benefit before it fills, scored by the STANDSTILL test) and a data check on every mirror (`scripts/check_data.py`, workflow `data-check`); before that 6.10, pipeline 7.3, the 1.0 results budget for 27 to 30 Oct and regression tests.** Every version and its changes are in `CHANGELOG.md`; releases from 6.0 on are listed under Releases.

This repository is a **mirror and a place to propose changes**. The live system runs in Claude (scheduled tasks, a Claude Project and a dashboard artifact). Claude writes snapshots here; ChatGPT and Tim read them and propose changes through pull requests.

## Start here

| To understand | Read |
|---|---|
| What Claude and ChatGPT last told each other | `handoff/` (newest notes; read `handoff/README.md` first) |
| What is held now, why, and what happened recently | `state/ft-game-state.md` (sections 1 to 5) |
| The rules every decision follows | `docs/ft-game-rules.md` (part E) |
| The game's rules, guardrails, timing and output style | `docs/ft-game-playbook.md` (parts A to D, I to K) |
| How each scheduled run works | `docs/ft-game-run-*.md` (part H) |
| Data sources and the pipeline's commands | `docs/ft-game-data.md` (parts F and G) |
| What has been built and what is still open | `docs/ft-game-roadmap.md` |
| The schedule | `ops/scheduled-tasks.md` |
| What changed in each version, and when | `CHANGELOG.md` |
| The broad scan: its rules, lists and record | `scan/README.md`, `scan/latest.md` |
| The price feed: what it carries and how it is checked | `feed/README.md`, `feed/latest.md` |
| When this copy was taken, and its file hashes | `SYNC.md`, and `state/last-sync.md` for the latest nightly mirror |

## Layout

```
docs/        playbook (core, rules, data, five run docs), roadmap, page notes
state/       ft-game-state.md: the narrative record, rewritten by every evening review
scripts/     ft_pipeline.py (version 7.7: scoring, performance, risk, day call, panel test,
             drift scan, standstill, expected benefit, the feed command); ft_score.py (screening);
             check_data.py (integrity and freshness of data/ and state/). Standard-library Python 3.
tests/       regression tests (pytest), run by .github/workflows/tests.yml on code changes;
             .github/workflows/data-check.yml runs scripts/check_data.py on every data push and
             after each evening and weekly review (a red badge above means look at the latest run)
scan/        the broad scan (scan.py, run nightly by .github/workflows/scan.yml) and its output
feed/        the price feed (feed.py, run by .github/workflows/feed.yml after the US close and on request):
             latest.json and live.json, read by the scheduled runs (data doc G8)
data/        stocks, ledger, history, macro, panel (JSON), written only by the pipeline
page/        the dashboard: index.html, app.js, fonts.css, logos.json
skills/      the two saved Claude skills (ft-game-playbook, stock-score)
ops/         the scheduled tasks, key redacted
handoff/     notes between Claude and ChatGPT, one per session (format in handoff/README.md)
proposals/   chatgpt/ and claude/: proposals for Tim to review
sync-test/   the 16 Oct connection test (kept as a record)
SYNC.md      sync manifest
```

The docs keep the paths they have in the Claude Project (`claude/ft-game-*.md`). In this repository those files are in `docs/`, except the state doc, which is in `state/`.

## Running the pipeline

```
python3 -I scripts/ft_pipeline.py                 # prints the full instructions
python3 -I scripts/ft_pipeline.py report --ledger data/ledger.json
python3 -I scripts/ft_pipeline.py panel --panel data/panel.json --history data/history.json
python3 -I scripts/check_data.py                  # integrity checks; --fresh also checks the last mirror
```

Tests (offline; they read the stored files and write only to a temporary folder):

```
pip install -r scan/requirements.txt pytest
python -m pytest -q tests
```

`report` and `panel` only read. The other commands (`template`, `run`, `refresh`, `reorder`, `closes`) are for Claude's scheduled runs, and write to a folder given by `--out`.

## Who writes what

| Writer | May change | How |
|---|---|---|
| Claude's scheduled runs | `data/`, `state/`, `SYNC.md`, and a line in `scan/request.txt` or `feed/request.txt` | Commit to `main` after each evening and weekly review, and a request line when the scan or the feed is needed (data doc G7, G8). Pull and rebase first; never force-push |
| The scan and feed jobs (GitHub Actions) | `scan/`, `feed/` | Commit to `main` after each run |
| Claude in a session with Tim | `docs/`, `scripts/`, `page/`, `skills/`, `ops/` | Only to mirror a change Tim approved |
| ChatGPT | Nothing on `main` | A branch and pull request, or a file under `proposals/chatgpt/` |
| Tim | Everything | Reviews and merges pull requests |

A change merged here does **not** reach the live system by itself. A code or playbook change goes live only when Tim asks Claude to apply it in the Claude Project and artifact; for the pipeline, that also means recording its new sha256 in part B of the playbook, which every run checks before running the script.

## Rules for any proposal

- Never commit an API key, token, password, account number or personal detail. The market data key lives only inside two Claude scheduled tasks; files here show it as `<REDACTED: held only in the scheduled task>`.
- Keep the existing style: British English, no em-dashes, UK times, plain words.
- The score's weights, the confidence anchor and the panel's members change only with Tim's agreement (playbook part K).
- Every portfolio figure is a sum of weight times return, never an average of returns (playbook part C).
- Say what evidence a change rests on. Seven weeks is too short to prove a method, so be honest about sample sizes.
