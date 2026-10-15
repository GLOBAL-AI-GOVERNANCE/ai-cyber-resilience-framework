#!/usr/bin/env python3
"""Validate a dependency exit evidence record. Standard library only. Fail closed."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "dependency-exit-evidence.schema.json"
DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
TIMESTAMP = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")


class ContractError(Exception):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def validate_dependency_exit(record: dict[str, Any]) -> dict[str, Any]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    _require(isinstance(record, dict), "record must be an object")
    missing = set(schema["required"]) - set(record)
    _require(not missing, f"missing required fields: {', '.join(sorted(missing))}")
    extra = set(record) - set(schema["properties"])
    _require(not extra, f"unsupported fields: {', '.join(sorted(extra))}")
    _require(record.get("schema_version") == "1.0.0", "schema_version mismatch")
    for key in ("dependency_id", "subject_id", "dependency_type", "owner_ref", "portability_basis"):
        _require(isinstance(record.get(key), str) and record[key].strip(), f"{key} must be a nonempty string")
    _require(DIGEST.fullmatch(str(record.get("configuration_digest", ""))), "configuration_digest malformed")
    for key in ("exercise_started_at", "exercise_completed_at"):
        _require(TIMESTAMP.fullmatch(str(record.get(key, ""))), f"{key} must use YYYY-MM-DDTHH:MM:SSZ")
    _require(record["exercise_completed_at"] >= record["exercise_started_at"], "exercise completion precedes start")
    for key in ("fallback_available", "fallback_demonstrated", "recovery_demonstrated", "data_or_state_recovered"):
        _require(isinstance(record.get(key), bool), f"{key} must be a boolean")
    for key in ("residual_dependencies", "limitations", "evidence_refs"):
        _require(isinstance(record.get(key), list), f"{key} must be an array")
        for item in record[key]:
            _require(isinstance(item, str) and item.strip(), f"{key} must contain nonempty strings")
    _require(record["limitations"] and record["evidence_refs"], "limitations and evidence refs are required")
    for key in ("replacement_ref", "switching_procedure_ref", "recovery_basis_ref", "observed_switch_time"):
        _require(isinstance(record.get(key), str), f"{key} must be a string")
    _require(record.get("outcome") in {"SUCCESS", "PARTIAL", "FAILED"}, "unsupported outcome")
    _require(record.get("reference_only") is True, "reference_only must be true")
    _require(record.get("human_review_required") is True, "human_review_required must be true")
    _require(record.get("authority_effect") == "NONE", "authority_effect must be NONE")
    if record["outcome"] == "SUCCESS":
        _require(record["replacement_ref"].strip(), "SUCCESS requires a replacement reference")
        _require(record["switching_procedure_ref"].strip(), "SUCCESS requires a switching procedure reference")
        _require(record["recovery_basis_ref"].strip(), "SUCCESS requires a recovery basis reference")
        _require(record["observed_switch_time"].strip(), "SUCCESS requires an observed switch time")
        _require(record["fallback_available"] is True, "SUCCESS requires an available fallback")
        _require(record["fallback_demonstrated"] is True, "SUCCESS requires a demonstrated fallback")
        _require(record["recovery_demonstrated"] is True, "SUCCESS requires demonstrated recovery")
        _require(record["data_or_state_recovered"] is True, "SUCCESS requires recovered data or state")
        _require(record["residual_dependencies"] == [], "SUCCESS cannot retain a critical residual dependency")
    return {
        "valid": True,
        "outcome": record["outcome"],
        "reference_only": True,
        "authority_effect": "NONE",
        "note": "Bounded dependency-exit exercise only. It does not establish supplier independence, operational resilience, production safety, or business continuity.",
    }


def main() -> None:
    import sys
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "examples" / "dependency-exit" / "synthetic-exit-record.json"
    record = json.loads(path.read_text(encoding="utf-8"))
    print(json.dumps(validate_dependency_exit(record), sort_keys=True))


if __name__ == "__main__":
    main()
