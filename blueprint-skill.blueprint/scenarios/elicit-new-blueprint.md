# Scenario: Elicit a new blueprint

## Trigger

A Spec Author invokes the skill to document a new or planned system that does not yet have a blueprint.

## Preconditions

- The Spec Author (or a Domain Expert they can consult) has knowledge of the system to be specified.
- No existing blueprint covers this system.

## Steps

1. **Opening.** The skill establishes the goal ("capture how this works, not how to build it"), establishes scope ("what are we covering?"), and asks for a one-sentence description of the system.
2. **Context phase.** The skill asks why this system exists, what problem it solves, what happens if it doesn't get built. Captured in context.md.
3. **Actors phase.** The skill identifies every party who interacts with the system — human and automated. Captured in actors.md.
4. **Terminology phase.** The skill builds shared vocabulary: the nouns of the domain, resolving conflicts between terms used by different roles. Captured in terminology.md.
5. **User stories phase.** The skill captures who needs what and why, asking for evidence where possible. Captured in stories.md.
6. **Scenarios phase.** For each key flow, the skill traces it end-to-end: trigger, preconditions, steps, outcomes. Then probes every branch: "What if this fails? What if the user waits too long? What if it triggers twice?" Captured in scenarios/.
7. **Domain model phase.** The skill names entities, their states, transitions, invariants, and relationships. Surfaces implicit state machines from boolean combinations. Captured in domain-model.md.
8. **Requirements phase.** The skill captures constraints — what must always happen, what must never happen, limits, time windows, eligibility conditions. Every rule must have a source. Captured in requirements.md.
9. **Closing.** Open questions are assigned owners and deadlines. Decisions made during the session are recorded with rationale. The changelog and README are updated.

## Key mechanics throughout

- **One question at a time.** No bundled questions.
- **Verification checkpoints** after each phase — show what was captured, get confirmation before proceeding.
- **Contradiction handling** — when a new statement conflicts with an earlier one, surface immediately: "Earlier you said X, now you're saying Y. Which takes precedence?"
- **"I don't know" handling** — convert to an open question with owner and deadline. Never invent an answer.
- **Scope creep handling** — park tangential topics and refocus.

## Outcomes

- A complete blueprint directory at the declared tier.
- All sections written, with statuses recorded in the README manifest.
- Open questions logged with owners and deadlines.
- Decisions logged with rationale.

## Error paths

- **Domain Expert unavailable for a phase.** The skill captures what it can and logs specific open questions for the missing information. Does not fabricate answers. States which phases are incomplete and what knowledge is needed to complete them.
- **Contradiction cannot be resolved.** Logged as an open question with both positions stated. The skill does not silently pick one. If the contradiction affects downstream sections (e.g., a terminology conflict that changes how scenarios read), the skill pauses and flags the dependency before continuing.
- **Scope is too large for one blueprint.** The skill recognises scope-sizing signals (>20 terms, disconnected actor groups, unrelated entity clusters) and recommends splitting. It proposes a boundary and asks the author to confirm before proceeding with the narrower scope.
- **Author gives contradictory information across phases.** The skill tracks key facts stated in earlier phases and checks new statements against them. When a conflict is detected across phases (e.g., actors phase said "admins can delete users" but scenarios phase implies they cannot), it surfaces immediately with the specific earlier statement quoted.
- **System is too complex for a single session.** The skill can pause at any phase boundary and resume later. On resumption, it shows the current state (completed sections, pending phases, open questions) so the author can re-orient. Each session ends with the closing protocol regardless of how many phases were covered.
- **Author drifts into implementation.** The skill redirects: "That sounds like an implementation detail — at the behaviour level, what happens from the user's perspective?" If the author insists, the skill notes the implementation detail as context in the decision log but does not include it in the section files.
- **Verification checkpoint rejected.** The author says "no, that's wrong." The skill asks what specifically is wrong, corrects the capture, and re-presents the checkpoint. Does not proceed until the author confirms.
