# Reconcile an uncertain write before retrying it

**Class:** Synthesized technical pattern. **Intent:** A service desk agent submitted an approved replacement order, but the reply timed out. Find out whether the order exists without placing it twice. This starts **after** authorization; it is not another approval workflow.

## Architecture

```mermaid
flowchart LR
    accTitle: Resolve a lost receipt at the order system
    U["Requester"] -->|"Check status or explicitly submit"| A["Copilot Studio agent"]
    A -->|"Check or reconcile"| Q["Read-status operation"]
    A -->|"Explicit submission only"| C["Submit operation"]
    Q -->|"Read by caller and request key"| S["Order system with unique request key"]
    C -->|"Verify approval, bind key and payload"| S
    S -->|"Receipt, pending, not found or unknown"| Q
    S -->|"Committed receipt or rejection"| C
    Q -->|"Caller-scoped status; never creates"| A
    C -->|"Receipt, rejection or uncertain outcome"| A
    A -->|"Confirmed, pending or needs review"| U
    A -.->|"Unresolved past deadline"| H["Operations reconciliation queue"]
```

**Review decision:** Which system guarantees one effect per business request and can return its receipt? A flow run ID identifies an attempt; it cannot prove the downstream write happened once.

## Technical flow

![Technical sequence: Reconcile an uncertain write before retrying it](../assets/flows/write-reconciliation.png)

<details>
<summary>Text and editable Mermaid sequence</summary>

```mermaid
sequenceDiagram
    accTitle: Query before replay after an ambiguous acknowledgment
    autonumber
    actor U as Requester
    participant A as Service desk agent
    participant B as Order tool
    participant S as Order system
    alt Status inquiry only
        U->>A: Check my replacement
        A->>B: Read status for this request ID
        B->>S: Look up caller-scoped key without creating
        S-->>B: Receipt, pending, not found or unknown
        B-->>A: Observed status only
        A-->>U: Show status without submitting
    else Explicit submission of approved order
        U->>A: Submit my approved replacement
        A->>B: Submit approved request ID
        B->>S: Verify authority and create once by key and payload
        alt Receipt or rejection returned
            S-->>B: Receipt or rejection
            B-->>A: Verified outcome
            A-->>U: Show receipt or rejection
        else Response missing after submission
            B->>S: Read status using the same caller and key
            S-->>B: Receipt, pending, not found or unknown
            B-->>A: Status without a second submission
            A-->>U: Show receipt or tracking reference for follow-up
        end
    end
```

</details>

## Copilot Studio components

**Recommended build:** Standard harness. The connector invokes a business API that atomically binds a caller-scoped key and payload to a single order. A [workflow approval](approval-workflow.md) or an existing order system provides authorization before this sequence.

| Component | Use in this pattern | Harness alternative |
| --- | --- | --- |
| [Connector tool](../COMPONENTS.md#connector-tools) | Expose submit and read-status operations. Bind the status lookup to the same tenant and authorized user as the order. | On another harness, keep the same backend contract; replacing the caller with MCP does not add idempotency. |
| [Human gate](../COMPONENTS.md#human-in-the-loop-gates) | Operations resolves ambiguous aged requests against the source before anyone replays them. | A case queue can outlive the chat session. |

**Copilot Credits drivers (medium):** Count submission and status lookups where metered. Return a tracking reference instead of keeping the agent polling; estimate background reconciliation and the order service separately. See [credit profiles](../COPILOT-CREDITS.md#pattern-credit-profiles).

## Design notes

- **Use when:** Retries could create duplicate refunds, orders or postings. For a service with no unique external key, idempotent operation or authoritative lookup, do not promise exactly-once behavior: hold ambiguous calls for review. A local “sent” flag cannot close the gap between a remote commit and a lost acknowledgment.
- **Trust:** The backend derives or verifies the key from the approved immutable business request and tenant; it does not trust a model-generated UUID on each turn. Reuse of a key with changed amount, recipient or payload is a conflict, not a replay. Recheck authorization on lookups and never treat possession of a request ID as authority.
- **Acceptance tests:** Ask “check my replacement” with an authorized request ID for which no order exists. Assert a status lookup, **zero submit calls**, and no new order. Return “not found” only when the lookup is authoritative; otherwise say “not verified.” If intent is ambiguous, ask which operation the caller wants and do not submit.
- **Lost-reply test:** Drop the response *after* the backend commits. Repeat the same explicitly requested and approved operation concurrently and from a new conversation: the caller should see one business receipt. A changed payload or a different tenant must not get that receipt. If a not-found response can lag the write, wait or escalate. A missing receipt is never an instruction to submit.

**Sources:** [Azure Architecture Center: Asynchronous Request-Reply, including idempotency keys](https://learn.microsoft.com/en-us/azure/architecture/patterns/asynchronous-request-reply) · [Retry pattern and idempotency](https://learn.microsoft.com/en-us/azure/architecture/patterns/retry) · [Studio tool credentials](https://learn.microsoft.com/en-us/microsoft-copilot-studio/configure-enduser-authentication).
