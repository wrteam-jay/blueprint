# Worked Examples

Before-and-after examples for every major section type. For smaller models especially: examples outperform descriptions. When in doubt about what "good" looks like, match these patterns.

---

## Example 1: Scenario

### Bad

```markdown
### User Login

The user enters their credentials. The system validates them and logs the user in.
The user is redirected to their dashboard.
```

**Why it fails:**
- No named actor — "the user" is not an actor declaration
- No trigger — what starts this? A button click? An API call? A redirect?
- No decision points — real login has multiple branches
- "The system validates" describes a mechanism, not a behaviour
- No failure paths — what happens with a wrong password? A locked account?
- No end state — what is true when this is complete?

### Good

```markdown
### Login

**Actor:** Visitor (unauthenticated)
**Trigger:** Visitor submits email and password

**Flow:**
1. Visitor submits email and password.
2. System checks whether an account with that email exists and the password matches.
   - If no account found or password incorrect → visitor sees a generic "incorrect
     email or password" message. No indication of which was wrong (prevents
     enumeration). Failed attempt counter increments.
   - If failed attempts reach the lockout threshold → account moves to *locked* status.
     See: [Account Lockout scenario].
   - If account is *locked* → visitor sees "account locked" with instructions to
     unlock. No further validation. See: [Account Unlock scenario].
3. If credentials are valid and account is *active*:
   - A new Session is created.
   - Failed attempt counter resets to zero.
   - Visitor is taken to the page they originally tried to access, or their home
     page if they arrived at login directly.
4. If credentials are valid but account is *unverified* → visitor is redirected
   to email verification prompt. No session is created.

**End state:** A Session exists and the visitor is authenticated — or the attempt
was rejected with a reason the visitor can act on.
```

---

## Example 2: Requirement

### Bad

```markdown
FR-005: The system should handle payments securely and efficiently.
```

**Why it fails:**
- "Should" signals optionality — if it's mandatory, use "must"
- "Securely" is undefined — secure against what threat, to what standard?
- "Efficiently" has no threshold — efficiently compared to what?
- No acceptance criteria — there is no test you could write against this
- No rationale — why does this requirement exist?

### Good

```markdown
**FR-005** [Must Have]

*Statement:* Payment card data must not pass through or be stored on company
servers at any point during the checkout flow.

*Rationale:* PCI DSS compliance. Storing card data would place the system in
scope for a full PCI audit and ongoing compliance programme. Tokenisation via
the payment processor keeps the system out of PCI scope.

*Source:* Legal/Security policy — Decision D-007.

*Acceptance criteria:*
- All card entry is handled by the payment processor's hosted fields or SDK;
  raw card numbers never reach the application
- Card numbers, CVVs and expiry dates do not appear in application logs,
  error messages or API responses at any level of the stack
- A PCI self-assessment questionnaire confirms reduced scope is achieved
```

---

## Example 3: Terminology entry

### Bad

```markdown
**Order**
An order is when a customer orders something from the store. Also sometimes
called a "purchase" in the checkout flow and a "transaction" by the finance team.
```

**Why it fails:**
- Circular — defines "order" using the word "order"
- Lists three names without resolving which is correct
- Conflates Order (intent to purchase), Purchase (synonym), and Transaction
  (financial record) — these are different things
- A reader still does not know what an Order is after reading this

### Good

```markdown
**Order**
The record of a customer's intent to purchase. Created when the customer confirms
their cart. Persists through fulfilment regardless of payment outcome. Has a lifecycle
from *pending* through to *delivered*, *cancelled* or *returned*.

*Distinct from:*
- **Transaction** — the financial record of a single payment attempt. An Order
  may have multiple Transactions (e.g. one declined, one successful).
- **Fulfilment** — the physical preparation and shipment of the Order. An Order
  has at most one Fulfilment, created when it enters *processing* status.

*Code note:* The checkout module uses "purchase" for Order. This is a known
inconsistency — flagged for cleanup. Blueprint term is **Order** everywhere.
(See Decision D-003.)

**Transaction**
The financial record of one payment attempt against an Order. Immutable once
created. An Order accumulates Transactions as payment is attempted.

*Distinct from:* an **Order** (the purchase intent) and a **Payment Method**
(the stored card details used to create a Transaction).
```

---

## Example 4: Domain model entity

### Bad

```markdown
**User**
- id: integer
- email: varchar
- name: varchar
- password_hash: varchar
- is_active: boolean
- is_verified: boolean
- created_at: timestamp
- deleted_at: timestamp (nullable)
```

**Why it fails:**
- This is a database schema, not a domain model
- No states — `is_active` and `is_verified` in combination imply four states nobody named
- No lifecycle — who creates a User? Who can change it? Who deletes it?
- No relationships — what does a User have, belong to, or interact with?
- Implementation field names (`password_hash`, `deleted_at`) belong in tech spec

### Good

```markdown
**Entity: User**

*Definition:* A person who has registered for an account. Can place orders and
manage their own data.

*States:*
- **unverified** — registered but email not yet confirmed
- **active** — verified and in good standing; can place orders
- **suspended** — access restricted due to payment failure or policy violation;
  cannot place new orders; existing orders unaffected
- **deleted** — soft-deleted; record retained for 7 years per legal requirement;
  cannot log in

*Transitions:*
- unverified → active: User confirms email address
- active → suspended: Payment processor webhook reports unrecoverable failure,
  or admin suspends manually
- suspended → active: User resolves payment issue or admin reinstates
- active | suspended → deleted: User requests deletion or admin deletes

*Invariants:* A deleted User cannot be reactivated. Email address must be unique
across all non-deleted Users.

*Relationships:* Places Orders (0 or more). Has Sessions (0 or more). Has one
Payment Method (optional).

*Lifecycle owner:* Created by registration flow. Transitions managed by payment
processor webhooks, email verification flow, and admin tools. Deletion by user
request or admin action.
```

