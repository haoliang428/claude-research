---
name: replication-check
description: "Use when you need to verify that every quantitative claim in the paper matches actual experiment output."
allowed-tools: Read, Glob, Grep, Bash(python*), Bash(uv*), Bash(cat*), Bash(jq*)
argument-hint: "[path-to-main.tex or no arguments to auto-detect]"
---

# Replication Check

Systematically verify that every quantitative claim in the paper is traceable to experiment output. Catches stale numbers, rounding errors, and claims that don't match the data.

## When to Use

- Before submission (after all experiments are final)
- After re-running experiments with updated parameters
- After any code change that could affect results
- "Check all the numbers", "verify the results match"

## Workflow

### Step 1: Extract All Quantitative Claims

Read the paper's `.tex` file and extract every quantitative claim:

- Percentages (e.g., `+12.6\%`, `2.7\%`)
- Counts (e.g., "6 datacenters", "28 studies", "8,786 hours")
- Statistics (e.g., `$\rho = -0.11$`, `CV = 0.41`)
- Ranges (e.g., "108\%--210\%")
- Comparative claims (e.g., "outperforms B2 by 0.4 percentage points")

For each claim, record:
- The exact text and line number
- Which section it appears in
- What it claims

### Step 2: Locate the Source

For each claim, find where the number comes from:

1. **Experiment results JSON** — check `paper/paper/figures/experiment_results.json` or `results/` directory
2. **Experiment script output** — check stdout captured from `code/experiments/` scripts
3. **Data source** — check `data/raw/` for raw data properties (e.g., number of hours, number of regions)
4. **Literature** — check `references.bib` and reading notes for cited statistics (e.g., "28 studies" from Asadov 2025)
5. **Computation** — some numbers are derived (e.g., "0.4 percentage points" = 12.6% - 12.2%)

### Step 3: Verify Each Claim

For each claim, check:

| Check | Pass criteria |
|-------|--------------|
| **Existence** | The source number exists and is findable |
| **Match** | The paper's number matches the source exactly (or within stated rounding) |
| **Currency** | The source is from the most recent experiment run (not a stale earlier run) |
| **Derivation** | If the number is derived (e.g., a difference), the arithmetic is correct |
| **Context** | The number is presented in the correct context (not cherry-picked from a subset) |

### Step 4: Report

Output a verification table:

```markdown
## Replication Check Report

**Paper:** <path>
**Results source:** <path to JSON or script output>
**Date:** YYYY-MM-DD

### Verified Claims

| Line | Claim | Source | Status |
|------|-------|--------|--------|
| 55 | LP achieves 12.6% savings | experiment_results.json: B3_LP.savings_pct = 12.623 | PASS (rounded) |
| 55 | temporal shifting +2.7% | experiment_results.json: B1.savings_pct = 2.705 | PASS (rounded) |
| 298 | B4 saves 10.2% | experiment_results.json: B4_DRO.savings_pct = 10.15 | PASS (rounded) |

### Failed Claims

| Line | Claim | Source | Issue |
|------|-------|--------|-------|
| 334 | B3 achieves +5.8% at 108% | capacity_sensitivity[0].B3_savings = 1.2 | FAIL: paper says 5.8%, data says 1.2% |

### Unverifiable Claims

| Line | Claim | Issue |
|------|-------|-------|
| 67 | "order of magnitude less carbon" | Qualitative claim, no specific number to verify |

### Summary

- Total claims checked: <N>
- Passed: <N>
- Failed: <N>
- Unverifiable: <N>
```

### Step 5: Fix Discrepancies

For each FAIL:
1. Determine which is correct: the paper or the experiment output
2. If the experiment is correct: update the paper text
3. If the paper is correct: the experiment may need re-running with different parameters
4. Recompile and re-check

## What Counts as a "Claim"

**Check these:**
- Any specific number in the text (%, count, statistic)
- Table entries
- Figure axis ranges and annotations
- Caption numbers
- Abstract numbers (must match body)
- Introduction preview numbers (must match Results section)

**Skip these:**
- General statements without numbers ("spatial shifting outperforms temporal")
- Methodology descriptions (equations, not results)
- Citations of others' findings (verified by `/bib-validate claims`)

## Integration

| Skill | Relationship |
|-------|-------------|
| `/experiment-runner` | Run experiments first, then check numbers |
| `/bib-validate claims` | Verifies citation claims; this skill verifies your own experimental claims |
| `/pre-submission-report` | Includes this as one of several checks |
