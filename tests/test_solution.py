import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.validate_solution import GROUPS, OBSERVED, PATTERN_RISKS, RISKS, ROOT, RULES, review


class SolutionReview(unittest.TestCase):
    def setUp(self):
        self.packet = json.loads((ROOT / "review/examples/proposed.json").read_text())

    def test_proposed_does_not_claim_approval(self):
        self.assertEqual(review(self.packet)["outcome"], "ready-for-human-review")

    def test_risks_require_explicit_booleans(self):
        for bad in (None, 0, "false"):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                self.packet["risks"]["writes"] = bad
                review(self.packet)
        del self.packet["risks"]["writes"]
        with self.assertRaises(ValueError):
            review(self.packet)

    def test_each_new_boundary_requires_its_evidence(self):
        for gate, (risk, _, _) in RULES.items():
            if risk not in self.packet["risks"]:
                continue
            with self.subTest(risk=risk):
                self.packet["risks"][risk] = True
                self.packet["checks"].pop(gate, None)
                self.assertIn(gate, {f["gate"] for f in review(self.packet)["findings"]})

    def test_existing_design_only_is_insufficient(self):
        self.packet["stage"] = "existing"
        result = review(self.packet)
        self.assertEqual(result["outcome"], "incomplete")
        self.assertIn("runtime", {f["gate"] for f in result["findings"]})
        for g in result["required"]:
            self.packet["checks"][g] = dict(self.packet["checks"]["fit"], basis="observed" if g in OBSERVED else "design")
        self.assertEqual(review(self.packet)["outcome"], "ready-for-human-review")

    def test_existing_failure_beats_incomplete(self):
        p = json.loads((ROOT / "review/examples/existing-blocked.json").read_text())
        self.assertEqual(review(p)["outcome"], "blocked")

    def test_selected_pattern_cannot_deny_intrinsic_risk(self):
        self.packet["risks"]["retrieval"] = False
        with self.assertRaisesRegex(ValueError, "requires risks.retrieval"):
            review(self.packet)

    def test_all_catalog_entries_have_reviewed_risks(self):
        catalog = {p.relative_to(ROOT).as_posix()
                   for group in GROUPS for p in (ROOT / group).glob("*.md")}
        self.assertEqual(PATTERN_RISKS.keys(), catalog)
        for path, risks in PATTERN_RISKS.items():
            self.assertTrue(set(risks) <= set(RISKS), path)
        with patch.dict(PATTERN_RISKS, clear=True), self.assertRaisesRegex(ValueError, "classification missing"):
            review(self.packet)

    def test_sap_cannot_skip_receipt_or_oversight(self):
        self.packet["patterns"] = ["reference-architectures/sap-order-acknowledgments.md"]
        self.packet["scope"] = "Read the current PO, submit the SAP confirmation and report its receipt."
        self.packet["risks"] = dict.fromkeys(RISKS, False)
        with self.assertRaises(ValueError) as error:
            review(self.packet)
        for risk in ("retrieval", "writes", "autonomous", "consequential"):
            self.assertIn(f"requires risks.{risk}=true", str(error.exception))
            self.packet["risks"][risk] = True
        result = review(self.packet)
        self.assertEqual(result["outcome"], "incomplete")
        self.assertEqual({f["gate"] for f in result["findings"]}, {"trigger", "receipt", "oversight"})

    def test_read_only_evidence_does_not_require_a_receipt(self):
        self.packet["patterns"] = ["technical-patterns/change-window-evidence.md"]
        self.packet["scope"] = "Read policy, inventory and availability to propose a window. Do not book it."
        result = review(self.packet)
        self.assertEqual(result["outcome"], "ready-for-human-review")
        self.assertNotIn("receipt", result["required"])
        self.assertIn("grounding", result["required"])

    def test_multiple_patterns_require_the_union_of_risks(self):
        self.packet["patterns"].append("technical-patterns/write-reconciliation.md")
        with self.assertRaisesRegex(ValueError, "requires risks.writes"):
            review(self.packet)
        self.packet["risks"]["writes"] = True
        self.assertEqual([f["gate"] for f in review(self.packet)["findings"]], ["receipt"])

    def test_unmapped_architecture_needs_explanation(self):
        self.packet["patterns"] = []
        with self.assertRaises(ValueError):
            review(self.packet)
        self.packet["unmapped_reason"] = "Edge inference; see private provider design review."
        self.assertEqual(review(self.packet)["outcome"], "ready-for-human-review")

    def test_unknown_paths_or_gates_are_invalid(self):
        self.packet["checks"]["wrong"] = {}
        with self.assertRaises(ValueError):
            review(self.packet)
        del self.packet["checks"]["wrong"]
        self.packet["patterns"] = ["../outside.md"]
        with self.assertRaises(ValueError):
            review(self.packet)

    def test_blank_reference_is_not_evidence(self):
        self.packet["checks"]["fit"]["reference"] = "   "
        self.assertEqual(review(self.packet)["outcome"], "incomplete")

    def test_cli_contract(self):
        command = [sys.executable, str(ROOT / "tools/validate_solution.py")]
        for stage in ("existing", "proposed"):
            p = subprocess.run(command + ["--init", stage], capture_output=True)
            self.assertEqual(p.returncode, 0)
            self.assertEqual(json.loads(p.stdout)["stage"], stage)
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "packet.json"
            for value, code in [('{"version":1,"version":2}', 2), ("[", 2),
                                (json.dumps(self.packet), 0),
                                ((ROOT / "review/examples/existing-blocked.json").read_text(), 1)]:
                path.write_text(value)
                p = subprocess.run(command + [str(path)], capture_output=True)
                self.assertEqual(p.returncode, code)
                self.assertIn("outcome", json.loads(p.stdout or p.stderr))
