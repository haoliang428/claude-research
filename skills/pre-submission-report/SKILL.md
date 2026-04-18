---
name: pre-submission-report
description: "Use when you need all quality checks run before submission, producing a single dated report."
allowed-tools: Bash(latexmk*, mkdir*, ls*, wc*), Read, Write, Edit, Glob, Grep, Task, Skill, mcp__bibliography__scholarly_search, mcp__bibliography__scholarly_verify_dois
argument-hint: "[path/to/main.tex or no arguments to auto-detect]"
---

# Pre-Submission Report

Run all quality checks before submitting to a journal. Produces a single dated report.

## When to Use

- Before submitting a paper to a venue
- Before sharing a draft with co-authors
- "Is this ready?", "run everything", "pre-submission check"

## Workflow

### 1. Locate the Paper

If no argument provided, search for the main `.tex` file:
1. Check `paper/paper/main.tex`
2. Check `paper/*.tex` for `\begin{document}`
3. Ask if ambiguous

### 2. Integrity Gate (must pass before quality checks)

Quick checks that block submission:

1. **Placeholder scan** — grep for `TODO`, `FIXME`, `XXX`, `TBD`, `[INSERT`, `PLACEHOLDER`
2. **Section completeness** — Abstract, Introduction, at least one body section, Conclusion all exist and non-empty
3. **Broken references** — grep compiled `.log` for undefined `\ref` or `\cite` warnings
4. **Citation integrity** — run `/bib-validate` standard mode. Every `\cite{}` must resolve.

If any fail, stop and report blockers. Do not proceed to quality checks.

### 3. Quality Checks (run in parallel where possible)

Launch these as parallel agents:

**Check A: Paper Critic** — launch `paper-critic` agent
- Scores content quality, identifies structural issues
- Produces CRITIC-REPORT.md with scored issues

**Check B: Domain Review** — launch `domain-reviewer` agent
- Verifies mathematical derivations against code
- Checks assumption completeness
- Validates notation consistency
- Produces DOMAIN-REVIEW.md

**Check C: Bibliography Deep Validation** — run `/bib-validate deep`
- DOI verification with title matching
- Preprint staleness check
- Entry type correctness
- Author completeness

**Check D: Citation Claim Verification** — run `/bib-validate claims`
- For each citation, verify the claim in the paper matches what the cited paper actually says
- Cross-reference against reading notes in `docs/readings/notes/`
- This catches the most damaging errors (misattributions that reviewers will flag)

**Check E: Compilation** — run `latexmk -pdf`
- Record warnings count
- Check for overfull/underfull hboxes

### 4. Aggregate Report

Save to `reviews/pre-submission/YYYY-MM-DD_report.md`:

```markdown
# Pre-Submission Report

**Project:** <name>
**Date:** YYYY-MM-DD
**File:** <path>
**Target venue:** <venue>
**Page count:** <N>

## Integrity Gate: PASS / FAIL

- Placeholders: <count>
- Section completeness: PASS / <missing sections>
- Broken references: <count>
- Citation integrity: <missing keys>

## Quality Checks

### Paper Critic (Score: XX/100)
- Critical issues: <count>
- Major issues: <count>
- Top 3 issues: ...

### Domain Review
- Math errors: <count>
- Assumption gaps: <count>
- Code-theory mismatches: <count>
- Top issues: ...

### Bibliography
- DOI issues: <count>
- Preprint staleness: <count>
- Incomplete entries: <count>

### Citation Claims
- Misattributions found: <count>
- Severity breakdown: <critical/major/minor>
- Top issues: ...

### Compilation
- Status: PASS / FAIL
- Warnings: <count>

## Recommendation

**[Submit / Revise / Not ready]**

<summary of what needs to happen>
```

### 5. Present Summary

Display the report path and recommendation. If "Revise", list issues by priority (critical first). If "Submit", confirm the paper is ready.

## Key Lesson

The citation claim check (Check D) is the most important non-obvious check. Citation claims can be inaccurate even when all papers are real and all DOIs are valid (e.g., attributing a finding to a paper that makes a different argument, or calling a single-site method "spatial shifting"). A reviewer who knows the cited paper would flag the misattribution immediately.

## Integration

| Check | Tool/Agent |
|-------|-----------|
| Paper Critic | `paper-critic` agent |
| Domain Review | `domain-reviewer` agent |
| Bibliography | `/bib-validate deep` |
| Citation Claims | `/bib-validate claims` |
| Compilation | `/latex-autofix` |
| Proofreading | `/proofread` (optional, run separately) |
