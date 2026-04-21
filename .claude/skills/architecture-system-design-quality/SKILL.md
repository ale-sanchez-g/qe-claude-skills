---
name: architecture-system-design-quality
description: Use this skill to evaluate architecture quality with coupling, blast radius, resilience pattern coverage, and drift metrics.
---

# Architecture & System Design Quality

Use this skill when validating architectural fitness and systemic design quality at scale.

## Tools
- Service dependency maps
- Change impact analysis
- Config and policy audits

## Script
- `bash .claude/skills/shared/scripts/generate_quality_report.sh architecture-system-design-quality 30`

## Metrics
- Service Coupling / Dependency Density
- Blast Radius per Change
- Number of Cross-Service Transactions
- Resilience Patterns Coverage (timeouts, retries, circuit breakers)
- Config vs Code Drift
