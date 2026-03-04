# Requirements

## Core discipline

**REQ-1.** A blueprint must describe observable system behaviour only — never implementation details. No database names, API endpoints, framework concepts, library names, or UI component names.
*Source: DEC-1 (behaviour over implementation).*
*Test: Every sentence passes the abstraction test: "Would someone need to know this to understand behaviour, without knowing how it is built?"*

**REQ-2.** The blueprint always documents the current state of the system. Version history lives in version control, not in the spec.
*Source: DEC-11 (current version only).*
*Test: No section contains version annotations ("in v1 this works like X, in v2 like Y"). Only current behaviour is described.*

**REQ-3.** One blueprint per system. There are no cross-blueprint conflicts to manage. Conflicts within a blueprint are surfaced to the Spec Owner for resolution.
*Source: DEC-8 (one blueprint per system).*
*Test: No blueprint depends on another blueprint for shared definitions or conflict resolution. Informational cross-references ("related blueprints") are permitted.*

## Terminology

**REQ-4.** Every term in the terminology section must have exactly one definition. No synonyms ("also known as"), no homonyms (one word meaning two things).
*Source: DEC-6 (terminology as first-class section).*
*Test: Grep the blueprint for each term — it appears with one consistent meaning throughout.*

**REQ-5.** When different roles use different names for the same concept, resolve immediately. Pick the business/product term. Flag the alternative for cleanup — do not document it as a synonym.
*Source: Terminology governance, distill skill constraints.*
*Test: No term entry contains "also known as", "equivalent to", or "sometimes called."*

## Scenarios

**REQ-6.** Every scenario must have a trigger, preconditions, numbered steps, outcomes, and at least one error path.
*Source: Elicit skill constraints, scenario completeness.*
*Test: Each scenario file contains all five structural elements.*

**REQ-7.** Every actor defined in the actors section must appear in at least one scenario. Every actor in a scenario must be defined in the actors section.
*Source: Cross-reference consistency.*
*Test: Diff the actor list against scenario actor references — no orphans in either direction.*

**REQ-8.** Every entity referenced in a scenario must be defined in the domain model. Every entity in the domain model should appear in at least one scenario.
*Source: Cross-reference consistency.*
*Test: Diff the entity list against scenario entity references — no orphans in either direction.*

**REQ-9.** Every user story must have at least one delivering scenario.
*Source: Scenario coverage (audit dimension 2).*
*Test: Each story ID maps to at least one scenario that fulfils it.*

## Panel and debate

**REQ-10.** Every panellist must respond to every item in a debate. Silence is not consent.
*Source: Panel invariant (TEAM.md).*
*Test: In every debate report, each panellist has a response for each item.*

**REQ-11.** Maximum two debate cycles per item. If a refined proposal does not reach consensus, it becomes a split.
*Source: Debate protocol (TEAM.md).*
*Test: No debate report contains more than two rounds for a single item.*

**REQ-12.** Split verdicts are deferred to the Spec Owner. The panel presents both positions but does not resolve the disagreement.
*Source: DEC-5 (consensus over voting), panel authority boundary.*
*Test: Split items in debate reports contain both positions and name the Spec Owner as arbiter.*

**REQ-13.** The default 9 panellists are not a closed set. Users can add domain-specific panellists when the domain calls for it. Custom panellists must have a defined perspective, blind spot, and character card.
*Source: DEC-9 (extensible panel).*
*Test: The skill accepts custom panellist definitions and includes them in debate rounds alongside default panellists.*

**REQ-14.** Review and propose use different default dispositions. Review: fix the problem (burden on inaction). Propose: leave the system as described (burden on the proposal).
*Source: Review skill, propose skill.*
*Test: Debate reports reflect the correct disposition — review defaults to change, propose defaults to status quo.*

## Ownership and maintenance

**REQ-15.** A blueprint must have exactly one Spec Owner at all times. Not a team — one person.
*Source: DEC-2 (singular spec ownership).*
*Test: README manifest contains one named individual in the Spec Owner field.*

**REQ-16.** Every open question must have an owner and a deadline.
*Source: Open question invariant.*
*Test: Every entry in questions.md has both fields populated.*

**REQ-17.** Every decision in the decision log must include rationale — not just the outcome. The rationale must explain why, what alternatives were considered, and who decided.
*Source: Decision log invariant.*
*Test: Every entry in decisions.md has a "Why" and "Alternatives considered" section with substantive content.*

