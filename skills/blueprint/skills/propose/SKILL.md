---
name: propose
description: Use when evaluating a proposed change to a system described in a blueprint — a new feature, behaviour change, rule modification, or scope expansion. Convenes the review panel.
---

<skill name="propose">

<brief>Convene the review panel to evaluate a proposed change to a system described in a blueprint — new feature, behaviour change, rule modification, or scope expansion. For quality problems in an existing blueprint, use review instead.</brief>

Read the full blueprint before evaluating the proposal. Evaluate against coherence (does the change fit without contradicting what is specified?) and value (does it solve a real problem proportionate to the complexity it introduces?).

Simulate the review panel from <ref src="../../TEAM.md" load="eager"/>. Follow debate protocol. Every panellist weighs in.

Default disposition: leave the system as described. Burden of proof is on the proposal. Every change has a cost — implementation, testing, documentation, user communication, support burden.

<evaluation-criteria>
<criterion n="1" name="The problem">What limitation or need does this address? Is it real and recurring, or hypothetical? Concrete evidence — user feedback, support tickets, observed behaviour?</criterion>
<criterion n="2" name="The fit">How does it interact with existing actors, flows and domain model? Composes cleanly, or requires special cases? Changes meaning of anything currently specified?</criterion>
<criterion n="3" name="The scope">What is the minimum version that solves the problem? Is proposed scope proportionate? Over-scoped changes should be scoped down, not rejected.</criterion>
<criterion n="4" name="The cost">Implementation effort, documentation burden, user communication, support complexity? User flows that become more complicated? Existing users or integrations affected?</criterion>
<criterion n="5" name="The reversibility">If wrong, how hard to undo? Changes easy to add and hard to remove deserve extra scrutiny. External-facing changes are harder to reverse than internal ones.</criterion>
</evaluation-criteria>

Also consider: what is the cost of not making this change? A serious recurring problem deserves more latitude than a theoretical future need.

Produce the report in the output format specified in <ref src="../../TEAM.md" name="Review panel" load="eager"/>.
<ref src="../../references/section-guide.md" name="Section guide" load="lazy"/>

</skill>
