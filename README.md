# qe-claude-skills
A set of QE skills for claude code

## Included skills

- Delivery & Flow Quality (DORA-aligned)
- Reliability & Production Stability
- Codebase Health & Maintainability
- Architecture & System Design Quality
- Operational Excellence & Observability
- Security & Compliance Quality
- User-Centric Quality (Outcome-Based)
- Workflow & Engineering Efficiency

Each skill lives under `.claude/skills/<skill-name>/SKILL.md` and can use:

`bash .claude/skills/shared/scripts/generate_quality_report.sh <domain> [window_days]`

The skills are designed as expert playbooks with strict metric definitions, diagnostic patterns, and intervention guidance.
