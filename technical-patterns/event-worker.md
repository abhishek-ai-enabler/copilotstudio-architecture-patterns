# Start a bounded agent task from a business event

**Class:** Synthesized technical pattern. **Intent:** Act on a new business record without waiting for someone to open a chat.

**Flow:** A configured connector event sends a payload to a published agent with generative orchestration. For example, on creation of a new equipment request, use the record key to retrieve current state, classify the request and propose the responsible queue. Persist event ID, processing status and outcome; a deterministic worker should handle any committed routing change.

**Choose it when** the event is known but the appropriate next step depends on the record. Use a simple flow without an agent if a field-to-queue mapping suffices. Filter events upstream and budget for burst traffic and credit consumption.

**Trust boundary:** The documented event triggers use maker credentials, not the event sender's delegated identity. Scope the configured connections; verify the originating record and permitted actions. A message body in the event is untrusted data, not instructions from an administrator.

**Failure handling:** Deduplicate on event and record version. Avoid retriggering on the agent's own status update. Isolate failed records for review, and reconcile state before replay. Test duplicate, out-of-order and unauthorized events, including when no interactive user is present.

**Source:** [Event trigger overview, billing and publishing behavior](https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-triggers-about).
