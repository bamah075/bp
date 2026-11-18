# Superpowers for this repo

[Superpowers](https://github.com/obra/superpowers) (MIT, by Jesse Vincent) gives Claude Code a
working method: **brainstorm → plan → write tests first → build → check its own work before saying "done".**

## How it's turned on

`.claude/settings.json` enables the plugin from Anthropic's official marketplace:

```json
{ "enabledPlugins": { "superpowers@claude-plugins-official": true } }
```

When you open this repo in Claude Code and trust the folder, Claude Code offers to install it.
To install it by hand instead (or for all your projects), run inside Claude Code:

```
/plugin install superpowers@claude-plugins-official
```

Check it worked: run `/plugin` and look for `superpowers`, or start a new session and ask
"what superpowers skills do you have?".

## What you get (skills load automatically when they fit)

| Stage | Skill | What it makes Claude do |
|---|---|---|
| Idea | `brainstorming` | Asks questions and agrees a design with you before any code |
| Plan | `writing-plans` | Breaks the design into small, testable steps |
| Build | `test-driven-development` | Writes a failing test first, then the code to pass it |
| Build | `subagent-driven-development` / `executing-plans` | Works through the plan task by task |
| Bugs | `systematic-debugging` | Finds the root cause before changing anything |
| Finish | `verification-before-completion` | Runs the checks before claiming "fixed" or "done" |
| Review | `requesting-code-review` / `receiving-code-review` | Reviews work; weighs feedback instead of blindly applying it |
| Ship | `finishing-a-development-branch`, `using-git-worktrees` | Clean branch handling |

## Try it

> "Let's add a voice command to JARVIS that reads today's schedule."

Claude should start with **brainstorming** (questions), then a **plan**, then **tests**, then code.
