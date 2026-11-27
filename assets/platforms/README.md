# Architecture artwork and attribution

These are official Microsoft product or service icons, used only inside documentation illustrating those products. Microsoft retains all rights to its marks. Inclusion does not imply endorsement. The SVGs are unmodified; they are fitted proportionally on white next to the named platform. The [registry](products.json) records the display name, exact archive member and original SHA-256 for each asset. The [public-use notice](Microsoft-public-use-icon-terms.pdf) is included as supplied in the Power Platform download.

| Pack | Terms and source |
| --- | --- |
| `power` | [Microsoft Power Platform icons](https://learn.microsoft.com/en-us/power-platform/guidance/icons), December 2025 scalable download |
| `azure` | [Azure architecture icons](https://learn.microsoft.com/en-us/azure/architecture/icons/), public service icons V25. The Cognitive Search member depicts the service now called Azure AI Search. |
| `fabric` | [Microsoft Fabric icons](https://learn.microsoft.com/en-us/fabric/fundamentals/icons), linked `Icons.zip` v6.1.0; uses the product and specific data-agent, semantic-model and Eventhouse icons |
| `dynamics` | [Dynamics 365 icons](https://learn.microsoft.com/en-us/dynamics365/get-started/icons), scalable app icons |

**Reading a flow:** The heading above a lifeline identifies its platform; the box names its role in the sequence. A Studio workflow is not labeled Power Automate merely because it contains flow nodes. The direct Fabric pattern has no Studio logo. A person, generic backend, abstract MCP server or custom adapter receives **no vendor logo**. A named external product or API without verified, reusable artwork in these packs is spelled out instead: for example SAP, Jira Cloud, Stripe, Microsoft Graph, Work IQ and Web IQ. Azure Resource Graph is not Resource Graph *Explorer*. Do not substitute an unrelated logo or assume permission to republish a partner's mark.

To change an attribution, edit the [lifeline map](../../tools/diagrams/platforms.txt), verify it against the implementation described in the entry, and [regenerate and test the diagrams](../../tools/diagrams/README.md).
