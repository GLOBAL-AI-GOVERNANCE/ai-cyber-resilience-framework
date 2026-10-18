# Compatibility: v0.1.1 to v0.2.0

**Status:** Compatibility assessment for the unreleased v0.2.0 candidate. Steward review under the v0.2.0 release gate (G6): PENDING STEWARD DECISION. Applies only if v0.2.0 is released.

## Unchanged

- All v0.1.1 templates, the NIST SP 800-160 mapping, the threat model, the principles, the article, and three of the four checklists are unchanged in substance.
- v0.1.1 had no machine-readable schemas, so no schema contract can break.

## Changed meaning

- `checklists/ai-compressed-readiness-checklist.md` tightens scoring. **Strong** now requires current, relevant verification evidence. **N/A** requires a written applicability rationale. A new "Critical exceptions and evidence limits" section must be completed before an overall label, and an overall label cannot hide an open critical exception.
- Effect: a v0.1.1 assessment that rated an item Strong without current verification evidence would rate Partial or Weak under v0.2.0. Labels from the two versions are not directly comparable.

## Added

- Continuous Assurance Thread documents, nine `1.0.0` schemas with a digest catalog, a synthetic reference bundle, a guided assessment, dependency-exit evidence, an optional crypto-agility thread, and an attack-phase mitigation matrix. All are additive.

## What downstream users must change

- Re-score Strong and N/A items against the tightened rules before comparing results across versions.
- Pin to a tag. `main` can differ from any release.

## Not guaranteed

- Stability of `1.0.0` schemas beyond the documented versioning policy.
- That any validator in this repository enforces every schema keyword. See `docs/schema-versioning-and-validation.md`.
- Fitness, conformance, or effectiveness of any assessed system.
