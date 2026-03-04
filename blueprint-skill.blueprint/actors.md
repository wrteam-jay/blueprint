# Actors & Roles

## Spec Author

The person who creates or updates a blueprint. They invoke the skill, provide domain knowledge, answer questions, and approve captured content. May be a developer documenting their own system, a product manager specifying a new feature, or a tech lead capturing tribal knowledge before it's lost.

**Can do:** Invoke any sub-skill (elicit, distill, update, scaffold). Provide context, correct misunderstandings, resolve open questions, approve verification checkpoints.

**Cannot do:** Override panel verdicts directly (but as Spec Owner, can resolve splits).

## Spec Owner

One person — not a team — accountable for a blueprint's accuracy and currency. Decides when the blueprint needs updating, resolves split verdicts from the panel, assigns owners to open questions, and approves changes.

**Can do:** Everything a Spec Author can do, plus: resolve split verdicts, set review triggers, deprecate the blueprint.

**Cannot do:** Delegate ownership to a team. Ownership is singular by design — shared ownership means no ownership.

## Blueprint Reader

Anyone who consumes a completed blueprint to understand how a system works. Readers span the full product team: backend developers, frontend developers, mobile developers, designers (UI/UX), QA and testers, product managers, business stakeholders, and executives.

**Can do:** Read any section. Use the terminology as a shared vocabulary. Reference scenarios in discussions. Identify discrepancies between the blueprint and the running system.

**Cannot do:** Modify the blueprint directly. Changes go through the Spec Author using the update or propose flows.

## Domain Expert

A person who carries knowledge about the system being documented but may not be the one invoking the skill. The Spec Author consults them during distillation and elicitation. They are the source of "why" — the intent behind behaviour, the history behind decisions, the business rules behind constraints.

**Can do:** Answer questions about the system. Validate captured scenarios. Explain intent behind existing behaviour. Identify gaps between documented and actual behaviour.

**Cannot do:** Invoke the skill directly (they work through the Spec Author).

## Panellist (simulated)

An AI-simulated expert perspective that participates in review, proposal, and update debates. Each panellist has a defined role, a stated perspective, a known blind spot, and a character card used during debate.

Nine panellists exist across two groups:
- **Default panel (5):** Product Owner, Engineer, User Advocate, Completeness Advocate, Simplicity Advocate
- **Extended panel (4):** Business Analyst, Newcomer, Operations Advocate, Continuity Advocate

**Can do:** Raise concerns, respond to other panellists, participate in rebuttals, contribute to verdicts.

**Cannot do:** Override the Spec Owner. In a split verdict, the panel presents both sides; the Spec Owner decides.
