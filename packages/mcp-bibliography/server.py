#!/usr/bin/env python3
"""
Bibliography MCP Server — self-contained, no external biblio-sources dependency.

Sources: OpenAlex (always) + Crossref (always) + Semantic Scholar (always, key optional)
         + Scopus (key required) + CORE (key required)

Keys loaded from environment variables (set in .env at project root).
"""

import asyncio
import json
import os
import sys
import time
from typing import Any

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# ── Configuration ─────────────────────────────────────────────────────────────

EMAIL = os.environ.get("OPENALEX_EMAIL", "haoliang428@outlook.com")
SCOPUS_KEY = os.environ.get("SCOPUS_API_KEY", "")
S2_KEY = os.environ.get("S2_API_KEY", "")
CORE_KEY = os.environ.get("CORE_API_KEY", "")


def log(msg: str):
    print(f"[bibliography-mcp] {msg}", file=sys.stderr, flush=True)


log(f"OpenAlex: active (email={EMAIL})")
log(f"Crossref: active (no key needed)")
log(f"Semantic Scholar: {'active (API key)' if S2_KEY else 'active (no key, 1 req/s)'}")
log(f"Scopus: {'active' if SCOPUS_KEY else 'inactive (no key)'}")
log(f"CORE: {'active' if CORE_KEY else 'inactive (no key)'}")

# ── HTTP helpers ───────────────────────────────────────────────────────────────

def _get(url: str, params: dict = None, headers: dict = None, timeout: int = 15) -> dict:
    """Synchronous GET with retry on 429."""
    h = {"User-Agent": f"bibliography-mcp/1.0 (mailto:{EMAIL})"}
    if headers:
        h.update(headers)
    for attempt in range(3):
        try:
            r = httpx.get(url, params=params, headers=h, timeout=timeout)
            if r.status_code == 429:
                time.sleep(2 ** attempt)
                continue
            r.raise_for_status()
            return r.json()
        except httpx.HTTPStatusError as e:
            if attempt == 2:
                return {"error": str(e)}
        except Exception as e:
            if attempt == 2:
                return {"error": str(e)}
    return {"error": "max retries exceeded"}


# ── OpenAlex ──────────────────────────────────────────────────────────────────

def _openalex_search(query: str, year: str = None, min_citations: int = None,
                     open_access: bool = False, sort: str = "relevance_score:desc",
                     limit: int = 25) -> list[dict]:
    # Use default.search (title+abstract). Caller should quote key phrases for precision.
    filters = [f"default.search:{query}"]
    if year:
        if year.startswith(">"):
            filters.append(f"publication_year:>{year[1:]}")
        elif "-" in year:
            a, b = year.split("-", 1)
            filters.append(f"publication_year:{a}-{b}")
        else:
            filters.append(f"publication_year:{year}")
    if min_citations:
        filters.append(f"cited_by_count:>{min_citations}")
    if open_access:
        filters.append("is_oa:true")
    params = {
        "filter": ",".join(filters),
        "sort": sort,
        "per-page": min(limit, 50),
        "mailto": EMAIL,
    }

    data = _get("https://api.openalex.org/works", params=params)
    return data.get("results", [])


def _fmt_openalex_work(w: dict) -> dict:
    doi = w.get("doi") or ""
    if doi:
        doi = doi.replace("https://doi.org/", "")
    authors = [a["author"]["display_name"] for a in w.get("authorships", [])[:5]]
    if len(w.get("authorships", [])) > 5:
        authors.append("et al.")
    return {
        "title": w.get("display_name", ""),
        "authors": "; ".join(authors),
        "year": w.get("publication_year", ""),
        "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name", ""),
        "citations": w.get("cited_by_count", 0),
        "doi": doi,
        "openalex_id": w.get("id", "").replace("https://openalex.org/", ""),
        "open_access": w.get("open_access", {}).get("is_oa", False),
        "abstract": _reconstruct_abstract(w.get("abstract_inverted_index")),
    }


def _reconstruct_abstract(inv_index: dict | None) -> str:
    if not inv_index:
        return ""
    words = {}
    for word, positions in inv_index.items():
        for pos in positions:
            words[pos] = word
    return " ".join(words[i] for i in sorted(words))


# ── Semantic Scholar ───────────────────────────────────────────────────────────

