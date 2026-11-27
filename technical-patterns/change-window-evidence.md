# Combine policy evidence, Microsoft Graph and Azure inventory in a change brief

**Class:** Synthesized technical pattern. **Intent:** Answer “Which maintenance window can I propose for the orders service?” A policy passage explains the rule; Azure Resource Graph identifies the visible resources; Microsoft Graph supplies free/busy slots. The output is a proposal, not a calendar booking or an Azure change.

## Architecture

```mermaid
flowchart TB
    accTitle: Three independent authorities contribute to one reviewable brief
    U["Change owner"] -->|"Service, dates and zone"| A["Copilot Studio topic"]
    A -->|"Approved policy scope"| K["Knowledge source<br/>change policy"]
    K -->|"Versioned citation"| A
    A -->|"Service ID and window"| B["Read-only evidence service"]
    B -->|"Scoped inventory query"| R["Azure Resource Graph"]
    B -->|"Free/busy request"| G["Microsoft Graph"]
    R -->|"Visible inventory"| B
    G -->|"Calendar availability"| B
    B -->|"Facts with scope and time"| A
    A -->|"Draft or missing evidence"| U
    U -.->|"Separate submission"| H["Change approval system"]
```

**Review decision:** Assign an authority to each claim. A calendar can say a reviewer appears available; it cannot grant change approval. Inventory can identify resources visible in a subscription; it cannot prove the absence of dependencies.

## Technical flow

![Technical sequence: Combine policy evidence, Microsoft Graph and Azure inventory in a change brief](../assets/flows/change-window-evidence.png)

<details>
<summary>Text and editable Mermaid sequence</summary>

```mermaid
sequenceDiagram
    accTitle: Reconcile policy, inventory scope and time before drafting
    autonumber
    actor U as Change owner
    participant A as Studio agent
    participant B as Evidence service
    participant R as Azure Resource Graph
    participant G as Microsoft Graph
    U->>A: Request windows for one service and date range
    A->>A: Retrieve the applicable policy and its citation
    A->>B: Supply approved service key, range and time zone
    B->>R: Read visible inventory in allowed subscriptions
    R-->>B: Scoped results or incomplete coverage
    B->>G: Request free/busy for the approved review group
    G-->>B: Time slots or unavailable calendars
    B-->>A: Return separate results, scopes and lookup times
    alt All required facts present and policy applies
        A-->>U: Propose windows with evidence for review
    else Source failed, missing permission or scope mismatch
        A-->>U: Identify the missing check without declaring a safe window
    end
```

</details>

## Copilot Studio components

**Recommended build:** Standard harness. A [topic](../COMPONENTS.md#topics-and-system-topics) collects the service and time zone; a [knowledge source](../COMPONENTS.md#knowledge-sources) grounds the policy; one user-authenticated [connector tool](../COMPONENTS.md#connector-tools) calls the team's read-only evidence service. If that service already serves several agents, [expose the reads through MCP](apim-rest-to-mcp.md) instead. For a curated policy corpus spanning repositories, [Foundry IQ](foundry-iq-knowledge-base.md) is a retrieval alternative, not a replacement for either live lookup.

| Component | Use in this pattern | Harness alternative |
| --- | --- | --- |
| [Topic nodes](../COMPONENTS.md#topic-nodes) | Ask for service and dates; use a condition to withhold a proposal if required evidence is missing. | On the Microsoft Copilot harness use a workflow if this check must always run in order. |
| Knowledge + connector tool | Cite a policy passage and return independently sourced inventory and calendar facts. | Keep the three sources distinguishable even if one MCP server exposes both live reads. |
| [Human gate](../COMPONENTS.md#human-in-the-loop-gates) | The change owner takes the draft to the existing approval process; the agent has no write tool. | The external approval remains authoritative on any harness. |

**Copilot Credits drivers (medium):** Count policy grounding and billable agent actions on the selected harness. Two downstream API requests behind one tool are not automatically two Studio agent actions. Estimate service hosting, any gateway, and any alternative knowledge-base/model usage separately. See [Copilot Credits guidance](../COPILOT-CREDITS.md).

## Design notes

- **Design the evidence contract first.** Return the policy URL/version, inventory scope and observation time, calendar time zone and slot, and a completeness flag for each source. Map service IDs to known subscriptions and review groups in trusted configuration. Use a fixed inventory query and a bounded time range. If the only need is meeting availability, use a calendar tool alone.
- **Trust boundary:** Call the Azure Resource Graph `Resources` API with Azure RBAC read access and Microsoft Graph `getSchedule` with an independently authorized, delegated work-account connection (`Calendars.ReadBasic` is the documented least privilege). A middle tier needs tokens for the correct audiences. Return only free/busy intervals, not event subjects; do not treat a partially visible subscription as a complete service inventory.
- **Failure handling and acceptance:** Azure Resource Graph is eventually consistent. If an authoritative last-minute configuration check is mandatory, require it in the change system. Test a hidden subscription, missing free/busy data and a daylight-saving transition. Each must produce a qualified proposal or no proposal, never a false approval. The agent has no tool to deploy a change or send a meeting invitation.

**Sources:** [Azure Resource Graph Resources REST API](https://learn.microsoft.com/en-us/rest/api/azureresourcegraph/resourcegraph/resources/resources?view=rest-azureresourcegraph-resourcegraph-2024-04-01) · [Resource Graph permissions and consistency](https://learn.microsoft.com/en-us/azure/governance/resource-graph/overview) · [Microsoft Graph calendar getSchedule](https://learn.microsoft.com/en-us/graph/api/calendar-getschedule?view=graph-rest-1.0).
