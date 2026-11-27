# Separate bug intake from follow-up correspondence

**Class:** Microsoft solution idea. **Intent:** Turn ordinary product-support email into useful Azure DevOps records while keeping new reports separate from requests for updates.

## Architecture

```mermaid
flowchart TB
    accTitle: Separate bug intake from follow-up correspondence - architecture
    accDescr: A tracking number correlates a reply; it does not authorize access. Keep reporter-supplied observations separate from facts the agent still needs to confirm.
    subgraph group0["Support inbox"]
        U["Reporter"]
        O["Outlook"]
    end
    subgraph group2["Triage service"]
        A["Intake agent"]
        B["Follow-up agent"]
        F["Power Automate and<br/>message mapping"]
    end
    subgraph group5["Engineering"]
        D["Azure DevOps project"]
        K["Product documentation"]
    end
    U -->|"New report or reply"| O
    O -->|"Initial report"| A
    O -->|"Follow-up<br/>correspondence"| B
    A -->|"Resolve product<br/>terminology"| K
    A -->|"Validated report fields"| F
    B -->|"Verified update or<br/>status request"| F
    F -->|"Scoped create or update"| D
```

**Review decision:** A tracking number correlates a reply; it does not authorize access. Keep reporter-supplied observations separate from facts the agent still needs to confirm.

## Technical flow

```mermaid
sequenceDiagram
    accTitle: Separate bug intake from follow-up correspondence - technical flow
    autonumber
    participant U as Reporter
    participant A as Intake or follow-up
    participant F as Case mapping
    participant D as Azure DevOps
    U->>A: Email report or reply
    A->>F: Resolve message and tracking<br/>identifiers
    alt New message with no prior item
        A->>D: Create work item with observed facts
        D-->>A: Return work item ID
        A->>F: Persist message-to-item mapping
        A-->>U: Acknowledge tracking number
    else Authorized reply on existing item
        A->>D: Append supplied facts or read<br/>public-safe status
    else Duplicate delivery or unrelated sender
        A->>A: Do not create a duplicate or<br/>disclose internal details
    end
```

## Components and flow

1. An Outlook-triggered Copilot Studio intake agent extracts the affected product, observed symptom and reporter-provided steps. Consult product documentation for terminology; label inferred context separately and request missing facts rather than inventing observations.
2. A Power Automate action creates the work item in the permitted project. Persist the message-to-item mapping, then acknowledge the item number.
3. A second agent resolves replies against that mapping, validates the reporter, appends relevant changes and returns a customer-safe status. Internal engineering comments do not belong in the reply.

**When to choose it:** Useful for a high-volume shared inbox with predictable fields. A structured intake form is cheaper when the organization controls all submissions. Send sensitive reports to a restricted human intake path.

**Trust boundary:** Treat message bodies and attachments as untrusted evidence. Limit create/update rights to the support project; a work item number is a reference, not proof the sender may read or edit it.

**Failure handling and acceptance:** Deduplicate by message ID and handle an email-send failure separately from work-item creation. Test a forwarded thread from an unrelated sender and two deliveries of the same original email.

**Source:** [Microsoft Learn: Automate software bug reporting with Auto Triage AI Agent](https://learn.microsoft.com/en-us/power-platform/architecture/solution-ideas/auto-ai-triage).
