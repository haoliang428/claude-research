---
name: AI Energy OT Review Notes
description: Domain review findings for Kantorovich LP + Wasserstein DRO carbon-aware dispatch paper
type: project
---

## Key Findings (2026-04-19)

- Paper is mathematically sound -- 0 critical issues, 5 major, 11 minor
- DRO correctly applies ME&K 2018 Theorem 4.2 with l1 ground metric
- Main code-theory gap: B5 (spatio-temporal) hardcoded in main experiment script
- Capacity model implicitly scales with demand (fraction-based, not absolute)
- Spatial dominance claim needs capacity threshold qualifier (~120%)
- Fleet extrapolation to Google's 15.5 TWh needs stronger caveats

## DRO Derivation Pattern
- Linear loss + l1 ground metric -> l_inf Lipschitz constraint -> max_i l_i <= lambda
- Non-negativity of loads means |l_i| = l_i, so one-sided constraint suffices
- Unbounded support (R^n) is conservative; bounded support wouldn't need Lipschitz constraint

## Notation
- gamma_ij = spatial transport plan; gamma_ijts = spatio-temporal
- CI_t(i) in LP section; xi_i in DRO section (intentional: random variable)
- lambda = DRO dual variable only; latency = RTT (no conflict)
- Minor collision: r = DRO radius in equations, r = correlation in prose
