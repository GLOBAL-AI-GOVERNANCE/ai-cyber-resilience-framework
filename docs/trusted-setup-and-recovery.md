# Trusted Setup and Recovery

Recovery means re-establishing sufficient trust for the intended mission state, not merely restoring service.

## Trusted setup record

A trusted setup should identify at minimum:

- system and configuration identifiers;
- architecture and realm-model digests;
- hardware identifiers;
- firmware, software, model, and reference-data identifiers;
- authorized-flow digest;
- authority references;
- evidence-manifest digest; and
- recovery-basis identifier.

These fields form the `System Configuration Passport`.

## Recovery evidence

A recovery path should answer:

1. Which trusted basis is being restored?
2. Which components were replaced, rebuilt, or reimaged?
3. Which evidence survived and which evidence was invalidated?
4. Which keys, credentials, policies, models, or reference data changed?
5. Which invariants require new verification?
6. Who has authority to return the system to an authorized state?

A configuration mismatch after recovery requires renewed evaluation. The reference model does not permit a prior `PERMITTED` disposition to carry forward by default.

## Recovery boundary

Passing repository tests demonstrates only that the reference state machine and example artifacts obey these declared rules. Real recovery requires environment-specific evidence and authorized validation.
