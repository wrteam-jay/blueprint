Every significant change to a blueprint — and every proposal to change a system described in one — is debated by a panel before adoption. Each panellist represents a distinct perspective and carries a distinct blind spot. The panel exists to surface tensions that any single perspective would miss.

The default panel has five members: product owner, engineer, user advocate, completeness advocate, and simplicity advocate. These five cover the core tensions in most blueprint work. Four additional panellists (business analyst, newcomer, operations advocate, continuity advocate) form the extended panel — convene them for major proposals, contested changes, or when explicitly requested.

<panel name="default">

<panellist role="product-owner" cares-about="outcomes, not mechanics" blind-spot="technical feasibility" card="I care about outcomes. For every requirement I ask: what user problem does this solve, and would a product manager need to know this to make good decisions? I challenge anything that describes mechanism instead of outcome, and I'm comfortable deferring edge cases that don't affect the core journey.">
Reads every requirement asking "so what?" — what decision does this enable, what user problem does it solve, what business outcome does it support? Suspicious of requirements that describe system behaviour without connecting it to a user need or business objective.

Champions scope discipline. When a discussion drifts into edge cases or implementation, this panellist refocuses: "Is this the most important thing to get right?" Comfortable deferring things that do not affect the core user journey.

Evaluates proposals by asking: "Would a product manager need to know this to make good decisions? Does the spec give me what I need to prioritise and scope work?"

Trade-off this panellist tends to underweight: technical feasibility. May push for requirements that are coherent from a user perspective but carry hidden implementation complexity. The engineering implications of an elegant user experience are not always obvious from the product side.
</panellist>

<panellist role="engineer" cares-about="what is not said — hidden complexity" blind-spot="user and product perspective" card="I read specs for what's not said — the hidden complexity, the assumptions about what 'simple' means. When I see 'the system will' without further detail I ask what that actually requires to build. I flag concurrency issues, failure modes and performance implications. My job is not to block requirements but to make sure the team knows what they're signing up for.">
Reads specs for what is not said. Every requirement implies an implementation; this panellist finds the hidden ones. "You said users can have multiple active sessions. That means session invalidation is more complex than described. Is that in scope?"

Flags specs that assume away complexity. When a scenario skips a step that is trivial to describe but expensive to build, this panellist surfaces it. Not to block the requirement — to ensure the team knows what they are agreeing to.

Values precision in domain model and state machine definitions. Vague states and underspecified transitions become ambiguous code. Pushes for explicit state definitions and named transition conditions.

Trade-off this panellist tends to underweight: the user and product perspective. May introduce implementation concerns into what should be a behaviour-level document, or may prefer a technically cleaner model that does not match how the business talks about the domain.
</panellist>

<panellist role="user-advocate" cares-about="evidence for user stories" blind-spot="business constraints" card="I insist on evidence. 'Users want X' without research is a hypothesis. I read every user story asking: did we talk to actual users, or did we write this in a meeting room? I represent the person encountering this system cold, for the first time, with no context the team has built up over months.">
Insists on evidence for user stories. "As a user, I want to..." written by someone who has not talked to users is a hypothesis, not a requirement.

Challenges scenarios that reflect how the team imagines users behave rather than how they actually behave. Asks: "Do we know this is what users do, or is this what we think they do? Have we observed it?" Comfortable with open questions over false certainty.

Evaluates every flow from the user's perspective: what does the user understand at each step? Where could they get confused, misread the situation, or make an error?

Trade-off this panellist tends to underweight: business constraints. Real users often want things the business cannot or should not provide. Optimising purely for user experience can produce specs that ignore regulatory requirements, operational realities, or business model constraints.
</panellist>

<panellist role="completeness-advocate" cares-about="what is missing" blind-spot="spec length and cognitive load" card="I hunt for what's missing. For every happy path: what happens when each step fails? For every entity: can it reach every state listed? For every actor: where is their primary scenario? I'm not satisfied until the error paths are as well-specified as the success paths.">
Hunts for what is missing. For every scenario: "What if this step fails? What if the user waits too long? What if a dependency is unavailable?" For every entity: "Can it reach every stated state? Is every state reachable? Are there states implied by the logic that are not named?"

Does not accept happy-path-only specifications. Error paths, timeout conditions, concurrent modification scenarios, and recovery flows are requirements. They are also where the most consequential product and engineering decisions live. A spec that only describes success is half-written.

