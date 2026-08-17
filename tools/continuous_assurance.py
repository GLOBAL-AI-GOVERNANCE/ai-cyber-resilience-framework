#!/usr/bin/env python3
"""Deterministic reference evaluator for the ACRF Continuous Assurance Thread."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

SUPPORTED_SCHEMA_VERSION = "1.0.0"
REQUIRED_PROPERTIES = {"P1", "P2", "P3", "P4", "P5"}

ALLOWED_TRANSITIONS = {
    "UNESTABLISHED": {"TRUST_ESTABLISHMENT", "RETIRED"},
    "TRUST_ESTABLISHMENT": {"AUTHORIZED", "CONTAINED", "RETIRED"},
    "AUTHORIZED": {"PERMITTED", "CONTAINED", "RETIRED"},
    "PERMITTED": {"DEGRADED", "CONTAINED", "RETIRED"},
    "DEGRADED": {"CONTAINED", "INVESTIGATION", "RETIRED"},
    "CONTAINED": {"INVESTIGATION", "RECOVERY_PENDING", "RETIRED"},
    "INVESTIGATION": {"RECOVERY_PENDING", "RETIRED"},
    "RECOVERY_PENDING": {"RECONSTITUTION", "RETIRED"},
    "RECONSTITUTION": {"REVERIFICATION", "CONTAINED", "RETIRED"},
    "REVERIFICATION": {"REAUTHORIZATION_REQUIRED", "AUTHORIZED", "CONTAINED", "RETIRED"},
    "REAUTHORIZATION_REQUIRED": {"AUTHORIZED", "CONTAINED", "RETIRED"},
    "RETIRED": set(),
}

DECISION_RANK = {
    "PERMITTED": 0,
    "REVERIFICATION_REQUIRED": 10,
    "REAUTHORIZATION_REQUIRED": 20,
    "INCOMPLETE": 30,
    "CONTAINED": 40,
    "RETIRED": 50,
    "FAIL_CLOSED": 60,
}


def parse_time(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def transition_allowed(source: str, target: str) -> bool:
    return target in ALLOWED_TRANSITIONS.get(source, set())


def _stronger(current: str, candidate: str) -> str:
    return candidate if DECISION_RANK[candidate] > DECISION_RANK[current] else current


def _transaction_allowed(bundle: dict[str, Any]) -> bool:
    request = bundle.get("transaction_request")
    if not request:
        return True

    p1 = next(
        (item for item in bundle.get("security_invariants", []) if item.get("property_id") == "P1"),
        None,
    )
    if not p1:
        return False

    for allowed in p1.get("authorized_transactions", []):
        if (
            request.get("source_realm") == allowed.get("source_realm")
            and request.get("destination_realm") == allowed.get("destination_realm")
            and request.get("message_type") == allowed.get("message_type")
            and request.get("endpoint") == allowed.get("endpoint")
            and request.get("authority_ref") == allowed.get("authority_ref")
            and int(request.get("bytes", 0)) <= int(allowed.get("max_bytes", 0))
            and int(request.get("rate_per_minute", 0)) <= int(allowed.get("rate_per_minute", 0))
            and bundle.get("operating_disposition", {}).get("state") in allowed.get("allowed_states", [])
        ):
            return True
    return False


def evaluate(bundle: dict[str, Any], at_time: str | None = None) -> tuple[str, list[str]]:
    reasons: list[str] = []
    decision = "PERMITTED"

    if bundle.get("schema_version") != SUPPORTED_SCHEMA_VERSION:
        return "FAIL_CLOSED", ["unsupported bundle schema version"]

    passport = bundle.get("configuration_passport", {})
    disposition = bundle.get("operating_disposition", {})
    change = bundle.get("change_impact", {})
    claims = bundle.get("system_claims", [])
    invariants = bundle.get("security_invariants", [])
    evidence = bundle.get("evidence_artifacts", [])

    current_time = parse_time(at_time or bundle.get("evaluation_time", "1970-01-01T00:00:00Z"))

    for artifact_group in (claims, invariants, evidence, [passport, change, disposition]):
        for artifact in artifact_group:
            if artifact.get("schema_version") != SUPPORTED_SCHEMA_VERSION:
                return "FAIL_CLOSED", ["unsupported artifact schema version"]

    property_ids = {item.get("property_id") for item in invariants}
    missing = sorted(REQUIRED_PROPERTIES - property_ids)
    if missing:
        decision = _stronger(decision, "INCOMPLETE")
        reasons.append("missing required properties: " + ",".join(missing))

    config_id = passport.get("config_id")
    if not config_id:
        return "FAIL_CLOSED", ["configuration passport missing config_id"]

    try:
        if not (parse_time(passport["valid_from"]) <= current_time <= parse_time(passport["valid_until"])):
            decision = _stronger(decision, "REAUTHORIZATION_REQUIRED")
            reasons.append("configuration passport outside validity window")
    except (KeyError, ValueError):
        return "FAIL_CLOSED", ["invalid configuration validity interval"]

    if disposition.get("authority_state") != "VALID":
        decision = _stronger(decision, "REAUTHORIZATION_REQUIRED")
        reasons.append("authority is not valid")

    if disposition.get("config_id") != config_id:
        decision = _stronger(decision, "REAUTHORIZATION_REQUIRED")
        reasons.append("operating disposition configuration mismatch")

    evidence_by_id = {item.get("evidence_id"): item for item in evidence}
    claim_ids = {item.get("claim_id") for item in claims}

    for item in claims:
        for evidence_id in item.get("evidence_ids", []):
            if evidence_id not in evidence_by_id:
                decision = _stronger(decision, "INCOMPLETE")
                reasons.append(f"claim {item.get('claim_id')} references missing evidence {evidence_id}")

    for item in evidence:
        if any(cid not in claim_ids for cid in item.get("claim_ids", [])):
            decision = _stronger(decision, "INCOMPLETE")
            reasons.append(f"evidence {item.get('evidence_id')} references unknown claim")
        if item.get("configuration_id") != config_id or item.get("state") == "CONFIGURATION_MISMATCH":
            decision = _stronger(decision, "REAUTHORIZATION_REQUIRED")
            reasons.append(f"evidence {item.get('evidence_id')} configuration mismatch")
            continue
        if item.get("state") != "CURRENT":
            decision = _stronger(decision, "REVERIFICATION_REQUIRED")
            reasons.append(f"evidence {item.get('evidence_id')} is {item.get('state')}")
            continue
        try:
            if current_time > parse_time(item["valid_until"]):
                decision = _stronger(decision, "REVERIFICATION_REQUIRED")
                reasons.append(f"evidence {item.get('evidence_id')} expired")
        except (KeyError, ValueError):
            return "FAIL_CLOSED", [f"invalid evidence time for {item.get('evidence_id')}"]

    change_state = change.get("disposition")
    if change_state == "REVERIFICATION_REQUIRED":
        decision = _stronger(decision, "REVERIFICATION_REQUIRED")
        reasons.append("change impact requires reverification")
    elif change_state == "REAUTHORIZATION_REQUIRED":
        decision = _stronger(decision, "REAUTHORIZATION_REQUIRED")
        reasons.append("change impact requires reauthorization")
    elif change_state == "RETIREMENT_REQUIRED":
        decision = _stronger(decision, "RETIRED")
        reasons.append("change impact requires retirement")
    elif change_state != "NO_IMPACT":
        return "FAIL_CLOSED", ["unsupported change-impact disposition"]

    if disposition.get("state") == "RETIRED":
        if not disposition.get("retirement_complete", False):
            return "FAIL_CLOSED", ["retirement state is incomplete"]
        decision = _stronger(decision, "RETIRED")
        reasons.append("system is retired")
    elif disposition.get("state") != "PERMITTED":
        decision = _stronger(decision, "CONTAINED")
        reasons.append(f"operating state is {disposition.get('state')}")

    if not _transaction_allowed(bundle):
        decision = _stronger(decision, "CONTAINED")
        reasons.append("transaction is not explicitly authorized")

    return decision, reasons or ["all reference assurance conditions satisfied"]
