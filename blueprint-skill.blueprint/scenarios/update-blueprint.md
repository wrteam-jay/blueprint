# Scenario: Update a blueprint

## Trigger

A Spec Author invokes the skill because the system has changed and the blueprint needs to reflect it. Can also be triggered by the skill's staleness detection identifying that the blueprint and system have diverged.

## Preconditions

- A blueprint exists for the system.
- The nature of the change is known (new flow, removed feature, terminology change, etc.), or the skill has detected staleness and needs the author to confirm what changed.

## Steps

1. **Identify the change type.** The skill determines what kind of change occurred and maps it to affected files:
   - New flow → scenarios/, _index.md, stories.md
   - Removed feature → scenarios/, stories.md, domain-model.md, requirements.md
   - Terminology change → terminology.md + every file using the old term
   - New entity or state → domain-model.md, scenarios that reference it
   - New business rule → requirements.md, affected scenarios
   - Behaviour change → affected scenarios, requirements.md
2. **Read only affected files.** The skill does not re-read the entire blueprint for a targeted change.
3. **Apply the updates.** Section files are modified to reflect the new state of the system.
4. **Cross-reference check.** The skill verifies that the change is consistent across all affected files — no orphaned terms, no scenarios referencing removed entities, no actors that lost their only scenario.
5. **Quick review.** A 3- or 5-panellist review of the changes only (not the full blueprint).
6. **Update changelog.** A new entry records what changed, why, and when.
7. **Update decisions.md** if the change involved a deliberate decision.
8. **Update README.md** if section statuses changed.

## Outcomes

- Blueprint reflects the current state of the system.
- Changelog records the delta.
- Cross-references are consistent.

## Error paths

- **Change is too large for incremental update.** The skill recognises when the delta is so significant that a full re-elicitation or re-distillation would be more reliable — e.g., more than half the scenarios are affected, or the core context has changed. It recommends the appropriate approach and explains why.
- **Change introduces a terminology conflict.** The skill surfaces the conflict and resolves it before proceeding — does not leave two terms for the same concept. If the new term replaces an old one, the skill updates every occurrence across all files.
- **Change breaks an invariant.** The skill flags the break (e.g., an actor referenced in a scenario but no longer defined, an entity state with no transition leading to it) and requires resolution before completing the update.
- **Multiple simultaneous changes.** Several things changed at once (e.g., after a major release). The skill processes them one at a time, in dependency order: terminology first (since everything depends on it), then domain model, then scenarios, then requirements. Each change's cross-reference impact is checked before moving to the next.
- **Staleness detected but author cannot confirm what changed.** The skill has detected drift but the author doesn't know exactly what happened. The skill falls back to comparing the blueprint against the current system (a mini-distillation of the affected area) and presents the discrepancies for the author to confirm or correct.
- **Quick review produces split verdicts.** A change that seemed straightforward turns out to be contested. The skill escalates: the split items go to the Spec Owner, and the update is not marked as complete until the splits are resolved. The changelog notes the update is partial.
- **Change cascades further than expected.** An update to one section reveals that other sections are also stale — the change exposed pre-existing drift. The skill reports the cascade: "Updating [section] revealed that [other sections] are also inconsistent with the system. These should be addressed in a follow-up update."
