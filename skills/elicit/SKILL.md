---
name: elicit
description: Use when building a blueprint from scratch through conversation — specifying a new feature, capturing a planned system, or turning stakeholder descriptions into a structured living spec.
---

# Elicitation

This skill builds a blueprint through conversation. The goal is to surface ambiguities, establish shared vocabulary, trace real flows end-to-end, and produce a document the whole team can reason about.

The same principles apply whether you are talking to a product manager about a new feature or a founder describing a system they want to build. The challenge is always the same: separating what the system should *do* from how it might be *built*, and making implicit decisions explicit.

---

## Do not

These are the most common ways elicitation goes wrong. Check against this list before publishing any output.

- **Do not write a scenario without first identifying its trigger.** A scenario without a trigger is a story without a beginning.
- **Do not write a scenario without at least one failure path.** Happy paths alone are half a spec.
- **Do not define a term using that term in the definition.** Circular definitions give the reader nothing.
- **Do not write a business rule without a source.** If you cannot name the policy, regulation or decision that created the rule, mark it as an open question.
- **Do not infer a missing actor — ask.** "The system sends an email" has a missing actor. Who or what triggers the send?
- **Do not write implementation into the blueprint.** If you write the words `API`, `database`, `endpoint`, `table`, `component`, `Redis`, `SQL`, `webhook handler`, `cron job`, `microservice` — stop and rephrase at the behaviour level.
- **Do not fill an open question with an assumption.** If you do not know something, open a question and assign it. Do not invent an answer to keep moving.
- **Do not proceed past a phase without a verification checkpoint.** Show captures, get confirmation, then continue.
- **Do not leave a contradiction silently in the document.** Surface it immediately when you detect it.
- **Do not accept "it depends" as an answer.** It is the location of a requirement. Ask: "Depends on what? Walk me through the cases."
- **Do not generate a complete spec from a single sentence.** Elicitation is a conversation. Generating all at once produces confident-sounding fiction.

---

## Conversation mechanics

### Opening

Start every elicitation session with:

1. Establish the goal: "We are going to capture how this works and what it must do — not how we will build it."
2. Establish scope for this session: "What are we covering today? Should we stay focused on one flow, or capture the whole feature?"
3. Ask the one-sentence question: "In one sentence, what does this thing do?"

The one-sentence answer reveals whether you are aligned on the subject before spending time on details.

### One question at a time

Ask one question. Wait for the answer. Probe the answer. Then ask the next question. Do not bundle questions. Bundled questions produce bundled answers that are hard to separate later.

### Verification checkpoints

After each phase, show what has been captured and ask for confirmation before proceeding:

> "Here's what I've captured so far. Does this match your understanding? Is anything missing or wrong?"

Show only the section you just captured — not the whole draft. Reviewing too much at once causes people to stop reading carefully. Checkpoints after each phase prevent large amounts of wrong work accumulating silently.

### Handling "I don't know"

When a stakeholder says "I don't know", do not fill the gap. Convert it to an open question immediately:

> "That's fine — let me note that as an open question rather than assume. Who should resolve this? By when does it need to be resolved?"

Then move on. Do not get stuck. Accumulate open questions and return to them at the end.

### Handling contradictions

When a new statement conflicts with something already captured, surface it immediately:

> "I want to flag a conflict before we go further. Earlier you said [X]. Now you're saying [Y]. These two things cannot both be true as stated. Which takes precedence? Or is there a condition that determines which applies?"

Do not silently note both. Do not average them. Name the conflict, explore it, and either resolve it or log it as an open question with an owner.

Track contradictions actively. Keep a mental (or explicit) list of key facts stated: statuses, rules, actor capabilities. When a new statement touches the same area, check it against what was said before.

### Handling scope creep

When a stakeholder introduces something outside the agreed scope:

> "That sounds important — let me note it so we don't lose it. I'll add it to the out-of-scope list with a note that it may need its own blueprint. For now, can we stay focused on [current topic]?"

Park it, do not chase it. Scope creep in elicitation produces bloated blueprints that are accurate about many things but authoritative about nothing.

### Signalling phase transitions

When moving between phases, name it explicitly:

> "Good — I have the actors and terminology captured. Let me show you what I have, and then we'll move to user stories."

Explicit transitions keep the stakeholder oriented and set expectations for what comes next.

### Closing a session

At the end of every session:
1. Show the full draft (or the sections covered in this session)
2. Read through the open questions list — assign an owner and deadline to each
3. Record any decisions made during the session in the decision log with rationale
4. State what is covered and what still needs to be captured in a follow-up

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

Capture at the top of the document before any other section:

```markdown
**About:** [one sentence]
**Covers:** [what is in scope]
**Does not cover:** [what is explicitly out — with reasons]
**Related blueprints:** [adjacent systems/specs]
```

---

## Elicitation phases

### Phase 1: Context

**Goal:** Understand why this exists before capturing what it does.

