# Travel concierge with public guidance and private booking lookup

**Class:** Microsoft solution idea. **Intent:** Answer “what does my fare include?” and “what balance remains?” in one website conversation without treating a knowledge document as a booking ledger.

## Architecture

```mermaid
flowchart TB
    accTitle: Travel concierge with public guidance and private booking lookup - architecture
    accDescr: Decide exactly where a public conversation becomes a private lookup. A booking reference helps locate a record but cannot establish ownership.
    subgraph group0["Travel website"]
        U["Traveler"]
        A["Copilot Studio<br/>concierge"]
    end
    subgraph group2["Public information"]
        K["Travel and fare<br/>documents"]
    end
    subgraph group3["Private booking systems"]
        I["Authenticated lookup"]
        D["Dataverse customer<br/>mapping"]
        S["SQL reservations and<br/>transactions"]
    end
    U -->|"Travel or account<br/>question"| A
    A -->|"Retrieve applicable<br/>guidance"| K
    A -->|"Request scoped account<br/>data"| I
    I -->|"Resolve verified<br/>traveler"| D
    I -->|"Read owned itinerary or<br/>balance"| S
    I -->|"Scoped account result"| A
    A -->|"Cited guidance or<br/>verified account data"| U
```

**Review decision:** Decide exactly where a public conversation becomes a private lookup. A booking reference helps locate a record but cannot establish ownership.

## Technical flow

![Technical sequence: Travel concierge with public guidance and private booking lookup](../assets/flows/travel-concierge.png)

<details>
<summary>Text and editable Mermaid sequence</summary>

```mermaid
sequenceDiagram
    accTitle: Travel concierge with public guidance and private booking lookup - technical flow
    autonumber
    participant U as Traveler
    participant A as Concierge
    participant K as Knowledge
    participant S as Booking service
    U->>A: Ask about a trip
    alt Public fare or destination question
      A->>K: Find applicable current document
      K-->>A: Return source and effective date
      A-->>U: Cite applicable guidance
    else Personal balance request
      A->>U: Require verified traveler identity
      U->>A: Complete sign-in
      A->>S: Query authorized booking
      alt Live balance available
        S-->>A: Return balance, currency and time
        A-->>U: Show verified balance
      else Backend unavailable
        A-->>U: Withhold amount and offer<br/>representative
      end
    end
```

</details>

## Copilot Studio components

**Recommended build ([harness](../COMPONENTS.md#the-harness-is-the-first-decision)):** Standard harness on a website, with a switch to authenticated lookup. This design needs one verified reservation read, not a reasoning loop; compare another harness only if the itinerary task becomes more complex.

| Component | Use in this pattern | Harness alternative |
| --- | --- | --- |
| [Knowledge](../COMPONENTS.md#knowledge-sources): Travel, fare and rescheduling documents | Return cited policy with its effective date. | All harnesses. |
| [Authentication](../COMPONENTS.md#authentication-and-tool-credentials): Website sign-in | Required before any itinerary or balance lookup. | All harnesses. |
| [Topics](../COMPONENTS.md#topics-and-system-topics): Authenticated lookup topic | Marks where the public conversation becomes a private lookup. | Copilot: workflow tool. |
| [Connector tool](../COMPONENTS.md#connector-tools): Dataverse and SQL reservations | Return the permitted booking, currency and lookup time. | All harnesses. |
| [Escalation and handoff](../COMPONENTS.md#escalation-and-handoff): Travel representative | Handles exceptions and transactions outside the agent's scope. | All harnesses. |

**Not the right component:** A booking reference as proof of ownership.

**Copilot Credits drivers (medium):** Travelers are not covered by Microsoft 365 Copilot licenses. Answers bill at 1 or 2 and lookup steps at 5 each. Authored topics for frequent questions reduce generative answers. See [Copilot Credits guidance](../COPILOT-CREDITS.md).

## Components and flow

1. Copilot Studio clarifies the destination, operator or fare type. Retrieve the applicable travel, airport or rescheduling document and show its source and effective date.
2. Switch to authenticated lookup for itineraries or balances. Resolve the traveler's permitted booking against Dataverse customer/location records and the reservation and transaction system in SQL. Return the currency and time of the lookup.
3. Distinguish an explanation of the change policy from a change to an actual reservation. Direct exceptions or transactions outside the agent's approved scope to a travel representative.

**When to choose it:** Useful when public content and live reservations change at different rates. If customers only need opening hours or directions, do not introduce a connection to the reservation system.

**Trust boundary:** A booking reference or surname alone must not unlock an itinerary. Scope database operations to the verified traveler and booking; do not copy private balances into the searchable travel corpus.

**Failure handling and acceptance:** On stale or conflicting travel guidance, link to the current authority rather than guaranteeing eligibility. If SQL is unavailable, continue public Q&A but explicitly withhold the balance. Test two travelers with the same surname.

**Source:** [Microsoft Learn: Travel concierge using generative AI with Copilot Studio](https://learn.microsoft.com/en-us/power-platform/architecture/solution-ideas/agent-travel-customer).
