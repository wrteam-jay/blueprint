---
name: elicit
description: Use when building a blueprint from scratch through conversation — specifying a new feature, capturing a planned system, or turning stakeholder descriptions into a structured living spec.
---

<skill name="elicit">

<brief>Build a blueprint through conversation. Surface ambiguities, establish shared vocabulary, trace real flows end-to-end, produce a document the whole team can reason about. Same principles whether talking to a product manager about a new feature or a founder describing a system.</brief>

<constraints>
<c rule="No scenario without a trigger">A scenario without a trigger is a story without a beginning</c>
<c rule="No scenario without a failure path">Happy paths alone are half a spec</c>
<c rule="No circular definitions">Defining a term using that term gives the reader nothing</c>
<c rule="No business rule without a source">If you cannot name the policy, regulation or decision, mark it as an open question</c>
<c rule="No inferred actors — ask">"The system sends an email" has a missing actor. Who triggers the send?</c>
<c rule="No implementation in the blueprint">Rephrase at the behaviour level. See core discipline.</c>
<c rule="No assumptions for open questions">If you do not know, open a question and assign it. Do not invent an answer.</c>
<c rule="No skipping verification checkpoints">Show captures, get confirmation, then continue</c>
<c rule="No silent contradictions">Surface immediately when detected</c>
<c rule="No accepting 'it depends'">It is the location of a requirement. Ask: "Depends on what? Walk me through the cases."</c>
<c rule="No generating a complete spec from a single sentence">Elicitation is a conversation. Generating all at once produces confident-sounding fiction.</c>
</constraints>

<mechanics>

<mechanic name="opening">
Start every session with:
1. Establish goal: "We are going to capture how this works and what it must do — not how we will build it."
2. Establish scope: "What are we covering today? One flow, or the whole feature?"
3. One-sentence question: "In one sentence, what does this thing do?"
The one-sentence answer reveals alignment before spending time on details.
</mechanic>

<mechanic name="one-question-at-a-time">
Ask one question. Wait for the answer. Probe the answer. Then ask the next. Bundled questions produce bundled answers that are hard to separate later.
</mechanic>

<mechanic name="verification-checkpoints">
After each phase, show what has been captured and ask for confirmation:
"Here's what I've captured so far. Does this match your understanding? Is anything missing or wrong?"
Show only the section just captured — not the whole draft. Checkpoints prevent wrong work accumulating silently.
</mechanic>

<mechanic name="handling-i-dont-know">
Convert to an open question immediately:
"That's fine — let me note that as an open question rather than assume. Who should resolve this? By when?"
Then move on. Accumulate open questions; return to them at the end.
</mechanic>

<mechanic name="handling-contradictions">
Surface immediately:
"I want to flag a conflict. Earlier you said [X]. Now you're saying [Y]. These cannot both be true. Which takes precedence? Or is there a condition?"
Do not silently note both. Name the conflict, explore it, resolve or log as open question with owner.

Track contradictions actively. Keep a mental (or explicit) list of key facts stated: statuses, rules, actor capabilities. When a new statement touches the same area, check it against what was said before.
</mechanic>

<mechanic name="handling-scope-creep">
Park it:
"That sounds important — let me note it. I'll add it to the out-of-scope list. For now, can we stay focused on [current topic]?"
Scope creep produces blueprints that are accurate about many things but authoritative about nothing.
</mechanic>

<mechanic name="phase-transitions">
Name transitions explicitly:
"Good — I have the actors and terminology captured. Let me show you what I have, then we'll move to user stories."
</mechanic>

<mechanic name="closing">
At the end of every session:
1. Show the full draft (or sections covered this session)
2. Read through open questions — assign owner and deadline to each
3. Record decisions made during the session in the decision log with rationale
4. State what is covered and what still needs follow-up
</mechanic>

</mechanics>

<questions name="scoping">
<q>"What is this blueprint about — one sentence?" — gets to the core without implementation. If the answer contains a tech stack, redirect.</q>
<q>"Is this new, a change to something existing, or documentation of something that already works?" — new → elicit forward from intent. Change → start from existing behaviour before the delta. Existing → use the distill skill instead.</q>
<q>"What is definitely out of scope?" — out-of-scope is as important as in-scope. Get both lists before proceeding.</q>
<q>"Are there related systems we should know about but not specify here?" — establishes boundaries and identifies related blueprints to reference.</q>
</questions>

Capture answers in context.md and scope.md.

<process name="elicitation">

Phases are numbered for reference, not prescription. Order can adapt. Verification checkpoints and contradiction checks are invariants; sequence is default.

<phase n="1" name="Context">
Goal: Understand why this exists before capturing what it does.

<questions>
<q>"What problem does this solve? Who has this problem today?"</q>
<q>"What happens if this doesn't get built?"</q>
<q>"Is there an existing workaround? What is broken about it?"</q>
<q>"Who asked for this — and what did they actually say they needed?"</q>
<q>"Is there a deadline? Fixed or flexible?"</q>
</questions>

