---
name: elicit
description: Use when building a blueprint from scratch through conversation — specifying a new feature, capturing a planned system, or turning stakeholder descriptions into a structured living spec.
---

# Elicitation

This skill builds a blueprint through conversation. The goal is to surface ambiguities, establish shared vocabulary, trace real flows end-to-end, and produce a document the whole team can reason about.

The same principles apply whether you are talking to a product manager about a new feature or a founder describing a system they want to build. The challenge is always the same: separating what the system should **do** from how it might be **built**, and making implicit decisions explicit.

---

## Scoping the session

Before any detail, establish what you are specifying and where the edges are.

**"What is this blueprint about — one sentence?"**
Gets to the core without implementation. If the answer contains a tech stack, redirect.

**"Is this a new capability, a change to something existing, or documentation of something that already works?"**
New capability → elicit forward from intent. Change → start from the existing behaviour before describing the delta. Existing system → use the distill skill instead.

**"What is definitely out of scope for this spec?"**
Out-of-scope is as important as in-scope. Get both lists before proceeding.

**"Are there related systems or features we should know about but not specify here?"**
Establishes boundaries and identifies related blueprints to reference.

Capture at the top:
```markdown
**About:** [one sentence]
**Covers:** [what's in scope]
**Does not cover:** [what's explicitly out]
**Related:** [adjacent systems/specs]
```

---

## Elicitation phases

### Phase 1: Context

**Goal:** Understand why this exists before capturing what it does.

1. "What problem does this solve? Who has this problem today?"
2. "What happens if this doesn't get built?"
3. "Is there an existing workaround? What breaks about it?"
4. "Who asked for this — and what did they actually say they needed?"
5. "Is there a deadline? Is it fixed or flexible?"

**Output:** A Context section that a new team member could read to understand why this feature exists.

**Watch for:** Features described in terms of their solution ("we need a dashboard"). Redirect: "What decisions does someone currently make without enough information?"

---

### Phase 2: Actors and roles

**Goal:** Name every party who interacts with the system and describe what they can do.

1. "Who uses this?"
2. "Are there different types of user? What distinguishes them?"
3. "Are there system actors — automated processes, external services?"
4. "What can each actor do that the others cannot?"
5. "Is there a guest or unauthenticated state? What can someone do before they log in?"

For each actor, capture:
- Name (use what the business actually calls them)
- Who they are
- What they can do
- What they cannot do (if the restriction matters)

**Watch for:** Actors that are actually two things. "Admin" often means both a billing admin and a user admin — different permissions, different flows. Probe when a role seems broad.

---

### Phase 3: Terminology

**Goal:** Build the shared vocabulary before anything else, so the rest of the conversation uses consistent terms.

This is the most underrated phase. Terminology conflicts cause more miscommunication than missing requirements. If your product team calls it a "project" and your engineering team calls it a "workspace", you have a bug waiting to happen.

Questions:
1. "What are the main things this system manages — the nouns?"
2. "What do you call [thing]? Does engineering use the same word?"
3. "Is [term A] and [term B] the same thing, or different?"
4. "Are there terms you use that might mean something different to someone outside the team?"

For each key term, capture a precise one-sentence definition. Not a dictionary definition — what it means *in this system*.

```markdown
**Order** — A customer's intent to purchase a set of products. Exists from the point
            of cart confirmation. Distinct from a *Transaction*, which is the financial
            record of payment.

**Transaction** — The financial record of a payment attempt. An Order may have
                  multiple Transactions (e.g., one failed attempt, one successful).
```

**Watch for:**
- The same word meaning different things to different stakeholders
- Two words being used for the same concept ("booking" and "reservation")
- Terms that only make sense to insiders ("the pipeline", "the queue")

When you find a conflict: stop, name it, resolve it. "You said 'booking' and earlier you said 'reservation'. Are these the same thing?" Do not move on until it is resolved. Terminology conflicts that survive into implementation become dual models with join tables pointing both ways.

---

### Phase 4: User stories

