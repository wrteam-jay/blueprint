# Scenario: Read and navigate a blueprint

## Trigger

A Blueprint Reader needs to understand how a system works — to build a feature, write tests, design an interface, make a prioritisation decision, or verify a business rule.

## Preconditions

- A blueprint exists at Tier 1 or above.
- The reader has access to the blueprint directory.

## Steps

1. **Start at the README manifest.** The reader opens `README.md` to see the blueprint's status, tier, spec owner, and section index. The tier tells them what to expect — a Tier 1 blueprint won't have scenarios; a Tier 3 is the full reference.
2. **Navigate to the relevant section.** The reader follows the section link for their immediate question:
   - **Developer** looking for what to build → `scenarios/` for end-to-end flows with preconditions, steps, and error paths.
   - **QA/tester** looking for what to test → `scenarios/` for error paths alongside happy paths, and `requirements.md` for acceptance criteria.
   - **Designer** looking for user needs → `actors.md` for who uses the system and `stories.md` for evidence-grounded user stories.
   - **Product manager** looking for scope and priorities → `context.md` for why the system exists, `scope.md` for boundaries, `requirements.md` for behaviour-level constraints free of implementation detail.
   - **Business stakeholder** looking for rules they can change → `requirements.md` for business rules with sources (policy, regulation, or decision) showing which rules are externally imposed and which are internal choices.
3. **Use terminology as the shared vocabulary.** When the reader encounters a domain term, they check `terminology.md` for its precise definition. One concept, one name — no ambiguity regardless of the reader's role.
4. **Cross-reference as needed.** Scenarios reference actors and entities. The reader follows these references to `actors.md` and `domain-model.md` for definitions, states, and invariants.
5. **Check the decision log for context.** When the reader asks "why does it work this way?", `decisions.md` provides the rationale, alternatives considered, and who decided.

## Outcomes

- The reader understands the system's behaviour at the level of detail they need for their role.
- Shared vocabulary ensures the reader uses the same terms in subsequent discussions.
- No implementation details — the reader understands what the system does without needing to know how it is built.

## Error paths

- **Blueprint is at a lower tier than expected.** The reader needs scenarios but the blueprint is Tier 1 (Skeleton). The README manifest's tier and section statuses make this clear upfront — the reader knows which sections have content and which don't, rather than discovering empty files.
- **Reader encounters an undefined term.** A term used in a scenario or requirement is not in `terminology.md`. This is a blueprint quality issue — the reader flags it to the Spec Owner for resolution.
- **Reader finds a discrepancy with the running system.** The blueprint says one thing; the system does another. The reader reports it to the Spec Owner, who can invoke the update flow to reconcile. The blueprint documents current behaviour — discrepancies mean the blueprint is stale.
- **Reader needs implementation details.** The blueprint intentionally excludes implementation. If the reader needs to know which API to call or which database to query, they consult technical design documents or the codebase. The blueprint tells them *what* happens; code and architecture docs tell them *how*.
