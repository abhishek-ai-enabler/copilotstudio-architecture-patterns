# Multilingual IT self-service across identity providers

**Class:** Microsoft reference architecture. **Intent:** Give employees one Teams entry point for IT guidance, catalog lookup and incident management without granting them access to anyone else's tickets.

## Architecture

```mermaid
flowchart TB
    accTitle: Multilingual IT self-service across identity providers - architecture
    accDescr: Approve incident updates only if ITSM can identify the employee and enforce ownership at its own boundary, including when a service connection is used.
    subgraph group0["Employee channel"]
        U["Teams employee"]
        ID["Entra ID"]
    end
    subgraph group2["Self-service"]
        A["Copilot Studio IT agent"]
        K["SharePoint IT guides"]
        B["Optional live-chat<br/>bridge"]
    end
    subgraph group5["Service desk"]
        I["ITSM catalog and<br/>incidents"]
        H["Desk analyst"]
    end
    ID -->|"Verified employee<br/>context"| A
    U -->|"Local-language request"| A
    A -->|"Find approved procedure"| K
    A -->|"Employee-scoped lookup<br/>or update"| I
    A -->|"Unresolved request and<br/>summary"| B
    B -->|"Translated live<br/>conversation"| H
    A -->|"Answer or receipt in<br/>employee language"| U
```

**Review decision:** Approve incident updates only if ITSM can identify the employee and enforce ownership at its own boundary, including when a service connection is used.

## Technical flow

![Technical sequence: Multilingual IT self-service across identity providers](../assets/flows/multilingual-it-service.png)

<details>
<summary>Text and editable Mermaid sequence</summary>

```mermaid
sequenceDiagram
    accTitle: Multilingual IT self-service across identity providers - technical flow
    autonumber
    participant U as Employee
    participant A as IT agent
    participant I as ITSM
    participant H as Service desk
    U->>A: Add a note to my incident
    A->>U: Confirm ticket and description in<br/>employee language
    U->>A: Confirm the requested change
    A->>I: Submit verified employee ID and<br/>ticket ID
    alt Employee owns incident
        I-->>A: Return update receipt
        A-->>U: Confirm with unchanged incident ID
    else Employee has no access
        I-->>A: Deny without exposing ticket data
        A-->>U: Explain that the update was not made
        opt Employee requests help
            A->>H: Request staffed handoff via<br/>configured bridge
        end
    end
```

</details>

## Copilot Studio components

**Recommended build ([harness](../COMPONENTS.md#the-harness-is-the-first-decision)):** Standard harness, generative orchestration in Teams with additional languages enabled. The Microsoft Copilot harness controls response language through instructions. Validate the ITSM connector and the live-chat bridge before you move.

| Component | Use in this pattern | Harness alternative |
| --- | --- | --- |
| [Authentication](../COMPONENTS.md#authentication-and-tool-credentials): Entra ID | Identifies the employee for every ticket operation. | All harnesses. |
| [Orchestration](../COMPONENTS.md#orchestration-modes): Generative orchestration | Separates how-to guidance, catalog requests and incident status. | Copilot: reasoning loop. |
| [Knowledge](../COMPONENTS.md#knowledge-sources): SharePoint guides and ITSM knowledge | Grounds cited guidance in the conversation language. | All harnesses. |
| [Connector tool](../COMPONENTS.md#connector-tools): ITSM connector | Reads catalog items and creates or updates incidents. ITSM enforces ownership. | All harnesses. |
| [Topics](../COMPONENTS.md#topics-and-system-topics): Incident confirmation topic | Shows the description before submission and keeps IDs untranslated. | Copilot: workflow tool. |
| [Escalation and handoff](../COMPONENTS.md#escalation-and-handoff): Optional Microsoft 365 Agents SDK bridge | Live chat with a summary and two-way translation. *(Optional.)* | Confirm support per harness. |

**Not the right component:** A service connection that lets any employee read any ticket.

**Copilot Credits drivers (medium):** Employee use by licensed Microsoft 365 Copilot users with their own identity is included. Otherwise, answers bill at 1 or 2 and tool steps bill as agent actions. Translation in the bridge is billed by that bridge's service. See [Copilot Credits guidance](../COPILOT-CREDITS.md).

## Components and flow

1. Entra ID identifies the employee in Teams. Copilot Studio detects the conversation language and distinguishes “how do I request a laptop?” from “where is my request?”
2. For guidance, retrieve an approved SharePoint guide or IT service management (ITSM) article and link to it. For orders, return the actual catalog form. For incidents, collect a local category, show the description and send the confirmed request through an ITSM connector.
3. Offer the service desk when self-service fails. The reference uses an optional Microsoft 365 Agents SDK bridge for live chat, a conversation summary and two-way translation. Keep incident IDs and product codes unchanged across languages.

**When to choose it:** Best when employees already work in Teams but the service desk and its knowledge use another platform. Search and deep links are cheaper to maintain than live chat; build the bridge only if the desk can staff it.

**Trust boundary:** Prefer per-user ITSM access. If identity providers differ, a scoped integration account must bind a verified employee identifier to every request; the ITSM backend must enforce ownership and record the actor. A name supplied in chat is not that identifier.

**Failure handling and acceptance:** If a create times out, reconcile it before creating another incident. When no analyst is available, offer a tracked callback rather than announcing a transfer. Test the same incident lookup in two languages and with a second employee who must not see it.

**Source:** [Microsoft Learn: Build a multilingual IT self-service agent](https://learn.microsoft.com/en-us/power-platform/architecture/reference-architectures/multilingual-it-self-service-agent).
