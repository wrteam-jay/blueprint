"""Parse blueprint markdown files into a searchable index."""

from __future__ import annotations

import re
import time
from pathlib import Path

from .types import (
    Actor,
    BlueprintIndex,
    BlueprintMeta,
    Decision,
    Entity,
    EntityState,
    EntityTransition,
    OpenQuestion,
    Requirement,
    Scenario,
    SectionInfo,
    Story,
    Term,
    is_index_stale,
)

_index_cache: dict[str, BlueprintIndex] = {}


def get_index(meta: BlueprintMeta, *, force: bool = False) -> BlueprintIndex:
    """Get or build the searchable index for a blueprint."""
    cache_key = str(meta.path)
    if not force and cache_key in _index_cache:
        cached = _index_cache[cache_key]
        if not is_index_stale(cached):
            return cached

    index = _build_index(meta)
    _index_cache[cache_key] = index
    return index


def _build_index(meta: BlueprintMeta) -> BlueprintIndex:
    """Parse all blueprint files and build a searchable index."""
    index = BlueprintIndex()
    bp_dir = meta.path

    # Parse each known section file
    section_files = {
        "context": "context.md",
        "scope": "scope.md",
        "actors": "actors.md",
        "terminology": "terminology.md",
        "stories": "stories.md",
        "domain-model": "domain-model.md",
        "requirements": "requirements.md",
        "decisions": "decisions.md",
        "questions": "questions.md",
        "changelog": "changelog.md",
    }

    for section_name, filename in section_files.items():
        filepath = bp_dir / filename
        if not filepath.exists():
            continue

        content = filepath.read_text(encoding="utf-8")
        rel_path = f"{bp_dir.name}/{filename}"

        index.sections[section_name] = SectionInfo(
            name=section_name,
            file=rel_path,
            status=meta.section_statuses.get(section_name, ""),
            content=content,
            line_count=len(content.splitlines()),
        )

        # Parse section-specific content
        if section_name == "terminology":
            index.terms = _parse_terms(content, rel_path)
        elif section_name == "actors":
            index.actors = _parse_actors(content, rel_path)
        elif section_name == "domain-model":
            index.entities = _parse_entities(content, rel_path)
        elif section_name == "requirements":
            index.requirements = _parse_requirements(content, rel_path)
        elif section_name == "decisions":
            index.decisions = _parse_decisions(content, rel_path)
        elif section_name == "stories":
            index.stories = _parse_stories(content, rel_path)
        elif section_name == "questions":
            index.questions = _parse_questions(content, rel_path)

    # Parse scenarios directory
    scenarios_dir = bp_dir / "scenarios"
    if scenarios_dir.is_dir():
        rel_scenarios = f"{bp_dir.name}/scenarios"
        # Read _index.md for the scenarios section content
        index_file = scenarios_dir / "_index.md"
        index_content = index_file.read_text(encoding="utf-8") if index_file.exists() else ""
        # Collect all scenario content for full-text search
        all_scenario_content = index_content + "\n"

        for scenario_file in sorted(scenarios_dir.glob("*.md")):
            if scenario_file.name == "_index.md":
                continue
            content = scenario_file.read_text(encoding="utf-8")
            all_scenario_content += content + "\n"
            rel_path = f"{bp_dir.name}/scenarios/{scenario_file.name}"
            scenario = _parse_scenario(content, rel_path)
            if scenario:
                index.scenarios[scenario.name.lower()] = scenario

        index.sections["scenarios"] = SectionInfo(
            name="scenarios",
            file=rel_scenarios,
            status=meta.section_statuses.get("scenarios & flows", ""),
            content=all_scenario_content,
            line_count=len(all_scenario_content.splitlines()),
        )

    index.built_at = time.time()
    return index


