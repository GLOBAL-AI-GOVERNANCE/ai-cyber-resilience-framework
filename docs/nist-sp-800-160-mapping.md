# NIST SP 800-160 Mapping

**Traceability from NIST SP 800-160, Vol. 1 Rev. 1 Principles to AI-Compressed Cyber Defense Framework Artifacts**
**Version:** v0.1.0

---

## Purpose

This mapping helps organizations demonstrate alignment between their use of this framework and the authoritative NIST systems security engineering guidance. It supports evidence-based claims for governance, acquisition, and audit purposes.

---

## Core Mapping

| NIST SP 800-160 Principle          | Primary AI-Compressed Cyber Defense Framework Artifact(s)                          | Evidence Type                  | Notes |
|------------------------------------|-----------------------------------------------------------------------|--------------------------------|-------|
| **Domain Separation**             | Domain Boundary Inventory<br>Authorized Flow Matrix<br>Domain Separation Assessment | Architecture diagrams, interface specs, test results | Foundational principle |
| **Least Privilege**               | Privileged Access Isolation Checklist<br>Evidence Cards              | Account inventories, role matrices, access reviews | Within-domain control |
| **Mediated Access**               | Boundary Enforcement Test Plan<br>Authorized Flow Matrix             | Test logs, policy decision records | Reference monitor concept |
| **Structured Decomposition**      | Domain Boundary Inventory<br>Attack Path Review                      | Decomposition diagrams, dependency maps | Prevents architecture drift |
| **Least Functionality**           | AI-Compressed Readiness Checklist<br>Domain Separation Assessment     | Service inventories, configuration baselines | Reduces attack surface |
| **Least Sharing**                 | Authorized Flow Matrix<br>Domain Boundary Inventory                  | Data flow diagrams, sharing justification logs | Minimizes information paths |
| **Least Persistence**             | Recovery State Protection Checklist<br>Privileged Access Isolation Checklist | Persistence mechanism inventories, least-persistence policy | Attacks foothold maintenance |
| **Anomaly Detection**             | Telemetry Map<br>Boundary Enforcement Test Plan                      | Monitoring requirements, alert definitions | Boundary-focused detection |
| **Continuous Protection**         | Recovery State Protection Checklist<br>Boundary Enforcement Test Plan | State transition test results, maintenance window procedures | Covers updates, recovery, failover |

---

## Additional Supporting Principles (Selected)

- **Clear Abstraction** — Supported by Evidence Card Template (clear claim-evidence separation)
- **Minimization** — Reinforced across multiple checklists and templates
- **Modularity** — Encouraged through structured decomposition guidance
- **Layering** — Implicit in domain separation and mediated access

---

## How to Use This Mapping

1. Select the system or enclave under assessment.
2. Complete the relevant checklists and templates.
3. For each completed artifact, record the mapping in your evidence package.
4. Use the "Evidence Type" column to identify what artifacts constitute acceptable evidence for claims.
5. Maintain traceability from individual evidence cards back to the NIST principle(s) they support.

This mapping supports **trustworthiness claims** in the sense of NIST SP 800-160 — claims that can be verified through analysis, inspection, and testing.

---

*Part of AI-Compressed Cyber Defense Framework v0.1.0*
