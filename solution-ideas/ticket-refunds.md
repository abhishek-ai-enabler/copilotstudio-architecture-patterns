# Assisted and email-driven refunds on a shared legacy workflow

**Class:** Microsoft solution idea. **Intent:** Give guest-services staff a Teams entry point and process eligible email requests without duplicating integrations to a ticketing system that lacks a suitable API.

## Architecture

```mermaid
flowchart TB
    accTitle: Assisted and email-driven refunds on a shared legacy workflow - architecture
    accDescr: Both agents must share one refund identity check and one case key. An uncertain desktop result must be reconciled in the ledger before another payment attempt.
    subgraph group0["Entry paths"]
        T["Employee in Teams"]
        E["Outlook email trigger"]
    end
    subgraph group2["Case processing"]
        A["Assisted or autonomous<br/>agent"]
        D["Dataverse refund cases"]
        F["Shared cloud flow"]
    end
    subgraph group5["Legacy finance"]
        R["Desktop flow on managed<br/>VM"]
        L["Legacy ticket ledger"]
        H["Refund reviewer"]
    end
    T -->|"Staff request"| A
    E -->|"Untrusted email request"| A
    A -->|"Locate or create refund<br/>case"| D
    D -->|"Case ready for<br/>validation"| F
    F -->|"Exception or approval<br/>required"| H
    F -->|"Authorized refund only"| R
    R -->|"Post and obtain receipt"| L
```

**Review decision:** Both agents must share one refund identity check and one case key. An uncertain desktop result must be reconciled in the ledger before another payment attempt.

## Technical flow

```mermaid
sequenceDiagram
    accTitle: Assisted and email-driven refunds on a shared legacy workflow - technical flow
    autonumber
    participant A as Intake agent
    participant F as Shared flow
    participant H as Reviewer
    participant R as Desktop worker
    participant L as Legacy ledger
    A->>F: Submit ticket and case key
    F->>F: Verify eligibility and existing<br/>outcome
    opt Exception requires approval
        F->>H: Request review of specific refund
        H-->>F: Return recorded decision
    end
    alt Approved and not previously paid
        F->>R: Issue refund
        R->>L: Submit to ticket system
        alt Receipt available
            L-->>R: Return refund reference
            R-->>F: Record confirmed payout
        else Desktop disconnected
            F->>L: Reconcile prior submission before<br/>retry
        end
    else Ineligible, declined or already paid
        F-->>A: Return existing status without a<br/>payout
    end
```

## Components and flow

1. The assisted agent gathers a request from an employee; the autonomous agent receives an Outlook event. Normalize both into the same Dataverse refund case, retaining origin, ticket reference and status.
2. A shared Power Automate cloud flow validates the request against the sale and refund policy. Send ambiguous, high-value or unauthorized cases to a reviewer. An email requests work; it does not approve payment.
3. A desktop flow on a managed VM performs the permitted legacy operation. Record the legacy transaction receipt on the case before either channel tells the requester the refund completed.

**When to choose it:** A practical bridge where only a legacy UI can issue the refund. Prefer an API when one exists: screen changes, desktop sessions and unattended licensing add ongoing cost.

**Trust boundary:** Separate mailbox access from refund authority. Restrict the robot identity and protect credentials (the reference uses Azure Key Vault). Confirm ownership and eligibility in the backend, irrespective of entry channel.

**Failure handling and acceptance:** If the desktop disconnects after submission, mark the outcome unknown and reconcile with the ledger before replay. Test one refund arriving through both email and Teams; there must be a single payout.

**Source:** [Microsoft Learn: Ticket management system with Copilot Studio agents](https://learn.microsoft.com/en-us/power-platform/architecture/solution-ideas/agent-ticket-and-refund).
