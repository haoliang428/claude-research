---
name: Feedback — Research Method Preferences
description: Methodological preferences learned from ai-energy-ot project. LP over Sinkhorn, proper DRO, design-first.
type: feedback
---

**Exact methods over approximate when tractable.** User pushed back on Sinkhorn when exact LP was available and in the research design. Don't default to popular/trendy methods when simpler exact methods exist.
**Why:** Approximate methods (Sinkhorn, heuristic DRO) introduce tuning parameters and can perform worse than exact alternatives.
**How to apply:** For dispatch/allocation problems, try exact LP first. Only use entropic regularization if the problem is too large for LP or you specifically need soft assignments.

**Use proper DRO formulations, not heuristics.** The r*sigma mean-shift approximation has no formal guarantee. The Mohajerin Esfahani & Kuhn (2018) Wasserstein dual is the standard.
**Why:** Papers need theoretical backing. Heuristics can't provide the finite-sample guarantees that reviewers expect.
**How to apply:** For any DRO application, implement the proper dual reformulation from M.E. & Kuhn 2018. Cite Theorem 1 (tractable dual) and Theorem 2 (finite-sample bound).

**Validate metric choice from literature.** For carbon accounting, MOER (marginal) is correct for load-shifting, not average CI. Bashir 2024 validates this.
**Why:** Using the wrong metric undermines the entire analysis.
**How to apply:** When working with emissions data, confirm whether marginal or average is appropriate for the specific decision being modeled.
