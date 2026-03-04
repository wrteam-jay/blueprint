---
name: distill
description: Use when a system already exists but is not documented — to capture how it actually works, build shared vocabulary around it, and produce a living spec that the team can reason about and discuss.
---

<skill name="distill">

<brief>Extract a blueprint from an existing system. The system may be partially documented, fully undocumented, or documented in ways that no longer match reality. Capture how things actually work — not how they were intended to work or how someone remembers they work. Code tells you what; tribal knowledge tells you why; a blueprint tells you both.</brief>

<constraints>
<c rule="Do not treat code as the spec">Code captures what the system does, including bugs and hacks. The blueprint captures what it should do.</c>
<c rule="No database column names or types">Use relationship names and domain concepts, not schema details.</c>
<c rule="No unresolved terminology conflicts">When you find different names in code vs product, pick one and flag the other for cleanup.</c>
<c rule="No 'this may be intentional'">If you do not know whether behaviour is intentional, open a question.</c>
<c rule="Do not spec dead code">If a code path is never reached in production, it does not belong in the blueprint.</c>
<c rule="Do not infer intent from implementation alone">Just because code does X does not mean X was intended. Validate with people.</c>
<c rule="No implementation in the blueprint">Rephrase at the behaviour level. See core discipline.</c>
<c rule="No complete spec from code alone">Distillation requires both code and people. Code reveals what; people reveal why.</c>
</constraints>

<questions name="before-you-start">
<q>"What part of the system are we documenting?" — full product, one feature, one service?</q>
<q>"What sources do we have?" — code, existing docs, people, Slack history, old tickets</q>
<q>"What is most uncertain or contested?" — start where the blueprint adds most value</q>
<q>"What should the blueprint be used for once it exists?" — onboarding, redesign, debugging?</q>
</questions>

<table name="abstraction-test">
The "would a stakeholder care?" test — for every detail found in code or conversation:

<row found="Invitation expires after 7 days" stakeholder-cares="yes" capture="yes — affects user experience"/>
<row found="Expiry enforced by cron job at midnight" stakeholder-cares="no" capture="no — mechanism"/>
<row found="Suspended accounts cannot reset password" stakeholder-cares="yes" capture="yes — policy"/>
<row found="Password reset uses HMAC-SHA256 tokens" stakeholder-cares="no" capture="no — implementation"/>
<row found="Order cancellable only before shipping" stakeholder-cares="yes" capture="yes — business rule"/>
<row found="Cancellation calls DELETE on orders service" stakeholder-cares="no" capture="no — implementation"/>
</table>

The "intentional or accidental?" test: designed behaviour → document as requirement. Accidental behaviour → document as open question: "The system currently does X. Was this intentional?"

<process name="distillation">

<step n="1" name="Map the territory">
Before capturing anything, understand the landscape.

From codebase: entry points (API routes, UI actions, webhooks, jobs, consumers), domain models (entities), core flows (services, handlers), external integrations.

From existing docs: product specs, API docs, runbooks, architecture diagrams, old tickets/PRs.

From people: "Walk me through [flow]", "What parts are you least confident about?", "What would a new team member need to know?", "What breaks most often?"

Produce a rough map before writing section files:

```
Entry points:
  - API: /api/orders/*, /api/payments/*
  - Webhooks: /webhooks/stripe, /webhooks/shipment-tracker
  - Jobs: expire_trials (nightly), send_digests (daily)

Key entities:
  - User, Subscription, Order, Payment, Invoice

Core flows:
  - Checkout, Subscription renewal, Order cancellation, Refund

External dependencies:
  - Stripe (payments), SendGrid (email), Shippo (shipping)
```
</step>

<step n="2" name="Extract terminology">
Establish vocabulary before documenting flows. Existing systems often have inconsistencies — codebase uses one name, product uses another, support uses a third.

Signals: classes/tables with different names than the product uses; same concept under multiple names; comments like "same as X".

Resolution: pick the business/product term. Document it; note code names needing cleanup.
</step>

<step n="3" name="Extract entities and states">
Find where data lives and what states it moves through.

In code, look for: enum fields and status columns, state machine libraries, boolean field combinations implying unnamed states, nullable timestamps encoding state.

Extract implicit states — the hardest part. Conditional logic checking field combinations is often an implicit state machine:

```python
# This code implies four states nobody named:
if user.is_active and user.verified_at is not None:
    # fully active
elif user.is_active and user.verified_at is None:
    # active but unverified
elif not user.is_active and user.deactivated_at is not None:
    # deactivated
else:
    # suspended (how did we get here?)
```

Surface the implicit state machine, give states names, flag: "Is this how this was intended to work?"
</step>

<step n="4" name="Extract flows">
Find where state changes happen and trace them.

Look for: status-changing functions, event handlers, webhook receivers, scheduled job bodies, API endpoint handlers (the action, not the endpoint).

For each flow trace: what triggers it, what preconditions must be true, what changes, what is communicated, what happens next.

The scattered logic problem: business logic often spread across multiple layers. Consolidate it:

```
API handler checks: user.is_active
Model method checks: subscription.status = active
Service checks: payment.status = confirmed

→ The actual preconditions for checkout are all three combined.
  Capture once in the blueprint; note that consolidation is needed in code.
```
</step>

<step n="5" name="Walk scenarios with people">
Code captures current behaviour including bugs. People carry intent. Walk key scenarios with someone who knows the system, then compare:

- "The code does X, but you described Y. Is one wrong?"
- "This flow has a case you didn't mention. Known edge case?"
- "The code does X here but I couldn't find a reason. Do you know why?"
</step>

<step n="6" name="Identify gaps and questions">
Distillation reveals:

- Undocumented decisions — things nobody can explain
- Undocumented requirements — behaviour never stated as a requirement
- Missing error handling — happy paths with no failure behaviour
- Stale documentation — docs that no longer match the system
- Behavioural debt — system does something two different ways for historical reasons
</step>

</process>

Output: blueprint directory — one file per section. Step 2 → terminology.md, Step 3 → domain-model.md, Step 4 → scenarios/, Step 5 → scenario updates + questions.md, Step 6 → questions.md + decisions.md. Update README.md and changelog.md at the end.

<checklist name="abstraction-check">
<check>No database column types or query syntax</check>
<check>No API endpoint paths or HTTP methods</check>
<check>No framework-specific concepts</check>
<check>No specific library names (unless the integration itself is a domain concern)</check>
<check>Foreign keys replaced with named relationships</check>
<check>Technical status values replaced with meaningful names</check>
<check>Implementation field names replaced with business names</check>
</checklist>

<checklist name="terminology-consistency">
<check>Each concept has exactly one name throughout the blueprint</check>
<check>No "also known as" or "equivalent to" notes (resolve, don't annotate)</check>
<check>Terminology matches what the product and business actually use</check>
<check>Code names that differ from blueprint terms are flagged for cleanup</check>
</checklist>

<watch-for>
<w>The behaviour nobody owns — logic nobody can explain. Document as-is, flag as open question.</w>
<w>The workaround that became permanent — "temporary" code that is now core. Document actual behaviour; note history.</w>
<w>The feature no one uses — code paths never triggered in production. Question whether these belong.</w>
<w>The inconsistent state machine — same state reachable via two paths with different outcomes. Document both; flag if intentional.</w>
</watch-for>

<ref src="../../references/section-guide.md" name="Section guide" load="lazy"/>
<ref src="../../references/diagram-guide.md" name="Diagram guide" load="lazy"/>

</skill>
