---
name: data-view
description: Show the data side of a project. For databases, an ASCII view of the tables a feature touches with keys and relationships; for projects without a database, the shape of the objects and payloads as they move (JSON, localStorage, API requests and responses). Reads the saved Mermaid data map instead of re-scanning, and coaches schema changes (user designs first or Claude proposes, always asks). Never connects to a live database. Use when the user runs /xstack:data-view, asks what the data looks like, during feature planning when a feature touches data, and in xstack:leaf-task when the piece is a query.
---

# xstack:data-view

First read `${CLAUDE_PLUGIN_ROOT}/RULES.md`. If `docs/xstack/onboarding.md` is missing, run xstack:onboard first.

## Safety first
- Read schema files, ORM models, migrations, type definitions, and fixtures only.
- **Never connect to a live database** to inspect it, not even test. Never read `.env*` files to find connection strings.
Why: the map comes from code, so there is no way for viewing data to hurt data.

## Step 1: Read the saved map
Read `docs/xstack/data-map.md` (built by the data-mapper agent) and `discovery/data.md`.
If neither exists, read the schema sources directly in the main session for just the part needed.
Do not launch agents from this skill.

## Step 2: Database projects, feature view
Show only the tables the feature touches. Keys and relationships only, no other columns:
```
[boards] 1 ───< [cards] >─── 1 [users]
 id PK           id PK           id PK
                 board_id FK
                 user_id FK
```
For beginner areas, add one plain line per relationship under the map: "one board has many cards."

## Step 3: No database, data shapes
Show what the data looks like as it moves, not what functions do (that is the flow map's job):
```
card = { id, title, boardId, dueDate }
  saved to: localStorage["cards"]
  sent to:  POST /api/cards
  returns:  { ok, card }
```
Cover: objects passed between files, JSON payloads, API requests and responses, browser storage, files on disk.
Why: flow maps answer "what happens", data views answer "what is being passed". Mixing them makes both messy.

## Step 4: Schema or shape changes (always ask)
When a feature needs a new table, column, or field, ask with AskUserQuestion:
**"Want to try designing it first, or should Claude propose one?"**
- **User designs:** they write the table or shape. Review card: **Works:** / **Watch out:** / **One improvement:**,
  explaining concepts at their level (what a primary key is for, why a foreign key goes on the "many" side, nullable vs required).
- **Claude proposes:** show the ASCII view of the change plus a one-line why for each decision.
Then write a migration file (or the shape change in code). **Never run migrations.** Tell the user the exact command to run themselves.

## Step 5: Save
Add or update the feature's data view in `docs/xstack/features/<feature>/discovery.md` under a `## Data` heading.
When the feature is marked finished, xstack:map-the-flow updates `data-map.md`.
