---
name: council
description: "Use when you need a multi-model review (Gemini + Claude) on any task — paper proofreading, code review, methodology critique, or any question where a second opinion adds value."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(uv*), Bash(cat*), Bash(mkdir*)
argument-hint: "[task description or 'proofread', 'review code', 'critique methodology']"
---

# Council — Multi-Model Deliberation

Send a task to both Gemini and Claude independently, cross-review their responses, and synthesize the best answer. Uses the `cli-council` package with your existing subscriptions (no API costs).

## When to Use

- Paper proofreading where you want a second set of eyes
- Methodology critique before submission
- Code review where different perspectives catch different bugs
- Any question where model diversity adds value
- "Get a second opinion", "council review", "ask Gemini too"

## Available Backends

- **Gemini 2.5 Pro** (via Gemini CLI)
- **Claude Sonnet 4.6** (via Claude Code)

## How It Works

1. Both models independently answer the same prompt
2. Each model reviews the other's answer (anonymized as "Assessment A/B")
3. A chairman (Claude) synthesizes the final answer

## Workflow

### Step 1: Build the Prompt

Based on what the user wants, construct a prompt file. Common patterns:

**Proofread a paper:**
```
Review this academic paper for: grammar, notation consistency, citation format,
academic tone, LaTeX issues, writing flow, and internal consistency.
For each issue found, report: location (file:line), severity (Critical/Major/Minor),
and a specific fix instruction.
```

**Review code:**
```
Review this Python research code for: reproducibility, structure, domain correctness,
duplicated logic, hardcoded paths, missing error handling, and test coverage.
```

**Critique methodology:**
```
Critique this research methodology. Check: are all assumptions stated? Do the
equations follow from the stated setup? Are there hidden assumptions? Does the
identification strategy actually identify what's claimed?
```

**General question:**
Use the user's prompt directly.

### Step 2: Build the Context

Gather the relevant content:
- For paper review: read all `.tex` files and concatenate
- For code review: read the target scripts
- For methodology: read the methodology section
- Save to a temp file

### Step 3: Invoke cli-council

```bash
cd packages/cli-council
uv run python -m cli_council \
    --prompt-file /tmp/council-prompt.txt \
    --context-file /tmp/council-context.txt \
    --output-md /tmp/council-result.md \
    --chairman claude \
    --timeout 180
```

Parameters:
- `--prompt-file`: the task/question
- `--context-file`: the paper/code/content to review (optional)
- `--output-md`: where to write the synthesized report
- `--chairman claude`: which model synthesizes (claude recommended)
- `--timeout 180`: seconds per backend (increase for large papers)

### Step 4: Present Results

Read `/tmp/council-result.md` and present to the user:
1. The synthesized answer (chairman's output)
2. Where the models agreed (high confidence findings)
3. Where they disagreed (worth investigating)
4. Any findings unique to one model (may be false positives or genuine catches the other missed)

### Step 5: Save Report (Optional)

If the user wants to keep the council output:
```
reviews/council/YYYY-MM-DD_<task>.md
```

## Quick Examples

**"Council proofread my paper"**
→ Read main.tex → write to context file → prompt = proofread instructions → run council → present issues

**"Council review my experiment code"**
→ Read code/experiments/*.py → write to context file → prompt = code review instructions → run council → present findings

**"Ask Gemini if our DRO formulation is correct"**
→ Read methodology section → write to context file → prompt = user's question → run council → present answer

## Notes

- Council takes ~20-30 seconds for short tasks, ~2-3 minutes for full paper reviews
- The 2-model setup (Gemini + Claude) is sufficient — adding Codex would require `npm install -g @openai/codex-cli` + ChatGPT Plus
- Council is most valuable for subjective tasks (proofreading, critique) where different models genuinely catch different things
- For objective tasks (math verification, number checking), a single model with `/domain-reviewer` or `/replication-check` is usually better
