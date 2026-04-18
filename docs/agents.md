# Agents (5)

Specialised review agents in `.claude/agents/`. Each runs as a sub-agent with its own context.

| Agent | Purpose | Produces |
|-------|---------|----------|
| `paper-critic` | Adversarial quality audit (9 check categories, scored) | `CRITIC-REPORT.md` |
| `domain-reviewer` | Math verification, code-theory alignment, assumptions (5 lenses) | `DOMAIN-REVIEW.md` |
| `peer-reviewer` | Review someone else's paper (referee role) | Structured referee report |
| `proposal-reviewer` | Review proposals and extended abstracts | Feasibility + novelty assessment |
| `referee2-reviewer` | Adversarial "Reviewer 2" critique of your own work | Hostile but constructive review |

## When to Use Which

- **Your own paper (quality check):** `paper-critic` for formatting/consistency, `domain-reviewer` for math/logic
- **Your own paper (stress test):** `referee2-reviewer` for adversarial critique
- **Someone else's paper:** `peer-reviewer` for a structured referee report
- **A proposal or abstract:** `proposal-reviewer` for feasibility assessment
- **Pre-submission:** Run `paper-critic` + `domain-reviewer` in parallel via `/pre-submission-report`
