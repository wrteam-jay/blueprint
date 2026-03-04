<ref-guide name="maintenance">

<brief>Keeping a blueprint current: detecting staleness, triggering reviews, recording changes, and assigning ownership.</brief>

<signals name="staleness">
Scenario-level: scenario references nonexistent entity state, flow that engineering says changed, end state contradicts domain model, acceptance criteria no longer satisfied.

Terminology: term doesn't match current codebase, new term in team conversation not in blueprint, unresolved term conflict between teams.

Domain model: entity has new undocumented state, relationship cardinality changed, lifecycle owner changed, invariant relaxed or tightened.

Requirements: "Must Have" not currently met with no open question, business rule source changed, NFR threshold no longer targeted.

Decision log: decision being re-debated (rationale may be wrong), outcome changed but log not updated, references nonexistent stakeholder or policy.
</signals>

<watch-for name="review-triggers">
<w>After a major release — review touched scenarios and domain model, update changelog</w>
<w>After an incident revealing undocumented behaviour — document it, open requirement if wrong</w>
<w>After significant user research — update stories, evidence annotations, deprecate disproven stories</w>
<w>When onboarding a new team member — have them read and flag gaps; their confusion is diagnostic</w>
<w>When a change proposal is adopted — update blueprint, record in changelog and decision log</w>
<w>Quarterly — "Is every scenario still how the system actually works?"</w>
</watch-for>

<process name="delta-protocol">
Edit only affected section files. After edits, update changelog.md and README.md section status.

Requires version bump: new scenario, substantive scenario change, entity state added/removed/renamed, relationship cardinality changed, business rule changed, new actor, new/changed requirement, terminology change.

Does not require version bump: typo/grammar, clarifying wording, adding open question, resolving open question without spec change.

Changelog entry format:

| Version | Date | Author | Summary |
|---------|------|--------|---------|

One sentence per change. Name the section. Reference resolved questions and new decisions. If correcting wrong behaviour, say so.

Decision log entry (when change involves a design decision):

```markdown
**D-012** — 2025-02-15
*Decision:* Payment retry policy — 3 attempts over 7 days, then subscription suspended.
*Rationale:* Finance data shows 70% of failures resolve within 7 days. Immediate suspension rejected as too aggressive.
*Decided by:* Product + Finance (meeting 2025-02-12)
*Supersedes:* D-004 (previous: retry once after 24 hours)
```
</process>

<process name="ownership">
Spec owner: one named person (not a team). Knows when stale, triggers reviews, ensures questions resolved, keeps decision log current, approves changes. Does not have to write all content — accountable for accuracy.

Section ownership (large blueprints): individual sections may have owners notified on changes and responsible for flagging staleness.

Open question ownership: every question must have an owner. "TBD" is not an owner.
</process>

<process name="deprecation">
When a system is retired: change status to Deprecated, add note at top, keep accessible but clearly marked. Do not delete — preserves decision history.

```markdown
> **DEPRECATED** — This feature was retired on 2025-06-01 and replaced by the
> [New Feature Name] blueprint. This document is kept for historical reference only.
```
</process>

<traps>
<trap name="update-later">"We'll update later." Later does not happen. Update when the system changes, at the same time.</trap>
<trap name="vague-changelog">Changelog that says "updated." Name what changed so readers know if their version is stale.</trap>
<trap name="verbal-resolution">Questions resolved in meetings but not in the document. Write it down immediately.</trap>
<trap name="code-comments">"I'll add a comment in the code." Code is read by engineers; blueprints by the whole team. Both need updating.</trap>
<trap name="historical-document">The Scenarios section always describes how the system works now, not how it worked before.</trap>
</traps>

</ref-guide>
