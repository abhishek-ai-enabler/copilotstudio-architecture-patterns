# Prototype an agent-local REST tool from OpenAPI

**Class:** Synthesized technical pattern. **Status:** The documented direct REST API tool is **preview** on the standard harness. **Intent:** Try a narrow API operation before investing in a shared connector.

## Architecture

```mermaid
flowchart TB
    accTitle: Prototype an agent-local REST tool from OpenAPI - architecture
    accDescr: Treat the direct REST tool as a standard-harness preview prototype. Decide whether reuse, release controls and support requirements justify a connector before moving to production.
    subgraph group0["Prototype"]
        A["Standard-harness agent"]
        T["Agent-local REST tool"]
    end
    subgraph group2["Maker-controlled<br/>configuration"]
        O["Reviewed OpenAPI<br/>contract"]
    end
    subgraph group3["Approved test service"]
        S["Read-only inventory API"]
    end
    O -->|"Permitted operations<br/>and schema"| T
    A -->|"Product and location<br/>inputs"| T
    T -->|"Authenticated<br/>availability request"| S
    S -->|"Quantity and snapshot<br/>time"| T
```

**Review decision:** Treat the direct REST tool as a standard-harness preview prototype. Decide whether reuse, release controls and support requirements justify a connector before moving to production.

## Technical flow

```mermaid
sequenceDiagram
    accTitle: Prototype an agent-local REST tool from OpenAPI - technical flow
    autonumber
    participant U as Tester
    participant A as Prototype agent
    participant T as REST tool
    participant S as Test API
    U->>A: Check availability for product and<br/>location
    A->>T: Select approved read operation
    T->>S: Submit scoped request
    alt Expected schema and authorized record
        S-->>T: Return quantity and snapshot time
        A-->>U: Present test availability
    else Schema mismatch or denial
        T-->>A: Return failure, not inventory data
        A-->>U: Withhold unverified quantity
    end
```

## Design notes

**Flow:** Give the agent a reviewed OpenAPI description for an approved service, configure the authentication scheme and select only the needed operations. For an availability prototype, accept a product ID and location, then present the returned quantity and snapshot time. Define what an empty result means.

**Choose it when** one agent needs a small, well-defined integration in a nonproduction evaluation. API configuration is local to the agent; promote widely reused operations to a governed connector or centrally managed tool service instead. Verify OpenAPI compatibility after import.

**Trust boundary:** Endpoint, method and credential policy belong in the configuration, not the prompt. Limit the prototype to read-only synthetic or approved test data. API scopes still need enforcement by the receiving service.

**Failure handling:** Validate required fields and response type; do not turn an error body into an availability answer. Test an incompatible schema revision and an unauthorized product before treating the prototype as evidence for a production design.

**Source:** [Extend your agent with tools from a REST API (preview)](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agent-extend-action-rest-api).
