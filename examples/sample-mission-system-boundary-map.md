# Sample Mission System Boundary Map

**Example System:** Notional High-Consequence Mission Planning & Control System (public-safe illustrative example only)
**Version:** v0.1.0 — AI-Compressed Cyber Defense Framework

## Domain Structure (Illustrative)

| Domain | Sensitivity | Key Functions | Example Separation |
|--------|-------------|---------------|--------------------|
| User / Analyst | Low-Medium | Mission planning interfaces, reporting | Standard user workstation domain |
| Mission Orchestration | High | Workflow coordination, tasking, data fusion | Micro-segmented; mediated access to specialized operational resources |
| Operational Control / Specialized Workload | Very High | Approved job execution, control actions, protected processing | Hardware- or policy-enforced isolation with strictly mediated interfaces |
| Administrative / Management | High | System administration, updates, secrets management | Separate admin domain; jump hosts + MFA + session recording |
| External / Partner | Variable | Data exchange with authorized partners | Cross-domain solution with strict allow-listing and inspection |

## Key Authorized Flows (Example)

- Analyst domain → Mission Orchestration: Task submission (mediated, authenticated, logged)
- Mission Orchestration → Operational Control / Specialized Workload: Approved request submission (mediated via secure API gateway + policy engine)
- Operational Control / Specialized Workload → Mission Orchestration: Results return (mediated, integrity protected)
- Administrative domain → All domains: Management operations (strictly mediated, time-limited, fully logged)

## Unauthorized Paths to Block / Monitor

- Direct workstation-to-operational-control access
- Lateral movement from partner exchange domain into mission orchestration
- Administrative tools reachable from user workstations without mediation
- Backup, recovery, or maintenance interfaces reachable from ordinary user domains

## Lessons from This Example

- High-consequence systems often start with overly broad trust relationships between ordinary user activity, operational functions, administrative tooling, and recovery paths.
- Specialized operational resources require strong containment because compromise can affect mission execution, safety, continuity, public trust, or sensitive data.
- Evidence (boundary inventory, flow matrix, test results) is essential to move from "we think it is isolated" to "we have verified isolation."

---

*This is an illustrative public-safe example only. Adapt structure and controls to your actual mission requirements, environment, and classification level.*
