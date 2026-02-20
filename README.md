# Blueprint

*A living spec for how things work*

---

A skill for building and maintaining a single source of truth about a system — how it works today, how it should work, and the shared vocabulary everyone uses to talk about it.

## Get started

Once installed in Claude Code, type `/blueprint` to get started. You can also jump to a specific mode:

- `/blueprint:elicit` — build a spec from scratch through structured conversation
- `/blueprint:distill` — document an existing system by walking through what it actually does
- `/blueprint:audit` — review an existing blueprint for gaps, conflicts and quality issues

## What problem this solves

Every product team runs into the same friction:

- **Tribal knowledge.** The system's behaviour lives in the heads of the people who built it. New team members learn through osmosis. When someone leaves, understanding leaves with them.
- **Terminology drift.** Engineering calls it a "job". Product calls it a "task". Support calls it a "ticket". Three teams, one concept, three implementations.
- **No shared reference.** Discussions about changes require reconstructing context from memory, tickets and code. Disagreements about "how it works" are hard to resolve without a canonical source.
- **Intent vs reality gap.** Code captures what the system does, including bugs and expedient decisions. There is no lightweight way to see what it was *meant* to do.

A blueprint is the answer to all of these. One document. The whole team maintains it. When someone asks "how does X work?", the answer is "check the blueprint."

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

## Three ways to use it

**Elicit** — you are specifying something new. Walk through it as a structured conversation: context, actors, terminology, stories, flows, domain model, requirements. End with a complete spec and a list of open questions.

**Distill** — the system exists but is not documented. Walk through the code and existing knowledge to capture what it actually does. Surface the implicit state machines, name the undocumented decisions, resolve the terminology conflicts.

**Audit** — you have a spec and want to stress-test it. Check for missing flows, terminology conflicts, untestable requirements, entities with unreachable states, decisions without rationale.

## Structure

```
blueprint/
├── README.md
├── SKILL.md                          # Main skill — routing, format, core discipline
├── skills/
│   ├── elicit/
│   │   └── SKILL.md                  # Build a blueprint from conversation
│   ├── distill/
│   │   └── SKILL.md                  # Extract a blueprint from an existing system
│   └── audit/
│       └── SKILL.md                  # Review a blueprint for gaps and quality
└── references/
    ├── section-guide.md              # What each section must contain
    └── diagram-guide.md              # Mermaid patterns for flows, states and domain models
```

## License

MIT © 2026