def _parse_terms(content: str, file: str) -> dict[str, Term]:
    """Parse terminology section: ## headings are term names, body is definition."""
    terms: dict[str, Term] = {}
    lines = content.splitlines()
    current_name = ""
    current_lines: list[str] = []
    current_start = 0

    for i, line in enumerate(lines, 1):
        if line.startswith("## "):
            if current_name:
                terms[current_name.lower()] = Term(
                    name=current_name,
                    definition="\n".join(current_lines).strip(),
                    file=file,
                    line_start=current_start,
                    line_end=i - 1,
                )
            current_name = line[3:].strip()
            current_lines = []
            current_start = i
        elif current_name:
            current_lines.append(line)

    if current_name:
        terms[current_name.lower()] = Term(
            name=current_name,
            definition="\n".join(current_lines).strip(),
            file=file,
            line_start=current_start,
            line_end=len(lines),
        )

    return terms


def _parse_actors(content: str, file: str) -> dict[str, Actor]:
    """Parse actors section."""
    actors: dict[str, Actor] = {}
    blocks = _split_h2_blocks(content)

    for name, body, start, end in blocks:
        actor = Actor(name=name, description="", file=file, line_start=start, line_end=end)
        lines = body.splitlines()
        desc_lines: list[str] = []
        mode = "desc"

        for line in lines:
            stripped = line.strip()
            lower = stripped.lower()
            if lower.startswith("**can do:**") or lower.startswith("**can do**"):
                mode = "can"
                rest = re.sub(r"\*\*[Cc]an do:?\*\*\s*", "", stripped)
                if rest:
                    actor.can_do.append(rest)
            elif lower.startswith("**cannot do:**") or lower.startswith("**cannot do**"):
                mode = "cannot"
                rest = re.sub(r"\*\*[Cc]annot do:?\*\*\s*", "", stripped)
                if rest:
                    actor.cannot_do.append(rest)
            elif stripped.startswith("- ") or stripped.startswith("* "):
                item = stripped.lstrip("-* ").strip()
                if mode == "can":
                    actor.can_do.append(item)
                elif mode == "cannot":
                    actor.cannot_do.append(item)
            elif mode == "desc" and stripped:
                desc_lines.append(stripped)

        actor.description = " ".join(desc_lines)
        actors[name.lower()] = actor

    return actors


def _parse_entities(content: str, file: str) -> dict[str, Entity]:
    """Parse domain model section."""
    entities: dict[str, Entity] = {}
    blocks = _split_h2_blocks(content)

    for name, body, start, end in blocks:
        # Skip the relationships diagram section
        if name.lower() in ("entity relationships", "relationships"):
            continue

        entity = Entity(name=name, definition="", file=file, line_start=start, line_end=end)

        # Extract definition (first non-empty paragraph before any ** heading)
        lines = body.splitlines()
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("**") and not stripped.startswith("```") and not stripped.startswith("|") and not stripped.startswith("-"):
                entity.definition = stripped
                break

        # Extract states from bullet list under **States:**
        states_block = _extract_bold_section(body, "States")
        if states_block:
            for match in re.finditer(r"-\s+\*\*(\w+)\*\*\s*[-—]\s*(.*)", states_block):
                entity.states.append(EntityState(
                    name=match.group(1),
                    description=match.group(2).strip(),
                ))

        # Extract transitions from mermaid state diagram
        for match in re.finditer(r"(\w+|\[\*\])\s+-->\s+(\w+|\[\*\])\s*:\s*(.*)", body):
            from_s = match.group(1).strip("[]* ")
            to_s = match.group(2).strip("[]* ")
            trigger = match.group(3).strip()
            if from_s and to_s:
                entity.transitions.append(EntityTransition(
                    from_state=from_s if from_s else "(initial)",
                    to_state=to_s if to_s else "(final)",
                    trigger=trigger,
                ))

        # Extract invariants
        invariants_block = _extract_bold_section(body, "Invariants")
        if invariants_block:
            for match in re.finditer(r"-\s+(.*)", invariants_block):
                entity.invariants.append(match.group(1).strip())

        # Extract relationships
        rels_block = _extract_bold_section(body, "Relationships")
        if rels_block:
            for match in re.finditer(r"-\s+(.*)", rels_block):
                entity.relationships.append(match.group(1).strip())

        entities[name.lower()] = entity

    return entities