**REQ-18.** The skill must detect staleness opportunistically — during operations that already read blueprint files (updates, reviews, audits, elicitation). When the skill is working on a section and encounters content that contradicts the current system or what the Spec Author states, it surfaces the discrepancy immediately. Detection is scoped to what the skill is currently working on, not a full-blueprint scan. Signals: content contradicting author statements, sections referencing entities or flows that no longer exist, and review triggers (major release, team change). Major staleness must be surfaced to the Spec Owner rather than silently fixed.
*Source: DEC-10 (active staleness detection).*
*Test: During any operation that reads blueprint sections, the skill flags stale content with specific evidence ("entity X no longer exists in the system but is referenced in scenario Y"). No standalone staleness scan is required.*

**REQ-19.** Every meaningful change to a blueprint must produce a changelog entry and update the README manifest.
*Source: Update skill, maintenance guide.*
*Test: Changelog entries exist for every version bump; README section statuses match actual file content.*

## Elicitation and distillation integrity

**REQ-20.** The skill must not generate a complete specification from a single sentence or minimal input. Elicitation is a conversation with verification checkpoints after each phase.
*Source: Elicit skill constraints.*
*Test: Elicitation sessions contain multiple verification checkpoints with user confirmations.*

**REQ-21.** When the user says "I don't know," the skill must convert it to an open question with an owner — never invent an answer.
*Source: Elicit skill constraints, DEC-14 (author as domain expert).*
*Test: No section contains fabricated content; "I don't know" responses map to entries in questions.md.*

**REQ-22.** Contradictions must be surfaced immediately when detected. The skill must never silently pick one position — it either resolves the conflict with the author or logs it as an open question with both positions stated.
*Source: Elicit skill constraints (no silent contradictions).*
*Test: No blueprint contains contradictory statements without a corresponding open question or decision.*

**REQ-23.** In solo developer workflows, the Spec Author is the Domain Expert. The skill consults them directly for conflicts, issues, and clarifications. This is normal operation, not a degraded mode.
*Source: DEC-14 (author as domain expert).*
*Test: The skill does not warn about "missing domain expert" when the author is available.*

## Scope integrity

**REQ-24.** When a blueprint exceeds scope-sizing thresholds (>20 terms, >10 disconnected scenarios, unrelated entity clusters, disconnected actor groups), the skill must recommend splitting.
*Source: Scope-sizing constraints (root skill).*
*Test: Scope-sizing check runs during elicitation, distillation, and update.*

## Approach and writing quality

**REQ-25.** The skill adapts its documentation approach (top-down vs bottom-up, depth-first vs breadth-first) based on context. Default is top-down with depth-first threads. The author can override by stating a preference.
*Source: DEC-12 (adaptive documentation approach).*
*Test: The skill does not force a fixed order when the author's natural flow follows a different one.*

**REQ-26.** Diagrams must always be accompanied by text descriptions of the same content. The diagram alone is never sufficient.
*Source: DEC-13 (writing philosophy — dual representation).*
*Test: Every Mermaid diagram in the blueprint has a corresponding text description within the same section.*

**REQ-27.** Granularity scales with complexity. Simple concepts are explained simply; complex concepts receive proportionally more detail. There is no fixed length target.
*Source: DEC-13 (writing philosophy).*
*Test: No section contains filler to reach a length target, and no section compresses a complex topic into insufficient space.*

**REQ-28.** Writing tone must respect the reader's intelligence while acknowledging they do not know the system. Not condescending, not dumbing down, not jargon-heavy. The document assumes a smart person encountering the system for the first time.
*Source: DEC-13 (writing philosophy — respect the reader).*
*Test: A newcomer with relevant domain experience can understand any section without asking the team for clarification. An expert does not feel patronised.*

## Audit integrity

**REQ-29.** The audit must check the declared tier and only audit against the expectations for that tier. Missing Tier 3 sections are not findings for a Tier 1 blueprint.
*Source: Audit skill constraints.*
*Test: Audit reports for Tier 1 blueprints do not flag absence of requirements or decision log content.*

**REQ-30.** Audit findings must be classified as Blocking (must fix before the blueprint is reliable) or Advisory (should fix to improve quality). The classification must be justified.
*Source: Audit skill severity model.*
*Test: Every finding in an audit report has a severity with a one-sentence justification.*
