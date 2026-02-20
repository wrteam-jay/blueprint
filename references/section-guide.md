# Section Guide

What each section of a blueprint must contain, what it must not contain, and common mistakes.

---

## Header block

Every blueprint opens with a metadata block:

```markdown
# Blueprint: [Name]

**Status:** Draft | Active | Deprecated
**Version:** 1.0
**Last updated:** [date]
**Owners:** [name / team]
**Related:** [links to related blueprints]
```

**Status** signals how trustworthy the document is. Draft = work in progress. Active = the team treats this as authoritative. Deprecated = the system has changed; this no longer reflects reality.

**Version** increments when the document changes in a meaningful way. Patch changes (typos, clarifications) do not need a version bump. Structural changes (new scenarios, revised domain model, resolved terminology conflicts) do.

---

## 1. Context

**Purpose:** Why this system or feature exists. The problem it solves. The decision to build it.

**Must contain:**
- The problem, stated from the perspective of who has it
- Why it matters (the business or user consequence of not having it)
- How this came to exist (customer request, internal pain, strategic decision, regulatory requirement)
- Any relevant history (what came before this, what it replaced)

**Must not contain:**
- How the system is built
- Requirements (those belong in Section 8)
- Detailed flows (those belong in Section 6)

**Antipattern:**
```
Bad: "This feature provides users with the ability to manage their account settings
     through a React-based settings panel backed by a REST API."

Good: "Account management was previously handled exclusively through support tickets.
      Support was spending approximately 30% of their time on requests that users
      could self-serve — password changes, notification preferences, billing details.
      This feature gives users direct control over these settings, removing the
      support bottleneck and the 24-48 hour resolution delay."
```

---

## 2. Scope

**Purpose:** Establish clear boundaries so the document does not silently include things it has not captured.

**Three lists, all required:**

### In scope
What this blueprint covers. Be specific.

```markdown
- Order placement: from cart confirmation to order creation
- Payment collection: card charge, failure handling, retry logic
- Order confirmation: email to customer, inventory reservation
```

### Out of scope
What this blueprint deliberately does not cover, with a reason for each.

```markdown
- Shipping and fulfilment — covered in the Fulfilment blueprint
- Refunds and disputes — separate flow, separate blueprint, planned for Q3
- Subscription orders — different lifecycle; out of scope for this version
```

Every item in the out-of-scope list prevents future confusion. "Is returns in this document?" "No — it's out of scope, see [link]."

### Related blueprints
Adjacent systems this one touches or depends on.

```markdown
- [Inventory blueprint] — this blueprint consumes inventory availability
- [Customer blueprint] — Order belongs to a Customer; Customer lifecycle is there
- [Notification blueprint] — sends confirmation emails; templates defined there
```

---

## 3. Actors & Roles

**Purpose:** Name every party who interacts with the system and describe what distinguishes them.

Each actor entry:
- Name (use what the business actually calls them, not the code name)
- One-sentence description of who they are
- What they can do (capabilities)
- What they cannot do (restrictions), if the restriction matters to understanding the system

```markdown
**Customer**
A registered user who places and manages orders. Can place orders, view their
order history, cancel orders before they ship, and request returns. Cannot see
other customers' orders.

**Fulfilment Staff**
An internal user who processes and ships orders. Can update order status, mark
items as unavailable, and trigger refunds. Cannot place orders or access
payment details.

**System (Order Processor)**
An automated actor. Runs on order creation: validates payment, reserves
inventory, sends confirmation. Triggered by order placement; not directly
controllable by users.
```

**Watch for:** A single actor name covering two different permission sets. "Admin" is often both a billing admin and a user admin — different permissions, should be named separately. Probe when an actor seems to have unrelated capabilities.

---

## 4. Terminology

**Purpose:** The shared vocabulary. Definitions so precise that any team member uses the same word to mean the same thing.

This section pays for itself. Terminology conflicts cause more bugs than missing requirements. When engineering calls it a "job" and product calls it a "task" and support calls it a "ticket", three different things end up in production.

**Format per term:**

```markdown
**Order**
The record of a customer's intent to purchase. Created when the customer
confirms their cart. Persists through fulfilment. Distinct from a *Transaction*,
which is the financial record of a payment attempt.

**Transaction**
The financial record of one payment attempt against an Order. An Order may
accumulate multiple Transactions (e.g., one declined, one successful). A
Transaction is immutable once created.

**Fulfilment**
The process of preparing and shipping an Order. An Order has exactly one
Fulfilment. Fulfilment begins when the Order reaches *processing* status.
```

