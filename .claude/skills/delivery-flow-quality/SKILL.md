---
name: delivery-flow-quality
description: Use this skill to assess DORA-aligned delivery quality by measuring lead time, deployment frequency, change failure rate, and MTTR.
---

# Delivery & Flow Quality (DORA-aligned)

Use this skill when you need leading indicators of software delivery quality and organizational resilience.

## Tools
- Git history and tags
- CI/CD deployment history
- Incident/postmortem tracking

## Script
- `bash .claude/skills/shared/scripts/generate_quality_report.sh delivery-flow-quality 30`

## Metrics
- Lead Time for Changes
- Deployment Frequency
- Change Failure Rate
- Mean Time to Recovery (MTTR)
