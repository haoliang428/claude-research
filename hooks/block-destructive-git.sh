#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
[ -z "$COMMAND" ] && exit 0
REASON=""
echo "$COMMAND" | grep -qE 'git\s+reset\s+--hard' && REASON="git reset --hard will discard all uncommitted changes"
echo "$COMMAND" | grep -qE 'git\s+push\s+(-f|--force)(\s|$)' && ! echo "$COMMAND" | grep -q '\-\-force-with-lease' && REASON="git push --force can overwrite remote history"
echo "$COMMAND" | grep -qE 'git\s+clean\s+-[a-zA-Z]*f' && ! echo "$COMMAND" | grep -qE 'git\s+clean\s+-[a-zA-Z]*n' && REASON="git clean -f will delete untracked files"
echo "$COMMAND" | grep -qE 'git\s+checkout\s+\.\s*$' && REASON="git checkout . will discard unstaged changes"
echo "$COMMAND" | grep -qE 'git\s+restore\s+\.\s*$' && REASON="git restore . will discard unstaged changes"
echo "$COMMAND" | grep -qE 'git\s+branch\s+-D\s' && REASON="git branch -D force-deletes a branch"
echo "$COMMAND" | grep -qE 'rm\s+-[a-zA-Z]*r[a-zA-Z]*f|rm\s+-[a-zA-Z]*f[a-zA-Z]*r' && REASON="rm -rf is destructive"
[ -z "$REASON" ] && exit 0
cat <<HOOK
{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"$REASON"}}
HOOK
exit 0
