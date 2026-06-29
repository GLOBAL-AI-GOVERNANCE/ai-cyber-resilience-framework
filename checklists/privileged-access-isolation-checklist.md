# Privileged Access Isolation Checklist

**Version:** v0.1.0 — AI-Compressed Cyber Defense Framework

**Documentation note:** Leave evidence fields blank if no evidence exists yet. The goal is progressive documentation: capture current state first, then close gaps with verifiable artifacts.

## Purpose
Assess whether administrative and privileged functions are structurally isolated from ordinary user activity and lower-privilege domains.

## Key Questions

| # | Question | Status (Strong / Partial / Weak) | Evidence / Gap |
|---|----------|----------------------------------|----------------|
| 1 | Administrative accounts and functions reside in a separate domain from general user activity | | |
| 2 | Elevation to administrative rights in a user domain does not grant administrative rights in the administrative domain | | |
| 3 | Privileged access requires explicit mediation and authorization at the domain boundary | | |
| 4 | Service accounts operate with least privilege and are not shared across domains unnecessarily | | |
| 5 | Credential stores and secrets management are isolated by domain sensitivity | | |
| 6 | Administrative tools and interfaces are not accessible from lower-privilege domains without mediation | | |
| 7 | Just-in-time / just-enough access is used for privileged operations where feasible | | |
| 8 | Privileged session activity is logged and attributable at the individual level | | |

## Observations

**Effective Controls:**
-

**Weaknesses / Attack Paths:**
-

**Remediation Priorities:**
-

---

*Complements Domain Separation and Least Privilege principles.*
