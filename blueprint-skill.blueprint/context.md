# Context

Product knowledge is scattered, implicit, and decays. Code captures what a system does — including its bugs and hacks. People carry why — but they leave, forget, or disagree. There is no single artefact that captures observable system behaviour in a way the whole team can use as a shared reference.

Teams try to solve this with wikis, Confluence pages, Notion docs, and README files. These efforts share a pattern: someone writes a document once, it falls behind the system within weeks, and nobody trusts it enough to use as a basis for decisions. The document was never wrong — it just stopped being maintained, because maintenance is overhead that competes with development work.

The blueprint skill exists because:

1. **Documentation is a maintenance problem, not a writing problem.** Most teams can write a spec. Few teams keep it current. The skill offloads the maintenance burden — consistency checks, cross-references, terminology alignment, section updates — to AI, so people can focus on domain knowledge and decisions.

2. **Specs written by one role serve that role.** A developer writing documentation produces developer documentation. A product manager produces product documentation. Neither serves the whole team. The skill uses simulated multi-perspective review panels to ensure the output works for developers, designers, QA, product managers, and business stakeholders alike.

3. **Shared vocabulary is a prerequisite for clear communication.** Teams waste time in meetings because the same word means different things to different people. The skill treats terminology as a first-class section, not an afterthought, and enforces consistent usage throughout.

4. **A spec should describe behaviour, not implementation.** Implementation details change faster than behaviour. A spec that names databases, endpoints, or UI components becomes stale the moment someone refactors. The skill enforces a strict separation: blueprints describe what the system does and why — never how it is built.
