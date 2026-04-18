# Council Mode (Gemini + Claude)

Multi-model deliberation using `cli-council`. Sends the same task to Gemini and Claude independently, cross-reviews, and synthesizes.

## How It Works

1. **Stage 1:** Gemini and Claude independently answer the same prompt
2. **Stage 2:** Each model reviews the other's answer (anonymized)
3. **Stage 3:** Chairman (Claude) synthesizes the final answer

## Prerequisites

- Gemini CLI installed and authenticated (`gemini` on PATH)
- Claude Code installed (`claude` on PATH)

Check availability:
```bash
cd packages/cli-council && uv run python -m cli_council --check
```

## Usage

### Via `/council` skill (recommended)
Just say "council proofread my paper" or "get a second opinion on this methodology."

### Via command line
```bash
cd packages/cli-council
uv run python -m cli_council \
    --prompt-file /tmp/prompt.txt \
    --context-file /tmp/context.txt \
    --output-md /tmp/result.md \
    --chairman claude \
    --timeout 180
```

## When Council Adds Value

- **Proofreading:** Different models catch different grammar/style issues
- **Methodology critique:** Models have different reasoning patterns
- **Code review:** Each may spot different bugs

## When to Skip Council

- **Math verification:** Use `domain-reviewer` agent instead
- **Number checking:** Use `/replication-check`
- **Simple tasks:** Council overhead (~30s) isn't worth it for quick questions
