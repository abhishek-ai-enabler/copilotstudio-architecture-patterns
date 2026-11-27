# Rental discovery with a separate reservation and payment path

**Class:** Microsoft solution idea. **Intent:** Let a customer describe the rental they want in ordinary language while keeping availability, pricing and payment under transactional control.

## Architecture

```mermaid
flowchart TB
    accTitle: Rental discovery with a separate reservation and payment path - architecture
    accDescr: Approve chat for discovery, not settlement. A verified payment notification and a reconciled reservation, not the browser redirect, establish a completed booking.
    subgraph group0["Discovery"]
        U["Customer in Power Pages"]
        A["Copilot Studio search"]
        D["Dataverse listings and<br/>reservations"]
    end
    subgraph group3["Booking authority"]
        C["Checkout and hold<br/>service"]
        P["Payments API"]
        S["Azure SQL"]
    end
    subgraph group6["Payment provider"]
        T["Stripe hosted checkout"]
    end
    U -->|"Search criteria"| A
    A -->|"Allowed listings"| D
    U -->|"Select listing and<br/>request hold"| C
    C -->|"Request checkout for<br/>held price"| P
    U -->|"Pay on hosted page"| T
    T -->|"Return to portal after<br/>checkout"| U
    T -->|"Signed payment<br/>notification"| P
    P -->|"Record settlement"| S
    S -->|"Reconcile reservation<br/>status"| D
    A -->|"Matching listing cards"| U
    C -->|"Recheck and place<br/>time-limited hold"| D
    P -->|"Create hosted session"| T
```

**Review decision:** Approve chat for discovery, not settlement. A verified payment notification and a reconciled reservation, not the browser redirect, establish a completed booking.

## Technical flow

```mermaid
sequenceDiagram
    accTitle: Rental discovery with a separate reservation and payment path - technical flow
    autonumber
    participant U as Customer
    participant C as Checkout and hold
    participant D as Reservation store
    participant P as Payments API
    participant T as Stripe
    U->>C: Request selected listing
    C->>D: Recheck availability and acquire<br/>time-limited hold
    alt Inventory held
      D-->>C: Return hold and server-side price
      C->>P: Request checkout for held price
      P->>T: Create hosted checkout session
      T-->>P: Return session URL
      P-->>C: Return checkout link
      C-->>U: Redirect to hosted checkout
      U->>T: Complete payment on provider page
      T-->>U: Return to portal, pending<br/>confirmation
      T->>P: Deliver signed payment event
      P->>P: Verify signature and deduplicate<br/>event
      P->>D: Record settlement and confirm<br/>reservation
    else Another customer owns the hold
      D-->>C: Return unavailable
      C-->>U: Report unavailable without starting<br/>payment
    end
```

## Copilot Studio components

**Recommended build ([harness](../COMPONENTS.md#the-harness-is-the-first-decision)):** Standard harness in Power Pages for discovery. Checkout and payment stay outside the agent. Discovery has no need for the Microsoft Copilot harness; payment must never be an agent tool in any harness.

| Component | Use in this pattern | Harness alternative |
| --- | --- | --- |
| [Channel](../COMPONENTS.md#channels): Power Pages | Hosts discovery beside the portal's normal search. | Validate per harness. |
| [Prompt tool](../COMPONENTS.md#prompt-tools): AI Builder filter extraction | Turns the customer's description into listing filters. | Copilot: skill. |
| [Connector tool](../COMPONENTS.md#connector-tools): Dataverse listing query | Returns matching listings. | All harnesses. |
| [Topic nodes](../COMPONENTS.md#topic-nodes): Adaptive card | Shows listing cards that link to canonical listing pages. | Copilot: response formatting. |

**Not the right component:** A payment, hold or reservation tool in the agent. Checkout belongs to the Payments API.

**Copilot Credits drivers (medium):** Each search bills a prompt (AI tools rate) plus a generative answer for anonymous visitors. Cache common filters and keep listing cards compact. See [Copilot Credits guidance](../COPILOT-CREDITS.md).

## Components and flow

1. In Power Pages, Copilot Studio and AI Builder turn the customer's terms into listing filters. Query Dataverse and return cards linking to canonical listings; the portal's normal search remains available.
2. The customer selects a listing. Checkout rechecks availability, places a time-limited reservation under a lock, and creates a Stripe-hosted checkout session through the Payments API. No card details pass through the agent.
3. The Payments API verifies the provider notification and records the outcome in Azure SQL. Reconcile this state to the Dataverse reservation shown in the portal and model-driven admin app. A browser redirect is not proof of settlement.

**When to choose it:** Good for exploratory searches whose results lead to scarce inventory. Ordinary faceted search is easier to validate for exact criteria. Keep the two paths so a chat outage need not stop booking.

**Trust boundary:** Publish only customer-visible listing fields; bind the hold to the authenticated customer and price it server-side. Restrict payment/refund operations separately from listing edits.

**Failure handling and acceptance:** Deduplicate webhook deliveries by provider event ID. Expire unpaid holds; route a late successful payment for reconciliation rather than double-booking. Test two customers selecting the final available unit.

**Source:** [Microsoft Learn: Property rental portal with AI-driven search and payment processing](https://learn.microsoft.com/en-us/power-platform/architecture/solution-ideas/agent-rental-portal).
