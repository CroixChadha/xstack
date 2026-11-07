---
name: onboard
description: Initialize xstack in a project. Detects repo state, rates the user's competencies (beginner, comfortable, confident) with an optional mini quiz, captures the project rundown and the feature being added, then routes to codebase mapping or new-project planning. Use when the user runs /xstack:onboard, when any other xstack skill finds no docs/xstack/onboarding.md, or when the user wants to update ratings or start a new feature.
---

# xstack:onboard

First read `${CLAUDE_PLUGIN_ROOT}/RULES.md` and follow it for the whole session.

## Step 0: Show the menu
Run the xstack:help menu (the code block only, no status card) so the user sees every command.

## Step 1: Already onboarded?
If `docs/xstack/onboarding.md` exists, read it and ask with AskUserQuestion:
- **Update ratings** (re-rate and optional quiz, append to history)
- **New feature** (jump to Step 6, existing-code branch)
- **Full redo** (run everything below, keep old history)
- **Just show the menu** (stop here)

Why: you rarely need the whole thing again, so only ask what changed.

## Step 2: Detect quietly (no questions, no decisions)
Check, without asking the user anything:
- Is there a `.git` folder? (repo or no repo)
- Is there real code? (anything beyond README, license, config) (existing or new)
- Stack clues: `package.json`, `requirements.txt`, `pyproject.toml`, `Pipfile`, `go.mod`, `Cargo.toml`,
  `Gemfile`, `pom.xml`, `*.csproj`, `docker-compose.yml`, `prisma/schema.prisma`, `migrations/`,
  `tailwind.config.*`, `pytest.ini`, `vite.config.*`, `next.config.*`, and similar.

Only read file names and the top of manifest files. Do not read source code here.
Write what you noticed to `docs/xstack/discovery/_hints.md` using `${CLAUDE_PLUGIN_ROOT}/templates/hints.md`.
Every hint is marked **unverified**. The scout agent confirms them later.

Why: the scout starts where you already looked, which saves tokens. Marking hints unverified keeps the scout from blindly trusting them.

Tell the user in one line what kind of project this looks like (for example: "Existing repo with code.").
Do not announce the stack. That is the scout's job.

## Step 3: Project rundown
For an existing project, draft answers from the README first, then show them and let the user edit.
For a new project, ask directly. Three questions:
- **What is it for?**
- **Who uses it?**
- **What does "done" look like?**

## Step 4: Competencies
Areas: frontend, backend/API, databases/SQL, testing, Git, debugging, plus any stack-specific area from the hints
(for example "Next.js" or "Flask"). Ask with AskUserQuestion, options beginner / comfortable / confident.
AskUserQuestion holds 4 questions per call, so use two calls at most.

## Step 5: Mini quiz (optional)
Ask with AskUserQuestion: **Multiple choice**, **Own words**, or **Skip**.
If not skipped, ask 2 to 3 questions on the areas this project leans on most (not every area).
- Multiple choice: use AskUserQuestion with one correct answer and plausible wrong ones.
- Own words: ask an open question and judge the answer.
If answers and ratings disagree, suggest an adjustment with one line of why. The user decides.
Why: self-ratings are often off in either direction. This is calibration, not a grade.

## Step 6: The fork
**Existing code:** ask four questions:
- What are you adding?
- Who is it for?
- What will it do?
- What does "done" look like for it?
Create `docs/xstack/features/<feature-slug>/plan.md` from `${CLAUDE_PLUGIN_ROOT}/templates/plan.md`
with these answers. Leave build mode unset for now (it is chosen once the plan is locked).

Then ask: **"Want me to map the codebase with subagents now?"**
- If `docs/xstack/discovery/_manifest.md` does not exist and the user says yes, run xstack:subagents (it shows its own pre-flight card).
- If it exists, say when it was built and offer a refresh check instead.
- If no, continue. Skills will map just what they need in the main session.

Then hand off to xstack:new-project **Part B** to lock the feature plan and choose Co-op or Captain.

**Existing code, no repo:** same feature questions, but no subagents. The main session maps only what the feature touches. Then xstack:new-project Part B.

**New project (repo or not):** hand off to xstack:new-project.

## Step 7: Save
- Write `docs/xstack/onboarding.md` from `${CLAUDE_PLUGIN_ROOT}/templates/onboarding.md`.
  Competency rows include a dated history and an `explains` tally (starts at `none yet`).
- If it is a repo, make sure `.gitignore` contains both lines below. Check first and never add duplicates:
  ```
  docs/xstack/
  .xstack/
  ```
- If `.xstack/protected.json` does not exist, create it from `${CLAUDE_PLUGIN_ROOT}/templates/protected.json`
  and tell the user in one line: "Add your production hostnames to `.xstack/protected.json` (hostnames only, never passwords)."
- Write or update `docs/xstack/plans/progress.md` from `${CLAUDE_PLUGIN_ROOT}/templates/progress.md`.

## Step 8: Summary card
- **Project:** one line
- **Ratings:** compact list
- **Next:** the one command to run next, and why