<checkpoint>"Here's the context I've captured: [show paragraph]. Does this accurately describe the problem and why this exists?"</checkpoint>

Output: Write context.md — a new team member could read it to understand why this feature exists.

<watch-for>
<w>Features described as solutions ("we need a dashboard"). Redirect: "What decisions does someone currently make without enough information?"</w>
</watch-for>
</phase>

<phase n="2" name="Actors and roles">
Goal: Name every party who interacts with the system.

<questions>
<q>"Who uses this?"</q>
<q>"Are there different types of user? What distinguishes them?"</q>
<q>"Are there system actors — automated processes, external services?"</q>
<q>"What can each actor do that the others cannot?"</q>
<q>"Is there a guest or unauthenticated state?"</q>
</questions>

For each actor: name, who they are, what they can do, what they cannot do.

<checkpoint>"Here are the actors I've identified: [list]. Are any missing? Does any actor cover two different roles that should be split?"</checkpoint>

<watch-for>
<w>"Admin" covering both billing admin and user admin — different permissions, should be named separately.</w>
</watch-for>
</phase>

<phase n="3" name="Terminology">
Goal: Build the shared vocabulary before anything else.

<questions>
<q>"What are the main things this system manages — the nouns?"</q>
<q>"What do you call [thing]? Does engineering use the same word?"</q>
<q>"Is [term A] and [term B] the same thing, or different?"</q>
<q>"Are there terms that might mean something different to someone outside the team?"</q>
</questions>

For each term, write a precise one-sentence definition — what it means in this system.

<checkpoint>"Here are the terms I've defined: [show glossary]. Are the definitions accurate? Are there terms we use that aren't here?"</checkpoint>

Resolution rule: When two terms exist for the same concept, resolve now. Pick one. Define it. The other must not appear in the document.

<watch-for>
<w>Two words for the same concept ("booking" and "reservation")</w>
<w>One word meaning two different things to different stakeholders</w>
<w>Terms that only make sense to insiders</w>
</watch-for>
</phase>

<phase n="4" name="User stories">
Goal: Capture who needs what and why.
Format: As a [actor], I want to [action], so that [outcome].

<questions>
<q>"Walk me through this from the user's perspective, not the system's."</q>
<q>"What are they trying to accomplish? What does success look like for them?"</q>
<q>"Do we have evidence this is what users actually need, or is this our assumption?"</q>
</questions>

For each story, ask for evidence: analytics, support tickets, user research, observed behaviour. If absent, note as open question: "We believe users need X, but we have not validated this."

<checkpoint>"Here are the user stories: [show list]. Are any missing? Does any story assume a need we haven't validated?"</checkpoint>

<watch-for>
<w>Stories from the system's perspective ("the system processes"). Reframe: who is the actor, what is their goal?</w>
</watch-for>
</phase>

<phase n="5" name="Scenarios and flows">
Goal: Trace real end-to-end journeys, including error paths.

Happy path first:
<questions>
<q>"Walk me through [scenario] from start to finish."</q>
<q>"What triggers this? User action? Time passing? External event?"</q>
<q>"What is the first thing that happens?"</q>
<q>"Then what? And then?"</q>
<q>"What has changed when this is complete? What is the end state?"</q>
</questions>

Then probe every branch:
<questions>
<q>"You described [decision point]. What determines which path is taken?"</q>
<q>"Is that decision made by the user, the system, or an admin?"</q>
<q>"What if [step] fails or is unavailable?"</q>
<q>"What if the user waits too long? Are there timeouts?"</q>
<q>"What if this action is triggered twice?"</q>
</questions>

Contradiction check after tracing a flow: "Does anything conflict with what we said in actors or terminology?"
After multiple flows: "Do any flows make assumptions about the domain model we haven't captured?"

<checkpoint>"Here is the [scenario name] flow: [show it]. Does this match how it actually works? Steps missing? Branches wrong?"</checkpoint>

<watch-for>
<w>Flows that assume capabilities not yet in scope</w>
<w>Flows with no terminal state</w>
<w>Decision points with no stated owner</w>
<w>"And then it sends a notification" without specifying who, when, and through what channel</w>
</watch-for>
</phase>

<phase n="6" name="Domain model">
Goal: Name the entities, their states, and their relationships.

<questions>
<q>"What are the things this system creates, stores, and manages?"</q>
<q>"What states can [entity] be in? What does each state mean?"</q>
<q>"What triggers the transition from one state to another?"</q>
<q>"How is [entity A] related to [entity B]?"</q>
<q>"Who creates [entity]? Who can change it? Who can delete it?"</q>
<q>"What must always be true about [entity], regardless of state?"</q>
</questions>

Use the structured entity card format from the section guide (Section 7).

