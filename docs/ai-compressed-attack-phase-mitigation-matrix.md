# AI-Compressed Attack Phase Mitigation Matrix

**Structural problem-solving map for bounding impact after initial access**
**Version:** v0.1.1 — AI Cyber Resilience Framework
**Grounding:** NIST SP 800-160 domain separation and complementary principles

---

## Purpose

This matrix turns the framework thesis into an immediate problem-solving tool. It shows which structural design principles most effectively raise attacker cost at each phase of an AI-compressed cyberattack and what concrete architectural outcome to seek.

It is defensive architecture guidance only. It does not describe offensive techniques or provide exploit guidance.

---

## Attack Phase × Structural Mitigation Matrix

| Attack Phase                  | Primary Structural Mitigations                                      | Desired Architectural Outcome                                      | Cost Imposed on Attacker |
|-------------------------------|---------------------------------------------------------------------|--------------------------------------------------------------------|--------------------------|
| Initial Access                | Least Functionality, Anomaly Detection                              | Fewer exposed services; anomalous probes become visible sooner     | Medium                  |
| Execution & C2 Establishment  | Domain Separation (data diodes / CDS), Continuous Protection        | Callback paths from sensitive domains are blocked or mediated      | High                    |
| Discovery / Enumeration       | Least Sharing, Domain Separation                                    | Attacker cannot see or reach assets outside the compromised domain | High                    |
| Lateral Movement              | Domain Separation + Mediated Access + Least Sharing                 | Cross-domain traversal is structurally impossible or explicitly authorized and logged only | Very High               |
| Privilege Escalation          | Least Privilege + Domain Separation (admin/user/mission split)      | Credentials or rights harvested in one domain do not operate in another | Very High               |
| Persistence                   | Least Persistence + Least Functionality                             | Unnecessary long-lived processes, services, and autoruns are absent | High                    |
| Mission Execution             | All principles combined + Anomaly Detection                         | Blast radius remains bounded; every boundary crossing is logged and reviewable | Prohibitive             |

---

## Five-Step Problem-Solving Path

Use this path on one mission-critical system or enclave. Do not attempt enterprise-wide application on the first pass.

1. **Identify the protected mission function**  
   Name the single business, operational, or safety function that must remain available even if other domains are compromised.

2. **Inventory domains and authorized flows**  
   Complete `checklists/domain-separation-assessment.md` and `templates/domain-boundary-inventory.md` + `templates/authorized-flow-matrix.md`. Record only what currently exists.

3. **Locate the highest-leverage gaps**  
   Using the matrix above, mark any phase where the corresponding structural mitigation is absent or untested. Priority order is lateral movement, privilege escalation, then persistence.

4. **Define the minimal architectural change**  
   For each high-leverage gap, specify the smallest change that creates a mediated, logged boundary (e.g., micro-segment one administrative plane, enforce least privilege on a service account, remove a shared administrative channel). Record the claim and required evidence using `templates/evidence-card-template.md`.

5. **Verify and maintain**  
   Test that unauthorized cross-domain attempts are blocked or mediated. Schedule re-verification after any change, update, or recovery event so continuous protection holds. Revisit the matrix after material architecture changes.

---

## Outcome Statement

When the matrix and five-step path are applied, an AI-compressed adversary who obtains initial access is forced to overcome explicit, verifiable domain boundaries before reaching higher-value mission functions. Impact is bounded by design rather than by detection speed alone.

**The failure mode remains inadequate engineering, not inadequate technology.**

---

## Related Artifacts

- `docs/article-defending-against-ai-compressed-cyberattacks.md` — core thesis
- `docs/structural-security-principles.md` — principle definitions
- `docs/threat-model.md` — defensive lifecycle characterization
- `checklists/domain-separation-assessment.md`
- `templates/authorized-flow-matrix.md`

---

*Part of AI Cyber Resilience Framework v0.1.1. Public-safe defensive guidance only.*
