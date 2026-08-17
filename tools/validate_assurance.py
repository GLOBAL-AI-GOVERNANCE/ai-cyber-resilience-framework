#!/usr/bin/env python3
"""Validate ACRF Continuous Assurance schemas, catalog, reference bundle, and decision."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

from continuous_assurance import evaluate

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "schemas" / "schema-catalog.json"
DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")

REQUIRED = {
    "system-claim.schema.json": {
        "schema_version", "claim_id", "system_id", "statement", "criticality",
        "evidence_ids", "status", "assumptions",
    },
    "security-invariant.schema.json": {
        "schema_version", "invariant_id", "property_id", "claim_ids", "statement",
        "protected_property", "enforcement_boundary", "fail_behavior",
        "verification_methods", "authorized_transactions",
    },
    "evidence-artifact.schema.json": {
        "schema_version", "evidence_id", "claim_ids", "artifact_digest",
        "configuration_id", "provenance", "method", "authority", "observed_at",
        "valid_until", "assumptions", "dependencies", "invalidation_triggers",
        "independence_level", "result", "state",
    },
    "configuration-passport.schema.json": {
        "schema_version", "system_id", "config_id", "architecture_version",
        "realm_model_digest", "authorized_flow_digest", "hardware_ids",
        "firmware_software_model_ids", "reference_data_ids",
        "governance_decision_id", "authority_refs", "evidence_manifest_digest",
        "recovery_basis_id", "valid_from", "valid_until", "supersedes",
    },
    "change-impact.schema.json": {
        "schema_version", "change_id", "system_id", "prior_config_id",
        "proposed_config_id", "changed_elements", "affected_claim_ids",
        "affected_invariant_ids", "affected_evidence_ids", "disposition", "rationale",
    },
    "operating-disposition.schema.json": {
        "schema_version", "disposition_id", "system_id", "config_id", "issued_at",
        "state", "reasons", "authority_refs", "authority_state", "evidence_ids",
        "retirement_complete",
    },
}

def fail(message: str) -> None:
    raise SystemExit(f"Continuous assurance validation failed: {message}")

def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{path.relative_to(ROOT)}: {exc}")

def check_schema_catalog() -> None:
    catalog = read_json(CATALOG)
    entries = catalog.get("entries", [])
    names = set()
    for entry in entries:
        rel = entry.get("schema_file", "")
        path = ROOT / rel
        if not path.is_file():
            fail(f"catalog path missing: {rel}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != entry.get("content_sha256"):
            fail(f"schema digest mismatch: {rel}")
        names.add(path.name)
        schema = read_json(path)
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            fail(f"schema draft mismatch: {rel}")
        required = set(schema.get("required", []))
        if not REQUIRED.get(path.name, set()).issubset(required):
            fail(f"required-field contract missing in {rel}")
    if names != set(REQUIRED):
        fail("schema catalog does not exactly cover required assurance schemas")

def require_keys(obj: dict[str, Any], keys: set[str], label: str) -> None:
    missing = sorted(keys - set(obj))
    if missing:
        fail(f"{label} missing keys: {', '.join(missing)}")

def check_bundle(bundle: dict[str, Any]) -> None:
    if bundle.get("schema_version") != "1.0.0":
        fail("reference bundle schema version unsupported")

    for item in bundle.get("system_claims", []):
        require_keys(item, REQUIRED["system-claim.schema.json"], "system claim")
    for item in bundle.get("security_invariants", []):
        require_keys(item, REQUIRED["security-invariant.schema.json"], "security invariant")
    for item in bundle.get("evidence_artifacts", []):
        require_keys(item, REQUIRED["evidence-artifact.schema.json"], "evidence artifact")
        if not DIGEST.fullmatch(item["artifact_digest"]):
            fail(f"invalid evidence digest: {item['evidence_id']}")
    passport = bundle.get("configuration_passport", {})
    require_keys(passport, REQUIRED["configuration-passport.schema.json"], "configuration passport")
    for field in ("realm_model_digest", "authorized_flow_digest", "evidence_manifest_digest"):
        if not DIGEST.fullmatch(passport[field]):
            fail(f"invalid passport digest: {field}")
    require_keys(bundle.get("change_impact", {}), REQUIRED["change-impact.schema.json"], "change impact")
    require_keys(bundle.get("operating_disposition", {}), REQUIRED["operating-disposition.schema.json"], "operating disposition")

    decision, reasons = evaluate(bundle)
    if decision != bundle.get("expected_decision"):
        fail(f"expected {bundle.get('expected_decision')}, got {decision}: {reasons}")

def main() -> None:
    bundle_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "examples" / "secure-inference-cell" / "reference-bundle.json"
    if not bundle_path.is_absolute():
        bundle_path = ROOT / bundle_path
    check_schema_catalog()
    bundle = read_json(bundle_path)
    check_bundle(bundle)
    decision, reasons = evaluate(bundle)
    print(f"Continuous assurance validation passed: decision={decision}; reasons={'; '.join(reasons)}")

if __name__ == "__main__":
    main()
