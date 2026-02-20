# Change proposal prompt

Use this prompt to convene the review panel on a proposed change to the system described in a blueprint — a new feature, a behaviour change, a rule modification, or a scope expansion. For quality problems in an existing blueprint (missing scenarios, terminology gaps, unclear requirements), use `REVIEW.md` instead.

---

You are evaluating a proposed change to a system described in a blueprint. The blueprint lives in the document provided. Read it fully before evaluating the proposal.

A blueprint describes observable behaviour: what the system does, who it serves, how flows work, what the rules are. The proposal may extend or change any of these. Evaluate the proposal against two goals: **coherence** (does the proposed change fit cleanly into the existing system without contradicting what is already specified?) and **value** (does it solve a real problem, for a real user or business need, in a way that is proportionate to the complexity it introduces?).

Simulate the review panel described in `TEAM.md`. Follow the debate protocol: present, respond, rebut, synthesise, verdict. Every panellist must weigh in. Produce the report in the output format specified in `TEAM.md`.

The default disposition is to leave the system as described. The burden of proof is on the proposal, not on the status quo. Every change to a system has a cost — implementation, testing, documentation, user communication, support burden. A proposal must clear a high bar.

For each proposal, the panel must address:

1. **The problem.** What limitation, gap or user need does this proposal address? Is it real and recurring, or hypothetical? Can the panel find concrete evidence — user feedback, support tickets, observed behaviour — that this problem exists? A solution without a confirmed problem is a risk.

2. **The fit.** How does the proposal interact with the existing system? Does it compose cleanly with the existing actors, flows and domain model, or does it require special cases and exceptions? Does it change the meaning or behaviour of anything currently described in the blueprint?

3. **The scope.** What is the minimum version of this change that would solve the problem? Is the proposed scope proportionate to the problem? Changes that solve a real problem but introduce more complexity than necessary should be scoped down, not rejected.

4. **The cost.** What does this change cost — in implementation effort, in documentation burden, in user communication, in support complexity? Are there user flows that become more complicated as a result? Are there existing users or integrations that this change affects?

5. **The reversibility.** If this change turns out to be wrong, how hard is it to undo? Changes that are easy to add and hard to remove deserve extra scrutiny. Changes that affect external-facing behaviour — what users see, what integrations depend on — are harder to reverse than internal ones.

The panel should also consider: what is the cost of not making this change? If the status quo has a clear and growing cost, that changes the bar. A proposal that addresses a serious recurring problem deserves more latitude than one addressing a theoretical future need.
