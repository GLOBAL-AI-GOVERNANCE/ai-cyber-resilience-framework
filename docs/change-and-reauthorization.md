# Change and Reauthorization

`ChangeImpact` is a first-class assurance artifact.

A change record names the previous and proposed configuration, changed elements, affected claims, affected invariants, affected evidence, and the required disposition.

## Examples of changes that can invalidate assurance

- boundary-controller replacement;
- firmware or boot-policy update;
- model or inference-runtime replacement;
- reference-data replacement;
- trust-store or signing-key change;
- authorized-flow policy change;
- recovery-image replacement;
- administrator or authority change;
- hardware topology change.

The existence of a historical approval does not answer whether the changed system remains authorized.

## Decision rule

The reference evaluator applies the strongest required outcome:

```text
NO_IMPACT
< REVERIFICATION_REQUIRED
< REAUTHORIZATION_REQUIRED
< RETIREMENT_REQUIRED
```

Human authority may always choose a more conservative outcome.

## Reauthorization packet

A reauthorization packet should include:

- the change record;
- affected claims and invariants;
- invalidated and replacement evidence;
- updated configuration passport;
- verification results;
- unresolved assumptions and exceptions; and
- the proposed operating disposition.

This repository does not grant authority. It makes the authority dependency explicit and machine-checkable in the reference artifacts.
