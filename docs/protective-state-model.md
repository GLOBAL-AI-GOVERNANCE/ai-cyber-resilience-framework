# Protective State Model

The protective-state model prevents a degraded or recovering system from silently returning to normal operation.

```text
UNESTABLISHED
→ TRUST_ESTABLISHMENT
→ AUTHORIZED
→ PERMITTED
```

A permitted system can leave the normal path:

```text
PERMITTED
→ DEGRADED
→ CONTAINED
→ INVESTIGATION
→ RECOVERY_PENDING
→ RECONSTITUTION
→ REVERIFICATION
→ REAUTHORIZATION_REQUIRED
→ AUTHORIZED
→ PERMITTED
```

`RETIRED` is terminal.

## Design rules

1. `PERMITTED` requires current evidence, current configuration binding, valid authority, and the required P1–P5 invariant set.
2. `CONTAINED` is a protective condition, not evidence of successful recovery.
3. `RECONSTITUTION` restores a candidate trusted basis; it does not itself authorize mission operation.
4. `REVERIFICATION` re-establishes evidence.
5. `REAUTHORIZATION_REQUIRED` makes the human authority boundary explicit.
6. Unsupported or unknown transitions fail closed.

The reference Python module exposes `transition_allowed()` so these transition rules can be tested deterministically.
