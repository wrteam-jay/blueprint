# Diagram Guide

When to use diagrams, which type to use, and Mermaid patterns for each.

Diagrams compress complex flows into a form that is faster to scan than prose. Use them where a flow has branching, multiple actors, or is long enough that a reader would lose the thread. Do not use them instead of prose — prose is searchable, linkable, and readable in any context. Use them alongside.

All diagrams use [Mermaid](https://mermaid.js.org), which renders in GitHub, Notion, VS Code (with extensions), and most modern documentation tools.

---

## Choosing the right diagram type

| Situation | Diagram type |
|-----------|-------------|
| A user flow with decision points | Flowchart |
| Multiple actors passing data or control between them | Sequence diagram |
| An entity moving through states | State diagram |
| Entities and how they relate to each other | Entity-relationship diagram |

---

## Flowchart — user flows and decision trees

Use for: single-actor journeys, flows with branching, step-by-step processes.

```mermaid
flowchart TD
    A([Customer confirms cart]) --> B{Payment method on file?}
    B -->|No| C[Prompt to add payment method]
    C --> B
    B -->|Yes| D[Create Order in pending status]
    D --> E[Charge payment method]
    E --> F{Payment successful?}
    F -->|No| G[Move Order to payment_failed]
    G --> H[Notify customer]
    H --> Z([End: order failed])
    F -->|Yes| I[Reserve inventory]
    I --> J{All items available?}
    J -->|No| K[Move Order to on_hold]
    K --> L[Notify customer and fulfilment]
    L --> Z2([End: order on hold])
    J -->|Yes| M[Move Order to confirmed]
    M --> N[Send confirmation email]
    N --> Z3([End: order confirmed])
```

**Shapes:**
- `([text])` — start/end (rounded rectangle)
- `[text]` — process step (rectangle)
- `{text}` — decision (diamond)
- `((text))` — connector

**Tips:**
- Keep labels short — one action or one question
- Decision diamonds should always have labelled branches
- Every branch should reach a terminal state or loop explicitly
- Use `TD` (top-down) for step-by-step flows; `LR` (left-right) for pipelines

---

## Sequence diagram — multi-actor interactions and data flows

Use for: flows involving more than one actor passing data or control, API interactions, event-driven flows.

```mermaid
sequenceDiagram
    actor Customer
    participant App
    participant PaymentProcessor
    participant EmailService

    Customer->>App: Confirm cart
    App->>PaymentProcessor: Charge card (amount, token)
    PaymentProcessor-->>App: Payment success (transaction_id)
    App->>App: Create Order (confirmed)
    App->>App: Reserve inventory
    App->>EmailService: Send confirmation (order_id, customer_email)
    EmailService-->>Customer: Order confirmation email
    App-->>Customer: Order confirmed (order_id)
```

**Syntax:**
- `->>` — synchronous message (request)
- `-->>` — response
- `-x` — message that fails
- `actor Name` — a human actor (displayed with a person icon)
- `participant Name` — a system participant

**For failure paths:**

```mermaid
sequenceDiagram
    actor Customer
    participant App
    participant PaymentProcessor

    Customer->>App: Confirm cart
    App->>PaymentProcessor: Charge card
    PaymentProcessor-->>App: Payment declined
    App->>App: Move Order to payment_failed
    App-->>Customer: Payment failed — please update payment method
```

**Tips:**
- Keep actors to 3-5; more than that and the diagram becomes hard to read
- Show the response to every request — what comes back matters
- For async flows, add a note: `Note over App: waits for webhook`

---

## State diagram — entity lifecycles

Use for: any entity with more than two states, showing what triggers each transition.

```mermaid
stateDiagram-v2
    [*] --> pending : Order created

    pending --> confirmed : Payment successful
    pending --> payment_failed : Payment declined
    pending --> cancelled : Customer cancels

    payment_failed --> confirmed : Customer retries, payment successful
    payment_failed --> cancelled : Customer abandons

    confirmed --> processing : Fulfilment staff picks up
    confirmed --> cancelled : Customer cancels (before processing)

    processing --> shipped : Items dispatched
    processing --> on_hold : Item unavailable

    on_hold --> processing : Item restocked
    on_hold --> cancelled : Customer cancels or item never restocked

    shipped --> delivered : Delivery confirmed
    shipped --> returned : Customer initiates return

    delivered --> returned : Customer initiates return (within return window)

    cancelled --> [*]
    delivered --> [*]
    returned --> [*]
```

**Tips:**
- Label every transition with what triggers it
- Every state should have a path to a terminal state (`[*]`)
- Group related states with comments if the diagram is large:
  ```
  state "Active states" as active {
      confirmed
      processing
      shipped
  }
  ```

---

## Entity-relationship diagram — domain model

Use for: showing how entities relate to each other, cardinality, naming relationships.

```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains
    PRODUCT ||--o{ LINE_ITEM : "included in"
    ORDER ||--o| FULFILMENT : "fulfilled by"
    ORDER ||--o{ TRANSACTION : "paid via"

    CUSTOMER {
        string email
        string name
    }
    ORDER {
        string status
        timestamp placed_at
    }
    LINE_ITEM {
        int quantity
        decimal unit_price
    }
```

**Cardinality:**
- `||--||` — exactly one to exactly one
- `||--o|` — exactly one to zero or one
- `||--|{` — exactly one to one or more
- `||--o{` — exactly one to zero or more
- `o|--o{` — zero or one to zero or more

**Tips:**
- Include only the fields that matter for understanding the domain — not every column
- Relationship labels describe the relationship in plain English ("places", "contains", "fulfilled by")
- For large models, split into multiple diagrams by bounded context

---

## When not to use a diagram

- **Simple linear flows** — if there are no branches and only one actor, prose is clearer
- **Already obvious from the prose** — a diagram that mirrors the text exactly adds no value
- **More than ~8 nodes or ~6 actors** — diagrams become hard to read; break into sub-diagrams
- **As a substitute for text** — diagrams cannot be searched, linked to precisely, or read in plain text form

---

## Diagram placement

Place diagrams **after** the prose they illustrate:

```markdown
### Order Placement

1. Customer confirms cart...
2. System charges payment...
[full prose scenario]

**Flow:**

\`\`\`mermaid
flowchart TD
...
\`\`\`
```

Label every diagram with a caption so it can be referenced:

```markdown
*Figure 1: Order placement — happy path and payment failure*
```
