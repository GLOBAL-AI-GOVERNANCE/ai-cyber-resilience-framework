# Compatibility: v0.1.1 to v0.2.0

**Status:** Compatibility assessment for the unreleased v0.2.0 candidate. Steward review under the v0.2.0 release gate (G6) recorded 2026-10-18. Applies only if v0.2.0 is released. v0.2.0 is not released.

## Unchanged

- All v0.1.1 templates, the NIST SP 800-160 mapping, the threat model, the principles, the article, and three of the four checklists are unchanged in substance.
- v0.1.1 had no machine-readable schemas, so no schema contract can break.

## Changed meaning

- `checklists/ai-compressed-readiness-checklist.md` tightens scoring. **Strong** now requires current, relevant verification evidence. **N/A** requires a written applicability rationale. A new "Critical exceptions and evidence limits" section must be completed before an overall label, and an overall label cannot hide an open critical exception.
- Effect: a v0.1.1 assessment that rated an item Strong without current verification evidence would rate Partial or Weak under v0.2.0. Labels from the two versions are not directly comparable.

## Added

- Continuous Assurance Thread documents, nine `1.0.0` schemas with a digest catalog, a synthetic reference bundle, a guided assessment, dependency-exit evidence, an optional crypto-agility thread, and an attack-phase mitigation matrix. All are additive.
- Standard JSON Schema validation (`tools/validate_schemas_standard.py`) with a hash-locked engine in `requirements-schema.lock`. It is required in repository CI and optional for users. The core validators remain dependency-free.

## Schema compatibility

- Schema compatibility follows the semantic-versioning rules in `docs/schema-versioning-and-validation.md`. A major version change can break consumers. Minor and patch changes are intended not to.
- Published schema contracts are not edited in place. Any schema byte change gets a new catalog digest, and a meaning change gets a new `schema_version`.
- Consumers should record the `schema_version` and catalog digest they rely on, and reject unknown major versions.

## What downstream users must change

- Re-score Strong and N/A items against the tightened rules before comparing results across versions.
- Pin to a tag. `main` can differ from any release.

## Not guaranteed

- Stability of `1.0.0` schemas beyond the documented versioning policy.
- That a schema-valid artifact is semantically correct or describes a real system. See the validation layers in `docs/schema-versioning-and-validation.md`.
- Fitness, conformance, or effectiveness of any assessed system.
