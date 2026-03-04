# XML Schema Reference

Tag vocabulary for blueprint skill files. XML replaces the markdown body below YAML frontmatter. Plain English inside tags; attributes carry metadata.

## Conventions

- Max 2 levels of nesting
- Attributes: metadata. Body: content.
- `priority`: must | should | could (MoSCoW)
- `severity`: blocking | advisory
- `load`: eager | lazy (default: lazy)
- Templates inside tags use markdown (Claude generates markdown output)

## Tags

### Structure

| Tag | Parent | Attrs | Purpose |
|-----|--------|-------|---------|
| `<skill>` | root | `name` | Root element, replaces heading + description |
| `<brief>` | skill | — | 1-3 sentence operational summary |
| `<ref>` | skill, any | `src`, `load`, `section`, `name` | Lazy/eager load reference file |

### Rules & Constraints

| Tag | Parent | Attrs | Purpose |
|-----|--------|-------|---------|
| `<constraints>` | skill | `name` | Container for rules/prohibitions |
| `<c>` | constraints | `rule`, `priority`, `severity` | Single constraint; body = rationale |
| `<core-discipline>` | skill | — | Behaviour vs implementation test |
| `<yes>` | core-discipline | — | Passes the behaviour test |
| `<no>` | core-discipline | — | Fails the behaviour test (implementation) |

### Workflows

| Tag | Parent | Attrs | Purpose |
|-----|--------|-------|---------|
| `<process>` | skill | `name` | Named ordered workflow |
| `<phase>` | process | `n`, `name` | Major phase in a workflow |
| `<step>` | process, phase | `n`, `name` | Single step |

### Questions & Verification

| Tag | Parent | Attrs | Purpose |
|-----|--------|-------|---------|
| `<questions>` | skill, phase | `name` | Container for structured questions |
| `<q>` | questions | `probe` | Single question; `probe` marks follow-ups |
| `<checkpoint>` | phase, step, skill | — | Verification prompt |

### Routing

| Tag | Parent | Attrs | Purpose |
|-----|--------|-------|---------|
| `<routing>` | skill | — | Skill routing table |
| `<route>` | routing | `task`, `skill` | Single route; body = when to use |

### Sections & Tiers

| Tag | Parent | Attrs | Purpose |
|-----|--------|-------|---------|
| `<sections>` | skill | — | Blueprint section definitions |
| `<section>` | sections | `n`, `name` | One section; body = description |
| `<tiers>` | skill | — | Completion tier definitions |
| `<tier>` | tiers | `n`, `name` | One tier; body = what it contains |

### Review Panel

| Tag | Parent | Attrs | Purpose |
|-----|--------|-------|---------|
| `<panel>` | skill | `name` | Panel definition (default/extended) |
| `<panellist>` | panel | `role`, `cares-about`, `blind-spot`, `card` | One panellist; body = full description |

### Debate System

| Tag | Parent | Attrs | Purpose |
|-----|--------|-------|---------|
| `<debate>` | skill | — | Debate system definition |
| `<protocol>` | debate | — | Debate protocol steps |
| `<verdicts>` | debate | — | Container for verdict definitions |
| `<verdict>` | verdicts | `name` | One verdict; body = definition |
| `<modes>` | debate | — | Panel size modes (quick/standard/full) |

### Audit & Review

| Tag | Parent | Attrs | Purpose |
|-----|--------|-------|---------|
| `<dimension>` | skill | `n`, `name` | Audit dimension; body = checks |
| `<focus-areas>` | skill | — | Container for review focus areas |
| `<focus-area>` | focus-areas | `n`, `name` | One focus area; body = what to check |
| `<evaluation-criteria>` | skill | — | Container for proposal criteria |
| `<criterion>` | evaluation-criteria | `n`, `name` | One criterion; body = what to evaluate |

### Output & Examples

| Tag | Parent | Attrs | Purpose |
|-----|--------|-------|---------|
| `<template>` | skill, any | `name` | Output format template (markdown inside) |
| `<example>` | skill | `n`, `name` | Worked example |
| `<bad>` | example | — | Bad example |
| `<why-bad>` | example | — | Why the bad example fails |
| `<good>` | example | — | Good example |

### Anti-patterns & Principles

| Tag | Parent | Attrs | Purpose |
|-----|--------|-------|---------|
| `<traps>` | skill | — | Container for anti-patterns |
| `<trap>` | traps | `name` | One anti-pattern; body = description |
| `<principles>` | skill | — | Container for guiding principles |
| `<principle>` | principles | `name` | One principle; body = description |

### Conversation

| Tag | Parent | Attrs | Purpose |
|-----|--------|-------|---------|
| `<mechanics>` | skill | — | Conversation mechanics |
| `<mechanic>` | mechanics | `name` | One mechanic; body = how to do it |

### Detection & Checklists

| Tag | Parent | Attrs | Purpose |
|-----|--------|-------|---------|
| `<signals>` | skill | `name` | Detection signals |
| `<s>` | signals | — | One signal |
| `<checklist>` | skill | `name` | Verification checklist |
| `<check>` | checklist | — | One check item |
| `<watch-for>` | phase, step, skill | — | Container for warning signals |
| `<w>` | watch-for | — | One warning signal |

### Data

| Tag | Parent | Attrs | Purpose |
|-----|--------|-------|---------|
| `<table>` | skill, any | `name` | Lookup table |
| `<row>` | table | varies | One row; attrs are columns |
| `<findings>` | skill | — | Review/audit output structure |
| `<finding>` | findings | `id`, `severity` | One finding |

### Reference Guide (for reference files)

| Tag | Parent | Attrs | Purpose |
|-----|--------|-------|---------|
| `<ref-guide>` | root | `name` | Root element for reference files (replaces `<skill>`) |
