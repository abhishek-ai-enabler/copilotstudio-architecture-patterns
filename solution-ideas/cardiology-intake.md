# Clinician-reviewed cardiology intake and scheduling

**Class:** Microsoft solution idea, adapted with a mandatory clinician review. **Intent:** Coordinate intake paperwork, assignment and scheduling; the agent neither decides urgency nor gives clinical advice.

## Architecture

```mermaid
flowchart TB
    accTitle: Clinician-reviewed cardiology intake and scheduling - architecture
    accDescr: Approve scheduling only on a recorded clinician decision for the verified case. A completed upload or successful extraction must never release the booking step.
    subgraph group0["Registration"]
        U["Front desk and patient"]
        A["Copilot Studio intake"]
        P["Power Apps upload"]
    end
    subgraph group3["Restricted review"]
        D["Dataverse case and<br/>originals"]
        X["AI Builder draft"]
        H["Qualified clinician"]
    end
    subgraph group6["Scheduling"]
        F["Power Automate"]
        B["Bookings and Outlook"]
    end
    U -->|"Open case"| A
    U -->|"Submit document"| P
    A -->|"Register verified case"| D
    P -->|"Attach original"| D
    D -->|"Prepare optional draft<br/>fields"| X
    X -->|"Draft for verification<br/>against original"| H
    D -->|"Case in staffed review<br/>queue"| H
    H -->|"Recorded scheduling<br/>authorization"| F
    F -->|"Book authorized<br/>appointment"| B
    F -->|"Booking reference to<br/>front desk"| U
```

**Review decision:** Approve scheduling only on a recorded clinician decision for the verified case. A completed upload or successful extraction must never release the booking step.

## Technical flow

```mermaid
sequenceDiagram
    accTitle: Clinician-reviewed cardiology intake and scheduling - technical flow
    autonumber
    participant U as Intake staff
    participant D as Case queue
    participant H as Clinician
    participant F as Scheduling
    participant B as Bookings
    U->>D: Attach paperwork to verified case
    D->>H: Assign case with original and<br/>optional draft
    alt Clinician records scheduling authorization
      H->>F: Release administrative scheduling<br/>request
      F->>B: Reserve authorized appointment
      B-->>F: Return booking reference
      F-->>U: Notify intake staff to confirm with<br/>patient
    else Review incomplete or identity uncertain
      H->>D: Record follow-up needed, no booking
      D-->>U: Route case to staffed follow-up
    end
```

## Components and flow

1. A front-desk Copilot Studio agent opens a Dataverse case. Staff or a patient submits documents through an approved Power Apps intake experience. Keep the original tied to the verified case.
2. AI Builder may prepare draft extracted fields. A Power Automate event puts the case, original document and draft in a restricted clinical review queue. A qualified clinician verifies the record and makes the disposition through the organization's established process.
3. Only a recorded, authorized scheduling instruction can start the Bookings/Outlook step. Send the patient a minimal administrative confirmation through the approved contact channel.

**When to choose it:** Useful when handoffs between registration, review and scheduling are the bottleneck. Do not substitute an automated queue for staffed clinical coverage or an emergency pathway. Extraction is optional if it slows review.

**Trust boundary:** Separate registration, reviewing clinician and scheduling roles. A scheduling worker needs the authorized appointment request, not the full report. Never send an unreviewed interpretation to a patient.

**Failure handling and acceptance:** Unreadable uploads, uncertain identity or missing approval remain assigned to staff; none imply a reassuring outcome. Monitor unacknowledged cases under the provider's existing fallback process. Test that a complete upload without clinician authorization cannot book, close or notify a clinical result.

**Source:** [Microsoft Learn: Intelligent cardiac triage and scheduling with Power Platform](https://learn.microsoft.com/en-us/power-platform/architecture/solution-ideas/cardio-triage-agent). This adaptation covers service orchestration only.
