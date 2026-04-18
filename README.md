# Claude Code for Academic Research

A Claude Code workspace for academic researchers — skills, agents, hooks, and rules for literature review, paper writing, experiments, and submission workflows.

## What's Included

| Component | Count | Description |
|-----------|-------|-------------|
| **Skills** | 30 | Slash commands for research tasks (`/literature`, `/paper-draft`, `/proofread`, `/experiment-runner`, etc.) |
| **Agents** | 5 | Review agents (paper-critic, domain-reviewer, peer-reviewer, proposal-reviewer, referee2) |
| **Hooks** | 4 | Automated guardrails (context loading, destructive git protection, compact state save/restore) |
| **Rules** | 7 | Always-on policies (plan-first, scope discipline, design before results, etc.) |
| **MCP Bibliography** | — | Multi-source scholarly search (OpenAlex + Scopus + CORE) |
| **Council Mode** | — | Multi-model review via Gemini + Claude |

## Quick Start

```bash
git clone https://github.com/haoliang428/claude-research.git ~/Desktop/claude-research
cd ~/Desktop/claude-research
```

Then open with Claude Code. See [`docs/getting-started.md`](docs/getting-started.md) for full setup.

## Typical Workflow

1. `/init-project-research` — scaffold a new project
2. `/literature` — search for papers
3. `/reading-notes` — take structured notes
4. `/paper-draft` — write the paper
5. `/experiment-runner` — run experiments and generate figures
6. `/bib-validate claims` — verify citation accuracy
7. `/proofread` — quality check + AI pattern scan
8. `/pre-submission-report` — full audit before submission
9. `/venue-research` — choose where to submit
10. `/progress-log` — record progress for next session

## Project Structure

```
claude-research/
├── CLAUDE.md                    # Main instruction file
├── .claude/
│   ├── agents/                  # 5 review agents
│   └── rules/                   # 7 auto-loaded rules
├── skills/                      # 30 skills
├── hooks/                       # 4 lifecycle hooks
├── packages/
│   ├── mcp-bibliography/        # Academic search MCP server
│   └── cli-council/             # Multi-model council (Gemini + Claude)
├── .context/                    # Workspace context (focus, projects)
├── docs/                        # Documentation
└── .mcp.json                    # MCP server configuration
```

## Documentation

- [`docs/getting-started.md`](docs/getting-started.md) — Setup guide
- [`docs/skills.md`](docs/skills.md) — All 30 skills
- [`docs/agents.md`](docs/agents.md) — 5 review agents
- [`docs/hooks.md`](docs/hooks.md) — 4 lifecycle hooks
- [`docs/rules.md`](docs/rules.md) — 7 auto-loaded rules
- [`docs/system.md`](docs/system.md) — Architecture overview
- [`docs/bibliography-setup.md`](docs/bibliography-setup.md) — MCP bibliography server
- [`docs/council-mode.md`](docs/council-mode.md) — Multi-model council

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- [Python 3.11+](https://www.python.org/) + [uv](https://docs.astral.sh/uv/)
- [Gemini CLI](https://github.com/google-gemini/gemini-cli) (for council mode)
- [TeX Live](https://tug.org/texlive/) (for LaTeX compilation)
- [Git](https://git-scm.com/)

## License

MIT
