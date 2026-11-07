---
name: new-project
description: Deep planning for a new project (problem, must/should/won't scope, stack choice the user researches and decides, user-first data design, architecture in plan mode, walking skeleton, feature breakdown, safe repo setup), plus feature planning and the Co-op or Captain build loop for any feature, new or existing code. Use when the user runs /xstack:new-project, when xstack:onboard finds a new project, or when a feature needs its plan and build mode set.
---

# xstack:new-project

First read `${CLAUDE_PLUGIN_ROOT}/RULES.md`. If `docs/xstack/onboarding.md` is missing, run xstack:onboard first.

This skill has two parts:
- **Part A: Project planning** (new projects, usually one long session)
- **Part B: Feature planning and the build loop** (every feature, new or existing code)

Save progress to `docs/xstack/plans/progress.md` after every phase, so a session can stop anywhere and the
next one picks up exactly there. At the start, if `progress.md` shows Part A in progress, resume from that phase.

---

## Part A: Project planning

### A1. Problem
Reuse the rundown in `onboarding.md` (what it is for, who uses it, what done looks like). Confirm it, sharpen it.
Write `docs/xstack/plans/project-plan.md` from `${CLAUDE_PLUGIN_ROOT}/templates/project-plan.md`.

### A2. Scope
Sort features into **Must / Should / Won't (for now)** with the user. Push for a short Must list.
Why: scope creep is the number one reason side projects stall. Writing down "won't" is as important as "must".

### A3. Stack choice (the user decides)
Propose 2 to 3 stack options. For each:
- **Fits because:** one or two bullets tied to the project and the user's competency levels
- **Tradeoffs:** one or two bullets
- **Market note:** what remote job postings commonly ask for here, framed as "check a few postings yourself"
- **Research prompts:** 2 or 3 things to look up and questions to answer
Then stop and let the user research. Do not pick for them. Record their choice and their reason in `project-plan.md`.
Why: evaluating tools is a real engineering skill, and owning the decision means understanding the build.

### A4. Data design (the user goes first)
Ask with AskUserQuestion: **"Want to try designing the data first, or should Claude propose it?"**
Same coaching as xstack:data-view Step 4. Result goes in `project-plan.md` and becomes the first `data-map.md`.

### A5. Architecture (plan mode)
Enter plan mode (use the EnterPlanMode tool; if it is not available, ask the user to switch to plan mode with Shift+Tab).
Go back and forth with the user in short cards until the architecture is agreed:
- Main parts and how they talk (ASCII sketches while discussing)
- Where key logic lives, with a why for each choice
- Auth, config, and environments (test vs production)
Nothing is written to disk until the user approves. Then write the planned `docs/xstack/system-map.md` and
`data-map.md` in Mermaid, every box marked as planned.
Why plan mode: it is read-only, so nothing gets built on an unapproved plan.

### A6. Walking skeleton first
The first feature is always the walking skeleton: the thinnest working path end to end
(one button saves one thing and displays it, through every layer). Features grow from there.
Why: it surfaces integration problems on day one, when they are cheapest to fix.

### A7. Feature breakdown
Turn the Must list into features in build order (skeleton first). For each, create
`docs/xstack/features/<feature-slug>/plan.md` from `${CLAUDE_PLUGIN_ROOT}/templates/plan.md` with a checklist.
Build mode stays unset until Part B.

### A8. Repo setup (safe from day one)
Do each step only with the user's go-ahead, and show what will change first:
- `git init` if needed, default branch `main`, then work on `feat/<feature>` branches
- `.gitignore` for the chosen stack: `.env`, `.env.*` (but keep `.env.example`), dependency folders
  (`node_modules/`, `venv/`, `.venv/`), caches (`__pycache__/`, `.pytest_cache/`, `dist/`, `build/`),
  editor and OS files (`.vscode/`, `.idea/`, `.DS_Store`, `Thumbs.db`), plus `docs/xstack/` and `.xstack/`
- `.env.example` with placeholder names only, no values
- Env split: `.env` points at the test environment only. Production credentials live in a separate file
  (for example `.env.production`) that Claude is never allowed to read. List it in `.xstack/protected.json`.
- `.xstack/protected.json` with production hostnames (hostnames only, never passwords)
- Reminder card: turn on **branch protection for main** in GitHub (Settings, Branches). It is the strongest guardrail.
Why day one: safety is free at the start and painful to retrofit.

Then mark Part A done in `progress.md` and move to Part B for the walking skeleton.

---

## Part B: Feature planning and the build loop

Used for every feature: each feature from Part A, and features on existing code handed over by xstack:onboard.

### B1. Lock the plan
Read the feature's `plan.md`. Make sure it has: goal, who it is for, what it does, done criteria, and a checklist
of small steps. Run xstack:map-the-flow (planned or traced) and xstack:data-view if the feature touches data.
Show the plan as a card. When the user approves, mark it `locked` with the date.

### B2. Choose the build mode
Ask with AskUserQuestion:
- **Co-op**: you and Claude split the coding. Claude hands you pieces through leaf tasks.
- **Captain**: Claude writes the code, you own architecture and design. Claude checks in before and after each chunk.
Save the choice in `plan.md` under "Build mode" with the date. The user can switch anytime (see xstack:leaf-task Step 1).
Create the branch `feat/<feature-slug>`.

### B3a. Co-op loop
For each checklist item, decide who takes it (suggest based on competency and leaf size, the user confirms).
- User's pieces: xstack:leaf-task.
- Claude's pieces: write them, then a short card: **What I wrote / How it connects / One question**.

### B3b. Captain loop
Before each chunk, a checkpoint card (about 10 lines max):
```
Decision: validation in the API, not the frontend
Why:
- frontend checks can be bypassed
- one place to update the rules
Calls: POST /api/cards → validateCard() → insertCard()
[Form] --POST--> [API: validate] --ok--> [DB: cards]
                       |
                   400 error --> [Form shows message]
Approve or redirect?
```
(Use real bold labels in the card; the example is in a code block only to show layout.)
Wait for approve or redirect. Then write the chunk.
After each chunk: **Here's how it works** (2 to 4 bullets) plus **one question** to check understanding.
If the user answers well in an area, add to that area's explains tally.
Bugs still go through xstack:error-detective with the user, even though Claude writes the fix if asked.

### B4. Commit and pull request
- Small commits on the feature branch, clear messages, no AI attribution of any kind.
- When the checklist is done, ask the user before pushing. Push the feature branch (never main).
- Open a pull request (with `gh pr create` if available) with a short summary and a test plan. No AI attribution, no generated-by footer, no session links.

### B5. Finish
Handled by xstack:map-the-flow Step 7 (checklist complete, the user confirms, system map auto-updates).
Then offer xstack:explain-it-back once, and update `progress.md` with the next feature.