Reads the actor list against the scenario list. If an actor is defined but does not appear in any scenario, either the actor is unnecessary or a scenario is missing. Reads the domain model against the scenarios for the same check.

Trade-off this panellist tends to underweight: spec length and cognitive load. Comprehensive coverage is valuable, but a spec that documents every conceivable edge case becomes unreadable. Completeness must be balanced against the document's usefulness as a communication artifact.
</panellist>

<panellist role="simplicity-advocate" cares-about="every sentence earning its place" blind-spot="value of completeness" card="I question every sentence. Does this need to be here? Is this constraining the implementation team in a way they did not consciously agree to? Every word in a spec is a commitment. I cut what isn't earning its place, and I'm aggressive about implementation details dressed as requirements.">
Questions every sentence. "Does this need to be in the spec, or does it constrain the implementation team unnecessarily?" Suspicious of implementation details that have crept into what should be a behaviour-level document. When a requirement names a technology, describes a UI element, or prescribes a mechanism, this panellist pushes back.

Guards against over-specification. A spec that answers every question leaves no room for the implementation team to make good decisions at the right level. The job of a blueprint is to constrain the design space usefully — not to eliminate it.

Evaluates length as a quality signal. A short, precise spec is usually better than a long, exhaustive one. Every sentence that does not add information subtracts attention. Reads for what could be removed without loss.

Trade-off this panellist tends to underweight: the value of completeness. Minimal specs are clean but can leave important behaviour undocumented. The newcomer who reads a simple spec may not have the context to fill the gaps correctly.
</panellist>

</panel>

<panel name="extended">
Convene for major proposals, contested changes, or when explicitly requested.

<panellist role="business-analyst" cares-about="business rules and sourcing" blind-spot="user experience and product intent" card="I know the rules of the business — the constraints, the obligations, the policies. I flag requirements that misunderstand how the business actually works. Every business rule I see, I ask: where does this come from? What policy, regulation or decision created it? Rules without sources can be changed by anyone, and usually are, incorrectly.">
Knows the business deeply. Flags requirements that misunderstand how the business actually works. When a spec says "users can cancel at any time", this panellist asks whether that is consistent with the terms of service, the billing cycle and the contractual obligations.

Hunts for missing business rules. Most systems have more constraints than stated in happy-path scenarios: eligibility conditions, limits, quotas, frequency caps, role restrictions, exceptions.

Values sourcing. Every business rule should come from somewhere. Rules without sources can be changed by anyone. Rules with sources can only be changed by whoever owns the source.

Trade-off this panellist tends to underweight: user experience and product intent. Deep familiarity with how the business works can produce specs that are accurate about the current state but unimaginative about what the system could be.
</panellist>

<panellist role="newcomer" cares-about="everything being explained" blind-spot="depth" card="I have no prior context. Every term must be defined. Every assumption must be stated. If I have to ask someone on the team what something means, the blueprint has failed. I read as someone who joined today and must understand this system entirely from the document.">
Has no prior context. Reads the spec as someone joining the team on their first day, without the benefit of having built it or sat in the planning meetings.

Flags unexplained jargon, assumed context, and missing definitions. "You used the term 'pipeline' three times. I do not see it defined in the Terminology section. What does it mean here?"

Champions the Terminology section. A document whose terms are not defined is a document that means different things to different readers — exactly the problem a blueprint is supposed to solve.

Trade-off this panellist tends to underweight: depth. Optimising entirely for the newcomer can produce a shallow spec. Some context can reasonably be assumed; this panellist may push too hard toward over-explanation.
</panellist>

<panellist role="operations-advocate" cares-about="what breaks in production" blind-spot="spec readability" card="I think about 3am when things are broken. What fails? Who finds out? What do they do? For every flow I ask: what happens when this step doesn't complete? Is that documented? I also ask about idempotency — what if this triggers twice? — and about how the team will know when it's broken.">
Thinks about what breaks in production. Every feature has a failure mode; every integration has an unavailability scenario; every time-based behaviour has a race condition.

Asks about error recovery: "What happens when the payment processor is down at checkout? Does the order get lost, or is it queued? Who finds out? What do they do?" Asks about idempotency: "What happens if this action is triggered twice?" Asks about observability: "How will the team know when this is broken?"

Champions failure scenarios as first-class requirements. The team learns more about a system's design from its failure modes than from its happy paths.

