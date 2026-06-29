# Structural Security Design Principles

**Domain Separation and Complementary NIST SP 800-160 Principles for AI-Compressed Threat Defense**
**Version:** v0.1.0 — AI-Compressed Cyber Defense Framework

---

## Overview

This document expands on the core principles referenced in the main article. It is intended for security architects and systems engineers who need deeper understanding to apply these principles in real architectures.

---

## 1. Domain Separation (Foundational)

**NIST SP 800-160 Definition:** Domains with distinctly different protection needs are physically or logically separated.

**Protective Effects:**
- **Susceptibility** — Limits external influence on a domain.
- **Containment** — Limits the ability of a compromised domain to affect external domains.

**Modern Application:** Mission-driven separation from hardware substrate through application and data layers. Especially critical for:
- High-consequence systems combining business, operational, administrative, recovery, and vendor domains
- OT/ICS and cyber-physical environments
- Cloud/SaaS, identity, and administrative management planes
- Administrative vs. user vs. mission domains

**Implementation Mechanisms:**
- Hardware-enforced isolation (trusted execution environments, secure enclaves, data diodes)
- Logical separation via micro-segmentation, software-defined networking, and cross-domain solutions
- Mandatory access control (MAC) policies
- Explicit boundary interfaces with mediation and logging

**Verification Evidence:** Boundary inventory, authorized flow matrix, interface control documents, test results showing blocked unauthorized cross-domain attempts.

---

## 2. Least Privilege

Each system element is allocated only the privileges necessary to accomplish its specified functions.

**Synergy with Domain Separation:** Domain separation sets coarse-grained boundaries; least privilege enforces fine-grained control *within* each domain.

**AI-Compressed Relevance:** Reduces the value of credential harvesting and limits the damage a compromised process or account can cause even inside its domain.

---

## 3. Mediated Access

All access to and operations on system elements are mediated by a policy decision point.

**Key Concept:** Reference monitor — always invoked, tamper-resistant, small enough to verify.

**AI-Compressed Relevance:** Every cross-domain or privileged operation becomes a decision point that AI reasoning must overcome or subvert. Creates auditable chokepoints rather than implicit trust.

---

## 4. Structured Decomposition and Composition

System complexity is managed through structured decomposition into constituent elements and structured composition to deliver capability.

**AI-Compressed Relevance:** Prevents "architecture drift" where convenience connections erode intended boundaries over time. Makes domains explicit, traceable, and verifiable — reducing unintended paths that AI reasoning can discover.

---

## 5. Least Functionality

Each system element has only the capabilities required for its mission.

**AI-Compressed Relevance:** Disables or blocks services and interfaces that are common vectors (SMB file sharing, PowerShell remoting, DCOM, legacy admin interfaces, etc.). Reduces the richness of the environment that AI tools can exploit.

---

## 6. Least Sharing

System resources are shared among elements only when necessary and among as few elements as possible.

**Classic Reference:** Saltzer & Schroeder — every shared mechanism represents a potential information path that must be designed with care.

**AI-Compressed Relevance:** Shared storage, naming services, authentication infrastructure, and administrative channels are high-value targets for lateral movement and information gathering. Least sharing minimizes these paths.

---

## 7. Least Persistence

System elements and resources are available, accessible, and active only for the time they are needed.

**Three Conditions Targeted:**
1. Presence (installed in memory or storage)
2. Accessibility (invocable)
3. Active (currently executing)

**AI-Compressed Relevance:** Directly attacks the persistence mechanisms (registry autoruns, scheduled tasks, services, DLL hijacking, boot implants) that frameworks rely on to maintain footholds across reboots and sessions.

---

## 8. Anomaly Detection (Architecturally Informed)

Any salient anomaly is detected in a timely manner that enables effective response.

**AI-Compressed Relevance:** In domain-separated architectures, unauthorized boundary crossings are structurally anomalous by definition. This transforms detection from a needle-in-haystack problem (finding malicious traffic among millions of legitimate flows) into a targeted problem (detecting violations of explicit boundary policy).

---

## 9. Continuous Protection

Protection for a system element must be effective and uninterrupted during the time protection is required.

**AI-Compressed Relevance:** AI-compressed tools specifically target transitional states (updates, restarts, authentication windows, backup operations). Continuous protection requires that domain boundaries and mediation remain effective across all system states and modes.

---

## Integration: Creating Structural Defense-in-Depth

These principles are not independent controls. They form an interlocking set:

- Domain separation provides the **coarse boundaries**
- Least privilege, least functionality, and least sharing provide **fine-grained control inside domains**
- Mediated access and anomaly detection provide **visibility and enforcement at boundaries**
- Least persistence and continuous protection address **temporal attack surfaces**
- Structured decomposition ensures the architecture remains **verifiable and maintainable**

The result is a system where damaging attacks are **structurally difficult**, **operationally visible**, and **mission-limited**.

---

*Part of AI-Compressed Cyber Defense Framework v0.1.0*
