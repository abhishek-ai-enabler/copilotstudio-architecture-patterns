# Package reusable procedures as skills

**Class:** Synthesized technical pattern. **Intent:** Share a bounded procedure, such as formatting a service review, without duplicating long instructions or operating a separate agent.

**Flow:** On the Microsoft Copilot harness, keep global behavior in the agent instructions. Package task-specific guidance and vetted resources as a named skill with a precise description. When the request matches, the agent loads the procedure and uses its available tools. Version the skill and check its result against a representative service review.

**Choose it when** several agents perform the same procedure with their own authorized data. A skill describes *how*; use a tool for an external action, a knowledge source for changing policy facts, and a workflow for a mandatory execution order. These instruction-based skills are not the Azure Bot Service skills used by some handoff bridges.

**Trust boundary:** Review packages and any scripts as supply-chain inputs. Do not package credentials, production records or implied permission grants. The consuming agent still needs its own authorized tool connections.

**Failure handling:** Detect missing tools and incompatible versions before rollout. Test an unrelated request that must not load this skill, as well as a matching request with no access to the report. Keep a known-good package to restore through the normal release process.

**Source:** [Skills overview for agents on the Microsoft Copilot harness](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-overview).
