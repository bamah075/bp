---
name: ultracode
description: Flexible multi-agent coding workflow for this J.A.R.V.I.S repo. Runs any mix of plan, build, test, review, security, debug, docs and explain agents, picked by mode, by flags, or automatically from the request. Use when the user types /ultracode.
argument-hint: "[mode] [--flags] <request>   e.g. /ultracode review --agents security"
---

# /ultracode — flexible agent workflow

Everything after `/ultracode` is the **input**. Read it in this order:
**mode → flags → request**. All three are optional except the request,
which some modes don't need (for example `review` checks the current
uncommitted changes).

If the input is empty, show the "Quick help" block at the bottom and stop.
If the request is unclear, ask ONE clarifying question, then proceed.

---

## Step 1 — Pick the mode

The first word may be a mode. If it isn't one, use `auto`.

| Mode | Agents run, in order | Use it for |
|---|---|---|
| `auto` (default) | Chosen by you from the request (see Step 3) | Anything |
| `full` | planner → coder → tester → reviewer → commit | New features |
| `quick` | coder → tester → commit | Small, obvious changes |
| `plan` | planner only | "How would we do X?" — no code changes |
| `build` | planner → coder | Write code, test it later |
| `test` | tester | Add or run tests for existing code |
| `review` | reviewer + security (in parallel) | Check current changes before committing |
| `fix` | debugger → coder → tester → commit | A bug or error message |
| `secure` | security → coder → tester → commit | Find and fix security problems |
| `docs` | docs → commit | Update README / setup guides |
| `explain` | explainer | Learn how part of the code works |

## Step 2 — Apply the flags

Flags change the mode's agent list. They can appear anywhere in the input.

| Flag | Effect |
|---|---|
| `--agents a,b,c` | Use exactly these agents, in this order (overrides the mode). Short names: `planner, coder, tester, reviewer, security, debugger, docs, explainer`, or any other `ultra-*` agent name |
| `--add a,b` | Add agents to the mode's list (e.g. `full --add docs`) |
| `--skip a,b` | Remove agents from the mode's list (e.g. `full --skip tester`) |
| `--parallel` | Run agents that don't edit files (planner, reviewer, security, explainer, debugger) at the same time where their order doesn't matter |
| `--no-commit` | Do everything except commit and push |
| `--ask` | Pause for the user's OK after every agent |
| `--auto` | Never pause for confirmation (except for destructive actions) |
| `--max-rounds N` | How many fix → re-test rounds before giving up (default 3) |
| `--explain` | Add the explainer at the end, so the user gets a lesson on what changed |

Rules when flags conflict:
- `--agents` wins over the mode, `--add` and `--skip`.
- `--skip` wins over `--add` for the same agent.
- If `tester` is skipped, say clearly in the final report that the change
  is **untested**.
- If `reviewer` and `security` are both skipped on a change that touches
  `os.system`, `subprocess`, file paths or network code, warn the user once.

## Step 3 — `auto` mode: choose the agents yourself

Look at the request and choose:
- Mentions an error, traceback, "doesn't work", "crash", "bug" → `fix`
- "How does", "explain", "what is" → `explain`
- "Review", "check", "is this OK" → `review`
- "Security", "safe", "vulnerab" → `secure`
- "README", "docs", "setup guide" → `docs`
- A one-line change in one file → `quick`
- Anything else → `full`

Always tell the user which mode you picked and why in one line, for
example: `Mode: fix (you pasted a traceback) → debugger → coder → tester → commit`.
They can interrupt and re-run with a different mode.

## Step 4 — Show the run plan, then run it

Before starting, print the final agent list as a single line, for example:
`Running: planner → coder → tester → reviewer+security → commit  (flags: --no-commit)`

Then run each agent with the Agent tool, using `subagent_type: ultra-<name>`.
Pass each agent:
1. The user's request.
2. The output of the agents before it (the plan, the list of changed files,
   the test failures, the review findings).
3. Any project rules from below that matter for its job.

Pause for the user's confirmation when:
- `--ask` is set, after every agent; or
- without `--auto`: the plan touches more than ~5 files, deletes files, or
  changes the startup threads in `jarvis.py`.

### Feedback loops (these happen automatically)
- **Tester fails** → send the failure to coder → re-test. Stop after
  `--max-rounds` failed rounds and report honestly, with the test output.
- **Reviewer or security reports HIGH** → send it to coder → re-test →
  re-review just that finding. Same round limit.
- **Debugger can't reproduce the bug** → stop and ask the user for the
  exact steps or error output. Don't guess at a fix.

## Step 5 — Commit (unless `--no-commit`, or nothing changed)
- Show `git status` and `git diff --stat`.
- Commit with a clear message saying what changed and why.
- Push only to the current branch: `git push -u origin <branch>`.
- Never open a pull request unless the user asks.

## Final report (keep it short)
1. Mode + agents that ran (and any that were skipped, with the reason)
2. What changed and why
3. Files changed
4. Tests: passed / failed counts, or "untested"
5. Open review notes (MEDIUM/LOW that weren't fixed)
6. "How it works" — one paragraph, so the user learns from it

---

## Adding your own agents (plug-in system)

Any file `.claude/agents/ultra-<name>.md` is automatically usable as
`<name>` in `--agents`, `--add` and `--skip`. No change to this file is
needed. To give it its own mode, add a row to the table in Step 1.

Agent file template:
```markdown
---
name: ultra-<name>
description: One line saying what it does and when to use it.
tools: Read, Grep, Glob, Bash          # leave out Edit/Write for read-only agents
---
Instructions for the agent...
```

---

## Project rules (pass the relevant ones to every agent)
- Python 3.9+. Entry point `jarvis.py` (starts background threads);
  command handling lives in `co_brain.py`; features are grouped in folders
  (`Automation/`, `TextToSpeech/`, `NetHyTechSTT/`, `Vision/`,
  `Whatsapp_automation/`, `Time_Operations/`, `Weather_Check/`, ...).
- Cross-platform: `os.path.join` / `pathlib`; guard Windows-only imports
  (`wmi`, `comtypes`, `pycaw`, `winotify`) with `sys.platform`.
  See `PLATFORM_COMPATIBILITY.md`.
- No API keys, tokens or personal data in code or commits.
- Match the existing style of the file being edited.

---

## Quick help (show this when the input is empty)
```
/ultracode <request>                      auto-pick agents
/ultracode full <request>                 plan → build → test → review → commit
/ultracode quick <request>                build → test → commit
/ultracode plan <request>                 plan only, no code changes
/ultracode fix <error or bug>             debug → fix → test → commit
/ultracode review                         review + security check of current changes
/ultracode secure                         find and fix security issues
/ultracode docs <what to document>        update docs
/ultracode explain <file or feature>      learn how it works

Flags: --agents a,b  --add a  --skip a  --parallel  --no-commit
       --ask  --auto  --max-rounds N  --explain
Agents: planner coder tester reviewer security debugger docs explainer
```
