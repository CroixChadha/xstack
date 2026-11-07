# Bugs: <feature>

## <bug-slug> (YYYY-MM-DD)
- **Symptom:** the error and what you saw
- **Bug map (as found):**
```mermaid
flowchart LR
  ui["File.tsx"] --> shown["file: fn()"]
  class shown err

  classDef err fill:#fdecea,stroke:#c62828,stroke-width:2px,color:#111
```
- **Expected / actual / repro:** (from Level 2)
- **What you tried:**
  - <attempt and what it showed>
- **Hint level reached:** 1 | 2 | 3 | 4 | answer given early (override)
- **Cause and why:**
- **Bug map (as solved):** added at Level 4, same map plus the cause class
```mermaid
flowchart LR
  ui["File.tsx"] --> shown["file: fn()"]
  shown --> origin["file: fn()"]
  class shown err
  class origin cause

  classDef err fill:#fdecea,stroke:#c62828,stroke-width:2px,color:#111
  classDef cause fill:#fff4e5,stroke:#ef6c00,stroke-width:2px,stroke-dasharray:4,color:#111
```
- **Fix:** what changed, written by you | Claude
- **Lesson:** one line
