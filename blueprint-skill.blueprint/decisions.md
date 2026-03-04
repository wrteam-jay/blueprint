# Decision Log

## DEC-1: Behaviour over implementation

**Date:** Pre-v1
**Decision:** Blueprints describe observable behaviour only — never implementation.
**Why:** Implementation details change faster than behaviour. A spec that names databases or endpoints becomes stale the moment someone refactors. The whole team (PM, QA, design, business) can understand behaviour; only engineering understands implementation. Keeping implementation out means the spec serves everyone.
**Alternatives considered:** Allow "implementation notes" sections — rejected because they blur the line and eventually dominate the document.

## DEC-2: Singular spec ownership

**Date:** Pre-v1
**Decision:** Every blueprint has exactly one Spec Owner — one person, not a team.
**Why:** Shared ownership means diffused accountability. When everyone owns it, nobody updates it. One person must be the arbiter for split verdicts, the assigner of open question owners, and the one who decides when the blueprint needs review.
**Alternatives considered:** Rotating ownership, team ownership — both rejected because they produce documents with no clear authority.

## DEC-3: Simulated panel for multi-perspective review

**Date:** Pre-v1
**Decision:** Quality review uses AI-simulated expert panels rather than requiring actual multi-role review meetings.
**Why:** Getting a product manager, engineer, QA lead, and designer into the same review meeting is expensive and rare. Simulating their perspectives produces 80% of the value at near-zero coordination cost. The panel is a heuristic, not a replacement for real stakeholder input — but it catches the most common blind spots.
**Alternatives considered:** Template-based checklists only (became the audit skill — both approaches coexist), requiring actual multi-role reviews (too expensive for routine use).

## DEC-4: Directory of files over single document

