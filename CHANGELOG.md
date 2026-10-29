# Changelog

## v0.2.0 — Continuous Assurance Thread

Released 2026-10-29.

### Documentation and release assets

- Added a Release Assets workflow. When a release is published, it reruns the framework checks on the tag, builds a source archive with SHA-256 checksums, attests build provenance, and attaches the files without replacing existing assets. Manual runs keep the output as a workflow artifact.
- Added a public-safe AI-compressed attack-phase mitigation reference. It states intended architectural effects and claim limits. `authority_effect: NONE`. Included in v0.2.0.
- Bounded capability, containment, and reference-decision wording, and stated in the README, claims boundary, state model, and validator output that `PERMITTED` is a reference-model output, not an operating authorization. Included in v0.2.0.
- Added standard JSON Schema Draft 2020-12 validation of all nine schemas and their canonical instances, with a hash-locked engine required in CI, and documented the three validation layers. Schemas and catalog digests are unchanged. Included in v0.2.0.
- Recorded the G3 to G6 steward decisions in the v0.2.0 release gate, added a schema-compatibility note, and added a review kit for the qualified crypto-agility review required by G7. Release gate closed for v0.2.0.
- Linked the separate Containment Ledger review instrument. Containment Ledger remains a separate instrument; a ledger record is not certification or operational authorization.

### Continuous assurance

- Clarified qualitative readiness scoring so Strong requires current, relevant verification evidence, N/A requires an applicability rationale, and an overall label cannot conceal a failed or unevidenced critical isolation or recovery boundary. Added one synthetic decision-package walkthrough that reuses the existing templates. Documentation and synthetic walkthrough; does not authorize operation.

- Added a configuration-bound Continuous Assurance Thread from claims and invariants through evidence, operating disposition, recovery, reauthorization, and retirement.
- Added nine machine-readable assurance schemas plus a digest-verified schema catalog.
- Added a separate System Configuration Passport; Agent Trust Passport semantics remain outside this repository and are not redefined.
- Added explicit evidence invalidation states and first-class ChangeImpact semantics.
- Added a protective-state model that prevents recovery from silently returning directly to permitted operation.
- Added a synthetic secure-inference-cell reference bundle and fail-closed evaluator.
- Added adversarial regression tests for unknown flows, evidence expiry, configuration mismatch, revoked authority, missing P1–P5 properties, unsupported schemas, superseded evidence, reauthorization, and incomplete retirement.
- Added a dependency-free local guided-assessment path with a deterministic, schema-backed, non-authorizing assurance artifact.
- Added an optional synthetic quantum-era cryptographic resilience / crypto-agility reference thread with an explicit human release boundary; it does not evidence a real migration or deployment.
- Bound current evidence to the named recovery basis. The evaluator fails closed on a missing recovery basis, and evidence not bound to that basis cannot support permitted operation.
- Added dependency-exit evidence: a schema, synthetic passing and failed exit records, a validator, and regressions. It does not evidence a real dependency exit.
- Added a public-safe machine-only release-readiness record and strengthened deterministic consistency regressions for duplicate identifiers, evidence results, disposition references, system identity, and malformed times.
- Published as v0.2.0.

## v0.1.1 — Public Identity and Verification

- Aligned the public title with the repository name: AI Cyber Resilience Framework.
- Preserved “AI-compressed cyberattacks” as the threat thesis rather than a competing product name.
- Corrected stale repository URLs and citation metadata.
- Added a five-minute Start Here path and a defined finished artifact package.
- Added explicit evidence, maturity, authorization, and human-judgment boundaries.
- Revalidated the five listed public source pages on 2026-07-29.
- Added hosted framework checks for internal links, identity, citation consistency, source-log discipline, workflow pins, and repository hygiene.
- Updated security-handling guidance for sensitive concerns.

## v0.1.0 — Initial Public Defensive Framework

Initial public release of AI Cyber Resilience Framework.

Included:
- Public-safe defensive article
- Threat model
- NIST SP 800-160 mapping
- Structural security principles
- Readiness and architecture checklists
- Boundary, flow, attack-path, telemetry, and evidence-card templates
- Sample mission-system boundary map
- Public-safe disclaimer, contribution guidance, security policy, citation metadata, and license
