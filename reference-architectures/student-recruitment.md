# Link recruitment conversations and touchpoints to enrollment

**Class:** Microsoft reference architecture. **Intent:** Help recruiters follow up on expressed interests and measure which outreach leads to enrollment, even when a student changes email address.

## Architecture

```mermaid
flowchart TB
    accTitle: Link recruitment conversations and touchpoints to enrollment - architecture
    accDescr: Decide who can link contact addresses to a person and who can see individual touchpoints. Aggregate campaign attribution is not an admissions decision.
    subgraph group0["Ingestion"]
        S["Student information<br/>system"]
        T["Forms and event<br/>registrations"]
    end
    subgraph group2["Recruitment data"]
        D["Dataverse people and<br/>touchpoints"]
        J["Customer Insights -<br/>Journeys"]
    end
    subgraph group4["Staff and reporting"]
        A["Copilot Studio staff<br/>agent"]
        U["Recruiter"]
        R["Power BI funnel"]
    end
    S -->|"Scheduled enrollment<br/>dataflow"| D
    T -->|"Timestamped engagement<br/>via flows"| D
    U -->|"Request follow-up draft"| A
    A -->|"Read permitted contact<br/>history"| D
    D -->|"Consented outreach<br/>audience"| J
    D -->|"Aggregate touchpoints<br/>and enrollments"| R
    A -->|"Draft for recruiter<br/>review"| U
```

**Review decision:** Decide who can link contact addresses to a person and who can see individual touchpoints. Aggregate campaign attribution is not an admissions decision.

## Technical flow

```mermaid
sequenceDiagram
    accTitle: Link recruitment conversations and touchpoints to enrollment - technical flow
    autonumber
    participant S as Student system
    participant D as Dataverse intake
    participant H as Recruitment steward
    participant J as Journeys
    S->>D: Import enrollment and contact<br/>identifiers
    alt Match is unambiguous
        D->>D: Link enrollment to one person
        opt Current consent permits outreach
            D->>J: Supply eligible contact and program
        end
    else Personal and institutional addresses conflict
        D->>H: Request identity review
        H->>D: Resolve before counting or<br/>contacting
    end
```

## Components and flow

1. Scheduled dataflows import programs and enrollments from the student information system. In Dataverse, distinguish a person from their contact addresses, and a promoted program from the academic programs it represents.
2. Registration forms, events and imports create dated recruitment touchpoints. Customer Insights - Journeys uses these records for consented outreach. A Copilot Studio agent can summarize authorized activity for a recruiter and draft a follow-up.
3. Compare touchpoints and enrollments by program and period in Power BI. State the attribution rule: attendance before enrollment is an association, not proof the event caused enrollment.

**When to choose it:** Valuable when recruitment and enrollment live in different systems. For simple event registration, the cost of reconciling identities and maintaining program mappings may exceed the benefit.

**Trust boundary:** Separate staff access to individual histories from aggregate reporting and public program information. Verify consent for the specific channel before sending a draft. Do not use engagement data to make an admissions decision.

**Failure handling and acceptance:** Hold ambiguous identity matches for a steward. Deduplicate reimported attendance records and show the last enrollment refresh date. Test a student with personal and institutional addresses: their enrollment should count once and an opted-out address must not receive outreach.

**Source:** [Microsoft Learn: Build a student recruitment solution with Power Platform](https://learn.microsoft.com/en-us/power-platform/architecture/reference-architectures/student-recruitment-solution).
