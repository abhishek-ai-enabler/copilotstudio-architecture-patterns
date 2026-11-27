# Copilot Studio architecture catalog

**Coverage as of 2026-11-27.** The baseline is the [Microsoft Learn Copilot Studio architecture index](https://learn.microsoft.com/en-us/power-platform/architecture/products/copilot-studio), updated November 26. The tables map sources to **49 separate pattern files**. Start with a scenario if you know the business problem, or with a decision if you are choosing between implementations.

| What the source represents | Files | Coverage rule |
| --- | ---: | --- |
| [Microsoft reference architectures](#microsoft-reference-architectures) | 9 | Every entry under **Reference architectures** in the baseline. |
| [Microsoft solution ideas](#microsoft-solution-ideas) | 11 | Every entry under **Solution ideas**. These are starting points, not validated deployments. |
| [Microsoft decision-guide patterns](#fabric-integration-options) | 4 | Every numbered option in the baseline's **Key concepts** guide on Fabric. |
| [Microsoft implementation-guide patterns](#orchestration-and-handoff-options) | 5 | Three orchestration modes and two handoff topologies named in the linked implementation guidance. |
| [Synthesized technical patterns](#synthesized-technical-patterns) | 20 | Selected reusable designs derived from product documentation and public samples; **not** Microsoft reference architectures. |

Classification describes the **source**, not Microsoft's endorsement of the wording or design additions here. Each file is an original design note with a flow, selection criteria, trust boundary, failure case and sources. The first 24 files are exhaustive **for the named baseline sections and date**; the rest extend coverage, not the completeness claim. Lifecycle overviews are navigation resources, not additional reference architectures. No entry implies that a feature is generally available, licensed or supported in every channel.

**Reading the diagrams:** Each entry opens with two original diagrams. **Architecture** groups the actors and systems by responsibility; labeled arrows show what crosses between them, including the result returned to the caller, and a dashed arrow marks a validation or optional path. The groups are logical boundaries, not claims about network isolation. **Technical flow** follows a representative request or lifecycle event from top to bottom. Numbered arrows show calls; dashed arrows show responses. `alt` marks alternative outcomes, `opt` marks an optional step and `loop` marks bounded repetition. The **Review decision** between the diagrams names the choice an architecture board should settle. For example, compare [hub-owned handoff](decision-patterns/hub-front-handoff.md#architecture) with [agent-owned handoff](decision-patterns/bot-front-handoff.md#architecture) to see who controls the session after escalation.

**Components and Copilot Credits:** After the diagrams, each entry has a **Copilot Studio components** section. It names the recommended harness, maps every responsibility to a component (topics, hooks, knowledge, tools, flows and workflows, triggers, skills, memory, agents and human gates), gives the alternative on other harnesses and summarizes what drives Copilot Credits. Use the [component guide](COMPONENTS.md) to choose a harness and component, and the [pattern component matrix](COMPONENTS.md#pattern-component-matrix) to compare entries. The [Copilot Credits guidance](COPILOT-CREDITS.md) explains rates, inclusions, estimation and governance, and ranks every entry by [credit profile](COPILOT-CREDITS.md#pattern-credit-profiles).

## Microsoft reference architectures

| Microsoft Learn source | Pattern file | Decision the design addresses |
| --- | --- | --- |
| [Analytics agent over a Fabric semantic model](https://learn.microsoft.com/en-us/power-platform/architecture/key-concepts/copilot-studio-fabric/copilot-studio-fabric-analytics-agent) | [Analyst-reviewed reporting](reference-architectures/fabric-analytics.md) | Generate live figures and draft commentary while leaving sign-off to an analyst. |
| [Multilingual IT self-service](https://learn.microsoft.com/en-us/power-platform/architecture/reference-architectures/multilingual-it-self-service-agent) | [IT service across identity providers](reference-architectures/multilingual-it-service.md) | Preserve employee identity across a Teams conversation and ITSM actions. |
| [Regulatory application management](https://learn.microsoft.com/en-us/power-platform/architecture/reference-architectures/regulatory-application-management) | [Applicant and assessor workspaces](reference-architectures/regulatory-applications.md) | Share case stages without sharing internal assessment documents. |
| [Procurement order acknowledgment matching with SAP](https://learn.microsoft.com/en-us/power-platform/architecture/reference-architectures/order-acknowledgment-validation) | [Supplier acknowledgment matching](reference-architectures/sap-order-acknowledgments.md) | Confirm within agreed tolerances and escalate line-level discrepancies. |
| [Student recruitment](https://learn.microsoft.com/en-us/power-platform/architecture/reference-architectures/student-recruitment-solution) | [Recruitment touchpoints and enrollment](reference-architectures/student-recruitment.md) | Reconcile changing student identities and measure outreach outcomes. |
| [Conversation transcript analysis](https://learn.microsoft.com/en-us/power-platform/architecture/reference-architectures/analyze-agent-conversation-transcripts) | [Transcript-derived service signals](reference-architectures/conversation-transcripts.md) | Expose useful trends without distributing raw conversation text. |
| [Migrate legacy meetings](https://learn.microsoft.com/en-us/power-platform/architecture/reference-architectures/migrate-legacy-meetings) | [Organizer-led meeting migration](reference-architectures/meeting-migration.md) | Preview selected changes and update supported events in place. |
| [Modernize employee HR support](https://learn.microsoft.com/en-us/power-platform/architecture/reference-architectures/modernize-hr-support) | [HR domain specialists](reference-architectures/hr-specialists.md) | Keep policy search separate from employee and manager transactions. |
| [Agents in model-driven apps](https://learn.microsoft.com/en-us/power-platform/architecture/reference-architectures/contextual-ai-model-driven-app) | [Contextual form recommendations](reference-architectures/model-driven-form.md) | Show suggestions for the current record without auto-saving them; preview API. |

## Microsoft solution ideas

| Microsoft Learn source | Pattern file | Decision the design addresses |
| --- | --- | --- |
| [Healthcare Patient Support Agent](https://learn.microsoft.com/en-us/power-platform/architecture/solution-ideas/agent-healthcare-patient-support) | [Patient administrative support](solution-ideas/patient-support.md) | Separate appointment service from clinician-led care. |
| [Property rental portal](https://learn.microsoft.com/en-us/power-platform/architecture/solution-ideas/agent-rental-portal) | [Rental search and hosted checkout](solution-ideas/rental-search-checkout.md) | Keep AI search out of inventory locking and payment settlement. |
| [Custom contact center](https://learn.microsoft.com/en-us/power-platform/architecture/solution-ideas/agent-custom-contact-center) | [Third-party contact center](solution-ideas/custom-contact-center.md) | Keep an existing center and integrate customer and employee assistance. |
| [Travel concierge](https://learn.microsoft.com/en-us/power-platform/architecture/solution-ideas/agent-travel-customer) | [Travel guidance and booking lookup](solution-ideas/travel-concierge.md) | Switch from public answers to authenticated live reservation data. |
| [Ticket management and refunds](https://learn.microsoft.com/en-us/power-platform/architecture/solution-ideas/agent-ticket-and-refund) | [Shared legacy refund workflow](solution-ideas/ticket-refunds.md) | Let assisted and email-triggered agents use one controlled refund path. |
| [Auto Triage AI Agent](https://learn.microsoft.com/en-us/power-platform/architecture/solution-ideas/auto-ai-triage) | [Bug intake and follow-up](solution-ideas/bug-intake.md) | Create a work item once; authenticate and correlate later correspondence. |
| [Intelligent cardiac triage and scheduling](https://learn.microsoft.com/en-us/power-platform/architecture/solution-ideas/cardio-triage-agent) | [Clinician-reviewed intake and scheduling](solution-ideas/cardiology-intake.md) | Coordinate review and booking without automating clinical disposition. |
| [Anomaly detection with Fabric](https://learn.microsoft.com/en-us/power-platform/architecture/solution-ideas/agent-anomaly-detection) | [Spend anomaly investigation](solution-ideas/spend-anomalies.md) | Detect with reproducible rules and let investigators decide what happens next. |
| [Customer support assistance](https://learn.microsoft.com/en-us/power-platform/architecture/solution-ideas/customer-support-agent) | [Self-service to Dynamics workstream](solution-ideas/customer-support.md) | Transfer a live session with context or offer a tracked case. |
| [Smart new-hire onboarding](https://learn.microsoft.com/en-us/power-platform/architecture/solution-ideas/onboarding-agent) | [Cross-system onboarding](solution-ideas/new-hire-onboarding.md) | Coordinate milestones without treating a draft plan as completed training. |
| [AI-enabled donor management](https://learn.microsoft.com/en-us/power-platform/architecture/solution-ideas/agent-donor-management) | [Donor approvals and finance reconciliation](solution-ideas/donor-management.md) | Trace extracted form fields through approval to a finance receipt. |

## Fabric integration options

The [Fabric architecture decision guide](https://learn.microsoft.com/en-us/power-platform/architecture/key-concepts/copilot-studio-fabric/) compares **where the query is written**. All four options should be evaluated on the same semantic model, identities and expected results. Option 4 is also the mechanism used in the separately indexed end-to-end analytics reference architecture, not a second distinct business scenario.

| Source option | Pattern file | Query author | Choose it for |
| --- | --- | --- | --- |
| Fabric guide, 1 | [Fabric data agent published directly](decision-patterns/fabric-direct.md) | Fabric data agent | A baseline or simple Q&A. No Copilot Studio agent in the path. |
| Fabric guide, 2 | [Connected Fabric data agent](decision-patterns/fabric-connected.md) | Fabric data agent | A separately maintained model-aware specialist behind a Copilot Studio front end. |
| Fabric guide, 3 | [Standard harness + Power BI connector](decision-patterns/fabric-standard-harness.md) | Copilot Studio | A stable, compact model description and low-latency direct queries. |
| Fabric guide, 4 | [Microsoft Copilot harness + Power BI connector](decision-patterns/fabric-copilot-harness.md) | Copilot Studio, guided by a skill | Direct queries, reusable schema guidance and correction of failed DAX. |

## Orchestration and handoff options

These are named approaches from **implementation guidance**, not entries in the baseline's reference architecture table.

| Microsoft Learn source | Pattern file | Where control sits |
| --- | --- | --- |
| [Understand harnesses: classic](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/understand-harnesses#standard-harness-classic-orchestration) | [Classic topic routing](decision-patterns/classic-topics.md) | A matched topic owns the ordered conversation. |
| [Understand harnesses: generative](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/understand-harnesses#standard-harness-generative-orchestration) | [Generative planning](decision-patterns/generative-planning.md) | The standard harness plans using topics, tools, knowledge and agents. |
| [Understand harnesses: reasoning loop](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/understand-harnesses#copilot-harness-reasoning-loop) | [Observe and choose the next action](decision-patterns/copilot-reasoning-loop.md) | The Microsoft Copilot harness revises the route after observing results. |
| [Channels, handoff pattern 1](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/channels) | [Hub in front: Bot-as-an-Agent](decision-patterns/hub-front-handoff.md) | The hub owns the canvas and takes over routing. |
| [Channels, handoff pattern 2](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/channels) | [Agent in front: Bot-in-the-Loop](decision-patterns/bot-front-handoff.md) | A bridge relays the human exchange through the agent canvas. |

## Synthesized technical patterns

These files are catalog designs, not additional Microsoft reference architectures. The sources below document the relevant capabilities. Individual files link further reading and public samples where useful; samples illustrate integration shapes, not production guarantees.

| Area | Primary source | Pattern file |
| --- | --- | --- |
| Knowledge | [SharePoint knowledge](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-add-sharepoint) | [Permission-trimmed internal answers](technical-patterns/sharepoint-grounding.md) |
| Knowledge | [Public website knowledge](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-add-public-website) | [Bounded public website Q&A](technical-patterns/public-knowledge.md) |
| Knowledge | [Custom data in generative answers nodes](https://learn.microsoft.com/en-us/microsoft-copilot-studio/nlu-generative-answers-custom-data) | [Custom permission-aware retrieval](technical-patterns/custom-retrieval.md) |
| Analytics | [Prepare a semantic model](https://learn.microsoft.com/en-us/power-platform/architecture/key-concepts/copilot-studio-fabric/semantic-model-ai-agents) | [Shared metric contract](technical-patterns/semantic-model-contract.md) |
| Composition | [Child agents](https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-agent-child-agent) | [One specialist inside the parent](technical-patterns/child-agent.md) |
| Composition | [Connect Copilot Studio agents](https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-agent-copilot-studio-agent) | [Independently published specialist](technical-patterns/connected-agent.md) |
| Composition | [Skills overview](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-overview) | [Reusable procedure as a skill](technical-patterns/skill-package.md) |
| Identity | [Tool authentication](https://learn.microsoft.com/en-us/microsoft-copilot-studio/configure-enduser-authentication) | [Carry end-user authority to the tool](technical-patterns/tool-identity.md) |
| Integration | [Integration strategies](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/integrations) | [Narrow connector action](technical-patterns/connector-action.md) |
| Integration | [Direct REST tool (preview)](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agent-extend-action-rest-api) | [Agent-local OpenAPI prototype](technical-patterns/direct-rest-tool.md) |
| Integration | [Model Context Protocol](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/extend-with-model-context-protocol) | [Centrally managed MCP tools](technical-patterns/mcp-tools.md) |
| Automation | [Agent flow tool contract](https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-flow-create) | [Synchronous flow with a typed result](technical-patterns/synchronous-agent-flow.md) |
| Automation | [Event triggers](https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-triggers-about) | [Event-driven agent worker](technical-patterns/event-worker.md) |
| Automation | [AI-powered automations](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/ai-powered-automation) | [Workflow-owned approval](technical-patterns/approval-workflow.md) |
| Channel | [Web and Direct Line security](https://learn.microsoft.com/en-us/microsoft-copilot-studio/configure-web-security) | [Secured custom web client](technical-patterns/secured-web-client.md) |
| Channel | [Customer Conversation harness](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/overview-customer-conversation) | [Distinct paths for voice and chat](technical-patterns/customer-voice-chat.md) |
| Governance | [Zoned governance](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/sec-gov-phase2) | [Risk-based environment controls](technical-patterns/zoned-governance.md) |
| Delivery | [Application lifecycle management](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/alm) | [Promote a tested solution](technical-patterns/solution-promotion.md) |
| Quality | [Agent evaluation](https://learn.microsoft.com/en-us/agents/agent-evaluation/) | [Gate releases on answers and actions](technical-patterns/evaluation-gate.md) |
| Operations | [Monitoring and capacity](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/sec-gov-phase5) | [Service outcome, health and consumption](technical-patterns/operational-monitoring.md) |

## Architecture review

Use the [Microsoft framework for architecting agent solutions](https://learn.microsoft.com/en-us/agents/architecture/) to review any choice above:

| Framework pillar | Question to settle before adopting a pattern |
| --- | --- |
| [Fit for purpose](https://learn.microsoft.com/en-us/agents/architecture/determine-fit-for-purpose) | Would a form, search page or deterministic workflow solve the problem more reliably? What outcome justifies an agent? |
| [Operability](https://learn.microsoft.com/en-us/agents/architecture/determine-operability) | Which receipt proves success, how will an owner spot partial failure, and how can they resume without repeating an action? |
| [Trust, traceability and transparency](https://learn.microsoft.com/en-us/agents/architecture/determine-trust) | Whose identity reaches each system, what evidence supports the answer, and who authorizes consequential changes? |

**Maintaining coverage:** Compare the baseline's three named sections against these tables at the next review. Add newly listed entries as separate files in the right class; record reclassifications and update the date and counts. Check current feature status, permissions, licensing, regional availability and published-channel behavior before implementing any design.
