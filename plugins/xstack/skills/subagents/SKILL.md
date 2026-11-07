---
name: subagents
description: Map an entire existing codebase with read-only xstack agents (scout, area mappers, data mapper, synthesizer, path checker, flow reviewer) using a fixed model and effort routing table, always after a pre-flight card and the user's yes. Writes short two-layer discovery docs, a Mermaid system map, and a Mermaid data map. Also handles refreshes of only the changed areas. Use when the user runs /xstack:subagents or says "remap", when xstack:onboard offers mapping on an existing repo, or when a skill finds the maps are stale.
---

# xstack:subagents

First read `${CLAUDE_PLUGIN_ROOT}/RULES.md`.

## Routing table
| Role | Agent | Model | Effort | Job |
|---|---|---|---|---|
| Scout | `scout` | Haiku | low | Inventory: files, frameworks, entry points |
| Area mappers (max 4) | `area-mapper` | Sonnet | medium | Map each area's flow |
| Data mapper | `data-mapper` | Sonnet | medium | Tables and relationships, or data shapes |
| Synthesizer | `synthesizer` | Opus | medium | Merge into one system map, flag leaf pieces |
| Path checker | `path-checker` | Haiku | low | Confirm every file in the maps exists |
| Flow reviewer | `flow-reviewer` | Sonnet | medium | Spot check arrows by finding real call sites |

Model and effort are set in each agent's frontmatter. When calling the Agent tool, use the plugin's namespaced
agent type (for example `xstack:scout`). If that is not found, try the plain name (`scout`).
All six agents are read-only (Read, Grep, Glob). **Only the main session writes files.**
Why read-only: mappers can never accidentally edit your code.

## When not to use this
- No git repo: map in the main session instead.
- A single feature: feature-discovery runs in the main session (see the end of this file), no subagents.

## Step 1: Full map or refresh?
- If `docs/xstack/discovery/_manifest.md` does not exist: **full map**.
- If it exists: run `git diff --name-only <manifest commit>..HEAD`, match changed files to areas in the manifest.
  Nothing changed: say so and stop. Otherwise: **refresh** of only the changed areas (plus data mapper if schema files changed).

## Step 2: Pre-flight card (always, then wait)
```
xstack mapping pre-flight
Type:    full map | refresh (areas: api, data)
Areas:   frontend, api, logic, data
Agents:  scout (Haiku) → 3 area mappers (Sonnet) + data mapper (Sonnet)
         → synthesizer (Opus) → path checker (Haiku) → flow reviewer (Sonnet)
Writes:  docs/xstack/discovery/*, system-map.md, data-map.md
```
Ask with AskUserQuestion: **Go** / **Cancel** / **Fewer areas** (merge areas to launch fewer agents).
Nothing launches without **Go**.
Why: subagents start cold and cost real usage, so you see exactly what runs before it runs.

For a full map, the area list is a draft from `_hints.md` and the top-level folders; say it is a draft. The scout confirms it.

## Step 3: Scout
Launch `scout` with: the project root, the contents of `docs/xstack/discovery/_hints.md`, and a request for
the stack (confirmed or corrected hints), entry points, top-level layout, and a proposed split into at most 4 areas
plus the data sources. Write the result to `discovery/stack.md` (two-layer format, see RULES.md section 14).

## Step 4: Areas and data, in parallel
From the scout's split, decide the areas. **Max 4 area mappers.** Group small areas together.
Launch in a single message, in parallel:
- one `area-mapper` per area, each given: the area name, its folders and files, the stack summary, and the entry points in that area
- one `data-mapper`, given: schema, model, migration, and type file locations from the scout
Write each result to `discovery/area-<name>.md` and `discovery/data.md`.

## Step 5: Synthesize
Launch `synthesizer` with the text of `stack.md`, every `area-*.md`, and `data.md`.
It returns: a Mermaid system map, a Mermaid data map, the cross-area connections, and a leaf piece list.

## Step 6: Check, in order
1. Launch `path-checker` with every file path and function name in the synthesizer's output.
2. Fix any missing paths in the main session.
3. Then launch `flow-reviewer` with the corrected maps (it did not build them, which is the point).
Why this order: there is no point reviewing arrows that point at files that do not exist.

## Step 7: Write the docs
Main session writes, using templates in `${CLAUDE_PLUGIN_ROOT}/templates/`:
- `docs/xstack/system-map.md` and `docs/xstack/data-map.md`
- a `## Corrections` section listing anything the checkers fixed (so the user sees what was wrong)
- `docs/xstack/discovery/_manifest.md`: commit (`git rev-parse --short HEAD`), date, areas with their folders, agents run
Every discovery doc follows the two-layer format: `## TL;DR` (max 5 bullets) and `## Reference` (about one screen).

## Step 8: Summary card
- **Stack:** one line
- **Areas:** list
- **Corrections:** count
- **Open:** "Open docs/xstack/system-map.md in your editor to see the full map."

## Feature-discovery (main session, no agents)
For a single feature, the main session reads only what the feature touches, using the existing discovery docs
as a guide, and writes `docs/xstack/features/<feature>/discovery.md` in the two-layer format.
