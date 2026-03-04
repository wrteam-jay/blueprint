# Scenario: Audit a blueprint

## Trigger

A Spec Owner invokes the skill to perform a systematic checklist audit of a blueprint — structured findings without panel debate.

## Preconditions

- A blueprint exists with content to audit (at least Tier 1).

## Steps

1. **Read the full blueprint.** All section files are loaded.
2. **Check six dimensions sequentially:**
   - **Terminology consistency** — same concept under multiple names? One term meaning different things?
   - **Scenario coverage** — every actor has a scenario? Every story has a delivering scenario? Every entity state is reachable?
   - **Domain model completeness** — every entity has definition, states, transitions, lifecycle owner?
   - **Requirements quality** — testable? No weasel words? Business rules sourced?
   - **Decision log and open questions** — rationale present? Owners assigned? Deadlines set?
   - **Implementation leakage** — databases, endpoints, libraries, UI elements in the spec?
3. **Classify findings.** Each finding is either:
   - **Blocking** — must fix before the blueprint is reliable enough to use as a reference.
   - **Advisory** — should fix to improve quality, but the blueprint is usable without it.
4. **Produce the audit report.** Summary table, blocking findings, advisory findings.

## Outcomes

- A structured audit report with findings classified by dimension and severity.
- Blocking findings clearly separated from advisory findings.
- No debate — just facts and classifications.

## Error paths

- **Blueprint is at Tier 1 but audited against Tier 3 expectations.** The skill checks the declared tier and only audits against the expectations for that tier. Missing Tier 3 sections are not findings for a Tier 1 blueprint.
- **No findings.** A clean audit report is produced — this is a valid outcome, not an error. The report still states what was checked and at what tier level.
- **Audit reveals systematic issues.** Multiple findings in the same dimension suggest a pattern rather than isolated problems. The skill groups related findings and identifies the root cause: "5 findings in terminology consistency suggest the terminology was not established before scenarios were written. Consider a terminology pass before addressing individual findings."
- **Audit reveals the blueprint is fundamentally misscoped.** Disconnected actor groups, unrelated entity clusters, or >20 terms. The skill flags this as a blocking finding at the blueprint level — not a section-level issue — and recommends splitting before further investment.
- **Declared tier does not match actual content.** The README says Tier 2 but requirements are empty and the domain model is a placeholder. The skill flags the mismatch: "Declared tier is 2 (Workable) but actual content matches Tier 1 (Skeleton). Recommend updating the declared tier or completing the missing sections."
- **Audit finds findings that contradict each other.** Two findings suggest opposite fixes (e.g., "this term is undefined" and "this term is used inconsistently" — if you define it, the inconsistency may resolve). The skill groups related findings and notes the dependency.