<checkpoint>"Here is the domain model: [show entities]. States right? Entities missing? Relationships wrong?"</checkpoint>

<watch-for>
<w>Boolean fields or nullable timestamps encoding implicit states. is_active + is_verified = four unnamed states. Name them.</w>
</watch-for>
</phase>

<phase n="7" name="Requirements and business rules">
Goal: Capture constraints — what the system must do and what it must prevent.

Functional requirements:
<questions>
<q>"What must always happen when [event]?"</q>
<q>"What must never be allowed?"</q>
<q>"Are there limits — maximums, minimums, quotas?"</q>
<q>"Are there time windows — deadlines, expirations, schedules?"</q>
</questions>

Business rules:
<questions>
<q>"Are there eligibility conditions?"</q>
<q>"Are there role restrictions?"</q>
<q>"Are there compliance requirements?"</q>
<q>"What are the exceptions — cases where the normal rule does not apply?"</q>
</questions>

For every rule: name its source. Source-less rules can be changed by anyone. If you cannot name the source, open a question.

Non-functional requirements: specific thresholds, not vague adjectives.
- Not "should be fast" → "p95 response under 2s at 1,000 concurrent users"
- Not "should be secure" → "must satisfy SOC 2 Type II access controls"
- Not "should be available" → "99.9% uptime, 8h RTO, 1h RPO"

<checkpoint>"Here are the requirements: [show list]. Any missing? Sources correct? Non-functional thresholds right?"</checkpoint>
</phase>

<phase n="8" name="Open questions and decisions">
At the end of every session:

Open questions — everything unresolved:
"We talked about [X] but were not sure. Let me capture that: [precise statement]. Who owns this? By when? What does it block?"

Decision log — everything decided:
"We decided [X]. The reason was [Y]. Let me record that."
Include: what was decided, why, who decided, what alternatives were considered.

Every open question must have an owner and a deadline.
</phase>

</process>

<principles>
<principle name="follow-the-data">When something is created, changed or sent, ask where it comes from, where it goes, who can see it. "You said the user receives a confirmation email. Where does the email address come from? What does it contain? What if the send fails?"</principle>
<principle name="work-through-implications">Every decision has downstream effects. Ask what each choice implies. "You said invitations expire after 7 days. What happens to the slots that were offered? What does the candidate see when they click an expired link?"</principle>
<principle name="name-ambiguity">Voice uncertainty: "I am not sure what happens here — let me note this as an open question rather than assume." Voiced ambiguity gets resolved; silent ambiguity becomes a bug.</principle>
<principle name="explicit-vocabulary">When a new term appears, pause and define it. "You said 'pipeline' — what do you mean by that in this context?" Add to Terminology immediately. If you catch yourself using two terms for the same concept, resolve it on the spot.</principle>
<principle name="existing-vs-intended">Ask: "Does the system do this today, or is this how you want it to work?" Both are useful but go in different places — existing behaviour is a starting point; intended behaviour is a requirement. Mixing them silently produces a spec that is half-true and half-aspirational.</principle>
</principles>

<traps>
<trap name="the-and-then-trap">Long chains without decision points. Probe every step with "always?" or "only if...?"</trap>
<trap name="the-obviously-trap">"Obviously" marks an unstated assumption. Probe: "Obviously the admin approves it — are there cases where approval is automatic? What if the admin is unavailable?"</trap>
<trap name="the-how-trap">Conversation drifts to implementation. Redirect: "At the behaviour level, what needs to happen and when?"</trap>
<trap name="the-one-user-trap">Scenarios from one actor's perspective miss multi-party interactions. "You described the buyer's journey. Walk me through the same flow from the seller's perspective."</trap>
<trap name="the-happy-path-only-trap">Only success scenarios. Probe each step: "What happens if this fails?"</trap>
<trap name="the-equivalent-terms-trap">Two terms for the same concept. Do not annotate as "also known as" — resolve it. Pick one, use everywhere.</trap>
<trap name="the-no-source-trap">A business rule nobody can explain the origin of. Do not include as fact. Open a question: "This rule exists in the current system. Do we know where it came from? Is it a legal requirement, a product decision, or something else?"</trap>
</traps>

<checklist name="session-closing">
<check>Verification checkpoint shown for every section captured this session</check>
<check>All contradictions surfaced and either resolved or logged as open questions</check>
<check>Every open question has an owner and a deadline</check>
<check>Every decision made this session is in the decision log with rationale</check>
<check>Changelog updated if meaningful changes were made</check>
<check>README.md manifest updated with current section statuses</check>
<check>Next session scope agreed</check>
</checklist>

<ref src="../../references/examples.md" name="Worked examples" load="lazy"/>
<ref src="../../references/section-guide.md" name="Section guide" load="lazy"/>
<ref src="../../references/diagram-guide.md" name="Diagram guide" load="lazy"/>

</skill>
