# Getting Started

## Prerequisites

- Claude Code CLI installed
- Gemini CLI installed and authenticated (`gemini` on PATH)
- `uv` installed for Python environment management
- LaTeX distribution (e.g., TexLive) for paper compilation
- Git

## Setup

1. **Clone the workspace:**
   ```bash
   git clone https://github.com/haoliang428/claude-research.git ~/Desktop/claude-research
   cd ~/Desktop/claude-research
   ```

2. **Symlink hooks, agents, and rules:**
   The workspace uses symlinks from `~/.claude/` to this repo:
   ```bash
   ln -sf ~/Desktop/claude-research/hooks ~/.claude/hooks
   ln -sf ~/Desktop/claude-research/.claude/agents ~/.claude/agents
   ln -sf ~/Desktop/claude-research/.claude/rules ~/.claude/rules
   ```

3. **Configure MCP bibliography server:**
   Edit `.mcp.json` with your API keys (see [bibliography-setup.md](bibliography-setup.md)).

4. **Install cli-council dependencies:**
   ```bash
   cd packages/cli-council && uv sync
   ```

5. **Verify everything works:**
   ```bash
   # Check MCP server
   cd ~/Desktop/claude-research && claude  # should auto-load context

   # Check council
   cd packages/cli-council && uv run python -m cli_council --check
   ```

## Starting a New Research Project

```
/init-project-research
```

This scaffolds the directory structure, creates the Overleaf symlink, initializes git, and creates seed files (CLAUDE.md, .context/, code/lib/).

## Typical Workflow

1. `/literature` — search for papers on your topic
2. `/reading-notes` — read and take notes on key papers
3. `/paper-draft` — write the paper section by section
4. `/experiment-runner` — run experiments and generate figures
5. `/replication-check` — verify all numbers match
6. `/bib-validate claims` — verify all citation claims are accurate
7. `/proofread` — quality check + AI pattern density scan
8. `/pre-submission-report` — full audit before submission
9. `/venue-research` — choose where to submit
10. `/progress-log` — record what was done for next session
