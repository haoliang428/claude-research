---
name: proofread
description: "Use when you need academic proofreading of a LaTeX paper (14 check categories)."
allowed-tools: Read, Glob, Grep
argument-hint: [project-path or tex-file]
---

# Academic Proofreading

**Report-only skill.** Never edit source files — produce `PROOFREAD-REPORT.md` only.

## When to Use

- Before sending a draft to supervisors
- Before submission to a journal/conference
- After major revisions to check consistency
- When you want a fresh-eyes check on writing quality

## When NOT to Use

- **Formal audits** — use the Referee 2 agent for systematic verification
- **Argument quality** — use `/devils-advocate` for logical scrutiny
- **Citation completeness** — use `/bib-validate` for bibliography cross-referencing (though this skill flags obvious citation format issues)

## Workflow

1. **Locate files**: Find all `.tex` files in the project (and `.log` files for LaTeX diagnostics)
2. **Read the document**: Read all `.tex` source files in order
3. **Run 14 check categories** (below)
4. **Produce report**: Write `YYYY-MM-DD_PROOFREAD-REPORT.md` in `reviews/proofread/` under the project directory (create the directory if it does not exist). Do NOT overwrite previous reports — each review is dated.

## Check Categories

### 1. Grammar & Spelling

- Spelling errors (including technical terms)
- Subject-verb agreement
- Sentence fragments or run-ons
- Misused words (e.g., "effect" vs "affect", "which" vs "that")
- American English is the default for all papers and conference articles. Flag any British English spellings (e.g., -ise, -our, -re, analyse, scepticism).

### 2. Notation Consistency

- Variable notation used consistently throughout (e.g., always `$x_i$` or always `$x_{i}$`, not both)
- Subscript/superscript style (e.g., `$\beta_1$` vs `$\beta_{OLS}$`)
- Matrix/vector formatting conventions (bold, uppercase, etc.)
- Consistent use of `\mathbb`, `\mathcal`, `\mathbf` for sets, operators, vectors
- Equation numbering: all referenced equations numbered, unreferenced ones unnumbered

### 3. Citation Format

- Consistent use of `\citet` (textual) vs `\citep` (parenthetical)
- No raw `\cite{}` when `\citet`/`\citep` is available
- Author name spelling matches between text mentions and citation keys
- Multiple citations in chronological or alphabetical order (check which convention)
- No "As shown by (Author, Year)" — should be "As shown by \citet{key}"

### 4. Academic Tone

