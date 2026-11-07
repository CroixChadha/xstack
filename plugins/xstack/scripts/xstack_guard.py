#!/usr/bin/env python3
"""xstack guard: a PreToolUse hook for Claude Code.

What it does, in order of strictness:

DENY (always blocked, no approval option)
  - Any command or file access that touches a production env file (default: .env.production, .env.prod)
  - Any command or MCP call that mentions a production host from .xstack/protected.json
  - git push to a protected branch (default: main, master), including a bare push while on main
  - Commits or pull requests that contain AI attribution (Co-Authored-By Claude, generated-by footers, session links)

ASK (Claude Code shows YOU an approval prompt; Claude cannot approve for you)
  - Destructive SQL: DROP, TRUNCATE, DELETE FROM, UPDATE ... SET, ALTER TABLE ... DROP
  - Migration and database tooling: prisma migrate, alembic upgrade, manage.py migrate, rails db:, and more
  - Force pushes to any branch

Everything else: no output, so Claude Code's normal permission rules apply unchanged.
This script never returns "allow", because "allow" would skip your normal permission prompts.

Production hosts are hostnames only. Never put passwords in .xstack/protected.json.
"""

import fnmatch
import json
import os
import re
import shlex
import subprocess
import sys

DEFAULT_CONFIG = {
    "prod_hosts": [],
    "prod_env_files": [".env.production", ".env.prod", ".env.production.local"],
    "protected_branches": ["main", "master"],
}

DESTRUCTIVE_SQL = [
    (r"\bdrop\s+(table|database|schema|index|view|column|collection)\b", "DROP"),
    (r"\btruncate\b", "TRUNCATE"),
    (r"\bdelete\s+from\b", "DELETE FROM"),
    (r"\bupdate\s+[\w.\"`\[\]]+\s+set\b", "UPDATE ... SET"),
    (r"\balter\s+table\b[^;]*\bdrop\b", "ALTER TABLE ... DROP"),
    (r"\bdropdatabase\s*\(", "dropDatabase()"),
    (r"\bflushall\b|\bflushdb\b", "Redis FLUSH"),
]

DB_TOOLING = [
    (r"\bprisma\s+(migrate|db\s+push|db\s+execute)\b", "prisma migrate/db push"),
    (r"\balembic\s+(upgrade|downgrade|stamp)\b", "alembic upgrade/downgrade"),
    (r"\bflask\s+db\s+(upgrade|downgrade|stamp)\b", "flask db upgrade/downgrade"),
    (r"\bmanage\.py\s+(migrate|flush|sqlflush|loaddata)\b", "django migrate/flush"),
    (r"\b(rails|rake)\s+db:", "rails db:"),
    (r"\bknex\s+migrate:", "knex migrate"),
    (r"\bsequelize(-cli)?\s+db:", "sequelize db:"),
    (r"\bdrizzle-kit\s+(push|migrate|drop)\b", "drizzle-kit push/migrate"),
    (r"\bsupabase\s+db\s+(reset|push)\b", "supabase db reset/push"),
    (r"\btypeorm\b.*\bmigration:(run|revert)\b", "typeorm migration"),
    (r"\b(dropdb|createdb)\b", "dropdb/createdb"),
    (r"\bmongosh?\b.*\b(drop|deletemany|remove)\b", "mongo drop/delete"),
]

ATTRIBUTION = [
    r"co-authored-by:[^\n]*(claude|anthropic)",
    r"noreply@anthropic\.com",
    r"generated\s+with\s+\[?claude",
    r"claude\.ai/code/session",
    r"claude-session:",
]


