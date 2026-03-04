<ref-guide name="worked-examples">

<brief>Before-and-after examples for every major section type. Examples outperform descriptions — when in doubt, match these patterns.</brief>

<example n="1" name="Context">
<bad>
This feature provides users with the ability to manage their account settings
through a React-based settings panel backed by a REST API. It uses Redux for
state management and connects to the user_preferences table in PostgreSQL.
</bad>
<why-bad>Names implementation (React, REST, Redux, PostgreSQL). Describes how, not why. No problem statement or history.</why-bad>
<good>
Account management was previously handled through support tickets. Support spent
~30% of their time on self-serviceable requests — password changes, notification
preferences, billing details. Average resolution: 24-48 hours for changes that
take seconds directly.

This feature gives users direct control, removing the support bottleneck.
Prioritised after Q3 2024 analysis showed self-serviceable requests were the
largest ticket category.
</good>
</example>

<example n="2" name="Scope">
<bad>This blueprint covers the order system.</bad>
<why-bad>"The order system" is undefined. No out-of-scope list. No related blueprints. No exclusion reasons.</why-bad>
<good>
### In scope
- Order placement: from cart confirmation to order creation
- Payment collection: card charge, failure handling, retry logic
- Order confirmation: email to customer, inventory reservation

### Out of scope
- Shipping and fulfilment — covered in the Fulfilment blueprint
- Refunds and disputes — separate flow, planned for Q3
- Subscription orders — different lifecycle; out of scope for this version

### Related blueprints
- Inventory — consumes inventory availability
- Customer — Order belongs to a Customer; lifecycle defined there
- Notification — sends confirmation emails; templates defined there
</good>
</example>

<example n="3" name="Actors & Roles">
<bad>
- Admin
- User
- System
</bad>
<why-bad>Generic labels. No descriptions, capabilities, or restrictions. "Admin" likely covers multiple permission sets.</why-bad>
<good>
**Customer** — registered user who places and manages orders. Can place orders,
view history, cancel before shipping, request returns. Cannot see other customers'
orders.

**Fulfilment Staff** — internal user who processes and ships. Can update order
status, mark items unavailable, trigger refunds. Cannot place orders or access
payments.

**Billing Admin** — manages payment issues and refund approvals. Can view payment
details, approve refunds over threshold, override payment failures. Cannot modify
orders or fulfilment.

**System (Order Processor)** — automated. Validates payment, reserves inventory,
sends confirmation on order creation. Not directly controllable by users.
</good>
</example>

<example n="4" name="Scenario">
<bad>
### User Login

The user enters their credentials. The system validates them and logs the user in.
The user is redirected to their dashboard.
</bad>
<why-bad>No named actor. No trigger. No decision points. "The system validates" is mechanism. No failure paths. No end state.</why-bad>
<good>
### Login

**Actor:** Visitor (unauthenticated)
**Trigger:** Visitor submits email and password

**Flow:**
1. Visitor submits email and password.
2. System checks whether account exists and password matches.
   - If no match → generic "incorrect email or password" (prevents enumeration).
     Failed counter increments.
   - If lockout threshold reached → account moves to *locked*.
     See: Account Lockout scenario.
   - If account *locked* → "account locked" with unlock instructions.
3. If valid and account *active*: new Session created, counter resets, visitor
   taken to original page or home.
4. If valid but *unverified* → redirected to email verification. No session created.

**End state:** Session exists and visitor is authenticated — or attempt rejected
with actionable reason.
</good>
</example>

<example n="5" name="Requirement">
<bad>
FR-005: The system should handle payments securely and efficiently.
</bad>
<why-bad>"Should" signals optionality. "Securely" and "efficiently" undefined. No acceptance criteria. No rationale.</why-bad>
<good>
**FR-005** [Must Have]

*Statement:* Payment card data must not pass through or be stored on company
servers at any point during checkout.

*Rationale:* PCI DSS compliance — storing card data requires full PCI audit.
Tokenisation keeps system out of scope.

*Source:* Legal/Security policy — Decision D-007.

*Acceptance criteria:*
- All card entry via payment processor's hosted fields/SDK
- Card numbers, CVVs, expiry dates never in logs, errors or API responses
- PCI self-assessment confirms reduced scope
</good>
</example>

<example n="6" name="Terminology entry">
<bad>
**Order** — An order is when a customer orders something. Also called a "purchase"
in checkout and a "transaction" by finance.
</bad>
<why-bad>Circular definition. Three unresolved names. Conflates Order, Purchase and Transaction.</why-bad>
<good>
**Order** — The record of a customer's intent to purchase. Created when customer
confirms cart. Persists through fulfilment regardless of payment outcome. Lifecycle:
*pending* through *delivered*, *cancelled* or *returned*.

