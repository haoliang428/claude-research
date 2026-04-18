#!/bin/bash
CWD="$(pwd)"
CONTEXT=""
MAX_LINES=30
WORKSPACE="$HOME/Desktop/claude-research"

add_section() {
  local title="$1" file="$2" lines="${3:-$MAX_LINES}"
  if [ -f "$file" ]; then
    local content=$(head -"$lines" "$file")
    if [ -n "$content" ]; then
      [ -n "$CONTEXT" ] && CONTEXT="$CONTEXT\n\n"
      CONTEXT="${CONTEXT}## ${title}\n${content}"
    fi
  fi
}

add_section "Current Focus" "$WORKSPACE/.context/current-focus.md" 25
add_section "Project Index" "$WORKSPACE/.context/projects/_index.md" 40

PROJECT_ROOT=""
[ "$CWD" != "$WORKSPACE" ] && PROJECT_ROOT=$(git -C "$CWD" rev-parse --show-toplevel 2>/dev/null || echo "$CWD")

if [ "$CWD" = "$WORKSPACE" ]; then
  add_section "MEMORY.md" "$WORKSPACE/MEMORY.md" 30
elif [ -n "$PROJECT_ROOT" ]; then
  add_section "Project MEMORY" "$PROJECT_ROOT/MEMORY.md" 30
fi

if [ -n "$PROJECT_ROOT" ] && [ "$PROJECT_ROOT" != "$WORKSPACE" ]; then
  add_section "Project Progress" "$PROJECT_ROOT/.context/progress.md" 30
  add_section "Project Focus" "$PROJECT_ROOT/.context/current-focus.md" 25
fi

for DIR in "$PROJECT_ROOT/log/plans" "$WORKSPACE/log/plans"; do
  if [ -d "$DIR" ]; then
    LATEST=$(find "$DIR" -maxdepth 1 -name "*.md" -type f 2>/dev/null | sort -r | head -1)
    [ -n "$LATEST" ] && add_section "Latest Plan ($(basename "$LATEST"))" "$LATEST" 25 && break
  fi
done

[ -z "$CONTEXT" ] && exit 0
CONTEXT="# Session Context (auto-loaded)\n\n${CONTEXT}"
echo -e "$CONTEXT" | jq -Rs '{hookSpecificOutput:{hookEventName:"SessionStart",additionalContext:.}}'
exit 0
