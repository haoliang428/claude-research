---
name: literature
description: "Use when you need academic literature discovery, synthesis, or bibliography management."
allowed-tools: Bash(curl*), Bash(mkdir*), Bash(ls*), Bash(uv*), Read, Write, Edit, WebSearch, WebFetch, Task, mcp__bibliography__scholarly_search, mcp__bibliography__scholarly_paper_detail, mcp__bibliography__scholarly_citations, mcp__bibliography__scholarly_references, mcp__bibliography__scholarly_similar_works, mcp__bibliography__scholarly_author_papers, mcp__bibliography__scholarly_verify_dois, mcp__bibliography__scholarly_source_status
argument-hint: [topic-or-paper-query]
---

# Literature Skill

## Core Rules

1. **Every citation must be verified to exist.** Never include a paper you cannot find via MCP or web search. Hallucinated citations are worse than no citations.
2. **Every DOI must be verified before entering a `.bib`.** Use `scholarly_verify_dois` with title-matching. A DOI that resolves to a different title is WRONG.
3. **Prefer published versions over preprints.** If found on arXiv/SSRN, search for the published version first.
4. **Match existing citation key format.** Check the project's `references.bib` and follow its convention (e.g., `lastname2020keyword`).
5. **List ALL authors in BibTeX.** Never "et al." in metadata.
6. **Verify claims, not just existence.** When a paper is cited for a specific finding, confirm that finding is actually in the paper (see Phase 4).

## When to Use

- Starting a literature review for a new project
- Finding papers on a specific topic or to support a specific claim
- Building or expanding a `references.bib`
- Synthesising a field overview

## Workflow

```
Phase 1: Check what exists (references.bib, docs/readings/notes/)
Phase 2: Search (MCP bibliography + WebSearch, parallel queries)
Phase 3: Deduplicate, rank, select candidates
Phase 4: Verify (DOIs, metadata, claims)
Phase 5: Download PDFs + write reading notes
Phase 6: Update references.bib
Phase 7: Synthesise (if writing a lit review section)
```

## Phase 1: Check What Exists

Before searching externally:

1. Read `references.bib` at the project root — note existing keys and coverage gaps
2. Scan `docs/readings/notes/` — which papers already have reading notes?
3. Check `scholarly_source_status` to see which MCP sources are active

This prevents re-discovering papers already in the project.

## Phase 2: Search

Use the bibliography MCP tools from the main context. Run multiple searches in parallel:

1. **`scholarly_search`** — primary tool. Run 2-4 queries with different keyword angles for the same topic. Use `year`, `min_citations`, and `show_abstracts` parameters to filter.
2. **`scholarly_similar_works`** — pass a description of the topic to find semantically related papers beyond keyword matches.
3. **`scholarly_author_papers`** — if key authors are known, fetch their publication lists.
4. **`scholarly_citations` / `scholarly_references`** — snowball from seed papers (forward and backward citation tracking).
5. **WebSearch** — supplement for very recent papers, working papers, or topics with non-standard terminology.

Run searches in parallel where possible. For a typical literature review (20-40 papers), run 4-6 `scholarly_search` queries covering different facets of the topic.

## Phase 3: Deduplicate and Rank

1. Merge results from all searches
2. Remove duplicates (match on title similarity)
3. Rank by relevance to the research question, citation count, and recency
4. Select top N candidates (typically 20-30 for a full review, 5-10 for targeted search)

Present the ranked list to the user for approval before proceeding.

## Phase 4: Verify

For each selected paper:

1. **DOI verification** — call `scholarly_verify_dois` on all DOIs. Check that the returned title matches. For any mismatch, use Crossref API: `curl -sL "https://api.crossref.org/works?query.bibliographic=[title+author]&rows=3"`
2. **Metadata check** — confirm authors, year, venue, volume, pages via `scholarly_paper_detail`
3. **Preprint check** — if the entry is arXiv/SSRN, search for a published version via `scholarly_search` with the exact title
4. **Claim verification** — if the paper is being cited for a specific claim (e.g., "X finds that Y"), read the paper notes or abstract to confirm the claim is accurate. This is the most important step. See the citation rigor memory for common errors.

## Phase 5: Download and Read

For papers that need reading notes:

1. Download PDFs to `docs/readings/cluster-N/` (organised by topic cluster)
2. Use `/split-pdf` for papers longer than ~15 pages
3. Write structured reading notes to `docs/readings/notes/cluster-N/authorYEAR-notes.md`

Reading notes should extract (per the split-pdf skill):
- Research question, method, data, key results
- Assumptions and limitations
- Relevance to our project
- Gaps this paper leaves open
- Follow-up citations worth pursuing

## Phase 6: Update references.bib

Add verified entries to the project's `references.bib`:

```bibtex
@article{lastname2020keyword,
  title     = {Full Title},
  author    = {Last, First and Last, First},
  journal   = {Journal Name},
  volume    = {XX},
  pages     = {1--20},
  year      = {2020},
  doi       = {10.1000/example},
}
```

Rules:
- Match the citation key convention already in the `.bib` file
- List all authors explicitly
- Include DOI for every entry (flag `% NO DOI` for pre-DOI papers)
- Use correct entry types: `@article` for journals, `@inproceedings` for conferences, `@misc` for arXiv preprints
- After adding entries, run `/bib-validate` to catch formatting issues

If the paper directory has a separate copy (`paper/paper/references.bib`), sync it: `cp references.bib paper/paper/references.bib`

## Phase 7: Synthesise (Optional)

When writing a literature review section for a paper:

1. Group papers by theme, not by paper — write about the field, not individual papers
2. Use transition sentences between themes, not subsection headers
3. Identify the specific gap your work fills
4. End with a comparison table that systematically positions your contribution against prior work

For a quick field synthesis (~400 words), structure as:
1. What the field collectively believes (consensus)
2. Where researchers disagree (active debates)
3. What has been proven (strong evidence)
4. The key unanswered question (gap)

## Output Structure

```
project/
├── docs/
│   └── readings/
│       ├── cluster-N/           # PDFs by topic cluster
│       └── notes/cluster-N/     # Reading notes per paper
├── references.bib               # Master bibliography
└── paper/paper/references.bib   # Copy for Overleaf
```

## Cross-References

| Skill | When to use |
|-------|-------------|
| `/split-pdf` | Deep-read a paper found during search |
| `/bib-validate` | After adding entries to `.bib` |
| `/proofread` | After writing a lit review section |
