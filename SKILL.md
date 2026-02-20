---
name: blueprint
description: A living product specification skill. Use when you want to document how a system works, capture user stories and flows, build shared vocabulary, discuss existing functionality, or create a single source of truth for a feature or product area.
version: 1
auto_trigger:
  - file_patterns: ["**/*.blueprint.md", "**/blueprint.md"]
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
| Reviewing a blueprint for gaps | `audit` | You have a blueprint and want to stress-test it for missing flows, terminology conflicts and coverage gaps |

## What a blueprint contains

```
1. Context        — why this exists; the problem it solves
2. Scope          — what's covered, what's adjacent, what's explicitly out
3. Actors & Roles — who interacts with the system and in what capacity
4. Terminology    — shared vocabulary; precise definitions for domain terms
5. User Stories   — who needs what and why
6. Scenarios      — how things work end-to-end, with diagrams
7. Domain Model   — entities, their states, their relationships
8. Requirements   — what the system must do; business rules; constraints
9. Decision Log   — settled decisions with their rationale
10. Open Questions — live discussion space
11. Changelog     — how this document has evolved
```

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

## Quick format

```markdown
# Blueprint: [Name]

**Status:** Draft | Active | Deprecated
**Version:** 1.0
**Last updated:** [date]
**Owners:** [names]
**Related:** [links to related blueprints]

---

## 1. Context
## 2. Scope
## 3. Actors & Roles
## 4. Terminology
## 5. User Stories
## 6. Scenarios & Flows
## 7. Domain Model
## 8. Requirements
   ### 8.1 Functional Requirements
   ### 8.2 Business Rules
   ### 8.3 Non-Functional Requirements
## 9. Decision Log
## 10. Open Questions
## 11. Changelog
```

## References

- [Elicitation guide](./skills/elicit/SKILL.md) — build a blueprint through structured conversation
- [Distillation guide](./skills/distill/SKILL.md) — extract a blueprint from an existing system
- [Audit guide](./skills/audit/SKILL.md) — review a blueprint for gaps and quality
- [Section guide](./references/section-guide.md) — what each section must contain
- [Diagram guide](./references/diagram-guide.md) — Mermaid patterns for flows, states and domain models