**Goal:** Capture who needs what and why, before getting into how the system delivers it.

Stories are not implementation tasks. They are statements of user need that frame every subsequent design decision.

Format: **As a [actor], I want to [action], so that [outcome].**

Questions per flow:
1. "Walk me through this from the user's perspective, not the system's perspective."
2. "What are they trying to accomplish? What does success look like for them?"
3. "What would make this frustrating or broken from their point of view?"

Group stories by actor or by flow. A story without a "so that" clause is incomplete — the outcome is what makes the story a requirement rather than a feature request.

**Watch for:** Stories written from the system's perspective ("the system processes the payment"). Reframe: who is the actor, what is their goal, why does it matter to them?

---

### Phase 5: Scenarios and flows

**Goal:** Trace real end-to-end journeys through the system, including error paths.

This is the most important phase. Requirements without scenarios are abstract. Scenarios without requirements miss constraints. The combination is what produces a spec the whole team can reason about.

#### For each major flow:

**Start with the happy path:**
1. "Walk me through [scenario] from start to finish."
2. "What triggers this? A user action? Time passing? An external event?"
3. "What is the first thing that happens?"
4. "Then what? And then?"
5. "What does the user see at each step?"
6. "What has changed in the system when this is complete?"

**Then probe the edges:**
1. "What if [step] fails? What does the user see? What does the system do?"
2. "What if the user does this in the wrong order?"
3. "What if they wait too long? Are there timeouts or deadlines?"
4. "What if the same action is triggered twice?"
5. "What if an external service is unavailable at this step?"

**Then check the decision points:**
1. "You described [branch]. What determines which path is taken?"
2. "Is that decision made by the user, the system, or an admin?"
3. "Can that decision be reversed? By whom?"

**Diagram as you go.** After tracing a flow verbally, sketch it as a diagram. Mermaid flowcharts for user journeys, sequence diagrams for multi-party interactions, state diagrams for entity lifecycles. See the [diagram guide](../../references/diagram-guide.md).

**Watch for:**
- Flows that assume capabilities not yet in scope
- Flows with no terminal state (every path must end somewhere)
- Decision points with no stated owner ("it depends" is a gap, not an answer)
- Notification steps that assume a notification system not specified

---

### Phase 6: Domain model

**Goal:** Name the entities the system manages, describe their states, and map their relationships.

Entities are the persistent things in the system — the nouns that have lifecycle and identity. Not UI components, not API responses — the actual domain objects.

Questions:
1. "What are the things this system creates, stores, and manages?"
2. "What states can [entity] be in? What does each state mean?"
3. "What triggers the transition from one state to another?"
4. "How is [entity A] related to [entity B]? One-to-one? One-to-many?"
5. "Who creates [entity]? Who can change it? Who can delete it?"
6. "What happens to [entity B] when [entity A] is deleted or cancelled?"

For each entity, capture:
- Name and one-sentence definition
- Its states (if it has a lifecycle)
- Its key relationships
- Who owns its lifecycle

**Watch for:** Entities that are really two things collapsed into one (a single "User" that is both a buyer and a seller). Entities with implicit states hidden in boolean fields ("is_active" and "is_verified" might mean the user has four actual states). Fields that are really relationships.

---

### Phase 7: Requirements and business rules

**Goal:** Capture the constraints — what the system must do and what it must prevent.

By this point you have flows and scenarios. Requirements are the rules that govern them. Work through:

**Functional requirements** — "must" statements about system behaviour:
- "What must always happen when [event]?"
- "What must never be allowed?"
- "Are there limits — maximums, minimums, quotas?"
- "Are there time windows — deadlines, expirations, schedules?"

**Business rules** — constraints that come from policy, regulation or product decision:
- "Are there eligibility conditions — who can do this, under what circumstances?"
- "Are there role restrictions — only [role] can do [action]?"
- "Are there compliance requirements — GDPR, SOC 2, industry-specific?"
- "Are there exceptions — cases where the normal rule does not apply?"

