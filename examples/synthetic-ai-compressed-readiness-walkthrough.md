# Synthetic AI-Compressed Readiness Walkthrough

**Synthetic reference.** Every system, role, date, and evidence identifier in this file is fictional. This is a non-authorizing example: not an assessment of a real system, not a customer record, and not an operating authorization. `authority_effect: NONE`.

**Example system:** Notional High-Consequence Mission Planning & Control System, the same fictional system sketched in [sample-mission-system-boundary-map.md](sample-mission-system-boundary-map.md).

**Assessed boundary:** B-OC-01, between the User / Analyst domain and the Operational Control / Specialized Workload domain.

**Fictional review date:** 2026-10-01

**Accountable human owner:** Mission System Owner (synthetic role, not a named person)

This walkthrough shows one pass through the existing artifacts:

Mission need → Boundaries → Authorized flows → Weak link → Evidence → Human decision → Hardening action → Reassessment

It reuses the published templates. It does not define a second data model. It assigns no numeric score.

## 1. Scope, assumptions, and owner

| Field | Synthetic content |
|---|---|
| Mission need | Analysts submit approved planning tasks. Only a mediated path may carry an approved task into operational control. |
| In scope | Boundary B-OC-01, the one shared identity group that can see both sides of that boundary, and the recovery-credential question for this same boundary. |
| Out of scope | Enterprise-wide inventory, partner exchange, endpoint hardening, and any system that is not this fictional example. |
| Assumptions | The fictional owner has authority to request an architecture review of this boundary. No production change is approved by this example. |
| Accountable human owner | Mission System Owner. A checklist does not own the decision. |

Assumption that limits the example: "mediated" here means the fictional design intends a single approved interface. That intention is not verification.

## 2. Domain separation and authorized flows

Start from the blank templates, not from a new form:

- [Domain Boundary Inventory](../templates/domain-boundary-inventory.md)
- [Authorized Flow Matrix](../templates/authorized-flow-matrix.md)
- [Domain Separation Assessment](../checklists/domain-separation-assessment.md)

Illustrative inventory excerpt for this boundary only:

| Domain ID | Domain Name | Sensitivity / Protection Needs | Primary Assets & Functions | Owner / Steward | Notes |
|---|---|---|---|---|---|
| D-AN | User / Analyst | Lower than operational control | Task submission from ordinary analyst principals | Mission System Owner | Ordinary workstations |
| D-OC | Operational Control / Specialized Workload | Highest in this fictional system | Approved job execution | Mission System Owner | Not directly reachable from D-AN in the intended design |

| Boundary ID | Between Domains | Separation Type | Enforcement Mechanism | Monitoring / Logging | Status |
|---|---|---|---|---|---|
| B-OC-01 | D-AN → D-OC | Logical, as reported | One approved task interface, as reported | One synthetic deny record for direct sessions; identity path not covered | Partial |

Illustrative flow excerpt:

| Flow ID | From Domain | To Domain | Data / Function | Business / Mission Justification | Mediation / Control | Logging Required | Review Frequency | Owner | Status |
|---|---|---|---|---|---|---|---|---|---|
| F-001 | D-AN | D-OC | Approved planning task | Mission need stated above | Approved task interface | Yes | Each architecture review | Mission System Owner | Reported, not fully verified |
| F-002 | D-AN | D-OC | Direct session to operational control | None | Must not exist | Yes | Each architecture review | Mission System Owner | One synthetic deny record for one interface |

No flow that is absent from the matrix is authorized. The shared identity path in section 3 was not listed as an authorized flow. That absence is a finding, not permission.

## 3. Shared-mechanism concern

The fictional review finds one privilege-boundary concern.

A single identity group contains both ordinary analyst principals and a privileged orchestration principal used to release work into D-OC. The group is a shared mechanism across protection needs. Least privilege and least sharing both ask whether an ordinary analyst principal can request the orchestration role. No current verification record answers that question.

This section does not describe how to obtain, reuse, or abuse a credential. The defensive question is structural: two protection needs share one identity mechanism, and the boundary is unevidenced.

## 4. Qualitative checklist excerpt

Scoring uses [AI-Compressed Readiness Checklist](../checklists/ai-compressed-readiness-checklist.md). Only the items needed to show the evidence rules are filled. Unlisted items are not implicitly Strong.

| # | Item | Status | Evidence / Notes |
|---|---|---|---|
| 1 | Mission-critical domains have been explicitly identified and bounded | Strong | Domain excerpt in section 2 was reviewed on the fictional date against the owner's scope statement. The record is current for B-OC-01 only. |
| 4 | Unauthorized cross-domain communication is structurally blocked | Partial | Demonstrated for one direct-session interface only (section 5). Other interfaces were not tested. Partial is not Strong. |
| 9 | Credential harvesting in one domain does not yield usable credentials in higher-privilege domains | Weak | Shared identity group in section 3. No verification record. Missing evidence is not Strong. Critical exception. |
| 13 | Shared mechanisms between domains have explicit security justification and controls | Weak | The shared group has no recorded justification and no current control test. |
| 14 | Persistence mechanisms are minimized | N/A | Applicability rationale: this review covers boundary B-OC-01, not workstation persistence. The rationale is recorded by the Mission System Owner. A blank N/A would have been incomplete. |
| 16 | Backup and recovery processes are isolated from production domains where possible | Weak | Recovery-credential separation for B-OC-01 is Unknown. Unknown is not Strong and is not a demonstrated failure. Evidence limit, listed below. |

