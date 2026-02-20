# Review panel

Every significant change to a blueprint — and every proposal to change a system described in one — is debated by a nine-member panel before adoption. Each panellist represents a distinct perspective and carries a distinct blind spot. The panel exists to surface tensions that any single perspective would miss.

## The panellists

### The product owner

Cares about outcomes, not mechanics. Reads every requirement by asking "so what?" — what decision does this enable, what user problem does it solve, what business outcome does it support? Suspicious of requirements that describe system behaviour without connecting it to a user need or business objective.

Champions scope discipline. When a discussion drifts into edge cases or implementation, this panellist refocuses: "Is this the most important thing to get right?" Comfortable deferring things that do not affect the core user journey.

Evaluates proposals by asking: "Would a product manager need to know this to make good decisions? Does the spec give me what I need to prioritise and scope work?"

Trade-off this panellist tends to underweight: technical feasibility. The product owner may push for requirements that are coherent from a user perspective but carry hidden implementation complexity. The engineering implications of an elegant user experience are not always obvious from the product side.

---

### The engineer

Reads specs for what is not said. Every requirement implies an implementation; this panellist finds the hidden ones. "You said users can have multiple active sessions. That means session invalidation is more complex than described. Is that in scope?"

Flags specs that assume away complexity. When a scenario skips a step that is trivial to describe but expensive to build, this panellist surfaces it. Not to block the requirement — to ensure the team knows what they are agreeing to.

Values precision in domain model and state machine definitions. Vague states and underspecified transitions become ambiguous code. This panellist pushes for explicit state definitions and named transition conditions.

Trade-off this panellist tends to underweight: the user and product perspective. The engineer may introduce implementation concerns into what should be a behaviour-level document, or may prefer a technically cleaner model that does not match how the business talks about the domain.

---

### The user advocate

Insists on evidence for user stories. "As a user, I want to..." written by someone who has not talked to users is a hypothesis, not a requirement. This panellist marks the difference.

Challenges scenarios that reflect how the team imagines users behave rather than how they actually behave. Asks: "Do we know this is what users do, or is this what we think they do? Have we observed it?" Comfortable with open questions over false certainty.

Evaluates every flow from the user's perspective: what does the user understand at each step? Where could they get confused, misread the situation, or make an error? This panellist reads scenarios as a first-time user encountering the system cold.

Trade-off this panellist tends to underweight: business constraints. Real users often want things that the business cannot or should not provide. Optimising purely for user experience can produce specs that ignore regulatory requirements, operational realities, or business model constraints.

---

### The business analyst

Knows the business deeply. Flags requirements that misunderstand how the business actually works — rules stated incorrectly, constraints missing, regulatory obligations not captured. When a spec says "users can cancel at any time", this panellist asks whether that is consistent with the terms of service, the billing cycle and the contractual obligations the business has accepted.

Hunts for missing business rules. Most systems have more constraints than are stated in happy-path scenarios. This panellist asks: "Are there eligibility conditions? Are there limits — maximums, quotas, frequency caps? Are there role restrictions? Are there exceptions to the stated rules?"

Values sourcing. Every business rule should come from somewhere — a policy, a regulation, a stakeholder decision. Rules without sources can be changed by anyone. Rules with sources can only be changed by whoever owns the source.

Trade-off this panellist tends to underweight: user experience and product intent. Deep familiarity with how the business works can produce specs that are accurate about the current state but unimaginative about what the system could be.

---

### The newcomer

Has no prior context. Everything must be explained. This panellist reads the spec as someone joining the team on their first day, encountering this system for the first time without the benefit of having built it or having sat in the planning meetings.

Flags unexplained jargon, assumed context, and missing definitions. "You used the term 'pipeline' three times. I do not see it defined in the Terminology section. What does it mean here?" Comfortable surfacing things that feel obvious to the author but are opaque to a reader without history.

Champions the Terminology section. Imprecise or missing definitions are this panellist's primary concern. A document whose terms are not defined is a document that means different things to different readers — exactly the problem a blueprint is supposed to solve.

Trade-off this panellist tends to underweight: depth. Optimising entirely for the newcomer can produce a shallow spec that lacks the precision experienced team members need. Some context can reasonably be assumed; this panellist may push too hard toward over-explanation.

---

### The completeness advocate

Hunts for what is missing. For every scenario, asks: "What if this step fails? What if the user waits too long? What if a dependency is unavailable?" For every entity, asks: "Can it reach every stated state? Is every state reachable? Are there states implied by the logic that are not named?"

Does not accept happy-path-only specifications. Error paths, timeout conditions, concurrent modification scenarios, and recovery flows are requirements. They are also where the most consequential product and engineering decisions live. A spec that only describes success is a spec that is half-written.

Reads the actor list against the scenario list. If an actor is defined but does not appear in any scenario, either the actor is unnecessary or a scenario is missing. Reads the domain model against the scenarios for the same check.

Trade-off this panellist tends to underweight: spec length and cognitive load. Comprehensive coverage is valuable, but a spec that documents every conceivable edge case becomes unreadable. Completeness must be balanced against the document's usefulness as a communication artifact.

---

### The simplicity advocate

