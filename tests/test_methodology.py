from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class MethodologyIntegrityTests(unittest.TestCase):
    def read(self, rel: str) -> str:
        return (ROOT / rel).read_text(encoding="utf-8")

    def test_identity_and_product(self):
        combined = self.read("README.md") + self.read("CITATION.cff") + self.read("RELEASE_NOTES.md")
        self.assertIn("Quantum Readiness for Space Communications", combined)
        self.assertIn("quantum-readiness-space-communications", combined)
        self.assertIn("Quantum Readiness Decision Pack", combined)

    def test_documentation_first_scope(self):
        self.assertFalse((ROOT / "src").exists())
        self.assertFalse((ROOT / "schema").exists())
        self.assertEqual([], list(ROOT.rglob("*.xlsx")))

    def test_unknown_and_not_applicable_are_separate(self):
        text = self.read("assessment/quantum-exposure-severity.md")
        self.assertIn("Unknown / Not Assessed", text)
        self.assertRegex(text, r"\|\s*0\s*\|\s*Not Applicable\s*\|")
        self.assertIn("accountable applicability", text)

    def test_ten_domains_and_no_weights(self):
        text = self.read("assessment/migration-readiness-profile.md")
        self.assertEqual(10, len(re.findall(r"^### Domain \d+\. ", text, re.M)))
        self.assertNotRegex(text, r"\b\d+(?:\.\d+)?%")
        self.assertNotRegex(text, r"(?i)\|\s*(?:weight|weighted|percentage)\s*\|")
        self.assertIn("not a weighted index", text.lower())
        self.assertIn("Sustained and Reassessed", text)

    def test_evidence_confidence_and_coverage(self):
        text = self.read("assessment/evidence-confidence-ledger.md")
        for token in ["Evidence Confidence and Coverage", "Evidence Coverage (%)", "Critical Unknowns", "Stale Evidence Items", "Conflicting Evidence Items", "Unassessed Critical-Scope Items", "Approved Exclusions"]:
            self.assertIn(token, text)

    def test_twelve_semantic_critical_conditions(self):
        text = self.read("assessment/critical-risk-overrides.md")
        for i in range(1, 13):
            self.assertIn(f"CR-{i:02d}", text)
        self.assertIn("harvest-now-decrypt-later", text)
        self.assertIn("contradictory", text)

    def test_complete_decision_pack_example(self):
        directory = ROOT / "examples/sample-small-satellite-decision-pack"
        self.assertTrue(directory.is_dir())
        self.assertEqual(11, len(list(directory.glob("*.md"))))
        self.assertIn("Critical Action Required", self.read("examples/sample-small-satellite-decision-pack/10-decision-record-and-review.md"))

    def test_release_status_is_explicit(self):
        text = self.read("release/release-status.md")
        self.assertIn("Current source version: **0.2.4**", text)
        self.assertIn("Latest published GitHub Release: **v0.2.3**", text)
        self.assertIn("not represented as a published release", text)

    def test_release_metadata(self):
        metadata = json.loads(self.read("release/release-metadata.json"))
        self.assertEqual("quantum-readiness-space-communications", metadata["name"])
        self.assertEqual("0.2.4", metadata["version"])
        self.assertEqual("{{RELEASE_DATE}}", metadata["release_date"])
        self.assertEqual("0.2.4", self.read("VERSION").strip())
        self.assertEqual("Quantum Readiness Decision Pack", metadata["decision_pack_name"])

    def test_current_federal_pqc_policy_context(self):
        register = self.read("docs/standards-register.md")
        readme = self.read("README.md")
        for token in ["EO 14412", "M-26-15", "2030", "2031", "2035"]:
            self.assertIn(token, register)
        self.assertIn("Federal PQC Policy Context", readme)
        self.assertIn("not an automatic compliance determination", readme)
        self.assertIn("does not apply to National Security Systems", readme)

    def test_current_source_is_not_presented_as_formally_released(self):
        status = self.read("release/release-status.md")
        self.assertIn("Latest published GitHub Release: **v0.2.3**", status)
        self.assertIn("Source version 0.2.4 is not represented as a published release", status)
        self.assertIn("0.2.4 - Unreleased source", self.read("CHANGELOG.md"))

if __name__ == "__main__":
    unittest.main()
