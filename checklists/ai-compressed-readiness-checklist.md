# AI-Compressed Readiness Checklist

**Purpose:** High-level assessment of structural security posture against AI-compressed cyber threats
**Version:** v0.1.0 — AI-Compressed Cyber Defense Framework
**Instructions:** For each item, indicate status and note key evidence or gaps. Focus on one critical system or enclave at a time.

**Documentation note:** Leave evidence fields blank if no evidence exists yet. The goal is progressive documentation: capture current state first, then close gaps with verifiable artifacts.

---

## Scoring

- **Strong** — Implemented, documented, and verified with evidence
- **Partial** — Partially implemented or documented but gaps exist
- **Weak** — Not implemented or no meaningful evidence
- **N/A** — Not applicable to this system

---

## Checklist

### Domain Separation & Boundaries

| # | Item | Status | Evidence / Notes |
|---|------|--------|------------------|
| 1 | Mission-critical domains have been explicitly identified and bounded |        | |
| 2 | Domains with different protection needs are physically or logically separated |        | |
| 3 | Cross-domain interfaces are explicitly defined and documented |        | |
| 4 | Unauthorized cross-domain communication is structurally blocked (not merely monitored) |        | |
| 5 | A current domain boundary inventory exists and is maintained |        | |

### Privilege & Access Isolation

| # | Item | Status | Evidence / Notes |
|---|------|--------|------------------|
| 6 | Administrative domains/functions are separated from user/ordinary domains |        | |
| 7 | Least privilege is enforced within each domain |        | |
| 8 | Service accounts and processes operate with minimal necessary privileges |        | |
| 9 | Credential harvesting in one domain does not yield usable credentials in higher-privilege domains |        | |
| 10 | Privileged access paths are mediated and logged |        | |

### Functionality & Sharing

| # | Item | Status | Evidence / Notes |
|---|------|--------|------------------|
| 11 | Unnecessary services, protocols, and interfaces are disabled within each domain |        | |
| 12 | Shared infrastructure (storage, auth, naming, admin channels) is minimized and justified |        | |
| 13 | Shared mechanisms between domains have explicit security justification and controls |        | |

### Persistence & State Protection

| # | Item | Status | Evidence / Notes |
|---|------|--------|------------------|
| 14 | Persistence mechanisms are minimized (no unnecessary autoruns, scheduled tasks, services) |        | |
| 15 | Protections remain effective during system updates, restarts, and recovery |        | |
| 16 | Backup and recovery processes are isolated from production domains where possible |        | |
| 17 | Maintenance and update windows do not create persistent unprotected pathways |        | |

### Visibility & Evidence

| # | Item | Status | Evidence / Notes |
|---|------|--------|------------------|
| 18 | Boundary crossings are logged and subject to anomaly detection |        | |
| 19 | Security claims about domain separation and isolation are supported by verifiable evidence |        | |
| 20 | Evidence cards or equivalent artifacts exist for key architectural claims |        | |

---

## Overall Assessment

**Current Structural Resilience Level:**
☐ Strong — Architecture significantly limits blast radius and mission impact
☐ Moderate — Some structural protections exist but significant gaps remain
☐ Emerging — Early awareness; major architectural work needed
☐ Initial — Flat or implicit-trust architecture dominant

**Priority Gaps (Top 3):**

1.
2.
3.

**Recommended Next Actions:**

- Complete Domain Boundary Inventory for this system
- Perform Authorized Flow Matrix review
- Develop remediation plan with evidence milestones

---

*Use in conjunction with Domain Separation Assessment and other checklists in this framework.*