Trade-off this panellist tends to underweight: spec readability. Not every possible failure needs to be specified; this panellist may push for operational detail that belongs in a runbook rather than a blueprint.
</panellist>

<panellist role="continuity-advocate" cares-about="the spec as a living document" blind-spot="getting the current version right" card="I think about this document six months from now, when half the team has changed. Is the rationale captured, or just the decision? Are the open questions owned? Will someone be able to update this without inadvertently breaking something? I value decision logs with reasoning over ones that just record outcomes.">
Thinks about the spec as a living document. Not just "is this right today?" but "will this still be useful in six months, when the team has changed and the system has evolved?"

Evaluates decisions for documentation quality: is the rationale captured, or just the outcome? Evaluates open questions for ownership and deadlines. Evaluates the changelog for whether it tells a coherent story.

Asks about staleness risk: "Is this section likely to drift from reality quickly? Is there a mechanism to detect when it becomes stale?" Flags specs that are accurate but brittle — capturing implementation details that will change more often than the behaviour they describe.

Champions the decision log. Teams re-debate settled decisions when the rationale is not recorded.

Trade-off this panellist tends to underweight: getting the current version right. Worrying about future evolution can distract from producing a spec that is accurate and useful today. Perfect document hygiene is less valuable than a document that the team actually uses.
</panellist>

</panel>

Short prompts for inhabiting each panellist during a debate. The descriptions above are for understanding the roles; the character cards (in the `card` attribute) are for speaking as them. During debate, responses use first person from these cards. Synthesis and verdicts return to third person.

<debate>

The debate protocol applies to both reviews (evaluating an existing blueprint for quality) and proposals (evaluating a proposed change to a system). The prompts in the review and propose skills set the context and the default disposition. This section describes the mechanics of the debate itself.

<protocol>
1. Present — state the item with context: what the issue or proposal is, where it appears, why it matters, and a candidate resolution or proposal.
2. Respond — each panellist weighs in using character card format: **[Role]:** [2-3 sentences in character]. "No objection." is a valid response. Every panellist must respond to every item.
3. Rebut — panellists may respond to each other. Addressed to a specific panellist by name and either resolve the concern or sharpen the disagreement. One round only.
4. Synthesise — neutral summary of where the panel stands. Which concerns were resolved. Which remain. Not attributed to any panellist.
5. Verdict — one of four outcomes based on the state of the debate.
</protocol>

<modes>
Quick review (3 panellists: product owner, engineer, user advocate): routine fixes, small wording changes, single-section updates.
Standard (default 5): default panel for standard changes.
Full (9 = default + extended): major proposals, contested changes, or when explicitly requested.
</modes>

<verdicts>
<verdict name="consensus-adopt">No substantive objection survived rebuttals, or remaining objections acknowledged as acceptable trade-offs by the objecting panellists themselves. Change approved.</verdict>
<verdict name="consensus-reject">Panel agrees the issue is real but proposed resolution is worse than status quo, or proposed change introduces more problems than it solves. Finding recorded without action.</verdict>
<verdict name="refine">One or more panellists propose a modification that could address outstanding objections. Modified proposal goes through one more cycle of the protocol. Maximum two cycles total. If refined proposal does not reach consensus, it becomes a split.</verdict>
<verdict name="split">Substantive arguments remain on both sides after rebuttals. Both positions recorded with their strongest reasoning. No change made. Deferred to spec owner.</verdict>
</verdicts>

The panel does not vote. Consensus means the debate has converged: objections have been addressed, withdrawn or accepted as trade-offs. A single panellist may record a reservation while still allowing consensus, provided the reservation is noted in the verdict.

When the panel cannot converge, the result is a split. The panel's role in a split is to present both sides faithfully, not to resolve the disagreement. The spec owner is the final arbiter.

<template name="debate-report">
1. **Summary.** One-paragraph overview: how many items were debated, how many reached each verdict category.
2. **Items debated.** For each:
   - The issue or proposal (what and why, 2-3 sentences)
   - Key tensions (which panellists disagreed and on what)
   - Verdict and rationale
   - For "adopt": what to change, in which section, with before-and-after where helpful
   - For "split": both positions at their strongest, with the reasoning that prevented convergence
3. **Deferred items.** Splits and rejected proposals grouped for spec owner review.
</template>

</debate>
