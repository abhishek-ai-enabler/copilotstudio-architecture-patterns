# Copilot Studio architecture patterns

Use this catalog to design a Microsoft Copilot Studio agent and explain the design at architecture review. Its **49 entries** cover decisions such as when a topic is enough, when to delegate to a specialist agent, and which steps a workflow or a person must control. These are illustrated design notes, not deployable templates. No tenant access is needed to read them.

**[Browse all 49 entries](CATALOG.md)** · **[Compare Copilot Studio components](COMPONENTS.md#pattern-component-matrix)** · **[Estimate Copilot Credits](COPILOT-CREDITS.md#5-estimate-measure-then-multiply)**

## Start with the decision you need to make

| If you need to… | Start here | Decision to take away |
| --- | --- | --- |
| Answer questions over Fabric or Power BI | [Four Fabric integration options](CATALOG.md#fabric-integration-options) | Should a Fabric data agent write the query, or should Copilot Studio query the semantic model through the Power BI connector? |
| Build an employee assistant | [HR specialists](reference-architectures/hr-specialists.md) and [SharePoint grounding](technical-patterns/sharepoint-grounding.md) | Which questions need a cited policy answer, and which need a tool authorized to read or change the employee's record? |
| Transfer a customer to a representative | [Hub-owned handoff](decision-patterns/hub-front-handoff.md) vs. [agent-owned handoff](decision-patterns/bot-front-handoff.md) | Who owns the live session, and how does the customer know whether the queue accepted the transfer? |
| Automate a transaction that needs approval | [Workflow-owned approval](technical-patterns/approval-workflow.md) | What may the agent draft, and whose recorded decision releases the write? |
| Decide whether an agent is ready for production | [Evaluation gate](technical-patterns/evaluation-gate.md) and [operational monitoring](technical-patterns/operational-monitoring.md) | What evidence shows that the task succeeded in the business system, not just that the agent replied? |

## Worked example: reviewing an SAP order acknowledgment

1. **Architect:** Open the [architecture diagram](reference-architectures/sap-order-acknowledgments.md#architecture). Agree with procurement on which differences can be accepted automatically and which must go to a specialist. The supplier document provides evidence; it does not set the tolerance.
2. **Developer:** Follow the [technical flow](reference-architectures/sap-order-acknowledgments.md#technical-flow) and [component mapping](reference-architectures/sap-order-acknowledgments.md#copilot-studio-components). A Dataverse-triggered cloud flow starts the agent. The agent extracts and compares the lines; SAP supplies the authoritative order and the confirmation receipt.
3. **Reviewer:** Ask what happens if SAP accepts the write but its reply never arrives. The design records a pending outcome and looks up the existing confirmation before any replay. That gives the team a concrete acceptance test: delivering the same acknowledgment twice must not confirm the order twice.

Every entry follows this reading order: an **architecture diagram** shows responsibilities, a **numbered sequence** shows what crosses each boundary, and **design notes** explain when to choose the pattern, when not to, and how to handle failure.

## Choose components and estimate cost

The [component guide](COMPONENTS.md#the-harness-is-the-first-decision) compares the standard, Microsoft Copilot and Customer Conversation harnesses. Use it to decide between topics and hooks, tools and skills, child and connected agents, or agent flows and workflows. The per-entry mapping explains which components are required or optional; a feature available on one harness isn't necessarily available on another.

The [Copilot Credits guide](COPILOT-CREDITS.md) separates standard-harness event rates from usage-based billing. Its [per-pattern profiles](COPILOT-CREDITS.md#pattern-credit-profiles) identify what to measure, not what a deployment will cost. For example, estimate scheduled runs separately from interactive employee requests rather than assuming the same license covers both.

## Coverage and sources

| Source class | Entries | What it covers |
| --- | ---: | --- |
| [Microsoft reference architectures](CATALOG.md#microsoft-reference-architectures) | 9 | End-to-end designs, including multilingual IT service, SAP procurement and Fabric analytics |
| [Microsoft solution ideas](CATALOG.md#microsoft-solution-ideas) | 11 | Scenario starting points, including onboarding, customer support and clinician-reviewed intake |
| [Microsoft decision-guide patterns](CATALOG.md#fabric-integration-options) | 4 | The four Fabric integration options |
| [Microsoft implementation-guide patterns](CATALOG.md#orchestration-and-handoff-options) | 5 | Three orchestration modes and two handoff designs |
| [Synthesized technical patterns](CATALOG.md#synthesized-technical-patterns) | 20 | Reusable designs for retrieval, tool identity, approvals, governance and operations |

Coverage is dated **November 27, 2026**, against the [Microsoft Learn Copilot Studio architecture index](https://learn.microsoft.com/en-us/power-platform/architecture/products/copilot-studio). The [catalog](CATALOG.md) maps each entry to its sources. The synthesized patterns are not Microsoft reference architectures. Before approving a design, check the linked product documentation for current preview status, channel support and licensing.
