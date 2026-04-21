---
name: delivery-flow-quality
description: Use this skill to assess DORA-aligned delivery quality by measuring lead time, deployment frequency, change failure rate, and MTTR.
dependencies: python>=3.12
---

# Delivery & Flow Quality (DORA-aligned)

Use this skill to run a full DORA assessment, identify systemic bottlenecks, and produce a prioritized improvement plan tied to business risk.

## Required tools
- Git history (commit, merge, and tag/deploy markers)
- CI/CD run history (successful/failed production deploys)
- Incident/postmortem records linked to deploys
- Work-tracking data for commit-to-prod traceability

## Analysis runbook
1. **Build change ledger**: map each production deploy to included commits/PRs.
2. **Compute core DORA metrics** for the same time window/team boundaries.
3. **Segment results** by service, team, risk class, and change type.
4. **Correlate failures with delivery speed** (size, batching, review delay, release train policy).
5. **Identify queueing hotspots** (PR wait, QA wait, release approval, deploy freeze windows).
6. **Output interventions** with owner, expected effect, and review date.

## Metric definitions (strict)
- **Lead Time for Changes**: `production_timestamp - commit_timestamp` (report median/p75/p95)
- **Deployment Frequency**: successful production deploys per day/week
- **Change Failure Rate**: `failed_deploys_or_incident_causing_releases / total_releases`
- **MTTR**: `incident_resolved_at - incident_started_at` (median and p90)

## Expert diagnostic patterns
- High lead time + low failure rate: excessive controls/manual approvals.
- High frequency + high CFR: unsafe release slicing or weak safeguards.
- Low frequency + long MTTR: brittle rollback strategy, weak runbooks.
- Large p95 lead-time gap vs median: inconsistent flow and hidden queues.

## Improvement interventions
- Enforce smaller PR/release batch size thresholds.
- Introduce progressive delivery (canary + automatic rollback).
- Add PR aging SLOs and blocked-work escalation policy.
- Standardize incident-to-release linkage for accurate CFR/MTTR.

## Deliverables
- DORA scorecard by service/team
- Bottleneck map (where time is spent)
- 30/60/90-day action plan with expected metric movement

## Resources

### Scripts
- `scripts/compute_dora.py` — Compute all four DORA metrics from git history and a deployments CSV. Classifies output into an Elite/High/Medium/Low performance band.
  ```
  python scripts/compute_dora.py --repo /path/to/repo --deployments deploys.csv --days 30
  ```

### References
- `references/dora-benchmarks.md` — DORA performance band thresholds, lead time decomposition stages, and key anti-patterns.

### Assets
- `assets/dora-scorecard-template.md` — Fillable scorecard template for per-service/team DORA reviews including 30/60/90-day targets.

## Script
- `bash .claude/skills/shared/scripts/generate_quality_report.sh delivery-flow-quality 30`
