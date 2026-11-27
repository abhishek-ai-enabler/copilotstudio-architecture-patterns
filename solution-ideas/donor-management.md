# Donor inquiry intake, approvals and finance reconciliation

**Class:** Microsoft solution idea. **Intent:** Give fundraising staff a traceable route from email or a donation form to the appropriate follow-up, approval and finance record.

## Architecture

```mermaid
flowchart TB
    accTitle: Donor inquiry intake, approvals and finance reconciliation - architecture
    accDescr: Approve the fundraising-to-finance handoff only when the reviewed amount and decision are traceable to the original form. A draft consent flag is not outreach authorization.
    subgraph group0["Inbound materials"]
        O["Outlook or document<br/>upload"]
    end
    subgraph group1["Donor operations"]
        D["Dataverse donor case"]
        X["AI Builder"]
        A["Copilot Studio and<br/>staff app"]
    end
    subgraph group4["Financial authority"]
        F["Power Automate approval"]
        H["Authorized reviewer"]
        S["SAP Finance"]
    end
    O -->|"Capture message and<br/>source"| D
    D -->|"Extract draft fields"| X
    X -->|"Proposed amount and<br/>donor reference"| A
    A -->|"Record checked values"| D
    D -->|"Submit case version for<br/>approval"| F
    F -->|"Request financial<br/>decision"| H
    F -->|"Post approved amount"| S
```

**Review decision:** Approve the fundraising-to-finance handoff only when the reviewed amount and decision are traceable to the original form. A draft consent flag is not outreach authorization.

## Technical flow

```mermaid
sequenceDiagram
    accTitle: Donor inquiry intake, approvals and finance reconciliation - technical flow
    autonumber
    participant D as Donor case
    participant A as Engagement agent
    participant H as Reviewer
    participant F as Approval flow
    participant S as Finance
    D->>A: Supply draft fields and source<br/>reference
    A->>F: Submit checked proposal for review
    F->>H: Request approval for this donation<br/>and amount
    alt Reviewer approves
        H-->>F: Record decision
        F->>S: Post with donation reference
        S-->>F: Return receipt for case
    else Missing evidence or declined
        F->>D: Record hold or decline without<br/>posting
    end
```

## Components and flow

1. Ingest permitted Outlook messages and SharePoint or OneDrive documents into a Dataverse case. AI Builder extracts draft fields such as amount and donor reference; retain a link to the source for review.
2. The Copilot Studio engagement agent proposes a follow-up task or requests clarification. Staff inspect the case in a model-driven app. A consent flag extracted from a form must be checked against the actual authorization before outreach.
3. A Power Automate approval routes financial changes to an authorized reviewer. After approval, an integration may reconcile with SAP Finance. Record the finance receipt and communicate only the appropriate status in Teams.

**When to choose it:** Valuable when document-heavy donations cross fundraising and finance teams. A structured donation form can avoid extraction entirely. Sentiment can flag a message for review; it should not determine donor treatment.

**Trust boundary:** Separate fundraiser, approver and finance privileges. Keep donor details out of broad channels; use a link to the access-controlled case.

**Failure handling and acceptance:** Missing consent, conflicting amounts or an unidentified donor require a person. If finance times out, reconcile using the donation reference rather than initiating another posting. Test a duplicate form and an approval declined after extraction.

**Source:** [Microsoft Learn: AI-enabled donor management solution](https://learn.microsoft.com/en-us/power-platform/architecture/solution-ideas/agent-donor-management).
