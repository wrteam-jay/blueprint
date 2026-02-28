---
name: blueprint
description: A living product specification skill. Use when you want to document how a system works, capture user stories and flows, build shared vocabulary, discuss existing functionality, or create a single source of truth for a feature or product area.
version: 1
auto_trigger:
  - file_patterns: ["**/*.blueprint/README.md", "**/*.blueprint/**/*.md"]
  - keywords: ["blueprint", "living spec", "product spec", "system spec", "document how this works", "single source of truth", "spec this out"]
---

# Blueprint

A living specification for how things work. Not a one-time approval document — a persistent reference that a team maintains, discusses, and evolves alongside the product.

A blueprint answers:
- **What** the system does, and why it exists
- **Who** uses it, in what roles, with what goals
- **How** things flow — the real scenarios, step by step
- **What** the domain looks like — the entities, their states, their relationships
- **What words** mean — the shared vocabulary everyone uses to talk about this

It covers both what the system **does** today and what it **should** do. When these diverge, that divergence is worth examining.

## Routing table

| Task | Skill | When |
|------|-------|------|
| Building a spec from scratch | `elicit` | You are describing a new feature or system and need to capture it |
| Documenting existing functionality | `distill` | The system exists but is not documented; you want to understand and capture what it does |
| Reviewing a blueprint for quality | `review` | You have a blueprint and want the review panel to debate its clarity and completeness |
| Auditing a blueprint for gaps | `audit` | You want a systematic checklist audit — six dimensions, structured findings report |
| Evaluating a proposed change | `propose` | You want the review panel to evaluate a new feature, behaviour change or rule modification |
| Updating an existing blueprint | `update` | The system has changed and the blueprint needs to reflect it |
| Scaffolding a new blueprint | `scaffold` | You want to create the directory structure for a new blueprint with placeholder files |

## What a blueprint contains

```
1. Context        — why this exists; the problem it solves
2. Scope          — what's covered, what's adjacent, what's explicitly out
3. Actors & Roles — who interacts with the system and in what capacity
4. Terminology    — shared vocabulary; precise definitions for domain terms
5. User Stories   — who needs what and why
6. Scenarios      — how things work end-to-end, with diagrams
7. Domain Model   — entities with states, invariants, transitions, and relationships
8. Requirements   — what the system must do; business rules with sources; constraints
9. Decision Log   — settled decisions with rationale (not just outcomes)
10. Open Questions — every question has an owner and a deadline
11. Changelog     — how this document has evolved
```

## Scope sizing

A single blueprint should cover one cohesive area. Consider splitting when you see:

- **>20 terms** in the Terminology section — the domain is likely covering multiple bounded contexts
- **>10 scenarios** with disconnected actors — if actor groups do not overlap, they may belong in separate blueprints
- **Unrelated entity clusters** — if the domain model has groups of entities with no relationships between them, those are separate domains
- **Disconnected actor groups** — actors who never appear in the same scenario are likely working in different systems

When in doubt, start with one blueprint and split when the size makes targeted updates difficult.

## Completion tiers

Not every blueprint needs to be complete on day one. Tiers describe how much has been captured.

- **Tier 1 (Skeleton):** Context, Scope, Actors, Terminology — enough to align on vocabulary and boundaries
- **Tier 2 (Workable):** + User Stories, primary Scenarios, Domain Model — enough to start implementation discussions
- **Tier 3 (Authoritative):** + Error scenarios, Requirements with sources, Decision log — the single source of truth the whole team relies on

State the current tier in the `README.md` manifest so readers know what to expect.

## The core discipline

A blueprint describes **observable behaviour**, not implementation. It says what happens — not which database stores it, which API returns it, or which component renders it.

The test for every detail: **"Would someone need to know this to understand how the system behaves, without knowing how it is built?"**

- "A user can have one active subscription at a time" → Yes. Behaviour.
- "Subscriptions are stored in the `subscriptions` table" → No. Implementation.
- "An expired invitation cannot be accepted" → Yes. Behaviour.
- "Invitations expire via a nightly cron job" → No. Mechanism.
- "Admins can see all workspaces; members only their own" → Yes. Access behaviour.
- "Access is enforced by a middleware guard on the API" → No. Implementation detail.

