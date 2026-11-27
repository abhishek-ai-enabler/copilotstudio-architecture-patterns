# Expose a narrow business operation through a connector

**Class:** Synthesized technical pattern. **Intent:** Let an agent use a business API through a reusable operation rather than inventing arbitrary requests.

## Architecture

```mermaid
flowchart TB
    accTitle: Expose a narrow business operation through a connector - architecture
    accDescr: Approve specific business operations and scopes, not broad API reach. A shipment status question should have no route to a write unless a separate change is explicitly authorized.
    subgraph group0["Conversation"]
        U["User"]
        A["Copilot Studio"]
    end
    subgraph group2["Integration contract"]
        C["Prebuilt or custom<br/>connector"]
    end
    subgraph group3["Service ownership"]
        S["Shipment API"]
        D["Shipment records"]
    end
    U -->|"Ask for status"| A
    A -->|"Invoke named read<br/>operation"| C
    C -->|"Validated ID and scoped<br/>connection"| S
    S -->|"Enforce access and read<br/>state"| D
    S -->|"Return status and<br/>timestamp"| C
    C -->|"Mapped allowed fields"| A
    A -->|"Verified status"| U
```

**Review decision:** Approve specific business operations and scopes, not broad API reach. A shipment status question should have no route to a write unless a separate change is explicitly authorized.

## Technical flow

```mermaid
sequenceDiagram
    accTitle: Expose a narrow business operation through a connector - technical flow
    autonumber
    participant U as User
    participant A as Agent
    participant C as Connector
    participant S as Shipment API
    U->>A: Where is my shipment
    A->>C: Select status operation with<br/>shipment ID
    C->>S: Make bounded read request
    alt Authorized shipment found
        S-->>C: Return current status and timestamp
        C-->>A: Map response to allowed fields
        A-->>U: Present verified status
    else Denied or throttled
        C-->>A: Return safe error category
        A-->>U: Report lookup unavailable, no change<br/>requested
    end
```

## Design notes

**Flow:** Start with a supported prebuilt Power Platform connector. If none meets the need, define a custom connector around an owned REST API. Expose a specific operation such as “read shipment status,” with required identifiers, a bounded response and a description distinct from “request shipment change.” Return the system's status and timestamp, not its full raw object.

**Choose it when** several agents or flows need a stable service contract. A custom connector requires someone to own API versioning and authentication. A [direct REST tool](direct-rest-tool.md) may suit a one-agent prototype; [MCP](mcp-tools.md) may suit a centrally changing catalog.

**Trust boundary:** Configure which identity the connection uses. Validate record access, fields and business rules at the service. Put endpoint selection under maker/admin control, not a user-provided URL.

**Failure handling:** Map not found, permission denied and temporarily unavailable to distinct safe outcomes. Respect throttling; replay writes only with an idempotency key and reconciliation. Test that a status question cannot accidentally call the change operation.

**Source:** [Plan and design integration strategies for Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/integrations).
