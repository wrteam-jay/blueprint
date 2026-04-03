"""Blueprint health checks: completeness, cross-references, staleness."""

from __future__ import annotations

import re

from .discovery import TIER_1_SECTIONS, TIER_2_SECTIONS, TIER_3_SECTIONS, _determine_tier
from .parser import get_index
from .types import BlueprintMeta, HealthIssue


def check_health(meta: BlueprintMeta) -> dict:
    """Run health checks on a blueprint and return structured results."""
    index = get_index(meta)
    issues: list[HealthIssue] = []

    # 1. Tier validation
    actual_tier = _determine_tier(meta.section_statuses)
    declared_tier = meta.tier
    tier_mismatch = actual_tier != declared_tier and declared_tier > 0

    if tier_mismatch:
        issues.append(HealthIssue(
            kind="tier_mismatch",
            message=f"Declared tier {declared_tier} but actual completeness is tier {actual_tier}",
        ))

    # 2. Missing sections for declared tier
    missing = _check_missing_sections(meta, index)
    issues.extend(missing)

    # 3. Empty sections
    for name, section in index.sections.items():
        if section.content and section.line_count <= 2:
            issues.append(HealthIssue(
                kind="empty_section",
                message=f"Section '{name}' has minimal content ({section.line_count} lines)",
                file=section.file,
                section=name,
            ))

    # 4. Cross-reference checks
    issues.extend(_check_cross_references(index))

    # 5. Staleness signals
    issues.extend(_check_staleness(index))

    return {
        "blueprint": meta.name,
        "declared_tier": declared_tier,
        "actual_tier": actual_tier,
        "tier_mismatch": tier_mismatch,
        "issues": [
            {
                "kind": i.kind,
                "message": i.message,
                "file": i.file,
                "section": i.section,
            }
            for i in issues
        ],
        "summary": {
            "total_issues": len(issues),
            "cross_reference": sum(1 for i in issues if i.kind == "cross_reference"),
            "empty_section": sum(1 for i in issues if i.kind == "empty_section"),
            "staleness": sum(1 for i in issues if i.kind == "staleness"),
            "tier_mismatch": 1 if tier_mismatch else 0,
            "missing_section": sum(1 for i in issues if i.kind == "missing_section"),
        },
        "stats": {
            "terms": len(index.terms),
            "entities": len(index.entities),
            "scenarios": len(index.scenarios),
            "requirements": len(index.requirements),
            "decisions": len(index.decisions),
            "actors": len(index.actors),
            "stories": len(index.stories),
            "open_questions": len(index.questions),
        },
    }


def _check_missing_sections(meta: BlueprintMeta, index) -> list[HealthIssue]:
    """Check for sections that should exist based on declared tier."""
    issues: list[HealthIssue] = []

    if meta.tier <= 0:
        return issues

    expected: set[str] = set()
    if meta.tier >= 1:
        expected |= {"context", "scope", "actors", "terminology"}
    if meta.tier >= 2:
        expected |= {"stories", "scenarios", "domain-model"}
    if meta.tier >= 3:
        expected |= {"requirements", "decisions", "questions", "changelog"}

    existing = set(index.sections.keys())

    for section in sorted(expected - existing):
        issues.append(HealthIssue(
            kind="missing_section",
            message=f"Section '{section}' expected for tier {meta.tier} but file not found",
            section=section,
        ))

    return issues


