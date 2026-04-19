# Claude Code for Academic Research

## Before You Start

Read these context files:

1. `.context/profile/profile.md` — Who you are, research areas, CV
2. `.context/current-focus.md` — What you're working on NOW
3. `.context/projects/_index.md` — Overview of all projects

## Key Information

**Who I am:**
- AI/ML Engineer at Roche; research active (2 published papers, 9 journal reviewer roles)
- MS Machine Learning & Data Science (Northwestern), BS Statistics + Economics (UW-Madison)
- FRM certified, CFA Sustainable Investing

**Research areas:**
- Energy economics (EV adoption, AI energy consumption, carbon-aware computing)
- Optimal transport / DRO for operational problems
- Environmental disclosure and AI innovation zones
- Financial forecasting (volatility, Chinese futures)

**How I work:**
- Flexible/reactive style — prefers autonomous execution over step-by-step approval
- Wants questions over lists when direction is unclear
- Full context in task descriptions
- Pushes back when implementation drifts from research design — stick to the plan

## Quick Commands

| You say | Claude does |
|---------|-------------|
| "What should I work on?" | Reviews current-focus.md and helps decide |
| "Find references on [topic]" | `/literature` — academic search with verified citations |
| "Read this paper" | `/reading-notes` — structured notes with 8-dimension extraction |
| "Write the methodology section" | `/paper-draft` — section-by-section drafting with conventions |
| "Proofread my paper" | `/proofread` — quality check across 14 categories |
| "Validate my bibliography" | `/bib-validate` — cross-references cite keys, DOIs, claims |
| "Run the experiments" | `/experiment-runner` — run, generate figures, update paper |
| "Is this ready to submit?" | `/pre-submission-report` — full audit (critic + domain + bib + claims) |
| "Where should I submit?" | `/venue-research` — journal comparison with IF, acceptance rate, fit |
| "Review my code" | `/code-review` — scorecard for Python research scripts |
| "Get a second opinion" | `/council` — sends to Gemini + Claude, cross-reviews, synthesizes |
| "New project" | `/init-project-research` — scaffold directory, Overleaf symlink, git init |
| "Save progress" | `/progress-log` — detailed record of what was done, decisions, results, next steps |

## Conventions

### LaTeX
- Compile with `/latex-autofix` (auto-fixes errors, runs citation audit)
- Build artifacts in `out/`, PDF copied back via `.latexmkrc`
- Paper source in `paper/paper/` (Overleaf symlink). Code never in `paper/`.

### Python
- Always use `uv` (never bare pip)
- Shared library pattern: `code/lib/` with config, data, solvers, plotting modules
- Scripts run via `uv run code/experiments/<script>.py`

### Experiments
Before running any experiment sweep:
1. Write sanity-check assertions first
2. Run a single-seed sanity check
3. Validate parameters against domain knowledge
4. Only then proceed to full experiments

### Paper Writing
- Academic papers in LaTeX. Methodology first, abstract last.
- Flowing prose, no bullet-point findings, no boilerplate
- Every assumption needs evidence. Every number needs a source.
- See `/paper-draft` and `/proofread` skills for full conventions.

### Git
- Check if a local copy exists before cloning any repo

## Skills (30)

All skills live as flat directories under `skills/`. Grouped by purpose:

**Research Discovery:**
`literature` · `split-pdf` · `reading-notes` · `devils-advocate` · `multi-perspective`

**Paper Writing:**
`paper-draft` · `latex` · `latex-autofix` · `proofread`

**Experiments:**
`experiment-runner` · `replication-check` · `pipeline-manifest`

**Quality & Submission:**
`bib-validate` · `pre-submission-report` · `venue-research` · `process-reviews` · `council`

**Code:**
`code-review` · `code-archaeology` · `python-env`

**Project & Context:**
`init-project-research` · `progress-log` · `update-focus` · `save-context` · `update-project-doc`

**Meta:**
`learn` · `lessons-learned` · `consolidate-memory` · `creation-guard` · `system-audit` · `shared`

## Agents (5)

| Agent | Purpose |
|-------|---------|
| `paper-critic` | Adversarial quality audit (9 check categories, scored CRITIC-REPORT.md) |
| `domain-reviewer` | Math verification, code-theory alignment, assumptions (5 lenses) |
| `peer-reviewer` | Review someone else's paper (referee role) |
| `proposal-reviewer` | Review proposals and extended abstracts |
| `referee2-reviewer` | Adversarial "Reviewer 2" critique of your own work |

## Hooks (4 active, wired in ~/.claude/settings.json)

| Hook | Trigger | What it does |
|------|---------|-------------|
| `startup-context-loader.sh` | Session start/resume | Auto-loads focus, project index, progress, latest plan |
| `block-destructive-git.sh` | Before Bash | Catches `git reset --hard`, `push --force`, `rm -rf`, etc. |
| `precompact-autosave.py` | Before compression | Saves state snapshot to log/ |
| `postcompact-restore.py` | After compression | Restores context from snapshot |

## Rules (7 Auto-Loaded)

| Rule | Purpose |
|------|---------|
| `design-before-results` | Lock research design before examining point estimates |
| `lean-claude-md` | Keep CLAUDE.md lean — every line costs tokens |
| `learn-tags` | Record learnings with [LEARN] tags in project MEMORY.md |
| `overleaf-separation` | `paper/` is for LaTeX only — no code or data |
| `plan-first` | Plan before implementing (multi-file edits) |
| `read-docs-first` | Read docs before searching |
| `scope-discipline` | Only make changes explicitly requested |

## After Every Session

Run `/progress-log` to record what was done, decisions made, results produced, and what's next. This is the working memory between sessions.

## File Structure

| Path | What lives there |
|------|-----------------|
| `.context/` | Profile, current focus, projects index |
| `.claude/agents/` | 5 agent definitions |
| `.claude/rules/` | 7 auto-loaded rules |
| `skills/` | 30 skills (see above) |
| `hooks/` | Hook scripts |
| `packages/mcp-bibliography/` | MCP bibliography server (OpenAlex + Scopus) |
| `packages/cli-council/` | Multi-model council (Gemini + Claude) |
| `docs/` | Documentation |
