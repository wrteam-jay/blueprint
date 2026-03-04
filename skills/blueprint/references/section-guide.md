<ref-guide name="section-guide">

<brief>What each section of a blueprint must contain, what it must not, and common mistakes.</brief>

<template name="header-block">
# Blueprint: [Name]

**Status:** Draft | Active | Deprecated
**Version:** 1.0
**Last updated:** [date]
**Spec owner:** [name — one person, not a team]
**Related blueprints:** [links, with one-phrase description]

---

## Sections

| # | Section | File | Status |
|---|---------|------|--------|
| 1 | Context | [context.md](./context.md) | Complete |
| 2 | Scope | [scope.md](./scope.md) | Complete |
| 3 | Actors & Roles | [actors.md](./actors.md) | Complete |
| 4 | Terminology | [terminology.md](./terminology.md) | Complete |
| 5 | User Stories | [stories.md](./stories.md) | Draft |
| 6 | Scenarios & Flows | [scenarios/](./scenarios/_index.md) | Draft |
| 7 | Domain Model | [domain-model.md](./domain-model.md) | Draft |
| 8 | Requirements | [requirements.md](./requirements.md) | Pending |
| 9 | Decision Log | [decisions.md](./decisions.md) | Active |
| 10 | Open Questions | [questions.md](./questions.md) | Active |
| 11 | Changelog | [changelog.md](./changelog.md) | Active |

## Completion tier

**Current: [Tier]** — [brief description]
</template>

Status: Draft (WIP), Active (authoritative), Deprecated (no longer reflects reality).
Version: increment on meaningful change (new scenarios, revised domain model, resolved terminology); not on typos.
Section status: Pending (not started), Draft (in progress), Complete (captured and verified), Active (always evolving — decisions, questions).

<section n="1" name="Context">
Purpose: why this system exists. The problem it solves. The decision to build it.

Must contain: the problem (from who has it), why it matters, how it came to exist, relevant history.
Must not contain: how it is built, requirements (Section 8), detailed flows (Section 6).

<example>
<bad>This feature provides users with the ability to manage their account settings through a React-based settings panel backed by a REST API.</bad>
<why-bad>Names implementation (React, REST API). Describes how, not why. No problem statement.</why-bad>
<good>Account management was previously handled through support tickets. Support was spending ~30% of time on self-serviceable requests. This feature gives users direct control, removing the support bottleneck and 24-48h resolution delay.</good>
</example>
</section>

<section n="2" name="Scope">
Purpose: clear boundaries so the document does not silently include uncaptured things.

Three required lists:

```markdown
### In scope
- Order placement: from cart confirmation to order creation
- Payment collection: card charge, failure handling, retry logic

### Out of scope
- Shipping and fulfilment — covered in the Fulfilment blueprint
- Refunds and disputes — separate flow, planned for Q3

### Related blueprints
- [Inventory blueprint] — this blueprint consumes inventory availability
- [Customer blueprint] — Order belongs to a Customer; Customer lifecycle is there
```

Every out-of-scope item prevents future confusion.
</section>

<section n="3" name="Actors & Roles">
Purpose: name every interacting party and what distinguishes them.

Each entry: name (business term), one-sentence description, capabilities, restrictions (if the restriction matters).

```markdown
**Customer**
A registered user who places and manages orders. Can place orders, view their
order history, cancel orders before they ship. Cannot see other customers' orders.

**System (Order Processor)**
An automated actor. Runs on order creation: validates payment, reserves
inventory, sends confirmation. Not directly controllable by users.
```

<watch-for>
<w>"Admin" covering different permission sets — billing admin vs user admin should be named separately.</w>
</watch-for>
</section>

<section n="4" name="Terminology">
Purpose: shared vocabulary so precise that any team member uses the same word to mean the same thing. Terminology conflicts cause more bugs than missing requirements.

Each term: one-sentence definition (what it is in this system), what it is distinct from, scope.