def _s2_headers() -> dict:
    h = {}
    if S2_KEY:
        h["x-api-key"] = S2_KEY
    return h


def _s2_search(query: str, limit: int = 25) -> list[dict]:
    params = {
        "query": query,
        "limit": min(limit, 100),
        "fields": "title,authors,year,venue,citationCount,externalIds,abstract,tldr",
    }
    data = _get("https://api.semanticscholar.org/graph/v1/paper/search",
                params=params, headers=_s2_headers())
    return data.get("data", [])


def _s2_paper(paper_id: str) -> dict:
    """Get full paper detail by S2 ID or DOI."""
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}"
    params = {"fields": "title,authors,year,venue,citationCount,referenceCount,externalIds,abstract,tldr,citations,references"}
    return _get(url, params=params, headers=_s2_headers())


def _s2_citations(paper_id: str, limit: int = 50) -> list[dict]:
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/citations"
    params = {"fields": "title,authors,year,citationCount,externalIds", "limit": limit}
    data = _get(url, params=params, headers=_s2_headers())
    return [item.get("citingPaper", {}) for item in data.get("data", [])]


def _s2_references(paper_id: str, limit: int = 50) -> list[dict]:
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/references"
    params = {"fields": "title,authors,year,citationCount,externalIds", "limit": limit}
    data = _get(url, params=params, headers=_s2_headers())
    return [item.get("citedPaper", {}) for item in data.get("data", [])]


def _s2_recommendations(paper_id: str, limit: int = 20) -> list[dict]:
    url = f"https://api.semanticscholar.org/recommendations/v1/papers/forpaper/{paper_id}"
    params = {"fields": "title,authors,year,citationCount,externalIds,abstract", "limit": limit}
    data = _get(url, params=params, headers=_s2_headers())
    return data.get("recommendedPapers", [])


def _fmt_s2_paper(p: dict) -> dict:
    doi = (p.get("externalIds") or {}).get("DOI") or ""
    authors = [a.get("name", "") for a in p.get("authors", [])[:5]]
    if len(p.get("authors", [])) > 5:
        authors.append("et al.")
    tldr = (p.get("tldr") or {}).get("text", "")
    return {
        "title": p.get("title", ""),
        "authors": "; ".join(authors),
        "year": p.get("year", ""),
        "venue": p.get("venue", ""),
        "citations": p.get("citationCount", 0),
        "doi": doi,
        "s2_id": p.get("paperId", ""),
        "abstract": p.get("abstract", ""),
        "tldr": tldr,
    }


# ── Scopus ────────────────────────────────────────────────────────────────────

def _scopus_search(query: str, limit: int = 25) -> list[dict]:
    if not SCOPUS_KEY:
        return []
    # Use plain keyword search — TITLE-ABS-KEY with many terms over-constrains
    scopus_query = query
    params = {
        "query": scopus_query,
        "count": min(limit, 25),
        "sort": "citedby-count:desc",
        "field": "dc:title,dc:creator,prism:publicationName,prism:coverDate,citedby-count,prism:doi,dc:description",
        "httpAccept": "application/json",
    }
    headers = {"X-ELS-APIKey": SCOPUS_KEY, "Accept": "application/json"}
    data = _get("https://api.elsevier.com/content/search/scopus",
                params=params, headers=headers)
    return (data.get("search-results", {}) or {}).get("entry", [])


def _fmt_scopus(e: dict) -> dict:
    return {
        "title": e.get("dc:title", ""),
        "authors": e.get("dc:creator", ""),
        "year": (e.get("prism:coverDate", "") or "")[:4],
        "venue": e.get("prism:publicationName", ""),
        "citations": int(e.get("citedby-count", 0) or 0),
        "doi": e.get("prism:doi", ""),
        "abstract": e.get("dc:description", ""),
    }


# ── CORE ──────────────────────────────────────────────────────────────────────

def _core_search(query: str, limit: int = 25) -> list[dict]:
    if not CORE_KEY:
        return []
    headers = {"Authorization": f"Bearer {CORE_KEY}", "Accept": "application/json"}
    payload = {"q": query, "limit": min(limit, 25), "offset": 0}
    try:
        r = httpx.post("https://api.core.ac.uk/v3/search/works",
                       json=payload, headers=headers, timeout=15)
        r.raise_for_status()
        return r.json().get("results", [])
    except Exception as e:
        return []


