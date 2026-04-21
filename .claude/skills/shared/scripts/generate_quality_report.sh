#!/usr/bin/env bash
set -euo pipefail

DOMAIN="${1:-}"
WINDOW_DAYS="${2:-30}"

if [[ -z "$DOMAIN" ]]; then
  echo "Usage: $0 <domain> [window_days]" >&2
  exit 1
fi

since_date="$(python - "$WINDOW_DAYS" <<'PY'
from datetime import datetime, timedelta, timezone
import sys

days = int(sys.argv[1])
print((datetime.now(timezone.utc) - timedelta(days=days)).strftime('%Y-%m-%d'))
PY
)"

print_header() {
  local title="$1"
  cat <<MD
# ${title} scorecard

- Time window: last ${WINDOW_DAYS} days (since ${since_date})
- Generated at: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
- Purpose: operational quality review with trend + diagnostic follow-up

MD
}

case "$DOMAIN" in
  delivery-flow-quality)
    print_header "Delivery & Flow Quality (DORA-aligned)"
    cat <<'MD'
## Metrics
- Lead Time for Changes
- Deployment Frequency
- Change Failure Rate
- Mean Time to Recovery (MTTR)

## Data sources
- Git commit/merge timestamps
- CI/CD deployment history
- Incident tickets and postmortems

## Calculation guidance
- Lead Time: production timestamp - commit timestamp (report median/p75/p95)
- CFR: incident-causing releases / total releases
- MTTR: incident resolved - incident started (report median and p90)

## Diagnostic checklist
- Identify queue delays (review, approval, release windows)
- Segment by service and change type
- Correlate CFR with release batch size
MD
    ;;
  reliability-production-stability)
    print_header "Reliability & Production Stability"
    cat <<'MD'
## Metrics
- Availability / Uptime (%)
- Mean Time Between Failures (MTBF)
- Incident Rate
- Incident Severity Distribution
- Error Rates (5xx, failed transactions)
- Latency / Response Time

## Data sources
- APM/monitoring dashboards
- Incident management timeline
- SLO and error budget reports

## Calculation guidance
- Availability = successful service time / total service time
- MTBF = total uptime / number of failures
- Latency and error rates should include p95/p99 and journey-level aggregation

## Diagnostic checklist
- Check severity mix and recurring fault domains
- Separate deploy-driven incidents from infra/dependency failures
- Verify error budget burn concentration by service
MD
    ;;
  codebase-health-maintainability)
    print_header "Codebase Health & Maintainability"
    cat <<'MD'
## Metrics
- Code Complexity (Cyclomatic, Cognitive)
- Code Churn
- Duplication Ratio
- Coupling / Cohesion Metrics
- Static Analysis Violations
- Technical Debt Index

## Data sources
- Static analysis tools
- Git churn history
- Architecture/code quality reports

## Calculation guidance
- Hotspot score = normalized(complexity) x normalized(churn) x normalized(defects)
- Debt index should track trend and remediation throughput
- Report complexity at function and file granularity

## Diagnostic checklist
- Highlight high-risk hotspots with active ownership
- Track architecture boundary violations
- Compare churn spikes against incident and rollback history
MD
    ;;
  architecture-system-design-quality)
    print_header "Architecture & System Design Quality"
    cat <<'MD'
## Metrics
- Service Coupling / Dependency Density
- Blast Radius per Change
- Number of Cross-Service Transactions
- Resilience Patterns Coverage
- Config vs Code Drift

## Data sources
- Service dependency maps
- Change impact analysis
- Resilience policy/config audits

## Calculation guidance
- Dependency density = avg inbound+outbound deps per service
- Blast radius = count of affected components/services per release
- Resilience coverage = guarded interactions / total critical interactions

## Diagnostic checklist
- Identify high-hop transactions in critical user flows
- Flag unguarded service boundaries
- Review config/code mismatches by environment
MD
    ;;
  operational-excellence-observability)
    print_header "Operational Excellence & Observability"
    cat <<'MD'
## Metrics
- Time to Detect (TTD)
- Alert Noise Ratio
- On-call Load / Alerts per Engineer
- Runbook Coverage
- Observability Coverage

## Data sources
- Alerting platform metrics
- On-call rotations
- Runbook repositories and telemetry standards

## Calculation guidance
- TTD = first actionable alert - incident start
- Alert noise ratio = non-actionable alerts / total alerts
- Observability coverage = critical flows with logs+metrics+traces

## Diagnostic checklist
- Identify top noisy alert classes by owner
- Map incidents without sufficient telemetry
- Audit runbook freshness and drill validation cadence
MD
    ;;
  security-compliance-quality)
    print_header "Security & Compliance Quality"
    cat <<'MD'
## Metrics
- Vulnerability Density
- Time to Remediate Vulnerabilities
- Secrets Exposure Incidents
- Dependency Risk Score

## Data sources
- SAST/SCA/DAST findings
- Vulnerability management SLA data
- Secret scanning alerts

## Calculation guidance
- Vulnerability density = open vulns / KLOC (or service)
- Remediation time = resolved_at - detected_at by severity
- Dependency risk score should weight CVSS, exploitability, and asset criticality

## Diagnostic checklist
- Flag SLA breaches by severity and owner
- Identify repeated secret exposure sources
- Track risk concentration in transitive dependencies
MD
    ;;
  user-centric-quality)
    print_header "User-Centric Quality"
    cat <<'MD'
## Metrics
- Customer-Reported Defects
- User Error Rate / Failed Journeys
- Apdex / User Satisfaction Score
- Feature Adoption Rate
- Churn due to Product Issues

## Data sources
- Product analytics and support tickets
- UX telemetry and session funnels
- CSAT/NPS/Apdex dashboards

## Calculation guidance
- Failed journey rate = failed completions / total attempts
- Adoption rate = active feature users / eligible users
- Churn attribution should be cohort-based and linked to quality events

## Diagnostic checklist
- Segment issues by customer tier and journey
- Correlate reliability/latency shifts with satisfaction drop
- Identify escaped defects with highest business impact
MD
    ;;
  workflow-engineering-efficiency)
    print_header "Workflow & Engineering Efficiency"
    cat <<'MD'
## Metrics
- Work in Progress (WIP)
- Cycle Time
- PR Size & Review Time
- Rework Rate

## Data sources
- Work tracking tools
- Pull request analytics
- Rollback/reopen incident links

## Calculation guidance
- Cycle time = in-progress timestamp -> production timestamp
- Rework rate = reopened items + rollbacks / completed changes
- Review latency should include wait-for-first-review and wait-for-reapproval

## Diagnostic checklist
- Detect queue accumulation by workflow state
- Track oversized PR impact on review delay and rework
- Correlate WIP spikes with incident or rollback frequency
MD
    ;;
  *)
    echo "Unsupported domain: $DOMAIN" >&2
    exit 2
    ;;
esac