```markdown
**Order**
The record of a customer's intent to purchase. Created when the customer
confirms their cart. Distinct from a *Transaction*, which is the financial
record of a payment attempt.

**Transaction**
The financial record of one payment attempt against an Order. An Order may
accumulate multiple Transactions. A Transaction is immutable once created.
```

Good definitions: one sentence saying what the thing is, what it is distinct from, scope.
Bad definitions: circular, vague, absent.

Resolution rule: two terms for same concept → pick one, define it, do not include the other even as "see also".
</section>

<section n="5" name="User Stories">
Purpose: who needs what and why, before describing how.
Format: As a [actor], I want to [action], so that [outcome].

Each story: independent, testable, valuable. Group by actor or flow.

```markdown
**US-001** [Must Have]
As a customer, I want to see all my past orders in one place, so that I can
track what I've purchased and refer back to past purchases.
*Evidence:* "Where is my order?" is 34% of support ticket volume (Zendesk Q3 2024).
*Acceptance criteria:* Customer can view the last 24 months of orders without
contacting support.
```

Evidence annotation required for every story:
- Analytics: "accounts for X% of support tickets"
- User research: "validated in N interviews on [date]"
- Observed behaviour: "current system logs show..."
- Explicit: "assumption: not yet validated" — honest and useful

Bad stories: no "so that" clause, system's perspective, feature as need, no evidence, untestable acceptance criteria.
</section>

<section n="6" name="Scenarios & Flows">
Purpose: trace real end-to-end journeys. Most valuable section — where the blueprint becomes concrete.

Each scenario: name (what happens, not who), actors, trigger, step-by-step flow, end state, diagram where branching warrants one.

```markdown
### Order Placement

**Actors:** Customer, System (Order Processor)
**Trigger:** Customer confirms cart

**Flow:**
1. Customer reviews cart and confirms.
2. System validates payment method on file.
   - If no valid payment method → customer is prompted to add one.
3. System creates an Order in *pending* status.
4. System attempts to charge the payment method.
   - If payment fails → Order moves to *payment_failed*. Customer is notified.
5. System reserves inventory for each line item.
6. Order moves to *confirmed* status.
7. Customer receives order confirmation email.

**End state:** Order is in *confirmed* status. Inventory is reserved.
```

File per scenario in scenarios/ directory. _index.md lists all with one-line summary.
Diagrams after prose, not instead of it. See <ref src="./diagram-guide.md" load="lazy"/>.
Error/edge case scenarios accompany every happy path: payment failure, timeout, concurrent modification, external dependency down, invalid state transition.
</section>

<section n="7" name="Domain Model">
Purpose: entities, their states, relationships and lifecycle.

Entity card format:

```markdown
**Entity: Order**

*Definition:* The record of a customer's intent to purchase. Created when the
customer confirms their cart.

*States:*
- **pending** — created, payment not yet attempted
- **confirmed** — payment successful, inventory reserved
- **processing** — fulfilment staff has picked up the order
- **shipped** — dispatched; tracking reference exists
- **cancelled** — abandoned before processing, or cancelled by staff

*Transitions:*
- pending → confirmed: payment succeeds and inventory reserves
- pending → cancelled: customer cancels or payment fails permanently
- confirmed → processing: fulfilment staff accepts the order

*Invariants:*
- A cancelled order cannot be reactivated
- An order must have at least one LineItem

*Relationships:*
- Belongs to one Customer
- Contains one or more LineItems
- Has at most one Fulfilment
- Accumulates Transactions as payment is attempted (0 or more)

*Lifecycle owner:* Created by checkout flow. Status transitions by Order Processor
(automated), Fulfilment Staff (manual), or Customer (within allowed states).
```

Why this format:
- Definition — one sentence, unique identification
- States — named and described, not just listed
- Transitions — explicit trigger for each edge; without a trigger nobody knows what causes it
- Invariants — constraints that must hold regardless of state
- Relationships — named and directional with cardinality; not "Order has Transactions" but "Order accumulates Transactions as payment is attempted"
- Lifecycle owner — who is responsible for each class of transition; ambiguous ownership causes double-writes and race conditions

