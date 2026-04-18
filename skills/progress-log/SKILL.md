---
name: progress-log
description: "Use at the end of every session or when you need to record detailed progress. Updates the project's progress record so the next session can pick up exactly where you left off."
allowed-tools: Read, Write, Edit, Glob, Grep
argument-hint: "[no arguments — auto-detects project context]"
---

# Progress Log

Record detailed session progress so the next session (or a different person) can pick up exactly where things were left off. This replaces the old "update current focus" workflow with a more structured, detailed approach.

## When to Use

- At the end of every work session (mandatory)
- After completing a major milestone within a session
- When switching between projects mid-session
- When the user says "save progress", "record what we did", "update the log"

## Where to Write

Two files are updated:

1. **Project-level:** `<project>/.context/progress.md` — detailed progress for this specific project
2. **Workspace-level:** `claude-research/.context/current-focus.md` — which project is active and high-level status

## Project Progress Record (`progress.md`)

This is the most important file. It should contain enough detail that a fresh session can continue the work without any explanation from the user.

### Template

```markdown
# Progress Record — <Project Name>

> Last updated: YYYY-MM-DD

## Current Status

<One sentence: what state is the project in right now?>

## What Was Done This Session (YYYY-MM-DD)

### Completed
- <Specific action with file paths and outcomes>
- <e.g., "Wrote Section 3.1 (Problem Setting) in paper/paper/main.tex — 2 pages, 5 citations">
- <e.g., "Ran latency sensitivity experiments at 30/50/100ms — results in results/figures/experiment_results.json">
- <e.g., "Fixed 8 citation inaccuracies: Clover (not spatial), Bashir (operational vs lifecycle), ...">

### Key Decisions Made
- <Decision and rationale>
- <e.g., "Chose r=0.1 for DRO radius based on sensitivity analysis (not theoretical calibration — 168^{-1/6}=0.43, not 0.13)">
- <e.g., "Deprioritised IJDS (IF 2.6) in favour of Applied Energy (IF 11.0) or Energy and AI (IF 9.6)">

### Numbers and Results
- <Any quantitative results produced this session>
- <e.g., "B3 LP: +12.6%, B4 DRO: +10.2%, B5 Spatio-temporal: +12.8%">
- <e.g., "Capacity sensitivity: +1.2% at 108% → +22.3% at 210%">

## What's Left To Do

- [ ] <Specific next action with enough detail to start immediately>
- [ ] <e.g., "Choose target journal (Applied Energy vs Energy and AI) and adjust formatting">
- [ ] <e.g., "Run /pre-submission-report for final audit">
- [ ] <e.g., "Generate missing Figure 8 (deferral window sensitivity)">

## Open Questions

- <Unresolved decisions or uncertainties>
- <e.g., "Should we add a 7th DC region (SERC) to improve geographic coverage?">
- <e.g., "Demand shares are assumed, not data-backed — is this a reviewer concern?">

## File Locations

<Key files the next session will need to find>
- Paper: `paper/paper/main.tex` (23 pages, compiles cleanly)
- Experiment results: `paper/paper/figures/experiment_results.json`
- Bibliography: `references.bib` (73 entries, all verified)
- Literature notes: `docs/readings/notes/` (68 papers, 8 clusters)
```

### What Makes a Good Progress Record

**Be specific, not vague:**
- Bad: "Worked on the paper"
- Good: "Wrote Sections 3.1-3.4 (Methodology) and Section 4 (Experiments) in paper/paper/main.tex. Paper is now 15 pages with 7 figures. All experiment numbers validated against code/experiments/06-paper-experiments.py output."

**Include file paths:**
- Bad: "Fixed some citations"
- Good: "Fixed 8 citation claims in main.tex (lines 69, 83, 91, 93, 99, 103, 124, 193). Verified all 22 lit review citations against docs/readings/notes/. See reviews/paper-critic/2026-04-13_CRITIC-REPORT.md for the full audit."

**Record decisions with rationale:**
- Bad: "Changed the DRO radius"
- Good: "Changed DRO radius justification from 'theoretically calibrated' to 'empirically validated' because 168^{-1/6}≈0.43, not 0.13 as originally stated. Sensitivity analysis in Section 4 independently supports r=0.1."

**List next actions as actionable tasks:**
- Bad: "Continue working on the paper"
- Good: "Choose venue (Applied Energy vs Energy and AI), reformat if needed, run /pre-submission-report, submit"

## Workspace Focus Update (`current-focus.md`)

After updating the project progress record, also update the workspace-level file:

```markdown
# Current Focus — Claude Research Workspace

> Last updated: YYYY-MM-DD

## Active Project

**<project-name>** — <one-line description>
- **Location:** `~/Desktop/<project>/`
- **Status:** <current state>
- **Context:** See `~/Desktop/<project>/.context/progress.md` for full details

## What Was Done Recently

<3-5 bullet summary of the last 1-2 sessions>

## Next Steps

<2-3 concrete next actions>
```

This file is intentionally brief — it points to the project-level progress record for details.

## Workflow

1. Read the current `progress.md` (if it exists) to understand what was recorded before
2. Ask the user: "Anything else to record before I update the progress log?" (optional — skip if the session ending is obvious)
3. Write/update `<project>/.context/progress.md` with full session details
4. Update `claude-research/.context/current-focus.md` with high-level summary
5. If the project has a `MEMORY.md`, check if any [LEARN] tags should be added from this session

## Integration

| Skill | Relationship |
|-------|-------------|
| `/update-focus` | Older skill — `progress-log` supersedes it with more structure |
| `/save-context` | For ad-hoc saves to context files mid-session |
| `/learn` | For extracting reusable skills (different from progress recording) |
