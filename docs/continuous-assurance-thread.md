# Continuous Assurance Thread

**Status:** v0.2.0 development candidate. This document is not a release claim, certification, authorization, or proof that a deployed system is trustworthy.

The Continuous Assurance Thread turns structural-security claims into a traceable engineering loop that can survive configuration change, evidence expiry, incident response, recovery, and reauthorization.

```text
Mission need
→ system claim
→ unacceptable loss / claim boundary
→ hazard
→ security constraint
→ system requirement
→ security invariant
→ authorized configuration
→ authority
→ bounded action
→ observation + evidence
→ verification
→ operating disposition
→ contain / recover / reauthorize
→ measure + learn
→ change / retire
↺
```

## Why this exists

A security statement such as “the inference enclave is isolated” is not durable by itself. The statement can become invalid when a boundary controller changes, a firmware image changes, evidence expires, a recovery baseline is replaced, or an authority is revoked.

Continuous assurance therefore binds claims to:

- a specific system configuration;
- named security invariants;
- evidence with provenance and validity;
- current authority;
- a current operating disposition; and
- explicit invalidation and re-entry rules.

## Assurance graph

The minimum graph is:

```text
Loss
→ Hazard
→ Constraint
→ Invariant
→ Boundary
→ Evidence
→ Monitor
→ Operating Disposition
```

Every edge is reviewable. Missing or stale edges do not silently inherit confidence from historical approvals.

## Three-state discipline

Historical decisions, current verification, and current operation are distinct.

A system may have:

- a historically issued approval;
- a current verification state of `CONFIGURATION_MISMATCH`; and
- an operating disposition of `REAUTHORIZATION_REQUIRED`.

The historical decision is preserved. It is not rewritten to make the current state look cleaner.

## Evidence states

Evidence uses explicit state:

- `CURRENT`
- `STALE`
- `SUPERSEDED`
- `ASSUMPTION_INVALID`
- `CONFIGURATION_MISMATCH`
- `REVERIFICATION_REQUIRED`

Only `CURRENT` evidence bound to the current configuration is eligible to support a `PERMITTED` disposition.

## Fail-closed rule

Unknown flows, unsupported schema versions, revoked authority, expired evidence, configuration mismatch, incomplete required invariants, and invalid recovery basis are not treated as “probably okay.”

The reference validator returns a non-permitted decision and records why.

## Scope boundary

This repository validates the internal consistency of reference artifacts and the deterministic rules encoded here. It does not independently validate a real system, prove control effectiveness, authorize operation, or replace qualified systems-security engineering judgment.
