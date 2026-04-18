---
name: init-project-research
description: "Use when you need to bootstrap a full research project with directory scaffold and Overleaf symlink."
allowed-tools: Bash(mkdir*), Bash(ln*), Bash(ls*), Bash(git*), Bash(touch*), Bash(uv*), Read, Write, Edit, Glob, Grep
argument-hint: "[project-name or no arguments for guided setup]"
---

# Init Project Research

Scaffolds a research project directory with the standard structure, Overleaf symlink, git init, and seed files.

## When to Use

- Starting a new research paper or project from scratch
- "New project", "set up a project", "init project"

## Setup Interview

Ask the user (keep it brief — 3-5 questions):

1. **Project name** — kebab-case slug for the directory (e.g., `my-research-project`)
2. **Working title** — full paper title
3. **Author** — name and affiliation
4. **Location** — where to create (default: `~/Desktop/<project-name>/`)
5. **Overleaf** — does the Overleaf project already exist? If yes, get the folder name under `~/Apps/Overleaf/`. If no, create it via `mkdir`.

## Directory Structure

Create this structure:

```
<project-name>/
├── CLAUDE.md              # Project instructions for Claude
├── MEMORY.md              # Notation, decisions, pitfalls
├── README.md              # Human-readable project overview
├── references.bib         # Master bibliography
├── pyproject.toml         # Python project config (uv)
├── .gitignore
├── .context/
│   ├── current-focus.md   # What's active NOW
│   └── project-recap.md   # Research design notes
├── code/
│   ├── lib/               # Shared modules
│   │   ├── __init__.py
│   │   ├── config.py      # Paths, constants, parameters
│   │   ├── data.py        # Data loading utilities
│   │   ├── solvers.py     # Core algorithms (fill as needed)
│   │   └── plotting.py    # Matplotlib style + helpers
│   ├── experiments/        # Experiment scripts
│   ├── eda/               # Exploratory data analysis
│   └── archive/           # Superseded scripts
├── data/
│   ├── raw/               # Original data (gitignored)
│   └── processed/         # Derived data (gitignored)
├── docs/
│   ├── readings/
│   │   └── notes/         # Paper reading notes by cluster
│   ├── explainers/        # Methodology walkthroughs
│   └── venue/             # CFP, templates, submission info
├── paper/
│   └── paper/             # Symlink → ~/Apps/Overleaf/<folder>
├── results/
│   └── figures/           # Generated figures
├── reviews/               # Audit reports
├── log/                   # Session logs
│   └── plans/             # Implementation plans
└── src/<package>/         # Python package (optional)
    └── __init__.py
```

## Seed Files

### CLAUDE.md

```markdown
# <Project Name> — Claude Instructions

## Project Overview

**Title:** <title>
**Author:** <author>
**Stage:** Initial setup

## Directory Structure

<tree from above>

## Safety Rules

- Never place code or data inside `paper/` — it syncs to Overleaf
- Design before results — lock research design before running experiments

## Setup

\`\`\`bash
cd <path>
uv sync
\`\`\`

## Conventions

### Python
- Package manager: `uv`
- Shared library: `code/lib/`

### LaTeX
- Source: `paper/paper/`
- Build: `latexmk -pdf main.tex`

## Session Recovery

1. `.context/current-focus.md`
2. `MEMORY.md`
3. Latest file in `log/`
```

### .gitignore

```
.DS_Store
__pycache__/
*.pyc
.venv/
uv.lock
*.aux
*.log
*.out
*.fls
*.fdb_latexmk
*.synctex.gz
out/
data/raw/
data/processed/
*.csv
*.xlsx
*.parquet
*.pkl
results/figures/*.png
results/figures/*.pdf
docs/readings/**/*.pdf
docs/readings/**/split_*
docs/venue/**/*.pdf
paper/paper/
.claude/state/
.env
```

### .context/current-focus.md

```markdown
# Current Focus — <Project Name>

> Last updated: <date>

## Status: Initial Setup

Project scaffolded. Next: define research questions and begin literature review.
```

### code/lib/config.py

```python
"""Project-wide configuration."""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = PROJECT_ROOT / "data" / "raw"
RESULTS_FIGURES = PROJECT_ROOT / "results" / "figures"
PAPER_FIGURES = PROJECT_ROOT / "paper" / "paper" / "figures"
RANDOM_SEED = 42
```

## Overleaf Symlink

```bash
ln -s ~/Apps/Overleaf/<folder-name> paper/paper
```

If the Overleaf folder doesn't exist, create it:
```bash
mkdir -p ~/Apps/Overleaf/<folder-name>
ln -s ~/Apps/Overleaf/<folder-name> paper/paper
```

## Git Init

```bash
cd <project-path>
git init
git add .
git commit -m "Initialize project: <title>"
```

## Python Setup

```bash
cd <project-path>
uv init --name <slug> --python 3.12
uv add numpy pandas matplotlib scipy
```

## Update Workspace Index

After creating the project, update the claude-research workspace:
- Add entry to `.context/projects/_index.md`
- Update `.context/current-focus.md` to reflect the new active project

## What NOT to Do

- Don't run literature review automatically (user will trigger when ready)
- Don't create presentation templates
- Don't set up CI/CD