*Distinct from:*
- **Transaction** — financial record of a single payment attempt. An Order may
  have multiple.
- **Fulfilment** — physical preparation and shipment. At most one per Order,
  created at *processing*.

*Code note:* Checkout module uses "purchase" for Order. Known inconsistency flagged
for cleanup. Blueprint term: **Order** everywhere. (See Decision D-003.)
</good>
</example>

<example n="7" name="Domain model entity">
<bad>
**User** — id: integer, email: varchar, name: varchar, password_hash: varchar,
is_active: boolean, is_verified: boolean, created_at: timestamp, deleted_at: timestamp
</bad>
<why-bad>Database schema, not domain model. No states (is_active + is_verified = 4 unnamed states). No lifecycle, relationships, or invariants.</why-bad>
<good>
**Entity: User**

*Definition:* A person who has registered. Can place orders and manage their own data.

*States:*
- **unverified** — registered, email not confirmed
- **active** — verified, in good standing
- **suspended** — access restricted (payment failure or policy violation)
- **deleted** — soft-deleted, retained 7 years per legal requirement

*Transitions:*
- unverified → active: email confirmed
- active → suspended: unrecoverable payment failure or admin action
- suspended → active: payment resolved or admin reinstates
- active | suspended → deleted: user request or admin action

*Invariants:* Deleted cannot be reactivated. Email unique across non-deleted users.

*Relationships:* Places Orders (0+). Has Sessions (0+). Has one Payment Method
(optional).

*Lifecycle owner:* Created by registration. Transitions by payment webhooks, email
verification, admin tools.
</good>
</example>

<example n="8" name="User story">
<bad>
US-003: As a user, I want notifications.
</bad>
<why-bad>"User" not specific. "Notifications" is solution, not need. No outcome. Not testable.</why-bad>
<good>
**US-003** [Must Have]

As a **customer who has placed an order**, I want to be notified when my order
ships with a tracking reference, so that I can track delivery without contacting
support.

*Evidence:* "Where is my order?" = 34% of support volume (Zendesk Q3 2024).
61% of churned post-purchase users cited lack of shipping updates. 6 interviews
confirmed shipping notification expected within minutes.

*Acceptance criteria:*
- Notification within 5 minutes of *shipped* status
- Includes order number, carrier, tracking link
- Tracking link valid and current when opened
- Sent to email on the order (not necessarily current account email)
</good>
</example>

<example n="9" name="Elicitation conversation">
<bad>
User: We need a user authentication system.
Model: I'll spec that out. [generates 400 words from a single sentence]
</bad>
<why-bad>Made up session duration, password requirements, auth method. No scope, actors, or open questions. Treated all gaps as decisions.</why-bad>
<good>
User: We need a user authentication system.
Model: Let's capture this properly. What problem are we solving? New system or changing existing?

User: New system, starting from scratch.
Model: Who are the users — internal staff, customers, or both?

User: Customers (B2C) and internal admins.
Model: Do they authenticate the same way?

User: Customers use email/password or Google. Admins use company SSO.
Model: Let me check what I have:
*Actors: Customer (email/password or Google), Admin (SSO). Scope: new auth system.* Match?

User: Yes.
Model: Great. What happens to a customer's session — timeout, or stay logged in?

Demonstrates: one question at a time, asks before assuming, verification checkpoint, scope and actors before requirements.
</good>
</example>

<example n="10" name="Contradiction surfaced">
User: Users can cancel their subscription at any time.
[later]
User: We need to honour the 30-day notice period in our terms.
Model: I want to flag a conflict. "Cancel at any time" vs "30-day notice" cannot both be true.
Options: immediate cancel with billing remainder, 30-day effective date, trial exceptions.

Logging as OQ-004: When a user cancels, immediate or 30-day? Billing treatment?
Owner: [assign] | Blocking: BR-002, FR-011
</example>

<example n="11" name="Handling 'I don't know'">
<bad>
User: I'm not sure what happens when the payment fails.
Model: Typically the system retries 3 times with exponential backoff, then suspends.
</bad>
<why-bad>Invented retry count, backoff, and notification. Filled gap with fiction.</why-bad>
<good>
User: I'm not sure what happens when the payment fails.
Model: Let me note that as an open question:

OQ-007: Payment failure policy — retry count and period? Subscription status?
Who notified, how, when? Grace period?
Owner: [Product/Finance] | Blocking: Scenarios 6, 7; FR-019, BR-005

We can continue and come back to this.
</good>
</example>

</ref-guide>
