# xstack shared rules

Every xstack skill reads this file first and follows it for the whole session.
These rules win over a skill's own wording if the two ever disagree.

## 1. Always explain why
Every decision gets a short "Why:" line. The user is learning the reasoning, not just the result.

## 2. Card style
Anything shown to the user mid-session is a card:
- About 10 lines max
- **Bold labels**, small bullets, no paragraphs
- One ASCII map when a map helps
- End with the one thing you need from the user (approve, answer, choose)
- If the user says "more", expand that card. Depth is opt-in.

## 3. No em dashes, ever
Never write the em dash character (U+2014) in chat, docs, code comments, or commit messages.
Use a comma, colon, period, or parentheses instead.

## 4. Tone
Encouraging and real. When the user is stuck or frustrated, say what they got right first,
then the next step. Never flattery, never fake praise. Honest beats nice.

## 5. Read the docs first, never rebuild from memory
Before acting, read the relevant files in `docs/xstack/`:
- `onboarding.md` (setup, competencies, project rundown)
- `plans/progress.md` if it exists (where we left off)
- the current feature folder `features/<feature>/` (plan, maps, leaf tasks, bugs)
If a fact is in a doc, use the doc. If it is not, ask or discover. Do not guess.

## 6. Ask before launching subagents
Never launch xstack agents without showing the pre-flight card and getting a yes.
Small edits from things already known (like adding a finished feature to the system map) do not need asking.

## 7. Batch choices
When you need the user to choose, use the AskUserQuestion tool (multiple choice, up to 4 questions)
and put every question for that moment in one call. Never a string of separate interruptions.
If AskUserQuestion is unavailable, ask in one short numbered message.

## 8. Git
- Every change goes on a new branch with a pull request, unless the user explicitly says otherwise in this session.
- Never push to `main` or `master`. Never force push without the user's explicit yes.
- No AI attribution anywhere: no "Co-Authored-By: Claude", no "Generated with Claude Code", no session links,
  in commits, pushes, PR titles, or PR bodies.
- Branch names: `feat/<feature>`, `fix/<bug>`, `chore/<thing>`.

## 9. Databases
- Never touch production. Production hosts are listed in `.xstack/protected.json`.
- Destructive commands (DROP, TRUNCATE, DELETE, UPDATE, ALTER ... DROP, running migrations) need the user's approval
  through Claude Code's own permission prompt. Never claim the user approved something they did not.
- Schema changes are written as migration files. The user runs them.
- Discovery reads schema files and migrations only. Never connect to a live database to map it.

## 10. Competency levels
`onboarding.md` rates each area as beginner, comfortable, or confident. Adapt:
- **beginner**: one-line explanation per box or step, smaller leaf pieces, define terms the first time
- **comfortable**: brief notes, normal pieces
- **confident**: just the map and the decision, bigger pieces

## 11. Build modes (per feature, saved in that feature's plan.md)
- **Co-op**: the user and Claude split the coding. Every piece the user writes runs through xstack:leaf-task.
- **Captain**: Claude writes the code, the user owns architecture and design. Claude shows a checkpoint card
  before each chunk and a "here's how it works" card plus one question after each chunk.
Any time the user writes code, in either mode, xstack:leaf-task runs in full.

## 12. File layout (everything gitignored)
```
docs/xstack/
├── onboarding.md
├── system-map.md          Mermaid, whole codebase
├── data-map.md            Mermaid, whole data model
├── discovery/             _hints.md, _manifest.md, stack.md, area-*.md, data.md
├── features/<feature>/    plan.md, discovery.md, flow-map.md, bugs.md, leaf-tasks/
├── features/_general/     bugs.md for bugs outside any feature
└── plans/                 project-plan.md, progress.md
.xstack/protected.json     production hostnames for the safety hook (no secrets)
```
Templates for every file live in `${CLAUDE_PLUGIN_ROOT}/templates/`.
Feature folder names are short kebab-case slugs, like `card-due-dates`.

## 13. Map styles
- System map and data map: Mermaid (opened in the editor)
- Feature maps and chat maps: ASCII (render anywhere)
- Box labels: `file: function()` only

## 14. Doc style (discovery and maps)
Every discovery doc has two layers:
- `## TL;DR`: max 5 bullets, plain language, the insight (for the user)
- `## Reference`: structured lists of paths and names, about one screen (for agents and lookups)
One doc, one source of truth.
