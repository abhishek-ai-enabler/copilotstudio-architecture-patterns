# Preview and migrate an organizer's meetings in place

**Class:** Microsoft reference architecture. **Intent:** Move conferencing details to Teams without making employees recreate their invitations or giving a migration operator standing access to every calendar.

## Architecture

```mermaid
flowchart TB
    accTitle: Preview and migrate an organizer's meetings in place - architecture
    accDescr: Approval is per organizer, meeting and previewed version. A timeout is a reason to check the original event, not to create a replacement invitation.
    subgraph group0["Organizer channel"]
        U["Organizer in Teams"]
        A["Copilot Studio"]
    end
    subgraph group2["Migration automation"]
        F["Power Automate"]
        D["Dataverse migration<br/>history"]
    end
    subgraph group4["Calendar authorities"]
        L["Legacy conferencing<br/>system"]
        G["Microsoft Graph<br/>calendar and meetings"]
    end
    U -->|"Select and confirm<br/>preview"| A
    A -->|"Delegate approved scope"| F
    F -->|"Read source meeting<br/>details"| L
    F -->|"Convert eligible event<br/>in place"| G
    F -->|"Record outcome per<br/>event"| D
    D -->|"Progress and unresolved<br/>items"| A
    A -->|"Preview, progress and<br/>exceptions"| U
```

**Review decision:** Approval is per organizer, meeting and previewed version. A timeout is a reason to check the original event, not to create a replacement invitation.

## Technical flow

```mermaid
sequenceDiagram
    accTitle: Preview and migrate an organizer's meetings in place - technical flow
    autonumber
    participant U as Organizer
    participant A as Agent
    participant F as Migration flow
    participant G as Calendar via Graph
    participant D as Migration history
    U->>A: Preview my eligible meetings
    A->>F: Collect organizer's scoped events
    F-->>A: Return preview and versions
    A-->>U: Display attendees, rooms and<br/>recurrence
    U->>A: Confirm selected meetings
    A->>F: Submit selected IDs and versions
    loop For each selected meeting
      alt Eligible and unchanged
        F->>G: Update existing event
        alt Conversion confirmed
          G-->>F: Return authoritative event state
        else Update response times out
          F->>G: Read existing event before retrying
        end
      else Changed since preview
        F->>F: Skip and require a new preview
      end
      F->>D: Record outcome for this event
    end
    F-->>A: Return migrated, skipped and<br/>unresolved meetings
    A-->>U: Show per-meeting outcome
```

## Copilot Studio components

**Recommended build ([harness](../COMPONENTS.md#the-harness-is-the-first-decision)):** Standard harness in Teams, with agent flows for Microsoft Graph calendar operations. On the Microsoft Copilot harness, the migration becomes a workflow with a request-for-information or approval node for the organizer's selection.

| Component | Use in this pattern | Harness alternative |
| --- | --- | --- |
| [Authentication](../COMPONENTS.md#authentication-and-tool-credentials): Entra ID sign-in, delegated connections | Limit the inspection to the signed-in organizer's own meetings. | All harnesses. |
| [Topics](../COMPONENTS.md#topics-and-system-topics): Preview and confirm topic | Shows proposed changes and collects the organizer's selection. | Copilot: workflow human input node. |
| [Topic nodes](../COMPONENTS.md#topic-nodes): Adaptive card, Question, Condition | Present recurring series and rooms, then confirm per event. | Copilot: Adaptive Card node. |
| [Agent flow](../COMPONENTS.md#agent-flows): Migration flow | Converts supported events in place through Microsoft Graph and records per-event status. | Copilot: workflow with connector actions. |
| [Variables](../COMPONENTS.md#variables-and-conversation-state): Selection and event identifiers | Track the exact events and versions approved. | Copilot: workflow variables. |

**Not the right component:** Cancel-and-reinvite automation, or an operator connection with standing access to every calendar.

**Copilot Credits drivers (medium):** Agent flow actions scale with the number of meetings (13 per 100 actions). They are included when a licensed Microsoft 365 Copilot organizer starts the flow interactively through **When an agent calls the flow**. Unlicensed organizers and any scheduled batch runs are billed. See [Copilot Credits guidance](../COPILOT-CREDITS.md).

## Components and flow

1. An organizer signs into the Copilot Studio agent in Teams. Delegated access lets the migration automation inspect eligible meetings. Show the proposed changes, including recurring series and room bookings, before requesting a selection.
2. On confirmation, Power Automate reads the source details and uses calendar/meeting operations through Microsoft Graph to convert supported events in place. Track the existing event identifier rather than canceling and reinviting by default.
3. Record per-event status and reason in Dataverse. Return separate lists for converted, skipped and unresolved events; Power BI can report aggregate progress without publishing attendee lists.

**When to choose it:** Suitable where the source calendar and its event types support a tested in-place conversion. Prove that attendee lists, series exceptions, invitations and room reservations survive. Route unsupported meeting types to manual migration.

**Trust boundary:** Authorization comes from the signed-in organizer's delegated permissions, not possession of an event ID. A preview is not perpetual consent: check whether the event changed before applying it.

**Failure handling and acceptance:** Re-read an event after a timeout; never create a second invite to “fix” an unknown outcome. Retry only unconverted eligible events. Test a partial batch and verify the employee can see precisely what still needs attention.

**Source:** [Microsoft Learn: Migrate legacy meetings to Microsoft Teams with a conversational agent](https://learn.microsoft.com/en-us/power-platform/architecture/reference-architectures/migrate-legacy-meetings).
