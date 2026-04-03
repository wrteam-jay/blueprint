"""Diff parsing and drift detection against blueprint specifications."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .parser import get_index
from .types import BlueprintMeta, DriftAlert


# Directories/patterns to skip (implementation-only, not spec-relevant)
SKIP_PATHS = {
    "test/", "tests/", "spec/", "__tests__/", "test_", "_test.",
    ".github/", ".gitlab/", ".circleci/", "Dockerfile", "docker-compose",
    ".env", ".gitignore", "Makefile", "Jenkinsfile",
    "node_modules/", "venv/", "__pycache__/",
    ".blueprint/",  # blueprint files themselves are not code drift
}

SKIP_EXTENSIONS = {
    ".md", ".txt", ".rst", ".yml", ".yaml", ".toml", ".ini", ".cfg",
    ".json", ".lock", ".sum", ".mod",
}


@dataclass
class DiffChange:
    """A meaningful change extracted from a git diff."""

    file: str
    line: int
    kind: str  # "new_type", "new_state", "new_role", "new_validation", "new_flow", "modified_logic"
    name: str
    snippet: str


def detect_drift(
    meta: BlueprintMeta,
    diff_text: str,
    context: str = "",
) -> dict:
    """Analyze a git diff against the blueprint and flag spec-relevant drift.

    Returns a dict with 'alerts' list and 'summary' dict.
    """
    index = get_index(meta)
    bp_name = meta.path.name

    # Step 1: Parse the diff into file-level hunks
    changes = _extract_changes(diff_text)

    # Step 2: Filter out non-spec-relevant changes
    changes = [c for c in changes if _passes_abstraction_test(c)]

    # Step 3: Match against blueprint
    alerts: list[DriftAlert] = []

    for change in changes:
        if change.kind == "new_state":
            alert = _check_state_drift(change, index, bp_name)
            if alert:
                alerts.append(alert)

        elif change.kind == "new_type":
            alert = _check_entity_drift(change, index, bp_name)
            if alert:
                alerts.append(alert)

        elif change.kind == "new_role":
            alert = _check_actor_drift(change, index, bp_name)
            if alert:
                alerts.append(alert)

        elif change.kind == "new_validation":
            alert = _check_rule_drift(change, index, bp_name)
            if alert:
                alerts.append(alert)

        elif change.kind == "new_flow":
            alert = _check_flow_drift(change, index, bp_name)
            if alert:
                alerts.append(alert)

    # Also check PR context for high-level drift signals
    if context:
        context_alerts = _check_context_signals(context, index, bp_name)
        alerts.extend(context_alerts)

    return {
        "alerts": [_alert_to_dict(a) for a in alerts],
        "summary": {
            "drift_count": sum(1 for a in alerts if a.severity == "drift"),
            "uncovered_count": sum(1 for a in alerts if a.severity == "uncovered"),
            "changes_analyzed": len(changes),
        },
    }


def _extract_changes(diff_text: str) -> list[DiffChange]:
    """Parse unified diff into meaningful change candidates."""
    changes: list[DiffChange] = []
    current_file = ""
    line_num = 0

    for line in diff_text.splitlines():
        # Track file being changed
        if line.startswith("+++ b/"):
            current_file = line[6:]
            continue
        if line.startswith("@@ "):
            # Parse hunk header for line numbers
            match = re.search(r"\+(\d+)", line)
            if match:
                line_num = int(match.group(1))
            continue
        if not line.startswith("+") or line.startswith("+++"):
            if not line.startswith("-"):
                line_num += 1
            continue

        added_line = line[1:]  # Remove the leading +
        line_num += 1

        if _should_skip_file(current_file):
            continue

        # Detect new type/class/struct definitions
        type_match = re.match(
            r"\s*(?:class|struct|type|interface|enum)\s+(\w+)", added_line
        )
        if type_match:
            changes.append(DiffChange(
                file=current_file, line=line_num, kind="new_type",
                name=type_match.group(1), snippet=added_line.strip(),
            ))
            continue

        # Detect new state/status constants
        state_match = re.search(
            r"""(?:STATUS_|STATE_|status|state)\s*[=:]\s*['"](\w+)['"]"""
            r"""|['"](\w+)['"]\s*(?:=>|:)\s*['"].*(?:status|state)"""
            r"""|(?:PENDING|ACTIVE|DRAFT|SUSPENDED|CANCELLED|COMPLETED|EXPIRED|ARCHIVED|BLOCKED|PAUSED|REJECTED|APPROVED)\b""",
            added_line, re.IGNORECASE,
        )
        if state_match:
            state_name = state_match.group(1) or state_match.group(2) or state_match.group(0).strip("'\" ")
            changes.append(DiffChange(
                file=current_file, line=line_num, kind="new_state",
                name=state_name, snippet=added_line.strip(),
            ))
            continue

        # Detect new enum values
        enum_match = re.match(r"\s*(\w+)\s*[=,]", added_line)
        if enum_match and _in_enum_context(diff_text, current_file, line_num):
            changes.append(DiffChange(
                file=current_file, line=line_num, kind="new_state",
                name=enum_match.group(1), snippet=added_line.strip(),
            ))
            continue

        # Detect role/permission patterns
        role_match = re.search(
            r"""(?:role|permission|can_|is_|has_|allow|deny|grant)\w*\s*[=(]\s*['"](\w+)['"]""",
            added_line, re.IGNORECASE,
        )
        if role_match:
            changes.append(DiffChange(
                file=current_file, line=line_num, kind="new_role",
                name=role_match.group(1), snippet=added_line.strip(),
            ))
            continue

        # Detect new validation/business rules
        validation_match = re.search(
            r"""(?:raise|throw|Error|Exception|validate|assert|must|invalid|forbidden)""",
            added_line, re.IGNORECASE,
        )
        if validation_match and len(added_line.strip()) > 20:
            changes.append(DiffChange(
                file=current_file, line=line_num, kind="new_validation",
                name="validation_rule", snippet=added_line.strip(),
            ))
            continue

        # Detect new endpoints/routes/handlers (flow candidates)
        flow_match = re.search(
            r"""(?:@(?:app|router|api)\.\w+|\.(?:get|post|put|patch|delete)\(|def\s+(?:handle|process|on_)\w+|function\s+(?:handle|process|on_)\w+)""",
            added_line, re.IGNORECASE,
        )
        if flow_match:
            changes.append(DiffChange(
                file=current_file, line=line_num, kind="new_flow",
                name=flow_match.group(0).strip(), snippet=added_line.strip(),
            ))
            continue

    return changes


