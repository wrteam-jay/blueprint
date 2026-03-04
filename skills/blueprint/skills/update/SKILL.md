---
name: update
description: Use when a system has changed and its blueprint needs to reflect the change — new behaviour, modified flows, revised rules, or resolved questions.
---

<skill name="update">

<brief>Incrementally update an existing blueprint after a system change. Read only affected sections, make targeted edits, record the change — without rewriting the entire blueprint.</brief>

Inputs: blueprint directory path, description of what changed.

<process name="update">

<step n="1" name="Read the manifest">
Open README.md: current state, sections, version, completion tier.
</step>

<step n="2" name="Identify affected files">
<table name="change-mapping">
<row change="New flow or behaviour" files="scenarios/ (new file), _index.md, stories.md"/>
<row change="Modified flow" files="scenarios/[name].md"/>
<row change="New entity or state" files="domain-model.md"/>
<row change="New or changed rule" files="requirements.md"/>
<row change="New actor" files="actors.md, scenarios/"/>
<row change="Terminology change" files="terminology.md, any file using old term"/>
<row change="Resolved question" files="questions.md, decisions.md"/>
<row change="Scope change" files="scope.md"/>
</table>
</step>

<step n="3" name="Read only affected files">
Targeted loading is the point of the multi-file format.
</step>

<step n="4" name="Check staleness signals">
Consult <ref src="../../references/maintenance.md" section="staleness-signals" load="lazy"/>. Does this change reveal other stale sections?
</step>

<step n="5" name="Draft updates">
Edit affected files. Follow <ref src="../../references/section-guide.md" load="lazy"/>. Preserve existing accurate content.
</step>

<step n="6" name="Update changelog.md">
Add entry per delta protocol: | [version] | [date] | [author] | [one sentence per change] |
</step>

<step n="7" name="Update decisions.md">
If decisions were made — terminology resolutions, scope boundaries, rule changes — record with rationale.
</step>

<step n="8" name="Update manifest">
In README.md: bump version, update date, update section statuses, update tier if advanced.
</step>

<step n="9" name="Quick review">
Convene 5-panellist quick review (product owner, engineer, user advocate, completeness advocate, simplicity advocate). For trivial changes (typo, single open question), use 3 panellists.
</step>

</process>

Output: updated section files, updated changelog.md, updated decisions.md (if applicable), updated README.md manifest.

<ref src="../../references/maintenance.md" name="Maintenance guide" load="lazy"/>
<ref src="../../references/section-guide.md" name="Section guide" load="lazy"/>
<ref src="../../TEAM.md" name="Review panel" load="lazy"/>

</skill>
