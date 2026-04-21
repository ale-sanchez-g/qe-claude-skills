# DORA Performance Band Benchmarks

Source: DORA State of DevOps Report (industry benchmarks)

## Performance Bands

| Metric                  | Elite              | High              | Medium               | Low                |
|-------------------------|--------------------|-------------------|----------------------|--------------------|
| Deployment Frequency    | Multiple/day       | 1/week–1/day      | 1/month–1/week       | < 1/month          |
| Lead Time for Changes   | < 1 hour           | 1 day – 1 week    | 1 week – 1 month     | > 1 month          |
| Change Failure Rate     | 0–5%               | 5–10%             | 10–15%               | > 15%              |
| MTTR                    | < 1 hour           | < 1 day           | 1 day – 1 week       | > 1 week           |

## Interpreting Your Band

**Elite** teams deploy on demand and restore service in under an hour. They use
feature flags, progressive delivery, and automated quality gates to maintain low CFR
despite high velocity.

**High** performers have automated pipelines but may rely on periodic releases.
Improving to Elite typically requires removing manual approval bottlenecks and
introducing trunk-based development.

**Medium** performers often struggle with batch releases, manual QA gates, and
infrequent production exposure. Priorities: reduce batch size, increase deploy
frequency, and improve rollback speed.

**Low** performers are characterized by fear-driven, infrequent deploys. Root causes
include unstable test suites, poor trunk hygiene, and heavy change-control processes.

## Key Anti-patterns

- Release trains that batch work for weeks → high CFR when deploys do occur
- Manual change approval boards adding days to lead time
- No automated rollback → MTTR measured in hours/days
- Incident tracking not linked to deploy ledger → inaccurate CFR/MTTR

## Lead Time Decomposition

Break lead time into stages to find the real constraint:
1. Coding time (commit to PR open)
2. Review time (PR open to approval)
3. Merge-to-deploy queue (approval to pipeline trigger)
4. Build + test duration
5. Deploy propagation (canary → full rollout)

## References
- Accelerate (Forsgren, Humble, Kim)
- DORA Quick Check: https://dora.dev/quickcheck/
