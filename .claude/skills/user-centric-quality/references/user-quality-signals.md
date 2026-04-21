# User-Centric Quality Signal Reference

## Journey Success Rate Thresholds

| Rate        | Status    | Recommended Action                                   |
|-------------|-----------|------------------------------------------------------|
| > 97%       | Healthy   | Monitor; run preventive experiments                  |
| 92–97%      | At risk   | Root cause analysis; A/B test improvements           |
| 85–92%      | Degraded  | Escalate to product + engineering; immediate sprint  |
| < 85%       | Critical  | All-hands remediation; release freeze consideration  |

## Apdex (Application Performance Index)

```
Apdex = (Satisfied + Tolerating × 0.5) / Total

Satisfied:   response_time ≤ T
Tolerating:  T < response_time ≤ 4T
Frustrated:  response_time > 4T
```

Common T values:
- Checkout / payment: T = 2 seconds
- Page load: T = 3 seconds
- API call: T = 500 ms
- Search: T = 1 second

| Apdex Score | Grade | User Perception          |
|-------------|-------|--------------------------|
| 1.0–0.94    | A     | Excellent                |
| 0.94–0.85   | B     | Good                     |
| 0.85–0.70   | C     | Fair                     |
| 0.70–0.50   | D     | Poor                     |
| < 0.50      | F     | Unacceptable             |

## Customer-Reported Defect Classification

| Class              | Definition                                         | SLA for Fix |
|--------------------|-----------------------------------------------------|-------------|
| Data loss          | User data corrupted or deleted                     | Immediate   |
| Blocking defect    | Core journey blocked (cannot checkout, login, etc.)| 24 hours    |
| Significant defect | Feature broken but workaround exists               | 72 hours    |
| Minor defect       | UI issue, cosmetic, or infrequent edge case        | Sprint      |

## Feature Adoption Signal Interpretation

| Adoption Rate (30-day) | Interpretation                                      |
|------------------------|-----------------------------------------------------|
| < 5%                   | Likely discoverability or usability failure         |
| 5–20%                  | Early adoption; validate with user research         |
| 20–50%                 | Growing adoption; identify activation bottlenecks   |
| > 50%                  | Strong adoption; optimise retention/depth of use    |

## Release Cohort Quality Analysis

Compare the same journey success rate across release cohorts to detect regressions:
1. Group users by the version they first experienced after a deploy
2. Compute success rate per cohort for the same journey
3. A sudden drop in a new cohort vs. prior cohort indicates a release regression
4. Segment by platform (mobile/web), geography, and user tier for precision

## Feedback Signal Sources (Ranked by Signal Quality)

| Source                   | Signal Quality | Latency   | Notes                            |
|--------------------------|---------------|-----------|----------------------------------|
| Failed journey telemetry | Very High     | Real-time | Most actionable                  |
| Support ticket tags      | High          | Hours     | Requires taxonomy discipline     |
| NPS verbatim comments    | Medium        | Days      | Rich context, low volume         |
| App store reviews        | Medium        | Days      | High visibility, noisy           |
| CSAT surveys             | Medium        | Days      | Biased toward extremes           |
| Social media mentions    | Low           | Real-time | Very noisy; only flag P1 patterns|

## Escaped Defect Cost Estimation

Use this model to prioritise customer-facing fixes:
```
impact_score = defect_frequency × affected_user_pct × journey_revenue_weight
```

Focus remediation on defects with impact_score in the top decile.
