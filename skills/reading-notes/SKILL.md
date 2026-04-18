---
name: reading-notes
description: "Use when you need to write structured reading notes for an academic paper. Works with PDFs, MCP search results, or papers already in the project."
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Bash(uv*), Bash(mkdir*), mcp__bibliography__scholarly_search, mcp__bibliography__scholarly_paper_detail
argument-hint: "[paper-title, citation-key, or pdf-path]"
---

# Reading Notes

Write structured reading notes for an academic paper and save them to the project's `docs/readings/notes/` directory.

## When to Use

- After finding a paper via `/literature` that needs deeper reading
- When reading a paper for the first time and want to capture key information
- When building notes for a literature review section
- When verifying a citation claim against the actual paper

## Input

One of:
- A paper title or search query (will find via MCP or web)
- A citation key from `references.bib` (will look up metadata)
- A path to a local PDF (will use `/split-pdf` if needed)

## Workflow

### Step 1: Locate the Paper

- If citation key: look up in `references.bib` for metadata (title, authors, year, DOI)
- If title/query: search via `scholarly_search` or `scholarly_paper_detail` for metadata
- If PDF path: extract metadata from filename or first page

### Step 2: Determine Reading Method

- **Short paper (<15 pages)**: Read the PDF directly via the Read tool
- **Long paper (>15 pages)**: Use `/split-pdf` to split and read in batches
- **No PDF available**: Use abstract + `scholarly_paper_detail` TLDR + WebSearch for summaries. Flag as "notes from metadata only — full paper not read"

### Step 3: Write Structured Notes

Save to `docs/readings/notes/<cluster>/<authorYEAR-keyword-notes>.md`

If no cluster structure exists yet, save to `docs/readings/notes/`.

Template:

```markdown
# <Paper Title>

**Authors:** <full author list>
**Year:** <year>
**Venue:** <journal or conference, volume, pages>
**DOI:** <doi>
**File:** <path to PDF if available>

---

## Core Contribution

<1-2 sentences: what is the main thing this paper does?>

## Problem Setup

<What problem are they solving? What setting? What constraints?>

## Methods

<How do they solve it? Key equations, algorithms, or approaches.>

## Key Results

<Main findings with specific numbers where possible.>

## Assumptions & Limitations

<What do they assume? What are the explicit and implicit limitations?>

## Relevance to Our Project

<How does this paper relate to the current research project? What can we use, cite, or build on?>

## Gap This Paper Leaves Open

<What doesn't this paper address that we could? This is where our contribution fits.>

## Follow-up Citations

<Papers referenced here that are worth reading next.>
```

### Step 4: Update references.bib

If the paper isn't already in `references.bib`, add it with correct metadata (verify DOI via `scholarly_verify_dois` if available).

## Notes Quality Checklist

Good reading notes should contain:
- Specific numbers (sample size, effect size, performance metrics)
- Exact method names (not "they use machine learning" but "they use a two-stage Wasserstein DRO with N=168 scenarios")
- Explicit assumptions (stated and unstated)
- At least one concrete gap that connects to our work
- At least one follow-up citation worth pursuing

Bad reading notes are:
- Paraphrased abstracts
- Vague summaries ("they find interesting results")
- Missing the limitations section
- No connection to our project

## Batch Mode

When reading multiple papers (e.g., for a literature review), work through them in order:

1. Read and write notes for each paper
2. After every 3-5 papers, look for emerging themes and connections
3. Note which papers cite each other and where they disagree
4. Update the "Relevance" section as the picture becomes clearer

## Cross-References

| Skill | When to use |
|-------|-------------|
| `/split-pdf` | For papers >15 pages that need page-by-page reading |
| `/literature` | For finding papers to read |
| `/bib-validate` | After adding new entries to references.bib |
