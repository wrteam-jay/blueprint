---
name: scaffold
description: Use when creating a new blueprint — generates the full directory structure with placeholder files and inline hints for each section.
---

# Blueprint Scaffold

This skill generates the directory structure for a new blueprint. It creates all section files with headings and comment hints so that the team knows what each file should contain.

---

## Quick questions

Before generating the scaffold, ask:

1. **Blueprint name** — what is this blueprint about? (used for the directory name and title)
2. **Scope** — one sentence describing what this blueprint covers
3. **Spec owner** — who is accountable for this blueprint's accuracy?
4. **Related blueprints** — are there adjacent blueprints this one touches?

---

## Output

Creates the following directory structure:

```
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
```

### README.md

Populated with the answers from the quick questions:

```markdown
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
```

### Section files

Each section file has a heading and a comment hint describing what belongs there:

```markdown
# Context
<!-- Why this exists. The problem, who has it, why it matters. Not how it is built. -->
```

```markdown
# Scope
<!-- What is in scope, what is out of scope (with reasons), and related blueprints. -->
```

```markdown
# Actors & Roles
<!-- Every party who interacts with the system. Name, description, capabilities, restrictions. -->
```

```markdown
# Terminology
<!-- Shared vocabulary. One precise sentence per term. Resolve conflicts — one term per concept. -->
```

```markdown
# User Stories
<!-- As a [actor], I want [action], so that [outcome]. Include evidence annotation for each. -->
```

```markdown
# Domain Model
<!-- Entities with states, transitions, invariants, relationships, and lifecycle owners. -->
```

```markdown
# Requirements
<!-- Functional requirements (FR-), business rules (BR-) with sources, non-functional (NFR-) with thresholds. -->
```

```markdown
# Decision Log
<!-- Settled decisions with rationale. Format: what was decided, why, who decided, what it supersedes. -->
```

```markdown
# Open Questions
<!-- Unresolved items. Each needs: question, owner, what it blocks, deadline. -->
```

```markdown
# Changelog
<!-- Version history. One sentence per substantive change. -->

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 0.1 | [date] | Scaffold created | [spec owner] |
```

### scenarios/_index.md

```markdown
# Scenarios

<!-- Add one row per scenario. Each scenario gets its own file in this directory. -->

| Scenario | Actors | File |
|----------|--------|------|
```

---

## References

- [Section guide](../../references/section-guide.md) — what each section must contain
