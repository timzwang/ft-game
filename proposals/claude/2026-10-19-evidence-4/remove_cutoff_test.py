"""Remove the Mon 26 Oct 07:15 UK cut-off experiment from the playbook, roadmap, state doc and skill copy (Tim's
decision, 19 Oct 2026). Every replacement must match exactly once, or nothing is written for that file. The ordinary
06:36 morning check, the precautionary 07:00 UK cut-off and every order are left as they are.

    python3 remove_cutoff_test.py --playbook P --roadmap R [--state S] [--skill K] [--outdir D]
Writes the edited copies to D (default: in place) and prints each change.
"""
import argparse
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
for k in ("playbook", "roadmap", "state", "skill", "outdir"):
    ap.add_argument("--" + k)
A = ap.parse_args()

EDITS = {
    "playbook": [
        ("Until the FT or the test below settles it, treat **07:00 UK** as the daily cut-off for everything",
         "Until the FT confirms it, treat **07:00 UK** as the daily cut-off for everything"),
        ("- Cut-off test (agreed 17 Oct). At about 07:15 UK on Mon 26 Oct Tim moves one point of weight between two highly "
         "correlated holdings (Exxon Mobil 15 to 14 and Chevron 15 to 16, or the same between whichever oil majors are held). "
         "If the game fills it on Mon 26 Oct, the cut-off is 08:00 UK; if on Tue 27 Oct, it is 07:00 UK. Tim says which in the "
         "project chat; the next evening review records the change through `order` (with `effective` set to the fill date he "
         "reports, or 27 Oct if he has not said) and notes the answer in section 8 of the state doc. Until then the 07:00 UK rule stands.\n",
         "- No cut-off test (removed 19 Oct at Tim's request, playbook 6.11.1): the one-point Exxon and Chevron test planned for "
         "about 07:15 UK on Mon 26 Oct will not be made. No run proposes or records a test order; the 07:00 UK rule stands until "
         "the FT answers.\n"),
        ("Playbook version 6.11, 19 Oct 2026 (evening):",
         "Playbook version 6.11.1, 19 Oct 2026 (late evening): at Tim's request the Mon 26 Oct 07:15 UK cut-off test is "
         "removed (part C). The 06:36 UK morning check, the 07:00 UK cut-off and every order are unchanged; no pipeline, page or "
         "scheduled task changed. Version 6.11, 19 Oct 2026 (evening):"),
    ],
    "roadmap": [
        ("a one-point test between Exxon Mobil and Chevron at about 07:15 on Mon 26 Oct settles it (part C). A draft question "
         "to FT help is in Tim's Gmail drafts.]",
         "a one-point test between Exxon Mobil and Chevron at about 07:15 on Mon 26 Oct was planned (part C). A draft question "
         "to FT help is in Tim's Gmail drafts. Test removed 19 Oct at Tim's request (playbook 6.11.1): 07:00 UK stays the "
         "cut-off until the FT answers.]"),
        ("Handled as 07:00 UK until confirmed (item 44). Once the FT or the 26 Oct test settles it, either keep 07:00 or go "
         "back to 08:00 and a 07:26 morning check, with Tim's agreement.",
         "Handled as 07:00 UK until confirmed (item 44; the 26 Oct test was removed on 19 Oct). Once the FT confirms it, either "
         "keep 07:00 or go back to 08:00 and a 07:26 morning check, with Tim's agreement."),
    ],
    "state": [
        (" The Mon 26 Oct cut-off test order (07:15 UK) must carry the same Coca-Cola weight as that morning's 07:00 order.", ""),
        ("- Mon 26 Oct: cut-off test at about 07:15 UK (part C).",
         "- Mon 26 Oct: Coca-Cola's last order, before 07:00 UK. (The 07:15 UK cut-off test was removed on 19 Oct at Tim's request.)"),
        ("4. The cut-off after the clock change: 07:00 or 08:00 UK. Tim asked FT help on 18 Oct; the one-point Exxon and "
         "Chevron test at about 07:15 UK on Mon 26 Oct settles it (with Chevron now at 10%, the test is Exxon 15 to 14 and "
         "Chevron 10 to 11). Until then 07:00 UK.",
         "4. The cut-off after the clock change: 07:00 or 08:00 UK. Tim asked FT help on 18 Oct. The Mon 26 Oct 07:15 UK test "
         "was removed on 19 Oct at Tim's request, so no test order is made: 07:00 UK stays the cut-off until the FT answers."),
        ("Last updated: Mon 19 Oct 2026, about 22:15 UK (evening review,",
         "Last updated: Mon 19 Oct 2026, about 22:25 UK (hand-run session with Tim: playbook 6.11.1, the 26 Oct 07:15 UK cut-off "
         "test removed; the 07:00 UK cut-off, the 06:36 morning check and the order unchanged; pipeline 7.6 prepared for review, "
         "not deployed, 7.4 stays live. Before that, about 22:15 UK (evening review,"),
        ("- **Playbook version 6.11** (6.11, 19 Oct evening:",
         "- **Playbook version 6.11.1** (6.11.1, 19 Oct late evening: the 26 Oct cut-off test removed at Tim's request; 6.11, 19 Oct evening:"),
        ("- Playbook docs (version 6.11):", "- Playbook docs (version 6.11.1):"),
        ("## 6. Review log (newest first, keep the latest 15)\n\n",
         "## 6. Review log (newest first, keep the latest 15)\n\n- Mon 19 Oct 2026 (about 22:25): Hand-run session with Tim. "
         "The Mon 26 Oct 07:15 UK cut-off test removed (playbook 6.11.1, part C); the 07:00 UK cut-off, the 06:36 morning check "
         "and the order unchanged. ChatGPT's review of pipeline 7.5 (PR #5) checked: its findings reproduced; pipeline 7.6 "
         "prepared on a branch for Tim's approval, not deployed; 7.4 stays live.\n"),
        ("- Fri 16 Oct 2026 (about 01:30): Hand-run session with Tim. GitHub repository `timzwang/ft-game` set up as a shared "
         "mirror; playbook 6.1.\n", ""),
    ],
    "skill": [
        ("A test on Mon 26 Oct settles it; part C of the core doc has the current rule.",
         "No test order is made (the 26 Oct test was removed on 19 Oct); part C of the core doc has the current rule."),
    ],
}

out = Path(A.outdir) if A.outdir else None
ok = True
for kind, pairs in EDITS.items():
    p = getattr(A, kind)
    if not p:
        continue
    text = Path(p).read_text(encoding="utf-8")
    for old, new in pairs:
        n = text.count(old)
        if n != 1:
            print(f"SKIP {kind}: expected one match, found {n}: {old[:70]!r}")
            ok = False
            continue
        text = text.replace(old, new)
        print(f"EDIT {kind}: {old[:70]!r}")
    dst = (out / Path(p).name) if out else Path(p)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text, encoding="utf-8")
sys.exit(0 if ok else 1)
