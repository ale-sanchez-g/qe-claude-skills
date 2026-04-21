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
MD
    ;;
  *)
    echo "Unsupported domain: $DOMAIN" >&2
    exit 2
    ;;
esac
