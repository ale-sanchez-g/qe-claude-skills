# Technical Debt Register — [Service/Component Name]

**Owner**: [Name]  
**Last Updated**: [YYYY-MM-DD]  
**Review Cadence**: Monthly

---

## 1. Hotspot Summary

| File / Module | Complexity | Churn (90d) | Defect Count | Hotspot Score | Risk   |
|---------------|------------|-------------|--------------|---------------|--------|
|               |            |             |              |               | ☐ High |
|               |            |             |              |               | ☐ Med  |
|               |            |             |              |               | ☐ Low  |

---

## 2. Duplication Register

| Duplicated Block    | Files Affected | LOC | Removal Effort (h) | Priority |
|---------------------|----------------|-----|--------------------|----------|
|                     |                |     |                    |          |

---

## 3. Architecture Violations

| Violation                    | From Module | To Module | Severity | Remediation   |
|------------------------------|-------------|-----------|----------|---------------|
|                              |             |           |          |               |

---

## 4. Static Analysis Debt

| Severity | Count (this period) | Count (prior period) | Trend |
|----------|---------------------|----------------------|-------|
| Critical |                     |                      | ☐↑☐→☐↓|
| Major    |                     |                      | ☐↑☐→☐↓|
| Minor    |                     |                      | ☐↑☐→☐↓|

Technical Debt Ratio: ____%  (SonarQube rating: ☐ A ☐ B ☐ C ☐ D ☐ E)

---

## 5. Debt Reduction Plan

| Item                           | Effort (days) | Risk Reduction | Owner | Sprint Target |
|--------------------------------|---------------|----------------|-------|---------------|
|                                |               |                |       |               |
|                                |               |                |       |               |

---

## 6. Guardrail Policy Proposals

- [ ] Complexity cap for new/changed code: cyclomatic ≤ ___
- [ ] PR block on hotspot score increase without justification
- [ ] Architecture boundary check in CI pipeline
- [ ] Required test coverage threshold on high-risk modules: ___%

---

## 7. Trend Tracking

| Metric                  | 3 months ago | 2 months ago | Last month | This month |
|-------------------------|--------------|--------------|------------|------------|
| High-risk hotspot count |              |              |            |            |
| Technical debt ratio %  |              |              |            |            |
| Duplication ratio %     |              |              |            |            |
| Critical violations     |              |              |            |            |