def _fmt_core(p: dict) -> dict:
    authors = [a.get("name", "") for a in (p.get("authors") or [])[:5]]
    return {
        "title": p.get("title") or "",
        "authors": "; ".join(authors),
        "year": p.get("yearPublished") or "",
        "venue": p.get("publisher") or "",
        "citations": 0,
        "doi": p.get("doi") or "",
        "abstract": p.get("abstract", ""),
        "download_url": p.get("downloadUrl", ""),
    }


# ── Crossref DOI verification ─────────────────────────────────────────────────

def _crossref_verify_doi(doi: str) -> dict:
    data = _get(f"https://api.crossref.org/works/{doi}",
                params={"mailto": EMAIL})
    if "error" in data:
        return {"doi": doi, "status": "NOT_FOUND", "title": "", "authors": ""}
    msg = data.get("message", {})
    title = (msg.get("title") or [""])[0]
    authors = [f"{a.get('family', '')} {a.get('given', '')[:1]}".strip()
               for a in (msg.get("author") or [])[:3]]
    return {
        "doi": doi,
        "status": "VERIFIED",
        "title": title,
        "authors": "; ".join(authors),
        "year": (msg.get("published", {}) or {}).get("date-parts", [[""]])[0][0],
        "journal": (msg.get("container-title") or [""])[0],
    }


# ── Cross-source search ────────────────────────────────────────────────────────

def _merge_results(openalex: list, s2: list, scopus: list, core: list) -> list[dict]:
    """Merge and deduplicate results from all sources by DOI and title."""
    seen_dois = set()
    seen_titles = set()
    merged = []

    def _add(paper: dict):
        doi = (paper.get("doi") or "").lower().strip()
        title = (paper.get("title") or "").lower().strip()[:60]
        if doi and doi in seen_dois:
            return
        if title and title in seen_titles:
            return
        if doi:
            seen_dois.add(doi)
        if title:
            seen_titles.add(title)
        merged.append(paper)

    for w in openalex:
        p = _fmt_openalex_work(w); p["source"] = "OA"; _add(p)
    for p in s2:
        p = _fmt_s2_paper(p); p["source"] = "S2"; _add(p)
    for e in scopus:
        p = _fmt_scopus(e); p["source"] = "SC"; _add(p)
    for p in core:
        p = _fmt_core(p); p["source"] = "CO"; _add(p)

    # Preserve source relevance order (each source already ranks by relevance)
    return merged


def _papers_to_markdown(papers: list[dict], show_abstract: bool = False) -> str:
    if not papers:
        return "No results found."
    lines = ["| # | Src | Title | Authors | Year | Citations | DOI |",
             "|---|-----|-------|---------|------|-----------|-----|"]
    for i, p in enumerate(papers, 1):
        title = p.get("title", "")[:65]
        authors = p.get("authors", "")[:35]
        doi = p.get("doi", "")
        doi_link = f"[{doi}](https://doi.org/{doi})" if doi else ""
        src = p.get("source", "?")
        lines.append(f"| {i} | {src} | {title} | {authors} | {p.get('year','')} | "
                     f"{p.get('citations',0)} | {doi_link} |")
        if show_abstract and p.get("tldr"):
            lines.append(f"|   |   | *{p['tldr']}* | | | | |")
    return "\n".join(lines)


# ── MCP Server ────────────────────────────────────────────────────────────────

server = Server("bibliography")

