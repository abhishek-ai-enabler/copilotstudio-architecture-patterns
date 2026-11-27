# Standard harness: generative orchestration over topics, tools and knowledge

**Class:** Microsoft implementation-guide pattern (orchestration). **Intent:** Handle requests that combine several familiar tasks without writing a topic for every possible sequence.

## Architecture

```mermaid
flowchart TB
    accTitle: Standard harness: generative orchestration over topics, tools and knowledge - architecture
    accDescr: Use the planner to combine intents, but keep the evidence for each result separate. A cited warranty answer says nothing about whether a private repair lookup succeeded.
    subgraph group0["User channel"]
        U["Customer"]
    end
    subgraph group1["Standard harness"]
        A["Generative planner"]
        T["Authored topics and<br/>tool descriptions"]
    end
    subgraph group3["Evidence sources"]
        K["Warranty knowledge"]
        R["Authorized repair<br/>service"]
    end
    U -->|"Multi-intent request"| A
    T -->|"Candidate capabilities"| A
    A -->|"Find warranty policy"| K
    A -->|"Check repair under user<br/>identity"| R
    A -->|"Combine citation and<br/>live status"| U
```

**Review decision:** Use the planner to combine intents, but keep the evidence for each result separate. A cited warranty answer says nothing about whether a private repair lookup succeeded.

## Technical flow

```mermaid
sequenceDiagram
    accTitle: Standard harness: generative orchestration over topics, tools and knowledge - technical flow
    autonumber
    participant U as Customer
    participant A as Planner
    participant K as Knowledge
    participant R as Repair service
    U->>A: Find warranty and check my repair
    A->>K: Retrieve applicable terms
    K-->>A: Return cited policy
    A->>U: Ask for missing repair identifier
    U->>A: Supply identifier
    A->>R: Query permitted repair
    alt Authorized repair found
        R-->>A: Return current status
        A-->>U: Report status separately from<br/>warranty
    else Lookup denied or unavailable
        A-->>U: Show policy and identify unresolved<br/>lookup
    end
```

## Design notes

**Flow:** A planner selects from descriptions of tools, knowledge, topics and eligible agents, gathers missing inputs and combines their outputs. For “find the warranty and check my repair,” keep the cited warranty text distinct from the repair system's live status. Use an authored topic or flow for any fixed confirmation sequence.

**Choose it when** users express multiple intents and the capabilities have distinct purposes. Broad or overlapping descriptions make routing less predictable. For a mandatory fixed dialogue use [classic topics](classic-topics.md); for iterative exploration compare the [Copilot harness loop](copilot-reasoning-loop.md).

**Trust boundary:** A tool description tells the planner *when* to call, not *who* is allowed to act. Backend permissions, validation and confirmation still apply. Do not let the content of a retrieved warranty instruct the agent to invoke a tool.

**Failure handling:** If one part fails, label its outcome independently; finding the warranty is not evidence the repair lookup succeeded. Evaluate ambiguous tool pairs, missing identifiers and interrupted multi-intent conversations in the published channel.

**Sources:** [Microsoft Learn: Standard harness generative orchestration](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/understand-harnesses#standard-harness-generative-orchestration) · [Orchestrate agent behavior with generative AI](https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-generative-actions).