- No informal contractions (don't, can't, won't → do not, cannot, will not)
- No first-person overuse (some "we" is fine; excessive "I think" is not)
- No casual hedging ("pretty much", "kind of", "a lot")
- Appropriate use of hedging language ("suggests" vs "proves")
- No exclamation marks in body text
- Consistent tense (present for established facts, past for specific studies)

### 5. LaTeX-Specific Issues

- **Overfull hbox**: Check `.log` file for `Overfull \hbox` warnings — report line numbers and severity (badness)
- **Equation overflow**: Long equations that exceed column/page width
- **Float placement**: Check for `[h!]` or `[H]` overuse; prefer `[tbp]`
- **Missing labels**: Figures/tables/equations referenced but without `\label{}`
- **Orphan/widow lines**: Check for `\\` abuse that creates bad page breaks
- **Unresolved references**: `??` in output indicating broken `\ref{}` or `\cite{}`

### 6. Citation Voice Balance

Check the ratio of in-line (`\citet`) to parenthetical (`\citep`) citations:

- **Count in-line vs parenthetical citations** across the full document
- **Flag if ratio exceeds 1:1** (in-line should be the minority) — Major
- **Flag runs of 3+ consecutive in-line citations** in a paragraph or section — Major
- **Flag paragraphs that open with an in-line citation** when the author's identity isn't the point — Minor
- **Flag "As shown by \citet{}" patterns** where parenthetical would be more natural — Minor
- **Report the overall ratio** (e.g., "42 parenthetical, 28 in-line — ratio 1.5:1")

See `docs/conventions.md` § Citation Voice Balance for the full convention.

### 7. TikZ Diagram Review

If the document contains TikZ code (`\begin{tikzpicture}` or `\tikz`):

- **Label positioning**: Labels not overlapping nodes or edges
- **Geometric accuracy**: Coordinates and angles consistent with intended layout
- **Visual semantics**: Arrow styles match meaning (solid = direct, dashed = indirect, etc.)
- **Spacing**: Nodes not too cramped or too spread out
- **Consistency**: Style matches across all diagrams in the document
- **Standalone compilability**: Each diagram should compile independently

For detailed spatial verification (Bezier depth calculations, gap minimums, shape boundary clearance), see [`../shared/tikz-rules.md`](../shared/tikz-rules.md).

### 8. Numeric Text↔Table Cross-Check

Cross-check every number mentioned in the prose against the corresponding table or figure. Flag ANY discrepancy, no matter how small.

- **Coefficient claims**: "a 3.2 percentage point increase" in text vs coefficient of 0.031 in the table — flag the mismatch
- **Sample sizes**: "N = 1,247" in text vs N row in table — must match exactly
- **Significance claims**: "statistically significant at the 5% level" in text vs the actual stars/p-value in the table
- **Summary statistics**: means, medians, standard deviations mentioned in prose must match the descriptive statistics table
- **Figure references**: claims about trends or magnitudes must be consistent with what the figure shows
- **Table/figure existence**: every table/figure referenced in text must exist; every table/figure in the document must be referenced in text
- **N consistency**: the number of observations should be consistent across related specifications unless there's an explained reason for differences

### 9. Causal Language Audit

Audit causal claims against the stated identification strategy. The strength of causal language must match the strength of the research design.

- **Flag "X causes Y"** or "the causal effect of X" when the identification strategy is observational (OLS with controls, correlational) — should be "is associated with" or "predicts"
- **Flag "proves"** — almost never appropriate; use "provides evidence consistent with"
- **Match language to design**:
  - DiD/RDD/IV → "we estimate the causal effect" is acceptable with qualifiers
  - OLS with controls → "we find a relationship" or "our estimates suggest"
  - Correlational → never use causal language
- **Flag "significant" ambiguity** — must always be clear whether "statistically significant" or "economically meaningful/large"
- **Flag coefficient descriptions without units or scale** — "a coefficient of 0.031" means nothing without knowing the units of X and Y
- **Flag correlation/causation conflation** — any statement that slides from an association to a causal claim without an identification argument

### 10. Equation Completeness

Verify that mathematical notation is complete and internally consistent.

- **Every variable in an equation must be defined** in the text (either before or immediately after the equation)
- **Error terms**: properly specified (ε_it vs u_i vs e_ij) and consistent with the econometric framework described
- **Equation numbering**: sequential, and all cross-references to equations are correct
- **Subscript/index structure must match the level of observation** — e.g., if the text describes individual-level variation, the equation should have individual subscripts, not county-level
- **Summation/expectation indices**: verify bounds match the described sample
- **Consistent notation across equations**: don't switch between β and b for the same coefficient, or between X_i and x_i

### 11. Preprint Staleness

For every citation that looks like a preprint or working paper, check whether a peer-reviewed version has since been published. Flag stale preprints as Major issues.

- **Detection signals**: URL contains `arxiv.org`, `ssrn.com`, `nber.org`; journal field says "Working Paper", "mimeo"; entry type is `@techreport` or `@unpublished`
- **Action**: note the stale citation and suggest the published venue/year
- **This is a lighter version of `/bib-validate`'s preprint check** — only flag obvious cases visible from the `.bib` or `\bibitem` entries. For thorough preprint checking, recommend running `/bib-validate` separately.

### 12. Abbreviation Completeness

Scan the entire document for abbreviations (2+ uppercase letters used as a word) and verify each is defined at first use.

- **Grep for all-caps tokens** (LP, DRO, MOER, SLO, RTT, MILP, CDN, etc.) and check each has "(Full Name)" before its first occurrence
- **Abstract and body are separate scopes** — abbreviations defined in the abstract should be re-defined at first body use
- **Table-only abbreviations** (e.g., SA in a comparison table) can be defined in the table footnote
- **Remove redundant re-definitions** — define once, use thereafter; don't re-expand in later sections
- **Common misses**: abbreviations introduced in the literature review for other papers' methods, then used later without definition

### 13. Inline Sub-Header Audit

Check for `\emph{Title.}` or `\emph{Title:}` patterns used as paragraph-opening sub-headers. These should be rewritten as flowing prose transitions.

- **Flagged pattern**: `\emph{Word(s).} Sentence continues...` at the start of a paragraph
- **Acceptable**: `\item \emph{Label.}` inside enumerations (constraint/item labels)
- **Acceptable**: `\emph{word}` for emphasis of a single word mid-sentence
- **Fix**: rewrite with a transition sentence (e.g., `\emph{What limits B3?}` → "Despite these gains, B3 captures only a fraction of the theoretical maximum.")

### 14. Unfulfilled Forward References

Scan for forward references ("we discuss in Section X", "as we show below", "we report in the following section") and verify the promise is fulfilled.

- **Grep for**: "we discuss", "we show in", "we report", "as noted in Section", "we describe in", "we analyze in"
- **For each match**: follow the reference and verify the content actually exists in the target section
- **Flag as Major**: any forward reference that points to content that doesn't exist
- **Common pattern**: early sections promise analysis that was planned but never written, or was cut during revision

## Severity Levels

| Level | Definition | Example |
|-------|-----------|---------|
| **Critical** | Will be noticed by reviewers, may cause rejection | Broken references, major grammar errors, inconsistent core notation, text↔table number mismatch, causal overclaiming with weak design |
| **Major** | Noticeable quality issue | Inconsistent citation style, tone issues, overfull hbox > 10pt, undefined variable in equation, stale preprint, ambiguous "significant" |
| **Minor** | Polish issue | Occasional British/American mix, minor spacing, missing equation number for referenced equation |

## Quality Scoring

Apply numeric quality scoring using the shared framework and skill-specific rubric:

- **Framework:** [`../shared/quality-scoring.md`](../shared/quality-scoring.md) — severity tiers, thresholds, verdict rules
- **Rubric:** [`references/quality-rubric.md`](references/quality-rubric.md) — issue-to-deduction mappings for this skill

Start at 100, deduct per issue found, apply verdict. Insert the Score Block into the report after the summary table.

## Report Format

```markdown
# Proofread Report

**Document:** [filename]
**Date:** YYYY-MM-DD
**Pages:** [approximate]

## Summary

| Category | Critical | Major | Minor |
|----------|----------|-------|-------|
| Grammar & spelling | 0 | 0 | 0 |
| Notation consistency | 0 | 0 | 0 |
| Citation format | 0 | 0 | 0 |
| Academic tone | 0 | 0 | 0 |
| LaTeX-specific | 0 | 0 | 0 |
| Citation voice balance | 0 | 0 | 0 |
| TikZ diagrams | 0 | 0 | 0 |
| Numeric cross-check | 0 | 0 | 0 |
| Causal language | 0 | 0 | 0 |
| Equation completeness | 0 | 0 | 0 |
| Preprint staleness | 0 | 0 | 0 |
| Abbreviation completeness | 0 | 0 | 0 |
| Inline sub-headers | 0 | 0 | 0 |
| Unfulfilled references | 0 | 0 | 0 |
| **Total** | **0** | **0** | **0** |

## Critical Issues

[List each with file, line/section, and specific issue]

## Major Issues

[List each with file, line/section, and specific issue]

## Minor Issues

[List each with file, line/section, and specific issue]

## Quality Score

| Metric | Value |
|--------|-------|
| **Score** | XX / 100 |
| **Verdict** | Ship / Ship with notes / Revise / Revise (major) / Blocked |

### Deductions

| # | Issue | Tier | Deduction | Category |
|---|-------|------|-----------|----------|
| 1 | [description] | [tier] | -X | [category] |
| | **Total deductions** | | **-XX** | |

## Recommendations

[Optional: overall observations about the writing — prioritise fixes by deduction size]
```

## Writing Style Checks

In addition to the standard categories, check for these style issues (per user preference):

- **No bullet-point findings in Introduction** — results should be flowing prose
- **Minimal em-dashes** — only where they do real structural work (~1 per 4 pages)
- **No boilerplate** — no "The remainder of the paper is organized as follows"
- **No "to our knowledge" claims** — cite the gap factually instead
- **No stylistic italics** — keep \emph only for constraint/item labels in enumerations
- **Flowing transitions** — sections should connect with transition sentences, not fragment with subsection headers (except Methodology where cross-references require labels)
- **No abstract/intro duplication** — intro should add depth, not restate same numbers

## AI Pattern Density Check

After proofreading, run the AI pattern density scanner on the paper to check if it reads too "AI-generated":

```bash
uv run python skills/proofread/ai_pattern_density.py paper/paper/main.tex
```

Thresholds (patterns per 100 words):
- < 0.5: Excellent (indistinguishable from human)
- 0.5–1.0: Good (minor patterns)
- 1.0–2.0: Caution (may flag detectors)
- \> 2.0: Rewrite needed

If density is above 1.0, identify the flagged patterns and rewrite those sentences. Common AI patterns: "it is important to note", "plays a pivotal role", "a comprehensive overview", "leveraging", "delve into".

## Cross-References

- **`/bib-validate`** — For thorough bibliography cross-referencing
- **`/latex-autofix`** — For compilation and error resolution (run before proofreading)
- **`/devils-advocate`** — For argument quality and logical scrutiny
