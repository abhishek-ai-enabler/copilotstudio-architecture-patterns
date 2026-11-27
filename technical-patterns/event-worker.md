# Start a bounded agent task from a business event

**Class:** Synthesized technical pattern. **Intent:** Act on a new business record without waiting for someone to open a chat.

## Architecture

```mermaid
flowchart TB
    accTitle: Start a bounded agent task from a business event - architecture
    accDescr: Approve the trigger identity and retry policy before enabling autonomous work. Event contents supply data; they do not represent a signed-in user's delegated authority.
    subgraph group0["Event source"]
        E["Equipment request event"]
    end
    subgraph group1["Published agent"]
        T["Maker-authenticated<br/>connector trigger"]
        A["Generative<br/>orchestration"]
    end
    subgraph group3["Controlled execution"]
        D["Request state and event<br/>history"]
        W["Deterministic routing<br/>worker"]
    end
    E -->|"Event and record<br/>identifiers"| T
    T -->|"Start autonomous task"| A
    A -->|"Read current version<br/>and prior outcome"| D
    A -->|"Proposed route for<br/>validated event"| W
    W -->|"Commit authorized<br/>routing and receipt"| D
```

**Review decision:** Approve the trigger identity and retry policy before enabling autonomous work. Event contents supply data; they do not represent a signed-in user's delegated authority.

## Technical flow

```mermaid
sequenceDiagram
    accTitle: Start a bounded agent task from a business event - technical flow
    autonumber
    participant E as Event source
    participant A as Agent worker
    participant D as State store
    participant W as Routing worker
    E->>A: Deliver event ID and record version
    A->>D: Check prior delivery and current<br/>record
    alt Fresh permitted record
        A->>W: Propose responsible queue
        W->>D: Validate and persist routing outcome
    else Duplicate, stale or self-triggered event
        A->>D: Record skipped outcome without<br/>another write to source
    else Processing failed
        A->>D: Mark for review and reconciliation
    end
```

## Design notes

**Flow:** A configured connector event sends a payload to a published agent with generative orchestration. For example, on creation of a new equipment request, use the record key to retrieve current state, classify the request and propose the responsible queue. Persist event ID, processing status and outcome; a deterministic worker should handle any committed routing change.

**Choose it when** the event is known but the appropriate next step depends on the record. Use a simple flow without an agent if a field-to-queue mapping suffices. Filter events upstream and budget for burst traffic and credit consumption.

**Trust boundary:** The documented event triggers use maker credentials, not the event sender's delegated identity. Scope the configured connections; verify the originating record and permitted actions. A message body in the event is untrusted data, not instructions from an administrator.

**Failure handling:** Deduplicate on event and record version. Avoid retriggering on the agent's own status update. Isolate failed records for review, and reconcile state before replay. Test duplicate, out-of-order and unauthorized events, including when no interactive user is present.

**Source:** [Event trigger overview, billing and publishing behavior](https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-triggers-about).
