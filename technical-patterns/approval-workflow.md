# Let a workflow own approvals and an agent own the draft

**Class:** Synthesized technical pattern. **Intent:** Use AI for an uncertain input while keeping a predictable, auditable path for a consequential action.

## Architecture

```mermaid
flowchart TB
    accTitle: Let a workflow own approvals and an agent own the draft - architecture
    accDescr: Only a recorded decision for the exact version and amount may release posting. The AI step prepares evidence; it does not select its own approver or authorize the transaction.
    subgraph group0["Intake and drafting"]
        D["Expense case"]
        A["Agent draft"]
    end
    subgraph group2["Process controls"]
        W["Deterministic workflow"]
        H["Authorized reviewer"]
    end
    subgraph group4["Financial system"]
        S["Posting service"]
    end
    D -->|"Case key and version"| W
    W -->|"Request classification<br/>with evidence"| A
    A -->|"Draft reason and source<br/>fields"| W
    W -->|"Request decision from<br/>assigned reviewer"| H
    W -->|"Only post approved<br/>version"| S
    H -->|"Recorded decision"| W
```

**Review decision:** Only a recorded decision for the exact version and amount may release posting. The AI step prepares evidence; it does not select its own approver or authorize the transaction.

## Technical flow

```mermaid
sequenceDiagram
    accTitle: Let a workflow own approvals and an agent own the draft - technical flow
    autonumber
    participant W as Workflow
    participant A as AI step
    participant H as Approver
    participant S as Posting service
    W->>A: Classify exception against source<br/>fields
    A-->>W: Return draft and evidence
    W->>H: Present amount, version and<br/>supporting fields
    alt Approved and case unchanged
        H-->>W: Return recorded approval
        W->>S: Post once against case reference
        S-->>W: Return posting receipt
    else Declined, expired or changed
        W->>W: Hold posting and record reason
    end
```

## Copilot Studio components

**Recommended build ([harness](../COMPONENTS.md#the-harness-is-the-first-decision)):** A Microsoft Copilot harness workflow, or a Standard harness agent flow with a Power Automate approval. On the standard harness, use an agent flow, a prompt tool for the draft and a Power Automate approval.

| Component | Use in this pattern | Harness alternative |
| --- | --- | --- |
| [Workflow](../COMPONENTS.md#workflows): Expense exception workflow | Owns the sequence from intake to posting. | Std: agent flow. |
| [Workflow nodes](../COMPONENTS.md#workflow-nodes): Inline agent node | Proposes a reason category and cites supporting fields. | Std: prompt tool. |
| [Workflow nodes](../COMPONENTS.md#workflow-nodes): Condition and lookup | Validate fields and look up the designated reviewer outside the model. | Std: flow condition and connector. |
| [Human gate](../COMPONENTS.md#human-in-the-loop-gates): Approvals or request-for-information node | Records the reviewer's decision for the exact version and amount. | Std: Power Automate approval. |
| [Connector tool](../COMPONENTS.md#connector-tools): Posting connector | Posts only after a recorded approval. | All harnesses. |

**Not the right component:** Letting the inline agent choose the approver or post the transaction.

**Copilot Credits drivers (medium):** Each workflow action costs 0.13 credits, and the inline agent adds usage-based charges. Its instructions are resent on every turn. Failed runs still pay for completed steps, so validate early. See [Copilot Credits guidance](../COPILOT-CREDITS.md).

## Design notes

**Flow:** A workflow receives an expense exception and records its key. An AI step proposes a reason category and cites supporting fields; the workflow validates those fields and looks up the designated reviewer outside the model. The reviewer sees the proposal and source evidence. Only a recorded approval releases the deterministic posting step. The initiating agent, if any, can report the pending case reference.

**Choose it when** branches and approvals are known in advance. Use Power Automate cloud flows where they already meet the need; consider Copilot Studio workflows when native AI and human-review steps add value. Compare with an [event-driven agent](event-worker.md), where the agent decides the next step at runtime.

**Trust boundary:** The approver must be authorized and distinct from the requester where policy requires. Bind the decision to the exact record version and amount. A chat message saying “approved” or a model classification cannot authorize the post.

**Failure handling:** Expire unanswered approvals and route them to a named owner. If input changes after approval, request a new decision. Test rejection, duplicate callbacks and a posting timeout; retain the receipt separately from the approval.

**Sources:** [Design AI-powered automations](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/ai-powered-automation) · [Microsoft public human-in-the-loop sample](https://github.com/microsoft/CopilotStudioSamples/tree/main/extensibility/human-in-the-loop).
