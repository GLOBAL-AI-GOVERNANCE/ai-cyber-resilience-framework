from __future__ import annotations

import json
import unittest
from pathlib import Path

from tools.validate_dependency_exit import ContractError, validate_dependency_exit

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = json.loads((ROOT / "examples" / "dependency-exit" / "synthetic-exit-record.json").read_text(encoding="utf-8"))
FAILED = json.loads((ROOT / "examples" / "dependency-exit" / "synthetic-exit-failed.json").read_text(encoding="utf-8"))


class DependencyExitTests(unittest.TestCase):
    def test_success_is_reference_only(self) -> None:
        result = validate_dependency_exit(SAMPLE)
        self.assertEqual(result["outcome"], "SUCCESS")
        self.assertEqual(result["authority_effect"], "NONE")

    def test_failed_fixture_cannot_become_success(self) -> None:
        result = validate_dependency_exit(FAILED)
        self.assertEqual(result["outcome"], "FAILED")
        self.assertEqual(result["authority_effect"], "NONE")
        self.assertTrue(result["reference_only"])
        with self.assertRaises(ContractError):
            validate_dependency_exit({**FAILED, "outcome": "SUCCESS"})

    def test_partial_and_failed_keep_incomplete_state(self) -> None:
        partial = {**SAMPLE, "outcome": "PARTIAL", "recovery_demonstrated": False}
        failed = {**SAMPLE, "outcome": "FAILED", "fallback_demonstrated": False, "residual_dependencies": ["undisclosed-component"]}
        self.assertEqual(validate_dependency_exit(partial)["outcome"], "PARTIAL")
        self.assertEqual(validate_dependency_exit(failed)["outcome"], "FAILED")

    def test_success_fails_closed(self) -> None:
        cases = [
            {**SAMPLE, "replacement_ref": ""},
            {**SAMPLE, "fallback_available": False},
            {**SAMPLE, "fallback_demonstrated": False},
            {**SAMPLE, "recovery_demonstrated": False},
            {**SAMPLE, "data_or_state_recovered": False},
            {**SAMPLE, "residual_dependencies": ["critical-residual"]},
            {**SAMPLE, "switching_procedure_ref": ""},
            {**SAMPLE, "authority_effect": "AUTHORIZE"},
            {**SAMPLE, "reference_only": False},
            {**SAMPLE, "human_review_required": False},
            {**SAMPLE, "configuration_digest": "sha256:short"},
        ]
        for record in cases:
            with self.subTest(record=sorted(record)[:1]):
                with self.assertRaises(ContractError):
                    validate_dependency_exit(record)


if __name__ == "__main__":
    unittest.main()
