# Changelog

## 0.2.0 (2026-11-06)
- Feature, leaf, and bug maps are now small Mermaid maps (max 8 nodes, Overview plus Zoom when bigger)
  instead of ASCII. Markers are color classes: leaf, you, err, cause, planned.
- Chat shows a one-line path instead of the full map, plus where to open the preview.
- Data views and Captain checkpoint sketches stay ASCII.
- Repo: marketplace moved to the repo root and the missing `.claude-plugin` manifests restored, so installing
  from GitHub works.

## 0.1.0 (2026-11-06)
First version.
- Skills: onboard, new-project, map-the-flow, leaf-task, error-detective, explain-it-back, data-view, subagents, help
- Agents: scout, area-mapper, data-mapper, synthesizer, path-checker, flow-reviewer (read-only, routed by model and effort)
- Safety hook: blocks production hosts, production env files, pushes to main, AI attribution; asks for destructive SQL,
  migrations, and force pushes; fails safe on errors
- Shared rules in RULES.md, templates for every xstack doc, recommended settings
