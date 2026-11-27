# Share a governed metric contract between agents and reports

**Class:** Synthesized technical pattern. **Intent:** Make “actual,” “target” and “last month” mean the same thing to a chat agent and an analyst's report, regardless of which Fabric integration is used.

## Architecture

```mermaid
flowchart TB
    accTitle: Share a governed metric contract between agents and reports - architecture
    accDescr: Approve the business definition of a measure, not just its name. The agent and reference report must reconcile for the same identity, filters and refresh state.
    subgraph group0["Model ownership"]
        O["Data owner"]
        M["Fabric semantic model"]
    end
    subgraph group2["Consumers"]
        A["Analytics agent query<br/>path"]
        R["Power BI report"]
    end
    subgraph group4["Reconciliation"]
        V["Reviewed test periods"]
    end
    O -->|"Govern units, calendar<br/>and measures"| M
    A -->|"Query named measures as<br/>consumer"| M
    R -->|"Use the same measures<br/>and filters"| M
    V -->|"Check agent results"| A
    V -->|"Compare report results"| R
```

**Review decision:** Approve the business definition of a measure, not just its name. The agent and reference report must reconcile for the same identity, filters and refresh state.

## Technical flow

```mermaid
sequenceDiagram
    accTitle: Share a governed metric contract between agents and reports - technical flow
    autonumber
    participant O as Data owner
    participant M as Model
    participant A as Agent path
    participant R as Reference report
    O->>M: Revise measure definition
    A->>M: Query fixture period with consumer<br/>identity
    M-->>A: Return figures and blanks
    R->>M: Query same period, filters and<br/>identity
    M-->>R: Return figures and blanks
    alt Both outputs match reviewed expectation
      O->>O: Approve measure contract
    else Figures or missing-value behavior differ
      O->>O: Withhold affected comparison and<br/>reconcile definition
    end
```

## Design notes

**Flow:** Data owners publish a semantic model with facts, dimensions, a marked date table and approved measures. Document exact names, business calendar, units and missing-value behavior. Point both the reference report and the query-generating component at that model. When scenario codes change, update model logic rather than teaching every agent a new calculation.

**Choose it when** several analytics consumers repeat the same calculations. A model cannot settle conflicting business definitions; nominate a measure owner first. This pattern prepares the data, whereas the [four Fabric choices](../CATALOG.md#fabric-integration-options) decide who queries it.

**Trust boundary:** Model access and RLS determine visible facts. Do not embed restricted results in a generally shared skill or examples. Compare figures using the same consumer identity, filters and refresh state.

**Failure handling:** Keep fixture periods for normal, missing and zero-denominator cases. When a measure changes, validate the report and agent together; withhold affected comparisons until the owner reconciles them.

**Sources:** [Prepare a semantic model for AI agents](https://learn.microsoft.com/en-us/power-platform/architecture/key-concepts/copilot-studio-fabric/semantic-model-ai-agents) · [Evaluate analytical agents](https://learn.microsoft.com/en-us/power-platform/architecture/key-concepts/copilot-studio-fabric/evaluate-analytical-agents).
