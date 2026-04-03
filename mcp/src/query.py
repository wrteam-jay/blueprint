"""Question routing and section-aware search for the query tool."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .parser import get_index
from .types import BlueprintIndex, BlueprintMeta, Citation


@dataclass
class QueryResult:
    """Result of a blueprint query."""

    confidence: str  # "documented", "inferred", "not_documented"
    excerpts: list[Citation] = field(default_factory=list)
    not_covered: str | None = None


def query_blueprint(meta: BlueprintMeta, question: str) -> QueryResult:
    """Answer a natural language question from the blueprint, with citations."""
    index = get_index(meta)
    question_lower = question.lower()
    tokens = _tokenize(question_lower)

    citations: list[Citation] = []

    # 1. Check for requirement/decision/story ID references
    citations.extend(_match_ids(question, index, meta))

    # 2. Check for entity name matches
    citations.extend(_match_entities(tokens, index, meta))

    # 3. Check for term matches
    citations.extend(_match_terms(tokens, index, meta))

    # 4. Check for actor matches
    citations.extend(_match_actors(tokens, index, meta))

    # 5. Route by question type
    if _is_why_question(question_lower):
        citations.extend(_search_decisions(tokens, index, meta))

    if _is_flow_question(question_lower):
        citations.extend(_search_scenarios(tokens, index, meta))

    if _is_rule_question(question_lower):
        citations.extend(_search_requirements(tokens, index, meta))

    # 6. If no targeted matches, do full-text search
    if not citations:
        citations.extend(_fulltext_search(tokens, index, meta))

    # Deduplicate citations by file+line range
    citations = _deduplicate(citations)

    # Limit to top 10 citations
    citations = citations[:10]

    if not citations:
        # Report what the spec does cover in the vicinity
        nearby = _find_nearby_coverage(tokens, index, meta)
        return QueryResult(
            confidence="not_documented",
            not_covered=nearby or "No relevant content found in the blueprint.",
        )

    # Determine confidence
    confidence = "documented" if len(citations) <= 5 else "documented"
    for c in citations:
        if "(inferred)" in c.section:
            confidence = "inferred"
            break

    return QueryResult(confidence=confidence, excerpts=citations)


def lookup_element(
    meta: BlueprintMeta, kind: str, name: str
) -> list[Citation]:
    """Direct lookup of a specific element by type and name/ID."""
    index = get_index(meta)
    name_lower = name.lower()
    bp_name = meta.path.name

    if kind == "term":
        term = index.terms.get(name_lower)
        if term:
            return [Citation(
                file=term.file, section=f"Term: {term.name}",
                line_start=term.line_start, line_end=term.line_end,
                excerpt=term.definition,
            )]
        # Fuzzy match
        for key, term in index.terms.items():
            if name_lower in key or key in name_lower:
                return [Citation(
                    file=term.file, section=f"Term: {term.name}",
                    line_start=term.line_start, line_end=term.line_end,
                    excerpt=term.definition,
                )]

    elif kind == "entity":
        entity = index.entities.get(name_lower)
        if entity:
            parts = [entity.definition]
            if entity.states:
                parts.append(f"States: {', '.join(s.name for s in entity.states)}")
            if entity.invariants:
                parts.append(f"Invariants: {'; '.join(entity.invariants)}")
            return [Citation(
                file=entity.file, section=f"Entity: {entity.name}",
                line_start=entity.line_start, line_end=entity.line_end,
                excerpt="\n".join(parts),
            )]

    elif kind == "scenario":
        for key, scenario in index.scenarios.items():
            if name_lower in key or key in name_lower:
                parts = []
                if scenario.trigger:
                    parts.append(f"Trigger: {scenario.trigger}")
                if scenario.steps:
                    parts.append(f"Steps: {len(scenario.steps)} steps")
                if scenario.outcomes:
                    parts.append(f"Outcomes: {'; '.join(scenario.outcomes[:3])}")
                return [Citation(
                    file=scenario.file, section=f"Scenario: {scenario.name}",
                    line_start=scenario.line_start, line_end=scenario.line_end,
                    excerpt="\n".join(parts) if parts else scenario.name,
                )]

    elif kind == "requirement":
        req = index.requirements.get(name_lower)
        if req:
            parts = [req.statement]
            if req.source:
                parts.append(f"Source: {req.source}")
            if req.test:
                parts.append(f"Test: {req.test}")
            return [Citation(
                file=req.file, section=f"Requirement: {req.id}",
                line_start=req.line_start, line_end=req.line_end,
                excerpt="\n".join(parts),
            )]

    elif kind == "decision":
        dec = index.decisions.get(name_lower)
        if dec:
            parts = [dec.decision]
            if dec.rationale:
                parts.append(f"Why: {dec.rationale}")
            if dec.alternatives:
                parts.append(f"Alternatives: {dec.alternatives}")
            return [Citation(
                file=dec.file, section=f"Decision: {dec.id}",
                line_start=dec.line_start, line_end=dec.line_end,
                excerpt="\n".join(parts),
            )]

    elif kind == "actor":
        actor = index.actors.get(name_lower)
        if not actor:
            # Try fuzzy
            for key, a in index.actors.items():
                if name_lower in key or key in name_lower:
                    actor = a
                    break
        if actor:
            parts = [actor.description]
            if actor.can_do:
                parts.append(f"Can do: {'; '.join(actor.can_do)}")
            if actor.cannot_do:
                parts.append(f"Cannot do: {'; '.join(actor.cannot_do)}")
            return [Citation(
                file=actor.file, section=f"Actor: {actor.name}",
                line_start=actor.line_start, line_end=actor.line_end,
                excerpt="\n".join(parts),
            )]

    elif kind == "story":
        story = index.stories.get(name_lower)
        if story:
            return [Citation(
                file=story.file, section=f"Story: {story.id}",
                line_start=story.line_start, line_end=story.line_end,
                excerpt=story.text,
            )]

    elif kind == "question":
        oq = index.questions.get(name_lower)
        if oq:
            parts = [oq.question]
            if oq.owner:
                parts.append(f"Owner: {oq.owner}")
            if oq.blocks:
                parts.append(f"Blocks: {oq.blocks}")
            return [Citation(
                file=oq.file, section=f"Question: {oq.id}",
                line_start=oq.line_start, line_end=oq.line_end,
                excerpt="\n".join(parts),
            )]

    return []


# -- Question type detection --


def _is_why_question(q: str) -> bool:
    return any(w in q for w in ["why", "reason", "rationale", "motivation", "decided"])


def _is_flow_question(q: str) -> bool:
    return any(w in q for w in [
        "what happens", "how does", "how do", "flow", "process", "step",
        "when", "trigger", "scenario", "sequence",
    ])


def _is_rule_question(q: str) -> bool:
    return any(w in q for w in [
        "must", "allowed", "can a", "cannot", "forbidden", "required",
        "rule", "constraint", "requirement", "limit", "valid",
    ])


# -- Internal search functions --


def _match_ids(question: str, index: BlueprintIndex, meta: BlueprintMeta) -> list[Citation]:
    """Match explicit IDs like REQ-1, DEC-3, US-5, OQ-2."""
    citations: list[Citation] = []

    for match in re.finditer(r"(REQ-\d+|DEC-\d+|US-\d+|OQ-\d+)", question, re.IGNORECASE):
        ref_id = match.group(1).lower()
        if ref_id.startswith("req-") and ref_id in index.requirements:
            req = index.requirements[ref_id]
            citations.append(Citation(
                file=req.file, section=f"Requirement: {req.id}",
                line_start=req.line_start, line_end=req.line_end,
                excerpt=req.statement,
            ))
        elif ref_id.startswith("dec-") and ref_id in index.decisions:
            dec = index.decisions[ref_id]
            citations.append(Citation(
                file=dec.file, section=f"Decision: {dec.id}",
                line_start=dec.line_start, line_end=dec.line_end,
                excerpt=f"{dec.decision} — {dec.rationale}" if dec.rationale else dec.decision,
            ))
        elif ref_id.startswith("us-") and ref_id in index.stories:
            story = index.stories[ref_id]
            citations.append(Citation(
                file=story.file, section=f"Story: {story.id}",
                line_start=story.line_start, line_end=story.line_end,
                excerpt=story.text,
            ))
        elif ref_id.startswith("oq-") and ref_id in index.questions:
            oq = index.questions[ref_id]
            citations.append(Citation(
                file=oq.file, section=f"Question: {oq.id}",
                line_start=oq.line_start, line_end=oq.line_end,
                excerpt=oq.question,
            ))

    return citations


def _match_entities(tokens: set[str], index: BlueprintIndex, meta: BlueprintMeta) -> list[Citation]:
    """Match entity names in the question."""
    citations: list[Citation] = []
    for name, entity in index.entities.items():
        name_tokens = set(name.lower().split())
        if name_tokens & tokens:
            # Check if any entity state is also mentioned
            mentioned_states = [s for s in entity.states if s.name.lower() in tokens]
            excerpt = entity.definition
            if mentioned_states:
                state_info = "; ".join(f"{s.name}: {s.description}" for s in mentioned_states)
                excerpt = f"{entity.definition}\nMentioned states — {state_info}"
            elif entity.states:
                excerpt = f"{entity.definition}\nStates: {', '.join(s.name for s in entity.states)}"

            citations.append(Citation(
                file=entity.file, section=f"Entity: {entity.name}",
                line_start=entity.line_start, line_end=entity.line_end,
                excerpt=excerpt,
            ))

            # Also find scenarios that reference this entity
            for sname, scenario in index.scenarios.items():
                scenario_text = _get_section_content(index, scenario.file)
                if scenario_text and name in scenario_text.lower():
                    citations.append(Citation(
                        file=scenario.file, section=f"Scenario: {scenario.name}",
                        line_start=scenario.line_start, line_end=scenario.line_end,
                        excerpt=f"Trigger: {scenario.trigger}" if scenario.trigger else scenario.name,
                    ))

    return citations


def _match_terms(tokens: set[str], index: BlueprintIndex, meta: BlueprintMeta) -> list[Citation]:
    """Match terminology entries."""
    citations: list[Citation] = []
    for name, term in index.terms.items():
        name_tokens = set(name.lower().split())
        if name_tokens & tokens and name_tokens.issubset(tokens | _stop_words()):
            citations.append(Citation(
                file=term.file, section=f"Term: {term.name}",
                line_start=term.line_start, line_end=term.line_end,
                excerpt=term.definition[:300],
            ))
    return citations


def _match_actors(tokens: set[str], index: BlueprintIndex, meta: BlueprintMeta) -> list[Citation]:
    """Match actor names."""
    citations: list[Citation] = []
    for name, actor in index.actors.items():
        name_tokens = set(name.lower().split())
        if name_tokens.issubset(tokens):
            citations.append(Citation(
                file=actor.file, section=f"Actor: {actor.name}",
                line_start=actor.line_start, line_end=actor.line_end,
                excerpt=actor.description[:200],
            ))
    return citations


def _search_decisions(tokens: set[str], index: BlueprintIndex, meta: BlueprintMeta) -> list[Citation]:
    """Search decision log for relevant decisions."""
    citations: list[Citation] = []
    for dec_id, dec in index.decisions.items():
        text = f"{dec.decision} {dec.rationale} {dec.alternatives}".lower()
        score = sum(1 for t in tokens if t in text and t not in _stop_words())
        if score >= 2:
            citations.append(Citation(
                file=dec.file, section=f"Decision: {dec.id}",
                line_start=dec.line_start, line_end=dec.line_end,
                excerpt=f"{dec.decision}\nWhy: {dec.rationale}" if dec.rationale else dec.decision,
            ))
    return citations


def _search_scenarios(tokens: set[str], index: BlueprintIndex, meta: BlueprintMeta) -> list[Citation]:
    """Search scenarios for relevant flows."""
    citations: list[Citation] = []
    for sname, scenario in index.scenarios.items():
        text = _get_section_content(index, scenario.file) or ""
        text_lower = text.lower()
        score = sum(1 for t in tokens if t in text_lower and t not in _stop_words())
        if score >= 2:
            parts = []
            if scenario.trigger:
                parts.append(f"Trigger: {scenario.trigger}")
            if scenario.steps:
                parts.append(f"{len(scenario.steps)} steps")
            citations.append(Citation(
                file=scenario.file, section=f"Scenario: {scenario.name}",
                line_start=scenario.line_start, line_end=scenario.line_end,
                excerpt="\n".join(parts) if parts else scenario.name,
            ))
    return citations


def _search_requirements(tokens: set[str], index: BlueprintIndex, meta: BlueprintMeta) -> list[Citation]:
    """Search requirements for relevant rules."""
    citations: list[Citation] = []
    for req_id, req in index.requirements.items():
        text = f"{req.statement} {req.source} {req.test}".lower()
        score = sum(1 for t in tokens if t in text and t not in _stop_words())
        if score >= 2:
            citations.append(Citation(
                file=req.file, section=f"Requirement: {req.id}",
                line_start=req.line_start, line_end=req.line_end,
                excerpt=req.statement,
            ))
    return citations


def _fulltext_search(tokens: set[str], index: BlueprintIndex, meta: BlueprintMeta) -> list[Citation]:
    """Full-text search across all sections as fallback."""
    citations: list[Citation] = []
    meaningful_tokens = tokens - _stop_words()
    if not meaningful_tokens:
        return citations

    for section_name, section in index.sections.items():
        if not section.content:
            continue

        content_lower = section.content.lower()
        score = sum(1 for t in meaningful_tokens if t in content_lower)

        if score >= 2:
            # Find the most relevant paragraph
            paragraphs = section.content.split("\n\n")
            best_para = ""
            best_score = 0
            for para in paragraphs:
                para_lower = para.lower()
                p_score = sum(1 for t in meaningful_tokens if t in para_lower)
                if p_score > best_score:
                    best_score = p_score
                    best_para = para.strip()

            if best_para:
                # Find line number of best paragraph
                lines = section.content.splitlines()
                para_start = 1
                for i, line in enumerate(lines, 1):
                    if best_para[:50] in line or line.strip() in best_para:
                        para_start = i
                        break

                citations.append(Citation(
                    file=section.file, section=section_name,
                    line_start=para_start, line_end=para_start + best_para.count("\n"),
                    excerpt=best_para[:400],
                ))

    # Sort by relevance (number of matching tokens)
    return sorted(citations, key=lambda c: -sum(1 for t in meaningful_tokens if t in c.excerpt.lower()))[:5]


def _find_nearby_coverage(tokens: set[str], index: BlueprintIndex, meta: BlueprintMeta) -> str:
    """When a question can't be answered, report what the spec does cover nearby."""
    meaningful = tokens - _stop_words()
    covered: list[str] = []

    for t in meaningful:
        # Check entities
        for name, entity in index.entities.items():
            if t in name:
                states = ", ".join(s.name for s in entity.states) if entity.states else "no states defined"
                covered.append(f"Entity '{entity.name}' exists with states: {states}")

        # Check terms
        for name, term in index.terms.items():
            if t in name:
                covered.append(f"Term '{term.name}' is defined: {term.definition[:100]}")

        # Check scenarios
        for name, scenario in index.scenarios.items():
            if t in name:
                covered.append(f"Scenario '{scenario.name}' exists")

    if covered:
        return "The blueprint covers the following related topics:\n- " + "\n- ".join(covered[:5])
    return ""


