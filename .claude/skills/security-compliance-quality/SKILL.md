---
name: security-compliance-quality
description: Use this skill to track security quality with vulnerability density, remediation speed, secret exposure, and dependency risk.
---

# Security & Compliance Quality

Use this skill when assessing non-negotiable security and compliance quality outcomes.

## Tools
- Vulnerability scanners (SAST/SCA/DAST)
- Secret scanning alerts
- Dependency risk dashboards

## Script
- `bash .claude/skills/shared/scripts/generate_quality_report.sh security-compliance-quality 30`

## Metrics
- Vulnerability Density (per KLOC or service)
- Time to Remediate Vulnerabilities
- Secrets Exposure Incidents
- Dependency Risk Score (3rd party libraries)
