# xstack

**Learn while you build.** A Claude Code plugin for pair coding with Claude without losing track of how your code works.

xstack gives you a map before every task, hands you small pieces to write yourself, coaches you through bugs with a strict
hint ladder, and maps whole codebases with read-only agents. Every choice comes with a "why".

## Commands

```
/xstack:onboard          setup, competencies, project rundown
/xstack:new-project      deep planning for a new project
/xstack:map-the-flow     map how a feature connects
/xstack:leaf-task        a piece for you to write
/xstack:error-detective  debug with the hint ladder
/xstack:explain-it-back  explain or predict code
/xstack:data-view        see the data and its shape
/xstack:subagents        map the whole codebase
/xstack:help             this menu
```

## Install

Requires Claude Code and Python 3 (the safety hook is a Python script).

From GitHub, after you push this repo:
```
/plugin marketplace add ghostpants05/xstack
/plugin install xstack@xstack
```

From a local folder (for testing before you push):
```
/plugin marketplace add ./path/to/xstack-marketplace
/plugin install xstack@xstack
```

Restart Claude Code, then run `/xstack:help` to confirm it loaded.

## One-time setup (do these once)

1. **Turn off AI attribution.** Merge `plugins/xstack/settings/recommended-settings.json` into `~/.claude/settings.json`.
   It removes the Co-Authored-By trailer, the PR footer, and session links, and denies reading production env files.
   Plugins cannot change your settings for you, so this step is manual. The hook also blocks attribution as a backup.
2. **Branch protection.** On GitHub, for each repo: Settings, Branches, protect `main`. This is the strongest guardrail
   because GitHub enforces it, not Claude.
3. **Mermaid preview.** In Cursor or VS Code, install a Mermaid markdown preview extension so `system-map.md` and
   `data-map.md` render as diagrams.

## Per project

`/xstack:onboard` sets everything up. It creates `.xstack/protected.json`. **Add your production hostnames there**
(hostnames only, never passwords). The hook blocks any command that mentions them.

Everything xstack writes lives in `docs/xstack/` and is gitignored. See `plugins/xstack/RULES.md` section 12 for the layout.

## Safety

| Situation | What happens |
|---|---|
| Command mentions a production host | Blocked, always |
| Reading or using a production env file | Blocked, always |
| Push to `main` or `master` (including a bare push while on main) | Blocked, always |
| Commit or PR with AI attribution | Blocked, always |
| DROP, TRUNCATE, DELETE, UPDATE, ALTER ... DROP | You approve in Claude Code's own prompt |
| Migrations and database tooling | You approve |
| Force push to a feature branch | You approve |

If the guard itself errors, it asks you instead of letting the command through.

**Honest limit:** the hook inspects commands Claude runs, not the code inside scripts. If `npm run migrate` reads
production credentials from your `.env`, the hook cannot see that. Keep `.env` pointed at test and production
credentials in a separate file Claude is denied (see xstack:new-project, repo setup).

Run the guard tests anytime:
```
python3 plugins/xstack/tests/test_guard.py
```

## Agent routing

| Role | Model | Effort |
|---|---|---|
| Scout | Haiku | low |
| Area mappers (max 4) | Sonnet | medium |
| Data mapper | Sonnet | medium |
| Synthesizer | Opus | medium |
| Path checker | Haiku | low |
| Flow reviewer | Sonnet | medium |

All agents are read-only. xstack always shows a pre-flight card and waits for your yes before launching them.

## Changing xstack

xstack is meant to morph. When you change it: edit the skill or rule, bump `version` in
`plugins/xstack/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`, add a line to `CHANGELOG.md`,
push, then run `/plugin marketplace update xstack` in Claude Code.
