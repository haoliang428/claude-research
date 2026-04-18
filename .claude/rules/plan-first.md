# Rule: Plan Before Implementing

## When This Applies

- Multi-file edits (touching 3+ files)
- New features or significant additions
- Unclear or ambiguous scope
- Refactoring existing code or structure

## When to Skip

- Single-file fixes (typos, one-line bugs)
- Running existing skills (`/proofread`, `/bib-validate`, etc.)
- Informational questions
- Updating context files
- User says "quick", "try this", "just do it"

## Assumption Check (Medium Tasks)

For 1-2 file tasks with ambiguous how: state in 2-4 lines what you'll do and which files you'll touch, then wait for confirmation. Skip if the user's instruction is fully explicit.

## Protocol (Large Tasks)

1. Draft a plan before writing code
2. Save to `log/plans/YYYY-MM-DD_description.md`
3. Get approval, then implement

Plan format:
```markdown
# Plan: [Short Description]
## Context — why this is needed
## Changes — files to create/modify
## Order of Operations — implementation steps
## Risks / Open Questions
```

For plans spanning 2+ distinct activities (code + experiments + writing), split into phases with stop points. Do not start the next phase without the user's go-ahead.

## Execution Stall Detector

- **2-message rule:** If 2 messages pass after a plan is confirmed with no file edited, start implementing immediately.
- **No re-planning approved plans.** Start from step 1 and make changes.
- **File-edit-first:** Make the first file change in your next response.

## Session Recovery

On new session: read `log/plans/` (latest), then `.context/current-focus.md`.
