"""Discover .blueprint/ directories and parse their README manifests."""

from __future__ import annotations

import re
import time
from pathlib import Path

from .types import BlueprintMeta

_cache: dict[str, tuple[float, list[BlueprintMeta]]] = {}
_CACHE_TTL = 30  # seconds


def discover_blueprints(project_root: Path, *, force: bool = False) -> list[BlueprintMeta]:
    """Find all .blueprint/ directories under project_root and parse their manifests."""
    cache_key = str(project_root)
    if not force and cache_key in _cache:
        cached_at, cached = _cache[cache_key]
        if (time.time() - cached_at) < _CACHE_TTL:
            return cached

    blueprints: list[BlueprintMeta] = []
    if not project_root.is_dir():
        return blueprints

    for item in sorted(project_root.rglob("*.blueprint")):
        if not item.is_dir():
            continue
        # Skip anything inside node_modules, .git, venv, etc.
        parts = item.relative_to(project_root).parts
        if any(p.startswith(".") or p in ("node_modules", "venv", "__pycache__") for p in parts[:-1]):
            continue

        readme = item / "README.md"
        if readme.exists():
            meta = _parse_readme(readme, item, project_root)
        else:
            meta = BlueprintMeta(
                name=item.stem,
                path=item,
            )
        blueprints.append(meta)

    _cache[cache_key] = (time.time(), blueprints)
    return blueprints


def _parse_readme(readme: Path, bp_dir: Path, project_root: Path) -> BlueprintMeta:
    """Parse a blueprint README.md manifest to extract metadata."""
    text = readme.read_text(encoding="utf-8")
    lines = text.splitlines()

    meta = BlueprintMeta(
        name=bp_dir.stem,
        path=bp_dir,
    )

    # Parse header block (key: value lines)
    for line in lines:
        lower = line.lower().strip()
        if lower.startswith("# "):
            # Extract name from heading: "# Blueprint: Something"
            heading = line.strip().lstrip("# ").strip()
            if ":" in heading:
                meta.name = heading.split(":", 1)[1].strip()
        elif lower.startswith("**status:**"):
            meta.status = _extract_value(line)
        elif lower.startswith("**version:**"):
            meta.version = _extract_value(line)
        elif lower.startswith("**spec owner:**"):
            meta.spec_owner = _extract_value(line)
        elif lower.startswith("**related blueprints:**"):
            val = _extract_value(line)
            if val.lower() not in ("none", ""):
                meta.related_blueprints = [b.strip() for b in val.split(",")]

    # Parse sections table
    meta.section_statuses = _parse_section_table(text)

    # Determine tier from section completeness
    meta.tier = _determine_tier(meta.section_statuses)

    # Check for explicit tier declaration
    tier_match = re.search(r"(?i)tier\s+(\d)", text)
    if tier_match:
        meta.tier = int(tier_match.group(1))

    return meta


def _extract_value(line: str) -> str:
    """Extract value from a '**Key:** value' line."""
    match = re.search(r"\*\*[^*]+:\*\*\s*(.*)", line)
    if match:
        return match.group(1).strip()
    return ""


def _parse_section_table(text: str) -> dict[str, str]:
    """Parse the sections table from README.md."""
    statuses: dict[str, str] = {}
    in_table = False

    for line in text.splitlines():
        stripped = line.strip()
        if "|" in stripped and ("section" in stripped.lower() or "file" in stripped.lower()):
            in_table = True
            continue
        if in_table and stripped.startswith("|---"):
            continue
        if in_table and "|" in stripped:
            cols = [c.strip() for c in stripped.split("|")]
            cols = [c for c in cols if c]  # remove empty from leading/trailing |
            if len(cols) >= 4:
                section_name = re.sub(r"\[([^\]]+)\].*", r"\1", cols[1]).strip()
                status = cols[3].strip()
                # Clean status of markdown artifacts
                status = re.sub(r"\(.*?\)", "", status).strip()
                statuses[section_name.lower()] = status
        elif in_table and not stripped:
            in_table = False

    return statuses


TIER_1_SECTIONS = {"context", "scope", "actors & roles", "terminology"}
TIER_2_SECTIONS = TIER_1_SECTIONS | {"user stories", "scenarios & flows", "domain model"}
TIER_3_SECTIONS = TIER_2_SECTIONS | {"requirements", "decision log", "open questions", "changelog"}


def _determine_tier(section_statuses: dict[str, str]) -> int:
    """Determine the actual tier based on which sections have content."""
    completed = set()
    for name, status in section_statuses.items():
        s = status.lower()
        if s in ("complete", "active") or s.startswith("active"):
            completed.add(name.lower())
        elif s == "resolved":
            completed.add(name.lower())

    if TIER_3_SECTIONS.issubset(completed):
        return 3
    if TIER_2_SECTIONS.issubset(completed):
        return 2
    if TIER_1_SECTIONS.issubset(completed):
        return 1
    return 0


def resolve_blueprint(
    project_root: Path, blueprint_name: str | None, blueprints: list[BlueprintMeta] | None = None
) -> BlueprintMeta:
    """Resolve a blueprint by name, or return the only one if there's just one.

    Raises ValueError if ambiguous or not found.
    """
    if blueprints is None:
        blueprints = discover_blueprints(project_root)

    if not blueprints:
        raise ValueError(
            "No blueprints found in this project. Use `/blueprint scaffold` to create one."
        )

    if blueprint_name:
        name_lower = blueprint_name.lower().replace(".blueprint", "")
        for bp in blueprints:
            if bp.name.lower() == name_lower or bp.path.stem.lower() == name_lower:
                return bp
        available = ", ".join(bp.name for bp in blueprints)
        raise ValueError(f"Blueprint '{blueprint_name}' not found. Available: {available}")

    if len(blueprints) == 1:
        return blueprints[0]

    available = ", ".join(bp.name for bp in blueprints)
    raise ValueError(
        f"Multiple blueprints found: {available}. Please specify which one with the 'blueprint' parameter."
    )
