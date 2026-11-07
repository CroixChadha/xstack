---
name: help
description: Show the xstack command menu, what each xstack skill does, and where xstack keeps its files. Use when the user types /xstack:help, asks what xstack can do, or seems unsure which xstack command to run.
---

# xstack:help

Print this menu exactly (it is a code block on purpose so it lines up in the terminal):

```
xstack: learn while you build

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

Then add a short status card, read from `docs/xstack/` (skip any line whose file does not exist):

- **Project:** one line from `onboarding.md`
- **Current feature:** from `plans/progress.md` or the newest `features/` folder, plus its build mode (Co-op or Captain)
- **Maps:** system map built on `<date>` at commit `<short sha>` (from `discovery/_manifest.md`)
- **Suggested next:** the single most useful command right now, with one line of why

If `docs/xstack/onboarding.md` does not exist, the suggested next command is `/xstack:onboard`.

Do not read any other files. Keep it to the menu plus that card.
