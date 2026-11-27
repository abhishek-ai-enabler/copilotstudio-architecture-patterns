# Match supplier acknowledgments to SAP purchase orders

**Class:** Microsoft reference architecture. **Intent:** Confirm unambiguous supplier acknowledgments automatically, and give procurement staff the exact lines that need a decision.

## Components and flow

1. A Power Automate flow captures a mailbox or EDI acknowledgment in Dataverse. Keep the original, its supplier reference and processing status together.
2. A Dataverse-triggered flow starts the Copilot Studio orchestrator. An extraction agent normalizes line identifiers, quantities, units, prices and dates. The orchestrator reads the current purchase order from SAP; a matching agent compares corresponding lines using procurement's tolerance rules.
3. Permit the SAP confirmation operation only after required fields and tolerance checks pass. Otherwise create an exception in Dataverse and notify the responsible specialist in Teams with the mismatched values and a link to the source.

**When to choose it:** Useful for high document volume and stable purchasing rules. For one structured EDI format, a deterministic integration may suffice. Keep supplier-specific extraction separate from centrally owned purchasing rules.

**Trust boundary:** Supplier documents are data, not authority to change prices or tolerances. Separate SAP read and confirmation privileges where practical. Record the rule version and acting integration or reviewer on each outcome.

**Failure handling and acceptance:** Quarantine ambiguous line mappings, missing units and changed purchase orders. On an uncertain SAP response, look up confirmation state before replay. Test an exact match, an out-of-tolerance line and delivery of the same acknowledgment twice; only one SAP confirmation should result.

**Source:** [Microsoft Learn: Automate procurement order acknowledgment matching with Copilot Studio and SAP](https://learn.microsoft.com/en-us/power-platform/architecture/reference-architectures/order-acknowledgment-validation).
