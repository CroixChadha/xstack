---
name: explain-it-back
description: Check the user's understanding of code. Two modes, explain (the user explains a function in their own words) and predict (the user predicts what code will output before it runs). Prioritizes code Claude wrote in Captain mode, grades with a short card, keeps a tally in onboarding.md, and suggests competency bumps. Use when the user runs /xstack:explain-it-back, says "quiz me" or "let me predict this", and offered at the end of a finished feature.
---

# xstack:explain-it-back

First read `${CLAUDE_PLUGIN_ROOT}/RULES.md`. If `docs/xstack/onboarding.md` is missing, run xstack:onboard first.

## Step 1: Mode
If the user did not say, ask with AskUserQuestion: **Explain this** / **Predict the output**.

## Step 2: Pick the code
If the user named a file or function, use it. Otherwise pick, in this order:
1. Code Claude wrote in Captain mode for the current feature (check `plan.md` mode history and recent commits)
2. Boxes on the current `flow-map.md` the user has not written
3. Something in an area rated beginner in `onboarding.md`
Why: the code you understand least is what you will get stuck on if a model runs out of context later.

Point to it by file and function name. Do not paste it. The user opens the file themselves.

## Mode A: Explain this
Ask the user to explain:
- What it does
- What goes in and what comes out
- What calls it
Reply with a card:
- **Got it:** what they nailed
- **Gaps:** what they missed
- **One-line fix:** the correction

## Mode B: Predict the output
Pick a small, runnable thing: a function call with specific inputs, a test, a script, an API call against test data.
Never anything that touches production or changes data.
1. Show the exact input or command
2. User predicts the output (and ideally why)
3. Run it and show the real output
4. Card: **Predicted / Actual / Why they differ** (or "Spot on" with one line of why)
Why: wrong guesses are where the learning sticks.

## Step 3: Tally (the only thing saved)
Results live in the chat. The only write is a one-line tally per area in the competency table of `onboarding.md`:
```
Backend/API | comfortable | explains: 3 solid, 1 partial
```
Count Mode A and Mode B together. "Solid" means no real gaps.

## Step 4: Suggest a bump
After 4 solid results in one area since its last rating change, suggest one level up with one line of why:
"You've nailed 4 API explanations. Move backend/API to confident?" The user decides.
On yes: update the level, add a dated history line, reset that area's tally.

## End of feature
When xstack:map-the-flow marks a feature finished, offer once: "Want to explain a couple of pieces before we close it out?"
