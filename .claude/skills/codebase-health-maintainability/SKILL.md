---
name: codebase-health-maintainability
description: Use this skill to track maintainability risks such as complexity, churn, duplication, coupling, and technical debt.
dependencies: python>=3.8
---

# Codebase Health & Maintainability

Use this skill to quantify structural code risk and prioritize debt reduction that materially improves delivery stability.

## Required tools
- Static analysis (complexity, duplication, violation severity)
- Git churn analytics by module/owner/time
- Architecture dependency insights (coupling/cohesion)
- Defect density and hot-spot history

## Analysis runbook
1. Establish module-level baseline for complexity/churn/duplication.
2. Build hotspot matrix: `high churn x high complexity x defect density`.
3. Distinguish intentional duplication from accidental duplication.
4. Track trend lines (not snapshots) to detect decay velocity.
5. Link maintainability metrics to incident/delivery outcomes.
6. Prioritize debt work by risk-adjusted ROI.

## Metric definitions (strict)
- **Complexity**: cyclomatic/cognitive complexity by file and function
- **Code Churn**: added/modified/deleted lines over time by module
- **Duplication Ratio**: duplicated LOC / total LOC
- **Coupling/Cohesion**: outgoing dependencies and domain boundary violations
- **Static Violations**: critical/major/minor counts and trend
- **Technical Debt Index**: estimated remediation effort / development effort

## Expert diagnostic patterns
- Rising churn in same modules: unstable requirements or weak design seams.
- High complexity + low coverage on hotspots: elevated regression probability.
- High coupling across domains: architecture erosion.

## Improvement interventions
- Refactor hotspot files first (not broad low-impact cleanups).
- Introduce architecture fitness checks and dependency boundaries.
- Add mandatory complexity caps for new/changed code.
- Track debt paydown as a productized backlog with outcome targets.

## Deliverables
- Hotspot heatmap with ownership
- Debt reduction plan tied to release-risk outcomes
- Guardrail policy proposal for code review and CI

## Resources

### Scripts
- `scripts/hotspot_analysis.py` — Combine git churn with structural complexity to score hotspot risk per file. Flags high-risk files and summarises debt signal.
  ```
  python scripts/hotspot_analysis.py --repo /path/to/repo --days 90 --top 20
  ```

### References
- `references/complexity-thresholds.md` — Industry thresholds for cyclomatic/cognitive complexity, churn risk classification, duplication ratios, and coupling metrics.

### Assets
- `assets/tech-debt-register-template.md` — Structured register for tracking hotspots, architecture violations, static analysis debt, and debt reduction plans.

## Script
- `bash .claude/skills/shared/scripts/generate_quality_report.sh codebase-health-maintainability 30`
