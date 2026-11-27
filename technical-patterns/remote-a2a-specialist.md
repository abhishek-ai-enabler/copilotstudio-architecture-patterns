# Delegate a bounded task to a remote Agent2Agent specialist

**Class:** Synthesized technical pattern. **Intent:** A standards team already operates an agent on another framework that compares *published* interface specifications. Let a Studio agent request its assessment without giving the remote agent a user session, unreleased designs or release authority.

## Architecture

```mermaid
flowchart LR
    accTitle: Reach a separately hosted standards specialist through A2A
    M["Maker"] -->|"Review card and endpoint before release"| C["Configured A2A connection"]
    U["Reviewer"] -->|"Published versions to compare"| A["Studio primary agent"]
    A -->|"Delegate assessment"| C
    C -->|"Authenticated A2A task"| R["Remote standards agent"]
    R -->|"Read approved specifications"| S["Released specification registry"]
    S -->|"Versioned clauses"| R
    R -->|"Assessment and references"| C
    C -->|"Result or unavailable"| A
    A -->|"Qualified recommendation"| U
```

**Review decision:** Is independent **reasoning** needed, and is the conversation safe to share with that endpoint? If all you need is a versioned clause, use a read-only API or [MCP tool](mcp-tools.md). Protocol compatibility is not a reason to send private history to another operator.

## Technical flow

![Technical sequence: Delegate a task to an approved remote specialist](../assets/flows/remote-a2a-specialist.png)

<details>
<summary>Text and editable Mermaid sequence</summary>

```mermaid
sequenceDiagram
    accTitle: Validate the remote assessment before presenting it
    autonumber
    actor U as Reviewer
    participant A as Studio primary
    participant R as Remote A2A agent
    participant S as Specification registry
    U->>A: Compare public versions two and three
    A->>R: Delegate within the approved public-only conversation
    R->>S: Retrieve the two released specifications
    S-->>R: Published clauses or no verified match
    R-->>A: Assessment with clause references or unresolved status
    alt References match both requested versions
        A-->>U: Show potential incompatibilities with citations
    else Denied, timed out or unsupported claim
        A-->>U: Report that compatibility is not verified
    end
```

</details>

## Copilot Studio components

**Recommended build:** Microsoft Copilot harness, using **Build → Connected agents → Add A2A agent**. Configure the approved *agent card* URL and restrict routing to released specifications. This is not a Foundry Activity connection.

| Component | Use in this pattern | Harness alternative |
| --- | --- | --- |
| [Connected agent](../COMPONENTS.md#connected-agents) | Review the card's declared capabilities and actual destination, then attach the named specialist. A card describes a service; it does not authorize it. | The standard harness wizard expects the **communication endpoint**, not the card URL. Use that harness's instructions and availability terms. |
| [Authentication](../COMPONENTS.md#authentication-and-tool-credentials) | Configure an approved OAuth connection. Verify which principal reaches the remote service and what that principal may read. | A service credential authenticates the connection, not the reviewer; do not use it to imply user-specific access. |

**Copilot Credits drivers (high):** Routing, delegated turns and returned evidence add usage on the Microsoft Copilot harness. Budget the remote operator's model, retrieval and service separately. Repeating an entire assessment is more expensive than asking the reviewer to disambiguate the version. See [credit guidance](../COPILOT-CREDITS.md).

## Design notes

- **Bound the data:** Use a dedicated public-specification conversation. The primary can forward relevant history or rephrase the task; an instruction to send only two IDs is not an enforced filter. If sensitive history can enter, do not connect this specialist. Use a typed connector that constructs a sanitized request instead.
- **Trust the source, not the card or answer:** Approve endpoint ownership, authentication, egress terms and a read-only registry scope. Treat returned text as evidence, not an instruction to call another service. An agent's “compatible” assessment never approves a release.
- **Failure handling and tests:** Change the advertised endpoint or remove a required capability: suspend routing until reviewed. Test missing versions, a denied connection and an assessment citing the wrong version. The user must see an unresolved result, not a guessed conclusion. Don't automatically replay a timed-out delegation if the remote implementation may have side effects.

**Sources:** [Microsoft Copilot harness A2A integration](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/add-agent-to-agent) · [Standard harness A2A endpoint](https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-agent-agent-to-agent) · [Context sharing on delegation](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/authoring-add-other-agents).
