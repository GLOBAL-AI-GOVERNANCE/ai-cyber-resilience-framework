# Secure AI Infrastructure Application

This document applies the Continuous Assurance Thread to a synthetic high-consequence AI inference cell.

It is a reference engineering example, not a representation of a deployed facility.

## Design input

The engineering pattern is informed by NIST SP 800-160 Vol. 1 Rev. 1 systems-security-engineering principles and by the 2026 secondary synthesis *Engineering Trustworthy Secure AI Infrastructure: How NIST SP 800-160 Design Principles and Life Cycle Processes Make RAND's Secure Inference Data Center Trustworthy and Resilient* by Ron Ross.

The secondary synthesis is used as design input. Public assurance claims in this repository remain bounded by the primary-source and evidence rules in `docs/sources-and-evidence.md`.

## Five required properties

The synthetic cell defines five required properties:

| ID | Property | Assurance question |
|---|---|---|
| P1 | Cross-boundary flow containment | Are cross-realm transactions explicitly bounded, mediated, and fail-closed? |
| P2 | Computational-state confidentiality | Is sensitive computational state protected from unauthorized observation or transfer? |
| P3 | Integrity of inference | Can the system establish that inference inputs, runtime, model/reference data, and outputs remain within the authorized integrity basis? |
| P4 | Assured recovery | Can the system re-establish a known trust basis and produce new evidence after disruption or compromise? |
| P5 | Cross-realm privilege separation | Are privileged authorities separated across realms so one compromise does not silently become universal authority? |

The reference validator requires all P1–P5 invariants before returning `PERMITTED`.

## Bounded transaction

A permitted cross-realm transaction records:

- source realm;
- destination realm;
- message type;
- endpoint;
- maximum size;
- rate limit;
- authority reference;
- allowed protective states; and
- expiration or decommission condition.

A transaction not matching the allowlist is denied and the evaluator returns `CONTAINED`.

## Example scenario

The bundled reference example begins in a fully current `PERMITTED` state.

Synthetic UAT then exercises:

1. unknown cross-realm flow → `CONTAINED`;
2. evidence expiry → `REVERIFICATION_REQUIRED`;
3. boundary-controller/configuration mismatch → `REAUTHORIZATION_REQUIRED`;
4. revoked authority → `REAUTHORIZATION_REQUIRED`;
5. missing P1–P5 invariant → `INCOMPLETE`;
6. unsupported schema version → `FAIL_CLOSED`;
7. recovery re-entry through reconstitution, reverification, and reauthorization;
8. superseded evidence cannot satisfy current assurance.

These are deterministic reference outcomes only. They do not establish the security of any real AI infrastructure.
