---
name: ultracode
description: Full-cycle coding workflow for this J.A.R.V.I.S repo — plan, build, test, review, then commit. Use when the user types /ultracode followed by a feature, bug fix or refactor request.
---

# /ultracode — Plan → Build → Test → Review → Commit

The user's request follows the command. If it is empty or unclear, ask ONE
clarifying question before starting, then proceed.

Work through these phases in order. Before each phase, tell the user in one
line which phase you are entering and why. Explain the "why" behind every
key decision — the user wants to learn, not just receive code.

## 1. Plan — agent: `ultra-planner`
- Hand the request to the `ultra-planner` agent.
- It returns: files to touch, step-by-step plan, risks, and how to test.
- Show the plan to the user as a short numbered list.
- If the change is large (> ~5 files) or risky (deletes data, changes
  startup flow in `jarvis.py`), ask the user to confirm before building.

## 2. Build — agent: `ultra-coder`
- Give `ultra-coder` the approved plan. It edits code following the
  project rules below.
- Keep the change to what the plan says; no drive-by refactors.

## 3. Test — agent: `ultra-tester`
- `ultra-tester` writes/updates pytest tests under `tests/` and runs them.
- Hardware (mic, speaker, camera, pyautogui, WhatsApp, network) is mocked —
  this code often runs where none of that exists.
- If tests fail, send the failure back to `ultra-coder`, then re-test.
  Stop after 3 failed rounds and report honestly with the output.

## 4. Review — agent: `ultra-reviewer`
- `ultra-reviewer` checks the diff for bugs, security issues, and
  cross-platform breakage (Windows / macOS / Linux).
- Fix any HIGH-severity finding (back to step 2), re-run tests.
- List remaining low-severity notes for the user; don't silently drop them.

## 5. Commit
- Run `git status` and `git diff --stat` and show the summary.
- Commit with a clear message: what changed and why.
- Push only to the current branch with `git push -u origin <branch>`.
- Never create a pull request unless the user asks.

## Final report (keep it short)
1. What was built and why
2. Files changed
3. Test results (passed / failed, with numbers)
4. Review notes still open
5. A one-paragraph "how it works" explanation for learning

## Project rules (apply in every phase)
- Python 3.9+. Entry point is `jarvis.py`; command handling lives in
  `co_brain.py`; features are grouped in folders (`Automation/`,
  `TextToSpeech/`, `NetHyTechSTT/`, `Vision/`, `Whatsapp_automation/`, ...).
- Cross-platform: use `os.path.join` / `pathlib`, never hard-coded `\\`
  paths. Guard Windows-only imports (`wmi`, `comtypes`, `pycaw`,
  `winotify`) with `sys.platform` checks. See `PLATFORM_COMPATIBILITY.md`.
- Never commit API keys, tokens, or personal data files.
- Match the existing code style of the file you edit.
