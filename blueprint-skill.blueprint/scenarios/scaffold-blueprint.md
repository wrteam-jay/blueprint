# Scenario: Scaffold a new blueprint

## Trigger

A Spec Author invokes the skill to generate an empty directory structure for a new blueprint.

## Preconditions

- None — scaffolding is the entry point for a new blueprint.

## Steps

1. **Ask four questions:**
   - What is the blueprint name?
   - What is the scope (one sentence)?
   - Who is the Spec Owner?
   - Are there related systems or context the blueprint should reference?
2. **Generate the directory structure.** Create the `[name].blueprint/` directory with all 11 section files, the `scenarios/` subdirectory with `_index.md`, and the `README.md` manifest.
3. **Populate placeholder files.** Each file contains a section heading and a brief hint (as an HTML comment) describing what belongs in that section.
4. **Set the README manifest.** Status: Draft. Tier: Scaffold (Tier 0). All sections: Pending. Spec Owner: the named individual.

## Outcomes

- A complete directory structure ready for content.
- README manifest with metadata and all sections listed as Pending.
- Tier 0 (Scaffold) declared — below Tier 1 because no content exists yet.

## Error paths

- **Blueprint name conflicts with an existing directory.** The skill warns and asks for confirmation or a different name. Does not overwrite an existing blueprint directory.
- **No Spec Owner named.** The skill requires one — it does not create an unowned blueprint. If the author says "I'll figure it out later," the skill insists: "A blueprint without an owner has no one responsible for its accuracy. Who should own this?"
- **Scope is too vague.** The one-sentence scope is too broad ("everything about the system") or too narrow ("the login button"). The skill asks for refinement: "That scope seems [too broad / too narrow]. Can you be more specific about what this blueprint should cover and what it should not?"
- **Author immediately wants to start filling in content.** The skill completes the scaffold first, then offers to transition into elicitation or distillation. It does not mix scaffolding with content creation — the scaffold is a clean structural starting point.
