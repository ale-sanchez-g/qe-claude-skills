---
name: operational-excellence-observability
description: Use this skill to measure detection and response quality through alert signal quality, on-call load, runbooks, and telemetry coverage.
dependencies: python>=3.12
---

# Operational Excellence & Observability

Use this skill to evaluate detection/response effectiveness and reduce operational toil while increasing incident handling precision.

## Required tools
- Alerting and paging analytics
- On-call schedule/interruptions data
- Runbook coverage inventory and freshness checks
- Logs/metrics/traces instrumentation maps

## Analysis runbook
1. Compute TTD, alert noise, and on-call load by team/service.
2. Classify alerts into actionable, duplicate, noisy, and stale.
3. Audit runbook existence, completeness, and last validation date.
4. Measure telemetry completeness for critical user journeys.
5. Identify detector blind spots from postmortem timelines.
6. Propose detection and runbook improvements with ownership.

## Metric definitions (strict)
- **TTD**: `first_actionable_signal_at - incident_start_at`
- **Alert Noise Ratio**: non-actionable alerts / total alerts
- **On-call Load**: pages per engineer per rotation window
- **Runbook Coverage**: % critical alerts with validated runbooks
- **Observability Coverage**: % critical flows with logs+metrics+traces

## Expert diagnostic patterns
- Low TTD but high MTTR: good detection, poor diagnosis/recovery.
- High page volume with low incident conversion: noisy alert policies.
- Observability gaps on top revenue journeys: unacceptable risk exposure.

## Improvement interventions
- Consolidate and deduplicate alerts by symptom hierarchy.
- Add SLO-burn-rate alerts over threshold-only alerts.
- Require runbook validation in incident readiness drills.
- Enforce telemetry minimum standards for every service.

## Deliverables
- Alert quality report and cleanup backlog
- On-call sustainability assessment
- Telemetry gap closure plan by critical journey

## Resources

### Scripts
- `scripts/alert_quality_audit.py` — Score alert quality (noise ratio, actionable vs. noisy), on-call load, and TTD proxy from an alerts CSV.
  ```
  python scripts/alert_quality_audit.py --alerts alerts.csv --days 30
  ```

### References
- `references/observability-standards.md` — Three-pillar minimum standards (logs/metrics/traces), alert quality classification, TTD targets, on-call sustainability thresholds, and runbook requirements.

### Assets
- `assets/runbook-template.md` — Standardised runbook structure with diagnosis steps, escalation path, rollback procedure, and post-incident checklist.

## Script
- `bash .claude/skills/shared/scripts/generate_quality_report.sh operational-excellence-observability 30`
