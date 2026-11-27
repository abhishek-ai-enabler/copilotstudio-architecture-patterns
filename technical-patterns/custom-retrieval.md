# Bring authorized search results to a generative answers node

**Class:** Synthesized technical pattern. **Intent:** Ground answers in a repository with specialized ranking or entitlements that native knowledge sources cannot represent.

**Flow:** A standard-harness topic calls an approved search endpoint using an HTTP request or Power Automate flow. The service authorizes the caller, ranks permitted matches and returns small excerpts. Map them into a table for the generative answers node's **Classic data / Custom data** option: `Content`, plus `Title` and `ContentLocation` for usable citations. The documented node uses only the first three records.

**Choose it when** you need to own search quality, freshness or source-specific filtering. For an ordinary SharePoint library use [native grounding](sharepoint-grounding.md) instead: a custom service adds availability, relevance and authorization work.

**Trust boundary:** Filter at retrieval time, before the model or logs see any excerpt. A link that requires sign-in does not protect text already returned to a user. Never grant a broad service identity unrestricted search solely to improve recall.

**Failure handling:** Distinguish no authorized matches from a backend outage internally; avoid revealing inaccessible records to the user. For restricted intents, do not allow a broader agent-level fallback to invent an answer. Test a revoked document and a timeout.

**Source:** [Use custom data in generative answers nodes](https://learn.microsoft.com/en-us/microsoft-copilot-studio/nlu-generative-answers-custom-data).
