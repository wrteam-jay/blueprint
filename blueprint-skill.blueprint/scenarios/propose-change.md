# Scenario: Propose a system change

## Trigger

A Spec Author or stakeholder wants the panel to evaluate a proposed change to the system described by a blueprint — a new feature, behaviour change, rule modification, or scope expansion.

## Preconditions

- A blueprint exists for the system being changed.
- The proposal is articulated: what change, and why.

## Steps

1. **Read the relevant blueprint sections.** Not necessarily the full blueprint — only sections the proposal affects.
2. **Frame the proposal.** The skill presents the proposed change in terms of the five evaluation criteria:
   - **The problem** — what need or gap does this address?
   - **The fit** — does this belong in this system or is it out of scope?
   - **The scope** — what sections of the blueprint would change?
   - **The cost** — what complexity does this add?
   - **The reversibility** — if this turns out wrong, how hard is it to undo?
3. **Convene the panel.** Standard mode (5) by default. Full (9) for major proposals.
4. **Debate the proposal.** The debate protocol runs with a key difference from review: the default disposition is to leave the system as described. Burden of proof is on the proposal.
5. **Produce the debate report.** Verdict, rationale, and if adopted — which blueprint sections need updating.

## Default disposition

Leave the system as described. The proposal must justify itself.

## Outcomes

- A debate report with the panel's verdict on the proposal.
- If consensus-adopt: a clear list of blueprint sections that need updating, with the nature of each change.
- If consensus-reject: the reasoning, so the proposer understands why.
- If split: both positions presented for the Spec Owner.

## Error paths

- **Proposal is too vague to evaluate.** The skill asks clarifying questions before convening the panel. Does not debate a vague proposal. States what specifically needs to be clarified: "The proposal says 'improve performance' but does not specify which flow, what the current behaviour is, or what 'improved' means."
- **Proposal fundamentally changes the system's purpose.** The skill flags this explicitly: "This proposal changes the core context of the blueprint — not just a section but the reason the system exists. Consider whether this is an update to the existing blueprint or a new system that warrants its own specification."
- **Proposal introduces new terminology.** The skill identifies new terms implied by the proposal and requires they be defined before the debate proceeds. Debating a proposal with undefined terms produces ambiguous verdicts.
- **Proposal conflicts with an existing requirement.** The skill surfaces the conflict: "This proposal contradicts REQ-[N]: [requirement]. The panel should evaluate whether the requirement should change, the proposal should change, or the conflict is unresolvable."
- **Adopted proposal requires complex updates.** The debate produces a consensus-adopt, but the changes span many sections and are interdependent. The skill recommends using the update flow rather than making changes inline, and produces a change plan showing the order of updates and dependencies between them.
- **Proposal is actually a bug report.** The proposer describes current behaviour that doesn't match the blueprint. This isn't a proposal — it's a staleness issue. The skill redirects to the update flow: "The system and the blueprint disagree. Let's update the blueprint to match reality first, then evaluate whether the current behaviour is what we want."
