# Route HR requests to domain-specific agents

**Class:** Microsoft reference architecture. **Intent:** Give employees and managers one front door in Teams or Microsoft Copilot without putting policy search, personal records and manager-only operations behind one unrestricted tool.

## Architecture

```mermaid
flowchart TB
    accTitle: Route HR requests to domain-specific agents - architecture
    accDescr: Choose a specialist boundary that matches the permission boundary. Being routed to a manager specialist does not establish a manager-to-employee relationship.
    subgraph group0["Employee channel"]
        U["Employee or manager"]
        A["Copilot Studio HR<br/>orchestrator"]
    end
    subgraph group2["Domain specialists"]
        P["Policy agent"]
        T["Personal, leave and<br/>manager agents"]
        L["Learning agent"]
    end
    subgraph group5["Systems of record"]
        K["Indexed ITSM guidance"]
        H["HCM"]
        LMS["Learning system"]
    end
    U -->|"Entra-authenticated<br/>request"| A
    A -->|"Policy question"| P
    A -->|"Employee or manager<br/>transaction"| T
    A -->|"Learning task"| L
    P -->|"Retrieve authorized<br/>article"| K
    T -->|"Scoped connector or<br/>flow"| H
    L -->|"Read or assign learning"| LMS
```

**Review decision:** Choose a specialist boundary that matches the permission boundary. Being routed to a manager specialist does not establish a manager-to-employee relationship.

## Technical flow

```mermaid
sequenceDiagram
    accTitle: Route HR requests to domain-specific agents - technical flow
    autonumber
    participant U as Manager
    participant A as Orchestrator
    participant T as HR specialist
    participant H as HCM
    U->>A: Change a direct report's HR record
    A->>T: Delegate target and requested<br/>operation
    T->>H: Check current reporting relationship<br/>and authority
    alt Manager is authorized and confirms change
        T->>H: Submit validated change
        H-->>T: Return system receipt
        T-->>A: Return confirmed outcome
        A-->>U: Show receipt
    else Outside scope or HCM unavailable
        T-->>A: Return denial or unavailable status
        A-->>U: Report no confirmed change
    end
```

## Components and flow

1. Entra ID signs in the user. A Copilot Studio orchestrator distinguishes personal data, time off, manager actions, learning and HR policy. It asks which task the user wants if a request crosses domains.
2. The policy specialist retrieves approved ITSM articles indexed through a Microsoft 365 Graph connector. Transaction specialists use custom connectors and Power Automate to read or update the human capital management (HCM) or learning system.
3. Return a policy citation for advice and a system receipt for a completed action. Route sensitive or unresolved requests to an HR case in the ITSM system rather than passing the full conversation among agents.

**When to choose it:** Choose specialists when domains have distinct owners, access rules or release cycles. For a handbook-only assistant, one knowledge agent is simpler and avoids extra routing latency.

**Trust boundary:** A manager's title in conversation is not permission. Recheck direct-report relationships in the HCM system for the requested operation. Avoid sending salary or profile fields to the policy agent.

**Failure handling and acceptance:** If HCM is unavailable, the agent can still explain policy but must not claim that leave was approved. Record the failed stage and a case reference. Test switching from a policy question to a manager action, including a target outside the manager's reporting line.

**Source:** [Microsoft Learn: Modernize employee HR support with a multi-agent solution](https://learn.microsoft.com/en-us/power-platform/architecture/reference-architectures/modernize-hr-support).
