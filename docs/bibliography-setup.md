# Bibliography MCP Server

Academic paper search across OpenAlex, Scopus, Semantic Scholar, and CORE. Already configured and working.

## Configuration

Lives in `.mcp.json` at the workspace root. API keys are set there — do not duplicate them in docs.

Enabled in `.claude/settings.local.json` via `"enabledMcpjsonServers": ["bibliography"]`.

## Available Tools

| Tool | What it does |
|------|-------------|
| `scholarly_search` | Cross-source keyword search (returns ranked, deduplicated table) |
| `scholarly_paper_detail` | Metadata, abstract, TLDR for a specific paper |
| `scholarly_citations` | Forward citation tracking (papers that cite X) |
| `scholarly_references` | Backward citation tracking (papers cited by X) |
| `scholarly_similar_works` | ML-based semantic similarity recommendations |
| `scholarly_author_papers` | Fetch an author's publication list |
| `scholarly_verify_dois` | Batch DOI verification with title matching |
| `scholarly_source_status` | Check which API sources are active |

## If Something Breaks

```bash
# Check which sources are active
# (call scholarly_source_status from a Claude session)

# Test the server directly
cd packages/mcp-bibliography
uv run python server.py
```

If a source stops working, the API key in `.mcp.json` may have expired. OpenAlex is always free (email only). Scopus and CORE keys need periodic renewal.