def _should_skip_file(filepath: str) -> bool:
    """Check if this file path is non-spec-relevant."""
    filepath_lower = filepath.lower()
    for skip in SKIP_PATHS:
        if skip in filepath_lower:
            return True
    for ext in SKIP_EXTENSIONS:
        if filepath_lower.endswith(ext):
            return True
    return False


def _passes_abstraction_test(change: DiffChange) -> bool:
    """Would someone need to know this to understand behaviour?"""
    # Skip obvious implementation details
    name_lower = change.name.lower()
    impl_patterns = [
        "helper", "util", "internal", "private", "_impl", "mixin",
        "factory", "builder", "adapter", "wrapper", "proxy",
        "cache", "pool", "buffer", "queue_impl", "retry",
    ]
    for pattern in impl_patterns:
        if pattern in name_lower:
            return False

    # Skip test-related
    if "test" in change.file.lower() or "spec" in change.file.lower():
        return False

    return True


def _in_enum_context(diff_text: str, current_file: str, line_num: int) -> bool:
    """Rough heuristic: is this line inside an enum block?"""
    # Look for enum keyword within 10 lines before
    lines = diff_text.splitlines()
    file_lines = [l for l in lines if not l.startswith("diff --git")]
    for i, line in enumerate(file_lines):
        if "enum" in line.lower() and i < line_num and (line_num - i) < 15:
            return True
    return False


# -- Blueprint matching --


def _check_state_drift(change: DiffChange, index, bp_name: str) -> DriftAlert | None:
    """Check if a new state exists in any entity's state list."""
    state_lower = change.name.lower()

    for entity_name, entity in index.entities.items():
        known_states = {s.name.lower() for s in entity.states}
        # Check if this looks like it belongs to this entity
        if entity_name in change.file.lower() or entity_name in change.snippet.lower():
            if state_lower not in known_states:
                return DriftAlert(
                    severity="drift",
                    summary=f"New '{change.name}' state added to code, but '{entity.name}' entity in blueprint only has states: {', '.join(s.name for s in entity.states)}",
                    category="new_entity_state",
                    code_file=change.file,
                    code_line=change.line,
                    code_snippet=change.snippet,
                    blueprint_file=entity.file,
                    blueprint_section=f"Entity: {entity.name}",
                    blueprint_excerpt=f"States: {', '.join(s.name for s in entity.states)}",
                    recommendation=f"Add '{change.name}' state to {entity.name} entity in domain-model.md. Document transitions to/from this state.",
                )

    # If no specific entity matched, check all entities
    all_known_states: set[str] = set()
    for entity in index.entities.values():
        for s in entity.states:
            all_known_states.add(s.name.lower())

    if state_lower not in all_known_states and len(state_lower) > 2:
        return DriftAlert(
            severity="uncovered",
            summary=f"New state '{change.name}' in code does not match any known entity state in the blueprint",
            category="new_entity_state",
            code_file=change.file,
            code_line=change.line,
            code_snippet=change.snippet,
            recommendation=f"Check if '{change.name}' represents a new entity state that should be documented in domain-model.md.",
        )

    return None


def _check_entity_drift(change: DiffChange, index, bp_name: str) -> DriftAlert | None:
    """Check if a new type/class maps to a known entity."""
    name_lower = change.name.lower()

    if name_lower not in index.entities and name_lower not in index.terms:
        # Check if the name is similar to any entity (could be a new entity)
        for entity_name in index.entities:
            if name_lower in entity_name or entity_name in name_lower:
                return None  # Close enough, probably the same thing

        return DriftAlert(
            severity="uncovered",
            summary=f"New type '{change.name}' does not correspond to any entity or term in the blueprint",
            category="new_term",
            code_file=change.file,
            code_line=change.line,
            code_snippet=change.snippet,
            recommendation=f"Consider adding '{change.name}' to terminology.md if it's a domain concept, or to domain-model.md if it has lifecycle states.",
        )

    return None


