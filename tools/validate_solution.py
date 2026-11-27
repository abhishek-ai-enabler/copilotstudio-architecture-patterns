"""Offline evidence-packet checks. This program never fetches a supplied reference."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GROUPS = ("reference-architectures", "solution-ideas", "decision-patterns", "technical-patterns")
# Trigger, question, useful catalog starting point.
RULES = {
    "fit": (None, "Name the outcome, accountable owner, acceptance threshold and simpler alternative.", "decision-patterns/classic-topics.md"),
    "architecture": (None, "Identify component owners, model/version, channels, supported integrations and trust boundaries.", "technical-patterns/zoned-governance.md"),
    "identity": (None, "Trace caller authority and data handling end to end; include a denied-access case.", "technical-patterns/tool-identity.md"),
    "quality": (None, "Define representative cases, failure thresholds, abstention and user fallback.", "technical-patterns/evaluation-gate.md"),
    "operations": (None, "Identify outcome telemetry, service target, rollback, incident owner and retention.", "technical-patterns/operational-monitoring.md"),
    "cost": (None, "Break out model, runtime and external charges; set a per-outcome budget and alert.", "COPILOT-CREDITS.md"),
    "grounding": ("retrieval", "Show provenance, freshness, permission checks and behavior on missing evidence.", "technical-patterns/custom-retrieval.md"),
    "receipt": ("writes", "Show approval authority, idempotency, durable receipt and lost-response handling.", "technical-patterns/write-reconciliation.md"),
    "egress": ("external", "List outbound fields, recipient, terms, retention and the enforced data boundary.", "technical-patterns/web-iq-research.md"),
    "trigger": ("autonomous", "Identify trigger identity, deduplication, volume bounds and stop control.", "technical-patterns/event-worker.md"),
    "oversight": ("consequential", "Name a qualified decision owner, independent approval and a safe staffed fallback.", "technical-patterns/approval-workflow.md"),
    "lineage": ("custom_model", "Trace the training data rights, model and evaluation versions, drift threshold and rollback target.", "review/README.md"),
    "runtime": ("existing", "Provide deployed version, measurement window, observed outcomes and known incidents.", "technical-patterns/solution-promotion.md"),
}
RISKS = ("retrieval", "writes", "external", "autonomous", "consequential", "custom_model")
OBSERVED = {"quality", "operations", "cost", "identity", "grounding", "receipt", "egress", "trigger", "oversight", "lineage", "runtime"}
# Only intrinsic risks: using a connector, for example, does not imply a write.
PATTERN_RISKS = {
    "technical-patterns/write-reconciliation.md": {"writes"},
    "technical-patterns/event-worker.md": {"autonomous"},
    "technical-patterns/partner-iq-provider.md": {"external"},
    "technical-patterns/web-iq-research.md": {"retrieval", "external"},
    "technical-patterns/custom-retrieval.md": {"retrieval"},
    "technical-patterns/azure-search-hybrid-rag.md": {"retrieval"},
    "technical-patterns/foundry-iq-knowledge-base.md": {"retrieval"},
    "technical-patterns/search-index-lifecycle.md": {"retrieval"},
    "technical-patterns/m365-retrieval-api.md": {"retrieval"},
}


def template(stage):
    return {"version": 1, "solution": "", "owner": "", "stage": stage, "scope": "",
            "patterns": [], "unmapped_reason": "", "risks": dict.fromkeys(RISKS),
            "checks": {}}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def field_text(value):
    return isinstance(value, str) and bool(value.strip())


def exact_fields(obj, keys, label):
    require(isinstance(obj, dict), f"{label} must be an object")
    missing, extra = set(keys) - obj.keys(), obj.keys() - set(keys)
    require(not missing and not extra,
            f"{label} fields: missing {sorted(missing)}, unexpected {sorted(extra)}")


def no_duplicates(pairs):
    obj = {}
    for key, value in pairs:
        require(key not in obj, f"duplicate JSON key: {key}")
        obj[key] = value
    return obj


def review(packet):
    exact_fields(packet, template("proposed"), "packet")
    require(type(packet["version"]) is int and packet["version"] == 1, "unsupported packet version")
    require(packet["stage"] in ("proposed", "existing"), "stage must be proposed or existing")
    for key in ("owner", "solution", "scope"):
        require(field_text(packet[key]), f"missing {key}")
    patterns = packet["patterns"]
    require(isinstance(patterns, list) and all(field_text(p) for p in patterns), "patterns must be a list of paths")
    require(len(patterns) == len(set(patterns)), "duplicate pattern")
    known = {p.relative_to(ROOT).as_posix() for g in GROUPS for p in (ROOT / g).glob("*.md")}
    require(set(patterns) <= known, f"unknown pattern(s): {sorted(set(patterns) - known)}")
    require(isinstance(packet["unmapped_reason"], str), "unmapped_reason must be text")
    require(bool(patterns) or field_text(packet["unmapped_reason"]), "select a pattern or explain the catalog gap")
    risks, checks = packet["risks"], packet["checks"]
    exact_fields(risks, RISKS, "risks")
    require(all(type(v) is bool for v in risks.values()), "set each risk explicitly to true or false")
    for path in patterns:
        for risk in sorted(PATTERN_RISKS.get(path, set())):
            require(risks[risk], f"{path} requires risks.{risk}=true")
    required = {k for k, (t, _, _) in RULES.items()
                if t is None or risks.get(t) or (t == "existing" and packet["stage"] == "existing")}
    require(isinstance(checks, dict), "checks must be an object")
    require(checks.keys() <= required, f"unknown or inapplicable checks: {sorted(checks.keys()-required)}")
    findings = []
    for rule, (_, question, source) in RULES.items():
        if rule not in required:
            continue
        issue = None
        if rule not in checks:
            issue = "missing"
        else:
            check = checks[rule]
            exact_fields(check, ("status", "owner", "basis", "reference", "finding"), rule)
            require(check["status"] in ("addressed", "open", "failed"), f"{rule}: unknown status")
            require(check["basis"] in ("design", "observed"), f"{rule}: unknown basis")
            require(all(isinstance(check[k], str) for k in ("owner", "reference", "finding")), f"{rule}: invalid text fields")
            if check["status"] != "addressed":
                issue = check["status"]
            elif not all(field_text(check[k]) for k in ("owner", "reference", "finding")):
                issue = "missing evidence, finding or owner"
            elif packet["stage"] == "existing" and rule in OBSERVED and check["basis"] != "observed":
                issue = "observed evidence required"
        if issue:
            findings.append({"gate": rule, "issue": issue, "request": question, "guidance": source})
    outcome = ("blocked" if any(f["issue"] == "failed" for f in findings)
               else "incomplete" if findings else "ready-for-human-review")
    return {"solution": packet["solution"], "stage": packet["stage"], "outcome": outcome,
            "required": sorted(required), "findings": findings}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument("packet", nargs="?", type=Path)
    mode.add_argument("--init", choices=("proposed", "existing"))
    args = p.parse_args(argv)
    if args.init:
        print(json.dumps(template(args.init), indent=2))
        return 0
    try:
        result = review(json.loads(args.packet.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates))
    except (OSError, ValueError) as e:
        print(json.dumps({"outcome": "invalid", "error": str(e)}), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result["outcome"] == "ready-for-human-review" else 1


if __name__ == "__main__":
    sys.exit(main())
