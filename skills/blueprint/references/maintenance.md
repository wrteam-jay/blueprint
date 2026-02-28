# Living Document Maintenance

A blueprint is only useful if it stays accurate. This guide covers how to keep it current: detecting staleness, triggering reviews, recording changes, and assigning ownership.

---

## Staleness signals

A blueprint becomes stale when the system changes but the document does not. These signals indicate a section may no longer be accurate:

**Scenario-level signals:**
- A scenario references an entity state that no longer exists in the domain model
- A scenario describes a flow that engineering says "we changed how that works"
- A scenario's end state contradicts the current domain model
- A user story's acceptance criteria is no longer satisfied by the system

**Terminology signals:**
- A term defined in the blueprint is not what the current codebase calls the concept
- A new term has appeared in team conversation that is not in the blueprint
- Two teams are using different terms for the same concept and the blueprint has not resolved it

**Domain model signals:**
- An entity has a new state that is not in the blueprint
- A relationship has changed cardinality (one-to-one became one-to-many)
- An entity's lifecycle owner has changed
- An invariant has been relaxed or tightened

**Requirements signals:**
- A "Must Have" requirement is not currently met and there is no open question about it
- A business rule's source (the policy or decision it came from) has changed
- A non-functional requirement threshold is no longer the target

**Decision log signals:**
- A decision is being re-debated in meetings (the rationale may be missing or wrong)
- The outcome of a decision has changed but the log still shows the old decision
- A decision references a stakeholder or policy that no longer exists

---

## Review triggers

A blueprint should be formally reviewed — not just read — when any of these occur:

**After a major release:**
Review all scenarios and domain model sections that the release touched. Update any that reflect the new behaviour. Add new scenarios for new flows. Update the changelog.

**After an incident or bug that revealed undocumented behaviour:**
The incident revealed something the blueprint did not capture. That is a gap. Document the actual behaviour. If the actual behaviour was wrong, document what the correct behaviour should be and open a requirement. Update the decision log if a decision was made about the correct behaviour.

**After significant user research:**
New research often contradicts assumptions in user stories. Update stories whose "so that" clauses are now disproven or refined. Update the evidence annotations. If a story turns out to be the wrong problem, deprecate it and add the right one.

**When onboarding a new team member:**
Ask the new person to read the blueprint and flag anything that does not match what they learn from the codebase or from the team. New readers find gaps that familiar readers stop seeing. Their confusion is diagnostic.

**When a change proposal is approved:**
Any time a propose skill debate results in an adopted change, update the blueprint to reflect it. Record the change in the changelog and the decision in the decision log.

**On a regular cadence (recommended: quarterly):**
Even without specific triggers, a quarterly review catches gradual drift. Ask: "Is every scenario in this blueprint still how the system actually works?"

---

## Delta protocol — how to record changes

When a blueprint is updated, edit only the affected section files — not the whole directory. After edits, update `changelog.md` and the section status in `README.md` so readers know whether the version they read last month is still current.

### What counts as a meaningful change

**Requires a version bump and changelog entry:**
- New scenario added
- Existing scenario substantively changed (not just wording)
- Entity state added, removed or renamed
- Relationship cardinality changed
- Business rule added, changed or removed
- New actor added
- New requirement added or existing requirement changed
- Terminology definition changed

**Does not require a version bump:**
- Typo or grammar corrections
- Clarifying wording without changing meaning
- Adding an open question
- Resolving an open question without changing the spec

### Changelog entry format

```markdown
| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.3 | 2025-02-15 | [name] | Added Payment Failure and Retry scenarios.
                              Updated Order domain model: added on_hold state.
                              Resolved OQ-007 (retry policy — see D-012). |
```

**Summary rules:**
- One sentence per substantive change
- Name the section changed, not just "updated scenarios"
- Reference resolved open questions and new decisions
- If a behaviour was wrong and is now corrected, say so: "Corrected: Order cancellation scenario was missing the on_hold case"

### Decision log entry format

When a change is made that involves a design decision, add it to the decision log at the same time:

```markdown
**D-012** — 2025-02-15
*Decision:* Payment retry policy — 3 attempts over 7 days, then subscription suspended.
*Rationale:* Finance team data shows 70% of payment failures resolve within 7 days.
3 retries matches industry standard. Immediate suspension was rejected as too aggressive
for recoverable failures.
*Decided by:* Product + Finance (meeting 2025-02-12)
*Supersedes:* D-004 (previous policy: retry once after 24 hours)
```

---

## Ownership model

A blueprint without clear ownership drifts. Clear ownership means: when something in the system changes, someone knows it is their job to update the blueprint.

### Spec owner

Every blueprint has one spec owner — a named person, not a team. The spec owner is responsible for:
- Knowing when the blueprint is stale
- Triggering reviews when review triggers are met
- Ensuring open questions get resolved
- Keeping the decision log current
- Approving changes before they are committed

The spec owner does not have to write all the content. They are accountable for accuracy.

### Section ownership

For large blueprints, individual sections may have owners who are responsible for the accuracy of that section:

```markdown
| Section | Owner |
|---------|-------|
| Domain Model | [Engineering lead] |
| Scenarios: Payment flows | [Product manager — payments] |
| Non-functional requirements | [Engineering lead / SRE] |
| Business rules | [Product manager + Legal] |
```

Section owners are notified when their section is changed. They are responsible for flagging when their section becomes stale.

### Open question ownership

Every open question must have an owner. "TBD" is not an owner. The owner is the person who will either resolve the question or escalate it to someone who can. Ownerless open questions do not get resolved.

---

## Deprecating a blueprint

When a system or feature is retired, the blueprint should not be deleted — it should be deprecated.

**Deprecation process:**
1. Change the status to `Deprecated`
2. Add a note at the top: what replaced this feature, when it was retired, where the new spec lives
3. Keep the document accessible but clearly marked so readers know not to trust it as current

```markdown
> **DEPRECATED** — This feature was retired on 2025-06-01 and replaced by the
> [New Feature Name] blueprint. This document is kept for historical reference only.
```

Deleting blueprints removes the decision history and makes it hard to understand why the new system was designed the way it was. Deprecation preserves that history.

---

## Anti-patterns

**"We'll update the blueprint later."**
Later does not happen. Update the blueprint when the system changes, at the same time, as part of the same work. A blueprint updated a month after the code change will miss the reasoning that was fresh in everyone's mind at the time.

**Changelog that just says "updated."**
A changelog entry that says "Updated scenarios" tells a reader nothing about whether the section they read last week is still accurate. Name what changed.

**Open questions that have been "resolved" verbally but not in the document.**
If a decision was made in a meeting and everyone remembers the outcome but it is not in the decision log, it will be re-debated. Write it down immediately.

**"I'll just add a comment in the code."**
Code comments are not a substitute for blueprint updates. Code is read by engineers. Blueprints are read by the whole team. Both need to be current.

**Treating the blueprint as a historical document.**
"That's how it worked in version 1" is fine in a changelog entry. It is not fine in the Scenarios section. The Scenarios section always describes how the system works now, not how it worked before.
