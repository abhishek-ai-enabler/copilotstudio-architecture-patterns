# Fabric 1: Publish a Fabric data agent directly

**Class:** Microsoft decision-guide pattern (Fabric option 1 of 4). **Intent:** Establish the simplest baseline for asking questions of a semantic model. **No Copilot Studio agent is in the request path.**

**Flow:** User in a supported Microsoft Copilot or Teams experience → published Fabric data agent → semantic model → answer. The Fabric data agent interprets the request, constructs the query and presents the result. Give it business terms and known examples; leave measure definitions in the model.

**Choose it when** an analyst needs a figure or small table and the data team owns the experience. It also isolates the data layer for comparison with the other three options. Don't add a second agent unless you need more control over the conversation or answer format. The direct option offers less control over a fixed narrative.

**Trust boundary:** Sharing the agent and granting access to the underlying data are distinct decisions. Verify Fabric capacity, tenant settings and permissions for the actual channel. Test with two users permitted to see different regions.

**Failure handling:** Compare the answer to a report using identical filters. If this path returns the wrong period or measure, fix the model or the data agent before adding orchestration. A known missing measure should result in no figure, not an estimate.

**Sources:** [Microsoft Fabric architecture choice: pattern 1](https://learn.microsoft.com/en-us/power-platform/architecture/key-concepts/copilot-studio-fabric/#pattern-1-fabric-data-agent-published-directly) · [Fabric data agent prerequisites and execution](https://learn.microsoft.com/en-us/fabric/data-science/concept-data-agent).