Implementation details belong in technical design documents. The blueprint belongs to the whole team — product, engineering, support, design — not just engineering.

## Blueprint output format

A blueprint is a directory, not a single file. Each section lives in its own file. This keeps individual files small enough for targeted loading and precise edits.

```
[name].blueprint/
├── README.md              # Manifest: header block, section index, status
├── context.md             # Section 1: Context
├── scope.md               # Section 2: Scope
├── actors.md              # Section 3: Actors & Roles
├── terminology.md         # Section 4: Terminology
├── stories.md             # Section 5: User Stories
├── scenarios/             # Section 6: Scenarios & Flows
│   ├── _index.md          # Scenario index with one-line summaries
│   ├── [scenario-name].md # One file per scenario
│   └── ...
├── domain-model.md        # Section 7: Domain Model
├── requirements.md        # Section 8: Requirements
├── decisions.md           # Section 9: Decision Log
├── questions.md           # Section 10: Open Questions
└── changelog.md           # Section 11: Changelog
```

### Why a directory

- **Targeted loading.** When updating terminology, only `terminology.md` enters the context — not the entire spec.
- **Scenarios get their own directory** because they are the largest section and grow independently. Each scenario is its own file. The `_index.md` gives a scannable overview.
- **Smaller files = better edits.** The LLM reads one focused file, makes precise changes, fewer hallucinations.
- **Cross-referencing works.** Files link to each other with relative paths (`see [Order Placement](./scenarios/order-placement.md)`).

### README.md manifest

```markdown
# Blueprint: [Name]

**Status:** Draft | Active | Deprecated
**Version:** 1.0
**Last updated:** [date]
**Spec owner:** [name — one person, not a team]
**Related blueprints:** [links with one-phrase description]

---

## Sections

| # | Section | File | Status |
|---|---------|------|--------|
| 1 | Context | [context.md](./context.md) | Complete |
| 2 | Scope | [scope.md](./scope.md) | Complete |
| 3 | Actors & Roles | [actors.md](./actors.md) | Complete |
| 4 | Terminology | [terminology.md](./terminology.md) | Complete |
| 5 | User Stories | [stories.md](./stories.md) | Draft |
| 6 | Scenarios & Flows | [scenarios/](./scenarios/_index.md) | Draft |
| 7 | Domain Model | [domain-model.md](./domain-model.md) | Draft |
| 8 | Requirements | [requirements.md](./requirements.md) | Pending |
| 9 | Decision Log | [decisions.md](./decisions.md) | Active |
| 10 | Open Questions | [questions.md](./questions.md) | Active |
| 11 | Changelog | [changelog.md](./changelog.md) | Active |

## Completion tier

**Current: [Tier]** — [brief description of what has been captured and what remains]
```

## References

### Sub-skills

- [Elicit](./skills/elicit/SKILL.md) — build a blueprint through structured conversation
- [Distill](./skills/distill/SKILL.md) — extract a blueprint from an existing system
- [Review](./skills/review/SKILL.md) — convene the review panel to debate clarity and completeness
- [Audit](./skills/audit/SKILL.md) — systematic checklist audit across six dimensions
- [Propose](./skills/propose/SKILL.md) — convene the review panel to evaluate a proposed change
- [Update](./skills/update/SKILL.md) — incrementally update a blueprint after system changes
- [Scaffold](./skills/scaffold/SKILL.md) — generate the directory structure for a new blueprint

### Reference guides

- [Section guide](./references/section-guide.md) — what each section must contain, including cross-blueprint references
- [Diagram guide](./references/diagram-guide.md) — Mermaid patterns for flows, states and domain models
- [Worked examples](./references/examples.md) — before/after examples for every section type
- [Maintenance guide](./references/maintenance.md) — keeping a blueprint current: staleness signals, review triggers, ownership
