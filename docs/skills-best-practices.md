# Skills Best Practices

> 30 custom skills for academic research. Each is a flat directory under `skills/` with a `SKILL.md` defining the workflow. This document covers when to use each, what to expect, and common pitfalls.

---

## Research Discovery

### `/literature`
**What it does:** Searches for academic papers via the MCP bibliography server (OpenAlex + Scopus), synthesizes findings, and manages `.bib` entries.

**Best practice:**
- Start with a broad query, then narrow. E.g., "carbon-aware computing" → "Wasserstein DRO for datacenter dispatch"
- Always verify DOIs and author names before adding to bib
- Use for building literature clusters, not for reading individual papers (use `/reading-notes` for that)

### `/split-pdf`
**What it does:** Downloads a PDF, splits it into 4-page batches, and reads each batch sequentially for deep comprehension.

**Best practice:**
- Use for papers you need to understand thoroughly (methodology, proofs, key results)
- Not needed for papers you only need to cite — a title/abstract is enough for those
- Works with local files or URLs

### `/reading-notes`
**What it does:** Produces structured reading notes with 8-dimension extraction: problem, method, data, results, limitations, connections, key equations, and open questions.

**Best practice:**
- Run after `/split-pdf` for important papers
- Notes are saved to `docs/readings/notes/` — these become the ground truth for `/bib-validate claims`
- Write notes before writing your paper, not after — they inform the literature review

### `/devils-advocate`
**What it does:** Challenges your research assumptions through structured multi-turn debate. Probes identification strategy, hidden assumptions, and alternative explanations.

**Best practice:**
- Use before locking your research design, not after
- Especially valuable for methodology choices that feel "obvious" — those are the ones with hidden assumptions
- The goal is to find weaknesses before reviewers do

### `/multi-perspective`
**What it does:** Explores a research question from multiple independent disciplinary perspectives (e.g., economics, CS, operations research, environmental science).

**Best practice:**
- Use when your question spans disciplines
- Good for finding related work in fields you wouldn't normally search
- Each perspective is independent — contradictions between them are features, not bugs

---

## Paper Writing

### `/paper-draft`
**What it does:** Guides section-by-section drafting with quality conventions: flowing prose, no bullet points, every claim cited, methodology-first writing order.

**Best practice:**
- Write in order: Methodology → Results → Introduction → Literature Review → Conclusion → Abstract
- Provide the section name as argument: `/paper-draft methodology`
- Conventions enforced: no inline sub-headers, no boilerplate, no abstract/intro duplication, American English
- After any figure update, verify all text references match (this is a common failure mode)

### `/latex`
**What it does:** Basic LaTeX compilation via `latexmk -pdf`.

**Best practice:**
- Use for quick compilation checks
- For compilation with error resolution, use `/latex-autofix` instead

### `/latex-autofix`
**What it does:** Compiles LaTeX, automatically diagnoses and fixes errors, runs citation audit.

**Best practice:**
- Run before any review skill (`/proofread`, `/pre-submission-report`)
- Fixes common issues: missing packages, undefined references, bib errors
- Always review the fixes — auto-fixes can occasionally be wrong

### `/proofread`
**What it does:** Report-only 14-category quality check. Never edits source files — produces `PROOFREAD-REPORT.md` with scored issues.

**14 categories:** grammar, notation consistency, citation format, academic tone, LaTeX warnings, citation voice balance, TikZ diagrams, numeric cross-check, causal language, equation completeness, preprint staleness, abbreviation completeness, inline sub-headers, unfulfilled forward references.

**Best practice:**
- Run after the paper is feature-complete, not during active drafting
- Fix Critical issues immediately; Major issues before submission; Minor issues if time permits
- Includes AI pattern density scan — target < 0.5 patterns per 100 words
- Does NOT fix anything — pair with manual edits after reading the report

---

## Experiments

### `/experiment-runner`
**What it does:** Runs experiment scripts, generates publication-quality figures, and updates the paper with validated results.

**Best practice:**
- Write sanity-check assertions before running full experiments
- Run single-seed sanity check first, then full sweep
- Validate parameters against domain knowledge before committing to long runs

### `/replication-check`
**What it does:** Verifies that every quantitative claim in the paper (numbers, percentages, p-values) matches actual experiment output.

**Best practice:**
- Run after all experiments are final and the paper text is stable
- Catches stale numbers from earlier experiment runs that were never updated in the text
- Especially important after re-running experiments with different parameters

### `/pipeline-manifest`
**What it does:** Maps every script to its inputs, outputs, and which paper figures/tables it produces.

**Best practice:**
- Run once after the experiment pipeline is stable
- Useful for reproducibility documentation and for onboarding collaborators
- Reveals orphaned scripts (output not used) and missing dependencies

---

## Quality & Submission

### `/bib-validate`
**What it does:** Cross-references `\cite{}` keys against `.bib` files. Three modes: standard (missing/unused keys), deep (DOI verification, preprint staleness), claims (verify citation claims against reading notes).

**Best practice:**
- Run `standard` mode frequently during writing
- Run `deep` mode before submission
- Run `claims` mode as part of `/pre-submission-report` — this is the most important check because misattributed citations are the most damaging reviewer finding
- Keep reading notes in `docs/readings/notes/` — claims mode cross-references against them

### `/pre-submission-report`
**What it does:** Runs all quality checks in parallel: paper-critic agent, domain-reviewer agent, bib-validate deep + claims, compilation. Produces a single aggregated report with priority-ranked fixes.

