---
name: user-centric-quality
description: Use this skill to evaluate product quality outcomes from user and customer impact signals.
---

# User-Centric Quality (Outcome-Based)

Use this skill to assess quality through user impact, not internal proxy metrics.

## Required tools
- Product analytics funnels and journey success telemetry
- Customer support/defect tagging and escalation logs
- Apdex/CSAT/NPS datasets
- Feature adoption and churn analytics

## Analysis runbook
1. Define critical user journeys and success criteria.
2. Quantify escaped defects and customer-reported quality issues.
3. Measure failed journeys/error rates by segment and release cohort.
4. Correlate latency, reliability, and UX friction with adoption/churn.
5. Identify top quality drivers of customer dissatisfaction.
6. Propose experience-focused remediation backlog.

## Metric definitions (strict)
- **Customer-Reported Defects**: escaped defect count per period/release
- **User Error Rate/Failed Journeys**: failed completions / total attempts
- **Apdex/User Satisfaction**: satisfaction index over critical interactions
- **Feature Adoption Rate**: active feature users / eligible users
- **Churn due to Product Issues**: attributed churn linked to quality signals

## Expert diagnostic patterns
- Good internal quality metrics + poor adoption: outcome blind spots.
- Defect spikes after releases on specific segments: cohort-specific regressions.
- Improved reliability without Apdex gain: UX bottlenecks still unresolved.

## Improvement interventions
- Add release guardrails on journey-level success, not just endpoint uptime.
- Tighten support-to-engineering feedback loops with taxonomy standards.
- Prioritize fixes by user impact and revenue sensitivity.
- Include customer-impact metrics in release readiness criteria.

## Deliverables
- Journey quality scorecard with segment-level breakdown
- Escaped defect taxonomy and top impact clusters
- Outcome-driven improvement roadmap

## Script
- `bash .claude/skills/shared/scripts/generate_quality_report.sh user-centric-quality 30`
