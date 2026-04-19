---
name: ai-energy-ot review patterns
description: Patterns and issues found in the AI Energy OT paper (carbon-aware dispatch via Kantorovich LP + Wasserstein DRO)
type: project
---

## Key Issues Found

### Round 1 (2026-04-13) -> Round 2 (2026-04-19)
- **Dumas misattribution (C1)**: R1 said "Wasserstein GANs"; R2 fix over-corrected to "normalizing flows, GANs, and VAEs" -- still wrong. Paper is normalizing-flows ONLY. **Persists across 2 rounds.**
- **HiGHS citation (C2)**: FIXED in R2 -- now cites huangfu2018highs correctly.
- **DRO Lipschitz constraint (M1)**: Interpretation unchanged across 2 rounds. The conflation of "load cap" with "sensitivity bound" is a recurring conceptual issue in the writing.
- **British/American mixing**: 2x "optimise" vs 19x "optimize" -- new finding in R2.
- **Unused bib entries**: >55% of bib entries uncited. The bib is a master file (56 entries) but only ~25 are used in the paper.
- **Float specifier warnings increased**: 5 in R1 -> 12 in R2 (paper grew from 23 to 28 pages).

## Project Conventions
- Uses INFORMS IJDS template (informs4.cls)
- natbib with author-year style
- Notation follows locked registry in docs/research-design-lock.md Section 9
- Paper has 28 pages (grew from 23 in R1), no stated page limit
- All experiments complete; paper is in writing/polishing stage
- American English is the dominant convention (INFORMS standard)
