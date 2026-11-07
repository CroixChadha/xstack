# Flow map: <feature>

- **Type:** traced | planned
- **Built:** YYYY-MM-DD at commit <short sha | no-repo>
- **Path:** File.tsx → x.py: create_x() → db.py: insert_x() (leaf) → x table

Preview with Ctrl+Shift+V (Cmd+Shift+V on Mac). Max 8 nodes; if bigger, use an Overview map and a Zoom map.

```mermaid
flowchart LR
  form["File.tsx"] -->|POST /api/x| create["x.py: create_x()"]
  create --> insert["db.py: insert_x()"]
  insert --> xs[("x table")]
  class insert leaf

  classDef leaf fill:#e6f4ea,stroke:#2e7d32,color:#111
  classDef you fill:#e3f2fd,stroke:#1565c0,stroke-width:3px,color:#111
  classDef err fill:#fdecea,stroke:#c62828,stroke-width:2px,color:#111
  classDef cause fill:#fff4e5,stroke:#ef6c00,stroke-width:2px,stroke-dasharray:4,color:#111
  classDef planned stroke-dasharray:5
```

## Leaf pieces
- `file: function()`: inputs -> output
