# System Architecture

## Overview

```
claude-research/                    ← workspace (this repo)
├── CLAUDE.md                       ← auto-loaded every session
├── .claude/
│   ├── agents/ (5)                 ← review agents (paper-critic, domain-reviewer, etc.)
│   └── rules/ (7)                  ← auto-loaded behavior rules
├── skills/ (30)                    ← reusable workflow definitions
├── hooks/ (4)                      ← lifecycle hooks (symlinked to ~/.claude/hooks/)
├── packages/
│   ├── mcp-bibliography/           ← academic search MCP server
│   └── cli-council/                ← multi-model council (Gemini + Claude)
├── .context/                       ← workspace-level context (focus, projects index)
├── docs/                           ← this documentation
└── scripts/                        ← setup scripts

~/Desktop/<project>/                ← individual research projects
├── CLAUDE.md                       ← project-specific instructions
├── MEMORY.md                       ← project learnings ([LEARN] tags)
├── .context/progress.md            ← detailed session progress
├── code/lib/                       ← shared Python modules (config, data, solvers, plotting)
├── code/experiments/               ← experiment scripts
├── data/raw/                       ← original data (gitignored)
├── docs/readings/notes/            ← paper reading notes
├── paper/paper/                    ← Overleaf symlink (LaTeX only)
├── results/figures/                ← generated figures
├── references.bib                  ← master bibliography
└── reviews/                        ← audit reports
```

## Data Flow

```
Literature search ──→ reading notes ──→ references.bib ──→ paper draft
        │                                      │                │
   /literature                           /bib-validate    /paper-draft
   /reading-notes                                         /latex-autofix
                                                                │
                                                          experiments
                                                                │
                                                         /experiment-runner
                                                         /replication-check
                                                                │
                                                          quality checks
                                                                │
                                                    /pre-submission-report
                                                    /proofread + /council
                                                                │
                                                         /venue-research
                                                                │
                                                            submit
```

## Key Design Decisions

- **Workspace vs project separation:** Skills, agents, rules are workspace-level (reusable). Data, code, paper, results are project-level.
- **Overleaf symlink:** `paper/paper/` symlinks to `~/Apps/Overleaf/<folder>`. Code never goes in `paper/`.
- **Shared code library:** Each project uses `code/lib/` (config, data, solvers, plotting) to eliminate duplication across experiment scripts.
- **MCP for bibliography:** Academic search via MCP server, not web scraping. Provides `scholarly_search`, `scholarly_verify_dois`, etc.
- **Council for second opinions:** Gemini + Claude via cli-council for tasks where model diversity helps (proofreading, critique).
