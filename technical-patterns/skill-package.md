# Package reusable procedures as skills

**Class:** Synthesized technical pattern. **Intent:** Share a bounded procedure, such as formatting a service review, without duplicating long instructions or operating a separate agent.

## Architecture

```mermaid
flowchart TB
    accTitle: Package reusable procedures as skills - architecture
    accDescr: Approve a skill as reusable procedure, not as a credential bundle. Its instructions cannot grant the consuming agent access to the data needed to execute it.
    subgraph group0["Package ownership"]
        O["Procedure owner"]
        S["Reviewed versioned<br/>skill"]
    end
    subgraph group2["Consuming agent"]
        A["Microsoft Copilot<br/>harness"]
        T["Authorized report tool"]
    end
    subgraph group4["Data authority"]
        R["Service review records"]
    end
    O -->|"Version procedure and<br/>examples"| S
    A -->|"Load only for matching<br/>task"| S
    A -->|"Request report data"| T
    T -->|"Check caller and record<br/>scope"| R
    T -->|"Authorized source<br/>fields"| A
```

**Review decision:** Approve a skill as reusable procedure, not as a credential bundle. Its instructions cannot grant the consuming agent access to the data needed to execute it.

## Technical flow

```mermaid
sequenceDiagram
    accTitle: Package reusable procedures as skills - technical flow
    autonumber
    participant U as Reviewer
    participant A as Agent
    participant S as Skill
    participant T as Report tool
    U->>A: Draft a service review
    A->>S: Load matching procedure
    S-->>A: Return procedure and examples
    A->>T: Read authorized reporting data
    alt Required data and tool are available
      T-->>A: Return source fields
      A-->>U: Format review for human sign-off
    else Tool missing or access denied
      A-->>U: Identify unavailable input rather<br/>than inventing it
    end
```

## Design notes

**Flow:** On the Microsoft Copilot harness, keep global behavior in the agent instructions. Package task-specific guidance and vetted resources as a named skill with a precise description. When the request matches, the agent loads the procedure and uses its available tools. Version the skill and check its result against a representative service review.

**Choose it when** several agents perform the same procedure with their own authorized data. A skill describes *how*; use a tool for an external action, a knowledge source for changing policy facts, and a workflow for a mandatory execution order. These instruction-based skills are not the Azure Bot Service skills used by some handoff bridges.

**Trust boundary:** Review packages and any scripts as supply-chain inputs. Do not package credentials, production records or implied permission grants. The consuming agent still needs its own authorized tool connections.

**Failure handling:** Detect missing tools and incompatible versions before rollout. Test an unrelated request that must not load this skill, as well as a matching request with no access to the report. Keep a known-good package to restore through the normal release process.

**Source:** [Skills overview for agents on the Microsoft Copilot harness](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-overview).
