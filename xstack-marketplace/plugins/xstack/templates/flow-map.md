# Flow map: <feature>

- **Type:** traced | planned
- **Built:** YYYY-MM-DD at commit <short sha | no-repo>

```
[File.tsx] --POST /api/x--> [x.py: create_x()]
                                  |
                            [db.py: insert_x()]  <- leaf
```

## Leaf pieces
- `file: function()`: inputs -> output
