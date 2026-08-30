from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from continuous_assurance import evaluate, transition_allowed  # noqa: E402
from validate_assurance import check_crypto_agility_thread  # noqa: E402

BASE = json.loads(
    (ROOT / "examples" / "secure-inference-cell" / "reference-bundle.json").read_text(encoding="utf-8")
)

class ContinuousAssuranceTests(unittest.TestCase):
    def bundle(self):
        return copy.deepcopy(BASE)

    def test_reference_bundle_is_permitted(self):
        decision, _ = evaluate(self.bundle())
        self.assertEqual(decision, "PERMITTED")

    def test_optional_crypto_agility_thread_is_bounded(self):
        self.assertIsNone(check_crypto_agility_thread())

    def test_unknown_flow_fails_closed_to_containment(self):
        data = self.bundle()
        data["transaction_request"]["endpoint"] = "/unknown"
        decision, reasons = evaluate(data)
        self.assertEqual(decision, "CONTAINED")
        self.assertTrue(any("not explicitly authorized" in reason for reason in reasons))

    def test_expired_evidence_requires_reverification(self):
        data = self.bundle()
        data["evidence_artifacts"][0]["valid_until"] = "2026-08-16T00:00:00Z"
        decision, _ = evaluate(data)
        self.assertEqual(decision, "REVERIFICATION_REQUIRED")

    def test_configuration_mismatch_requires_reauthorization(self):
        data = self.bundle()
        data["evidence_artifacts"][0]["configuration_id"] = "cfg-other"
        decision, _ = evaluate(data)
        self.assertEqual(decision, "REAUTHORIZATION_REQUIRED")

    def test_revoked_authority_requires_reauthorization(self):
        data = self.bundle()
        data["operating_disposition"]["authority_state"] = "REVOKED"
        decision, _ = evaluate(data)
        self.assertEqual(decision, "REAUTHORIZATION_REQUIRED")

    def test_missing_required_property_is_incomplete(self):
        data = self.bundle()
        data["security_invariants"] = [
            item for item in data["security_invariants"] if item["property_id"] != "P5"
        ]
        decision, _ = evaluate(data)
        self.assertEqual(decision, "INCOMPLETE")

    def test_unsupported_schema_version_fails_closed(self):
        data = self.bundle()
        data["schema_version"] = "2.0.0"
        decision, _ = evaluate(data)
        self.assertEqual(decision, "FAIL_CLOSED")

    def test_superseded_evidence_not_current(self):
        data = self.bundle()
        data["evidence_artifacts"][0]["state"] = "SUPERSEDED"
        decision, _ = evaluate(data)
        self.assertEqual(decision, "REVERIFICATION_REQUIRED")

    def test_failed_evidence_cannot_support_permission(self):
        data = self.bundle()
        data["evidence_artifacts"][0]["result"] = "FAIL"
        decision, reasons = evaluate(data)
        self.assertEqual(decision, "REVERIFICATION_REQUIRED")
        self.assertTrue(any("result is not PASS" in reason for reason in reasons))

    def test_duplicate_evidence_identifier_fails_closed(self):
        data = self.bundle()
        data["evidence_artifacts"][1]["evidence_id"] = data["evidence_artifacts"][0]["evidence_id"]
        decision, _ = evaluate(data)
        self.assertEqual(decision, "FAIL_CLOSED")

    def test_unknown_disposition_evidence_is_incomplete(self):
        data = self.bundle()
        data["operating_disposition"]["evidence_ids"].append("evidence.unknown")
        decision, _ = evaluate(data)
        self.assertEqual(decision, "INCOMPLETE")

    def test_system_identifier_mismatch_fails_closed(self):
        data = self.bundle()
        data["system_claims"][0]["system_id"] = "other-system"
        decision, _ = evaluate(data)
        self.assertEqual(decision, "FAIL_CLOSED")

    def test_non_string_time_fails_closed_deterministically(self):
        data = self.bundle()
        data["evidence_artifacts"][0]["valid_until"] = None
        decision, reasons = evaluate(data)
        self.assertEqual(decision, "FAIL_CLOSED")
        self.assertEqual(reasons, ["invalid evidence time for evidence.p1"])

    def test_invalid_evaluation_time_fails_closed(self):
        data = self.bundle()
        data["evaluation_time"] = "not-a-time"
        decision, reasons = evaluate(data)
        self.assertEqual(decision, "FAIL_CLOSED")
        self.assertEqual(reasons, ["invalid evaluation time"])

    def test_change_can_require_reauthorization(self):
        data = self.bundle()
        data["change_impact"]["disposition"] = "REAUTHORIZATION_REQUIRED"
        decision, _ = evaluate(data)
        self.assertEqual(decision, "REAUTHORIZATION_REQUIRED")

    def test_incomplete_retirement_fails_closed(self):
        data = self.bundle()
        data["operating_disposition"]["state"] = "RETIRED"
        data["operating_disposition"]["retirement_complete"] = False
        decision, _ = evaluate(data)
        self.assertEqual(decision, "FAIL_CLOSED")

    def test_protective_recovery_path(self):
        path = [
            "CONTAINED",
            "INVESTIGATION",
            "RECOVERY_PENDING",
            "RECONSTITUTION",
            "REVERIFICATION",
            "REAUTHORIZATION_REQUIRED",
            "AUTHORIZED",
            "PERMITTED",
        ]
        for source, target in zip(path, path[1:]):
            self.assertTrue(transition_allowed(source, target), f"{source} -> {target}")

    def test_invalid_shortcut_is_rejected(self):
        self.assertFalse(transition_allowed("CONTAINED", "PERMITTED"))
        self.assertFalse(transition_allowed("RECONSTITUTION", "PERMITTED"))

if __name__ == "__main__":
    unittest.main()
