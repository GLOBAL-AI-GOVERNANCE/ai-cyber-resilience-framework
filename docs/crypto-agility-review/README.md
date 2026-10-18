# Crypto-Agility Review Kit for the v0.2.0 Candidate

**Document status:** Review procedure for release gate item G7. It does not release v0.2.0, and a completed review does not by itself satisfy G7. v0.2.0 is not released.

Gate item G7 in [`docs/release-gate-v0.2.0.md`](../release-gate-v0.2.0.md) requires the cryptographic planning assumptions in the optional crypto-agility thread to be reviewed with qualified cryptographic and systems engineers. The synthetic horizon and placeholders are not evidence. This kit defines what is reviewed, who qualifies, and what a usable result looks like.

## Candidate under review

| Field | Value |
|---|---|
| Repository | `GLOBAL-AI-GOVERNANCE/ai-cyber-resilience-framework` |
| Review commit | `bf4fab7f590d4d2af6e08596f7a6fb1b0f220c96` |
| Review tree | `2aca76d0a53666361a37b6af197dfa8553aabe98` |
| Manifest | [`manifest.json`](manifest.json) |

The review commit is the `main` commit that contains the reviewed crypto-agility artifacts. Later commits that add this kit or update the gate record do not change any file in the manifest. A review applies only to files whose hashes match the manifest.

## Artifacts

Primary review artifacts:

- [`docs/quantum-era-crypto-agility-reference-thread.md`](../quantum-era-crypto-agility-reference-thread.md)
- [`schemas/crypto-agility-thread.schema.json`](../../schemas/crypto-agility-thread.schema.json)
- [`examples/crypto-agility/synthetic-reference-thread.json`](../../examples/crypto-agility/synthetic-reference-thread.json)

Supporting context, read as needed: the schema catalog, the validators and tests that check the thread, the claims boundary, the validation scope, the readiness record, and the source log. The manifest lists each file.

## Commands

```text
git checkout bf4fab7f590d4d2af6e08596f7a6fb1b0f220c96
git rev-parse HEAD^{tree}
python3 -B tools/validate_assurance.py examples/secure-inference-cell/reference-bundle.json
python3 -m venv .venv
.venv/bin/python -m pip install --require-hashes --no-deps -r requirements-schema.lock
.venv/bin/python -B tools/validate_schemas_standard.py
```

Confirm each manifest hash with `sha256sum` or an equivalent tool. These commands show only that the artifacts are internally consistent. They are not the review.

## Review areas

Record one result per area: `PASS`, `PASS_WITH_FINDINGS`, `FAIL`, or `NOT_REVIEWED`.

| Area | Question |
|---|---|
| R1 Planning assumptions | Are the stated planning assumptions reasonable, explicit, and labelled as assumptions? Is anything assumed that a planner would need to validate first? |
| R2 Dependency-inventory model | Does the inventory structure (dependency, function, owner role, replacement boundary) capture what a crypto-agility plan needs? What is missing? |
| R3 Confidentiality horizon | Is the horizon modelled in a way that ties to data-retention and threat-model needs without implying a recommended value? |
| R4 Migration readiness | Do the readiness states and gap model avoid implying readiness that has not been shown? |
| R5 Downgrade and rollback | Are downgrade and rollback evidence represented so that their absence is visible and cannot be mistaken for a passed test? |
| R6 Transition evidence | Does the thread require evidence of an actual transition before any conclusion, and are placeholders unmistakable? |
| R7 Interoperability | Is interoperability during transition represented adequately for planning? |
| R8 Residual-risk language | Is residual risk stated without minimizing it or implying it is resolved? |
| R9 Human release boundary | Do `NOT_MADE`, `release_tag_created: false`, `human_review_required`, and `authority_effect: NONE` keep every decision with a human? |
| R10 Claims and limitations | Do the document, schema, and fixture avoid every non-claim listed below? Are the limitations sufficient? |

## Not asked

The review is not asked to establish, and must not be reported as establishing:

- quantum-safe or post-quantum security of anything;
- cryptographic invulnerability;
- a real post-quantum deployment or migration;
- migration effectiveness;
- that any algorithm, product, or vendor is superior;
- certification or compliance;
- production or operating authorization.

## Reviewer qualification

The steward must be able to judge, from attributable information, that the reviewers together are competent in:

1. cryptography, or cryptographic migration and agility; and
2. systems engineering, architecture, or deployment transition.

One reviewer may cover both, or several reviewers may each cover one. Each receipt gives a qualification summary sufficient for that judgment, such as role, relevant experience, or public work. Do not include private information beyond what attribution needs.

Each reviewer discloses any relationship with the project, its maintainers, or a vendor with an interest in the outcome. A relationship does not automatically disqualify a reviewer, but it must be disclosed.

Project-authored or otherwise same-control-boundary reviews do not qualify as independent review.

## Severity

| Severity | Meaning |
|---|---|
| High | Wording, a model element, or a missing element that could lead a reader to an unsafe or unsupported cryptographic planning conclusion, or that implies a non-claim listed above. An open high finding prevents G7 from being satisfied. |
| Medium | An omission or ambiguity that weakens planning usefulness without implying an unsupported conclusion. |
| Low | Editorial or consistency issues. |
| Informational | Observations and suggestions. |

## Required review evidence

The review evidence consists of one [`REVIEW_RECEIPT_TEMPLATE.json`](REVIEW_RECEIPT_TEMPLATE.json) per reviewer and one [`FINDING_TEMPLATE.md`](FINDING_TEMPLATE.md) record per finding. Unfavorable findings carry the same evidential weight as a clean result.

## After review

The steward decides whether the receipts, taken together, satisfy G7. That decision is recorded in the gate. Satisfying G7 does not release v0.2.0. G9 (release metadata) and G10 (the steward release decision) remain separate steps.
