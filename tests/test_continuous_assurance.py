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

    def test_recovery_succession_and_requalification(self):
        trusted_basis = "recovery-basis-r1"
        trusted = self.bundle()
        self.assertEqual(trusted["configuration_passport"]["recovery_basis_id"], trusted_basis)
        historical_decision, _ = evaluate(trusted)
        self.assertEqual(historical_decision, "PERMITTED")
        historical = {
            "config_id": trusted["configuration_passport"]["config_id"],
            "decision": historical_decision,
            "disposition_id": trusted["operating_disposition"]["disposition_id"],
            "recovery_basis_id": trusted_basis,
        }

        failed = self.bundle()
        failed["configuration_passport"]["firmware_software_model_ids"] = [
            "synthetic-fw-1",
            "synthetic-runtime-1",
            "synthetic-model-2",
        ]
        failed["change_impact"].update(
            {
                "affected_claim_ids": ["claim.p3"],
                "affected_evidence_ids": ["evidence.p3"],
                "affected_invariant_ids": ["invariant.p3"],
                "change_id": "change.synthetic.failed-update",
                "changed_elements": ["synthetic-model-1"],
                "disposition": "REVERIFICATION_REQUIRED",
                "prior_config_id": "cfg-sic-001-r1",
                "proposed_config_id": "cfg-sic-001-r2",
                "rationale": "Synthetic model replacement failed verification.",
            }
        )
        failed["evidence_artifacts"][2]["result"] = "FAIL"
        failed["evidence_artifacts"][2]["state"] = "REVERIFICATION_REQUIRED"
        failed["operating_disposition"]["state"] = "CONTAINED"
        contained, contained_reasons = evaluate(failed)
        self.assertEqual(contained, "CONTAINED")
        self.assertTrue(any("result is not PASS" in reason or "REVERIFICATION" in reason or "operating state" in reason for reason in contained_reasons))
        self.assertNotEqual(contained, historical["decision"])

        path = [
            "PERMITTED",
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
        self.assertFalse(transition_allowed("CONTAINED", "PERMITTED"))
        self.assertFalse(transition_allowed("RECOVERY_PENDING", "PERMITTED"))
        self.assertFalse(transition_allowed("RECONSTITUTION", "PERMITTED"))

        restoring = self.bundle()
        self.assertEqual(restoring["configuration_passport"]["recovery_basis_id"], trusted_basis)
        restoring["evidence_artifacts"][2]["result"] = "FAIL"
        restoring["evidence_artifacts"][2]["state"] = "SUPERSEDED"
        restoring["operating_disposition"]["state"] = "RECONSTITUTION"
        restoring["change_impact"].update(
            {
                "affected_evidence_ids": ["evidence.p3"],
                "change_id": "change.synthetic.restore-basis",
                "changed_elements": ["recovery_basis_id"],
                "disposition": "REAUTHORIZATION_REQUIRED",
                "prior_config_id": "cfg-sic-001-r2",
                "proposed_config_id": "cfg-sic-001-r1",
                "rationale": "Synthetic restoration to the named trusted recovery basis before requalification.",
            }
        )
        self.assertEqual(evaluate(restoring)[0], "CONTAINED")
        retained = [
            item["evidence_id"]
            for item in restoring["evidence_artifacts"]
            if item["state"] == "CURRENT" and item["result"] == "PASS" and trusted_basis in item["dependencies"]
        ]
        invalidated = [
            item["evidence_id"]
            for item in restoring["evidence_artifacts"]
            if item["state"] != "CURRENT" or item["result"] != "PASS"
        ]
        self.assertEqual(retained, ["evidence.p1", "evidence.p2", "evidence.p4", "evidence.p5"])
        self.assertEqual(invalidated, ["evidence.p3"])

        premature = copy.deepcopy(restoring)
        premature["operating_disposition"]["state"] = "PERMITTED"
        premature_decision, _ = evaluate(premature)
        self.assertEqual(premature_decision, "REAUTHORIZATION_REQUIRED")
        self.assertNotEqual(premature_decision, historical["decision"])

        qualified = self.bundle()
        replacement = qualified["evidence_artifacts"][2]
        replacement["artifact_digest"] = "sha256:" + ("ab" * 32)
        replacement["assumptions"] = [
            "Synthetic reference evidence only. This records no real human approval and grants no operating authority."
        ]
        replacement["provenance"] = "Synthetic requalification evidence for recovery-basis-r1."
        replacement["result"] = "PASS"
        replacement["state"] = "CURRENT"
        qualified["configuration_passport"]["governance_decision_id"] = "decision.synthetic.requalification"
        qualified["operating_disposition"]["reasons"] = [
            "Synthetic requalification assumptions only. No operating authority is granted."
        ]
        qualified["operating_disposition"]["state"] = "PERMITTED"
        qualified["change_impact"].update(
            {
                "change_id": "change.synthetic.requalified",
                "disposition": "NO_IMPACT",
                "prior_config_id": "cfg-sic-001-r1",
                "proposed_config_id": "cfg-sic-001-r1",
                "rationale": "Synthetic evidence was replaced for the named recovery basis.",
            }
        )
        self.assertEqual(evaluate(qualified)[0], "PERMITTED")
        withheld = copy.deepcopy(qualified)
        withheld["evidence_artifacts"][2]["result"] = "FAIL"
        self.assertEqual(evaluate(withheld)[0], "REVERIFICATION_REQUIRED")

        stale = self.bundle()
        stale["evidence_artifacts"][0]["state"] = "STALE"
        self.assertEqual(evaluate(stale)[0], "REVERIFICATION_REQUIRED")

        mismatched_basis = self.bundle()
        mismatched_basis["configuration_passport"]["recovery_basis_id"] = "recovery-basis-untrusted"
        mismatched_decision, mismatched_reasons = evaluate(mismatched_basis)
        self.assertEqual(mismatched_decision, "REAUTHORIZATION_REQUIRED")
        self.assertTrue(any("not bound to recovery basis" in reason for reason in mismatched_reasons))

        wrong_subject = self.bundle()
        wrong_subject["configuration_passport"]["system_id"] = "other-system"
        self.assertEqual(evaluate(wrong_subject)[0], "FAIL_CLOSED")

        wrong_configuration = self.bundle()
        wrong_configuration["evidence_artifacts"][0]["configuration_id"] = "cfg-other"
        self.assertEqual(evaluate(wrong_configuration)[0], "REAUTHORIZATION_REQUIRED")

        changed_authority = self.bundle()
        changed_authority["operating_disposition"]["authority_state"] = "REVOKED"
        self.assertEqual(evaluate(changed_authority)[0], "REAUTHORIZATION_REQUIRED")

        unsupported = self.bundle()
        unsupported["schema_version"] = "9.9.9"
        self.assertEqual(evaluate(unsupported)[0], "FAIL_CLOSED")

        missing = self.bundle()
        missing["system_claims"][0]["evidence_ids"] = ["evidence.missing"]
        self.assertEqual(evaluate(missing)[0], "INCOMPLETE")

        blank_basis = self.bundle()
        blank_basis["configuration_passport"]["recovery_basis_id"] = " "
        self.assertEqual(evaluate(blank_basis), ("FAIL_CLOSED", ["invalid recovery basis"]))

        self.assertEqual(evaluate(trusted)[0], historical["decision"])
        self.assertEqual(historical["recovery_basis_id"], trusted_basis)
        self.assertEqual(historical["config_id"], "cfg-sic-001-r1")

if __name__ == "__main__":
    unittest.main()
