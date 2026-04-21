# Observability Standards & Alert Quality Reference

## Three Pillars: Minimum Standards per Service

### Logs
- Structured JSON logs for all request/response and error events
- Fields required: `timestamp`, `trace_id`, `span_id`, `service`, `level`, `message`, `user_id` (if applicable)
- Error logs must include stack trace and causal context
- Log sampling allowed only for high-volume success paths; always log errors at 100%

### Metrics
- Expose RED metrics per service: Request rate, Error rate, Duration (latency)
- Latency histograms (not summaries) to support cross-service aggregation
- Emit all critical business KPIs as custom metrics (e.g., orders placed, payments processed)
- Alert thresholds derived from SLO burn rate — not static value comparisons

### Traces
- All inbound requests must propagate trace context (W3C TraceContext or B3)
- Instrument external calls, DB queries, cache ops, and async message publishes
- Trace sampling: 100% for errors, ≥1% for success paths (adjust per volume)

## Alert Quality Classification

| Class        | Definition                                             | Target Action           |
|--------------|--------------------------------------------------------|-------------------------|
| Actionable   | Alert signals a specific, known failure requiring human action | Page / ticket  |
| Informational | Event of interest; no immediate action needed         | Dashboard only          |
| Noisy        | Fires frequently with no correlated user impact        | Suppress / remove       |
| Stale        | Was actionable; no longer reflects current system     | Delete or update        |

## Alert Design Principles

1. **Alert on symptoms, not causes** — page on user-visible impact, not internal signals
2. **Every alert must have a runbook** — linked in the alert body
3. **One alert per failure mode** — deduplicate before reaching on-call
4. **Test alerts in staging** before production deployment
5. **Review alerts that auto-resolve in < 1 minute** — likely noise

## TTD Improvement Targets

| Current TTD   | Target          | Priority                        |
|---------------|-----------------|---------------------------------|
| > 30 min      | < 10 min        | Critical — add leading indicators|
| 10–30 min     | < 5 min         | High — tune SLO burn-rate alerts |
| < 5 min       | < 2 min         | Medium — refine anomaly detection|

## On-Call Sustainability Thresholds

| Pages/engineer/week | Status    | Action                                          |
|---------------------|-----------|-------------------------------------------------|
| ≤ 2                 | Healthy   | Monitor                                         |
| 3–5                 | At risk   | Alert cleanup sprint                            |
| > 5                 | Critical  | Escalate; risk of on-call burnout and attrition |

## Runbook Minimum Requirements

Every runbook must include:
1. Alert description and triggering condition
2. Immediate investigation steps (first 5 minutes)
3. Known causes and their resolution steps
4. Escalation path and contacts
5. Rollback procedure (if deploy-related)
6. Post-incident follow-up checklist
7. Last validated date (must be within 6 months)

## Recommended Tooling
- Prometheus + Alertmanager (metrics and alerting)
- OpenTelemetry (tracing and unified instrumentation)
- Grafana (dashboards with SLO panels)
- PagerDuty / OpsGenie (on-call management and analytics)