TOOLS = [
    Tool(
        name="scholarly_source_status",
        description="Check which search sources are active and available.",
        inputSchema={"type": "object", "properties": {}},
    ),
    Tool(
        name="scholarly_search",
        description=(
            "Search for academic papers across OpenAlex, Semantic Scholar, Scopus, and CORE. "
            "Returns a ranked, deduplicated table of results."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query (keywords, topic, title fragment)"},
                "year": {"type": "string", "description": "Year filter: '2023', '>2020', or '2020-2024'"},
                "min_citations": {"type": "integer", "description": "Minimum citation count"},
                "limit": {"type": "integer", "description": "Max results per source (default 20, max 50)"},
                "show_abstracts": {"type": "boolean", "description": "Include TLDR summaries in output"},
            },
            "required": ["query"],
        },
    ),
    Tool(
        name="scholarly_paper_detail",
        description="Get full details for a paper by DOI or Semantic Scholar ID: abstract, authors, TLDR, citation count.",
        inputSchema={
            "type": "object",
            "properties": {
                "paper_id": {"type": "string", "description": "DOI (e.g. '10.1000/xyz') or S2 paper ID"},
            },
            "required": ["paper_id"],
        },
    ),
    Tool(
        name="scholarly_citations",
        description="Find papers that cite a given paper (forward snowball). Returns up to 100 citing papers.",
        inputSchema={
            "type": "object",
            "properties": {
                "paper_id": {"type": "string", "description": "DOI or S2 paper ID"},
                "limit": {"type": "integer", "description": "Max results (default 50)"},
            },
            "required": ["paper_id"],
        },
    ),
    Tool(
        name="scholarly_references",
        description="Find papers cited by a given paper (backward snowball). Returns up to 100 references.",
        inputSchema={
            "type": "object",
            "properties": {
                "paper_id": {"type": "string", "description": "DOI or S2 paper ID"},
                "limit": {"type": "integer", "description": "Max results (default 50)"},
            },
            "required": ["paper_id"],
        },
    ),
    Tool(
        name="scholarly_similar_works",
        description="Find papers similar to a given paper using Semantic Scholar recommendations.",
        inputSchema={
            "type": "object",
            "properties": {
                "paper_id": {"type": "string", "description": "DOI or S2 paper ID"},
                "limit": {"type": "integer", "description": "Max results (default 20)"},
            },
            "required": ["paper_id"],
        },
    ),
    Tool(
        name="scholarly_verify_dois",
        description=(
            "Verify a list of DOIs against Crossref. Returns status (VERIFIED/NOT_FOUND), "
            "actual title, and authors for each DOI — catches hallucinated or wrong DOIs."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "dois": {"type": "array", "items": {"type": "string"},
                         "description": "List of DOIs to verify (max 50)"},
            },
            "required": ["dois"],
        },
    ),
    Tool(
        name="scholarly_author_papers",
        description="Find all papers by a specific author via OpenAlex.",
        inputSchema={
            "type": "object",
            "properties": {
                "author_name": {"type": "string", "description": "Author name to search"},
                "limit": {"type": "integer", "description": "Max results (default 50)"},
            },
            "required": ["author_name"],
        },
    ),
]


@server.list_tools()
async def list_tools() -> list[Tool]:
    return TOOLS


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        result = await asyncio.get_event_loop().run_in_executor(
            None, _dispatch, name, arguments
        )
        return [TextContent(type="text", text=result)]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {e}")]