def _get_section_content(index: BlueprintIndex, file_ref: str) -> str | None:
    """Get raw content for a section by its file reference."""
    for section in index.sections.values():
        if section.file == file_ref or file_ref.endswith(section.file):
            return section.content

    # For scenario files, read directly
    # The content isn't stored in sections for individual scenario files,
    # so we return None and let the caller handle it
    return None


def _tokenize(text: str) -> set[str]:
    """Extract meaningful tokens from text."""
    words = re.findall(r"[a-z][a-z0-9_-]+", text.lower())
    return set(words)


def _stop_words() -> set[str]:
    return {
        "the", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would",
        "could", "should", "may", "might", "shall", "can",
        "not", "no", "nor", "but", "and", "or", "so", "if", "then",
        "than", "too", "very", "just", "about", "above", "after",
        "again", "all", "also", "an", "any", "as", "at", "because",
        "before", "between", "both", "by", "each", "for", "from",
        "get", "got", "here", "how", "in", "into", "it", "its",
        "more", "most", "of", "on", "only", "other", "our", "out",
        "over", "own", "same", "she", "he", "they", "them", "there",
        "this", "that", "these", "those", "through", "to", "under",
        "up", "us", "we", "what", "when", "where", "which", "while",
        "who", "whom", "why", "with", "you", "your",
        "does", "what", "happen", "happens", "tell", "me", "about",
        "explain", "describe", "show",
    }


def _deduplicate(citations: list[Citation]) -> list[Citation]:
    """Remove duplicate citations based on file + line range."""
    seen: set[str] = set()
    unique: list[Citation] = []
    for c in citations:
        key = f"{c.file}:{c.line_start}-{c.line_end}"
        if key not in seen:
            seen.add(key)
            unique.append(c)
    return unique
