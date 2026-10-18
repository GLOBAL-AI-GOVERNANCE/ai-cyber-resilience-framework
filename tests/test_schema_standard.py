from __future__ import annotations

import copy
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import validate_schemas_standard as standard  # noqa: E402



def engine_usable() -> bool:
    try:
        standard.load_engine()
    except standard.StandardValidationError:
        return False
    return True


AVAILABLE = engine_usable()
REQUIRED = os.environ.get("ACRF_REQUIRE_STANDARD_SCHEMA") == "1"
REASON = "hash-locked jsonschema engine unavailable; install requirements-schema.lock (required in CI)"


class StandardEngineRequirementTests(unittest.TestCase):
    def test_engine_present_when_required(self):
        if REQUIRED:
            self.assertTrue(AVAILABLE, "ACRF_REQUIRE_STANDARD_SCHEMA=1 but the jsonschema engine is unavailable")

    def test_missing_engine_is_a_failure_not_a_pass(self):
        if AVAILABLE:
            self.skipTest("jsonschema engine available")
        with self.assertRaises(standard.StandardValidationError):
            standard.load_engine()


@unittest.skipUnless(AVAILABLE or REQUIRED, REASON)
class StandardSchemaValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator_class, cls.checker = standard.load_engine()
        cls.mapping = standard.instance_map()

    def validator(self, rel):
        return self.validator_class(standard.read_json(ROOT / rel), format_checker=self.checker)

    def first(self, rel):
        return copy.deepcopy(self.mapping[rel][0][1])

    def assert_rejected(self, rel, instance):
        self.assertTrue(standard.errors_for(self.validator(rel), instance), f"{rel} accepted an invalid instance")

    def test_all_schemas_and_canonical_instances_pass(self):
        schema_count, instance_count = standard.run()
        self.assertEqual(schema_count, 9)
        self.assertGreaterEqual(instance_count, 9)

    def test_every_catalog_schema_has_a_canonical_instance(self):
        schemas = standard.catalog_schemas()
        self.assertEqual(sorted(schemas), sorted(self.mapping))
        for rel in schemas:
            self.assertTrue(self.mapping[rel], rel)

    def test_missing_required_field_is_rejected(self):
        rel = "schemas/operating-disposition.schema.json"
        instance = self.first(rel)
        del instance["state"]
        self.assert_rejected(rel, instance)

    def test_wrong_type_is_rejected(self):
        rel = "schemas/dependency-exit-evidence.schema.json"
        instance = self.first(rel)
        instance["human_review_required"] = "true"
        self.assert_rejected(rel, instance)

    def test_unknown_enum_value_is_rejected(self):
        rel = "schemas/operating-disposition.schema.json"
        instance = self.first(rel)
        instance["state"] = "APPROVED_FOR_PRODUCTION"
        self.assert_rejected(rel, instance)

    def test_const_boundary_is_enforced(self):
        rel = "schemas/crypto-agility-thread.schema.json"
        instance = self.first(rel)
        instance["human_release_boundary"]["release_tag_created"] = True
        self.assert_rejected(rel, instance)

    def test_additional_property_is_rejected(self):
        rel = "schemas/guided-assessment-artifact.schema.json"
        instance = self.first(rel)
        instance["operating_authorization"] = True
        self.assert_rejected(rel, instance)

    def test_malformed_date_time_is_rejected(self):
        rel = "schemas/operating-disposition.schema.json"
        instance = self.first(rel)
        instance["issued_at"] = "2026-13-45T99:00:00Z"
        self.assert_rejected(rel, instance)

    def test_malformed_date_is_rejected(self):
        rel = "schemas/crypto-agility-thread.schema.json"
        instance = self.first(rel)
        instance["long_term_confidentiality_horizon"]["review_by"] = "2027-02-30"
        self.assert_rejected(rel, instance)


if __name__ == "__main__":
    unittest.main()
