"""Blueprint MCP server — makes blueprints queryable and drift-detectable."""

from __future__ import annotations

import json
import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .discovery import discover_blueprints, resolve_blueprint
from .drift import detect_drift
from .health import check_health
from .parser import get_index
from .query import QueryResult, lookup_element, query_blueprint

# Project root is passed via env or defaults to cwd
PROJECT_ROOT = Path(os.environ.get("PROJECT_ROOT", os.getcwd())).resolve()

mcp = FastMCP(
    "blueprint",
    instructions=(
        "Blueprint MCP server. Provides tools to query living product specifications "
        "(.blueprint/ directories), detect code drift against specs, and check blueprint health. "
        "Use 'discover' first to find available blueprints, then 'query' or 'lookup' to "
        "retrieve specific information with citations."
    ),
)


@mcp.tool()
def discover() -> str:
    """Find all blueprint directories in the project and summarize their metadata.

    Returns a list of blueprints with name, path, tier, status, version,
    spec owner, and section completeness. Call this first to orient yourself.
    """
    blueprints = discover_blueprints(PROJECT_ROOT)

    if not blueprints:
        return json.dumps({
            "blueprints": [],
            "message": "No blueprints found in this project. Use `/blueprint scaffold` to create one.",
        })

    result = []
    for bp in blueprints:
        index = get_index(bp)
        result.append({
            "name": bp.name,
            "path": str(bp.path.relative_to(PROJECT_ROOT)),
            "status": bp.status,
            "version": bp.version,
            "tier": bp.tier,
            "spec_owner": bp.spec_owner,
            "sections": bp.section_statuses,
            "stats": {
                "terms": len(index.terms),
                "entities": len(index.entities),
                "scenarios": len(index.scenarios),
                "requirements": len(index.requirements),
                "decisions": len(index.decisions),
                "actors": len(index.actors),
                "stories": len(index.stories),
            },
        })

    return json.dumps({"blueprints": result}, indent=2)


@mcp.tool()
def query(question: str, blueprint: str = "") -> str:
    """Answer a natural language question from the blueprint, with citations.

    Args:
        question: The question to answer (e.g., "What happens when an order is cancelled?")
        blueprint: Name of the blueprint to query. Optional if only one blueprint exists.

    Returns grounded excerpts with file paths and line numbers. If the answer is not
    in the spec, says so explicitly — never fabricates.
    """
    try:
        meta = resolve_blueprint(PROJECT_ROOT, blueprint or None)
    except ValueError as e:
        return json.dumps({"error": str(e)})

    result = query_blueprint(meta, question)

    response: dict = {"confidence": result.confidence}

    if result.excerpts:
        response["citations"] = [
            {
                "file": c.file,
                "section": c.section,
                "line_range": f"{c.line_start}-{c.line_end}",
                "excerpt": c.excerpt,
            }
            for c in result.excerpts
        ]

    if result.not_covered:
        response["not_covered"] = result.not_covered

    return json.dumps(response, indent=2)


@mcp.tool()
def lookup(kind: str, name: str, blueprint: str = "") -> str:
    """Direct retrieval of a specific blueprint element by type and name/ID.

    Args:
        kind: Element type — one of: term, entity, scenario, requirement, decision, question, actor, story
        name: Name or ID of the element (e.g., "Order", "REQ-1", "DEC-3", "US-5")
        blueprint: Name of the blueprint. Optional if only one exists.

    Faster and more precise than query for known elements.
    """
    valid_kinds = {"term", "entity", "scenario", "requirement", "decision", "question", "actor", "story"}
    if kind not in valid_kinds:
        return json.dumps({"error": f"Invalid kind '{kind}'. Must be one of: {', '.join(sorted(valid_kinds))}"})

    try:
        meta = resolve_blueprint(PROJECT_ROOT, blueprint or None)
    except ValueError as e:
        return json.dumps({"error": str(e)})

    citations = lookup_element(meta, kind, name)

    if not citations:
        return json.dumps({
            "found": False,
            "message": f"No {kind} named '{name}' found in the blueprint.",
        })

    return json.dumps({
        "found": True,
        "results": [
            {
                "file": c.file,
                "section": c.section,
                "line_range": f"{c.line_start}-{c.line_end}",
                "content": c.excerpt,
            }
            for c in citations
        ],
    }, indent=2)


@mcp.tool()
def detect_blueprint_drift(diff: str, blueprint: str = "", context: str = "") -> str:
    """Analyze code changes (git diff) against the blueprint and flag spec-relevant drift.

    Args:
        diff: Raw unified diff text (e.g., output of `git diff` or `git diff main...HEAD`)
        blueprint: Name of the blueprint. Optional if only one exists.
        context: Optional PR title or description for additional signal.

    Flags new entity states, changed flows, new actors, modified business rules, and
    new terms that aren't covered by the blueprint. Filters out implementation-only
    changes (tests, config, refactors) to minimize false positives.
    """
    try:
        meta = resolve_blueprint(PROJECT_ROOT, blueprint or None)
    except ValueError as e:
        return json.dumps({"error": str(e)})

    result = detect_drift(meta, diff, context)
    return json.dumps(result, indent=2)


@mcp.tool()
def check_blueprint_health(blueprint: str = "") -> str:
    """Check blueprint completeness, cross-reference integrity, and staleness.

    Args:
        blueprint: Name of the blueprint. Optional if only one exists.

    Reports: tier validation (actual vs declared), missing sections, cross-reference
    issues (actors in scenarios not defined, entities referenced but not modeled),
    empty sections, and staleness signals.
    """
    try:
        meta = resolve_blueprint(PROJECT_ROOT, blueprint or None)
    except ValueError as e:
        return json.dumps({"error": str(e)})

    result = check_health(meta)
    return json.dumps(result, indent=2)


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
