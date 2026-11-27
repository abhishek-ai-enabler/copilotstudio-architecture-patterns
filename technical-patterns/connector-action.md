# Expose a narrow business operation through a connector

**Class:** Synthesized technical pattern. **Intent:** Let an agent use a business API through a reusable operation rather than inventing arbitrary requests.

**Flow:** Start with a supported prebuilt Power Platform connector. If none meets the need, define a custom connector around an owned REST API. Expose a specific operation such as “read shipment status,” with required identifiers, a bounded response and a description distinct from “request shipment change.” Return the system's status and timestamp, not its full raw object.

**Choose it when** several agents or flows need a stable service contract. A custom connector requires someone to own API versioning and authentication. A [direct REST tool](direct-rest-tool.md) may suit a one-agent prototype; [MCP](mcp-tools.md) may suit a centrally changing catalog.

**Trust boundary:** Configure which identity the connection uses. Validate record access, fields and business rules at the service. Put endpoint selection under maker/admin control, not a user-provided URL.

**Failure handling:** Map not found, permission denied and temporarily unavailable to distinct safe outcomes. Respect throttling; replay writes only with an idempotency key and reconciliation. Test that a status question cannot accidentally call the change operation.

**Source:** [Plan and design integration strategies for Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/integrations).
