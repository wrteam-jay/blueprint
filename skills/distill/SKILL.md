---
name: distill
description: Use when a system already exists but is not documented — to capture how it actually works, build shared vocabulary around it, and produce a living spec that the team can reason about and discuss.
---

# Distillation

This skill extracts a blueprint from an existing system. The system may be partially documented, fully undocumented, or documented in ways that no longer match reality. The goal is to capture how things actually work — not how they were intended to work or how someone remembers they work.

Code tells you what the system does. Tribal knowledge tells you why. A blueprint tells you both, in a form the whole team can read, discuss and evolve.

## Why distill?

Systems accumulate behaviour that was never written down. Decisions made in a sprint planning meeting three years ago now live silently in the codebase. New team members learn the system through osmosis and asking questions. Every time someone leaves, some of that understanding leaves with them.

Distillation makes the implicit explicit. It also reveals the gaps — things the system does that nobody intended, and things nobody knows whether were intentional or not.

The gap between what the system **does** and what it **should do** is information. Distillation surfaces both.

---

## Do not

- **Do not treat code as the spec.** Code is one input. It captures what the system does, including bugs, expedient hacks, and dead code. The blueprint captures what it should do.
- **Do not include database column names or types.** `user_id: integer`, `deleted_at: timestamp` — these are schema details. Use relationship names and domain concepts.
- **Do not leave terminology conflicts unresolved.** When you find `purchase` in the code and `order` in the product, pick one and flag the other for cleanup. Do not note both.
- **Do not write "this may be intentional" and move on.** If you do not know whether behaviour is intentional, open a question. "May be intentional" is not a finding.
- **Do not spec dead code.** If a code path is never reached in production, it does not belong in the blueprint.
- **Do not infer intent from implementation alone.** Just because the code does X does not mean X was intended. Validate with people who know the system.
- **Do not write implementation into the blueprint.** Rephrase at the behaviour level. See the [core discipline](../../SKILL.md#the-core-discipline) for the test and examples.
- **Do not generate a complete spec from reading code alone.** Distillation requires both code and people. Code reveals what happens; people reveal why and whether it was intended.

---

## What to read before you start

Before asking any questions or reading any code, establish the scope.

**"What part of the system are we documenting?"**
A full product, one feature area, one service? Be explicit about the boundary.

**"What sources do we have?"**
Code, existing documentation (even if outdated), people who know this system, Slack history, old tickets. All are valid. Different sources reveal different things.

**"What is most uncertain or most contested?"**
Start with what people disagree about or cannot confidently describe. That is where the blueprint adds the most value.

**"What should the blueprint be used for once it exists?"**
Onboarding? Discussing a redesign? Debugging a recurring issue? The use case shapes how detailed to go.

---

## Finding the right level of abstraction

The same discipline applies here as in forward elicitation: capture behaviour, not implementation.

### The "would a stakeholder care?" test

For every detail found in code or conversation, ask: "Would a product manager, designer or support team member need to know this?"

| Found | Stakeholder cares? | Capture |
|-------|-------------------|---------|
| Invitation expires after 7 days | Yes — affects user experience | Yes |
| Expiry enforced by a cron job running at midnight | No — mechanism | No |
| Users with suspended accounts cannot reset their password | Yes — policy | Yes |
| Password reset uses HMAC-SHA256 token generation | No — implementation | No |
| An order can be cancelled only before it ships | Yes — business rule | Yes |
| Cancellation calls a DELETE endpoint on the orders service | No — implementation | No |

### The "intentional or accidental?" test

When you find a behaviour, ask: "Was this designed, or did it accumulate?" Both matter, but differently.

- **Designed behaviour** → Document as a requirement or business rule
- **Accidental behaviour** → Document as an open question: "The system currently does X. Was this intentional? Is it correct?"

Some of the most valuable output from distillation is a list of things nobody can answer with confidence.

---

## Distillation process

### Step 1: Map the territory

Before capturing anything in the blueprint format, understand the landscape.

**From the codebase:**
- Entry points — where does the system accept input? (API routes, UI actions, webhooks, scheduled jobs, message consumers)
- Domain models — what entities does it manage? (usually in `models/`, `entities/`, `domain/`, or equivalent)
- Core flows — what are the main things the system does? (services, use cases, handlers)
- External integrations — what does it call or depend on?

**From existing documentation:**
- Product specs, even outdated ones (what was intended)
- API documentation (what is exposed)
- Runbooks (what happens when things go wrong — reveals implicit state machines)
- Architecture diagrams (boundaries between systems)
- Old tickets and PRs (why specific decisions were made)

**From people:**
- "Walk me through [flow] as you understand it"
- "What parts of this system are you least confident about?"
- "What would you want a new team member to know about this?"
- "What breaks most often, and why?"

Produce a rough map before writing any blueprint section files:

```
Entry points:
  - API: /api/orders/*, /api/payments/*, /api/subscriptions/*
  - Webhooks: /webhooks/stripe, /webhooks/shipment-tracker
  - Jobs: expire_trials (nightly), send_digests (daily)

Key entities:
  - User, Subscription, Order, Payment, Invoice

Core flows:
  - Checkout, Subscription renewal, Order cancellation, Refund

External dependencies:
  - Stripe (payments), SendGrid (email), Shippo (shipping)
```

### Step 2: Extract the terminology

Before documenting flows, establish the vocabulary. Existing systems often have terminology inconsistencies — the codebase uses one name, the product uses another, support uses a third.

**Signals to watch for:**
- Classes or tables with different names than what the product calls them (`invoice` in code, "receipt" in the product)
- The same concept appearing under multiple names in different parts of the codebase
- Comments like "same as X" or "equivalent to Y"

**Resolution:** Pick one term. The one the business and product use is usually right — not the one in the database column. Document the chosen term and note any code names that will need updating.

```markdown
**Subscription** — The ongoing commercial relationship between a customer and the
                   business. The codebase calls this `plan_membership` in some places
                   and `subscription` in others. *Blueprint term: Subscription.
                   Code cleanup needed.*
```

### Step 3: Extract entities and their states

Find where the system's data lives and what states it moves through.

**In code, look for:**
- Enum fields and status columns (`status: 'pending' | 'active' | 'cancelled'`)
- State machine libraries or explicit state transition methods
- Boolean fields that, in combination, imply states (`is_active` + `is_verified` = four implicit states)
- Nullable timestamp fields that encode state (`cancelled_at: null` means not cancelled)

**Extract implicit states.** The hardest part of distillation is finding the states nobody named. Look for conditional logic that checks combinations of fields — that is often an implicit state machine.

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

Surface the implicit state machine, give states names, and flag the question: "Is this how this was intended to work?"

### Step 4: Extract flows

Find where state changes and actions happen and trace them.

**Look for:**
- Functions or methods that change entity status
- Event handlers and webhook receivers
- Scheduled job bodies
- API endpoint handlers (the action the endpoint performs, not the endpoint itself)

For each flow, trace:
1. **What triggers it** — user action, time, external event, another flow completing
2. **What preconditions must be true** — what state must the system be in
3. **What changes** — what entities are created, updated or deleted
4. **What is communicated** — emails, notifications, webhooks sent
5. **What happens next** — does this trigger another flow

**The scattered logic problem.** Business logic is often spread across multiple layers — a check in the API handler, a method on the model, validation in a service. Consolidate it:

```
API handler checks: user.is_active
Model method checks: subscription.status = active
Service checks: payment.status = confirmed

→ The actual preconditions for checkout are all three combined.
  Capture once in the blueprint; note that consolidation is needed in code.
```

### Step 5: Walk scenarios with people

Code captures the current behaviour, including bugs. People carry the intent. Walk through key scenarios with someone who knows the system:

"Walk me through what happens when a customer cancels their subscription. Step by step, from their perspective."

Then compare with what the code actually does. Divergences are findings:
- "The code does X, but you described Y. Is one wrong, or are there cases where the code path is not what you described?"
- "This flow has a case the code handles but you didn't mention. Is this a known edge case?"
- "The code does X here but I couldn't find a reason. Do you know why?"

### Step 6: Identify gaps and questions

Distillation reveals:

**Undocumented decisions** — things the code does that nobody can explain. "Why does the system do X when Y happens?" If nobody knows, that is an open question.

**Undocumented requirements** — behaviour the system has that was never stated as a requirement. "The system does X. Is that intentional? Should it always do X?"

**Missing error handling** — flows that succeed in the happy path but have no documented failure behaviour. "What happens to the subscription when the payment processor is unavailable during renewal?"

**Stale documentation** — existing docs that describe behaviour the system no longer has, or vice versa. Flag and update.

**Technical debt visible at the spec level** — not implementation debt, but behavioural debt. The system does something in two different ways for historical reasons. The blueprint surfaces this, and the team can decide whether to reconcile it.

---

## Output format

Distillation produces a blueprint directory — one file per section. Each step in the distillation process writes its corresponding section file:

- Step 2 (terminology) → `terminology.md`
- Step 3 (entities and states) → `domain-model.md`
- Step 4 (flows) → `scenarios/` directory with one file per flow and `_index.md`
- Step 5 (walk scenarios) → updates to scenario files and `questions.md`
- Step 6 (gaps and questions) → `questions.md` and `decisions.md`

Context, scope, actors, stories, and requirements are captured throughout and written to their respective files. Update the `README.md` manifest and `changelog.md` at the end.

---

## Checklist: have you abstracted enough?

Before publishing a distilled blueprint:

- [ ] No database column types or query syntax
- [ ] No API endpoint paths or HTTP methods
- [ ] No framework-specific concepts
- [ ] No specific library names (unless the integration itself is a domain concern)
- [ ] Foreign keys replaced with named relationships ("Order belongs to Customer")
- [ ] Technical status values replaced with meaningful names ("soft_deleted" → described as a behaviour)
- [ ] Implementation-specific field names replaced with business names

## Checklist: terminology consistency

- [ ] Each concept has exactly one name throughout the blueprint
- [ ] No "also known as" or "equivalent to" notes (resolve, don't annotate)
- [ ] Terminology matches what the product and business actually use
- [ ] Code names that differ from blueprint terms are flagged for cleanup

## Common distillation findings

**The behaviour nobody owns.** Logic that runs but that no current team member can explain or owns. Document it as-is, flag as an open question.

**The workaround that became permanent.** Something added temporarily that is now core to how the system works. The code often has a comment about it being temporary. Document the actual behaviour; note the history.

**The feature no one uses.** Code paths that exist but are never triggered in production. Distillation is a good time to question whether these belong in the spec at all.

**The inconsistent state machine.** An entity that can reach the same state via two paths, with subtly different outcomes. Document both paths; flag whether this is intentional.

---

## References

- [Section guide](../../references/section-guide.md) — what each section must contain
- [Diagram guide](../../references/diagram-guide.md) — Mermaid patterns for flows, states and domain models