## 5. Evidence card

Fields follow [Evidence Card Template](../templates/evidence-card-template.md).

**Claim ID:** SYN-EC-BND-014

**Related NIST principle:** Domain separation; mediated access

**Date:** 2026-10-01 (fictional)

**Author:** Architecture Reviewer (synthetic role)

### Claim

Direct analyst-workstation sessions to the fictional operational-control address range used by B-OC-01 are denied at the approved boundary interface.

### Evidence state

| Statement | Evidence state | What the record actually shows |
|---|---|---|
| Direct analyst sessions on the named interface are denied | Demonstrated, inside this fiction only | Synthetic inspection record REF-SYN-BND-014, dated 2026-10-01, says deny for that one interface. It does not cover every path. |
| Administrative updates use a separate jump path | Reported | An operator statement is cited. No log extract is attached. Reported is not Demonstrated. |
| An analyst principal cannot request the privileged orchestration role | Unknown | No group-membership test and no deny record. Unknown is not Strong. |
| Backup restore credentials cannot be used from the analyst domain | Unknown | No inventory entry, configuration record, or test was supplied. |

**Type of evidence checked for the demonstrated row:** Test result / log (synthetic reference only)

**Location:** `REF-SYN-BND-014` (fictional identifier; no external system)

**Verification method:** Inspection of the fictional deny record: principal class, interface, time, and result. The record was not independently reproduced outside this example.

**Limitations:** Synthetic. One interface. One fictional date. Not evidence about any real network.

**Confidence:** Low for the boundary as a whole. The single demonstrated row does not raise the unknown rows.

## 6. Defensive weak-link finding

Template: [Attack Path Review](../templates/attack-path-review.md). Structural weakness only. No procedure.

| Path ID | Starting Point | Target | Primary Enabling Weakness | Structural Control That Should Block | Current Status | Evidence |
|---|---|---|---|---|---|---|
| P-01 | D-AN ordinary analyst principal | Privileged orchestration role for D-OC | Shared identity group across protection needs | Separate identity boundary; analyst principals excluded from the privileged group; authorized negative check recorded on an evidence card | Weak / unevidenced | Unknown. Not listed as an authorized flow. |

The finding is not that a compromise has occurred. The finding is that the structural control is not evidenced, so the boundary cannot be treated as closed.

## 7. Proposed remediation

| Field | Synthetic content |
|---|---|
| Action | Remove the privileged orchestration principal from the analyst-reachable group and place it in a separate administrative identity boundary. |
| Owner | Identity Boundary Steward (synthetic role), accountable to the Mission System Owner |
| Verification method | Inspection of group membership after the change, plus one authorized negative check limited to the approved interface: an ordinary analyst principal, with no privileged role, requests the orchestration role. The expected defensive result is denial. Record principal class, interface, time, and result on a new evidence card. |
| What verification would change | Only that one check can move the orchestration-role statement from Unknown toward Demonstrated. It still would not speak to recovery credentials or to interfaces that were not tested. |
| What this example does not do | It does not approve a change on a real system, and it does not describe a way around the control. |

## 8. Thirty-day illustrative backlog

Planning input only. Dates are fictional and start at 2026-10-01.

| Window | Action | Owner role | Verification method | Exit evidence |
|---|---|---|---|---|
| Days 1–5 | Freeze the in-scope identity group list for B-OC-01 | Mission System Owner | Compare the current group export with section 2 | Inventory note; gaps stay Unknown |
| Days 6–15 | Separate the privileged orchestration principal from the analyst-reachable group | Identity Boundary Steward | Inspect membership after the change | Membership difference cited on the evidence card |
| Days 16–25 | Authorized negative check on the approved interface | Authorized Boundary Tester | Record deny or allow, with principal class, interface, and time | Evidence state updated only for that interface |
| Days 26–30 | Decide whether the Unknown recovery-credential question stays open or enters a new scoped review | Mission System Owner | Written decision using section 10 | Decision record. No operating authorization. |

## 9. Human decision record

**Record class:** Synthetic. Non-authorizing. `authority_effect: NONE`.

**Decision:** No operating decision. The backlog is a planning input only.

**Decider:** Mission System Owner (fictional role)

**Date:** 2026-10-01 (fictional)

The owner does not assign an overall resilience label. Item 9 is a Weak critical exception. Recovery-credential separation is an Unknown evidence limit. Either one is enough to refuse closure. An aggregate label would conceal them.

This record does not authorize operation, testing, or change on any real system. It does not certify resilience. It does not prove that a control works. It does not transfer the decision to a model, a checklist, or this example.

## 10. When to reopen

Reopen this assessment, rather than reuse it, when any of the following is true:

- Domain membership, shared identity mechanisms, authorized flows, mediation, or the recovery path change.
- Evidence is superseded, expires, or is found to describe a different boundary.
- A critical exception closes, opens, or is reclassified.
- The accountable human owner changes.
- Scope moves beyond B-OC-01.

Until a named human reviews the new evidence, the prior qualitative notes stay historical. They do not become Strong by age or by repetition.

## What this example does not establish

- That any real architecture matches this fiction
- That a deny result on one interface blocks every other path
- That recovery, identity, or isolation controls are effective anywhere
- Compliance, certification, or permission to operate
- A numeric or calibrated measure of risk

No numeric score is assigned. Synthetic evidence supports only the internal consistency of this reference.