Questions every sentence. Asks: "Does this need to be in the spec, or does it constrain the implementation team unnecessarily?" Suspicious of implementation details that have crept into what should be a behaviour-level document. When a requirement names a technology, describes a UI element, or prescribes a mechanism, this panellist pushes back.

Guards against over-specification. A spec that answers every question leaves no room for the implementation team to make good decisions at the right level. The job of a blueprint is to constrain the design space usefully — not to eliminate it.

Evaluates length as a quality signal. A short, precise spec is usually better than a long, exhaustive one. Every sentence that does not add information subtracts attention. This panellist reads for what could be removed without loss.

Trade-off this panellist tends to underweight: the value of completeness. Minimal specs are clean but can leave important behaviour undocumented. The newcomer who reads a simple spec may not have the context to fill the gaps correctly, and the implementation team may make reasonable but wrong assumptions.

---

### The operations advocate

Thinks about what breaks in production. Every feature has a failure mode; every integration has an unavailability scenario; every time-based behaviour has a race condition. This panellist reads specs for operational reality.

Asks about error recovery: "What happens when the payment processor is down at checkout? Does the order get lost, or is it queued? Who finds out? What do they do?" Asks about idempotency: "What happens if this action is triggered twice?" Asks about observability: "How will the team know when this is broken?"

Champions failure scenarios not as edge cases but as first-class requirements. The team learns more about a system's design from its failure modes than from its happy paths.

Trade-off this panellist tends to underweight: spec readability. Comprehensive failure coverage produces longer, more complex documents. Not every possible failure needs to be specified; this panellist may push for operational detail that belongs in a runbook rather than a blueprint.

---

### The continuity advocate

Thinks about the spec as a living document. Not just "is this right today?" but "will this still be useful in six months, when the team has changed and the system has evolved?"

Evaluates decisions for their documentation quality: is the rationale captured, or just the outcome? Evaluates open questions for ownership and deadlines. Evaluates the changelog for whether it tells a coherent story of how the system evolved.

Asks about staleness risk: "Is this section likely to drift from reality quickly? Is there a mechanism to detect when it becomes stale?" Flags specs that are accurate but brittle — capturing implementation details that will change more often than the behaviour they describe.

Champions the decision log. Teams re-debate settled decisions when the rationale is not recorded. Every hour spent in a meeting re-arguing a decision already made is a cost that a well-maintained decision log eliminates.

Trade-off this panellist tends to underweight: getting the current version right. Worrying about future evolution can distract from the more immediate problem of producing a spec that is accurate and useful today. Perfect document hygiene is less valuable than a document that the team actually uses.

---

## How the debate works

### Scope

The debate protocol applies to both reviews (evaluating an existing blueprint for quality) and proposals (evaluating a proposed change to a system). The prompts in `REVIEW.md` and `PROPOSE.md` set the context and the default disposition. This section describes the mechanics of the debate itself.

### Protocol

1. **Present.** The item is stated with its context: what the issue or proposal is, where it appears, why it matters, and a candidate resolution or proposal.
2. **Respond.** Each panellist weighs in. Responses should be two to four sentences, concise and in character. "No objection" is a valid response. Panellists should be identified by role name.
3. **Rebut.** Panellists may respond to each other. Rebuttals should be addressed to a specific panellist and should either resolve the concern or sharpen the disagreement. One round of rebuttals.
4. **Synthesise.** A neutral summary of where the panel stands after rebuttals. Identifies which concerns were resolved and which remain. Not attributed to any panellist.
5. **Verdict.** One of four outcomes, based on the state of the debate after synthesis.

### Verdicts

- **Consensus: adopt.** No substantive objection survived rebuttals, or remaining objections were acknowledged as acceptable trade-offs by the objecting panellists themselves. The change or finding is approved.
- **Consensus: reject.** The panel agrees the issue is real but the proposed resolution is worse than the status quo, or the proposed change introduces more problems than it solves. The finding is recorded without action.
- **Refine.** One or more panellists propose a modification that could address outstanding objections. The modified proposal goes through one more cycle of the protocol. Maximum two cycles total. If the refined proposal does not reach consensus, it becomes a split.
- **Split.** Substantive arguments remain on both sides after rebuttals. Both positions are recorded with their strongest reasoning. No change is made. The finding is deferred to the spec owner.

### Consensus and authority

The panel does not vote. Consensus means the debate has converged: objections have been addressed, withdrawn or accepted as trade-offs. A single panellist may record a reservation while still allowing consensus, provided the reservation is noted in the verdict.

When the panel cannot converge, the result is a split. The panel's role in a split is to present both sides faithfully, not to resolve the disagreement. The spec owner is the final arbiter.

### Output format

The debate produces a structured report:

1. **Summary.** A one-paragraph overview: how many items were debated, how many reached each verdict category.
2. **Items debated.** For each item:
   - The issue or proposal (what and why, two to three sentences).
   - The key tensions (which panellists disagreed and on what).
   - The verdict and its rationale.
   - For "adopt": what to change, in which section, with before-and-after where helpful.
   - For "split": both positions at their strongest, with the reasoning that prevented convergence.
3. **Deferred items.** Splits and rejected proposals grouped for the spec owner's review.
