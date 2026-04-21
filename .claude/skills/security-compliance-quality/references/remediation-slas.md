# Security Vulnerability Remediation SLAs & Risk Scoring Reference

## Remediation SLA by Severity

| Severity  | CVSS Range | Remediation SLA | Escalation if Breached         |
|-----------|------------|-----------------|--------------------------------|
| Critical  | 9.0–10.0   | 7 days          | CISO + VP Engineering          |
| High      | 7.0–8.9    | 30 days         | Engineering Director           |
| Medium    | 4.0–6.9    | 90 days         | Team Lead                      |
| Low       | 0.1–3.9    | 180 days        | Backlog review                 |

Exceptions require documented approval with compensating controls and a hard deadline.

## Risk Score Formula

```
risk_score = (CVSS / 10) × exploit_weight × asset_tier_weight
```

**Exploit Maturity Weights**
| Maturity          | Weight |
|-------------------|--------|
| High (weaponised) | 1.0    |
| Functional PoC    | 0.8    |
| Proof of Concept  | 0.5    |
| None/Theoretical  | 0.2    |

**Asset Tier Weights**
| Tier   | Description                    | Weight |
|--------|--------------------------------|--------|
| Tier 1 | Customer-facing / PII / revenue| 1.0    |
| Tier 2 | Internal tools / partner APIs  | 0.7    |
| Tier 3 | Dev tooling / low-impact       | 0.4    |

Prioritise remediations by risk_score descending, not just CVSS severity.

## Dependency Risk Assessment

Evaluate third-party dependencies on three axes:
1. **Severity**: CVSS score of known vulnerabilities
2. **Exploit Maturity**: is active exploitation occurring in the wild?
3. **Transitive Exposure**: is the vulnerable code reachable in your call graph?

If all three are high → treat as equivalent to Critical even if CVSS is High.

## Secret Exposure Response Procedure

1. **Detect** → automated scan fires (pre-commit hook, push protection, or scheduled scan)
2. **Rotate** → invalidate and reissue credentials within **1 hour** of detection
3. **Audit** → determine exposure window and what was accessible
4. **Notify** → inform security team and affected service owners
5. **Root cause** → identify how the secret was committed and fix the gap
6. **Post-mortem** → document in security incident tracker

**Exposure window SLA**: rotation must complete within 1 hour of confirmed exposure.

## Recurring Pattern Indicators

- Same developer or repo repeatedly commits secrets → targeted process gap
- Rising vulnerability age on same CVE → active suppression or ownership gap
- High transitive dependency risk → lack of SBOM and supply-chain governance

## Compliance Mapping (Common Frameworks)

| Control Area          | PCI-DSS            | SOC 2 (CC)   | ISO 27001      |
|-----------------------|--------------------|--------------|----------------|
| Vuln scanning         | Req 6.3.3          | CC7.1        | A.12.6.1       |
| Patch management      | Req 6.3.3          | CC7.2        | A.12.6.1       |
| Secret management     | Req 3, Req 8       | CC6.1        | A.9.4.3        |
| Third-party risk      | Req 12.8           | CC9.2        | A.15.2.1       |

## Recommended Tooling
- **SAST**: Semgrep, CodeQL
- **SCA**: Dependabot, Snyk, OWASP Dependency-Check
- **Secret scanning**: GitHub Advanced Security, truffleHog, detect-secrets
- **Container scanning**: Trivy, Grype
- **DAST**: OWASP ZAP, Burp Suite
