from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from guided_assessment import assess  # noqa: E402


class GuidedAssessmentTests(unittest.TestCase):
    def source(self):
        return json.loads((ROOT / "examples/guided-assessment/answers.json").read_text(encoding="utf-8"))

    def test_reference_is_bounded_and_deterministic(self):
        first = assess(self.source())
        second = assess(self.source())
        self.assertEqual(first, second)
        self.assertEqual(first["overall_state"], "INCOMPLETE_OR_GAPS")
        self.assertTrue(first["human_review_required"])
        self.assertEqual(first["authority_effect"], "NONE")

    def test_yes_without_evidence_fails_to_evidence_missing(self):
        source = self.source()
        source["answers"]["P1"] = {"response": "YES", "evidence_refs": []}
        result = assess(source)
        self.assertEqual(result["results"][0]["state"], "EVIDENCE_MISSING")


if __name__ == "__main__":
    unittest.main()