def _check_cross_references(index) -> list[HealthIssue]:
    """Check consistency across sections."""
    issues: list[HealthIssue] = []

    # Actors in scenarios must be in actors section
    defined_actors = {name.lower() for name in index.actors}
    for sname, scenario in index.scenarios.items():
        for actor_ref in scenario.actors:
            actor_lower = actor_ref.lower()
            # Check if any defined actor is a substring match
            if not any(da in actor_lower or actor_lower in da for da in defined_actors):
                issues.append(HealthIssue(
                    kind="cross_reference",
                    message=f"Actor '{actor_ref}' appears in scenario '{scenario.name}' but is not defined in actors.md",
                    file=scenario.file,
                    section="scenarios",
                ))

    # Every defined actor should appear in at least one scenario
    if index.scenarios:
        # Collect all scenario text (from section content + scenario files + index)
        all_scenario_text = ""
        for section in index.sections.values():
            if "scenario" in section.name.lower() or section.file.endswith("_index.md"):
                all_scenario_text += (section.content or "").lower() + " "

        # Also read individual scenario file content from sections
        for section in index.sections.values():
            if "/scenarios/" in section.file:
                all_scenario_text += (section.content or "").lower() + " "

        # Include actor refs parsed from scenarios
        for s in index.scenarios.values():
            for actor_ref in s.actors:
                all_scenario_text += " " + actor_ref.lower()

        for actor_name, actor in index.actors.items():
            # Check both the full name and individual words (e.g., "spec author" matches "Spec Author")
            if actor_name not in all_scenario_text and actor.name.lower() not in all_scenario_text:
                # Also try partial match — "panellist" should match "panellist (simulated)"
                base_name = actor_name.split("(")[0].strip()
                if base_name not in all_scenario_text:
                    issues.append(HealthIssue(
                        kind="cross_reference",
                        message=f"Actor '{actor.name}' is defined but does not appear in any scenario",
                        file=actor.file,
                        section="actors",
                    ))

    # Entities in scenarios should be in domain model
    defined_entities = {name.lower() for name in index.entities}
    for sname, scenario in index.scenarios.items():
        for entity_ref in scenario.entities:
            entity_lower = entity_ref.lower()
            if not any(de in entity_lower or entity_lower in de for de in defined_entities):
                issues.append(HealthIssue(
                    kind="cross_reference",
                    message=f"Entity '{entity_ref}' referenced in scenario '{scenario.name}' but not in domain-model.md",
                    file=scenario.file,
                    section="scenarios",
                ))

    # Every user story should have a delivering scenario
    if index.stories and index.scenarios:
        all_scenario_content = ""
        for s in index.scenarios.values():
            # Read scenario content from sections if available
            for section in index.sections.values():
                if section.file == s.file:
                    all_scenario_content += (section.content or "").lower()

        for story_id, story in index.stories.items():
            # Check if story ID appears in any scenario
            if story.id.lower() not in all_scenario_content:
                # Softer check: do the story's key words appear in scenarios?
                pass  # This is hard to check without full scenario content

    # Requirements should reference valid sources
    for req_id, req in index.requirements.items():
        if req.source:
            # Check if referenced decisions exist
            for match in re.finditer(r"DEC-\d+", req.source):
                dec_ref = match.group(0).lower()
                if dec_ref not in index.decisions:
                    issues.append(HealthIssue(
                        kind="cross_reference",
                        message=f"Requirement {req.id} references {match.group(0)} which is not in the decision log",
                        file=req.file,
                        section="requirements",
                    ))

    return issues


def _check_staleness(index) -> list[HealthIssue]:
    """Check for staleness signals within the blueprint itself."""
    issues: list[HealthIssue] = []

    # Entities with states but no transitions
    for name, entity in index.entities.items():
        if len(entity.states) > 2 and not entity.transitions:
            issues.append(HealthIssue(
                kind="staleness",
                message=f"Entity '{entity.name}' has {len(entity.states)} states but no transitions documented",
                file=entity.file,
                section="domain-model",
            ))

    # Entities with no invariants
    for name, entity in index.entities.items():
        if entity.states and not entity.invariants:
            issues.append(HealthIssue(
                kind="staleness",
                message=f"Entity '{entity.name}' has states but no invariants documented",
                file=entity.file,
                section="domain-model",
            ))

    # Decisions without rationale
    for dec_id, dec in index.decisions.items():
        if not dec.rationale:
            issues.append(HealthIssue(
                kind="staleness",
                message=f"Decision {dec.id} has no rationale documented",
                file=dec.file,
                section="decisions",
            ))

    # Open questions (their existence is a staleness signal)
    if index.questions:
        issues.append(HealthIssue(
            kind="staleness",
            message=f"{len(index.questions)} open question(s) remain unresolved",
            section="questions",
        ))

    # Scenarios without error paths
    for sname, scenario in index.scenarios.items():
        if scenario.steps and not scenario.error_paths:
            issues.append(HealthIssue(
                kind="staleness",
                message=f"Scenario '{scenario.name}' has no error paths documented",
                file=scenario.file,
                section="scenarios",
            ))

    return issues
