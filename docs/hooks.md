# Hooks (4 active)

Configured in `~/.claude/settings.json`. Scripts live in `hooks/` (symlinked from `~/.claude/hooks/`).

| Hook | Trigger | What it does |
|------|---------|-------------|
| `startup-context-loader.sh` | Session start/resume | Auto-loads focus, project index, progress, latest plan |
| `block-destructive-git.sh` | Before Bash commands | Catches `git reset --hard`, `push --force`, `rm -rf` |
| `precompact-autosave.py` | Before context compression | Saves state snapshot to project's `log/` |
| `postcompact-restore.py` | After context compression | Restores context from snapshot |

## How Hooks Work

Hooks are shell/Python scripts that Claude Code runs automatically at specific lifecycle events. They receive JSON on stdin and can output JSON to influence behavior (e.g., inject context, block a command, or ask for confirmation).

## Adding a Hook

1. Write the script in `hooks/`
2. Add the trigger config to `~/.claude/settings.json` under `hooks.<EventName>`
3. Make it executable: `chmod +x hooks/your-hook.sh`
