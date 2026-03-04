# Scenario: Review a blueprint

## Trigger

A Spec Owner invokes the skill to review an existing blueprint for quality — clarity, completeness, consistency, and adherence to core discipline.

## Preconditions

- A blueprint exists with at least Tier 1 content (Context, Scope, Actors, Terminology).
- The blueprint has been read in full before the panel convenes.

## Steps

1. **Read the full blueprint.** The skill reads every section file to understand the complete picture.
2. **Identify review items.** The skill evaluates the blueprint against six focus areas:
   - Terminology — all terms defined? Consistent usage? Synonyms or homonyms?
   - Scenario coverage — every actor in a scenario? Error paths? Every story delivered?
   - Domain model — every entity has states, transitions, invariants? Implicit states surfaced?
   - Requirements quality — testable? Business rules sourced? Non-functional with thresholds?
   - Implementation leakage — databases, endpoints, UI components, libraries in the spec?
   - Open questions and decisions — owners assigned? Rationale recorded?
3. **Convene the panel.** Standard mode (5 panellists) by default. Quick (3) for trivial reviews, Full (9) if requested.
4. **Debate each item.** For each finding, the debate protocol runs:
   - Present the issue with context and a candidate fix.
   - Each panellist responds in character.
   - Panellists rebut each other (one round).
   - Neutral synthesis of where the panel stands.
   - Verdict: adopt, reject, refine, or split.
5. **Produce the debate report.** Summary, items debated with verdicts, deferred items for Spec Owner.

## Default disposition

Fix the problem if a good fix exists. Burden of proof is on inaction, not on change.

## Outcomes

- A debate report listing every finding, the panel's discussion, and the verdict for each.
- Actionable fixes for consensus-adopt items.
- Split items presented with both positions for the Spec Owner to resolve.

## Error paths

- **Blueprint is too incomplete to review.** The skill identifies the current tier and recommends completing prerequisite sections before review. Does not review placeholder content. States which sections need content before a meaningful review can occur.
- **All items reach consensus.** Not an error — a clean report with no deferred items. The report still summarises what was reviewed and why no issues were found.
- **Panel cannot converge on any item.** Every unresolved item becomes a split, deferred to the Spec Owner with both positions faithfully presented. If the majority of items are splits, the report flags this as a signal that the blueprint may need more foundational work rather than item-by-item fixes.
- **Review finds a fundamental problem.** A structural issue (e.g., the scope is wrong, the actors are misidentified, terminology is built on a misconception) that invalidates downstream sections. The skill stops reviewing subsequent items and escalates: "A foundational issue was found in [section]. Downstream sections depend on this and should be re-evaluated after this is resolved."
- **Review reveals implementation leakage throughout.** Many sections contain implementation details rather than behaviour. Rather than debating each instance, the skill identifies the pattern and recommends a systematic pass to lift the entire blueprint to the behaviour level.
- **Stale content detected during review.** The blueprint describes behaviour that no longer matches the system. The skill flags the discrepancy and recommends an update before continuing the review — reviewing stale content produces findings against the wrong baseline.