1. "What problem does this solve? Who has this problem today?"
2. "What happens if this doesn't get built?"
3. "Is there an existing workaround? What is broken about it?"
4. "Who asked for this — and what did they actually say they needed?"
5. "Is there a deadline? Is it fixed or flexible?"

**Verification checkpoint:** "Here's the context I've captured: [show paragraph]. Does this accurately describe the problem and why this exists?"

**Output:** A Context section a new team member could read to understand why this feature exists.

**Watch for:** Features described in terms of their solution ("we need a dashboard"). Redirect: "What decisions does someone currently make without enough information?"

---

### Phase 2: Actors and roles

**Goal:** Name every party who interacts with the system.

1. "Who uses this?"
2. "Are there different types of user? What distinguishes them?"
3. "Are there system actors — automated processes, external services?"
4. "What can each actor do that the others cannot?"
5. "Is there a guest or unauthenticated state?"

For each actor: name, who they are, what they can do, what they cannot do (if the restriction matters).

**Verification checkpoint:** "Here are the actors I've identified: [list]. Are any missing? Does any actor here cover two different roles that should be split?"

**Watch for:** "Admin" covering both billing admin and user admin — different permissions, should be named separately.

---

### Phase 3: Terminology

**Goal:** Build the shared vocabulary before anything else.

1. "What are the main things this system manages — the nouns?"
2. "What do you call [thing]? Does engineering use the same word?"
3. "Is [term A] and [term B] the same thing, or different?"
4. "Are there terms you use that might mean something different to someone outside the team?"

For each key term, write a precise one-sentence definition. Not a dictionary definition — what it means *in this system*.

**Verification checkpoint:** "Here are the terms I've defined: [show glossary]. Are the definitions accurate? Are there terms we use that aren't here?"

**Resolution rule:** When two terms exist for the same concept, resolve it now. Pick one. Define it. The other term should not appear anywhere in the document — not even in a "see also" note. Terminology conflicts that survive into implementation become two models, two join tables, two sources of confusion.

**Watch for:**
- Two words for the same concept ("booking" and "reservation")
- One word meaning two different things to different stakeholders
- Terms that only make sense to insiders

---

### Phase 4: User stories

**Goal:** Capture who needs what and why.

Format: **As a [actor], I want to [action], so that [outcome].**

1. "Walk me through this from the user's perspective, not the system's."
2. "What are they trying to accomplish? What does success look like for them?"
3. "Do we have evidence this is what users actually need, or is this our assumption?"

For each story, ask for evidence: analytics data, support ticket patterns, user research findings, observed behaviour. Annotate the story with whatever exists.

**If evidence is absent:** Note it as an open question. "We believe users need X, but we have not validated this." A story with no evidence is a hypothesis. It should be marked as such.

**Verification checkpoint:** "Here are the user stories I've captured: [show list]. Are any missing? Does any story assume a user need we haven't validated?"

**Watch for:** Stories written from the system's perspective ("the system processes"). Reframe: who is the actor, what is their goal, why does it matter to them?

---

### Phase 5: Scenarios and flows

**Goal:** Trace real end-to-end journeys through the system, including error paths.

#### Happy path first

1. "Walk me through [scenario] from start to finish."
2. "What triggers this? A user action? Time passing? An external event?"
3. "What is the first thing that happens?"
4. "Then what? And then?"
5. "What has changed in the system when this is complete? What is the end state?"

#### Then probe every branch

6. "You described [decision point]. What determines which path is taken?"
7. "Is that decision made by the user, the system, or an admin?"
8. "What if [step] fails or is unavailable?"
9. "What if the user waits too long? Are there timeouts?"
10. "What if this action is triggered twice?"

#### Contradiction check

After tracing a flow: "Does anything in this scenario conflict with what we said in the actors section or the terminology section?"

After tracing multiple flows: "Do any of these flows make assumptions about the domain model that we haven't captured?"

**Verification checkpoint:** "Here is the [scenario name] flow: [show it]. Does this match how it actually works? Any steps missing? Any branches I got wrong?"

**Watch for:**
- Flows that assume capabilities not yet in scope
- Flows with no terminal state
- Decision points with no stated owner
- "And then it sends a notification" without specifying who is notified, when, and through what channel

---

### Phase 6: Domain model

**Goal:** Name the entities, their states, and their relationships.

1. "What are the things this system creates, stores, and manages?"
2. "What states can [entity] be in? What does each state mean?"
3. "What triggers the transition from one state to another?"
4. "How is [entity A] related to [entity B]?"
5. "Who creates [entity]? Who can change it? Who can delete it?"
6. "What must always be true about [entity], regardless of state?"

Use the structured entity card format for each entity:

```
Entity: [Name]
Definition: [One sentence]
States: state1 → state2 | terminal_state
Invariants: [What must always be true]
Relationships: [belongs to X, contains Y (0+), has one Z]
Lifecycle owner: [who creates, transitions, deletes]
```

**Verification checkpoint:** "Here is the domain model: [show entities]. Do the states look right? Are any entities missing? Any relationships wrong?"

