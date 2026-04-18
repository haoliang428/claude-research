# Rules (7 auto-loaded)

Rules in `.claude/rules/` are loaded into every session automatically. Keep them lean — every line costs tokens.

| Rule | Lines | Purpose |
|------|-------|---------|
| `design-before-results` | 52 | Lock research design before examining point estimates |
| `lean-claude-md` | 45 | Keep CLAUDE.md slim — instructions only, reference material in docs/ |
| `learn-tags` | 42 | Record learnings with `[LEARN:category]` tags in project MEMORY.md |
| `overleaf-separation` | 67 | `paper/` directory is for LaTeX only — no code or data |
| `plan-first` | 40 | Plan before multi-file edits; assumption check for medium tasks |
| `read-docs-first` | 50 | Read project docs before searching with Glob/Grep/web |
| `scope-discipline` | 28 | Only make changes explicitly requested; ask before fixing extras |

**Total: ~324 lines auto-loaded per session.**