---

## Example 5: User story

### Bad

```markdown
US-003: As a user, I want notifications.
```

**Why it fails:**
- "User" is not a specific actor — which user? In what context?
- "Notifications" is not a need — it is a solution; what does the user actually need?
- No "so that" clause — no outcome, no way to evaluate whether it was delivered
- Not testable — there is no observable state of the system that satisfies "wants notifications"

### Good

```markdown
**US-003** [Must Have]

As a **customer who has placed an order**, I want to be notified when my order
ships and given a tracking reference, so that I know when to expect delivery
and can track the package without contacting support.

*Evidence:* "Where is my order?" accounts for 34% of support ticket volume
(Zendesk, Q3 2024). Exit survey data shows 61% of users who abandoned
post-purchase return visits cited lack of shipping updates as the reason.
Six user interviews (2024-10-08) confirmed that shipping confirmation is
expected within minutes of dispatch.

*Acceptance criteria:*
- Customer receives notification within 5 minutes of order reaching *shipped* status
- Notification includes order number, carrier name, and tracking link
- Tracking link is valid and shows current status when opened
- Notification is sent to the email address on the order, not necessarily the
  current account email (in case it was updated after placing the order)
```

---

## Example 6: Elicitation conversation

### Bad (model fills gaps silently)

> **User:** We need a user authentication system.
>
> **Model:** I'll spec that out. Users authenticate with email and password. Sessions
> last 24 hours. Passwords must be 8+ characters. There's a "forgot password" flow
> that sends a reset link. Here's the full spec:
> [generates 400 words of spec from a single sentence]

**Why it fails:**
- Made up session duration (24 hours) without asking
- Assumed password requirements without asking
- Assumed email/password auth — could be SSO, OAuth, magic links
- No scope established — is this for a new system? Existing system?
- No actors named — who are the users?
- No open questions surfaced — treated all gaps as decisions

### Good (model asks, captures, verifies)

> **User:** We need a user authentication system.
>
> **Model:** Let's capture this properly. First — what problem are we solving?
> Is this for a system that currently has no auth, or are we changing how auth works?
>
> **User:** New system, starting from scratch.
>
> **Model:** Good. One sentence — who are the users? Are they internal staff,
> customers, or both?
>
> **User:** Customers. B2C. And internal admins.
>
> **Model:** Two different actor types — good to know early. Do customers and admins
> authenticate the same way, or differently? For example, some products use social
> login for customers but SSO/LDAP for internal staff.
>
> **User:** Customers use email/password or Google. Admins use the company SSO.
>
> **Model:** Noted. Before I go further — let me capture what I have and check
> it's right:
>
> *Actors: Customer (email/password or Google OAuth), Admin (company SSO)*
> *Scope: New authentication system*
>
> Does that match? Anything missing?
>
> **User:** Yes, that's right.
>
> **Model:** Great. Now — what happens to a customer's session? Is there a timeout,
> or do they stay logged in until they log out?

**What this demonstrates:**
- One question at a time
- Asks before assuming
- Verification checkpoint before moving forward
- Extracts scope and actors before requirements

---

## Example 7: Contradiction surfaced in real time

> **User:** Users can cancel their subscription at any time.
>
> [... later in the session ...]
>
> **User:** We need to honour the 30-day notice period in our terms of service.
>
> **Model:** I want to flag a conflict before we go further. Earlier you said users
> can cancel at any time. Now you've described a 30-day notice period in the terms.
> These two things cannot both be true as stated.
>
> Which takes precedence? Some options:
> - Cancel takes effect immediately but the 30-day period still applies for billing
>   (they stop service but are charged for the remaining period)
> - Users can request cancellation at any time, but the effective date is 30 days out
> - There are exceptions — e.g. within a trial period, cancellation is immediate
>
> I'll note this as an open question until it's resolved.
> **OQ-004:** When a user cancels, does the cancellation take effect immediately or
> after a 30-day notice period? What is the billing treatment in each case?
> *Owner: [to assign] | Blocking: BR-002, FR-011*

---

## Example 8: Handling "I don't know"

### Bad

> **User:** I'm not sure what happens when the payment fails.
>
> **Model:** Typically in these cases, the system retries 3 times with exponential
> backoff, then marks the subscription as suspended and notifies the user.

**Why it fails:** Made up behaviour to fill a gap. The retry count, backoff strategy and notification are all invented.

### Good

> **User:** I'm not sure what happens when the payment fails.
>
> **Model:** That's fine — let me note it as an open question rather than assume.
>
> **OQ-007:** What is the payment failure handling policy? Specifically:
> - Is there a retry? How many times, over what period?
> - What status does the subscription move to?
> - Who is notified, through what channel, and when?
> - Is there a grace period before access is revoked?
>
> *Owner: [Product/Finance to decide] | Blocking: Scenarios 6, 7; FR-019, BR-005*
>
> We can continue with the rest of the spec and come back to this. What happens
> when a payment succeeds?
