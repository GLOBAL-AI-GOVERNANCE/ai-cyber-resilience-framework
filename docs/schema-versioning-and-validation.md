# Schema Versioning and Validation Scope

**Status:** Documented versioning and validation scope for the unreleased v0.2.0 candidate. v0.2.0 is not released.

## Validation layers

Validation has three layers. Each answers a different question, and none substitutes for another.

| Layer | Tool | What it proves | What it does not prove |
|---|---|---|---|
| 1. Standard JSON Schema | `tools/validate_schemas_standard.py` | All nine schemas are valid Draft 2020-12 schemas. Every canonical instance conforms to its schema, including `type`, `enum`, `const`, `pattern`, `format` (`date`, `date-time`), `minLength`, `minItems`, `maxItems`, `uniqueItems`, `minimum`, nested `properties`, and `additionalProperties`. The catalog digests match and cover exactly `schemas/*.schema.json`. | Cross-field or cross-artifact rules, semantic correctness, or anything about a real system |
| 2. Repository semantic validation | `tools/validate_assurance.py`, `tools/validate_dependency_exit.py` | Required-field contracts, selected semantic constants, cross-references between artifacts, catalog digests, and dependency-exit SUCCESS conditions | Full schema conformance on its own; that is layer 1 |
| 3. Reference evaluation | `tools/continuous_assurance.py` and the unit suite | The deterministic decision rules: fail-closed handling of unsupported versions, unknown flows, revoked authority, stale or mismatched evidence, missing invariants, recovery basis, and retirement | That a decision is correct for, or applies to, a real system |

In CI, the reference bundle that yields `PERMITTED` passes all three layers. That result is still a reference-model output over synthetic fixtures. It is not an operating authorization, certification, compliance determination, or evidence of containment or deployed effectiveness.

## Instance mapping

`tools/validate_schemas_standard.py` maps every catalog schema to at least one canonical instance and fails if any schema has none:

| Schema | Canonical instances |
|---|---|
| `system-claim`, `security-invariant`, `evidence-artifact` | Every entry in the corresponding array of `examples/secure-inference-cell/reference-bundle.json` |
| `configuration-passport`, `change-impact`, `operating-disposition` | The corresponding object in the reference bundle |
| `crypto-agility-thread` | `examples/crypto-agility/synthetic-reference-thread.json` |
| `dependency-exit-evidence` | Both records in `examples/dependency-exit/` |
| `guided-assessment-artifact` | The artifact generated from `examples/guided-assessment/answers.json` |

The reference bundle's `transaction_request` has no schema. It is checked by the evaluator only.

Unit tests also check that mutated copies are rejected for a missing required field, a wrong type, an unknown enum value, a violated `const`, an additional property, and malformed `date` and `date-time` values.

## Dependencies and local use

Layer 1 needs `jsonschema` and `rfc3339-validator`. They are pinned exactly, with SHA-256 hashes, in `requirements-schema.lock`:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --require-hashes --no-deps -r requirements-schema.lock
.venv/bin/python -B tools/validate_schemas_standard.py
```

Layers 2 and 3 have no dependencies and run with any Python 3 standard library.

Without the locked engine, the layer 1 unit tests are reported as skipped with an explicit reason, and `tools/validate_schemas_standard.py` exits with a failure. CI installs the lock and sets `ACRF_REQUIRE_STANDARD_SCHEMA=1`, which turns a missing engine into a test failure. All layers run inside the required `Framework Checks` job.

## Versioning policy

- Each schema carries `schema_version` in semantic-version form. All current schemas are `1.0.0`.
- **Major:** removing or renaming a required field, narrowing a type, enum, or const, or changing the meaning of a value.
- **Minor:** adding an optional field or widening an enum without changing existing meanings.
- **Patch:** description-only changes.
- A published contract is never edited in place. Any schema byte change updates its catalog digest in the same change.
- Consumers should reject unknown major versions, as the evaluator does.
- `candidate_version` `0.2.0-unreleased` identifies the framework contract set introduced in v0.2.0. It is not a statement about current release state.