**What makes a good definition:**
- One sentence that says what the thing is
- What it is distinct from (the most common source of confusion)
- Scope: where does this term apply?

**What makes a bad definition:**
- Circular ("An order is what a customer orders")
- Vague ("An order represents a purchase intent in the system")
- Absent (the term is used in Scenarios but not defined here)

**Resolution rule:** When two terms exist for the same concept, this section resolves it. Pick one. Define it. Do not include the other term even as a "see also" — it will reappear in the codebase and in conversation.

---

## 5. User Stories

**Purpose:** Capture who needs what and why, before describing how the system delivers it.

Stories frame every downstream design decision. They are not tasks. A story without an outcome is incomplete.

**Format:** As a [actor], I want to [action], so that [outcome].

Group stories by actor or by flow. Each story should be:
- Independent (can be understood without reading other stories)
- Testable (there is a demonstrable state of the system that satisfies it)
- Valuable (the outcome matters to the actor)

```markdown
### Customer stories

**US-001** As a customer, I want to see all my past orders in one place, so that
I can track what I've purchased and refer back to past purchases.

**US-002** As a customer, I want to cancel an order I placed by mistake, so that
I am not charged for something I do not want.

**US-003** As a customer, I want to know immediately if my payment fails, so that
I can resolve the issue without losing my order.

### Fulfilment staff stories

**US-010** As a fulfilment staff member, I want to see all orders in *processing*
status, so that I can pick and pack in priority order.
```

**What makes a bad story:**
- No "so that" clause ("As a customer, I want to see my orders")
- Written from the system's perspective ("The system allows customers to...")
- Written as a feature ("As a customer, I want a dashboard")
- Acceptance criteria so vague they cannot be tested

---

## 6. Scenarios & Flows

**Purpose:** Trace real end-to-end journeys through the system. This is where the blueprint becomes concrete.

Scenarios are the most valuable section. Requirements without scenarios are abstract; scenarios without requirements miss constraints. Together they form a complete picture.

### Structure

Each scenario:
- A name that describes what happens (not who does it)
- The actor(s) involved
- The trigger (what starts the scenario)
- The step-by-step flow
- The end state (what is true when the scenario is complete)
- A diagram where the flow has branching or is complex enough to warrant one

```markdown
### Order Placement

**Actors:** Customer, System (Order Processor)
**Trigger:** Customer confirms cart

**Flow:**
1. Customer reviews cart and confirms.
2. System validates payment method on file.
   - If no valid payment method → customer is prompted to add one. Scenario pauses.
3. System creates an Order in *pending* status.
4. System attempts to charge the payment method.
   - If payment fails → Order moves to *payment_failed*. Customer is notified.
     See: [Payment Failure scenario].
5. System reserves inventory for each line item.
   - If any item is unavailable → Order moves to *on_hold*. Customer and
     Fulfilment are notified. See: [Inventory Unavailability scenario].
6. Order moves to *confirmed* status.
7. Customer receives order confirmation email.

**End state:** Order is in *confirmed* status. Inventory is reserved.
              Customer has received confirmation.
```

### Diagrams

Use Mermaid diagrams where a flow has branching, multiple actors, or is long enough that prose is hard to follow at a glance. See the [diagram guide](./diagram-guide.md) for patterns.

Place the diagram after the prose description, not instead of it. Prose is searchable and readable in any context; diagrams compress complex flows.

### Error and edge case scenarios

Every happy path scenario should be accompanied by its primary failure scenarios. These are not afterthoughts — they often contain the most important design decisions.

Common categories to cover:
- Payment failure
- Timeout (user does not complete an action within a time window)
- Concurrent modification (two actors act on the same entity simultaneously)
- External dependency unavailable (third-party service is down)
- Invalid state transition (user attempts an action that is not permitted in the current state)

---

## 7. Domain Model

**Purpose:** Name the entities the system manages and describe their states, relationships and lifecycle.

### Entities

Each entity entry:
- Name and one-sentence definition
- States (if it has a lifecycle)
- Key fields (at the business level — not database columns, but what data the entity carries that matters to understanding the system)
- Relationships (who owns it, what it belongs to, what it contains)
- Lifecycle owner (who creates it, who can update it, who can delete it)

