# Resolve customer questions or transfer them into a Dynamics workstream

**Class:** Microsoft solution idea. **Intent:** Let customers try self-service without making them start over when a representative is needed.

## Architecture

```mermaid
flowchart TB
    accTitle: Resolve customer questions or transfer them into a Dynamics workstream - architecture
    accDescr: Approve a live transfer only when a configured hub and staffed workstream can accept it. Otherwise promise a tracked follow-up, not a connected representative.
    subgraph group0["Self-service"]
        U["Customer"]
        A["Copilot Studio"]
        K["Approved SharePoint and<br/>Dataverse knowledge"]
    end
    subgraph group3["Engagement hub"]
        T["Escalate topic and<br/>transfer node"]
        W["Dynamics 365 workstream"]
        H["Representative"]
    end
    U -->|"Question or request for<br/>a person"| A
    A -->|"Retrieve approved<br/>answer"| K
    A -->|"Unresolved issue or<br/>explicit request"| T
    T -->|"Transfer session<br/>context"| W
    W -->|"Assign queued session"| H
    A -->|"Cited answer"| U
```

**Review decision:** Approve a live transfer only when a configured hub and staffed workstream can accept it. Otherwise promise a tracked follow-up, not a connected representative.

## Technical flow

```mermaid
sequenceDiagram
    accTitle: Resolve customer questions or transfer them into a Dynamics workstream - technical flow
    autonumber
    participant U as Customer
    participant A as Agent
    participant K as Approved knowledge
    participant W as Dynamics workstream
    participant H as Representative
    U->>A: Ask a question
    A->>K: Retrieve approved answer
    alt Approved answer found
      K-->>A: Return cited content
      A-->>U: Answer with source
    else Unresolved or person requested
      A->>W: Send transfer event and allowed<br/>context
      alt Representative accepts
        W->>H: Assign session and context
        H-->>U: Continue conversation and verify<br/>private requests
      else Queue closed or transfer fails
        A-->>U: Offer callback or tracked case<br/>instead
      end
    end
```

## Copilot Studio components

**Recommended build ([harness](../COMPONENTS.md#the-harness-is-the-first-decision)):** Standard harness, generative orchestration, with the Dynamics 365 Contact Center channel. The Dynamics 365 Contact Center channel is listed for the standard harness only. The Customer Conversation harness is the alternative for voice and chat with escalation.

| Component | Use in this pattern | Harness alternative |
| --- | --- | --- |
| [Knowledge](../COMPONENTS.md#knowledge-sources): Approved SharePoint and Dataverse content | Provides cited product guidance. | All harnesses. |
| [Connector tool](../COMPONENTS.md#connector-tools): Ticket creation | Opens a tracked follow-up when no transfer is available. | All harnesses. |
| [Topics](../COMPONENTS.md#topics-and-system-topics): Escalate system topic | Handles explicit requests for a person, failed tickets and unresolved issues. | Customer Conversation: **Escalate** tool. |
| [Topic nodes](../COMPONENTS.md#topic-nodes): Transfer conversation | Hands the session to the configured engagement hub. | Customer Conversation: **Escalate** tool. |
| [Escalation and handoff](../COMPONENTS.md#escalation-and-handoff): Dynamics 365 workstream and queue | Routes to a representative, who verifies the customer. | All harnesses. |

**Not the right component:** A default escalation message presented as a live transfer.

**Copilot Credits drivers (medium):** Customer traffic is billed: answers at 1 or 2 and agent actions at 5 until transfer. Representative time is licensed in Dynamics 365. Cited answers that resolve the issue reduce both transfers and credits. See [Copilot Credits guidance](../COPILOT-CREDITS.md).

## Components and flow

1. Copilot Studio separates product guidance from case-specific requests. Use approved SharePoint/Dataverse knowledge for a cited answer, or collect enough information for a follow-up ticket.
2. An explicit request for a person, a failed ticket operation or an unresolved issue reaches the Escalate system topic. Configure the **Transfer conversation** node and the engagement hub; a default escalation message alone does not connect a person.
3. Dynamics 365 routes the session to a workstream and queue. A representative picks it up in the service workspace with conversation context and verifies the customer before discussing private case details.

**When to choose it:** Useful when Dynamics already owns queues and case follow-up. For unstaffed channels, offer a tracked asynchronous ticket instead of advertising live chat. For an existing non-Microsoft hub, compare the [adapter-based solution](custom-contact-center.md).

**Trust boundary:** Handoff can transmit history and variables, not just an intent. Minimize sensitive data collected upstream and restrict access at the receiving queue. Do not treat possession of chat history as customer authentication.

**Failure handling and acceptance:** Distinguish requested, queued and accepted transfers. If no one accepts, offer a callback or case and display its reference. Test after-hours escalation and verify the bot does not keep responding over a human representative.

**Source:** [Microsoft Learn: Streamline customer service with a customer support assistance agent](https://learn.microsoft.com/en-us/power-platform/architecture/solution-ideas/customer-support-agent).
