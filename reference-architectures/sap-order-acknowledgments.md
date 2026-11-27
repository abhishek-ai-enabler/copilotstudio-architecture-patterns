# Match supplier acknowledgments to SAP purchase orders

**Class:** Microsoft reference architecture. **Intent:** Confirm unambiguous supplier acknowledgments automatically, and give procurement staff the exact lines that need a decision.

## Architecture

```mermaid
flowchart TB
    accTitle: Match supplier acknowledgments to SAP purchase orders - architecture
    accDescr: Agree the tolerance rules and which SAP operation can run unattended. A supplier document or an extraction result must never authorize its own exception.
    subgraph group0["Supplier intake"]
        S["Supplier mailbox or EDI"]
        F["Power Automate"]
        D["Dataverse<br/>acknowledgments"]
    end
    subgraph group3["Validation"]
        A["Copilot Studio<br/>orchestrator"]
        E["Extraction agent"]
        M["Matching agent"]
    end
    subgraph group6["Procurement"]
        P["SAP purchase order"]
        H["Procurement specialist<br/>in Teams"]
    end
    S -->|"Incoming acknowledgment"| F
    F -->|"Capture original and<br/>status"| D
    D -->|"Trigger on saved<br/>acknowledgment"| A
    A -->|"Normalize supplier<br/>lines"| E
    A -->|"Read current purchase<br/>order"| P
    A -->|"Compare normalized<br/>lines and SAP data"| M
    A -->|"Confirm only validated<br/>match"| P
    A -->|"Route disputed lines"| H
```

**Review decision:** Agree the tolerance rules and which SAP operation can run unattended. A supplier document or an extraction result must never authorize its own exception.

## Technical flow

```mermaid
sequenceDiagram
    accTitle: Match supplier acknowledgments to SAP purchase orders - technical flow
    autonumber
    participant F as Intake flow
    participant A as Orchestrator
    participant M as Extraction and matching
    participant P as SAP
    participant H as Procurement
    F->>A: Start from stored acknowledgment key
    A->>M: Normalize acknowledgment and return<br/>purchase order ID and lines
    M-->>A: Return extracted fields
    A->>P: Read current purchase order
    P-->>A: Return authoritative lines
    A->>M: Compare lines using approved tolerances
    M-->>A: Return match decision and differences
    alt All lines match
        A->>P: Request confirmation once
        alt SAP acknowledges
            P-->>A: Return confirmation reference
        else Confirmation outcome unknown
            A->>P: Check existing confirmation before<br/>any replay
        end
    else Disputed or unmapped line
        A->>H: Send differences for review, no SAP<br/>write
    end
```

## Copilot Studio components

**Recommended build ([harness](../COMPONENTS.md#the-harness-is-the-first-decision)):** Standard harness: a flow-triggered orchestrator with extraction and matching agents. On the Microsoft Copilot harness, model the process as a workflow: connector trigger, extract node, published-agent node for matching, condition, SAP connector and a human input node for exceptions.

| Component | Use in this pattern | Harness alternative |
| --- | --- | --- |
| [Power Automate flow](../COMPONENTS.md#power-automate-cloud-and-desktop-flows): Mailbox or EDI capture | Stores the original acknowledgment in Dataverse with its status. | Copilot: workflow trigger. |
| [Trigger](../COMPONENTS.md#triggers-and-autonomous-agents): Dataverse-triggered start | Starts the orchestrator autonomously for each new acknowledgment. | Copilot: workflow trigger and agent node, or agent trigger (preview). |
| [Child agent](../COMPONENTS.md#child-agents-and-sub-agents): Extraction and matching agents | Normalize lines and compare them with the purchase order under tolerance rules. | Copilot: workflow extract node and agent node. |
| [Connector tool](../COMPONENTS.md#connector-tools): SAP connector | Reads the purchase order and runs the confirmation operation only after checks pass. | All harnesses. |
| [Agent flow](../COMPONENTS.md#agent-flows): Confirmation and exception flow | Confirms in SAP or creates a Dataverse exception. | Copilot: workflow. |
| [Human gate](../COMPONENTS.md#human-in-the-loop-gates): Teams notification to a procurement specialist | Presents mismatched values with a source link. | Copilot: approvals or request-for-information node. |

**Not the right component:** Letting the extracted document or the extraction agent authorize an exception.

**Copilot Credits drivers (high):** Autonomous runs are billed even when staff hold Microsoft 365 Copilot licenses. Each acknowledgment incurs a trigger (agent action), extraction (content processing at 8 per page, or prompt usage), agent hops and agent flow actions. Deduplicate before triggering and route only unclear lines to AI. See [Copilot Credits guidance](../COPILOT-CREDITS.md).

## Components and flow

1. A Power Automate flow captures a mailbox or EDI acknowledgment in Dataverse. Keep the original, its supplier reference and processing status together.
2. A Dataverse-triggered flow starts the Copilot Studio orchestrator. An extraction agent normalizes line identifiers, quantities, units, prices and dates. The orchestrator reads the current purchase order from SAP; a matching agent compares corresponding lines using procurement's tolerance rules.
3. Permit the SAP confirmation operation only after required fields and tolerance checks pass. Otherwise create an exception in Dataverse and notify the responsible specialist in Teams with the mismatched values and a link to the source.

**When to choose it:** Useful for high document volume and stable purchasing rules. For one structured EDI format, a deterministic integration may suffice. Keep supplier-specific extraction separate from centrally owned purchasing rules.

**Trust boundary:** Supplier documents are data, not authority to change prices or tolerances. Separate SAP read and confirmation privileges where practical. Record the rule version and acting integration or reviewer on each outcome.

**Failure handling and acceptance:** Quarantine ambiguous line mappings, missing units and changed purchase orders. On an uncertain SAP response, look up confirmation state before replay. Test an exact match, an out-of-tolerance line and delivery of the same acknowledgment twice; only one SAP confirmation should result.

**Source:** [Microsoft Learn: Automate procurement order acknowledgment matching with Copilot Studio and SAP](https://learn.microsoft.com/en-us/power-platform/architecture/reference-architectures/order-acknowledgment-validation).
