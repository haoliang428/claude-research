---
name: ai-energy-ot review patterns
description: Patterns and issues found in the AI Energy OT paper (carbon-aware dispatch via Kantorovich LP + Wasserstein DRO)
type: project
---

## Key Issues Found (Round 1, 2026-04-13)

- **Citation misattributions**: Dumas et al. (2022) cited for "Wasserstein GANs" but paper is about normalizing flows. chen2020rsome cited for HiGHS solver but is about RSOME toolbox. Check all citation-claim pairs carefully on subsequent rounds.
- **DRO Lipschitz constraint**: The interpretation of ell_i <= lambda as "preventing load concentration" is an oversimplification. The actual mechanism bounds cost sensitivity to CI perturbations.
- **Redundancy pattern**: Author tends to repeat motivation (energy stats, inference dominance) across abstract, intro, and Section 3.1. Flag if still present in future rounds.
- **Bib key naming**: Several keys use given names instead of surnames (li2025carbonedge -> Wu is first author, xiang2023wasserstein -> Wei is first author, li2023equitable -> year is 2024 not 2023). Cosmetic but worth noting.

## Project Conventions
- Uses INFORMS IJDS template (informs4.cls)
- natbib with author-year style
- Notation follows locked registry in docs/research-design-lock.md Section 9
- Paper has 23 pages, no stated page limit
- All experiments complete; paper is in writing/polishing stage
