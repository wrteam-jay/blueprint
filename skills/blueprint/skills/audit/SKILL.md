---
name: audit
description: Use when reviewing an existing blueprint for gaps, missing flows, terminology conflicts, coverage of error cases, or untestable requirements.
---

<skill name="audit">

<brief>Structured checklist audit of an existing blueprint — evaluates systematically against six dimensions, produces a findings report. Not a rewrite. For panel debate with multiple perspectives, use review instead.</brief>

Read the entire blueprint before producing findings. Isolated observations often disappear when the document is read as a whole; apparent gaps may be covered elsewhere. Check the stated completion tier in README.md — audit against what the tier promises. A Tier 1 blueprint intentionally lacks scenarios.

<dimension n="1" name="Terminology consistency">
Terminology conflicts are the most damaging class of blueprint problem.

Check: same concept under multiple names, same term meaning different things in different sections, Terminology entries not used consistently in Scenarios/Requirements, terms in Scenarios/Requirements not in Terminology.

For each conflict: name the conflicting terms, state which sections each appears in, identify the canonical term, state what needs to change. Do not leave a conflict annotated as "equivalent to" — resolution means one term survives everywhere.
</dimension>

<dimension n="2" name="Scenario coverage">
For each actor: at least one scenario shows their primary journey, permissions demonstrated, restrictions demonstrated.

For each user story: at least one scenario traces how the system delivers the outcome.

For each entity state: at least one scenario shows entry, at least one shows exit (unless terminal).

Error path coverage for each scenario: happy path documented, primary failure modes documented, timeout edge cases covered, multi-actor interactions show each actor's view.
</dimension>

<dimension n="3" name="Domain model completeness">
Each entity: has definition, has states listed (if lifecycle), has named transitions with triggers, has named relationships with cardinality, has lifecycle owner.

Model as whole: every entity in scenarios appears in domain model and vice versa, no unreachable terminal states, no implicit states hiding in boolean combinations.
</dimension>

<dimension n="4" name="Requirements quality">
Testability: every functional requirement must support writing a pass/fail test.

<table name="weasel-words">
<row word="easily" problem="no threshold" fix="state measurable user outcome"/>
<row word="fast" problem="no metric" fix="name response time at specific load"/>
<row word="secure" problem="no definition" fix="name specific controls or standard"/>
<row word="appropriate" problem="undefined" fix="name the actual condition"/>
<row word="should (for musts)" problem="signals optionality" fix="replace with must"/>
<row word="flexible" problem="undefined" fix="state what must be configurable"/>
<row word="robust" problem="undefined" fix="state failure scenarios to handle"/>
</table>

Sourcing: every business rule needs a source — policy, regulation, stakeholder decision. "Users with free plans cannot create more than 3 projects" — why? Product decision? Pricing constraint? Infrastructure limit? The source determines whether the rule can be changed and by whom.

Coverage: scan scenarios for implied constraints not stated in requirements:
- A scenario shows a deadline — is the duration in Requirements?
- A scenario shows a role restriction — is it in Business Rules?
- A scenario shows a notification — is the triggering condition and recipient in Requirements?
</dimension>

<dimension n="5" name="Decision log and open questions">
Decision log: decisions recorded with rationale (not just outcome), contested decisions have both positions, each has date and owner.

Open questions: specific enough to be answerable (not "figure out the pricing model"), each has an owner, each has deadline or blocking note. Open questions without owners do not get resolved.

A decision log without rationale is almost useless. "We decided to use soft delete" is less valuable than "We decided to use soft delete because audit requirements mean we cannot lose the record."
</dimension>

<dimension n="6" name="Implementation leakage">
A blueprint must not contain implementation decisions. Every one is a constraint the team did not consciously impose.
<table name="implementation-signals">
<row found="Database or storage technology" problem="implementation choice"/>
<row found="API endpoint paths or methods" problem="interface design"/>
<row found="Specific libraries or frameworks" problem="technology choice"/>
<row found="UI element descriptions" problem="design decision"/>
<row found="Internal service names" problem="architecture detail"/>
<row found="Data types or schema details" problem="implementation"/>
<row found="Specific vendor when category suffices" problem="usually implementation"/>
</table>

Exception: when a vendor/technology is a genuine business constraint, name it and source it. The test is whether a business stakeholder made this decision, not an engineer.
</dimension>

<template name="audit-report">
# Blueprint Audit: [Name]

**Blueprint version audited:** [version]
**Audit date:** [date]

---

## Summary

[X] findings across [Y] dimensions. [Z] blocking, [W] advisory.

| Dimension | Findings | Blocking |
|-----------|----------|----------|
| Terminology | | |
| Scenario coverage | | |
| Domain model | | |
| Requirements quality | | |
| Decision log / open questions | | |
| Implementation leakage | | |

---

## Blocking findings

### [ID]: [Short title]

**Location:** Section [X], [specific element]
**Problem:** [What is wrong and why]
**Impact:** [What goes wrong if not fixed]
**Fix needed:** [Shape of resolution]

---

## Advisory findings

[Same format, lower severity]

---

## Open questions flagged during audit

- [Question] — Owner: [who], Deadline: [date]
</template>

<table name="severity-guide">
Blocking: terminology conflicts, missing primary journey scenarios, entity states with no entry/exit path, requirements with no acceptance criteria, ownerless blocking open questions, implementation decisions as requirements.

Advisory: missing minor edge case error paths, imprecise but testable requirements, unclear but unambiguous terminology, missing rationale for stable decisions, minor implementation leakage.
</table>

<ref src="../../references/section-guide.md" name="Section guide" load="lazy"/>
<ref src="../../references/diagram-guide.md" name="Diagram guide" load="lazy"/>

</skill>
