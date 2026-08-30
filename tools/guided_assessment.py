#!/usr/bin/env python3
"""Local guided assessment for the unreleased v0.2.0 candidate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

QUESTIONS = (
    ("P1", "Are cross-boundary flows explicitly authorized and mediated?"),
    ("P2", "Is sensitive computational state confined to authorized realms?"),
    ("P3", "Is execution bound to an identified model, runtime, data, and configuration?"),
    ("P4", "Does recovery return to a named trusted basis before reauthorization?"),
    ("P5", "Is privileged authority separated across realms?"),
)


def assess(source: dict) -> dict:
    answers = source.get("answers", {})
    results = []
    for property_id, question in QUESTIONS:
        answer = answers.get(property_id, {})
        response = answer.get("response", "UNKNOWN")
        evidence_refs = answer.get("evidence_refs", [])
        if response == "YES" and evidence_refs:
            state = "EVIDENCE_REVIEW_REQUIRED"
        elif response == "NO":
            state = "GAP_IDENTIFIED"
        else:
            state = "EVIDENCE_MISSING"
        results.append({
            "property_id": property_id,
            "question": question,
            "response": response,
            "evidence_refs": evidence_refs,
            "state": state,
        })
    return {
        "schema_version": "1.0.0",
        "candidate_version": "0.2.0-unreleased",
        "assessment_id": source["assessment_id"],
        "system_id": source["system_id"],
        "assessment_time": source["assessment_time"],
        "results": results,
        "overall_state": (
            "HUMAN_EVIDENCE_REVIEW_REQUIRED"
            if all(item["state"] == "EVIDENCE_REVIEW_REQUIRED" for item in results)
            else "INCOMPLETE_OR_GAPS"
        ),
        "human_review_required": True,
        "authority_effect": "NONE",
        "limitations": [
            "Responses and evidence references are user-supplied and are not independently verified.",
            "This artifact is not authorization, certification, or proof of control effectiveness.",
        ],
    }


def prompt_source() -> dict:
    print("Open — local guided assessment; no data is transmitted.")
    source = {
        "assessment_id": input("Assessment ID: ").strip(),
        "system_id": input("System ID: ").strip(),
        "assessment_time": input("Assessment time (ISO 8601): ").strip(),
        "answers": {},
    }
    for property_id, question in QUESTIONS:
        print(f"\n{property_id}: {question}")
        response = input("Answer YES, NO, or UNKNOWN: ").strip().upper()
        refs = [item.strip() for item in input("Evidence references (comma-separated): ").split(",") if item.strip()]
        source["answers"][property_id] = {"response": response, "evidence_refs": refs}
    return source


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--answers", type=Path, help="JSON answers; omit for interactive mode")
    parser.add_argument("--out", type=Path, required=True, help="assessment artifact path")
    args = parser.parse_args()
    source = json.loads(args.answers.read_text(encoding="utf-8")) if args.answers else prompt_source()
    artifact = assess(source)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Assess — {artifact['overall_state']}")
    print("Review evidence — human review remains required.")
    print(f"Export assurance artifact — {args.out}")


if __name__ == "__main__":
    main()
