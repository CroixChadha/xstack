#!/usr/bin/env python3
"""Tests for scripts/xstack_guard.py. Run: python3 tests/test_guard.py"""

import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GUARD = os.path.join(HERE, "..", "scripts", "xstack_guard.py")


def make_project(branch="feat/cards"):
    d = tempfile.mkdtemp(prefix="xstack-test-")
    os.makedirs(os.path.join(d, ".xstack"))
    with open(os.path.join(d, ".xstack", "protected.json"), "w") as f:
        json.dump({"prod_hosts": ["prod-db.boardlane.example.com"]}, f)
    subprocess.run(["git", "init", "-q", "-b", "main", d], check=True)
    subprocess.run(["git", "-C", d, "-c", "user.email=t@t", "-c", "user.name=t",
                    "commit", "-q", "--allow-empty", "-m", "init"], check=True)
    if branch != "main":
        subprocess.run(["git", "-C", d, "checkout", "-q", "-b", branch], check=True)
    return d


def run(project, tool, tool_input):
    payload = json.dumps({"tool_name": tool, "tool_input": tool_input, "cwd": project})
    env = dict(os.environ, CLAUDE_PROJECT_DIR=project)
    out = subprocess.run([sys.executable, GUARD], input=payload, capture_output=True, text=True, env=env)
    assert out.returncode == 0, f"guard exited {out.returncode}: {out.stderr}"
    if not out.stdout.strip():
        return "pass"
    return json.loads(out.stdout)["hookSpecificOutput"]["permissionDecision"]


feature = make_project("feat/cards")
on_main = make_project("main")

CASES = [
    # (project, tool, input, expected, label)
    (feature, "Bash", {"command": "ls -la"}, "pass", "harmless command"),
    (feature, "Bash", {"command": "cat .env"}, "pass", "dev .env is fine"),
    (feature, "Bash", {"command": "cat .env.production"}, "deny", "read prod env file"),
    (feature, "Bash", {"command": "source config/.env.prod && npm start"}, "deny", "source prod env file"),
    (feature, "Bash", {"command": "echo '.env.production' >> .gitignore"}, "pass", "ignoring prod env is fine"),
    (feature, "Read", {"file_path": "/repo/.env.production"}, "deny", "Read tool on prod env"),
    (feature, "Read", {"file_path": "C:\\repo\\.env.production"}, "deny", "Windows path to prod env"),
    (feature, "Read", {"file_path": "/repo/.env"}, "pass", "Read dev .env"),
    (feature, "Bash", {"command": "psql -h prod-db.boardlane.example.com -c 'select 1'"}, "deny", "prod host"),
    (feature, "Bash", {"command": "psql -h localhost -c 'DROP TABLE cards'"}, "ask", "drop table in test"),
    (feature, "Bash", {"command": "psql -c \"delete from cards where id = 3\""}, "ask", "delete with where"),
    (feature, "Bash", {"command": "psql -c 'TRUNCATE cards'"}, "ask", "truncate"),
    (feature, "Bash", {"command": "psql -c 'update cards set title = 1'"}, "ask", "update set"),
    (feature, "Bash", {"command": "psql -c 'select * from cards'"}, "pass", "plain select"),
    (feature, "Bash", {"command": "npx prisma migrate dev"}, "ask", "prisma migrate"),
    (feature, "Bash", {"command": "python manage.py migrate"}, "ask", "django migrate"),
    (feature, "Bash", {"command": "alembic upgrade head"}, "ask", "alembic upgrade"),
    (feature, "Bash", {"command": "git push origin main"}, "deny", "push to main"),
    (feature, "Bash", {"command": "git push origin HEAD:main"}, "deny", "push HEAD to main"),
    (feature, "Bash", {"command": "git push -u origin feat/cards"}, "pass", "push feature branch"),
    (feature, "Bash", {"command": "git push"}, "pass", "bare push on feature branch"),
    (on_main, "Bash", {"command": "git push"}, "deny", "bare push while on main"),
    (feature, "Bash", {"command": "git push --all"}, "deny", "push all"),
    (feature, "Bash", {"command": "git push --force origin feat/cards"}, "ask", "force push"),
    (feature, "Bash", {"command": "git add . && git push origin master"}, "deny", "chained push to master"),
    (feature, "Bash", {"command": "git commit -m 'Add cards\n\nCo-Authored-By: Claude <noreply@anthropic.com>'"}, "deny", "co-author trailer"),
    (feature, "Bash", {"command": "gh pr create --title x --body 'Generated with [Claude Code](https://claude.com)'"}, "deny", "PR footer"),
    (feature, "Bash", {"command": "git commit -m 'Add card due dates'"}, "pass", "clean commit"),
    (feature, "mcp__client-audit-sql__query", {"sql": "DELETE FROM audits"}, "ask", "MCP destructive SQL"),
    (feature, "mcp__client-audit-sql__query", {"sql": "SELECT * FROM audits"}, "pass", "MCP select"),
    (feature, "mcp__db__query", {"host": "prod-db.boardlane.example.com", "sql": "select 1"}, "deny", "MCP prod host"),
]

failures = 0
for project, tool, tool_input, expected, label in CASES:
    got = run(project, tool, tool_input)
    ok = got == expected
    failures += not ok
    print(f"{'PASS' if ok else 'FAIL'}  {label:<34} expected {expected:<5} got {got}")

# Broken config must fail safe (ask), never silently allow.
broken = make_project("feat/x")
with open(os.path.join(broken, ".xstack", "protected.json"), "w") as f:
    f.write("{not json")
got = run(broken, "Bash", {"command": "ls"})
ok = got == "ask"
failures += not ok
print(f"{'PASS' if ok else 'FAIL'}  {'broken config fails safe':<34} expected ask   got {got}")

print(f"\n{len(CASES) + 1 - failures}/{len(CASES) + 1} passed")
sys.exit(1 if failures else 0)
