# Standard harness: classic topic routing

**Class:** Microsoft implementation-guide pattern (orchestration). **Intent:** Keep the order and wording of a bounded transaction under maker control.

**Flow:** A request matches a topic's trigger phrases. Authored nodes collect fields, validate them, show a confirmation and explicitly call a tool or flow. If no topic matches, the agent can use a configured knowledge fallback and then its Fallback system topic. For a required disclosure, keep that wording in an authored node, not in generated fallback content.

**Choose it when** the interaction has a small set of stable intents and required steps, for example replacing a damaged badge. New phrasings and topic collisions need ongoing maintenance. If the main need is flexible composition of several intents, compare [generative orchestration](generative-planning.md).

**Trust boundary:** Selecting a topic is not authorization. Validate the badge owner and allowed operation at the tool; refuse to submit without confirmed inputs.

**Failure handling:** On an ambiguous match, ask the user to select a task. On a connector timeout, reconcile the requested replacement before offering retry. Test paraphrases, cancellation at confirmation and an out-of-scope request that must not enter the transaction.

**Source:** [Microsoft Learn: Understand harnesses — standard harness classic orchestration](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/understand-harnesses#standard-harness-classic-orchestration).
