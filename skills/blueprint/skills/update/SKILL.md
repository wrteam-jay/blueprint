---
name: update
description: Use when a system has changed and its blueprint needs to reflect the change — new behaviour, modified flows, revised rules, or resolved questions.
---

# Blueprint Update

This skill incrementally updates an existing blueprint after a system change. It reads only the affected section files, makes targeted edits, and records the change — without rewriting the entire blueprint.

---

## Inputs

1. **Blueprint directory path** — the `[name].blueprint/` directory to update
2. **Description of what changed** — what happened in the system, what behaviour is new or different

---

## Process

### 1. Read the manifest

Open `README.md` to understand the blueprint's current state: which sections exist, their status, the current version, and the completion tier.

### 2. Identify affected section files

From the change description, determine which section files need updating. Common mappings:

| Change type | Likely affected files |
|-------------|----------------------|
| New flow or behaviour | `scenarios/` (new file), `_index.md`, `stories.md` |
| Modified flow | `scenarios/[name].md` |
| New entity or state | `domain-model.md` |
| New or changed rule | `requirements.md` |
| New actor | `actors.md`, `scenarios/` |
| Terminology change | `terminology.md`, any file using the old term |
| Resolved question | `questions.md`, `decisions.md` |
| Scope change | `scope.md` |

### 3. Read only those files

Load the affected section files into context. Do not read the entire blueprint — targeted loading is the point of the multi-file format.

### 4. Check staleness signals

Consult the [maintenance guide](../../references/maintenance.md) staleness signals. Does this change reveal other sections that may also be stale? If so, note them for review.

### 5. Draft updates to affected files

Edit each affected file. Follow the format and conventions in the [section guide](../../references/section-guide.md). Preserve existing content that is still accurate — do not rewrite sections unnecessarily.

### 6. Update changelog.md

Add a changelog entry for every meaningful change. Follow the delta protocol in the [maintenance guide](../../references/maintenance.md):

```markdown
| [new version] | [date] | [author] | [one sentence per substantive change] |
```

### 7. Update decisions.md

If any decisions were made as part of this update — terminology resolutions, scope boundaries, rule changes — record them with rationale.

### 8. Update the manifest

In `README.md`:
- Bump the version if the change is meaningful (see delta protocol)
- Update the `Last updated` date
- Update section statuses if any changed
- Update the completion tier if it advanced

### 9. Quick review

Convene a quick review (5 panellists: product owner, engineer, user advocate, completeness advocate, simplicity advocate) to validate that the update is coherent with the rest of the blueprint. For trivial changes (typo fixes, resolving a single open question), use 3 panellists (product owner, engineer, user advocate).

---

## Output

- Updated section files (only the ones that changed)
- Updated `changelog.md` with entry
- Updated `decisions.md` if decisions were made
- Updated `README.md` manifest (version, date, section status)

---

## References

- [Maintenance guide](../../references/maintenance.md) — staleness signals, delta protocol, ownership
- [Section guide](../../references/section-guide.md) — what each section must contain
- [Review panel](../../TEAM.md) — panellist roles for quick review
