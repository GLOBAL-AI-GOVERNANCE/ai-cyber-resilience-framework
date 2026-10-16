# AI-Compressed Attack Phase Mitigation Matrix

**Defensive reference map for intended structural effects after initial access**
**Document status:** Unreleased documentation on the current branch. Not part of the published v0.1.1 tag.
**Published release identity:** v0.1.1 remains the published AI Cyber Resilience Framework release until a separate release gate.
**Grounding:** NIST SP 800-160 domain separation and complementary principles already documented in this repository
**authority_effect:** NONE

---

## Purpose

This matrix is a planning reference. It maps common post-compromise phases to structural design principles already defined in this repository and states the architectural effect those principles are intended to support.

It does not measure attacker cost, prove that a control works, certify a system, or authorize operation. Desired outcomes below are design intents. They become claims about a real system only when qualified people supply current evidence and test the actual environment.

This document is defensive architecture guidance only. It does not describe offensive techniques or provide exploit guidance.

Use the existing qualitative readiness checklist and evidence cards. This matrix does not introduce a second scoring system.

---

## Attack Phase × Structural Mitigation Matrix

| Attack Phase | Primary Structural Mitigations | Intended Architectural Effect | Claim Limit |
|---|---|---|---|
| Initial Access | Least Functionality, Anomaly Detection | Reduce unnecessary exposed services so unexpected probes are easier to distinguish from authorized use | Does not prevent initial access |
| Execution and external callback | Domain Separation, Continuous Protection | Make unauthorized callbacks from higher-sensitivity domains blocked or mediated where a boundary is actually enforced | Does not guarantee every callback path is closed |
| Discovery / Enumeration | Least Sharing, Domain Separation | Limit what a compromised domain can enumerate when shared paths and cross-domain reach are explicitly constrained | Does not make hidden or undocumented paths invisible by assertion |
| Lateral Movement | Domain Separation, Mediated Access, Least Sharing | Require cross-domain movement to use an explicit, mediated, and logged path instead of implicit trust | Does not make all lateral movement impossible |
| Privilege Escalation | Least Privilege, Domain Separation | Keep rights and credentials useful in one domain from automatically operating in another domain | Does not stop escalation inside a domain that is itself over-privileged |
| Persistence | Least Persistence, Least Functionality | Reduce long-lived processes, services, and startup mechanisms that are not required for the domain mission | Does not remove every possible foothold |
| Mission impact | Combined principles plus Anomaly Detection | Keep higher-value functions behind defined boundaries so impact is more likely to stay bounded and reviewable | Does not prove mission resilience or that every crossing is observed |

The right-hand column is a limit on the claim, not a measured attacker-cost rating.

---

## Five-Step Application Path

Apply this path to one system or enclave. Do not treat the first pass as an enterprise-wide assessment.

1. **Name the function to protect.** Identify one business, operational, or safety function that should remain available even if another domain is compromised.

2. **Record current boundaries.** Use `checklists/domain-separation-assessment.md`, `templates/domain-boundary-inventory.md`, and `templates/authorized-flow-matrix.md`. Record what exists. Leave evidence blank when none exists yet.

3. **Mark untested intents.** Using the matrix, note phases where the listed mitigation is absent, undocumented, or not tested. Start with lateral movement, privilege boundaries, and persistence.

4. **Specify one architectural change.** For each priority gap, name the smallest change that would create a mediated and logged boundary. Record the claim and the evidence still required with `templates/evidence-card-template.md`.

5. **Test and reassess.** Where authorized, test that an unauthorized cross-domain attempt is blocked or mediated. Reassess after change, update, recovery, or a new dependency. A completed template is not proof that the live system behaves as intended.

The existing 20-item qualitative readiness checklist remains the scoring aid. Strong still requires current, relevant verification evidence.

---

## Outcome Boundary

Applied as written, this reference helps a team state whether one boundary is designed to contain compromise. It does not establish that compromise is contained, that lateral movement is impossible, that every boundary crossing is observed, or that attacker cost has been measured.

**authority_effect: NONE.** Human review remains required before any operational conclusion.

---

## Related Artifacts

- [docs/article-defending-against-ai-compressed-cyberattacks.md](article-defending-against-ai-compressed-cyberattacks.md)
- [docs/structural-security-principles.md](structural-security-principles.md)
- [docs/threat-model.md](threat-model.md)
- [docs/nist-sp-800-160-mapping.md](nist-sp-800-160-mapping.md)
- [checklists/ai-compressed-readiness-checklist.md](../checklists/ai-compressed-readiness-checklist.md)
- [checklists/domain-separation-assessment.md](../checklists/domain-separation-assessment.md)
- [templates/authorized-flow-matrix.md](../templates/authorized-flow-matrix.md)
- [templates/evidence-card-template.md](../templates/evidence-card-template.md)
- [examples/synthetic-ai-compressed-readiness-walkthrough.md](../examples/synthetic-ai-compressed-readiness-walkthrough.md)

---

*Unreleased documentation proposed for current main. It is not included in the published v0.1.1 tag. The v0.2.0 Continuous Assurance Thread remains a separate unreleased candidate. Public-safe defensive guidance only. Not certification, compliance determination, production authorization, or proof of deployed resilience.*
