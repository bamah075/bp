# Claude Code plugins for this repo

`.claude/settings.json` turns on five free, open-source (MIT) plugins. When you open this repo in
Claude Code and trust the folder, Claude Code offers to add their marketplaces and install them.
Check with `/plugin`.

| # | Plugin | Role | What it makes Claude do |
|---|---|---|---|
| 1 | [Superpowers](https://github.com/obra/superpowers) | Lead planner | Brainstorm → plan → tests first → verify before "done" |
| 2 | [Karpathy Skills](https://github.com/multica-ai/andrej-karpathy-skills) | Rule book | Think before coding, simplicity first, surgical changes, goal-driven |
| 3 | [Ponytail](https://github.com/DietrichGebert/ponytail) | Simplifier | Laziest fix that works: YAGNI, stdlib first, fewer lines |
| 4 | [Matt Pocock Skills](https://github.com/mattpocock/skills) | Plan checker | `grill-me` questions your plan; spec, tickets, TDD, code review |
| 5 | [Agent Skills](https://github.com/addyosmani/agent-skills) | Senior mentor | Spec → plan → build small → test → review → ship |

**Not installed: ECC** (`affaan-m/ECC`). It's a large all-in-one kit that mostly repeats the
five above. Add it later if you want its memory and security checks.

## Install by hand (or for all your projects)

```
/plugin install superpowers@claude-plugins-official

/plugin marketplace add multica-ai/andrej-karpathy-skills
/plugin install andrej-karpathy-skills@karpathy-skills

/plugin marketplace add DietrichGebert/ponytail
/plugin install ponytail@ponytail

/plugin marketplace add mattpocock/skills
/plugin install mattpocock-skills@mattpocock

/plugin marketplace add addyosmani/agent-skills
/plugin install agent-skills@addy-agent-skills
```

## Good to know

- **They overlap.** Superpowers, Matt Pocock and Agent Skills each have TDD, planning and review
  skills, so Claude may pick a different one each time. If that's confusing, switch one off in
  `.claude/settings.json` (set it to `false`) or with `/plugin`.
- **Ponytail runs hooks.** After each turn it saves a small stats row (cost, turns, tokens) to
  `~/.config/ponytail/band/` on your own computer. Its webhook is empty by default, so nothing is
  sent anywhere. Turn the stats off with `/plugin` → ponytail → settings → *Task board*.
- **Third-party code.** Apart from Superpowers, these come from their authors' GitHub repos, not
  Anthropic's marketplace. Updates arrive when the authors push them.

## Try it

> "Let's add a voice command to JARVIS that reads today's schedule."

You should see: questions about your plan (brainstorming / grill-me) → a short plan →
a failing test → the simplest code that passes → a check before it says "done".
