# Architecture Coupling & Resilience Pattern Reference

## Coupling Risk Thresholds

| Metric                    | Healthy   | At Risk    | Critical   |
|---------------------------|-----------|------------|------------|
| Avg outgoing deps/service | < 5       | 5–10       | > 10       |
| Avg incoming deps/service | < 8       | 8–15       | > 15       |
| Blast radius (services)   | < 3       | 3–8        | > 8        |
| Hop count (critical path) | ≤ 3       | 4–6        | > 6        |

## Resilience Pattern Definitions

### Timeout
Every synchronous call must declare a maximum wait time.
- Recommended default: 2–5 seconds for read operations; 30 seconds for write/long-running.
- Must not inherit caller's timeout — each hop should set its own.

### Retry with Backoff and Jitter
Retry is appropriate for transient failures (network blips, rate limiting).
- Max attempts: 3 (idempotent reads), 1–2 (writes/mutations)
- Backoff: exponential with jitter (`min(cap, base * 2^attempt) + rand`)
- Disable retry for non-idempotent operations without deduplication tokens.

### Circuit Breaker
Stops request flow to a failing dependency to prevent cascade failures.
- Open threshold: 50% error rate over a 10-second window
- Half-open probe: 1 request per 30 seconds
- Close threshold: 3 consecutive successes

### Bulkhead (Thread/Connection Pool Isolation)
Prevents one consumer from exhausting shared resources.
- Assign separate thread pools per downstream dependency.
- Size pools based on expected concurrency × timeout.

## Architecture Smell Patterns

| Pattern                   | Symptom                                          | Resolution                                 |
|---------------------------|--------------------------------------------------|--------------------------------------------|
| Distributed Monolith      | Many services with tight synchronous coupling    | Introduce async events; enforce boundaries |
| Shared Database           | Multiple services on one DB schema               | Schema decomposition; event sourcing       |
| Chatty API                | Hundreds of calls per user request               | Aggregation layer or BFF pattern           |
| Mega-Service              | Single service with many unrelated responsibilities | Decompose by bounded context              |
| Config Drift              | Running behavior differs from declared config    | GitOps; automated drift detection          |

## Dependency Direction Rule

Dependencies should always flow:
```
Presentation → Application → Domain → Infrastructure
```

Cross-layer violations (e.g., domain depending on infrastructure) indicate
architecture erosion and require immediate refactoring.

## Blast Radius Reduction Strategies

1. **Async event boundaries**: replace sync calls with events for non-latency-critical operations
2. **Strangler fig pattern**: isolate changing components behind stable interfaces
3. **API versioning**: prevent callers from coupling to implementation details
4. **Consumer-driven contracts**: validate interface compatibility before deploy

## References
- "Building Microservices" — Sam Newman
- "Release It!" — Michael Nygard
- CNCF Resilience Whitepaper
