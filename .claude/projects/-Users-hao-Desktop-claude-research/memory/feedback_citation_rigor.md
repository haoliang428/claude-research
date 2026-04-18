---
name: Citation and bibliography rigor
description: Always verify citations against source material before submission — Hao expects 100% accuracy
type: feedback
---

During the ai-energy-ot paper, citation verification found 8 inaccurate claims and 8 bibliography errors. Hao expects thorough verification before presenting a draft as complete.

**Rule:** Before claiming a section is done, verify every citation against the actual paper or reading notes. Check:
1. Does the claim accurately represent what the cited paper actually found?
2. Are author names, title, year, venue, DOI correct in the bib entry?
3. Is the entry type (@article vs @inproceedings vs @misc) correct?
4. Are arXiv preprints that have been published updated to the published version?

**Common errors to watch for:**
- Attributing an argument to a paper that makes a different (related) argument (e.g., Bashir 2024 argues operational vs lifecycle, not marginal vs average)
- Calling a single-site method "spatial shifting" (e.g., Clover)
- Wrong application domain in parenthetical summaries (e.g., "portfolio optimisation" when the paper is about two-stage stochastic programming)
- Garbled LaTeX in author names
- Stale arXiv metadata (wrong title/authors from an earlier version)

**Why:** A single misattributed citation can get flagged by a reviewer who knows the paper, undermining credibility.

**How to apply:** Use the paper-critic and domain-reviewer agents. For critical papers (>5 citations in our manuscript), read the actual notes file, not just the bib entry.
