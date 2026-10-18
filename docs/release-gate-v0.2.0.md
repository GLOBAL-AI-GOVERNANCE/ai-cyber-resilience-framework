# v0.2.0 Release Gate

**v0.2.0 is NOT released. No release decision has been made.** This file defines the release gate and records evidence status for the v0.2.0 candidate. It is not a release decision. v0.1.1 remains the published release.

**Candidate base:** `main` at `bf4fab7`. The release commit is fixed only when the steward records the decision below.

Items marked **MUST** come from existing repository requirements. Items marked **SHOULD** are phrased as recommendations in this repository. **INFORMATIONAL** items record context. A MUST item without evidence is `NOT VERIFIED`. The release does not proceed while any MUST item is `NOT VERIFIED`, PENDING STEWARD DECISION, or WAITING. No item is waived.

## Gate items

| ID | Level | Requirement | Source | Status |
|---|---|---|---|---|
| G1 | MUST | Machine checks pass on the exact release commit: `validate_framework.py`, `validate_assurance.py` on the reference bundle, `validate_schemas_standard.py`, the unit suite, and `git diff --check` against the empty tree. | `docs/release-readiness-v0.2.0-machine.md`, "Exact machine checks"; `docs/schema-versioning-and-validation.md` | SATISFIED on `bf4fab7`. Must be re-run on the release commit. |
| G2 | MUST | Hosted `Framework Checks` pass on the exact release commit. | `.github/workflows/framework-checks.yml`; branch ruleset | SATISFIED on `bf4fab7` (run `39107008003`). Must be re-run on the release commit. |
| G3 | MUST | Steward decision on whether the v0.2.0 scope and terminology are coherent, and whether candidate documents need editorial or domain-expert review. | Readiness record, "Release risks requiring human/steward review", item 1 | SATISFIED. Steward decision recorded 2026-10-18; see [G3 to G6 steward decisions](#g3-to-g6-steward-decisions). |
| G4 | MUST | Review every public claim and the synthetic `PERMITTED` example for likely misreading. Correct or explicitly accept each finding. | Readiness record, item 2 | SATISFIED. Steward decision recorded 2026-10-18; corrections merged in #14 and #16. |
| G5 | MUST | Steward decision on whether dependency-free partial contract checking is sufficient or whether release policy requires full Draft 2020-12 validation in CI. | Readiness record, item 3 | SATISFIED. Steward decision recorded 2026-10-18: full Draft 2020-12 validation is required in CI (#17). |
| G6 | MUST | Review compatibility expectations for v0.1.1 users and the schema-versioning policy. | Readiness record, item 4 | SATISFIED. Steward decision recorded 2026-10-18; see `docs/compatibility-v0.1.1-to-v0.2.0.md` and `docs/schema-versioning-and-validation.md`. |
| G7 | MUST | Review cryptographic planning assumptions with qualified cryptographic and systems engineers. The synthetic horizon and placeholders are not evidence. | Readiness record, item 5 | WAITING EXTERNAL. Requires review by qualified cryptographic and systems engineers. No review evidence exists. Review kit: [`docs/crypto-agility-review/`](crypto-agility-review/README.md). |
| G8 | SHOULD | Re-check fast-moving AI capability and model-availability claims before publication. | `docs/sources-and-evidence.md`, "Use Rule" | SATISFIED (advisory). Re-check performed 2026-10-17; results below. Repeat before any publication. |
| G9 | MUST | Release metadata, changelog, citation and version updates, tag target, and repository cleanliness, confirmed only after a human authorizes release. | Readiness record, item 6 | BLOCKED BY G7. |
| G10 | MUST | Steward release decision recorded, naming the exact release commit. | Readiness record, "Explicit non-decision" | NOT MADE. |
| I1 | INFORMATIONAL | Release-state constants and their promotion. | This file, below | Procedure proposed |

No item is waived. The G3 to G6 steward decisions do not release v0.2.0, do not authorize a tag, and do not substitute for G7.

## G3 to G6 steward decisions

Recorded 2026-10-18 by the repository steward.

**G3, scope and terminology.** The candidate surface was reviewed in full: README, CHANGELOG, `docs/public-safe-claims.md`, the Continuous Assurance, lifecycle, protective-state, trusted-setup and recovery, change and reauthorization, and secure AI infrastructure documents, the crypto-agility thread, the attack-phase mitigation matrix, all schema titles and descriptions, and every `PERMITTED` use. Defects found were corrected in #16: unreleased items listed beside v0.1.1 content, missing candidate artifacts in the README inventory, an ambiguous statement of whether the mitigation matrix belongs to the candidate, and inconsistent "validator" and "evaluator" terminology.

- Scope: if v0.2.0 is released, it is released from `main` and includes every item under both Unreleased sections of the CHANGELOG.
- Specialist review: no editorial or non-cryptographic domain-expert review is required before release. Every candidate artifact is a synthetic reference model with explicit non-claims, and no release claim depends on domain correctness for a real system. Users are told that real conclusions need qualified people, system-specific evidence, and testing.
- This steward review does not substitute for G7. Cryptographic planning assumptions require the qualified review in G7.

**G4, claims.** Basis:

- The 2026-10-17 claims review, with corrections merged in #14.
- A full re-grep on 2026-10-18 after #14, over all tracked documentation, schemas, fixtures, and tools, for: secure, security, resilient, resilience, contain, verified, verification, assurance, permitted, authoriz, cryptographic, crypto, quantum, post-quantum, migration, rollback, recovery, production, compliance, certification, and safe. Of 706 matching lines, 138 are negations or boundaries. The remaining lines are descriptive: names, state and enum identifiers, NIST titles, audience lists, template fields, and design-intent statements with an adjacent limitation.
- `PERMITTED` boundary statements in the README, `docs/public-safe-claims.md`, the protective-state model, the secure AI infrastructure application, and validator output, merged in #16.

No consequential claim remains without an evidence and limitation boundary.

**G5, JSON Schema policy.** Release policy requires full Draft 2020-12 validation in CI. The model is layered, as documented in `docs/schema-versioning-and-validation.md`:

1. Standard JSON Schema validation of all nine schemas and every canonical instance, with format assertion, by a hash-locked engine required in `Framework Checks`.
2. Repository semantic validation.
3. Reference evaluation.

Schemas and catalog digests are unchanged.

**G6, compatibility and versioning.** `docs/compatibility-v0.1.1-to-v0.2.0.md` states:

- v0.1.1 had no machine-readable schemas, and the schemas are additive;
- checklist scoring is tightened, so labels are not comparable without re-scoring;
- users should pin to a tag;
- semantic-versioning rules govern schema compatibility, and published contracts are not edited in place.

The versioning policy in `docs/schema-versioning-and-validation.md` applies. No further compatibility guarantee is made.

## G8 source re-check, 2026-10-17

All five verification URLs in `docs/sources-and-evidence.md` were re-opened. Each loaded with the recorded title. This confirms availability and bounded support only; it is not an independent replication.

| Claim | Where | Result |
|---|---|---|
| Frontier models have demonstrated accelerated vulnerability discovery and multi-step reasoning in controlled contexts. | `docs/public-safe-claims.md`, `docs/threat-model.md`, `DISCLAIMER.md`, the article | Supported. The AI Security Institute evaluation reports controlled cyber-range and CTF results and states that its ranges lack active defenders. |
| The same capability has been demonstrated in "adversarial contexts". | `README.md` "Why This Framework Exists" | Not supported by the cited sources, which describe controlled evaluations and defensive use. Corrected in #14. |
| Comparable capabilities "could" be misused "if" they become broadly accessible. | Same files | Still conditional and supported. Access remains restricted: the expansion post requires partners to meet security requirements and states that general-access safeguards do not yet exist. A later update on the Glasswing page adds tiered access for qualifying security professionals. That is broader, but it is not general availability. |
| Defensive use and the remediation bottleneck. | Source log | Supported by both Glasswing pages. |
| NIST SP 800-160 Vol. 1 Rev. 1 and the NIST blog. | Source log | Pages available, titles unchanged. |

The source log's dated re-check line is a constant that `tools/validate_framework.py` checks. Updating it is a release-metadata step under G9.

## I1 release-state constants

| Location | Value | Class | Catalog digest effect |
|---|---|---|---|
| `schemas/guided-assessment-artifact.schema.json` | `candidate_version` const `0.2.0-unreleased` | Schema semantic constant | Editing changes this schema's catalog digest |
| `schemas/crypto-agility-thread.schema.json` | `candidate_version` const `0.2.0-unreleased`; `human_release_boundary.decision` const `NOT_MADE`; `release_tag_created` const `false` | Schema semantic constant and release-control assertion | Editing changes this schema's catalog digest |
| `examples/crypto-agility/synthetic-reference-thread.json` | the same three values | Synthetic fixture state | None |
| `tools/guided_assessment.py` | emits `candidate_version: 0.2.0-unreleased` | Candidate-state metadata in generated artifacts | None |
| `tools/validate_assurance.py` | requires those values | Release-control assertion | None |
| `tools/validate_framework.py` | requires the README candidate wording | Release-control assertion | None |
| `README.md`, `docs/release-readiness-v0.2.0-machine.md`, `docs/quantum-era-crypto-agility-reference-thread.md`, `docs/ai-compressed-attack-phase-mitigation-matrix.md`, `docs/continuous-assurance-thread.md` | candidate and "not released" wording | Candidate-state metadata | None |

The crypto-agility fixture records no decision time. Its `release_tag_created: false` describes the fixture's own human boundary: the artifact does not create or authorize a tag. It must not be changed to `true`, because a synthetic fixture would then appear to claim that a tag exists.

### Proposed promotion procedure

1. Keep `schema_version` `1.0.0` contracts unchanged for v0.2.0. Treat `candidate_version` `0.2.0-unreleased` as the identifier of the contract that v0.2.0 publishes, not as a statement about release state, and say so in `docs/schema-versioning-and-validation.md`. This leaves catalog digests unchanged.
2. Keep `decision: NOT_MADE` and `release_tag_created: false`. They state that the artifact itself makes no decision and creates no tag, which stays true after a release.
3. Change only prose candidate-state wording and the validator assertions that check it, in the release-metadata pull request under G9.
4. If a later version needs a released-state identifier, introduce it through a new `schema_version` under the versioning policy, with new catalog digests. Do not edit `1.0.0` contracts in place.
