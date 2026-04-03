"""Data models for the blueprint MCP server."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Citation:
    """A reference to a specific location in a blueprint file."""

    file: str
    section: str
    line_start: int
    line_end: int
    excerpt: str

    def format(self) -> str:
        return f"[{self.file}:{self.line_start}-{self.line_end}] {self.excerpt}"


@dataclass
class Term:
    name: str
    definition: str
    file: str
    line_start: int
    line_end: int


@dataclass
class EntityState:
    name: str
    description: str


@dataclass
class EntityTransition:
    from_state: str
    to_state: str
    trigger: str


@dataclass
class Entity:
    name: str
    definition: str
    states: list[EntityState] = field(default_factory=list)
    transitions: list[EntityTransition] = field(default_factory=list)
    invariants: list[str] = field(default_factory=list)
    relationships: list[str] = field(default_factory=list)
    file: str = ""
    line_start: int = 0
    line_end: int = 0


@dataclass
class Scenario:
    name: str
    file: str
    trigger: str = ""
    preconditions: list[str] = field(default_factory=list)
    actors: list[str] = field(default_factory=list)
    entities: list[str] = field(default_factory=list)
    steps: list[str] = field(default_factory=list)
    outcomes: list[str] = field(default_factory=list)
    error_paths: list[str] = field(default_factory=list)
    line_start: int = 0
    line_end: int = 0


@dataclass
class Requirement:
    id: str
    statement: str
    source: str = ""
    test: str = ""
    file: str = ""
    line_start: int = 0
    line_end: int = 0


@dataclass
class Decision:
    id: str
    decision: str
    rationale: str = ""
    decided_by: str = ""
    date: str = ""
    alternatives: str = ""
    file: str = ""
    line_start: int = 0
    line_end: int = 0


@dataclass
class Actor:
    name: str
    description: str
    can_do: list[str] = field(default_factory=list)
    cannot_do: list[str] = field(default_factory=list)
    file: str = ""
    line_start: int = 0
    line_end: int = 0


@dataclass
class Story:
    id: str
    text: str
    evidence: str = ""
    file: str = ""
    line_start: int = 0
    line_end: int = 0


@dataclass
class OpenQuestion:
    id: str
    question: str
    owner: str = ""
    deadline: str = ""
    blocks: str = ""
    file: str = ""
    line_start: int = 0
    line_end: int = 0


@dataclass
class SectionInfo:
    """Metadata about a blueprint section file."""

    name: str
    file: str
    status: str = ""
    content: str = ""
    line_count: int = 0


@dataclass
class BlueprintIndex:
    """Searchable index of a parsed blueprint."""

    terms: dict[str, Term] = field(default_factory=dict)
    entities: dict[str, Entity] = field(default_factory=dict)
    scenarios: dict[str, Scenario] = field(default_factory=dict)
    requirements: dict[str, Requirement] = field(default_factory=dict)
    decisions: dict[str, Decision] = field(default_factory=dict)
    actors: dict[str, Actor] = field(default_factory=dict)
    stories: dict[str, Story] = field(default_factory=dict)
    questions: dict[str, OpenQuestion] = field(default_factory=dict)
    sections: dict[str, SectionInfo] = field(default_factory=dict)
    built_at: float = 0.0


@dataclass
class BlueprintMeta:
    """Blueprint manifest metadata parsed from README.md."""

    name: str
    path: Path
    status: str = "Draft"
    version: str = ""
    spec_owner: str = ""
    tier: int = 0
    section_statuses: dict[str, str] = field(default_factory=dict)
    related_blueprints: list[str] = field(default_factory=list)


@dataclass
class DriftAlert:
    """A single drift detection finding."""

    severity: str  # "drift" or "uncovered"
    summary: str
    category: str
    code_file: str = ""
    code_line: int = 0
    code_snippet: str = ""
    blueprint_file: str = ""
    blueprint_section: str = ""
    blueprint_excerpt: str = ""
    recommendation: str = ""


@dataclass
class HealthIssue:
    """A single health check finding."""

    kind: str  # "cross_reference", "empty_section", "staleness", "tier_mismatch"
    message: str
    file: str = ""
    section: str = ""


INDEX_TTL = 30  # seconds


def is_index_stale(index: BlueprintIndex) -> bool:
    return (time.time() - index.built_at) > INDEX_TTL
