# SLO Design Patterns & Error Budget Reference

## Standard SLO Targets by Service Tier

| Tier  | Description                          | Availability Target | Error Rate SLO |
|-------|--------------------------------------|---------------------|----------------|
| Tier 1 | Revenue-critical / customer-facing  | 99.95%             | < 0.01%        |
| Tier 2 | Core internal / partner-facing      | 99.9%              | < 0.1%         |
| Tier 3 | Supporting / batch / analytics      | 99.5%              | < 1%           |

## Error Budget Calculation

```
Error budget (minutes/month) = (1 - SLO) × total_minutes_in_month
Example for 99.9% over 30 days:
  = 0.001 × 43,200 = 43.2 minutes
```

## Alerting on Error Budget Burn Rate

Prefer burn-rate alerts over static threshold alerts:

| Burn Rate | Lookback Window | Page?  | Urgency       |
|-----------|-----------------|--------|---------------|
| 14×       | 1 hour          | Yes    | Critical      |
| 6×        | 6 hours         | Yes    | High          |
| 3×        | 1 day           | Ticket | Medium        |
| 1×        | 3 days          | None   | Watch only    |

A 14× burn rate means you would exhaust the monthly budget in ~2 days.

## SLO Anti-patterns

- **SLOs set by intuition**: set from baseline + aspirational improvement, not gut feel
- **Measuring availability without user perspective**: use journey-level SLOs not host uptime
- **Single SLO per service**: multi-dimensional SLOs (availability, latency, error rate)
- **No error-budget policy**: error budget without a release/toil policy provides no feedback signal

## Latency SLO Guidance

Latency SLOs should be expressed on the request distribution, not averages:
- Set targets at p95 and p99 per critical endpoint/journey
- Track separately for authenticated vs. anonymous users
- Alert on sustained p99 breach, not transient spikes

## MTBF / Reliability Improvement Approach

1. Establish baseline MTBF and MTTR per service
2. Classify failures: deploy-induced, dependency, infra, or capacity
3. Prioritize root causes by frequency × severity × MTTR product
4. Implement targeted reliability investments (e.g., circuit breakers, caching, redundancy)
5. Re-measure after 30 days

## References
- Google SRE Book (Betsy Beyer et al.)
- SLO Academy: https://www.sloacademy.com/
