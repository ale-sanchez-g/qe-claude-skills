# Runbook: [Alert Name]

**Service**: [service-name]  
**Alert ID**: [alert-id]  
**Severity**: ☐ Critical ☐ High ☐ Medium ☐ Low  
**Owner**: [team-name]  
**Last Validated**: [YYYY-MM-DD]  
**Validation Method**: ☐ Game day ☐ Incident ☐ Drill

---

## 1. What Is Happening

> _One paragraph describing what the alert signals and why it matters to users._

**Alert condition**:
```
[Insert PromQL / alert rule]
```

**User impact**: [Describe user-visible effect if not immediately resolved]

---

## 2. First 5 Minutes

1. Acknowledge alert in [PagerDuty / OpsGenie]
2. Open dashboard: [URL]
3. Check recent deploys: [deploy dashboard URL]
4. Check dependency status: [status page / health endpoint]
5. Assess: is this impacting users? (check journey success rate: [URL])

---

## 3. Diagnosis Steps

### Step A — [Most Likely Cause]
- Check: [specific metric / log query]
- Indicators: [what you'd see]
- Action: [what to do]

### Step B — [Second Most Likely Cause]
- Check: [specific metric / log query]
- Indicators: [what you'd see]
- Action: [what to do]

### Step C — [Dependency or Infrastructure Cause]
- Check: [external status page / internal health endpoint]
- Action: [notify upstream / apply workaround]

---

## 4. Resolution Steps

### Option 1: [Primary Resolution]
```bash
# Command or procedure
```
Expected outcome: [describe what changes after this step]

### Option 2: [Rollback]
```bash
# Rollback command
```
Time to effect: ___  
Confirm recovery by checking: [metric / journey success rate]

---

## 5. Escalation Path

| Condition                              | Escalate To                | Contact          |
|----------------------------------------|----------------------------|------------------|
| No progress after 15 min               | On-call lead               | [name / channel] |
| User-visible impact > 10%              | Incident commander         | [name / channel] |
| Data loss or security concern          | CISO + Engineering Director| [contact]        |

---

## 6. Post-Incident Checklist

- [ ] Incident resolved and alert cleared
- [ ] Timeline documented in incident tracker
- [ ] Affected users notified (if applicable)
- [ ] Postmortem scheduled (Sev1/Sev2)
- [ ] Runbook updated with new findings
- [ ] Follow-up action items created in backlog

---

## 7. Related Resources
- Dashboard: [URL]
- Logs: [URL or query]
- Architecture diagram: [URL]
- Previous incidents: [link to search]
