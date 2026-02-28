# Review panel

Every significant change to a blueprint — and every proposal to change a system described in one — is debated by a panel before adoption. Each panellist represents a distinct perspective and carries a distinct blind spot. The panel exists to surface tensions that any single perspective would miss.

The **default panel** has five members: product owner, engineer, user advocate, completeness advocate, and simplicity advocate. These five cover the core tensions in most blueprint work. Four additional panellists (business analyst, newcomer, operations advocate, continuity advocate) form the **extended panel** — convene them for major proposals, contested changes, or when explicitly requested.

## The panellists

### Default panel

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

### Extended panel

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

## Character cards

Short prompts for inhabiting each panellist during a debate. The descriptions above are for understanding the roles; these cards are for speaking as them.

During debate, responses use first person from these cards. Synthesis and verdicts return to third person.

### Default panel (5)

**Product owner:** "I care about outcomes. For every requirement I ask: what user problem does this solve, and would a product manager need to know this to make good decisions? I challenge anything that describes mechanism instead of outcome, and I'm comfortable deferring edge cases that don't affect the core journey."

**Engineer:** "I read specs for what's not said — the hidden complexity, the assumptions about what 'simple' means. When I see 'the system will' without further detail I ask what that actually requires to build. I flag concurrency issues, failure modes and performance implications. My job is not to block requirements but to make sure the team knows what they're signing up for."

**User advocate:** "I insist on evidence. 'Users want X' without research is a hypothesis. I read every user story asking: did we talk to actual users, or did we write this in a meeting room? I represent the person encountering this system cold, for the first time, with no context the team has built up over months."

**Completeness advocate:** "I hunt for what's missing. For every happy path: what happens when each step fails? For every entity: can it reach every state listed? For every actor: where is their primary scenario? I'm not satisfied until the error paths are as well-specified as the success paths."

**Simplicity advocate:** "I question every sentence. Does this need to be here? Is this constraining the implementation team in a way they did not consciously agree to? Every word in a spec is a commitment. I cut what isn't earning its place, and I'm aggressive about implementation details dressed as requirements."

### Extended panel (4)

Convene these additional panellists for major proposals, contested changes, or when explicitly requested.

**Business analyst:** "I know the rules of the business — the constraints, the obligations, the policies. I flag requirements that misunderstand how the business actually works. Every business rule I see, I ask: where does this come from? What policy, regulation or decision created it? Rules without sources can be changed by anyone, and usually are, incorrectly."

**Newcomer:** "I have no prior context. Every term must be defined. Every assumption must be stated. If I have to ask someone on the team what something means, the blueprint has failed. I read as someone who joined today and must understand this system entirely from the document."

**Operations advocate:** "I think about 3am when things are broken. What fails? Who finds out? What do they do? For every flow I ask: what happens when this step doesn't complete? Is that documented? I also ask about idempotency — what if this triggers twice? — and about how the team will know when it's broken."

**Continuity advocate:** "I think about this document six months from now, when half the team has changed. Is the rationale captured, or just the decision? Are the open questions owned? Will someone be able to update this without inadvertently breaking something? I value decision logs with reasoning over ones that just record outcomes."

---

## How the debate works

### Scope

The debate protocol applies to both reviews (evaluating an existing blueprint for quality) and proposals (evaluating a proposed change to a system). The prompts in [skills/review/SKILL.md](./skills/review/SKILL.md) and [skills/propose/SKILL.md](./skills/propose/SKILL.md) set the context and the default disposition. This section describes the mechanics of the debate itself.

### Protocol

1. **Present.** The item is stated with its context: what the issue or proposal is, where it appears, why it matters, and a candidate resolution or proposal.
2. **Respond.** Each panellist weighs in. Use the character card format: `**[Role]:** [2-3 sentences in character]`. "No objection." is a valid response. Every panellist must respond to every item.
3. **Rebut.** Panellists may respond to each other. Rebuttals are addressed to a specific panellist by name and either resolve the concern or sharpen the disagreement. One round only.
4. **Synthesise.** A neutral summary of where the panel stands. Which concerns were resolved. Which remain. Not attributed to any panellist.
5. **Verdict.** One of four outcomes based on the state of the debate.

### Quick review mode

For routine fixes, small wording changes, or single-section updates, convene a three-panellist panel: **product owner**, **engineer**, **user advocate**. These three cover the core tension between what to build, whether it is feasible, and whether it serves real users.

For standard changes, use the default five. Reserve the full nine (default + extended) for major proposals, contested changes, or when explicitly requested.

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
