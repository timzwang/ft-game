# Handoff log

How Claude and ChatGPT keep each other up to date on Tim's FT Stock Picking Game system. Neither assistant can read the other's chats, so this folder is the bridge. Set up on 18 Oct 2026 at Tim's request (playbook version 6.6).

## The rule

- **Before starting** any piece of work on this system with Tim, read the newest notes here, from both assistants, since your own last note.
- **At the end** of any session that decided, changed or found something, write one note.
- **Notes say who said what. The rest of the repository says what is true.** If a note and the live files disagree, the files win: check `CHANGELOG.md`, `state/ft-game-state.md` and `state/last-sync.md` before relying on a note. The live system runs in Claude; this repository is a mirror (see `README.md`).

## Who writes how

| Writer | How | Where |
|---|---|---|
| Claude, in a session with Tim | Commits straight to `main` | `handoff/YYYY-MM-DD-claude.md` |
| ChatGPT | Never `main`: a branch `chatgpt/handoff-YYYY-MM-DD` and a pull request that Tim merges | `handoff/YYYY-MM-DD-chatgpt.md` |
| Scheduled Claude runs | Not yet (they do not write notes) | |

A second note by the same assistant on the same day adds `-2`, `-3` to the name. Never edit or delete another assistant's note; reply in your own.

Longer documents (audits, reviews, evidence) go in `proposals/claude/` or `proposals/chatgpt/`; the note links to them.

## Format

Keep a note under about one page. British English, UK times, no em-dashes.

```
# <date>, <Claude|ChatGPT>: <one-line title>

Session: <UK date and time>, <what Tim asked for>
Read before starting: <the notes and files read, with the repository commit>

## Decided
- <decision> (Tim approved | proposed only)

## Changed
- <file or system part>: <change> (commit <hash>, or "not applied")

## Found
- <finding> (evidence: <file and line, or data>)

## Open questions for the other assistant
- <question>: <what would answer it>

## Not changed
- <anything deliberately left alone>
```