State diagrams for entities with >2 states. See <ref src="./diagram-guide.md" load="lazy"/>.
</section>

<section n="8" name="Requirements">
8.1 Functional requirements:

```markdown
**FR-001** [Must]
Statement: A customer must receive an order confirmation within 5 minutes of
           placing a successful order.
Acceptance criteria:
  - Confirmation email sent within 5 minutes of Order reaching confirmed status
  - Email contains order number, line items, total, estimated delivery window
```

8.2 Business Rules:

```markdown
**BR-001**
Rule: An order cannot be cancelled after it reaches *processing* status.
Source: Fulfilment operations — once packing begins, reversal is not physically possible.
Exception: Fulfilment staff may override using admin cancellation flow.
```

Every rule needs a source. The source determines whether the rule can be changed and by whom.

8.3 Non-Functional requirements:

```markdown
**NFR-001** [Must]
The order placement flow must complete within 8 seconds (p95) at 1,000 concurrent users.
Rationale: Checkout abandonment increases significantly beyond 8 seconds.
```

Specific thresholds, not vague adjectives.
</section>

<section n="9" name="Decision Log">
Purpose: record settled decisions so they are not re-debated. Include rationale, not just outcome.

```markdown
**D-001** — 2024-11-12
Decision: Soft delete orders rather than hard delete.
Rationale: Legal requirement to retain transaction records for 7 years. Hard delete
would cascade to Transactions, violating retention policy.
Decided by: Engineering + Legal.
```

A decision without rationale is the same as no decision — the next person who questions it cannot evaluate whether the reasoning still applies.
</section>

<section n="10" name="Open Questions">
Purpose: live discussion space. Unresolved questions prevent the spec from being authoritative.

```markdown
**OQ-001**
Question: Should order cancellation generate a refund automatically, or require
          manual finance approval for amounts over a threshold?
Owner: [Product Manager name]
Blocking: FR-008, BR-004
Deadline: [date]
```

Open questions without owners do not get resolved. Open questions without "blocking" annotations do not get prioritised.
</section>

<section n="11" name="Changelog">
Purpose: track how the document evolved.

```markdown
| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2024-11-12 | Initial draft from elicitation sessions | [name] |
| 1.1 | 2024-11-20 | Added Payment Failure scenario; resolved OQ-001 | [name] |
```

See <ref src="./maintenance.md" section="delta-protocol" load="lazy"/> for version bump rules and entry format.
</section>

<section name="cross-blueprint-references">
A blueprint owns an entity if it governs its lifecycle. It references an entity if it reads from it.

Do not re-define entities owned by another blueprint — reference with a link.

In terminology.md:

```markdown
**Customer**
Defined in the [Customers blueprint](../customers.blueprint/README.md). For the purposes
of this blueprint: a registered account that places orders. The Orders blueprint
reads Customer.email and Customer.name; it does not modify Customer records.
```

In domain-model.md:

```markdown
*Relationships:* Belongs to one **Customer** ([Customers blueprint](../customers.blueprint/README.md)).
```

Shared terminology: define once in the authoritative blueprint, reference elsewhere. Never copy-paste — it will drift.

<table name="relationship-types">
<row type="Owns" meaning="Governs entity lifecycle" expression="Fully defined in Domain Model"/>
<row type="References" meaning="Reads from entity" expression="Short Terminology entry with link"/>
<row type="Triggers" meaning="Event from another blueprint causes behaviour" expression="Scenario trigger cites source"/>
<row type="Emits" meaning="Produces events another blueprint responds to" expression="Note in scenario end state"/>
</table>

Cross-blueprint event dependencies: name the source blueprint and scenario explicitly so the dependency is auditable.
</section>

</ref-guide>
