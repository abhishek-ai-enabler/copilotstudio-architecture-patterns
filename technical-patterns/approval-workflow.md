# Let a workflow own approvals and an agent own the draft

**Class:** Synthesized technical pattern. **Intent:** Use AI for an uncertain input while keeping a predictable, auditable path for a consequential action.

**Flow:** A workflow receives an expense exception and records its key. An AI step proposes a reason category and cites supporting fields; the workflow validates those fields and looks up the designated reviewer outside the model. The reviewer sees the proposal and source evidence. Only a recorded approval releases the deterministic posting step. The initiating agent, if any, can report the pending case reference.

**Choose it when** branches and approvals are known in advance. Use Power Automate cloud flows where they already meet the need; consider Copilot Studio workflows when native AI and human-review steps add value. Compare with an [event-driven agent](event-worker.md), where the agent decides the next step at runtime.

**Trust boundary:** The approver must be authorized and distinct from the requester where policy requires. Bind the decision to the exact record version and amount. A chat message saying “approved” or a model classification cannot authorize the post.

**Failure handling:** Expire unanswered approvals and route them to a named owner. If input changes after approval, request a new decision. Test rejection, duplicate callbacks and a posting timeout; retain the receipt separately from the approval.

**Sources:** [Design AI-powered automations](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/ai-powered-automation) · [Microsoft public human-in-the-loop sample](https://github.com/microsoft/CopilotStudioSamples/tree/main/extensibility/human-in-the-loop).
