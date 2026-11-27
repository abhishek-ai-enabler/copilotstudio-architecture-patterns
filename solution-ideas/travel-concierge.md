# Travel concierge with public guidance and private booking lookup

**Class:** Microsoft solution idea. **Intent:** Answer “what does my fare include?” and “what balance remains?” in one website conversation without treating a knowledge document as a booking ledger.

## Components and flow

1. Copilot Studio clarifies the destination, operator or fare type. Retrieve the applicable travel, airport or rescheduling document and show its source and effective date.
2. Switch to authenticated lookup for itineraries or balances. Resolve the traveler's permitted booking against Dataverse customer/location records and the reservation and transaction system in SQL. Return the currency and time of the lookup.
3. Distinguish an explanation of the change policy from a change to an actual reservation. Direct exceptions or transactions outside the agent's approved scope to a travel representative.

**When to choose it:** Useful when public content and live reservations change at different rates. If customers only need opening hours or directions, do not introduce a connection to the reservation system.

**Trust boundary:** A booking reference or surname alone must not unlock an itinerary. Scope database operations to the verified traveler and booking; do not copy private balances into the searchable travel corpus.

**Failure handling and acceptance:** On stale or conflicting travel guidance, link to the current authority rather than guaranteeing eligibility. If SQL is unavailable, continue public Q&A but explicitly withhold the balance. Test two travelers with the same surname.

**Source:** [Microsoft Learn: Travel concierge using generative AI with Copilot Studio](https://learn.microsoft.com/en-us/power-platform/architecture/solution-ideas/agent-travel-customer).
