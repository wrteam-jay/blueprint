# Scenario: Distill from an existing system

## Trigger

A Spec Author invokes the skill to document a system that already exists but is undocumented, partially documented, or documented in ways that no longer match reality.

## Preconditions

- The system exists and is accessible (codebase, running system, or both).
- The Spec Author can serve as the Domain Expert (solo workflow) or has access to one.

## Steps

1. **Before-you-start questions.** The skill asks: What part of the system? What sources do we have? What is most uncertain? What should the blueprint be used for?
2. **Map the territory.** The skill surveys the landscape: entry points, key entities, core flows, external dependencies. Produces a rough map before writing any section files.
3. **Extract terminology.** The skill identifies vocabulary from code and existing docs, resolves conflicts between code names and business names (business terms win), and builds the terminology section.
4. **Extract entities and states.** The skill finds where data lives and what states it moves through. Surfaces implicit state machines — boolean field combinations and nullable timestamps that encode unnamed states.
5. **Extract flows.** The skill traces where state changes happen: status-changing functions, event handlers, webhook receivers, scheduled jobs. For each flow: trigger, preconditions, changes, communications, next steps. Consolidates scattered preconditions from multiple layers.
6. **Walk scenarios with the author.** The skill compares what code does with what the author (as Domain Expert) describes. Surfaces discrepancies: "The code does X, but you described Y. Is one wrong?"
7. **Identify gaps and questions.** The skill catalogues: undocumented decisions, undocumented requirements, missing error handling, stale documentation, and behavioural debt (system does something two different ways for historical reasons).

## Key filters throughout

- **Abstraction test:** "Would a stakeholder care?" — yes, capture it. No, leave it out.
- **Intentional-or-accidental test:** Designed behaviour becomes a requirement. Accidental behaviour becomes an open question: "The system currently does X. Was this intentional?"

## Outcomes

- A complete blueprint directory reflecting how the system actually works.
- Terminology resolved — one name per concept, code names flagged for cleanup.
- Open questions for every behaviour nobody can explain.
- Clear separation between "what the system does" and "what it should do."

## Error paths

- **Author lacks knowledge about a specific area.** The skill documents what it can observe from code and marks the area with an open question: "Behaviour observed in code but intent unverified. Owner: [author]. Needs: someone with knowledge of [area] to confirm whether this is intentional." The author or someone else can resolve it later.
- **Code contradicts existing documentation.** Both are recorded. The skill does not assume either is correct — it flags the discrepancy as an open question with the specific conflict stated.
- **Dead code discovered.** Code paths that are never reached in production are excluded from the blueprint. Noted in the decision log: "Excluded [feature] — appears unreachable in production."
- **Implicit state machine with impossible states.** The skill finds boolean combinations that represent states nobody intended (e.g., `is_active=false` and `verified_at is not null` and `deactivated_at is null` — how did we get here?). Each impossible state is surfaced as an open question with the specific field combination that produces it.
- **Scattered business logic.** The same precondition is checked in multiple code layers. The skill consolidates it: "The actual preconditions for [flow] are [combined list]. These are currently checked across [N] layers." Captured once in the scenario; the scattered implementation is noted in the decision log as behavioural debt.
- **Workaround that became permanent.** Code that was clearly temporary ("TODO: fix this", "HACK:", "temporary workaround") but is now core to the system. The skill documents the actual behaviour (not the intended behaviour), notes the history, and opens a question: "This appears to have been a temporary fix. Is the current behaviour the desired behaviour?"
- **Codebase is too large to survey completely.** The skill focuses on the scope established in step 1, traces flows from entry points inward, and explicitly states what was not examined: "The following areas were outside the distillation scope: [list]."
