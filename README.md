# Copilot Studio architecture patterns

Use this catalog to design a Microsoft Copilot Studio agent or review an existing AI solution. Its **62 entries** cover decisions such as where to retrieve evidence, when to delegate to a specialist agent, and which steps a workflow or a person must control. These are illustrated design notes, not deployable templates. No tenant access is needed.

**[Validate a solution](review/README.md)** · **[Browse all 62 entries](CATALOG.md)** · **[Choose a retrieval or integration pattern](#choose-between-rag-iq-and-an-api)** · **[Compare components](COMPONENTS.md#pattern-component-matrix)** · **[Estimate Copilot Credits](COPILOT-CREDITS.md#5-estimate-measure-then-multiply)**

## Take a solution to architecture review

Start with the [review guide and evidence packet](review/README.md). For a **proposed** solution, describe the controls and acceptance tests. For an **existing** solution, include observed results from the deployed version. The local validator identifies missing evidence, failed controls and the patterns that help address them. It does not award approval or need access to your tenant.

Try `python3 tools/validate_solution.py review/examples/existing-blocked.json`. The example is deliberately blocked: replaying a timed-out request created two orders. Compare its finding with [reconcile an uncertain write](technical-patterns/write-reconciliation.md). The business system's receipt, not a successful chat turn, closes the review question.

## Start with the decision you need to make

| If you need to… | Start here | Decision to take away |
| --- | --- | --- |
| Answer questions over Fabric or Power BI | [Four Fabric integration options](CATALOG.md#fabric-integration-options) | Should a Fabric data agent write the query, or should Copilot Studio query the semantic model through the Power BI connector? |
| Build an employee assistant | [HR specialists](reference-architectures/hr-specialists.md) and [SharePoint grounding](technical-patterns/sharepoint-grounding.md) | Which questions need a cited policy answer, and which need a tool authorized to read or change the employee's record? |
| Transfer a customer to a representative | [Hub-owned handoff](decision-patterns/hub-front-handoff.md) vs. [agent-owned handoff](decision-patterns/bot-front-handoff.md) | Who owns the live session, and how does the customer know whether the queue accepted the transfer? |
| Automate a transaction that needs approval | [Workflow-owned approval](technical-patterns/approval-workflow.md) | What may the agent draft, and whose recorded decision releases the write? |
| Decide whether an agent is ready for production | [Evaluation gate](technical-patterns/evaluation-gate.md) and [operational monitoring](technical-patterns/operational-monitoring.md) | What evidence shows that the task succeeded in the business system, not just that the agent replied? |

## Choose between RAG, IQ and an API

Start with the claim the agent needs to make. **Retrieval-augmented generation (RAG)** can explain a rule from cited documents. A live API can report what a system currently records. A specialist agent can interpret evidence for a bounded task. Those contracts are different even when all three are presented to Studio as tools.

| What the answer needs | Designs to compare | Decision for review |
| --- | --- | --- |
| Passages from a published manual | [Native Search index lifecycle](technical-patterns/search-index-lifecycle.md) vs. [hybrid retrieval in Azure AI Search](technical-patterns/azure-search-hybrid-rag.md) | Is one corpus safe for the entire audience, or must a service apply per-user filters and tune the query? How quickly must a withdrawn passage disappear? |
| Text from an employee's Microsoft 365 libraries | [Native SharePoint knowledge](technical-patterns/sharepoint-grounding.md) vs. [Microsoft 365 Copilot Retrieval API](technical-patterns/m365-retrieval-api.md) | Does Studio only need a cited answer, or do several applications need the same permission-trimmed extracts without building another index? |
| A policy and a form held in different systems | [Foundry IQ knowledge base](technical-patterns/foundry-iq-knowledge-base.md) vs. [connected Microsoft Foundry specialist](technical-patterns/foundry-agent-specialist.md) | Should Studio interpret the returned evidence, or should a separately owned agent deliver a domain conclusion? |
| Recent employee work or relationships between business entities | [Work IQ context](technical-patterns/work-iq-context.md) vs. [Fabric IQ ontology](technical-patterns/fabric-iq-ontology.md) | Is the authority the signed-in employee's collaboration context, or a governed entity and its relationships? For a financial measure, start with the [Fabric integration options](CATALOG.md#fabric-integration-options). |
| A current public fact or a partner-held record | [Web IQ research](technical-patterns/web-iq-research.md) vs. [third-party context provider](technical-patterns/partner-iq-provider.md) | Which question is safe to send outside the organization? Who authorizes a partner read, and which source will the user see? |
| A proposal based on policy **and** live state | [Change-window evidence using Microsoft Graph and Azure Resource Graph](technical-patterns/change-window-evidence.md) | Keep the policy citation, scoped inventory and free/busy observations separate. None is change approval. |
| The same business operations in several agents | [Publish REST operations as MCP tools with APIM](technical-patterns/apim-rest-to-mcp.md) and [consume a curated MCP catalog](technical-patterns/mcp-tools.md) | Which operations may the gateway publish, and which may this agent invoke? For one stable operation, prefer a [connector tool](technical-patterns/connector-action.md). |

[Microsoft IQ](https://learn.microsoft.com/en-us/microsoft-iq/) groups **Work IQ, Fabric IQ, Foundry IQ and Web IQ**. It is not one interchangeable endpoint. For third-party context, name the provider, supported integration, authentication and terms. When combining sources, send only the minimum question each source needs. In particular, do not forward private conversation history to web search. Keep source, permissions and observation time with each result; if a required source is missing, qualify the answer rather than quietly substituting another.

## Worked example: reviewing an SAP order acknowledgment

1. **Architect:** Open the [architecture diagram](reference-architectures/sap-order-acknowledgments.md#architecture). Agree with procurement on which differences can be accepted automatically and which must go to a specialist. The supplier document provides evidence; it does not set the tolerance.
2. **Developer:** Follow the [technical flow](reference-architectures/sap-order-acknowledgments.md#technical-flow) and [component mapping](reference-architectures/sap-order-acknowledgments.md#copilot-studio-components). A Dataverse-triggered cloud flow starts the agent. The agent extracts and compares the lines; SAP supplies the authoritative order and the confirmation receipt.
3. **Reviewer:** Ask what happens if SAP accepts the write but its reply never arrives. The design records a pending outcome and looks up the existing confirmation before any replay. That gives the team a concrete acceptance test: delivering the same acknowledgment twice must not confirm the order twice.
4. **Review packet:** Select `reference-architectures/sap-order-acknowledgments.md`. The [validator](review/README.md) requires evidence for the authoritative PO (`grounding`), event replay (`trigger`), durable SAP confirmation (`receipt`) and the procurement owner's exception decision (`oversight`). The packet cannot pass by declaring the flow read-only.

Every entry follows this reading order: an **architecture diagram** shows responsibilities, a **numbered sequence** shows what crosses each boundary, and **design notes** explain when to choose the pattern, when not to, and how to handle failure. Each technical sequence includes platform labels and [official architecture icons](assets/platforms/README.md) where applicable. Open the text version below the image for the editable sequence.

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
| [Synthesized technical patterns](CATALOG.md#synthesized-technical-patterns) | 33 | Reusable designs for RAG, IQ, APIs and MCP, tool identity, approvals, reconciliation, governance and operations |

Coverage is dated **November 27, 2026**, against the [Microsoft Learn Copilot Studio architecture index](https://learn.microsoft.com/en-us/power-platform/architecture/products/copilot-studio). The [catalog](CATALOG.md) maps each entry to its sources. The synthesized patterns are not Microsoft reference architectures. Before approving a design, check the linked product documentation for current preview status, channel support and licensing.

See the [dated coverage review](REVIEW-2026-11-27.md) for what was verified and the [implementation and test plan](review/verification-plan.md) for how to repeat those checks.
