# v0.2.0 Machine-Only Release-Readiness Record

**Record date:** 2026-08-30
**Assessed candidate base:** `c167d17` (`main` at assessment start), plus the uncommitted machine-readiness changes represented by this record
**Comparison boundary:** published tag `v0.1.1` at `84490f2`
**Scope:** public-safe, offline, deterministic repository checks only
**Machine conclusion:** checks pass for the repository artifact set described below; this is not approval to publish.

## Release boundary

The published identity remains **v0.1.1** in `README.md`, `CITATION.cff`, and `docs/public-safe-claims.md`. Files headed as v0.2.0 are an unreleased development candidate. Current `main` must not be described as an already published v0.2.0.

**The human/steward v0.2.0 release decision has not been made. No v0.2.0 tag or release has been created.** Machine success has no authority effect and cannot make either decision.

## Exact machine checks

Run from the repository root with network access unnecessary:

```text
python -B tools/validate_framework.py
python -B tools/validate_assurance.py examples/secure-inference-cell/reference-bundle.json
python -B -m unittest discover -s tests -v
git diff --check
```

Observed on 2026-08-30:

- Framework validation: pass; 55 repository files checked; identity, links, citation, sources, security, workflow pins, and hygiene verified.
- Assurance validation: pass; synthetic reference decision `PERMITTED`; all encoded reference assurance conditions satisfied.
- Unit tests: pass; 21 tests; includes deterministic negative cases for unknown flow, expiry, configuration and system mismatch, revoked authority, missing P1-P5 properties, unsupported schemas, superseded and failed evidence, duplicate identifiers, missing disposition evidence, malformed time, reauthorization, retirement, recovery shortcuts, guided-assessment boundaries, and the optional synthetic crypto-agility boundary.
- Whitespace/error scan: pass; `git diff --check` reported no errors.

The reference decision `PERMITTED` is an evaluator output over a local synthetic fixture. It is not an operating authorization, containment claim, deployed-effectiveness result, certification, or real incident evidence.

## Changed-surface inventory from v0.1.1

- Public/release framing: `.gitignore`, `.github/workflows/framework-checks.yml`, `README.md`, and `CHANGELOG.md`.
- Continuous-assurance documentation: change and reauthorization, lifecycle thread, protective state, secure AI infrastructure application, trusted setup and recovery, and the core continuous-assurance thread.
- Machine contracts: claim, invariant, evidence, configuration-passport, change-impact, operating-disposition, guided-assessment, and optional crypto-agility schemas, with a digest catalog.
- Reference artifacts: the synthetic secure-inference-cell bundle, deterministic guided-assessment answers, and optional synthetic crypto-agility thread.
- Local tools: framework validation, assurance validation, deterministic continuous-assurance evaluation, and guided assessment.
- Regression surface: continuous-assurance and guided-assessment unit tests.
- Machine-readiness additions: this record and the optional quantum-era crypto-agility reference document, schema, fixture, catalog entry, semantic checks, and bounded regressions.

## Evidence-backed validation strengthening

Baseline checks passed before readiness work, but code inspection showed paths that were not covered by deterministic assertions. The candidate now rejects missing or duplicate claim, invariant, and evidence identifiers; rejects cross-system identity mismatch; prevents a non-`PASS` current artifact from supporting `PERMITTED`; checks disposition evidence references; and converts malformed time values to a deterministic fail-closed result. These checks address internal consistency only.

The optional crypto-agility fixture is checked for an explicit synthetic/reference-only scope, unique dependency identifiers, all six required assurance stages, non-empty limitations/evidence placeholders, and a closed human boundary (`human_review_required: true`, `authority_effect: NONE`, `decision: NOT_MADE`, `release_tag_created: false`).

## Limitations

- The validators check repository structure and encoded semantics; they do not execute JSON Schema as a complete general-purpose schema engine.
- Schema catalog digests establish local file consistency, not provenance, authenticity, publication status, or deployed conformance.
- Tests use synthetic local fixtures and fixed times. They do not inspect a live system, validate user-supplied evidence, exercise a real recovery, or demonstrate containment.
- The guided assessment records user responses and evidence references but does not verify either.
- The crypto-agility artifact does not prove dependency discovery, migration, downgrade protection, rollback behavior, interoperability, post-quantum deployment, quantum-safe superiority, cryptographic invulnerability, certification, or measured effectiveness. It prescribes no vendor.
- No network, GitHub, release service, external authority, or incident source was consulted by this machine-only pass.

## Release risks requiring human/steward review

- Decide whether the v0.2.0 scope and terminology are coherent for a public release and whether candidate documents need editorial or domain-expert review.
- Review every public claim and synthetic `PERMITTED` example for likely reader misinterpretation despite the stated boundaries.
- Decide whether dependency-free partial contract checking is sufficient or whether release policy requires full Draft 2020-12 JSON Schema validation in CI.
- Review compatibility expectations for downstream users of v0.1.1 and the new schema-versioning policy.
- Review cryptographic planning assumptions with qualified cryptographic and systems engineers; the synthetic horizon and placeholders are not evidence.
- Confirm release metadata, changelog text, citation/version updates, tag target, and final repository cleanliness only if a human later authorizes release.

## Explicit non-decision

This record reports machine readiness, not release readiness in the governance sense. It does not authorize a tag, GitHub release, version-identity change, deployment, certification statement, or operational claim. The steward must make and record a separate release decision; until then, v0.2.0 remains an unreleased candidate and v0.1.1 remains the public release.
