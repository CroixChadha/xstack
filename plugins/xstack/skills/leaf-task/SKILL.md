---
name: leaf-task
description: Hand the user one small, self-contained piece of code to write themselves, with a map of what connects to it, a spec file, tagged TODO comments in the code, light hints, and an analogous example they must adapt, then review their code against the spec. Use when the user runs /xstack:leaf-task, says "let me write this part" or "I'll handle X", in Co-op mode whenever a piece is assigned to the user, and whenever the user takes over a piece in Captain mode.
---

# xstack:leaf-task

First read `${CLAUDE_PLUGIN_ROOT}/RULES.md`. If `docs/xstack/onboarding.md` is missing, run xstack:onboard first.

## Step 1: Context
Read `onboarding.md`, the current feature's `plan.md`, and `flow-map.md`.
If the user is taking over mid-feature in Captain mode, ask with AskUserQuestion:
- **Just this part**, then hand it back
- **This part plus specific others** (ask which)
- **Everything from here on** (switch the feature to Co-op)
Record the switch in `plan.md` under "Mode history" with the date.

## Step 2: One batched prompt
Ask all of these in a single AskUserQuestion call:
1. **Scaffolding:** Comments only (default) / Skeleton (Claude writes function names, signatures, and variable names; you write the logic)
2. **Tests:** You write them / Claude writes them / No tests for this one
3. **Flow:** You explain the map / Claude explains it

## Step 3: Map
Run xstack:map-the-flow for this piece (it skips its own "who explains" question, you already asked).
Mark the user's piece with the `you` class instead of `leaf` (and `(YOU)` in the chat line).

## Step 4: Write the spec file
Create `docs/xstack/features/<feature>/leaf-tasks/<task-slug>.md` from `${CLAUDE_PLUGIN_ROOT}/templates/leaf-task.md`:
- **Choices:** the three answers from Step 2 (so review knows what Claude gave vs what the user built)
- **Goal:** one line
- **Where:** file, function name first, approximate lines second (`api.py`, `create_card()`, around lines 52 to 80).
  Why: line numbers drift as code changes, function names do not.
- **Map:** a tiny Mermaid map (max 5 nodes): what calls in, the `you` node, what it calls out
- **Inputs / outputs:** types and examples
- **Spec checklist:** what "done" means, as checkboxes
- **Hints:** 2 to 4 light nudges. Never the answer.
- **Similar example:** the same concept in a different context, so it cannot be pasted in.
  Example: if the task is try/except around the PSA API call, show try/except around a weather API fetch,
  with different names and a different error type. The user must translate the pattern.
  Why: translating a pattern into your own code is the actual learning step.
- **Tests:** what was chosen, and test cases if Claude is writing them

Keep the whole file about one screen.

## Step 5: Put TODOs in the code
At the exact spot the user will work, add tagged comments in the file's comment syntax:
```python
# TODO(xstack): wrap the PSA call in try/except
# TODO(xstack): return a 502 with a clear message on failure
```
If they chose Skeleton, also add the function signature and variable names, with the body left as TODOs.
Do not write any logic. Tell the user in a card where to go, then stop and let them work.

## Step 6: Review when they say they're done
- Read their code and compare it to the spec checklist, not to how Claude would have written it.
- Review card: **Works:** / **Spec gaps:** / **One thing to improve:**
- Run tests if any exist. If the user wrote tests, review those too.
- Do not rewrite their code. Point at the line and explain. If they ask Claude to fix something, it becomes a small change, explained.
- When it passes: check off the spec, remove that task's `TODO(xstack)` comments, mark the leaf task `done`,
  and check the matching item in `plan.md` if there is one.

## Step 7: Explain tally
If the user explained the map in Step 2 and nailed it, add one to the `explains` tally for that area in
`onboarding.md` (see xstack:explain-it-back for the format).
