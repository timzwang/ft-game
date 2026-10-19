# ft-game

[![data-check](https://github.com/timzwang/ft-game/actions/workflows/data-check.yml/badge.svg)](https://github.com/timzwang/ft-game/actions/workflows/data-check.yml) [![tests](https://github.com/timzwang/ft-game/actions/workflows/tests.yml/badge.svg)](https://github.com/timzwang/ft-game/actions/workflows/tests.yml)

Tim's entry ("Seeking Beta") in the FT Stock Picking Game, 5 Oct to 27 Nov 2026: a virtual 100,000-credit portfolio of 5 to 20 stocks. The aim is a finish in roughly the top 2% of players. No real money is involved.

**Current version: 6.11 (19 Oct 2026, evening): pipeline 7.4 (every change of order records its expected benefit before it fills, scored by the STANDSTILL test) and a data check on every mirror (`scripts/check_data.py`, workflow `data-check`). Previous: 6.10, pipeline 7.3, the 1.0 results budget for 27 to 30 Oct and regression tests.** Every version and its changes are in `CHANGELOG.md`; releases from 6.0 on are listed under Releases.

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
| When this copy was taken, and its file hashes | `SYNC.md`, and `state/last-sync.md` for the latest nightly mirror |

## Layout

```
docs/        playbook (core, rules, data, five run docs), roadmap, page notes
state/       ft-game-state.md: the narrative record, rewritten by every evening review
scripts/     ft_pipeline.py (version 7.4: scoring, performance, risk, day call, panel test,
             drift scan, standstill, expected benefit); ft_score.py (screening);
             check_data.py (integrity and freshness of data/ and state/). Standard-library Python 3.
tests/       regression tests (pytest), run by .github/workflows/tests.yml on code changes;
             .github/workflows/data-check.yml runs scripts/check_data.py on every data push and
             after each evening and weekly review (a red badge above means look at the latest run)
scan/        the broad scan (scan.py, run nightly by .github/workflows/scan.yml) and its output
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
| Claude's scheduled runs | `data/`, `state/`, `SYNC.md` | Commit to `main` after each evening and weekly review. Pull and rebase first; never force-push |
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
