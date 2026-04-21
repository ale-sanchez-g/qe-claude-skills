---
name: reliability-production-stability
description: Use this skill to evaluate quality through production reliability, uptime, error rates, incident trends, and latency.
---

# Reliability & Production Stability

Use this skill when validating whether quality holds under real production conditions.

## Tools
- Monitoring/APM dashboards
- Incident management data
- SLO/error budget reporting

## Script
- `bash .claude/skills/shared/scripts/generate_quality_report.sh reliability-production-stability 30`

## Metrics
- Availability / Uptime (%)
- Mean Time Between Failures (MTBF)
- Incident Rate (per deploy or per period)
- Incident Severity Distribution
- Error Rates (5xx, failed transactions)
- Latency / Response Time