**Best practice:**
- Run once, after the paper is otherwise complete
- Fix must-fix items (blockers), then should-fix items (strengthens paper), then nice-to-fix (polish)
- Do NOT run this repeatedly during active drafting — it's expensive (3 parallel agents)
- The citation claim check (Check D) is the most important non-obvious check

### `/venue-research`
**What it does:** Compares target journals: impact factor, acceptance rate, review speed, scope fit, formatting requirements, page limits.

**Best practice:**
- Run after the paper is shaped but before formatting
- Provide 2-3 candidate venues for comparison
- Check page limits early — a 28-page paper won't fit in a 15-page-limit venue

### `/process-reviews`
**What it does:** Processes referee comments from a reviews PDF into structured tracking files with response plan.

**Best practice:**
- Run immediately after receiving reviews
- Produces a checklist of required changes with severity and estimated effort
- Track each reviewer comment as a discrete item — don't batch

### `/council`
**What it does:** Sends a task to both Gemini and Claude independently, cross-reviews their responses, and synthesizes the best answer.

**Best practice:**
- Most valuable for subjective tasks: proofreading, methodology critique, code review
- For objective tasks (math verification, number checking), a single model is usually sufficient
- Takes 2-3 minutes for full paper reviews
- Results are anonymized as "Assessment A/B" during cross-review to avoid bias

---

## Code

### `/code-review`
**What it does:** Quality scorecard for Python research scripts: reproducibility, structure, domain correctness, hardcoded values, error handling.

**Best practice:**
- Run on experiment scripts before considering the results "final"
- Catches hardcoded paths, missing seeds, untested edge cases
- Focus on the scripts that produce paper figures — those are the highest-stakes code

### `/code-archaeology`
**What it does:** Reads and explains old or unfamiliar code, data files, or analysis scripts.

**Best practice:**
- Use when returning to code after weeks/months
- Use when inheriting code from collaborators
- Not needed for code you just wrote — it's for understanding, not review

### `/python-env`
**What it does:** Python environment management with `uv`: create venvs, install packages, manage dependencies.

**Best practice:**
- Always use `uv`, never bare `pip`
- Use inline script metadata (`# /// script`) for standalone scripts
- Use `uv sync` for project-level dependencies

---

## Project & Context

### `/init-project-research`
**What it does:** Bootstraps a full research project: directory scaffold (`code/`, `data/`, `paper/`, `docs/`, `.context/`), Overleaf symlink, git init, CLAUDE.md.

**Best practice:**
- Run once at project start
- If the Overleaf project already exists, provide the folder name for symlinking
- Never create a new Overleaf folder if one exists — this creates duplicates

### `/progress-log`
**What it does:** Records detailed session progress to `<project>/.context/progress.md` and updates `claude-research/.context/current-focus.md`.

**Best practice:**
- Run at the end of every session — this is mandatory
- Be specific: file paths, line numbers, exact numbers, decisions with rationale
- A fresh session should be able to continue work by reading this file alone
- Supersedes the older `/update-focus` skill

### `/update-focus`
**What it does:** Structured update to `current-focus.md`.

**Best practice:**
- Use `/progress-log` instead — it's more structured and updates both project and workspace files

### `/save-context`
**What it does:** Saves specific information from the current conversation to context library files.

**Best practice:**
- Use for ad-hoc saves mid-session (not end-of-session — use `/progress-log` for that)
- Good for capturing research decisions, field calibration data, or configuration details

### `/update-project-doc`
**What it does:** Updates a project's CLAUDE.md, README.md, or docs/ to reflect current state.

**Best practice:**
- Run after major milestones (experiments complete, paper drafted, submission)
- Keep CLAUDE.md lean — pointers to other docs, not the docs themselves

---

## Meta

### `/learn`
**What it does:** Extracts reusable knowledge from the current session into a persistent skill or memory.

**Best practice:**
- Use when you discover a non-obvious workflow, workaround, or multi-step process
- The output is a new skill or memory file, not a one-time fix
- Don't use for project-specific learnings — use `[LEARN]` tags in MEMORY.md for those

### `/lessons-learned`
**What it does:** Structured post-mortem after incidents, mistakes, or stuck sessions.

**Best practice:**
- Run after any session where something went wrong: wrong results, wasted time, broken pipeline
- Captures what happened, why, and what to do differently
- The goal is to prevent the same mistake in future sessions

### `/consolidate-memory`
**What it does:** Prunes duplicates and merges overlapping entries in MEMORY.md files.

**Best practice:**
- Run when MEMORY.md exceeds ~50 entries
- Removes stale entries, merges related items, keeps the file scannable

### `/creation-guard`
**What it does:** Pre-flight duplicate check before creating new skills or agents.

**Best practice:**
- Always run before `/learn` to avoid creating a skill that already exists
- Checks name similarity, not just exact matches

### `/system-audit`
**What it does:** Runs parallel audits across skills, hooks, agents, rules, and conventions.

**Best practice:**
- Run after major template changes (adding/removing skills, updating hooks)
- Catches stale references, missing files, inconsistent counts
- Good periodic hygiene — run every few weeks

---

## Workflow Patterns

### Starting a new paper
```
/init-project-research → /literature → /reading-notes (key papers) →
/devils-advocate (research design) → /paper-draft methodology →
/experiment-runner → /paper-draft results → /paper-draft introduction →
/paper-draft literature → /paper-draft conclusion → /paper-draft abstract
```

### Pre-submission checklist
```
/latex-autofix → /proofread → fix issues →
/pre-submission-report → fix issues →
/venue-research → format for venue → submit
```

### After receiving reviews
```
/process-reviews → plan responses → make changes →
/replication-check → /proofread → resubmit
```
