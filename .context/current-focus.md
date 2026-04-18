# Current Focus — Claude Research Workspace

> Last updated: 2026-04-18

## Active Project

**ai-energy-ot** — Carbon-Aware AI Workload Dispatch via Kantorovich LP and Wasserstein DRO
- **Location:** `~/Desktop/ai-energy-ot/`
- **Status:** Complete paper draft (23 pages), all experiments validated, ready for submission
- **Venue:** Evaluating Applied Energy (IF 11.0), Energy and AI (IF 9.6), Omega (IF 6.9). IJDS VSI deprioritised (low IF).
- **Context:** See `~/Desktop/ai-energy-ot/.context/current-focus.md` for full project state

## What Was Done Recently (Apr 13–18)

1. Wrote complete 23-page paper with all experiments validated and figures embedded
2. Full quality audit: citation claims, bibliography, paper-critic, domain-reviewer — all issues fixed
3. Restructured ai-energy-ot project: `code/lib/` shared library pattern
4. Major overhaul of claude-research workspace: 38→30 skills, 6→5 agents, 9→7 rules, 8→4 hooks
5. Added 8 new skills (paper-draft, experiment-runner, replication-check, venue-research, reading-notes, progress-log, council)
6. Rewrote all docs, README, cleaned up stale code (.scripts/, .mcp-server-biblio/, llm-council)
7. Wired up hooks in ~/.claude/settings.json, tested cli-council (Gemini + Claude working)
8. Pushed both repos to GitHub

## Next Steps

1. Choose target journal for ai-energy-ot (Applied Energy vs Energy and AI)
2. Run `/proofread` + `/pre-submission-report` for final audit
3. Submit paper

## Workspace Infrastructure

- MCP bibliography server: configured in `.mcp.json` (OpenAlex + Scopus)
- 30 skills, 5 agents, 7 rules, 4 hooks — all functional
- Research Vault at `~/Research-Vault`
