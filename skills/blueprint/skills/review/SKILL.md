---
name: review
description: Use when reviewing a draft or existing blueprint for quality — missing scenarios, terminology gaps, unclear requirements. Convenes the review panel for a structured debate.
---

<skill name="review">

<brief>Convene the review panel on a draft or existing blueprint to find rough edges, missing coverage, terminology conflicts and quality problems. For proposals to change the described system, use propose instead. For systematic checklist audit without debate, use audit.</brief>

Read the full blueprint. Evaluate against clarity (can any team member understand exactly how the system works?) and completeness (does it cover flows, states, rules and vocabulary someone needs to work confidently?).

Simulate the review panel from <ref src="../../TEAM.md" load="eager"/>. Follow the debate protocol: present, respond, rebut, synthesise, verdict. Every panellist weighs in on every item.

Default disposition: fix the problem if a good fix exists. Burden of proof is on inaction, not on change.

For each item, state: what the problem is (quote the section), where it appears, why it matters, and a candidate fix.

<focus-areas>
<focus-area n="1" name="Terminology">All key terms defined? Each used consistently? Two terms for the same concept, or one term for two things?</focus-area>
<focus-area n="2" name="Scenario coverage">Every actor has at least one scenario? Error paths documented? Every user story has a delivering scenario?</focus-area>
<focus-area n="3" name="Domain model">Every entity has definition, states, named transitions? All relationships captured? Implicit states hiding in booleans?</focus-area>
<focus-area n="4" name="Requirements quality">Testable? Business rules sourced? Non-functional requirements specific with thresholds?</focus-area>
<focus-area n="5" name="Implementation leakage">Describes behaviour or implementation? Flag databases, endpoints, UI components, libraries, architecture patterns.</focus-area>
<focus-area n="6" name="Open questions and decisions">Questions have owners and deadlines? Decision log has rationale? Decisions embedded in requirements that should be in the log?</focus-area>
</focus-areas>

<constraints>
<c rule="No new sections or capabilities beyond blueprint format"/>
<c rule="No style or prose preference feedback"/>
<c rule="Focus on problems affecting a reader's ability to understand the system correctly"/>
</constraints>

Produce the report in the output format specified in <ref src="../../TEAM.md" name="Review panel" load="eager"/>.
<ref src="../../references/section-guide.md" name="Section guide" load="lazy"/>
<ref src="../../references/examples.md" name="Worked examples" load="lazy"/>

</skill>