def emit(decision, reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def load_config(project_dir):
    config = {k: list(v) for k, v in DEFAULT_CONFIG.items()}
    path = os.path.join(project_dir, ".xstack", "protected.json")
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            user = json.load(f)
        for key in DEFAULT_CONFIG:
            if isinstance(user.get(key), list):
                config[key] = [str(x).strip() for x in user[key] if str(x).strip()]
    # Ignore very short host entries so "db" or "pg" cannot block everything by accident.
    config["prod_hosts"] = [h for h in config["prod_hosts"] if len(h) >= 4]
    return config


def basename(path):
    return re.split(r"[\\/]", path.rstrip("\\/"))[-1]


def matches_prod_env(name, config):
    base = basename(name)
    return any(fnmatch.fnmatch(base, pattern) for pattern in config["prod_env_files"])


def mentions_prod_env(text, config):
    for token in re.split(r"[\s'\"=<>|;&()]+", text):
        if token and matches_prod_env(token, config):
            return token
    return None


def mentions_prod_host(text, config):
    low = text.lower()
    for host in config["prod_hosts"]:
        if host.lower() in low:
            return host
    return None


def first_match(patterns, text):
    for pattern, label in patterns:
        if re.search(pattern, text, re.IGNORECASE | re.DOTALL):
            return label
    return None


def current_branch(cwd):
    try:
        out = subprocess.run(
            ["git", "-C", cwd, "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, timeout=3,
        )
        return out.stdout.strip() if out.returncode == 0 else None
    except Exception:
        return None


def split_commands(command):
    """Split a shell line on ; && || | and newlines so each git call is checked on its own."""
    return [c.strip() for c in re.split(r";|&&|\|\||\||\n", command) if c.strip()]


def check_git_push(segment, cwd, config):
    """Return ("deny"|"ask", reason) for a single git push segment, or None."""
    try:
        tokens = shlex.split(segment, posix=True)
    except ValueError:
        tokens = segment.split()
    if "git" not in tokens or "push" not in tokens:
        return None
    if tokens.index("push") < tokens.index("git"):
        return None
    args = tokens[tokens.index("push") + 1:]
    protected = [b.lower() for b in config["protected_branches"]]

    if any(a in ("--all", "--mirror") for a in args):
        return ("deny", "xstack: pushing all branches can push to a protected branch. Push your feature branch by name instead.")

    positional = [a for a in args if not a.startswith("-")]
    refspecs = positional[1:]
    for ref in refspecs:
        target = ref.split(":")[-1].lstrip("+")
        target = target.replace("refs/heads/", "").lower()
        if target in protected:
            return ("deny", f"xstack: never push to '{target}'. Push a feature branch and open a pull request.")

    if not refspecs:
        branch = current_branch(cwd)
        if branch and branch.lower() in protected:
            return ("deny", f"xstack: you are on '{branch}', so this push would update it. Create a feature branch first.")

    forced = any(a in ("-f", "--force") or a.startswith("--force-with-lease") or a.startswith("--force-if-includes")
                 for a in args) or any(r.startswith("+") for r in refspecs)
    if forced:
        return ("ask", "xstack: this is a force push, which rewrites history on the remote. Approve only if you meant it.")
    return None


def check_attribution(command):
    low = command.lower()
    is_commit_or_pr = re.search(r"\bgit\s+(commit|tag|notes)\b", low) or re.search(r"\bgh\s+pr\s+(create|edit|merge)\b", low)
    if not is_commit_or_pr:
        return None
    for pattern in ATTRIBUTION:
        if re.search(pattern, low):
            return "xstack: remove the AI attribution line (Co-Authored-By, generated-by footer, or session link) and try again."
    return None


def check_bash(command, cwd, config):
    # 1. Production env files: hard block. Editing .gitignore to ignore them is fine.
    if "gitignore" not in command.lower():
        hit = mentions_prod_env(command, config)
        if hit:
            emit("deny", f"xstack: '{hit}' is a production env file. Claude never reads or uses it. Run that yourself.")

    # 2. Production hosts: hard block.
    host = mentions_prod_host(command, config)
    if host:
        emit("deny", f"xstack: this command mentions production host '{host}'. Production is off limits. Run it yourself if needed.")

    # 3. AI attribution in commits and PRs: hard block.
    reason = check_attribution(command)
    if reason:
        emit("deny", reason)

    # 4. git push rules.
    ask_reason = None
    for segment in split_commands(command):
        result = check_git_push(segment, cwd, config)
        if result and result[0] == "deny":
            emit("deny", result[1])
        if result and result[0] == "ask":
            ask_reason = result[1]

    # 5. Destructive SQL and database tooling: you approve.
    label = first_match(DESTRUCTIVE_SQL, command)
    if label:
        emit("ask", f"xstack: destructive database command ({label}). Approve only if this is the test environment and you meant it.")
    label = first_match(DB_TOOLING, command)
    if label:
        emit("ask", f"xstack: this runs database tooling ({label}), which can change a schema or data. Approve only for the test environment.")

    if ask_reason:
        emit("ask", ask_reason)


def check_file_tool(tool_input, config):
    for key in ("file_path", "path", "notebook_path"):
        value = tool_input.get(key)
        if isinstance(value, str) and value and matches_prod_env(value, config):
            emit("deny", f"xstack: '{basename(value)}' is a production env file. Claude never reads or edits it.")
    pattern = tool_input.get("glob") or ""
    if isinstance(pattern, str) and pattern and matches_prod_env(pattern, config):
        emit("deny", "xstack: that search targets a production env file. Claude never reads it.")


def check_mcp(tool_input, config):
    text = json.dumps(tool_input)
    host = mentions_prod_host(text, config)
    if host:
        emit("deny", f"xstack: this tool call mentions production host '{host}'. Production is off limits.")
    label = first_match(DESTRUCTIVE_SQL, text)
    if label:
        emit("ask", f"xstack: this tool call contains a destructive database statement ({label}). Approve only if you meant it.")


def main():
    raw = sys.stdin.read()
    if not raw.strip():
        sys.exit(0)
    data = json.loads(raw)
    tool = data.get("tool_name", "")
    tool_input = data.get("tool_input") or {}
    cwd = data.get("cwd") or os.getcwd()
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR") or cwd
    config = load_config(project_dir)

    if tool == "Bash":
        check_bash(str(tool_input.get("command", "")), cwd, config)
    elif tool in ("Read", "Edit", "Write", "MultiEdit", "Grep", "Glob", "NotebookEdit"):
        check_file_tool(tool_input, config)
    elif tool.startswith("mcp__"):
        check_mcp(tool_input, config)
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:  # Fail safe: never silently allow when the guard breaks.
        emit("ask", f"xstack guard hit an error ({type(exc).__name__}: {exc}). Approve only if you are sure this is safe.")
