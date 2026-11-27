# Delegate release compatibility questions to a Foundry agent

**Class:** Synthesized technical pattern. **Intent:** Give employees one Studio front door while the release engineering team owns the Foundry agent that compares release notes, applies compatibility rules and cites its evidence.

## Architecture

```mermaid
flowchart TB
    accTitle: Studio routes a compatibility assessment to Foundry
    accDescr: Studio owns routing and presentation. A separately managed Foundry agent interprets the task and searches a release index approved for the front door's audience.
    subgraph front["Copilot Studio"]
        U["Employee"]
        A["Primary agent"]
        U -->|"Upgrade question and versions"| A
        A -->|"Cited assessment or unresolved status"| U
    end
    subgraph domain["Release engineering: Microsoft Foundry"]
        F["Connected Foundry agent"]
        T["Azure AI Search index tool"]
        F -->|"Retrieve release evidence"| T
        T -->|"Passages and source URLs"| F
    end
    subgraph data["Approved release corpus"]
        S["Versioned release notes in Search"]
    end
    A -->|"Activity protocol: delegated task and context"| F
    F -->|"Assessment and references"| A
    T -->|"Query using project connection"| S
    S -->|"Ranked release notes"| T
```

**Review decision:** Delegate when the release team owns **how to reach a conclusion**, including its model, instructions and tests. If the task is just “return the release note for version X,” give the parent a lookup tool instead: one query, one authorization check and no second agent interpreting the question.

## Technical flow

```mermaid
sequenceDiagram
    accTitle: One delegated assessment with an evidence check
    autonumber
    participant U as Employee
    participant P as Studio front door
    participant F as Foundry specialist
    participant S as Azure AI Search
    U->>P: Can team clients on v4 use the v6 service?
    P->>F: Delegate compatibility assessment for v4 and v6
    F->>S: Retrieve relevant notes through the index tool
    alt Both versions covered by approved evidence
        S-->>F: Versioned passages with source URLs
        F-->>P: Conclusion, conditions and citations
        P-->>U: Present conditions and supporting notes
    else Evidence absent, contradictory or retrieval unavailable
        S-->>F: Insufficient evidence or error
        F-->>P: Compatibility not verified
        P-->>U: Offer release engineering review
    end
```

## Copilot Studio components

**Recommended build ([harness](../COMPONENTS.md#the-harness-is-the-first-decision)):** Microsoft Copilot harness. Use **Build → Connected agents → Add → Add Foundry agent**. This is the documented external-agent integration, not the [same-environment Studio specialist](connected-agent.md). The specialist's Search tool belongs to Foundry; do not attach the index to the parent as well.

| Component | Use in this pattern | Alternative |
| --- | --- | --- |
| [Connected agent](../COMPONENTS.md#connected-agents): Microsoft Foundry | Select a connection using Microsoft Entra ID user login and the **Foundry project endpoint**. Supply the **Agent ID**, name and a description specific to cross-version assessments. | Standard documents a separate **preview** path: **Agents → Add an agent → Connect to an external agent → Microsoft Foundry**. |
| [Instructions](../COMPONENTS.md#instructions): routing and response | Parent retains ordinary lookups; specialist assesses compatibility. Require both versions and citations, or an explicit unresolved result. | Use a [Foundry IQ retrieval tool](foundry-iq-knowledge-base.md) if the parent should interpret the evidence itself. |
| [Authentication](../COMPONENTS.md#authentication-and-tool-credentials): front door and project access | Restrict entry to the approved audience; authorize the connection to the Foundry project separately. | For user-specific documents, choose retrieval that enforces the reader's grants rather than broadening the project connection. |

**Copilot Credits drivers (high):** On the Microsoft Copilot harness, routing, delegation and interpreting the result add runtime turns and tokens; returned context, retries, preview and evaluation affect usage. The Foundry specialist's model and its Search index, embeddings and optional semantic ranking are separate Azure costs, **not** a second Studio agent's credit charge. The Standard preview parent uses Standard billing instead. See [Copilot Credits guidance](../COPILOT-CREDITS.md).

## Design notes

- **Connection prerequisites:** Use an existing agent created in the current Foundry portal, permission to access its project, and the **Activity** protocol with the required authorization scheme (`BotServiceRbac`). Responses or A2A support alone is insufficient. A connection can save but fail on first use with HTTP 400 if Activity is missing; a previous-portal agent can return `404 - Version not found`. Check the integration and preview terms for the chosen harness.
- **Retrieval contract:** The Foundry index tool uses a project connection and named index. Provide searchable text and vectors plus retrievable passage text and source URLs. Pin the corpus to approved release notes; retrieve both versions and return only the conclusion, applicable conditions and links. If a necessary note is missing, “not verified” is different from “incompatible.”
- **Trust:** The parent can forward relevant history and rephrase the request. A routing description is not a redaction rule: use this design only if that context may cross into the Foundry project. The project connection's identity and any static index filter apply to the specialist's calls; neither proves access for the employee. Keep this index readable by the entire approved audience, or enforce verified per-document authorization before the model sees evidence. Use retrieval as a tool, not a second connected-agent hop.
- **Failure and evaluation:** Test a two-version comparison (delegates), a one-version lookup (stays local), and conflicting notes (abstains). Check citations and conditions in the **final channel response**, not just the specialist's output. Simulate project denial, an unavailable specialist and a Search timeout: the parent should stop without trying a broader source. Re-run these cases when the specialist, index or routing description changes; compare end-to-end latency and cost with a direct lookup.

**Sources:** [Studio: add a Foundry connected agent](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/add-agent-foundry) · [Standard harness integration (preview)](https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-agent-foundry-agent) · [Delegated context and one-level limit](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/authoring-add-other-agents) · [Foundry: connect a Search index tool](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/ai-search).
