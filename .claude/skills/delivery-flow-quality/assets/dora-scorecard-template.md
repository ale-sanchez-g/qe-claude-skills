# DORA Scorecard — [Service/Team Name]

**Review Period**: [START DATE] → [END DATE]  
**Reviewer**: [Name]  
**Date**: [YYYY-MM-DD]

---

## 1. Deployment Frequency

| Metric                     | Value | Band   |
|----------------------------|-------|--------|
| Successful prod deploys    |       |        |
| Deploys per day            |       | ☐ Elite ☐ High ☐ Medium ☐ Low |
| Trend vs. prior period     |       | ☐ ↑ ☐ → ☐ ↓ |

Notes:
> _Observations on release cadence, batch size, or deploy blockers._

---

## 2. Lead Time for Changes

| Percentile | Value (hours) | Target        |
|------------|---------------|---------------|
| Median     |               | < 24h (Elite) |
| p75        |               |               |
| p95        |               |               |

Lead time stages (where time is spent):
- [ ] Coding: ___h
- [ ] Review wait: ___h
- [ ] Merge-to-pipeline: ___h
- [ ] Build + test: ___h
- [ ] Deploy rollout: ___h

Notes:
> _Identify the dominant bottleneck stage._

---

## 3. Change Failure Rate

| Metric                     | Value | Band   |
|----------------------------|-------|--------|
| Total prod releases        |       |        |
| Incident-causing releases  |       |        |
| CFR %                      |       | ☐ Elite (≤5%) ☐ High (≤10%) ☐ Medium (≤15%) ☐ Low |
| Trend vs. prior period     |       | ☐ ↑ ☐ → ☐ ↓ |

Top failure causes this period:
1. 
2. 
3. 

---

## 4. Mean Time to Recovery

| Percentile | Value (hours) | Target      |
|------------|---------------|-------------|
| Median     |               | < 1h (Elite)|
| p90        |               |             |

Recovery blockers identified:
- [ ] Detection delay
- [ ] Rollback complexity
- [ ] Runbook gaps
- [ ] On-call availability

---

## 5. Overall DORA Band

| Metric                 | Band |
|------------------------|------|
| Deployment Frequency   |      |
| Lead Time              |      |
| Change Failure Rate    |      |
| MTTR                   |      |
| **Overall (weakest)**  |      |

---

## 6. Priority Actions (next 30 days)

| Action                          | Owner | Expected Impact       | Due Date |
|---------------------------------|-------|-----------------------|----------|
|                                 |       |                       |          |
|                                 |       |                       |          |
|                                 |       |                       |          |

---

## 7. 30/60/90-Day Targets

| Metric         | Current | 30-day target | 60-day target | 90-day target |
|----------------|---------|---------------|---------------|---------------|
| Deploy freq/day|         |               |               |               |
| Median LT (h)  |         |               |               |               |
| CFR %          |         |               |               |               |
| MTTR median (h)|         |               |               |               |
