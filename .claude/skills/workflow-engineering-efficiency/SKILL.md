---
name: workflow-engineering-efficiency
description: Use this skill to measure engineering workflow efficiency with WIP, cycle time, PR review dynamics, and rework.
dependencies: python>=3.8
---

# Workflow & Engineering Efficiency

Use this skill to identify execution constraints that degrade quality, increase rework, and slow delivery.

## Required tools
- Work tracking metrics (state transitions, queue times)
- PR analytics (size, review latency, iteration count)
- Release and rollback history
- Ticket reopen/rework records

## Analysis runbook
1. Map value stream from "work started" to "work in production".
2. Measure WIP, cycle time, queue time, and throughput by team.
3. Analyze PR size/review delays and review quality signals.
4. Quantify rework via reopen/rollback/cherry-pick patterns.
5. Detect systemic flow constraints (handoffs, approvals, batching).
6. Define flow improvements with expected quality impact.

## Metric definitions (strict)
- **WIP**: active items not yet delivered
- **Cycle Time**: `in_progress_at -> production_at`
- **PR Size & Review Time**: LOC changed and time-to-approved
- **Rework Rate**: reopened tickets + rollbacks / completed changes

## Expert diagnostic patterns
- High WIP + long review delays: context switching and quality dilution.
- Large PRs with repeated review rounds: late design feedback.
- Stable throughput with high rework: speed achieved by cutting quality corners.

## Improvement interventions
- Set WIP limits with escalation for blocked work.
- Cap PR size and enforce review response SLOs.
- Shift design/risk review earlier (before large implementation).
- Track rework as a first-class quality KPI in retrospectives.

## Deliverables
- Flow efficiency scorecard and bottleneck analysis
- Review policy improvements with measurable targets
- Rework reduction plan tied to release stability

## Resources

### Scripts
- `scripts/pr_analytics.py` — Measure PR cycle time, first review latency, size distribution, rework rate, and WIP from a pull-requests CSV.
  ```
  python scripts/pr_analytics.py --prs prs.csv --days 30
  ```

### References
- `references/flow-efficiency-patterns.md` — Cycle time benchmarks, PR size guidelines, first review SLOs, rework rate interpretation, WIP limit guidance, value stream waste patterns, and SPACE framework alignment.

### Assets
- `assets/flow-value-stream-template.md` — Value stream assessment covering WIP, cycle time distribution, PR quality, rework rate, flow waste identification, and trend tracking.

## Script
- `bash .claude/skills/shared/scripts/generate_quality_report.sh workflow-engineering-efficiency 30`
