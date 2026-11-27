# Return a typed result from an agent flow

**Class:** Synthesized technical pattern. **Intent:** Give a conversation one predictable operation assembled from several connector calls, such as validating a request and creating a service case.

## Architecture

```mermaid
flowchart TB
    accTitle: Return a typed result from an agent flow - architecture
    accDescr: Choose whether the response means completed or accepted. Only a system receipt supports completed; long work needs a durable job reference and status lookup.
    subgraph group0["Standard harness"]
        U["User"]
        A["Copilot Studio agent"]
    end
    subgraph group2["Agent flow"]
        F["When an agent calls the<br/>flow"]
        R["Respond to the agent"]
    end
    subgraph group4["Record authority"]
        S["Service case or job<br/>store"]
    end
    U -->|"Request service case"| A
    A -->|"Typed inputs and<br/>request key"| F
    F -->|"Validate access and<br/>persist case or job"| S
    F -->|"Set status and case or<br/>job ID"| R
    R -->|"Real-time typed<br/>response"| A
```

**Review decision:** Choose whether the response means completed or accepted. Only a system receipt supports completed; long work needs a durable job reference and status lookup.

## Technical flow

```mermaid
sequenceDiagram
    accTitle: Return a typed result from an agent flow - technical flow
    autonumber
    participant U as User
    participant A as Agent
    participant F as Agent flow
    participant S as Case or job store
    U->>A: Submit confirmed request
    A->>F: Send fields and stable request key
    F->>S: Check existing request and validate<br/>scope
    alt Case committed within response budget
        S-->>F: Return case receipt
        F-->>A: Respond completed with case ID
    else Longer processing needed
        F->>S: Persist pending job
        F-->>A: Respond accepted with job ID
    else Write result unknown
        F->>S: Reconcile by key before replay
    end
```

## Design notes

**Flow:** On the standard harness, the agent invokes a flow with **When an agent calls the flow**. The flow validates typed inputs, checks the system of record, performs the permitted operation, and uses **Respond to the agent** with a small result such as `status`, `caseId` and `message`. Configure a real-time response; the documented action limit is 100 seconds.

**Choose it when** execution order must be fixed and a result can be returned within the turn. For longer processing, persist a job and respond with an *accepted* receipt, not a completion claim. Run later steps after the response or in a separate worker; provide status lookup.

**Trust boundary:** Inspect the effective connection for each flow action. A user's authenticated conversation does not automatically make every connector call delegated. Revalidate record ownership in the write path.

**Failure handling:** Use a stable request key. If the flow times out after a write, look up the case instead of resubmitting. Test missing inputs, duplicate invocations and a downstream step that takes longer than the response budget.

**Source:** [Create an agent flow as a tool: trigger, response, credentials and limits](https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-flow-create).
