---
name: blueprint
description: A living product specification skill. Use when you want to document how a system works, capture user stories and flows, build shared vocabulary, discuss existing functionality, or create a single source of truth for a feature or product area.
version: 1
auto_trigger:
  - file_patterns: ["**/*.blueprint/README.md", "**/*.blueprint/**/*.md"]
  - keywords: ["blueprint", "living spec", "product spec", "system spec", "document how this works", "single source of truth", "spec this out"]
---

<skill name="blueprint">

<brief>A living specification for how things work. Not a one-time approval document — a persistent reference that a team maintains, discusses, and evolves alongside the product.

A blueprint answers:
- **What** the system does, and why it exists
- **Who** uses it, in what roles, with what goals
- **How** things flow — the real scenarios, step by step
- **What** the domain looks like — the entities, their states, their relationships
- **What words** mean — the shared vocabulary everyone uses to talk about this

It covers both what the system **does** today and what it **should** do. When these diverge, that divergence is worth examining.</brief>

<routing>
<route task="Building a spec from scratch" skill="elicit">Describing a new feature or system and need to capture it</route>
<route task="Documenting existing functionality" skill="distill">System exists but is not documented; want to understand and capture what it does</route>
<route task="Reviewing a blueprint for quality" skill="review">Have a blueprint and want the review panel to debate its clarity and completeness</route>
<route task="Auditing a blueprint for gaps" skill="audit">Want a systematic checklist audit — six dimensions, structured findings report</route>
<route task="Evaluating a proposed change" skill="propose">Want the review panel to evaluate a new feature, behaviour change or rule modification</route>
<route task="Updating an existing blueprint" skill="update">System has changed and the blueprint needs to reflect it</route>
<route task="Scaffolding a new blueprint" skill="scaffold">Want to create the directory structure for a new blueprint with placeholder files</route>
</routing>

<sections>
<section n="1" name="Context">Why this exists; the problem it solves</section>
<section n="2" name="Scope">What's covered, what's adjacent, what's explicitly out</section>
<section n="3" name="Actors & Roles">Who interacts with the system and in what capacity</section>
<section n="4" name="Terminology">Shared vocabulary; precise definitions for domain terms</section>
<section n="5" name="User Stories">Who needs what and why</section>
<section n="6" name="Scenarios">How things work end-to-end, with diagrams</section>
<section n="7" name="Domain Model">Entities with states, invariants, transitions, and relationships</section>
<section n="8" name="Requirements">What the system must do; business rules with sources; constraints</section>
<section n="9" name="Decision Log">Settled decisions with rationale (not just outcomes)</section>
<section n="10" name="Open Questions">Every question has an owner and a deadline</section>
<section n="11" name="Changelog">How this document has evolved</section>
</sections>

<constraints name="scope-sizing">
<c rule=">20 terms in Terminology">Domain likely covers multiple bounded contexts — split</c>
<c rule=">10 scenarios with disconnected actors">Non-overlapping actor groups belong in separate blueprints</c>
<c rule="Unrelated entity clusters">Entity groups with no relationships are separate domains</c>
<c rule="Disconnected actor groups">Actors who never share a scenario are in different systems</c>
</constraints>

When in doubt, start with one blueprint and split when size makes targeted updates difficult.

<tiers>
<tier n="1" name="Skeleton">Context, Scope, Actors, Terminology — enough to align on vocabulary and boundaries</tier>
<tier n="2" name="Workable">+ User Stories, primary Scenarios, Domain Model — enough to start implementation discussions</tier>
<tier n="3" name="Authoritative">+ Error scenarios, Requirements with sources, Decision log — the single source of truth</tier>
</tiers>

State the current tier in the README.md manifest so readers know what to expect.

<core-discipline>
A blueprint describes observable behaviour, not implementation. It says what happens — not which database stores it, which API returns it, or which component renders it.

The test for every detail: "Would someone need to know this to understand how the system behaves, without knowing how it is built?"

<yes>A user can have one active subscription at a time — Behaviour</yes>
<yes>An expired invitation cannot be accepted — Behaviour</yes>
<yes>Admins can see all workspaces; members only their own — Access behaviour</yes>
<no>Subscriptions are stored in the subscriptions table — Implementation</no>
<no>Invitations expire via a nightly cron job — Mechanism</no>
<no>Access is enforced by a middleware guard on the API — Implementation detail</no>

Implementation details belong in technical design documents. The blueprint belongs to the whole team — product, engineering, support, design — not just engineering.
</core-discipline>

<template name="blueprint-directory">
[name].blueprint/
├── README.md              # Manifest: header block, section index, status
├── context.md             # Section 1
├── scope.md               # Section 2
├── actors.md              # Section 3
├── terminology.md         # Section 4
├── stories.md             # Section 5
├── scenarios/             # Section 6
│   ├── _index.md          # Scenario index with one-line summaries
│   ├── [scenario-name].md # One file per scenario
│   └── ...
├── domain-model.md        # Section 7
├── requirements.md        # Section 8
├── decisions.md           # Section 9
├── questions.md           # Section 10
└── changelog.md           # Section 11
</template>

Why a directory: targeted loading (only read the section you're updating), scenarios grow independently (own directory), smaller files mean better edits, cross-referencing with relative paths works.

<template name="readme-manifest">
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
</template>

<ref src="./skills/elicit/SKILL.md" name="Elicit">Build a blueprint through structured conversation</ref>
<ref src="./skills/distill/SKILL.md" name="Distill">Extract a blueprint from an existing system</ref>
<ref src="./skills/review/SKILL.md" name="Review">Convene the review panel to debate clarity and completeness</ref>
<ref src="./skills/audit/SKILL.md" name="Audit">Systematic checklist audit across six dimensions</ref>
<ref src="./skills/propose/SKILL.md" name="Propose">Convene the review panel to evaluate a proposed change</ref>
<ref src="./skills/update/SKILL.md" name="Update">Incrementally update a blueprint after system changes</ref>
<ref src="./skills/scaffold/SKILL.md" name="Scaffold">Generate the directory structure for a new blueprint</ref>

<ref src="./references/section-guide.md" name="Section guide" load="lazy">What each section must contain, including cross-blueprint references</ref>
<ref src="./references/diagram-guide.md" name="Diagram guide" load="lazy">Mermaid patterns for flows, states and domain models</ref>
<ref src="./references/examples.md" name="Worked examples" load="lazy">Before/after examples for every section type</ref>
<ref src="./references/maintenance.md" name="Maintenance guide" load="lazy">Keeping a blueprint current: staleness signals, review triggers, ownership</ref>

</skill>
