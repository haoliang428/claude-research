---
name: paper-draft
description: "Use when you need to write or revise a section of an academic paper. Guides section-by-section drafting with quality conventions."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(latexmk*), mcp__bibliography__scholarly_search
argument-hint: "[section-name or 'full' for complete draft]"
---

# Paper Draft

Guide the writing of academic paper sections with consistent quality conventions.

## When to Use

- Writing a new paper section (methodology, results, introduction, etc.)
- Revising an existing section based on feedback
- "Write the methodology section", "draft the introduction", "revise the results"

## Writing Order

For a new paper, write sections in this order (methodology first, abstract last):

1. **Methodology** — the backbone; write this before anything else
2. **Results / Experiments** — flows directly from methodology
3. **Introduction** — easier to write once you know what you're claiming
4. **Literature Review** — position against the results you have
5. **Conclusion** — summarize contributions, limitations, future work
6. **Abstract** — last, once the paper is fully shaped

## Writing Conventions

### Structure
- Use `\section` for top-level structure (Introduction, Literature Review, Methodology, Experiments, Conclusion)
- Use `\subsection` only in Methodology where cross-references require labels
- Everywhere else, connect topics with transition sentences, not subsection headers
- No `\paragraph` headers — integrate into flowing prose

### Prose Style
- **No bullet-point findings.** Present results as flowing paragraphs in both intro and results
- **No boilerplate.** No "The remainder of the paper is organised as follows" unless the structure is non-standard
- **No "to our knowledge" claims.** Cite the relevant review paper and state the gap factually
- **No stylistic italics.** Keep `\emph` only for constraint/item labels in enumerations
- **Minimal em-dashes.** Use only where they do real structural work (~1 per 4 pages). Prefer commas, colons, parentheses, or sentence breaks
- **No abstract/intro duplication.** The intro should add depth and implications, not restate the same numbers

### Content
- **Every assumption needs evidence.** Either cite a source or honestly state it's an assumption with a sentence on why it doesn't affect conclusions
- **Every quantitative claim needs a source.** Either an experiment result, a cited paper, or a data source
- **Results preview in intro should be brief** (2-3 sentences with headline numbers only). Detailed analysis belongs in the Results section
- **Literature review should flow as a narrative**, not a list of paper summaries. Write about the field, not individual papers. End with a comparison/gap table

### Figures and Tables
- Generate figures from experiment code, save as PDF to `paper/paper/figures/`
- Every figure must be referenced in the text before it appears
- Captions should be self-contained (a reader should understand the figure from the caption alone)
- Use `\FloatBarrier` before sections to prevent figures from drifting past section boundaries
- **Verify text after figure updates.** After regenerating any figure, re-read every text reference, caption, and number that cites it. Stale references are a common source of reviewer complaints.

## Section Templates

### Introduction (~1.5 pages)
1. Problem and why it matters (with scale/impact citations)
2. The opportunity (what makes the problem tractable)
3. The gap (what existing approaches miss, with specific evidence from a review paper)
4. Our approach (1 paragraph on the method)
5. Results preview (2-3 sentences, headline numbers only)

### Literature Review (~2 pages)
1. Start with the closest work and trace the trajectory
2. Connect topics with transitions, not subsection headers
3. For each major paper: what they did, what they found, what limitation they left
4. End with a gap table positioning your contribution across multiple criteria

### Methodology (~4-5 pages)
1. Problem setting (data, fleet, constraints — with evidence for each assumption)
2. Core formulation (equations, decision variables, objective, constraints)
3. Extensions (robustness, temporal, etc.)
4. Each subsection should connect to the next with a motivation sentence

### Results (~4-5 pages)
1. Baselines table (what each baseline does, with references and parameter values)
2. Main results (flowing prose, not bullet points)
3. Sensitivity analyses (connect each to a specific assumption or design choice)
4. Figures integrated with text (not dumped at the end)

### Conclusion (~1 page)
1. Contributions (3 paragraphs, each starting with "First/Second/Third")
2. Limitations (honest, specific, with citations where others have noted the same issue)
3. Future work (concrete extensions that flow from the limitations)

## After Writing Each Section

1. Compile with `latexmk -pdf` to check for errors
2. Verify all `\ref` and `\cite` resolve
3. Check the section reads smoothly when read aloud (no abrupt transitions)
4. Verify every quantitative claim has a source
