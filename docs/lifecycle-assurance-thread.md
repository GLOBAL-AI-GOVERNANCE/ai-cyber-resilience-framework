# Lifecycle Assurance Thread

The assurance thread is intended to persist across the system life cycle rather than stop at design review.

## Engineering sequence

```text
Mission / stakeholder needs
→ system requirements
→ architecture and design
→ implementation and integration
→ verification and validation
→ transition
→ operation and maintenance
→ change / reauthorization
→ disposal
```

At every stage, the engineering question is the same:

> What claim is being made, what configuration does it apply to, what evidence supports it, what would invalidate that evidence, and what decision follows now?

## Assurance chain

A claim should be traceable through:

```text
objective
→ loss
→ hazard
→ constraint
→ requirement
→ architecture
→ mechanism
→ implementation
→ verification
→ validation
→ operational evidence
```

Not every repository artifact must contain the whole chain. The chain exists so that reviewers can identify where evidence is absent or where a claim has jumped over an unverified assumption.

## Change re-entry

A change is not automatically “maintenance only.” The `ChangeImpact` artifact determines which claims, invariants, evidence records, and authorities are affected.

Possible outcomes are:

- `NO_IMPACT`
- `REVERIFICATION_REQUIRED`
- `REAUTHORIZATION_REQUIRED`
- `RETIREMENT_REQUIRED`

The outcome is evidence-driven and may be escalated by human authority.

## Disposal

Retirement is a terminal engineering state only after required disposal obligations are complete. Examples include credential revocation, key destruction, media handling, evidence retention, authority closure, and dependent-system notification.

The reference schema therefore distinguishes `RETIRED` from an incomplete attempt to retire.