def _check_actor_drift(change: DiffChange, index, bp_name: str) -> DriftAlert | None:
    """Check if a new role exists in actors."""
    role_lower = change.name.lower()

    known_actors = {name.lower() for name in index.actors}
    # Also check as substrings
    for actor_name in known_actors:
        if role_lower in actor_name or actor_name in role_lower:
            return None

    return DriftAlert(
        severity="uncovered",
        summary=f"New role/permission '{change.name}' in code, no matching actor in blueprint",
        category="new_actor",
        code_file=change.file,
        code_line=change.line,
        code_snippet=change.snippet,
        recommendation=f"Check if '{change.name}' represents a new actor or capability that should be documented in actors.md.",
    )


def _check_rule_drift(change: DiffChange, index, bp_name: str) -> DriftAlert | None:
    """Check if a validation rule has a corresponding requirement."""
    # Extract the rule essence from the snippet
    snippet_lower = change.snippet.lower()

    # Check if any requirement mentions similar concepts
    for req_id, req in index.requirements.items():
        req_text = f"{req.statement} {req.test}".lower()
        # Simple word overlap check
        snippet_words = set(re.findall(r"\w{4,}", snippet_lower))
        req_words = set(re.findall(r"\w{4,}", req_text))
        if len(snippet_words & req_words) >= 2:
            return None  # Likely covered by this requirement

    # Only flag substantial validations, not simple null checks
    if any(w in snippet_lower for w in ["must", "invalid", "forbidden", "not allowed", "cannot"]):
        return DriftAlert(
            severity="uncovered",
            summary=f"New validation/business rule in code may not be documented in blueprint requirements",
            category="modified_business_rule",
            code_file=change.file,
            code_line=change.line,
            code_snippet=change.snippet,
            recommendation="Check if this validation implements a business rule that should be in requirements.md with a source.",
        )

    return None


def _check_flow_drift(change: DiffChange, index, bp_name: str) -> DriftAlert | None:
    """Check if a new endpoint/handler has a corresponding scenario."""
    snippet_lower = change.snippet.lower()

    # Extract handler/endpoint name
    name_parts = re.findall(r"\w+", change.name.lower())

    for sname, scenario in index.scenarios.items():
        scenario_words = set(re.findall(r"\w{3,}", sname))
        if set(name_parts) & scenario_words:
            return None  # Likely covered

    return DriftAlert(
        severity="uncovered",
        summary=f"New endpoint/handler in code, no matching scenario in blueprint",
        category="changed_flow",
        code_file=change.file,
        code_line=change.line,
        code_snippet=change.snippet,
        recommendation="Check if this endpoint represents a new user flow that should be documented as a scenario.",
    )


def _check_context_signals(context: str, index, bp_name: str) -> list[DriftAlert]:
    """Check PR title/description for high-level drift signals."""
    alerts: list[DriftAlert] = []
    context_lower = context.lower()

    # Look for mentions of new states
    for match in re.finditer(r"add(?:s|ed|ing)?\s+(?:a\s+)?['\"]?(\w+)['\"]?\s+(?:state|status)", context_lower):
        state_name = match.group(1)
        all_states = set()
        for entity in index.entities.values():
            for s in entity.states:
                all_states.add(s.name.lower())
        if state_name not in all_states:
            alerts.append(DriftAlert(
                severity="drift",
                summary=f"PR mentions adding '{state_name}' state, which is not in the blueprint's domain model",
                category="new_entity_state",
                recommendation=f"Update domain-model.md to include the '{state_name}' state.",
            ))

    # Look for mentions of new actors/roles
    for match in re.finditer(r"(?:new|add)\s+(?:role|actor|user type)\s*:?\s*['\"]?(\w+)", context_lower):
        role_name = match.group(1)
        if role_name.lower() not in {a.lower() for a in index.actors}:
            alerts.append(DriftAlert(
                severity="drift",
                summary=f"PR mentions new role '{role_name}', which is not in the blueprint's actors section",
                category="new_actor",
                recommendation=f"Add '{role_name}' to actors.md with capabilities and restrictions.",
            ))

    return alerts


def _alert_to_dict(alert: DriftAlert) -> dict:
    """Convert a DriftAlert to a serializable dict."""
    result: dict = {
        "severity": alert.severity,
        "summary": alert.summary,
        "category": alert.category,
        "recommendation": alert.recommendation,
    }
    if alert.code_file:
        result["code_evidence"] = {
            "file": alert.code_file,
            "line": alert.code_line,
            "snippet": alert.code_snippet,
        }
    if alert.blueprint_file:
        result["blueprint_evidence"] = {
            "file": alert.blueprint_file,
            "section": alert.blueprint_section,
            "excerpt": alert.blueprint_excerpt,
        }
    return result
