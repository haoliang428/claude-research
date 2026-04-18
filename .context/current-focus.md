# Current Focus — Claude Research Workspace

> Last updated: 2026-04-18

## Active Project

**ai-energy-ot** — Carbon-Aware AI Workload Dispatch via Kantorovich LP and Wasserstein DRO
- **Location:** `~/Desktop/ai-energy-ot/`
- **Status:** Complete paper draft (23 pages), all experiments validated, ready for submission
- **Venue:** Evaluating Applied Energy (IF 11.0), Energy and AI (IF 9.6), Omega (IF 6.9). IJDS VSI deprioritised (low IF).
- **Context:** See `~/Desktop/ai-energy-ot/.context/current-focus.md` for full project state

## What Was Done Recently (Apr 13–18)

1. Wrote complete 23-page paper: Abstract, Introduction, Literature Review (22 papers, integrated narrative), Methodology (4 subsections), Computational Experiments (7 figures, 4 tables), Conclusion
2. Ran all experiments with validated numbers: B0–B5 full year, DRO sensitivity, capacity sensitivity (108%–210%), latency sensitivity (30/50/100ms), seasonal breakdown, DC utilisation
3. Generated 7 publication-quality figures (PDF) embedded in paper
4. Verified all 22 citations against literature notes — fixed 8 inaccuracies (Clover not spatial, Bashir operational vs lifecycle, Ning biomass not storage, etc.)
5. Verified all 29 bibliography entries — fixed 8 issues (wrong authors, wrong titles, garbled names, misattributed solver citation)
6. Ran paper-critic and domain-reviewer agents — fixed 3 critical issues (DRO radius computation 168^{-1/6}≈0.43 not 0.13, HiGHS citation, Dumas characterisation)
7. Restructured project folder: notebooks/ → code/{experiments,eda,paper-figures,archive,lib}. Created shared library (code/lib/) with config, data, solvers, plotting modules
8. Pushed to GitHub (haoliang428/ai-energy-ot)

## Next Steps

1. Choose target journal (Applied Energy vs Energy and AI vs Omega)
2. Minor venue-specific formatting adjustments
3. Final proofread pass
4. Submit

## Workspace Infrastructure

- MCP bibliography server: configured in `.mcp.json` (OpenAlex + Scopus)
- 38 skills, 6 agents, 9 rules — all functional
- Research Vault at `~/Research-Vault`