For each rule, capture its source. "Users cannot delete their account while a subscription is active" needs a reason: legal obligation? Data integrity? Product decision? The reason matters when someone wants to change it.

**Non-functional requirements** — how well the system must perform:
- Performance targets (specific thresholds, not "should be fast")
- Availability requirements
- Security requirements (not "should be secure")
- Data retention and residency

---

### Phase 8: Open questions and decisions

**Goal:** Capture everything unresolved and everything already settled.

At the end of a session, surface all the things that came up but were not resolved.

"We talked about [X]. You were not sure. Let me capture that as an open question: [precise statement of the question]. Who should resolve this? By when?"

Also capture decisions made during the session in the Decision Log:

"We decided [X]. The reason was [Y]. Let me record that so we do not re-debate it."

A decision log is underrated. Every team re-debates settled decisions in meeting rooms. A log with rationale stops that.

---

## Elicitation principles

### Ask one question at a time

Compound questions produce compound answers that are hard to capture precisely. Ask one thing, get the answer, then ask the next thing.

### Follow the data

When something is created, changed or sent, ask where it comes from, where it goes, and who can see it. "You said the user receives a confirmation email. Where does the email address come from? Who sends it? What does it contain? What if the send fails?"

### Name ambiguity out loud

"I am not sure what happens here. Let me note this as an open question rather than assume." Voiced ambiguity gets resolved. Silent ambiguity becomes a bug.

### Work through implications

Every decision has downstream effects. When a choice is made, ask what it implies: "You said invitations expire after 7 days. What happens to the slots that were offered — do they become available again? What does the candidate see when they click an expired link?"

### Make the vocabulary explicit

When a new term appears, pause and define it. "You said 'pipeline' — what do you mean by that in this context?" Add it to the Terminology section. Use it consistently from that point on.

### Distinguish existing from intended

When the system already exists, ask: "Does the system do this today, or is this how you want it to work?" Both are useful, but they go in different places — existing behaviour is a starting point; intended behaviour is a requirement.

---

## Common traps

### The "and then" trap

Long chains of "and then" without decision points or conditions. Probe every "and then" with "always?" or "only if...?" Most flows have more branches than people initially describe.

### The "obviously" trap

When someone says "obviously" or "of course", probe. That phrase marks an unstated assumption. "Obviously the admin approves it — but are there cases where approval is automatic? What if the admin is not available?"

### The "how" trap

When the conversation drifts into implementation — "we'll use a webhook for that", "the frontend will poll" — redirect. "At the behaviour level, what needs to happen and when? We can capture the how separately."

### The "one user" trap

Scenarios narrated from the perspective of one archetypal user often miss multi-party interactions. "You described the buyer's journey. Walk me through the same flow from the seller's perspective. At what point do these paths intersect?"

### The "happy path only" trap

If the session produces only success scenarios, probe explicitly: "What if each step fails?" Error paths are requirements too. They are also where the most important UX and data integrity decisions live.

### The "equivalent terms" trap

Two terms being used for the same concept. Do not note them as equivalent — resolve them. Pick one term, define it, use it everywhere. The other term should not appear again, not even in a "see also" note.

---

## Session structure

**Opening (5 min).** State the goal: "We are capturing how this works and what it must do, not how we will build it." Agree on scope for this session.

**Context (10 min).** Why this exists, what problem it solves.

**Actors and terminology (15 min).** Who uses it. What the key terms mean. Resolve any conflicts.

**User stories and scenarios (30 min).** The main flows, happy path first, then edges. Diagram as you go.

**Domain model (15 min).** Key entities, their states, their relationships.

**Requirements and rules (15 min).** Constraints and non-functional requirements.

**Wrap-up (10 min).** Capture open questions with owners. Record decisions made. Note what to cover in the next session.

---

## References

- [Section guide](../../references/section-guide.md) — what each section must contain
- [Diagram guide](../../references/diagram-guide.md) — Mermaid patterns for flows, states and domain models