def _parse_requirements(content: str, file: str) -> dict[str, Requirement]:
    """Parse requirements section. Format: **REQ-1.** statement"""
    requirements: dict[str, Requirement] = {}
    lines = content.splitlines()

    current_id = ""
    current_statement = ""
    current_source = ""
    current_test = ""
    current_start = 0

    def _save_current():
        if current_id:
            requirements[current_id.lower()] = Requirement(
                id=current_id,
                statement=current_statement.strip(),
                source=current_source.strip(),
                test=current_test.strip(),
                file=file,
                line_start=current_start,
                line_end=i,
            )

    for i, line in enumerate(lines, 1):
        req_match = re.match(r"\*\*(REQ-\d+)\.\*\*\s*(.*)", line)
        if req_match:
            _save_current()
            current_id = req_match.group(1)
            current_statement = req_match.group(2)
            current_source = ""
            current_test = ""
            current_start = i
        elif current_id:
            if line.strip().startswith("*Source:"):
                current_source = re.sub(r"^\*Source:\s*", "", line.strip()).rstrip("*")
            elif line.strip().startswith("*Test:"):
                current_test = re.sub(r"^\*Test:\s*", "", line.strip()).rstrip("*")

    _save_current()
    return requirements


def _parse_decisions(content: str, file: str) -> dict[str, Decision]:
    """Parse decision log. Format: ## DEC-N: title"""
    decisions: dict[str, Decision] = {}
    blocks = _split_h2_blocks(content)

    for heading, body, start, end in blocks:
        dec_match = re.match(r"(DEC-\d+):?\s*(.*)", heading)
        if not dec_match:
            continue

        dec_id = dec_match.group(1)
        title = dec_match.group(2).strip()

        decision = Decision(
            id=dec_id,
            decision=title,
            file=file,
            line_start=start,
            line_end=end,
        )

        # Parse structured fields
        for line in body.splitlines():
            stripped = line.strip()
            if stripped.startswith("**Date:**"):
                decision.date = stripped.replace("**Date:**", "").strip()
            elif stripped.startswith("**Decision:**"):
                decision.decision = stripped.replace("**Decision:**", "").strip()
            elif stripped.startswith("**Why:**"):
                decision.rationale = stripped.replace("**Why:**", "").strip()
            elif stripped.startswith("**Alternatives considered:**"):
                decision.alternatives = stripped.replace("**Alternatives considered:**", "").strip()
            elif stripped.startswith("**Decided by:**"):
                decision.decided_by = stripped.replace("**Decided by:**", "").strip()

        decisions[dec_id.lower()] = decision

    return decisions


def _parse_stories(content: str, file: str) -> dict[str, Story]:
    """Parse user stories. Format: **US-N.** As a ..."""
    stories: dict[str, Story] = {}
    lines = content.splitlines()

    for i, line in enumerate(lines, 1):
        story_match = re.match(r"\*\*(US-\d+)\.\*\*\s*(.*)", line)
        if story_match:
            story_id = story_match.group(1)
            stories[story_id.lower()] = Story(
                id=story_id,
                text=story_match.group(2).strip(),
                file=file,
                line_start=i,
                line_end=i,
            )

    return stories


def _parse_questions(content: str, file: str) -> dict[str, OpenQuestion]:
    """Parse open questions. Format varies, look for OQ-N patterns."""
    questions: dict[str, OpenQuestion] = {}
    lines = content.splitlines()

    for i, line in enumerate(lines, 1):
        oq_match = re.match(r"\*?\*?(OQ-\d+)\*?\*?\s*[-:.]?\s*(.*)", line)
        if oq_match:
            oq_id = oq_match.group(1)
            questions[oq_id.lower()] = OpenQuestion(
                id=oq_id,
                question=oq_match.group(2).strip(),
                file=file,
                line_start=i,
                line_end=i,
            )

    return questions


