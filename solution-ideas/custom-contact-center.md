# Add Copilot Studio to an existing third-party contact center

**Class:** Microsoft solution idea. **Intent:** Preserve an existing contact center's queues, voice/chat channels and customer database while adding self-service and employee assistance.

## Architecture

```mermaid
flowchart TB
    accTitle: Add Copilot Studio to an existing third-party contact center - architecture
    accDescr: Keep queue ownership with the existing contact center. Approve public and staff knowledge paths separately; the adapter must not turn a customer session into an employee session.
    subgraph group0["Contact center"]
        U["Customer chat or voice"]
        Q["Third-party CCaaS and<br/>queue"]
        H["Representative"]
    end
    subgraph group3["Agent integration"]
        B["Session adapter"]
        A["Copilot Studio"]
        E["Employee portal"]
    end
    subgraph group6["Data scopes"]
        K["Public service guidance"]
        I["Staff-only search"]
        D["Customer database"]
    end
    U -->|"Contact request"| Q
    Q -->|"Mapped customer session"| B
    B -->|"Permitted context"| A
    E -->|"Authenticated staff<br/>session"| A
    A -->|"Customer-facing<br/>retrieval"| K
    A -->|"Employee-scoped<br/>retrieval only"| I
    A -->|"Verified customer<br/>lookup"| D
    Q -->|"Human takeover"| H
```

**Review decision:** Keep queue ownership with the existing contact center. Approve public and staff knowledge paths separately; the adapter must not turn a customer session into an employee session.

## Technical flow

```mermaid
sequenceDiagram
    accTitle: Add Copilot Studio to an existing third-party contact center - technical flow
    autonumber
    participant U as Customer
    participant Q as Contact center
    participant B as Adapter
    participant A as Agent
    U->>Q: Start service conversation
    Q->>B: Route mapped session to bot
    B->>A: Send customer-scoped context
    alt Public question is resolved
        A-->>B: Return approved guidance
        B-->>Q: Relay to same customer session
    else Transfer requested or integration fails
        Q->>Q: Keep original session and route to<br/>staffed queue
        Q->>B: Stop automated replies after<br/>takeover
    end
```

## Components and flow

1. The contact-center-as-a-service platform owns the customer session. Its integration passes the permitted context into the agent experience. Separately, employees can consult an agent in their own portal.
2. Route public service questions to customer-facing guidance. Use a separate, restricted knowledge path for staff procedures; the reference includes Azure AI Search and Azure AI services for material outside native agent knowledge. Retrieve live customer transactions from the source database rather than a document answer.
3. For an unresolved case, return control to the contact center with a correlation ID. Use Dataverse for service metrics and, only where authorized, retain transcripts in a restricted data lake for analysis.

**When to choose it:** Use when replacing the contact center would disrupt existing routing or service levels. An adapter, session mapping and two support teams cost more to operate than a natively supported engagement hub.

**Trust boundary:** Agent access in an employee portal does not confer customer-channel access to employee procedures. Bind the contact-center identity to a verified customer before looking up an account.

**Failure handling and acceptance:** If the integration times out, keep the caller in the original queue and stop automated responses after a human takes over. Test a disconnected session and an employee-only article from the public channel.

**Sources:** [Microsoft Learn: Custom contact center solution](https://learn.microsoft.com/en-us/power-platform/architecture/solution-ideas/agent-custom-contact-center) · [Microsoft public sample: Genesys handoff](https://github.com/microsoft/CopilotStudioSamples/tree/main/contact-center/genesys-handoff) (one adapter example, not a requirement).
