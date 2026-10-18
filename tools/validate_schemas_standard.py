#!/usr/bin/env python3
"""Validate ACRF schemas and canonical instances with a full JSON Schema Draft 2020-12 engine.

Requires the hash-locked dependencies in requirements-schema.lock. This check does not
replace the repository semantic validators; it adds standard structural validation.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DRAFT_2020_12 = "https://json-schema.org/draft/2020-12/schema"
CATALOG = ROOT / "schemas" / "schema-catalog.json"
BUNDLE = ROOT / "examples" / "secure-inference-cell" / "reference-bundle.json"
REQUIRED_FORMATS = ("date", "date-time")


class StandardValidationError(Exception):
    pass


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_engine():
    try:
        import jsonschema
    except ImportError as exc:
        raise StandardValidationError(
            "jsonschema is not installed; install requirements-schema.lock with "
            "python3 -m pip install --require-hashes --no-deps -r requirements-schema.lock"
        ) from exc
    validator_class = jsonschema.Draft202012Validator
    checker = validator_class.FORMAT_CHECKER
    missing = [name for name in REQUIRED_FORMATS if name not in checker.checkers]
    if missing:
        raise StandardValidationError(f"format assertion unavailable for: {', '.join(missing)}")
    return validator_class, checker


def guided_artifact() -> dict[str, Any]:
    from guided_assessment import assess

    return assess(read_json(ROOT / "examples" / "guided-assessment" / "answers.json"))


def instance_map() -> dict[str, list[tuple[str, Any]]]:
    """Map each catalog schema to the canonical instances it governs."""
    bundle = read_json(BUNDLE)
    bundle_label = "examples/secure-inference-cell/reference-bundle.json"

    def items(key: str) -> list[tuple[str, Any]]:
        return [(f"{bundle_label}#/{key}/{index}", value) for index, value in enumerate(bundle[key])]

    exits = ("synthetic-exit-record.json", "synthetic-exit-failed.json")
    return {
        "schemas/system-claim.schema.json": items("system_claims"),
        "schemas/security-invariant.schema.json": items("security_invariants"),
        "schemas/evidence-artifact.schema.json": items("evidence_artifacts"),
        "schemas/configuration-passport.schema.json": [
            (f"{bundle_label}#/configuration_passport", bundle["configuration_passport"])
        ],
        "schemas/change-impact.schema.json": [(f"{bundle_label}#/change_impact", bundle["change_impact"])],
        "schemas/operating-disposition.schema.json": [
            (f"{bundle_label}#/operating_disposition", bundle["operating_disposition"])
        ],
        "schemas/crypto-agility-thread.schema.json": [
            (
                "examples/crypto-agility/synthetic-reference-thread.json",
                read_json(ROOT / "examples" / "crypto-agility" / "synthetic-reference-thread.json"),
            )
        ],
        "schemas/dependency-exit-evidence.schema.json": [
            (f"examples/dependency-exit/{name}", read_json(ROOT / "examples" / "dependency-exit" / name))
            for name in exits
        ],
        "schemas/guided-assessment-artifact.schema.json": [
            ("generated from examples/guided-assessment/answers.json", guided_artifact())
        ],
    }


def catalog_schemas() -> list[str]:
    entries = read_json(CATALOG)["entries"]
    paths = []
    for entry in entries:
        rel = entry["schema_file"]
        digest = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        if digest != entry["content_sha256"]:
            raise StandardValidationError(f"catalog digest mismatch: {rel}")
        paths.append(rel)
    on_disk = sorted(path.relative_to(ROOT).as_posix() for path in (ROOT / "schemas").glob("*.schema.json"))
    if sorted(paths) != on_disk:
        raise StandardValidationError("schema catalog does not exactly cover schemas/*.schema.json")
    return paths


def errors_for(validator, instance: Any) -> list[str]:
    return [
        f"{'/'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path))
    ]


def run() -> tuple[int, int]:
    validator_class, checker = load_engine()
    schemas = catalog_schemas()
    mapping = instance_map()

    unmapped = sorted(set(schemas) - set(mapping))
    unknown = sorted(set(mapping) - set(schemas))
    if unmapped or unknown:
        raise StandardValidationError(f"schema/instance mapping incomplete: unmapped={unmapped} unknown={unknown}")

    failures: list[str] = []
    instance_count = 0
    for rel in schemas:
        schema = read_json(ROOT / rel)
        if schema.get("$schema") != DRAFT_2020_12:
            failures.append(f"{rel}: $schema is not Draft 2020-12")
            continue
        try:
            validator_class.check_schema(schema, format_checker=checker)
        except Exception as exc:  # jsonschema.SchemaError
            failures.append(f"{rel}: not metaschema-valid: {getattr(exc, 'message', exc)}")
            continue
        validator = validator_class(schema, format_checker=checker)
        if not mapping[rel]:
            failures.append(f"{rel}: no canonical instance")
        for label, instance in mapping[rel]:
            instance_count += 1
            failures.extend(f"{label} against {rel}: {message}" for message in errors_for(validator, instance))

    if failures:
        raise StandardValidationError("\n".join(failures))
    return len(schemas), instance_count


def main() -> int:
    try:
        schema_count, instance_count = run()
    except StandardValidationError as exc:
        print(f"Standard JSON Schema validation failed:\n{exc}", file=sys.stderr)
        return 1
    print(
        "Standard JSON Schema validation passed: "
        f"{schema_count} schemas metaschema-valid under Draft 2020-12; "
        f"{instance_count} canonical instances valid; formats asserted: {', '.join(REQUIRED_FORMATS)}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
