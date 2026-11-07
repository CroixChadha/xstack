# xstack

**Learn while you build.** A Claude Code plugin that keeps you in the loop when you code with AI.

AI can write code fast. xstack makes sure you still understand it: a map before every task, small pieces for you to
write yourself, a strict hint ladder when something breaks, and read-only agents that map whole codebases.
Every choice comes with a "why".

## Why I built this

Vibe coding works until something breaks and you don't know how the pieces connect. I wanted to keep the speed of
agentic coding while still building real skills: reading code, tracing data, and debugging on my own.

## Commands

| Command | What it does |
|---|---|
| `/xstack:onboard` | Setup, competency check, project rundown |
| `/xstack:new-project` | Deep planning for a new project |
| `/xstack:map-the-flow` | ASCII map of how a feature connects |
| `/xstack:leaf-task` | A small piece of code for you to write, with spec and hints |
| `/xstack:error-detective` | Debugging with a 4-level hint ladder |
| `/xstack:explain-it-back` | Explain or predict code to check understanding |
| `/xstack:data-view` | See the data and its shape |
| `/xstack:subagents` | Map the whole codebase with read-only agents |
| `/xstack:help` | Show the menu |

## How it works

- **Two build modes per feature.** Co-op: you and Claude split the coding. Captain: Claude codes, you own the design,
  with short checkpoint cards before and after each chunk.
- **Maps first.** Every task and every bug starts from a map, so you always know where you are.
- **Strict debugging.** Level 1 go search, Level 2 look here, Level 3 what to check, Level 4 the answer, unlocked only
  after you explain the cause.
- **Adapts to you.** Rate yourself beginner, comfortable, or confident per area, and explanations adjust.
- **Plans on disk.** Everything lives in `docs/xstack/` (gitignored), so Claude reads the plan instead of guessing.

## Install

Requires [Claude Code](https://docs.claude.com/en/docs/claude-code) and Python 3. Works in the terminal and in the
VS Code or Cursor extension.

```
claude plugin marketplace add ghostpants05/xstack
claude plugin install xstack@xstack
```

Then open a project and run `/xstack:onboard`.

**Recommended:** copy `plugins/xstack/settings/recommended-settings.json` into `~/.claude/settings.json` to turn off
AI attribution in commits and PRs.

## Safety

A built-in hook guards every command:

- **Always blocked:** production hosts, production env files, pushes to `main`, AI attribution in commits and PRs
- **You approve:** DROP, TRUNCATE, DELETE, UPDATE, migrations, force pushes
- **Fails safe:** if the guard errors, it asks instead of allowing

List production hostnames in `.xstack/protected.json` (hostnames only, never passwords).
Run the tests with `python3 plugins/xstack/tests/test_guard.py`.

## Agents

All read-only, and xstack always asks before launching them.

| Agent | Model | Job |
|---|---|---|
| Scout | Haiku | Inventory of files, stack, entry points |
| Area mappers (max 4) | Sonnet | Map each area's flow |
| Data mapper | Sonnet | Tables and relationships |
| Synthesizer | Opus | Merge into one system map |
| Path checker | Haiku | Confirm every file exists |
| Flow reviewer | Sonnet | Spot check the arrows |

## Status

v0.1.0, actively evolving. See [CHANGELOG.md](CHANGELOG.md).

## License

MIT