**Watch for:** Boolean fields or nullable timestamps encoding implicit states. `is_active` + `is_verified` = four unnamed states. Name them explicitly.

---

### Phase 7: Requirements and business rules

**Goal:** Capture constraints — what the system must do and what it must prevent.

**Functional requirements:**
- "What must always happen when [event]?"
- "What must never be allowed?"
- "Are there limits — maximums, minimums, quotas?"
- "Are there time windows — deadlines, expirations, schedules?"

**Business rules:**
- "Are there eligibility conditions — who can do this, under what circumstances?"
- "Are there role restrictions?"
- "Are there compliance requirements?"
- "What are the exceptions — cases where the normal rule does not apply?"

For every rule: **name its source**. The policy, regulation or stakeholder decision that created it. Source-less rules can be changed by anyone. If you cannot name the source, open a question.

**Non-functional requirements:** Specific thresholds, not vague adjectives.
- Not "should be fast" → "p95 response under 2s at 1,000 concurrent users"
- Not "should be secure" → "must satisfy SOC 2 Type II access controls"
- Not "should be available" → "99.9% uptime, 8h RTO, 1h RPO"

**Verification checkpoint:** "Here are the requirements I've captured: [show list]. Are any missing? Are any sourced incorrectly? Are the non-functional thresholds right?"

---

### Phase 8: Open questions and decisions

**At the end of every session:**

**Open questions** — everything unresolved:
- "We talked about [X] but were not sure. Let me capture that as an open question: [precise statement]. Who owns this? By when does it need to be resolved? What does it block?"

**Decision log** — everything decided during the session:
- "We decided [X]. The reason was [Y]. Let me record that so it does not get re-debated."
- Include: what was decided, why, who decided it, what alternatives were considered

Every open question must have an owner and a deadline. Ownerless questions do not get resolved.

---

## Elicitation principles

### Follow the data

When something is created, changed or sent, ask where it comes from, where it goes, and who can see it. "You said the user receives a confirmation email. Where does the email address come from? What does it contain? What if the send fails?"

### Work through implications

Every decision has downstream effects. When a choice is made, ask what it implies: "You said invitations expire after 7 days. What happens to the slots that were offered? What does the candidate see when they click an expired link?"

### Name ambiguity out loud

"I am not sure what happens here — let me note this as an open question rather than assume." Voiced ambiguity gets resolved. Silent ambiguity becomes a bug.

### Make the vocabulary explicit

When a new term appears, pause and define it. "You said 'pipeline' — what do you mean by that in this context?" Add it to Terminology immediately. Use it consistently from that point on. If you catch yourself using two terms for the same concept, resolve it on the spot.

### Distinguish existing from intended

When the system already exists, ask: "Does the system do this today, or is this how you want it to work?" Both are useful, but they go in different places — existing behaviour is a starting point; intended behaviour is a requirement. Mixing them silently produces a spec that is half-true and half-aspirational.

---

## Common traps

### The "and then" trap

Long chains of "and then" without decision points. Probe every step with "always?" or "only if...?" Most flows have more branches than people initially describe.

### The "obviously" trap

"Obviously" marks an unstated assumption. Probe: "Obviously the admin approves it — are there cases where approval is automatic? What if the admin is unavailable?"

### The "how" trap

When the conversation drifts into implementation — "we'll use a webhook for that", "the frontend will poll" — redirect: "At the behaviour level, what needs to happen and when?"

### The "one user" trap

Scenarios narrated from one actor's perspective miss multi-party interactions. "You described the buyer's journey. Walk me through the same flow from the seller's perspective."

### The "happy path only" trap

If the session produces only success scenarios, probe explicitly for each step: "What happens if this step fails?"

### The "equivalent terms" trap

Two terms for the same concept. Do not annotate as "also known as" — resolve it. Pick one term, define it, use it everywhere. The other term should not appear again.

### The "no source" trap

A business rule without a source ("users cannot do X") that nobody can explain the origin of. Do not include it as a fact. Open a question: "This rule exists in the current system. Do we know where it came from? Is it a legal requirement, a product decision, or something else?"

---

## Session structure

**Opening (5 min).** State the goal. Agree scope for this session.

**Context (10 min).** Why this exists. Verification checkpoint.

**Actors and terminology (15 min).** Who uses it. Shared vocabulary. Resolve conflicts. Verification checkpoint.

**User stories and scenarios (30 min).** Main flows, happy path first, then branches and failures. Diagram as you go. Contradiction checks throughout. Verification checkpoint after each scenario.

**Domain model (15 min).** Key entities, states, relationships. Structured entity cards. Verification checkpoint.

**Requirements and rules (15 min).** Constraints, business rules with sources, non-functional thresholds. Verification checkpoint.

**Wrap-up (10 min).** Open questions with owners and deadlines. Decisions with rationale. What to cover in the next session.

---

## References

- [Worked examples](../../references/examples.md) — before/after examples for every section type
- [Section guide](../../references/section-guide.md) — what each section must contain
- [Diagram guide](../../references/diagram-guide.md) — Mermaid patterns for flows, states and domain models
