# Blueprint

*A living spec for how things work*

---

A Claude Code skill for building and maintaining a single source of truth about a system — how it works today, how it should work, and the shared vocabulary everyone uses to talk about it.

## Install

**As a plugin (recommended for sharing):**

```bash
# From a marketplace (once published)
/plugin install blueprint@your-marketplace

# From a local checkout
claude --plugin-dir /path/to/blueprint
```

**As a local skill (for personal use):**

```bash
# Symlink the skill directory into your global skills
ln -s /path/to/blueprint/skills/blueprint ~/.claude/skills/blueprint

# Or into a specific project
ln -s /path/to/blueprint/skills/blueprint /your/project/.claude/skills/blueprint
```

**Into a project repo (for team use):**

Copy or symlink `skills/blueprint/` into your project's `.claude/skills/` directory and commit it. Anyone who clones the repo gets the skill automatically.

## Usage

Once installed, type `/blueprint` to get started. You can also jump to a specific skill:

- `/blueprint:elicit` — build a spec from scratch through structured conversation
- `/blueprint:distill` — document an existing system by walking through what it actually does
- `/blueprint:review` — convene the review panel to debate a blueprint's clarity and completeness
- `/blueprint:audit` — run a systematic checklist audit across six quality dimensions
- `/blueprint:propose` — convene the review panel to evaluate a proposed change
- `/blueprint:update` — incrementally update a blueprint after a system change
- `/blueprint:scaffold` — generate the directory structure for a new blueprint

## What problem this solves

Every product team runs into the same friction:

- **Tribal knowledge.** The system's behaviour lives in the heads of the people who built it. New team members learn through osmosis. When someone leaves, understanding leaves with them.
- **Terminology drift.** Engineering calls it a "job". Product calls it a "task". Support calls it a "ticket". Three teams, one concept, three implementations.
- **No shared reference.** Discussions about changes require reconstructing context from memory, tickets and code. Disagreements about "how it works" are hard to resolve without a canonical source.
- **Intent vs reality gap.** Code captures what the system does, including bugs and expedient decisions. There is no lightweight way to see what it was *meant* to do.

A blueprint is the answer to all of these. A directory of focused files. The whole team maintains it. When someone asks "how does X work?", the answer is "check the blueprint."

## What a blueprint is

A living specification — not a one-time approval document, but a persistent reference that evolves alongside the product. It covers:

- **Context** — why this exists
- **Actors & roles** — who uses it
- **Terminology** — shared vocabulary with precise definitions
- **User stories** — who needs what and why
- **Scenarios & flows** — how things work, end-to-end, with diagrams
- **Domain model** — the entities, their states, their relationships
- **Requirements** — what the system must do; the constraints and rules
- **Decision log** — what was decided and why (so settled things stay settled)
- **Open questions** — the live discussion space

## What a blueprint is not

- A technical design document (no architecture, no schemas, no APIs)
- A project plan (no timelines, no milestones)
- A one-time deliverable (it is maintained, not filed)
- A substitute for code review or testing

## How to use it

**Scaffold** — start a new blueprint. Generates the directory structure with placeholder files and inline hints for each section.

**Elicit** — you are specifying something new. Walk through it as a structured conversation: context, actors, terminology, stories, flows, domain model, requirements. Each phase produces its corresponding section file.

**Distill** — the system exists but is not documented. Walk through the code and existing knowledge to capture what it actually does. Surface the implicit state machines, name the undocumented decisions, resolve the terminology conflicts.

**Review** — convene the review panel (5 or 9 panellists) to debate a blueprint's clarity and completeness. The panel surfaces tensions that any single perspective would miss.

**Audit** — run a systematic checklist audit across six dimensions: terminology, scenario coverage, domain model, requirements quality, decision log, and implementation leakage. Produces a structured findings report.

**Propose** — evaluate a proposed change (new feature, behaviour change, rule modification) against the existing blueprint. The review panel debates coherence and value.

**Update** — the system has changed. Read only the affected section files, make targeted edits, update the changelog and decisions.

## Multi-file format

Blueprints are directories, not single files. Each section lives in its own file for targeted loading and precise edits.

```
orders.blueprint/
├── README.md              # Manifest: header, section index, completion tier
├── context.md             # Why this exists
├── scope.md               # What is covered and what is not
├── actors.md              # Who interacts with the system
├── terminology.md         # Shared vocabulary
├── stories.md             # User stories with evidence
├── scenarios/             # One file per scenario
│   ├── _index.md          # Scenario index with summaries
│   └── ...
├── domain-model.md        # Entities, states, relationships
├── requirements.md        # Functional, business rules, non-functional
├── decisions.md           # Settled decisions with rationale
├── questions.md           # Unresolved items with owners
└── changelog.md           # Version history
```

## Repo structure

```
blueprint/                                    # Plugin root
├── .claude-plugin/
│   └── plugin.json                           # Plugin manifest
├── README.md                                 # This file
└── skills/
    └── blueprint/                            # The skill
        ├── SKILL.md                          # Main skill — routing, format, core discipline
        ├── TEAM.md                           # Review panel — panellists, debate protocol, verdicts
        ├── skills/
        │   ├── elicit/SKILL.md               # Build a blueprint from conversation
        │   ├── distill/SKILL.md              # Extract a blueprint from an existing system
        │   ├── review/SKILL.md               # Review panel debate on quality
        │   ├── audit/SKILL.md                # Systematic checklist audit
        │   ├── propose/SKILL.md              # Review panel debate on proposed changes
        │   ├── update/SKILL.md               # Incremental blueprint updates
        │   └── scaffold/SKILL.md             # Generate directory structure for new blueprint
        └── references/
            ├── section-guide.md              # What each section must contain
            ├── diagram-guide.md              # Mermaid patterns for flows, states and domain models
            ├── examples.md                   # Before/after examples for every section type
            └── maintenance.md                # Keeping a blueprint current
```

## License

MIT © 2026
