# Flow & Value Stream Assessment — [Team Name]

**Review Period**: [START DATE] → [END DATE]  
**Reviewer**: [Name]  
**Date**: [YYYY-MM-DD]

---

## 1. WIP & Throughput

| Metric                       | Value | Target  |
|------------------------------|-------|---------|
| Current WIP items            |       | ≤ ___   |
| PRs merged (this period)     |       |         |
| Avg PRs merged/day           |       |         |
| Blocked items (> 2 days)     |       | 0       |

---

## 2. Cycle Time Distribution

| Percentile | Value (hours) | Benchmark     |
|------------|---------------|---------------|
| Median     |               | < 48h         |
| p75        |               | < 96h         |
| p95        |               | < 192h        |

p95 / Median ratio: ___ (target < 3×)

Dominant queue stage (where time is spent):
- [ ] Requirements / design: ___h avg
- [ ] Implementation: ___h avg
- [ ] Code review: ___h avg
- [ ] CI / testing: ___h avg
- [ ] Deploy / release approval: ___h avg

---

## 3. PR Review Quality

| Metric                     | Value | Target    |
|----------------------------|-------|-----------|
| Avg PR size (LOC)          |       | < 400     |
| PRs > 800 LOC (XL)         |       | 0         |
| Median first review (h)    |       | < 4h      |
| Median full cycle (h)      |       | < 24h     |
| PRs with > 2 iterations    |       | < 10%     |

---

## 4. Rework Rate

| Category                   | Count | % of Total |
|----------------------------|-------|------------|
| Reopened tickets           |       |            |
| Production rollbacks       |       |            |
| PRs requiring > 2 reviews  |       |            |
| **Total rework events**    |       |            |

Rework rate: ___% (target < 10%)

---

## 5. Flow Waste Identified

| Waste Type            | Observed? | Severity | Proposed Fix           |
|-----------------------|-----------|----------|------------------------|
| Queue wait            | ☐ Yes ☐ No|          |                        |
| Handoff overhead      | ☐ Yes ☐ No|          |                        |
| Rework                | ☐ Yes ☐ No|          |                        |
| Over-processing       | ☐ Yes ☐ No|          |                        |
| Batch inflation       | ☐ Yes ☐ No|          |                        |

---

## 6. Improvement Actions

| Action                             | Owner | Expected Impact         | Due Date |
|------------------------------------|-------|-------------------------|----------|
|                                    |       |                         |          |
|                                    |       |                         |          |

---

## 7. Trend Tracking

| Metric              | 3 months ago | 2 months ago | Last month | This month |
|---------------------|--------------|--------------|------------|------------|
| Median cycle time h |              |              |            |            |
| WIP avg             |              |              |            |            |
| Rework rate %       |              |              |            |            |
| Avg PR size LOC     |              |              |            |            |
