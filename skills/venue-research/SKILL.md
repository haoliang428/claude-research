---
name: venue-research
description: "Use when you need to research target journals for a paper submission. Compares IF, acceptance rate, review speed, scope fit, and formatting requirements."
allowed-tools: Read, Write, Edit, WebSearch, WebFetch, Glob, Grep, mcp__bibliography__scholarly_search
argument-hint: "[paper-topic or path-to-main.tex]"
---

# Venue Research

Research and compare target journals for a paper. Produces a ranked comparison table with actionable recommendations.

## When to Use

- Paper draft is near-complete and you need to choose where to submit
- Exploring venue options early to shape the paper's framing
- After a rejection, identifying the next best venue

## Input

Either:
- A description of the paper's topic and methodology
- A path to the paper's `.tex` file (will extract topic from abstract/title)

## Workflow

### Step 1: Understand the Paper

Read the abstract, introduction, and methodology to identify:
- **Primary discipline** (energy, OR, CS, sustainability, finance, etc.)
- **Methodology type** (optimization, ML, empirical, theoretical, simulation)
- **Application domain** (datacenters, power systems, transportation, etc.)
- **Key contribution** (new method, new application, empirical finding, framework)

### Step 2: Generate Candidate List

Based on the paper's profile, search for 10-15 candidate journals across:
- **Core discipline journals** (highest fit)
- **Cross-disciplinary journals** (broader audience)
- **Methods-focused journals** (if the methodology is the main contribution)
- **Applied/domain journals** (if the application is the main contribution)

For each candidate, search via WebSearch for:
- Impact Factor (latest, from JCR or Scopus)
- Acceptance rate (from LetPub, SciRev, or journal website)
- Average review time (first decision, from LetPub or SciRev)
- Total time to publication
- Scope description
- Page/word limits
- APC (if open access)

### Step 3: Assess Fit

For each candidate, evaluate:
- **Scope fit** (1-5): Does the paper's topic fall within the journal's stated scope?
- **Methodology fit** (1-5): Does the journal publish papers with this type of method?
- **Audience fit** (1-5): Would the journal's readers care about this contribution?
- **Changes needed**: What would need to change in the draft? (None / Minor reframing / Moderate / Major rewrite)

### Step 4: Output Comparison Table

```markdown
## Venue Comparison

| # | Journal | IF | Q | Accept Rate | First Decision | Scope Fit | Changes Needed |
|---|---------|-----|---|------------|----------------|-----------|----------------|
| 1 | ... | ... | ... | ... | ... | High/Med/Low | None/Minor/Moderate/Major |
```

### Step 5: Recommendation

Rank the top 3 venues by strategy:

- **High IF + good fit**: Best for career impact
- **Fastest turnaround**: Best if time-sensitive
- **Highest acceptance rate**: Best for first publication or if the paper has known weaknesses

For each top-3 venue, write 2-3 sentences on what specifically would need to change in the draft (framing, additional experiments, different emphasis, formatting).

## Key Data Sources

- **LetPub** (letpub.com): Acceptance rate, review speed, user reviews
- **SciRev** (scirev.org): Peer-reported review experiences
- **SCImago** (scimagojr.com): SJR rankings, quartiles
- **Journal websites**: Scope, submission guidelines, page limits
- **Academic Accelerator**: Acceptance rates, review speed

## Important Notes

- Never recommend one-稿多投 (simultaneous submission to multiple journals). Always submit to one venue at a time.
- Elsevier journals allow transfer between sister journals with reviewer comments, which can speed up resubmission after rejection.
- Impact factors change yearly — always search for the latest available.
- Acceptance rates are estimates and vary by source. Use them as rough guides, not precise numbers.
