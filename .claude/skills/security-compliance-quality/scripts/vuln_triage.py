#!/usr/bin/env python3
"""
vuln_triage.py — Triage open vulnerabilities by risk and remediation SLA status.

Usage:
    python vuln_triage.py --vulns vulns.csv --days 90

Vulnerabilities CSV schema:
    vuln_id, service, severity, cvss_score, detected_at, resolved_at, exploit_maturity, asset_tier
    (severity: critical | high | medium | low)
    (exploit_maturity: proof_of_concept | functional | high | none)
    (asset_tier: tier1 | tier2 | tier3)
    (resolved_at: empty if open)

SLA targets (days to remediate):
    Critical: 7  |  High: 30  |  Medium: 90  |  Low: 180

Output: JSON with density, SLA compliance, overdue breakdown, and risk scores.
"""

import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import median


SLA_DAYS: dict[str, int] = {
    "critical": 7,
    "high": 30,
    "medium": 90,
    "low": 180,
}

EXPLOIT_WEIGHT: dict[str, float] = {
    "high": 1.0,
    "functional": 0.8,
    "proof_of_concept": 0.5,
    "none": 0.2,
}

TIER_WEIGHT: dict[str, float] = {
    "tier1": 1.0,
    "tier2": 0.7,
    "tier3": 0.4,
}


def parse_iso(s: str) -> datetime | None:
    try:
        return datetime.fromisoformat(s).astimezone(timezone.utc)
    except (ValueError, AttributeError):
        return None


def risk_score(cvss: float, exploit_maturity: str, asset_tier: str) -> float:
    ew = EXPLOIT_WEIGHT.get(exploit_maturity.lower(), 0.2)
    tw = TIER_WEIGHT.get(asset_tier.lower(), 0.4)
    return round((cvss / 10.0) * ew * tw, 4)


def compute_triage(vulns_csv: Path, days: int) -> dict:
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=days)

    vulns: list[dict] = []
    with vulns_csv.open() as fh:
        for row in csv.DictReader(fh):
            detected = parse_iso(row.get("detected_at", ""))
            if not detected or detected < cutoff:
                continue
            resolved = parse_iso(row.get("resolved_at", ""))
            sev = row.get("severity", "low").lower()
            age_days = (now - detected).days
            sla_days = SLA_DAYS.get(sev, 180)
            sla_breached = resolved is None and age_days > sla_days
            remediation_days = (resolved - detected).days if resolved else None

            try:
                cvss = float(row.get("cvss_score", 0))
            except ValueError:
                cvss = 0.0

            vulns.append({
                **row,
                "detected_at": detected,
                "resolved_at": resolved,
                "age_days": age_days,
                "sla_days": sla_days,
                "sla_breached": sla_breached,
                "remediation_days": remediation_days,
                "risk_score": risk_score(cvss, row.get("exploit_maturity", "none"), row.get("asset_tier", "tier3")),
            })

    open_vulns = [v for v in vulns if not v["resolved_at"]]
    closed_vulns = [v for v in vulns if v["resolved_at"]]

    # SLA compliance
    sla_by_sev: dict[str, dict] = {}
    for sev in ("critical", "high", "medium", "low"):
        sev_open = [v for v in open_vulns if v.get("severity", "").lower() == sev]
        sev_closed = [v for v in closed_vulns if v.get("severity", "").lower() == sev]
        in_time = [v for v in sev_closed if (v["remediation_days"] or 0) <= SLA_DAYS[sev]]
        sla_by_sev[sev] = {
            "open": len(sev_open),
            "closed": len(sev_closed),
            "sla_breached_open": sum(1 for v in sev_open if v["sla_breached"]),
            "compliance_pct": round(len(in_time) / len(sev_closed) * 100, 2) if sev_closed else None,
        }

    # Remediation time stats
    rem_times = [v["remediation_days"] for v in closed_vulns if v["remediation_days"] is not None]

    # Top risk items
    top_risk = sorted(open_vulns, key=lambda v: v["risk_score"], reverse=True)[:10]

    return {
        "window_days": days,
        "total_vulns": len(vulns),
        "open_vulns": len(open_vulns),
        "closed_vulns": len(closed_vulns),
        "sla_breached_total": sum(1 for v in open_vulns if v["sla_breached"]),
        "sla_by_severity": sla_by_sev,
        "remediation_time_days": {
            "count": len(rem_times),
            "median": round(median(rem_times), 1) if rem_times else None,
        },
        "top_risk_open": [
            {"vuln_id": v["vuln_id"], "service": v["service"], "severity": v["severity"],
             "risk_score": v["risk_score"], "age_days": v["age_days"]}
            for v in top_risk
        ],
        "overall_risk": "critical" if sla_by_sev["critical"]["sla_breached_open"] > 0 else
                        "high" if sla_by_sev["high"]["sla_breached_open"] > 3 else "moderate",
    }


def main():
    parser = argparse.ArgumentParser(description="Vulnerability triage and SLA audit")
    parser.add_argument("--vulns", required=True, help="Vulnerabilities CSV file")
    parser.add_argument("--days", type=int, default=90, help="Look-back window in days")
    args = parser.parse_args()

    result = compute_triage(Path(args.vulns), args.days)
    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
