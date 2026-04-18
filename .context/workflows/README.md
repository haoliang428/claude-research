# Workflows Guide

> How to use the workflow files in this folder.

## What Are Workflows?

Workflows are step-by-step process guides for recurring tasks. They tell Claude how to help you with specific activities.

**Note:** Most capabilities are now in `skills/` instead — skills are more comprehensive and include prompt templates, while workflows are simpler process guides.

## Available Workflows

| Workflow | When to Use | Trigger Phrase |
|----------|-------------|----------------|
| `replication-protocol.md` | Replicating a paper's results | "Help me replicate [paper]" |

## Related Skills

These capabilities are in `skills/` folder (more comprehensive):

| Skill | When to Use | Trigger Phrase |
|-------|-------------|----------------|
| `code-archaeology/` | Revisiting old code | "Audit this codebase" |
| `literature/` | Literature search & synthesis | "Build a literature review on [topic]" |
| `experiment-runner/` | Running experiments | "Run the experiments" |

## How to Use

### Natural Language (Recommended)
Just ask naturally:

> "Help me replicate this paper's results"

### Direct Reference
Point to the specific workflow:

> "Read `.context/workflows/replication-protocol.md` and help me replicate"

## Tips

- **Workflows = processes** — Step-by-step guides for recurring tasks
- **Skills = capabilities** — Comprehensive instructions with templates
- **Combine as needed** — E.g., use code-archaeology skill with replication protocol
