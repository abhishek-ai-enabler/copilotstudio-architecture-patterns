# Standard harness: generative orchestration over topics, tools and knowledge

**Class:** Microsoft implementation-guide pattern (orchestration). **Intent:** Handle requests that combine several familiar tasks without writing a topic for every possible sequence.

**Flow:** A planner selects from descriptions of tools, knowledge, topics and eligible agents, gathers missing inputs and combines their outputs. For “find the warranty and check my repair,” keep the cited warranty text distinct from the repair system's live status. Use an authored topic or flow for any fixed confirmation sequence.

**Choose it when** users express multiple intents and the capabilities have distinct purposes. Broad or overlapping descriptions make routing less predictable. For a mandatory fixed dialogue use [classic topics](classic-topics.md); for iterative exploration compare the [Copilot harness loop](copilot-reasoning-loop.md).

**Trust boundary:** A tool description tells the planner *when* to call, not *who* is allowed to act. Backend permissions, validation and confirmation still apply. Do not let the content of a retrieved warranty instruct the agent to invoke a tool.

**Failure handling:** If one part fails, label its outcome independently; finding the warranty is not evidence the repair lookup succeeded. Evaluate ambiguous tool pairs, missing identifiers and interrupted multi-intent conversations in the published channel.

**Sources:** [Microsoft Learn: Standard harness generative orchestration](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/understand-harnesses#standard-harness-generative-orchestration) · [Orchestrate agent behavior with generative AI](https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-generative-actions).
