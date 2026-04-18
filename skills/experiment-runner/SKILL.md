---
name: experiment-runner
description: "Use when you need to run experiments, generate publication figures, and update the paper with validated results."
allowed-tools: Read, Write, Edit, Bash(uv*), Bash(python*), Bash(mkdir*), Bash(ls*), Bash(cp*), Bash(latexmk*), Glob, Grep
argument-hint: "[experiment-script or 'all' to run full pipeline]"
---

# Experiment Runner

Orchestrates the experiment → figures → paper update pipeline. Ensures every number in the paper comes from actual experiment output.

## When to Use

- Running experiments for a paper (sensitivity analyses, baseline comparisons, etc.)
- Regenerating figures after code changes
- Updating the paper text with validated numbers from experiment output
- "Run the experiments", "generate figures", "update the paper with real numbers"

## Workflow

### Step 1: Identify What to Run

Read the paper's methodology and results sections to determine:
- Which experiments are described but not yet run
- Which numbers in the text need validation
- Which figures need to be generated or regenerated

Check `code/experiments/` for existing scripts and `results/figures/` for existing outputs.

### Step 2: Write or Update Experiment Script

If the experiment script doesn't exist, write it following the project's `code/lib/` pattern:

```python
# Import from shared library
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.config import *
from lib.data import load_moer, load_latency_matrix, build_feasibility_mask, load_demand_profile
from lib.solvers import dispatch_lp, dispatch_dro
from lib.plotting import apply_style, save_figure, COLORS, LABELS
```

Script requirements:
- Use `uv` inline dependencies (`# /// script` header)
- Import from `code/lib/` for shared functions (data loading, solvers, plotting)
- Save results to JSON in `results/` for reproducibility
- Save figures as both PDF (for paper) and PNG (for reference) to `paper/paper/figures/` and `results/figures/`
- Print summary statistics to stdout
- Set random seed from `config.RANDOM_SEED`

### Step 3: Run Experiments

```bash
cd <project-root>
uv run code/experiments/<script>.py
```

For long-running experiments, use `run_in_background: true` and monitor progress.

If multiple independent experiments are needed (e.g., sensitivity at different parameter values), write them as a single script with a loop, not separate scripts.

### Step 4: Capture Results

After the script completes:
1. Read stdout for summary statistics
2. Read the JSON results file for detailed numbers
3. Verify figures were saved to both output directories

### Step 5: Update Paper Text

For each quantitative claim in the paper:
1. Find the corresponding number in the experiment output
2. Update the LaTeX with the exact number (no rounding beyond what the paper reports)
3. Update figure captions if the figures changed

Common patterns:
- `+12.6\%` → verify against `results["B3"]["savings_pct"]`
- Sensitivity ranges → verify against the sweep results
- Seasonal/temporal breakdowns → verify against per-period results

### Step 6: Compile and Verify

```bash
cd paper/paper && latexmk -pdf main.tex
```

Check:
- All figures appear in the correct location (no float drift past sections)
- No warnings about undefined references
- Page count is within limits

### Step 7: Save Results JSON

Always save experiment results to a JSON file for future reference:

```python
import json
results = {"main_results": {...}, "sensitivity": {...}}
with open("paper/paper/figures/experiment_results.json", "w") as f:
    json.dump(results, f, indent=2)
```

This creates an audit trail: any number in the paper can be traced back to this file.

## Figure Quality Checklist

Publication-quality figures should have:
- Readable font size (11pt minimum)
- Axis labels with units
- Legend that doesn't overlap data
- Consistent colour scheme across all figures (use `code/lib/plotting.py` colours)
- Saved as PDF (vector) for the paper, PNG for reference
- Caption that is self-contained

## Common Pitfalls

- **Y-axis labels**: Never use "arb. units". Use the actual unit, even if it's complex.
- **Missing baselines in sensitivity plots**: If the paper compares 5 methods, all 5 should appear in every figure (not just 2).
- **Hardcoded paths**: Use `config.PROJECT_ROOT` from `code/lib/config.py`, not absolute paths.
- **Duplicated solvers**: Import from `code/lib/solvers.py`, don't copy-paste solver functions into each script.