```markdown
**Order**
The record of a customer's purchase intent, from confirmation to fulfilment.

*States:* pending → confirmed → processing → shipped → delivered | cancelled | returned

*Key data:* Line items (products and quantities), delivery address, payment method,
total amount, placed timestamp.

*Relationships:* Belongs to one Customer. Contains one or more LineItems.
Has one Fulfilment (created when processing begins). May have multiple
Transactions.

*Lifecycle:* Created by the customer at checkout. Updated by the Order Processor
(status), Fulfilment Staff (status, tracking). Cancelled by the Customer
(before processing) or Fulfilment Staff (if items unavailable).
```

### State diagrams

For any entity with more than two states, include a state diagram. See the [diagram guide](./diagram-guide.md).

### Relationships

Capture how entities connect to each other:

```markdown
- Customer → Order: one Customer places many Orders
- Order → LineItem: one Order contains one or more LineItems
- Order → Transaction: one Order may have multiple Transactions
- Order → Fulfilment: one Order has at most one Fulfilment
```

Relationship names matter. Not "Order has Transactions" but "Order accumulates Transactions as payment is attempted."

---

## 8. Requirements

### 8.1 Functional Requirements

**Each requirement:**
- Unique ID (FR-001...)
- Priority: Must / Should / Could (MoSCoW — Must means the product fails without it)
- A statement of what must be true
- Acceptance criteria: what must be demonstrably true for this to be accepted

```markdown
**FR-001** [Must]
Statement: A customer must receive an order confirmation within 5 minutes of
           placing a successful order.
Acceptance criteria:
  - Confirmation email is sent within 5 minutes of Order reaching confirmed status
  - Email contains order number, line items, total, and estimated delivery window
  - Email is sent to the address on the customer's account at the time of order
```

### 8.2 Business Rules

Constraints the system must enforce.

```markdown
**BR-001**
Rule: An order cannot be cancelled after it reaches *processing* status.
Source: Fulfilment operations — once packing begins, reversal is not physically possible.
Exception: Fulfilment staff may override this using an admin cancellation flow.

**BR-002**
Rule: A customer may not have more than 10 pending orders simultaneously.
Source: Fraud prevention policy (Risk team, 2024-03).
Exception: None.
```

Every rule needs a source. The source determines whether the rule can be changed and by whom.

### 8.3 Non-Functional Requirements

```markdown
**NFR-001** [Must]
The order placement flow must complete within 8 seconds (from cart confirmation
to confirmation email sent) at the 95th percentile under a load of 1,000
concurrent users.
Rationale: Checkout abandonment increases significantly beyond 8 seconds per
internal analytics data.

**NFR-002** [Must]
Payment data must never be stored on our servers. All card details are
tokenised by the payment processor before reaching our system.
Rationale: PCI DSS compliance — storing card data would require full PCI audit.
```

---

## 9. Decision Log

**Purpose:** Record settled decisions so they are not re-debated. Include the rationale, not just the outcome.

```markdown
**D-001** — 2024-11-12
Decision: Soft delete orders rather than hard delete.
Rationale: Legal requirement to retain transaction records for 7 years. Hard
delete would cascade to Transactions, violating retention policy. Soft delete
keeps the record while hiding it from customer-facing views.
Decided by: Engineering + Legal.

**D-002** — 2024-11-19
Decision: Order cancellation is not permitted after processing begins.
Rationale: Fulfilment physically cannot reverse packing once started. Admin
override path exists for exceptional cases.
Decided by: Product + Fulfilment Operations.
```

A decision without rationale is the same as no decision — the next person who questions it cannot evaluate whether the reasoning still applies.

---

## 10. Open Questions

**Purpose:** Live discussion space. Unresolved questions get in the way of the spec being treated as authoritative.

```markdown
**OQ-001**
Question: Should order cancellation generate a refund automatically, or require
          manual finance approval for amounts over a threshold?
Owner: [Product Manager name]
Blocking: FR-008, BR-004
Deadline: [date]

**OQ-002**
Question: The code currently sends a second confirmation email if the payment
          processor webhook arrives more than 30 seconds after the initial charge.
          Was this intentional? Is it correct?
Owner: [Engineering lead]
Blocking: Nothing currently, but it will be codified in this blueprint once resolved.
```

Open questions without owners do not get resolved. Open questions without "blocking" annotations do not get prioritised.

---

## 11. Changelog

**Purpose:** Track how the document has evolved, so readers know whether the version they read last month is still current.

```markdown
| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2024-11-12 | Initial draft from elicitation sessions | [name] |
| 1.1 | 2024-11-20 | Added Payment Failure scenario; resolved OQ-001 | [name] |
| 1.2 | 2024-12-03 | Updated Domain Model after codebase distillation; flagged OQ-002 | [name] |
```
