---
name: security-compliance-quality
description: Use this skill to track security quality with vulnerability density, remediation speed, secret exposure, and dependency risk.
---

# Security & Compliance Quality

Use this skill to evaluate security risk exposure and remediation discipline as first-class quality indicators.

## Required tools
- SAST/SCA/DAST and container scanning reports
- Secret scanning alerts and response history
- Dependency inventory with CVE severity/age
- Compliance controls evidence and exception records

## Analysis runbook
1. Build vulnerability inventory normalized by service size/criticality.
2. Measure remediation lead time by severity and ownership.
3. Analyze secret exposure incidents and containment latency.
4. Score third-party dependency risk (criticality x exploitability x age).
5. Identify recurring policy exceptions and control drift.
6. Produce remediation roadmap with SLA and ownership.

## Metric definitions (strict)
- **Vulnerability Density**: open vulns / KLOC (or per service)
- **Time to Remediate**: `resolved_at - detected_at`, segmented by severity
- **Secrets Exposure Incidents**: count and exposure duration
- **Dependency Risk Score**: weighted CVSS, exploit maturity, asset criticality

## Expert diagnostic patterns
- Falling vuln counts with rising age: backlog stagnation hidden by volume.
- Repeated secret leaks in same repos: process gap, not one-off mistakes.
- High risk concentration in transitive dependencies: supply-chain blind spot.

## Improvement interventions
- Enforce severity-based remediation SLAs and breach escalation.
- Add pre-merge secret scanning and push protection controls.
- Reduce dependency sprawl and pin high-risk packages.
- Track security debt alongside product roadmap commitments.

## Deliverables
- Security quality scorecard by service/tier
- SLA compliance and overdue-risk report
- Prioritized remediation plan with risk burn-down targets

## Script
- `bash .claude/skills/shared/scripts/generate_quality_report.sh security-compliance-quality 30`
