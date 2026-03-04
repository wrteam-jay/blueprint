---
name: scaffold
description: Use when creating a new blueprint — generates the full directory structure with placeholder files and inline hints for each section.
---

<skill name="scaffold">

<brief>Generate the directory structure for a new blueprint with placeholder files and comment hints for each section.</brief>

<questions name="before-scaffolding">
<q>Blueprint name — what is this blueprint about? (used for directory name and title)</q>
<q>Scope — one sentence describing what this blueprint covers</q>
<q>Spec owner — who is accountable for accuracy?</q>
<q>Related blueprints — are there adjacent blueprints this one touches?</q>
</questions>

<template name="directory-structure">
[name].blueprint/
├── README.md
├── context.md
├── scope.md
├── actors.md
├── terminology.md
├── stories.md
├── scenarios/
│   └── _index.md
├── domain-model.md
├── requirements.md
├── decisions.md
├── questions.md
└── changelog.md
</template>

<template name="readme">
# Blueprint: [Name]

**Status:** Draft
**Version:** 0.1
**Last updated:** [date]
**Spec owner:** [name]
**Related blueprints:** [links or "None yet"]

---

## Sections

| # | Section | File | Status |
|---|---------|------|--------|
| 1 | Context | [context.md](./context.md) | Pending |
| 2 | Scope | [scope.md](./scope.md) | Pending |
| 3 | Actors & Roles | [actors.md](./actors.md) | Pending |
| 4 | Terminology | [terminology.md](./terminology.md) | Pending |
| 5 | User Stories | [stories.md](./stories.md) | Pending |
| 6 | Scenarios & Flows | [scenarios/](./scenarios/_index.md) | Pending |
| 7 | Domain Model | [domain-model.md](./domain-model.md) | Pending |
| 8 | Requirements | [requirements.md](./requirements.md) | Pending |
| 9 | Decision Log | [decisions.md](./decisions.md) | Active |
| 10 | Open Questions | [questions.md](./questions.md) | Active |
| 11 | Changelog | [changelog.md](./changelog.md) | Active |

## Completion tier

**Current: Tier 0 (Scaffold)** — Directory created. No sections captured yet.
</template>

<template name="section-files">
context.md:      # Context
                 &lt;!-- Why this exists. The problem, who has it, why it matters. Not how it is built. --&gt;

scope.md:        # Scope
                 &lt;!-- What is in scope, what is out of scope (with reasons), and related blueprints. --&gt;

actors.md:       # Actors &amp; Roles
                 &lt;!-- Every party who interacts with the system. Name, description, capabilities, restrictions. --&gt;

terminology.md:  # Terminology
                 &lt;!-- Shared vocabulary. One precise sentence per term. Resolve conflicts — one term per concept. --&gt;

stories.md:      # User Stories
                 &lt;!-- As a [actor], I want [action], so that [outcome]. Include evidence annotation for each. --&gt;

domain-model.md: # Domain Model
                 &lt;!-- Entities with states, transitions, invariants, relationships, and lifecycle owners. --&gt;

requirements.md: # Requirements
                 &lt;!-- Functional requirements (FR-), business rules (BR-) with sources, non-functional (NFR-) with thresholds. --&gt;

decisions.md:    # Decision Log
                 &lt;!-- Settled decisions with rationale. What was decided, why, who decided, what it supersedes. --&gt;

questions.md:    # Open Questions
                 &lt;!-- Unresolved items. Each needs: question, owner, what it blocks, deadline. --&gt;

changelog.md:    # Changelog
                 &lt;!-- Version history. One sentence per substantive change. --&gt;

                 | Version | Date | Changes | Author |
                 |---------|------|---------|--------|
                 | 0.1 | [date] | Scaffold created | [spec owner] |
</template>

<template name="scenarios-index">
# Scenarios

&lt;!-- Add one row per scenario. Each scenario gets its own file in this directory. --&gt;

| Scenario | Actors | File |
|----------|--------|------|
</template>

<ref src="../../references/section-guide.md" name="Section guide" load="lazy"/>

</skill>
