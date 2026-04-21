---
name: reliability-production-stability
description: Use this skill to evaluate quality through production reliability, uptime, error rates, incident trends, and latency.
---

# Reliability & Production Stability

Use this skill to evaluate whether production behavior is reliable under normal load and failure conditions.

## Required tools
- SLO/SLA dashboards (availability and error budget)
- APM + distributed tracing
- Incident timeline and severity records
- Traffic/load and release timeline overlays

## Analysis runbook
1. Define service boundaries and critical user journeys.
2. Calculate availability, incident rate, MTBF, and latency/error distributions.
3. Normalize by traffic volume and deploy count.
4. Separate transient blips from customer-impacting failures.
5. Attribute instability to release, infra, dependency, or capacity causes.
6. Produce hardening backlog ordered by risk reduction.

## Metric definitions (strict)
- **Availability/Uptime**: `successful_service_time / total_service_time`
- **MTBF**: `total_uptime / number_of_failures`
- **Incident Rate**: incidents per deploy and per time window
- **Severity Distribution**: % Sev1/Sev2/Sev3 incidents
- **Error Rate**: failing requests / total requests (e.g., 5xx ratio)
- **Latency**: p50/p95/p99 response time by endpoint/journey

## Expert diagnostic patterns
- Stable p50 but rising p99: tail-latency amplification, likely dependency or saturation.
- Low incident count but high severity skew: weak blast-radius containment.
- Good uptime with high error bursts: averages hiding user pain.

## Improvement interventions
- Set error-budget-based release policy gates.
- Add dependency isolation, load shedding, and retry budgets.
- Enforce SLO alerting on user journeys (not host metrics only).
- Run game days for rollback, failover, and degraded mode.

## Deliverables
- Reliability scorecard with trend and service segmentation
- Top recurring failure modes and owner-assigned remediations
- Capacity/risk forecast for next release cycle

## Script
- `bash .claude/skills/shared/scripts/generate_quality_report.sh reliability-production-stability 30`
