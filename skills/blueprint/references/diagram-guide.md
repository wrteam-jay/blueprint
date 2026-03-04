<ref-guide name="diagram-guide">

<brief>When to use diagrams, which type, and Mermaid patterns for each. Diagrams compress complex flows — use alongside prose, not instead of it. All diagrams use Mermaid.</brief>

<table name="diagram-selection">
<row situation="User flow with decision points" type="Flowchart"/>
<row situation="Multiple actors passing data or control" type="Sequence diagram"/>
<row situation="Entity moving through states" type="State diagram"/>
<row situation="Entities and how they relate" type="Entity-relationship diagram"/>
</table>

<section name="flowchart">
Use for: single-actor journeys, branching flows, step-by-step processes.

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

Shapes: `([text])` start/end, `[text]` process, `{text}` decision, `((text))` connector.
Tips: short labels, labelled decision branches, every branch reaches terminal or loops, TD for steps, LR for pipelines.
</section>

<section name="sequence-diagram">
Use for: multi-actor interactions, API flows, event-driven flows.

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

For failure paths:

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

Syntax: `->>` request, `-->>` response, `-x` failure, `actor` human, `participant` system.
Tips: 3-5 actors max, show response to every request, `Note over App: waits for webhook` for async.
</section>

<section name="state-diagram">
Use for: any entity with >2 states.

```mermaid
stateDiagram-v2
    [*] --> pending : Order created
    pending --> confirmed : Payment successful
    pending --> payment_failed : Payment declined
    pending --> cancelled : Customer cancels
    payment_failed --> confirmed : Retry succeeds
    payment_failed --> cancelled : Customer abandons
    confirmed --> processing : Fulfilment picks up
    confirmed --> cancelled : Customer cancels
    processing --> shipped : Dispatched
    processing --> on_hold : Item unavailable
    on_hold --> processing : Restocked
    on_hold --> cancelled : Never restocked
    shipped --> delivered : Delivery confirmed
    shipped --> returned : Return initiated
    delivered --> returned : Return within window
    cancelled --> [*]
    delivered --> [*]
    returned --> [*]
```

Tips: label every transition with trigger, every state reaches a terminal, group related states for large diagrams.
</section>

<section name="er-diagram">
Use for: entity relationships, cardinality, named relationships.

```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains
    PRODUCT ||--o{ LINE_ITEM : "included in"
    ORDER ||--o| FULFILMENT : "fulfilled by"
    ORDER ||--o{ TRANSACTION : "paid via"
```

Cardinality: `||--||` one-to-one, `||--o|` one-to-zero-or-one, `||--|{` one-to-one-or-more, `||--o{` one-to-zero-or-more.
Tips: only fields that matter for understanding, plain English relationship labels, split by bounded context for large models.
</section>

<constraints name="when-to-split">
Split when: >8 nodes, >5 actors in sequence, >8 states, mixed concerns (normal flow + error paths).

How: flowcharts split at decision points (happy path first, then branches). Sequence diagrams split by phase or actor group. State diagrams split by lifecycle stage. ER diagrams split by bounded context.

Name consistently: Figure 3a, 3b, 3c.
</constraints>

<constraints name="when-not-to-use">
<c rule="Simple linear flows">No branches, one actor — prose is clearer</c>
<c rule="Mirrors prose exactly">Adds no value</c>
<c rule=">8 nodes or >6 actors">Split into sub-diagrams instead</c>
<c rule="As substitute for text">Diagrams cannot be searched or linked precisely</c>
</constraints>

Place diagrams after prose, not instead. Label every diagram with a caption for reference.

</ref-guide>
