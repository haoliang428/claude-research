# Rule: Record Learnings with [LEARN] Tags

## Format

```
[LEARN:category] Incorrect → Correct
```

## Categories

| Category | What to record |
|----------|---------------|
| `notation` | Math/LaTeX notation conventions |
| `citation` | Bibliography and citation issues |
| `code` | Programming patterns, bugs, gotchas |
| `method` | Statistical/optimization method corrections |
| `domain` | Domain knowledge corrections |

## When to Record

Immediately when a correction is discovered. Do not batch.

## Where to Write

Append to `MEMORY.md` in the project root. Also add to the matching table:
- `[LEARN:notation]` → Notation Registry
- `[LEARN:code]` → Code Pitfalls
- `[LEARN:method]` or `[LEARN:domain]` → Anti-Patterns or Key Decisions
- `[LEARN:citation]` → Citations section

## MEMORY.md Sections (Research Projects)

| Section | Columns |
|---------|---------|
| **Key Decisions** | Decision / Rationale / Date |
| **Citations** | One-liner corrections |
| **Anti-Patterns** | What went wrong / Correction |
| **Code Pitfalls** | Bug / Impact / Fix |
| **Research Workflow Learnings** | Learning / Context / Date |

## Examples

```
[LEARN:citation] Mohajerin Esfahani & Kuhn (2018) key is mohajerin2018data not esfahani2018
[LEARN:code] .values on pandas selection returns read-only array — use .values.copy()
[LEARN:method] 168^{-1/6} ≈ 0.43 not 0.13 — always verify DRO radius numerically
[LEARN:domain] Clover (Li 2023) is single-site model selection, NOT spatial shifting
```