def _dispatch(name: str, args: dict) -> str:
    if name == "scholarly_source_status":
        lines = ["## Active Sources\n",
                 f"- **OpenAlex**: active (email: {EMAIL})",
                 f"- **Crossref**: active (no key needed)",
                 f"- **Semantic Scholar**: {'active (API key set)' if S2_KEY else 'active (no key — 1 req/s rate limit)'}",
                 f"- **Scopus**: {'active' if SCOPUS_KEY else 'inactive (set SCOPUS_API_KEY)'}",
                 f"- **CORE**: {'active' if CORE_KEY else 'inactive (set CORE_API_KEY)'}",
                 ]
        return "\n".join(lines)

    elif name == "scholarly_search":
        query = args["query"]
        year = args.get("year")
        min_cit = args.get("min_citations")
        limit = min(args.get("limit", 20), 50)
        show_abs = args.get("show_abstracts", False)

        log(f"scholarly_search: query='{query}' limit={limit}")
        oa = _openalex_search(query, year=year, min_citations=min_cit, limit=limit)
        s2 = _s2_search(query, limit=limit)
        scopus = _scopus_search(query, limit=limit)
        core = _core_search(query, limit=limit)

        merged = _merge_results(oa, s2, scopus, core)[:limit]
        sources = ["OpenAlex", "S2"] + (["Scopus"] if SCOPUS_KEY else []) + (["CORE"] if CORE_KEY else [])
        header = f"**Query:** {query} | **Sources:** {', '.join(sources)} | **Results:** {len(merged)}\n\n"
        return header + _papers_to_markdown(merged, show_abstract=show_abs)

    elif name == "scholarly_paper_detail":
        pid = args["paper_id"]
        # Prefix DOI for S2
        s2_id = f"DOI:{pid}" if pid.startswith("10.") else pid
        p = _s2_paper(s2_id)
        if "error" in p:
            return f"Paper not found: {p['error']}"
        fmt = _fmt_s2_paper(p)
        lines = [
            f"## {fmt['title']}",
            f"**Authors:** {fmt['authors']}",
            f"**Year:** {fmt['year']} | **Venue:** {fmt['venue']} | **Citations:** {fmt['citations']}",
            f"**DOI:** {fmt['doi']}",
            f"**S2 ID:** {fmt['s2_id']}",
        ]
        if fmt.get("tldr"):
            lines.append(f"\n**TL;DR:** {fmt['tldr']}")
        if fmt.get("abstract"):
            lines.append(f"\n**Abstract:** {fmt['abstract'][:800]}...")
        return "\n".join(lines)

    elif name == "scholarly_citations":
        pid = args["paper_id"]
        limit = args.get("limit", 50)
        s2_id = f"DOI:{pid}" if pid.startswith("10.") else pid
        papers = _s2_citations(s2_id, limit=limit)
        fmt = [_fmt_s2_paper(p) for p in papers if p.get("title")]
        return f"**Citing papers ({len(fmt)}):**\n\n" + _papers_to_markdown(fmt)

    elif name == "scholarly_references":
        pid = args["paper_id"]
        limit = args.get("limit", 50)
        s2_id = f"DOI:{pid}" if pid.startswith("10.") else pid
        papers = _s2_references(s2_id, limit=limit)
        fmt = [_fmt_s2_paper(p) for p in papers if p.get("title")]
        return f"**References ({len(fmt)}):**\n\n" + _papers_to_markdown(fmt)

    elif name == "scholarly_similar_works":
        pid = args["paper_id"]
        limit = args.get("limit", 20)
        s2_id = f"DOI:{pid}" if pid.startswith("10.") else pid
        papers = _s2_recommendations(s2_id, limit=limit)
        fmt = [_fmt_s2_paper(p) for p in papers]
        return f"**Similar works ({len(fmt)}):**\n\n" + _papers_to_markdown(fmt, show_abstract=True)

    elif name == "scholarly_verify_dois":
        dois = args["dois"][:50]
        log(f"scholarly_verify_dois: verifying {len(dois)} DOIs")
        results = []
        for doi in dois:
            r = _crossref_verify_doi(doi.strip())
            results.append(r)
            time.sleep(0.1)  # polite rate limiting

        lines = ["| DOI | Status | Title | Authors | Year |",
                 "|-----|--------|-------|---------|------|"]
        for r in results:
            status = "✅ VERIFIED" if r["status"] == "VERIFIED" else "❌ NOT FOUND"
            lines.append(f"| `{r['doi']}` | {status} | {r.get('title','')[:60]} | "
                         f"{r.get('authors','')[:40]} | {r.get('year','')} |")
        return "\n".join(lines)

    elif name == "scholarly_author_papers":
        name_q = args["author_name"]
        limit = args.get("limit", 50)
        # Search OpenAlex for the author
        data = _get("https://api.openalex.org/authors",
                    params={"search": name_q, "per-page": 1, "mailto": EMAIL})
        authors = data.get("results", [])
        if not authors:
            return f"No author found for '{name_q}'"
        author = authors[0]
        author_id = author["id"].replace("https://openalex.org/", "")
        works = _get("https://api.openalex.org/works",
                     params={"filter": f"author.id:{author_id}",
                             "sort": "cited_by_count:desc",
                             "per-page": min(limit, 50),
                             "mailto": EMAIL})
        papers = [_fmt_openalex_work(w) for w in works.get("results", [])]
        header = (f"**{author.get('display_name')}** — "
                  f"{author.get('works_count', 0)} total works, "
                  f"{author.get('cited_by_count', 0)} total citations\n\n")
        return header + _papers_to_markdown(papers)

    else:
        return f"Unknown tool: {name}"


# ── Entry point ───────────────────────────────────────────────────────────────

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
