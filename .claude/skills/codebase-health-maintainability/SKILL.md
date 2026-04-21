---
name: codebase-health-maintainability
description: Use this skill to track maintainability risks such as complexity, churn, duplication, coupling, and technical debt.
---

# Codebase Health & Maintainability

Use this skill when assessing internal quality factors that predict instability and long-term delivery drag.

## Tools
- Static analysis tools
- Git churn analysis
- Code quality reports

## Script
- `bash .claude/skills/shared/scripts/generate_quality_report.sh codebase-health-maintainability 30`

## Metrics
- Code Complexity (Cyclomatic, Cognitive)
- Code Churn (added/modified/deleted)
- Duplication Ratio
- Coupling / Cohesion Metrics
- Static Analysis Violations (critical vs minor)
- Technical Debt Index
