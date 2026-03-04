# Terminology

## Blueprint

A living product specification organized as a directory of markdown files. Covers 11 canonical sections — from context and scope through domain model, requirements, and decision log. Describes observable system behaviour, not implementation. Maintained over time as the system evolves.

## Section

One of 11 defined parts of a blueprint. Each section has a specific purpose, content rules, and an independent status (Pending, Draft, Complete, or Active). Sections are stored as individual files for targeted loading and independent editing.

## Tier

A completion level indicating how much of a blueprint has been captured. Three tiers exist:
- **Skeleton (Tier 1):** Context, Scope, Actors, Terminology — enough to align on vocabulary and boundaries.
- **Workable (Tier 2):** Adds User Stories, primary Scenarios, Domain Model — enough to start implementation discussions.
- **Authoritative (Tier 3):** Adds error scenarios, Requirements with sources, Decision Log — the single source of truth.

## Scenario

An end-to-end flow showing how something works. Every scenario has a trigger, preconditions, numbered steps, outcomes, and error paths. Scenarios live in individual files within a `scenarios/` directory and link to actors and entities.

## Entity

A domain concept described in the domain model. Every entity has a definition, named states, transitions between states (with triggers), invariants (what must always be true), and relationships to other entities.

## Panel

A group of simulated expert perspectives convened to debate blueprint quality or evaluate proposals. Three modes: Quick (3 panellists), Standard (5), Full (9). The panel does not vote — it debates until convergence or split.

## Panellist

One simulated expert role within a panel. Each panellist has a defined perspective (what they care about), a known blind spot (what they tend to underweight), and a character card (first-person prompt used during debate). Nine panellists exist: five default, four extended.

## Debate

A structured 5-step discussion following a fixed protocol: Present, Respond, Rebut, Synthesise, Verdict. Maximum two cycles (if the first round results in a "refine" verdict). Used by the review, propose, and update sub-skills.

## Verdict

The outcome of a debate. Four types:
- **Consensus-adopt:** No surviving objections; change approved.
- **Consensus-reject:** Problem is real but proposed fix is worse than status quo.
- **Refine:** A modification could address objections; one more cycle.
- **Split:** Both sides have strong arguments; deferred to Spec Owner.

## Finding

An issue discovered during review or audit. In audit, findings have severity: Blocking (must fix before the blueprint is reliable) or Advisory (should fix to improve quality). In review, findings are debated items with verdicts.

## Core Discipline

The principle that blueprints describe observable behaviour, not implementation. The test: "Would someone need to know this to understand how the system behaves, without knowing how it is built?" If yes, it belongs. If no, it doesn't.

## Abstraction Test

The filter applied to every detail: "Would a stakeholder care about this?" Expiry after 7 days — yes (affects user experience). Expiry enforced by cron job — no (mechanism). Used during distillation and review to keep blueprints at the behaviour level.

## Spec Owner

One person — not a team — responsible for a blueprint's accuracy and currency. Resolves split verdicts, assigns question owners, triggers reviews, decides when to deprecate. Singular ownership is a design choice: shared ownership means no ownership.

## Elicitation

The process of building a blueprint through structured conversation with a domain expert. Follows 8 phases, uses one-question-at-a-time mechanics, verification checkpoints after each phase, and explicit handling of contradictions and "I don't know" answers.

## Distillation

The process of extracting a blueprint from an existing system. Combines code reading (what the system does) with people consultation (why it does it). Follows 6 steps: map territory, extract terminology, extract entities and states, extract flows, walk scenarios with people, identify gaps.

## Verification Checkpoint

A pause during elicitation where captured content is shown to the domain expert for confirmation. Prevents wrong work from accumulating silently. Occurs after each phase — shows only the section just captured, not the entire draft.

## Scope-Sizing Constraint

A rule indicating when a single blueprint covers too much and should be split. Signals: more than 20 terms, more than 10 disconnected scenarios, unrelated entity clusters, disconnected actor groups.
