# Schema Versioning and Validation Scope

**Status:** Documented versioning and validation scope for the unreleased v0.2.0 candidate. Steward review under the v0.2.0 release gate (G5, G6): PENDING STEWARD DECISION.

## What the repository validators check

`tools/validate_assurance.py`:

- every catalog entry's SHA-256 matches the schema file, and the catalog covers exactly the required schemas;
- each schema declares `$schema` Draft 2020-12;
- each schema's `required` list includes the repository's required-field contract;
- the reference bundle and the crypto-agility fixture contain the required keys, plus selected semantic constants and cross-references.

`tools/validate_dependency_exit.py`:

- required and unexpected top-level fields, `schema_version`, selected non-empty values, and the SUCCESS conditions.

The evaluator (`tools/continuous_assurance.py`) fails closed on unsupported `schema_version` values and on the semantic conditions covered by the unit tests.

## What they do not check

They are not a general JSON Schema engine. They do not apply `type`, `enum`, `const` (except selected values), `pattern`, `format`, `minLength`, `minItems`, `maxItems`, `uniqueItems`, `minimum`, nested `properties`, or `additionalProperties` (except top-level fields for dependency-exit records). The schemas use all of these keywords.

No repository text claims full Draft 2020-12 conformance. Schema catalog digests establish local file consistency only.

## Versioning policy

- Each schema carries `schema_version` in semantic-version form. All current schemas are `1.0.0`.
- **Major:** removing or renaming a required field, narrowing a type, enum, or const, or changing the meaning of a value.
- **Minor:** adding an optional field or widening an enum without changing existing meanings.
- **Patch:** description-only changes.
- A published contract is never edited in place. Any schema byte change updates its catalog digest in the same change.
- Consumers should reject unknown major versions, as the evaluator does.
- `candidate_version` `0.2.0-unreleased` identifies the framework contract set introduced in v0.2.0. It is not a statement about current release state.
