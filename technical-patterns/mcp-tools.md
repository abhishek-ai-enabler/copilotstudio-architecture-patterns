# Discover centrally managed tools from an MCP server

**Class:** Synthesized technical pattern. **Intent:** Let several agents consume a tool catalog maintained by the API owner rather than maintaining a separate description in every agent.

**Flow:** An approved Model Context Protocol (MCP) server advertises tool definitions. Copilot Studio connects using a supported configuration and discovers tools; the agent invokes the relevant one with structured arguments. The server validates the operation, caller and arguments, calls the underlying system, and returns a bounded result.

**Choose it when** tools evolve together or are consumed by multiple agents or clients. A single supported connector usually costs less to operate. Check which tools, resources, authentication modes and transport the selected harness actually supports.

**Trust boundary:** Discovery is not approval. Restrict servers and downstream permissions; review changes in exposed tools and descriptions before broad use. Do not let a read-only agent acquire a write capability just because the server added it.

**Failure handling:** Set timeouts and validate tool output. On incompatible schema or an unavailable server, disable the affected capability rather than falling back to unbounded HTTP. Test a catalog update and verify denied tools stay inaccessible.

**Sources:** [Extend agents with Model Context Protocol](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/extend-with-model-context-protocol) · [Microsoft public Copilot Studio MCP samples](https://github.com/microsoft/CopilotStudioSamples/tree/main/extensibility/mcp).
