---
name: audit
description: Use when reviewing an existing blueprint for gaps, missing flows, terminology conflicts, coverage of error cases, or untestable requirements.
---

# Blueprint Audit

This skill reviews an existing blueprint for quality, completeness and consistency. The output is a structured report of specific findings — not a rewrite. Each finding names the problem, locates it in the document, states why it matters, and describes what a fix would look like.

Read the entire blueprint before producing any findings. Isolated observations often disappear when the document is read as a whole; apparent gaps may be covered elsewhere.

---

## Dimension 1: Terminology consistency

Terminology conflicts are the most damaging class of blueprint problem. Two names for the same thing means two mental models, two implementations, and two sources of confusion.

**What to check:**

Scan the entire document for:
- The same concept appearing under multiple names (even if one is mentioned as "also called X")
- The same term used to mean different things in different sections
- Terms in the Terminology section that are not used consistently in Scenarios or Requirements
- Terms in Scenarios and Requirements that do not appear in the Terminology section

**For each conflict found:**
- Name the two (or more) terms that conflict
- State which sections each appears in
- Identify the canonical term (usually the one the business/product uses)
- State what needs to change

**Do not leave a terminology conflict annotated as "equivalent to." Resolution means one term survives, everywhere.**

---

## Dimension 2: Scenario coverage

Scenarios are the core of a blueprint. Missing scenarios mean missing understanding.

**Completeness check:**

For each actor in the Actors section:
- [ ] At least one scenario shows this actor's primary journey
- [ ] The actor's permissions are demonstrated in at least one scenario (what they can do)
- [ ] The actor's restrictions are demonstrated (what they cannot do, if relevant)

For each user story:
- [ ] At least one scenario traces how the system delivers the story's outcome
- [ ] The scenario exists, not just the story

For each entity state in the Domain Model:
- [ ] At least one scenario shows an entity entering this state
- [ ] At least one scenario shows an entity leaving this state (unless it is terminal)

**Error path coverage:**

For each scenario, check:
- [ ] The happy path is documented
- [ ] At least the primary failure modes are documented
- [ ] Time-based edge cases are covered (what if the user waits too long, what if a deadline is missed)
- [ ] Multi-actor interactions identify what each actor sees at each step, not just one actor's view

---

## Dimension 3: Domain model completeness

**Check each entity:**
- [ ] Has a definition (one precise sentence)
- [ ] Has its states listed (if it has a lifecycle)
- [ ] Has its state transitions named (what triggers each transition)
- [ ] Has its key relationships named (not just entity references, but named relationships with cardinality)
- [ ] Has an owner for its lifecycle (who creates it, who can update it, who can delete it)

**Check the model as a whole:**
- [ ] Every entity mentioned in scenarios appears in the domain model
- [ ] Every entity in the domain model appears in at least one scenario
- [ ] No entity has a terminal state that is unreachable by any flow
- [ ] No entity has implicit states hiding in boolean combinations or nullable timestamp fields

---

## Dimension 4: Requirements quality

**Testability.** Every functional requirement must be testable. If you cannot describe a test that would pass or fail based on this requirement, it is not a requirement — it is a wish.

Weasel words that make requirements untestable:

| Word | Problem | Fix |
|------|---------|-----|
| "easily" | No threshold | State the measurable user outcome |
| "fast" | No metric | Name the response time at a specific load |
| "secure" | No definition | Name the specific controls or standard |
| "appropriate" | Undefined | Name the actual condition |
| "should" (used for musts) | Signals optionality | Replace with "must" if mandatory |
| "flexible" | Undefined | State what must be configurable |
| "robust" | Undefined | State what failure scenarios must be handled |

**Sourcing.** Every business rule should have a source. "Users with free plans cannot create more than 3 projects" — why? Product decision? Pricing constraint? Infrastructure limit? The source determines whether the rule can be changed and by whom.

**Coverage.** Scan scenarios for constraints that are implied but not stated:
- A scenario shows a deadline — is the duration in Requirements?
- A scenario shows a role restriction — is it in Business Rules?
- A scenario shows a notification — is the triggering condition and recipient in Requirements?

---

## Dimension 5: Decision log and open questions

**Decision Log:**
- [ ] Decisions made during design are recorded (not just the outcome, the rationale)
- [ ] Decisions that were contested have both positions recorded, plus the resolution
- [ ] Each decision has a date and an owner

A decision log without rationale is almost useless. "We decided to use soft delete" is less valuable than "We decided to use soft delete because audit requirements mean we cannot lose the record, and hard delete requires cascading to three related entities in a way that breaks our event log."

**Open Questions:**
- [ ] Each question is specific enough to be answerable (not "figure out the pricing model")
- [ ] Each question has an owner
- [ ] Each question has a deadline or a note on what it is blocking

Open questions without owners do not get resolved.

---

## Dimension 6: Implementation leakage

A blueprint must not contain implementation decisions. Every one is a constraint the team did not consciously impose.

**Signals:**

| Found in blueprint | Problem |
|-------------------|---------|
| Database or storage technology | Implementation choice |
| API endpoint paths or methods | Interface design |
| Specific libraries or frameworks | Technology choice |
| UI element descriptions (button, modal, form) | Design decision |
| Internal service names | Architecture detail |
| Data types or schema details | Implementation |
| Specific vendor when a category suffices | Usually implementation |

**The exception:** When a specific vendor or technology is a genuine business constraint ("we must integrate with Salesforce because customer contracts require it"), name it and source it. The test is whether a business stakeholder made this decision, not an engineer.

---

## Audit output format

```markdown
# Blueprint Audit: [Name]

**Blueprint version audited:** [version]
**Audit date:** [date]

---

## Summary

[X] findings across [Y] dimensions. [Z] are blocking (must be resolved before
the blueprint is treated as authoritative), [W] are advisory.

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
**Problem:** [What is wrong and why it matters]
**Impact:** [What goes wrong if this is not fixed]
**Fix needed:** [What a resolution looks like — not the resolution itself, the shape of it]

---

## Advisory findings

[Same format, lower severity]

---

## Open questions flagged during audit

- [Question] — Owner: [who should resolve], Deadline: [date]
```

---

## What makes a finding blocking vs advisory

**Blocking:**
- Terminology conflicts (two names for one thing, or one name for two things)
- Missing scenarios for primary user journeys
- Entity states with no entry or exit path
- Requirements with no acceptance criteria
- Open questions with no owner that are blocking design decisions
- Implementation decisions presented as requirements

**Advisory:**
- Missing error path scenarios for minor edge cases
- Requirements that are testable but imprecise
- Terminology that could be clearer but is not ambiguous
- Missing rationale for decisions that are unlikely to be revisited
- Minor implementation leakage that does not constrain engineering meaningfully
