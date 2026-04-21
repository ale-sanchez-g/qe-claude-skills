# Code Complexity & Maintainability Thresholds

## Cyclomatic Complexity Thresholds

| Score     | Risk Level | Recommended Action                          |
|-----------|------------|---------------------------------------------|
| 1–5       | Low        | No action required                          |
| 6–10      | Moderate   | Consider refactoring, add unit tests        |
| 11–20     | High       | Refactor; complex logic, high defect risk   |
| > 20      | Critical   | Block new features until complexity reduced |

Source: McCabe & Associates / SEI CMU guidance

## Cognitive Complexity (Sonar Scale)

Cognitive complexity measures how hard code is to understand (not just branching paths).

- **Target**: < 15 per function
- **Action required**: ≥ 25
- **Block PRs**: ≥ 50 on new/modified code

## Code Churn Risk Classification

Churn = number of times a file is modified over a window.

| Churn Percentile | Classification  | Combined Risk Signal                            |
|------------------|-----------------|-------------------------------------------------|
| Top 10%          | High churn      | Elevated risk if also high complexity           |
| Top 10% + CC>10  | Hotspot         | High defect probability; immediate focus        |
| Top 10% + defects| Critical        | Block non-bug changes; stabilise first          |

## Duplication Thresholds

| Duplication Ratio | Status    | Action                                         |
|-------------------|-----------|------------------------------------------------|
| < 3%              | Healthy   | Monitor                                        |
| 3–10%             | Moderate  | Deduplicate during normal refactoring          |
| > 10%             | High      | Scheduled debt sprint                          |
| > 20%             | Critical  | Architecture review; likely domain model issue |

## Coupling Metrics (Package/Module Level)

- **Afferent coupling (Ca)**: services/modules that depend on this one (incoming). High Ca = high blast radius.
- **Efferent coupling (Ce)**: services/modules this one depends on (outgoing). High Ce = high fragility.
- **Instability (I)**: `Ce / (Ca + Ce)`. Range 0 (stable) to 1 (unstable).
- **Target**: high-Ca components should have low I (stable abstractions principle).

## Technical Debt Ratio (SonarQube)

- **A (0–5%)**: Excellent
- **B (6–10%)**: Good
- **C (11–20%)**: Fair
- **D (21–50%)**: Poor — set remediation targets
- **E (>50%)**: Critical — reassess component viability

## Hotspot Scoring Formula

```
hotspot_score = 0.50 × norm(churn) + 0.35 × norm(complexity) + 0.15 × norm(LOC)
```

Files with hotspot_score > 0.65 require immediate remediation planning.

## Recommended Tooling
- **radon** (Python): cyclomatic and cognitive complexity
- **lizard**: multi-language complexity and function length
- **SonarQube/SonarCloud**: full debt tracking with trend reporting
- **CodeScene**: churn × complexity hotspot analysis with team annotation