**Date:** Pre-v1
**Decision:** A blueprint is a directory of markdown files, not a single document.
**Why:** Targeted loading (only read the section you're updating), scenarios grow independently, smaller files mean better diffs and easier edits, cross-referencing with relative paths works naturally. For AI consumption specifically: smaller files stay within context window limits.
**Alternatives considered:** Single markdown file — rejected because it becomes unwieldy past Tier 1, and AI tools struggle with surgical edits in long documents.

## DEC-5: Consensus over voting

**Date:** Pre-v1
**Decision:** The panel reaches verdicts through debate convergence, not voting.
**Why:** Voting produces outcomes without reasoning. A 3-2 vote tells you nothing about why the minority disagreed or whether their concerns were addressed. Debate convergence forces the panel to engage with objections until they're resolved, withdrawn, or explicitly recorded as trade-offs.
**Alternatives considered:** Majority voting, weighted voting — both rejected because they skip the reasoning step that makes verdicts useful.

## DEC-6: Terminology as first-class section

**Date:** Pre-v1
**Decision:** Terminology is a dedicated section (Section 4), not an appendix or inline definitions.
**Why:** Shared vocabulary is the foundation of clear communication. If a team doesn't agree on what "pipeline" or "workspace" means, every other discussion is built on ambiguity. Making terminology explicit and early forces resolution of conflicts before they cause downstream confusion in scenarios and requirements.
**Alternatives considered:** Inline definitions on first use — rejected because the same term would need re-definition in every section, and there's no single place to check for consistency.

## DEC-7: XML over markdown for skill files

**Date:** v2
**Decision:** Skill files use XML tags for semantic structure instead of markdown-only formatting.
**Why:** XML provides machine-parseable semantic boundaries (constraints, phases, mechanics, questions) that markdown headings and lists cannot express. AI can reason about `<constraint>` vs `<mechanic>` vs `<question>` distinctly. Markdown remains for content within tags — XML is structural scaffolding.
**Alternatives considered:** Pure markdown with conventions, YAML, JSON — markdown lacks semantic structure; YAML/JSON are too rigid for mixed prose and structure.

## DEC-8: One blueprint per system

**Date:** 2026-03-04
**Decision:** There is one blueprint per system or project. No cross-blueprint conflicts to manage.
**Why:** Multiple overlapping blueprints create a coordination problem — which one is authoritative? If there's a conflict within a single blueprint, the skill surfaces it to the Spec Owner for resolution. Cross-blueprint machinery is unnecessary complexity.
**Alternatives considered:** Multiple blueprints with cross-references and shared terminology — rejected as over-engineering for the actual use case.

## DEC-9: Panel is extensible

**Date:** 2026-03-04
**Decision:** The 9 panellists are defaults, not a closed set. Users can add domain-specific panellists (e.g., security advocate, compliance advocate) when the domain calls for it.
**Why:** Different domains have different blind spots. Auth systems need a security perspective. Healthcare systems need compliance. Fixed panels can't anticipate every domain. Extensibility lets the panel match the context.
**Alternatives considered:** Fixed panel only — rejected because it forces generic perspectives onto specialised domains.

## DEC-10: Active staleness detection

**Date:** 2026-03-04
**Decision:** The skill actively checks for staleness rather than relying on the Spec Owner to notice. Three signals: time since last update vs system changes, sections referencing entities/flows that no longer exist, and review triggers (major release, team change). Major staleness is surfaced to the Spec Owner rather than silently fixed.
**Why:** Passive staleness detection doesn't work — people don't notice gradual drift. The skill has access to both the blueprint and the system; it should use that to flag when they diverge. Major staleness needs human judgement, so surface it rather than auto-fix.
**Alternatives considered:** Purely owner-driven review schedule — rejected because it requires discipline that competes with development priorities.

## DEC-11: Blueprint documents current version only

**Date:** 2026-03-04
**Decision:** The blueprint always documents the current/latest version of the system. Version history lives in version control, not in the spec.
**Why:** Annotating "in v1 this works like X, in v2 like Y" makes the spec harder to read for its primary purpose — understanding how the system works now. Git provides full history for anyone who needs it. The blueprint is a snapshot of current truth, not an archive.
**Alternatives considered:** Version annotations within the blueprint, separate blueprints per version — both rejected as unnecessary complexity given version control already tracks history.

## DEC-12: Adaptive documentation approach

**Date:** 2026-03-04
**Decision:** The skill adapts its approach (top-down vs bottom-up, depth-first vs breadth-first) based on context rather than enforcing a fixed order. Default is top-down: overview first, then features, then details. Depth-first into a thread until complete, then next thread.
**Why:** Different systems and different authors think in different orders. Forcing breadth-first on someone who naturally thinks depth-first produces worse output. The skill should read the situation and adapt — unless the author explicitly requests an approach.
**Alternatives considered:** Fixed top-down only — rejected because it doesn't match how all people think about their systems.

## DEC-13: Writing philosophy

**Date:** 2026-03-04
**Decision:** Blueprints follow specific writing principles:
- **Granularity scales with complexity** — simple things explained simply; complex things get the space they need.
- **Dual representation** — diagrams always accompanied by text description of the same content. Never assume the diagram alone is sufficient.
- **Respect the reader** — acknowledge their intelligence while recognising they don't know the system. Not condescending, not dumbing down, not jargon-heavy.
- **The invisible things matter** — sentence length, tone, writing style, and reader psychology determine whether the document is actually read and understood.
**Why:** A blueprint that's technically complete but poorly written fails its purpose. The audience spans developers to CEOs — the writing must work for all of them. Diagrams exclude text-oriented readers; text without diagrams excludes visual learners. Condescending tone makes experts stop reading; jargon-heavy prose makes newcomers stop reading.
**Alternatives considered:** No explicit writing guidance (let quality emerge) — rejected because quality doesn't emerge without intent, and different authors default to different styles.

## DEC-14: Author as Domain Expert in solo workflows

**Date:** 2026-03-04
**Decision:** In solo developer workflows, the Spec Author is also the Domain Expert. The skill consults them directly for conflicts, issues, and clarifications. If the author says they don't have enough knowledge about something, it is documented as an open question so they or someone else can resolve it later.
**Why:** The original design treated "no Domain Expert" as a degraded mode. In practice, many systems are documented by the person who built them — they are both roles. The skill should treat this as normal, not exceptional. When knowledge gaps exist, documenting them honestly is better than fabricating answers or refusing to proceed.
**Alternatives considered:** Requiring a separate Domain Expert — rejected because it excludes the most common real-world scenario.
