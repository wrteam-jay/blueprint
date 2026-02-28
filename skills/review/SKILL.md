---
name: review
description: Use when reviewing a draft or existing blueprint for quality — missing scenarios, terminology gaps, unclear requirements. Convenes the review panel for a structured debate.
---

# Blueprint Review

Use this skill to convene the review panel on a draft or existing blueprint — to find rough edges, missing coverage, terminology conflicts and quality problems. For proposals to change the system described in a blueprint, use the `propose` skill instead.

This skill convenes the review panel for a structured debate. For a systematic checklist audit without panel debate, use the `audit` skill.

---

You are reviewing a blueprint document. A blueprint is a living specification that captures how a system works: its actors, its terminology, its user stories, its flows and scenarios, its domain model, and its requirements. The goal is for it to be the single source of truth that the whole team — product, engineering, design, support — can read, discuss and maintain.

Read the full blueprint. Then evaluate it against two goals: **clarity** (can any team member read this and understand exactly how the system works?) and **completeness** (does it cover the flows, states, rules and vocabulary someone would need to work confidently with this system?).

Simulate the review panel described in [TEAM.md](../../TEAM.md). Follow the debate protocol: present, respond, rebut, synthesise, verdict. Every panellist must weigh in on every item. Produce the report in the output format specified in [TEAM.md](../../TEAM.md).

The default disposition is to fix the problem if a good fix exists. The burden of proof is on inaction, not on the change. A blueprint with known gaps is less useful than one without them.

For each item found, state:
- **What the problem is** — be specific. Quote the section or sentence.
- **Where it appears** — section name and item identifier if present.
- **Why it matters** — what goes wrong for a reader or implementer if this is not fixed.
- **A candidate fix** — what a resolution would look like. If the fix requires a stakeholder decision, name the decision and who should make it.

Focus areas for this review:

1. **Terminology.** Are all key terms defined? Is each term used consistently throughout the document? Are there two terms for the same concept, or one term used to mean two different things?

2. **Scenario coverage.** Does every actor have at least one scenario tracing their primary journey? Are error paths and edge cases documented, not just the happy path? Does every user story have a scenario that delivers it?

3. **Domain model.** Does every entity have a definition, a set of states, and named transitions? Are all relationships captured? Are there implicit states hiding in boolean fields or nullable timestamps?

4. **Requirements quality.** Are requirements testable — can you write an acceptance test against each one? Are business rules sourced — do they name the policy, regulation or decision they come from? Are non-functional requirements specific, with thresholds, not vague ("should be fast")?

5. **Implementation leakage.** Does the blueprint describe behaviour, or does it describe implementation? Flag any mention of databases, API endpoints, UI components, libraries or architectural patterns that do not belong at the behaviour level.

6. **Open questions and decisions.** Do open questions have owners and deadlines? Does the decision log capture rationale, not just outcomes? Are there decisions embedded in requirements that should be in the decision log?

Do not propose new sections or capabilities beyond what the blueprint format already supports. Do not flag matters of style or prose preference. Focus on problems that affect a reader's ability to understand the system correctly.

---

## References

- [Review panel](../../TEAM.md) — panellist roles, debate protocol, verdicts
- [Section guide](../../references/section-guide.md) — what each section must contain
- [Worked examples](../../references/examples.md) — before/after examples for every section type
