# Telemetry Map Template

**System:** _______________________________
**Date:** ________________

## Purpose
Define what telemetry is required to detect boundary violations and support anomaly detection in a domain-separated architecture.

## Required Telemetry

| Telemetry Type | Source / Sensor | Events to Capture | Retention | Alerting Threshold / Correlation | Owner |
|----------------|-----------------|-------------------|-----------|----------------------------------|-------|
| Boundary Crossing Attempts | Firewall / CDS / Micro-segmentation | Denied flows, policy violations | | | |
| Authentication & Authorization | Identity provider, access control points | Failed auth, privilege use, cross-domain auth | | | |
| Administrative Activity | Privileged access workstations, jump hosts | All privileged commands, session recordings | | | |
| Persistence Indicators | Endpoint detection, system logs | New services, scheduled tasks, autoruns, unusual processes | | | |
| Data Flow Anomalies | Network sensors, DLP | Unexpected volume or destinations between domains | | | |

## Integration Notes

- How does this telemetry feed into existing SIEM / SOAR?
- Are there gaps in visibility at domain boundaries?
- What correlation rules are needed to turn raw logs into actionable boundary-violation alerts?

---

*Supports Anomaly Detection principle.*
