---
name: Feedback — Working Style Preferences
description: How Hao wants Claude to approach work. Autonomous execution, stick to design, concrete explainers, no unnecessary asks.
type: feedback
---

**Run autonomously and debug yourself.** When asked to run code, debug errors without asking — "run yourself and debug the code", "similarly, debug yourself". Only escalate if truly stuck after multiple attempts.
**Why:** User wants flow, not interruptions. Multiple sessions showed this pattern.
**How to apply:** When running experiments, catch errors, fix them, re-run. Report results, not intermediate failures.

**Stick to the research design.** Don't substitute methods without explicit approval — user asked "why you are using Sinkhorn?" and "can you stick to our research design?" when implementation drifted from the locked plan.
**Why:** The research design was carefully considered; deviating wastes time and produces results that don't match the paper's framing.
**How to apply:** Before implementing any method, check if it matches what's in the research design lock document. If you think a different method is better, explain why before switching.

**Write detailed explainers with concrete numbers.** User repeatedly asked for more detail — "can you explain more", "can you write everything in this great level of details". Preferred explainer MDs with worked examples, not just equations.
**Why:** User needs to deeply understand the methods to write the paper and defend the work.
**How to apply:** When explaining methods, include: the formal math, a concrete numerical example, and how results change with parameter choices.

**Provide notebooks (.ipynb) alongside scripts (.py).** User asked "can you write the code as notebook, so I can run it based on my need as well".
**Why:** Notebooks allow interactive exploration; scripts allow batch execution.
**How to apply:** For EDA and overview content, default to .ipynb. For full experiments, .py is fine but offer .ipynb conversion if asked.

**Don't ask permission for every step.** User's style is to give high-level direction and expect autonomous execution. Only pause for genuine design decisions, not implementation details.
**Why:** Asking too many clarifying questions breaks flow.
**How to apply:** Make reasonable choices and proceed. Explain what you chose after the fact.
