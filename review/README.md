# Validate a solution architecture

Use this review before approving a design or renewing approval for an existing AI solution. It is an **evidence checklist with a local validator**, not an AI judge or a Microsoft certification. It can review non-Copilot workloads: map only decisions that fit, explain unmatched areas and bring their provider-specific guidance. No catalog can establish that every AI workload is safe or supported.

## Run a review

1. **Scope the decision.** Name the owner, users, business outcome, supported channel and version. Identify what the system must not do. For an existing solution, review what is deployed, not the original slide deck.
2. **Trace one success and one failure.** Follow the sequence arrows: what data crosses each boundary, under whose identity, with which authority? Map those choices to [catalog paths](../CATALOG.md). If none fit, set `patterns` to `[]` and record `unmapped_reason`. Never select a Microsoft pattern just to make a review pass.
3. **Select the risks and attach evidence.** Declare every risk `true` or `false`. A reviewer challenges each `false` against the data-flow diagram, not just the tool descriptions. Record a named owner, an artifact reference and a concrete finding for each applicable gate. Design evidence can be a versioned ADR or acceptance test plan; observed evidence should identify the environment, measurement window, build and actual outcome.
4. **Run locally.** From the repository root, with Python 3.9+:

   ```sh
   python3 tools/validate_solution.py --init proposed > my-review.json
   python3 tools/validate_solution.py my-review.json
   ```

   Use `--init existing` for an operating solution. Fill in the scope and risks, then run with `checks: {}` to get the required gates, questions and related patterns. Copy the check shape from the [proposed example](examples/proposed.json). Keep real packets and evidence in your approved **private** system; the validator does not read evidence URLs, inspect tenants or call a model. Do not upload transcripts, credentials or sensitive architecture to this public repository.
5. **Record the human decision.** An architect and the accountable business owner inspect the referenced evidence. Record the solution/version, decision (approve scope / request changes / reject), rationale, outstanding actions, owner, due date, evidence snapshot and re-review trigger. An approval for a design is **not** go-live approval. Re-run after a new model, data source, permission, channel, write tool, material cost change or incident.

## What is checked

| Applies to | Gate IDs | What a reviewer should inspect |
| --- | --- | --- |
| Every solution | `fit`, `architecture`, `identity` | Baseline without AI, outcome target, component diagram, version/availability, data classification and retention, identity per hop and a denied case. For a batch model, include training/serving boundaries and the dataset/version. |
| Every solution | `quality`, `operations`, `cost` | Evaluation across representative user groups and failure cases, regression threshold, safe fallback, recovery owner, service target and cost per useful outcome. Include model/data drift where relevant. |
| Retrieves evidence | `grounding` | Source of truth, citations, stale/deleted evidence, wrong-audience and no-result tests. |
| Writes to another system | `receipt` | Confirm authorization, stable business key and definitive receipt. Test a lost reply after commit. |
| Crosses an external trust boundary | `egress` | Fields leaving the boundary, destination, credentials, terms and retention; prove a private input cannot reach an unapproved provider. |
| Runs autonomously | `trigger` | Event or schedule authority, replay behavior, concurrency/volume limits and stop control. |
| Material impact on people, money or rights | `oversight` | Decision authority outside the model, escalation path and evidence the system stops on missing authorization. In healthcare, involve the responsible clinician; this catalog does not validate clinical practice. |
| Owns trained or fine-tuned model artifacts | `lineage` | Dataset rights and splits, evaluation and model version lineage, serving/training skew, drift alert, rollback version. See [model lifecycle guidance](https://learn.microsoft.com/en-us/azure/machine-learning/concept-model-management-and-deployment?view=azureml-api-2) or the equivalent for your stack. |
| Already operating | `runtime` | Deployed version, representative observation window, business receipts, incident history and rollback evidence. Existing reviews also require `basis: "observed"` for quality, identity, operations, cost and applicable risk gates. |

These are catalog rules inspired by Microsoft's [fit, operability and trust pillars](https://learn.microsoft.com/en-us/agents/architecture/), not official Microsoft pass/fail criteria. Some selected patterns imply a risk: a write-reconciliation design cannot declare `writes: false`, for example. This catches contradictions, not undisclosed risks. For a regulated or safety-critical workload, route remaining domain and legal obligations to qualified reviewers.

## Interpret the result

| Result | Exit | Next action |
| --- | ---: | --- |
| `invalid` | 2 | Correct malformed JSON, unknown pattern paths, incomplete risk declarations or unsupported fields. |
| `blocked` | 1 | At least one applicable control has a recorded failure. Address it before approval. Other missing controls are still listed. |
| `incomplete` | 1 | Supply missing, open or insufficiently evidenced checks. A design plan cannot substitute for measured operating behavior. |
| `ready-for-human-review` | 0 | All applicable fields contain evidence references and findings of the required kind. Inspect them; the tool cannot verify their truth, sufficiency, freshness or the submitter's account of risk. |

Run `python3 tools/validate_solution.py review/examples/proposed.json` for a design packet ready for **human review**. Run `python3 tools/validate_solution.py review/examples/existing-blocked.json` for a failed replay test with outstanding operating evidence. Both use fictional `example:` references and are **not** attestations. To test the rules, run `python3 -m unittest discover -s tests -v`.
