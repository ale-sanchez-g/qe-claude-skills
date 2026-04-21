# Flow Efficiency & Engineering Workflow Reference

## Cycle Time Benchmarks

| Percentile  | Healthy   | At Risk    | Critical   |
|-------------|-----------|------------|------------|
| Median      | < 2 days  | 2–5 days   | > 5 days   |
| p75         | < 4 days  | 4–8 days   | > 8 days   |
| p95         | < 8 days  | 8–14 days  | > 14 days  |

Large p95/median ratios (> 4×) indicate inconsistent flow with hidden queue buildup.

## PR Size Guidelines

| Size          | LOC Changed | Risk                          | Review Quality          |
|---------------|-------------|-------------------------------|-------------------------|
| XS            | < 50        | Very low                      | Fast; thorough          |
| Small         | 50–200      | Low                           | Good                    |
| Medium        | 200–500     | Moderate                      | Drops as size grows     |
| Large         | 500–1000    | High                          | Significant review debt |
| XL            | > 1000      | Very high; decompose required | Superficial review risk |

Introduce a soft PR size limit of 400 LOC and hard limit of 800 LOC with exception approval.

## First Review Latency Targets

| SLO Target           | Notes                                                 |
|----------------------|-------------------------------------------------------|
| First review: 4 hours | Business hours only; rotate reviewers               |
| Re-review: 2 hours   | After author addresses feedback                      |
| Approval: 1 day      | Maximum from last review cycle                       |

Stale PRs (no activity > 48 hours) should trigger automated alerts to author and reviewer.

## Rework Rate Interpretation

Rework = reopened tickets + PR iteration count > 2 + production rollbacks.

| Rework Rate | Status    | Likely Root Cause                              |
|-------------|-----------|------------------------------------------------|
| < 5%        | Healthy   | Design clarity and test coverage are sufficient|
| 5–15%       | Moderate  | Upstream requirement instability or test gaps  |
| > 15%       | Critical  | Late design review; architectural drift        |

## WIP Limit Guidelines

WIP limits force prioritisation over parallelism and reduce context switching.

| Team Size | Max WIP (in-progress) | Notes                                |
|-----------|----------------------|--------------------------------------|
| 3–5       | 4–6                  | One WIP item per engineer preferred  |
| 6–10      | 8–12                 | Pair on complex items                |
| > 10      | Segment by squad     | Measure at squad level               |

## Value Stream Waste Patterns

| Waste Type          | Symptom                                          | Fix                                           |
|---------------------|--------------------------------------------------|-----------------------------------------------|
| Queue wait          | Work items idle between states                  | WIP limits + daily blocked-item review        |
| Handoff overhead    | Frequent cross-team dependencies in single work | Conways-law alignment; embed skills           |
| Rework              | Items returned to previous state                | Definition of Done; earlier review            |
| Over-processing     | More quality checks than risk warrants          | Right-size review by change class             |
| Batch inflation     | Large epics shipped at once                     | Vertical slicing; continuous delivery cadence |

## Key Flow Metrics (SPACE Framework Alignment)

| Dimension   | Metric                           |
|-------------|----------------------------------|
| Satisfaction| Survey scores + rework rate      |
| Performance | Deployment frequency + CFR       |
| Activity    | PR throughput + commit frequency |
| Communication| Review latency + collaboration   |
| Efficiency  | Cycle time + WIP                 |

## References
- "Team Topologies" — Matthew Skelton & Manuel Pais
- "Accelerate" — Forsgren, Humble, Kim
- SPACE Framework: https://queue.acm.org/detail.cfm?id=3454124
