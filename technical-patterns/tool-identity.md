# Carry the user's authority to a downstream tool

**Class:** Synthesized technical pattern. **Intent:** Ensure “show my cases” runs with the caller's permissions, not those of the person who built the agent.

**Flow:** Authenticate the user to the agent in a supported channel. Configure the private tool for **User authentication**. On invocation Copilot Studio finds the user's service connection or presents a connection card. The service authorizes the operation and record; the agent returns only permitted fields. Inspect the actual connection for each flow step as well.

**Choose it when** the underlying data or action is personal, role-scoped or auditable per user. Agent-author credentials can fit a tightly scoped, low-risk shared lookup (for example, published office hours). They are not a substitute for missing delegation on a private record system.

**Trust boundary:** Channel sign-in, permission to use the agent and permission to call the downstream API are separate. A user ID supplied in a prompt proves none of them. Check the product's channel support matrix, including custom-client consent handling.

**Failure handling:** Reconnect on expired consent; on denial, end the operation without an author-credential fallback. Test two users with different case access, revoked consent and a reused browser session.

**Sources:** [Configure end-user authentication for tools and supported channels](https://learn.microsoft.com/en-us/microsoft-copilot-studio/configure-enduser-authentication) · [Microsoft public SSO examples](https://github.com/microsoft/CopilotStudioSamples/tree/main/sso/entra-id).
