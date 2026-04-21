---
name: architecture-system-design-quality
description: Use this skill to evaluate architecture quality with coupling, blast radius, resilience pattern coverage, and drift metrics.
---

# Architecture & System Design Quality

Use this skill to assess systemic design integrity, resilience posture, and change impact radius across services.

## Required tools
- Service dependency graph and runtime call topology
- Change impact mapping (files -> services -> user journeys)
- Resilience policy inventory (timeouts/retries/circuit breakers)
- Config drift and infrastructure drift reports

## Analysis runbook
1. Generate dependency density map for critical domains.
2. Compute blast radius metrics per change (services/tables/APIs touched).
3. Measure cross-service transaction depth on key journeys.
4. Audit resilience pattern coverage at interaction boundaries.
5. Detect config-vs-code drift and stale operational assumptions.
6. Prioritize architecture remediations by systemic risk reduction.

## Metric definitions (strict)
- **Service Coupling/Dependency Density**: average inbound/outbound deps per service
- **Blast Radius per Change**: count of services/components affected per release
- **Cross-Service Transactions**: average hop count per critical workflow
- **Resilience Pattern Coverage**: % interactions with timeout/retry/breaker guards
- **Config vs Code Drift**: mismatches between declared and running behavior

## Expert diagnostic patterns
- Increasing dependency density: coordination tax and cascading failure risk.
- High hop count + high p99 latency: chatty architecture bottlenecks.
- Resilience gaps concentrated in critical edges: likely incident amplifiers.

## Improvement interventions
- Reduce synchronous call chains in high-traffic paths.
- Introduce bounded contexts with explicit ownership boundaries.
- Add mandatory resilience policies via platform defaults.
- Automate drift detection in release governance.

## Deliverables
- Architecture risk register with quantified blast radius
- Domain boundary and decoupling roadmap
- Resilience coverage gap report

## Script
- `bash .claude/skills/shared/scripts/generate_quality_report.sh architecture-system-design-quality 30`
