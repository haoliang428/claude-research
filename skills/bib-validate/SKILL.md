---
name: bib-validate
description: "Cross-reference \\cite{} keys against .bib files. Finds missing, unused, and typo'd keys. Deep mode verifies DOIs, metadata, and citation claims."
allowed-tools: Read, Glob, Grep, Write, Edit, Bash(mkdir*), Bash(ls*), Bash(curl*), Task, mcp__bibliography__scholarly_search, mcp__bibliography__scholarly_verify_dois, mcp__bibliography__scholarly_paper_detail
argument-hint: [project-path or tex-file]
---

# Bibliography Validation

Validates that every `\cite{}` key in the `.tex` files has a matching entry in `references.bib`, and that every `.bib` entry is accurate and complete.

## When to Use

- After adding new citations or bib entries
- Before compiling a final paper version
- As part of pre-submission checklist (pair with `/proofread`)
- When bibtex reports undefined citations

## Modes

### Standard Mode (default)
Read-only report. Finds:
- Missing keys (cited but not in .bib)
- Unused keys (in .bib but never cited)
- Possible typos (fuzzy match on near-miss keys)
- Incomplete entries (missing required fields: author, title, year, journal/booktitle)

### Deep Mode (`/bib-validate deep`)
Everything in standard mode, plus:
- DOI verification via `scholarly_verify_dois` with title matching
- Preprint staleness check (arXiv papers that now have published versions)
- Entry type correctness (@article vs @inproceedings vs @misc)
- Author name completeness (no "et al." in bib entries)

### Claim Mode (`/bib-validate claims`)
Everything in deep mode, plus:
- For each citation in the paper, check that the claim made about the cited paper is accurate
- Cross-reference against reading notes in `docs/readings/notes/` when available
- Flag potential misattributions (e.g., attributing a finding to a paper that makes a different argument)

Common examples: citing a single-site method as "spatial shifting", attributing an argument about X to a paper that actually argues about Y, or overstating a finding's scope.

## Workflow

### Step 1: Locate files

Find all `.tex` files and the `references.bib` in the project:
- Default bib: `references.bib` at project root or in `paper/paper/`
- Also check for any `.bib` referenced via `\bibliography{}` commands

### Step 2: Extract cite keys

Extract all `\cite{}`, `\citet{}`, `\citep{}`, `\citealt{}` keys from `.tex` files. Extract all `@type{key,` entries from `.bib` files.

### Step 3: Cross-reference

- **Missing:** keys in .tex not in .bib
- **Unused:** keys in .bib not in .tex
- **Typos:** Levenshtein distance ≤ 2 between a missing key and an existing key

### Step 4: Metadata validation (deep mode)

For each bib entry:
1. Check required fields are present (author, title, year, + journal or booktitle)
2. Check DOI exists and resolves correctly via `scholarly_verify_dois`
3. Check entry type matches venue (conference paper should be @inproceedings, not @article)
4. Check for preprint staleness: if entry has `eprint` or `archiveprefix = {arXiv}`, search for published version via `scholarly_search`
5. Check author field has no "et al."

### Step 5: Claim verification (claims mode)

For each `\cite` in the paper:
1. Read the surrounding sentence to understand what claim is attributed to the citation
2. Check `docs/readings/notes/` for the corresponding paper's notes
3. Verify the claim matches what the paper actually says
4. Flag misattributions with severity: CRITICAL (wrong paper), MAJOR (overstatement), MINOR (imprecise)

### Step 6: Report

Output a categorised report:

```
## Bibliography Validation Report

### Missing Keys (cited but not in .bib)
- \cite{smith2024xyz} — line 45 of main.tex

### Unused Keys (in .bib but not cited)
- jones2023abc

### Incomplete Entries
- doe2022def — missing: volume, pages

### DOI Issues (deep mode)
- lee2021ghi — DOI resolves to different title: "Expected Title" vs "Actual Title"

### Preprint Staleness (deep mode)
- wang2023jkl — arXiv version; published in Nature Energy (2024)

### Citation Claim Issues (claims mode)
- MAJOR: line 93 cites smith2024 for "spatial method" but Smith (2024) is a single-site approach
```

## Common Errors to Watch For

Common errors to watch for:
- Wrong authors (especially for arXiv papers with multiple versions)
- Garbled LaTeX in author names (encoding issues)
- Wrong pages (different across preprint vs published)
- Entry type mismatches (@article for arXiv preprints — should be @misc)
- Attributing an argument to the wrong paper (most common claim error)