def _parse_scenario(content: str, file: str) -> Scenario | None:
    """Parse a single scenario file."""
    lines = content.splitlines()
    if not lines:
        return None

    # Name from first heading
    name = ""
    for line in lines:
        if line.startswith("# "):
            name = line[2:].strip()
            name = re.sub(r"^Scenario:\s*", "", name, flags=re.IGNORECASE).strip()
            break

    if not name:
        name = Path(file).stem.replace("-", " ").title()

    scenario = Scenario(name=name, file=file, line_start=1, line_end=len(lines))

    # Parse sections by ## headings
    current_section = ""
    current_lines: list[str] = []

    def _save_section():
        text = "\n".join(current_lines).strip()
        if current_section == "trigger":
            scenario.trigger = text
        elif current_section == "preconditions":
            scenario.preconditions = [l.lstrip("-* ").strip() for l in current_lines if l.strip().startswith(("-", "*"))]
            if not scenario.preconditions and text:
                scenario.preconditions = [text]
        elif current_section == "steps":
            scenario.steps = [l.strip() for l in current_lines if re.match(r"\d+\.", l.strip())]
        elif current_section == "outcomes":
            scenario.outcomes = [l.lstrip("-* ").strip() for l in current_lines if l.strip().startswith(("-", "*"))]
            if not scenario.outcomes and text:
                scenario.outcomes = [text]
        elif current_section in ("error paths", "error path"):
            scenario.error_paths = [l.lstrip("-* ").strip() for l in current_lines if l.strip().startswith(("-", "*"))]

    for line in lines:
        if line.startswith("## "):
            _save_section()
            current_section = line[3:].strip().lower()
            current_lines = []
        else:
            current_lines.append(line)

    _save_section()

    # Extract actors and entities from content
    full_text = content
    scenario.actors = _extract_references_from_text(full_text, "actor")
    scenario.entities = _extract_references_from_text(full_text, "entity")

    return scenario


def _extract_references_from_text(text: str, _kind: str) -> list[str]:
    """Extract actor/entity references from scenario text.

    Uses the scenario's own metadata (Actors line in the _index.md table, or
    explicit mentions in steps) rather than just bold text, which is too noisy.
    """
    refs: list[str] = []
    # Look for explicit "Actors:" or actor-like patterns in scenario structure
    # Match patterns like "A Spec Author invokes..." or "The Spec Owner resolves..."
    for match in re.finditer(r"(?:the|a)\s+((?:[A-Z][a-z]+\s*){1,3}?)(?:\s+(?:invokes?|creates?|updates?|reads?|resolves?|approves?|reviews?|asks?|provides?))", text):
        ref = match.group(1).strip()
        if ref:
            refs.append(ref)
    return list(dict.fromkeys(refs))  # deduplicate preserving order


# -- Utilities --


def _split_h2_blocks(content: str) -> list[tuple[str, str, int, int]]:
    """Split content into (heading, body, start_line, end_line) blocks by ## headings."""
    blocks: list[tuple[str, str, int, int]] = []
    lines = content.splitlines()
    current_heading = ""
    current_body: list[str] = []
    current_start = 0

    for i, line in enumerate(lines, 1):
        if line.startswith("## "):
            if current_heading:
                blocks.append((current_heading, "\n".join(current_body), current_start, i - 1))
            current_heading = line[3:].strip()
            current_body = []
            current_start = i
        elif current_heading:
            current_body.append(line)

    if current_heading:
        blocks.append((current_heading, "\n".join(current_body), current_start, len(lines)))

    return blocks


def _extract_bold_section(text: str, label: str) -> str | None:
    """Extract text following a **Label:** line until the next **Label:** or ## heading."""
    pattern = rf"\*\*{re.escape(label)}:?\*\*"
    match = re.search(pattern, text, re.IGNORECASE)
    if not match:
        return None

    start = match.end()
    # Find the end: next **Bold:** section or ## heading
    end_match = re.search(r"\n\*\*[A-Z].*?\*\*|\n##\s", text[start:])
    if end_match:
        return text[start:start + end_match.start()]
    return text[start:]
