# Scope

## In scope

- **Specification creation** — building a blueprint from scratch through structured conversation (elicit), or extracting one from an existing undocumented system (distill)
- **Specification structure** — the 11-section format, directory layout, tier system, and rules governing what belongs in each section
- **Quality assurance** — reviewing blueprints through multi-perspective panel debate (review) and systematic checklist audit (audit)
- **Change evaluation** — evaluating proposed changes to a described system through panel debate (propose)
- **Incremental maintenance** — updating a blueprint after the system it describes has changed (update)
- **Scaffolding** — generating the directory structure for a new blueprint with placeholder files (scaffold)
- **Panel system** — the simulated expert reviewers, their perspectives, blind spots, and the debate protocol they follow
- **Terminology governance** — ensuring shared vocabulary is defined, consistent, and used uniformly
- **Core discipline enforcement** — keeping blueprints at the behaviour level, filtering out implementation details
- **Scope-sizing** — rules for when a single blueprint should be split into multiple

## Adjacent (referenced but not specified here)

- **The systems being documented** — blueprints describe external systems; the content of those blueprints is not in scope here
- **Claude Code skill system** — the platform that loads and executes skills; this blueprint documents what the skill does, not how Claude Code works
- **Mermaid diagram rendering** — the skill produces Mermaid syntax; how it renders is a tool concern

## Explicitly out of scope

- **Implementation architecture** — how the skill files are structured, which XML tags are used, how lazy loading works; these are implementation details of the skill itself
- **Technical design documents** — the skill produces behaviour-level specifications, not architecture docs or system design docs
- **Project management** — the skill does not track tasks, timelines, sprints, or assignments
- **Code generation** — the skill produces documentation, not code
- **Version control workflows** — how blueprints are stored, branched, or merged in git
