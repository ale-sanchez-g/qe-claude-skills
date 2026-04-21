#!/usr/bin/env python3
"""
alert_quality_audit.py — Score alert quality and on-call load from alert log CSV.

Usage:
    python alert_quality_audit.py --alerts alerts.csv --days 30

Alert CSV schema:
    alert_id, name, service, fired_at, resolved_at, actionable, paged_engineer, severity
    (actionable: true | false)

Output: JSON with noise ratio, on-call load, TTD metrics, and top noisy alert classes.
"""

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import median


def parse_iso(s: str) -> datetime | None:
    try:
        return datetime.fromisoformat(s).astimezone(timezone.utc)
    except (ValueError, AttributeError):
        return None


def compute_alert_quality(alerts_csv: Path, days: int) -> dict:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    alerts: list[dict] = []
    with alerts_csv.open() as fh:
        for row in csv.DictReader(fh):
            fired_at = parse_iso(row.get("fired_at", ""))
            if not fired_at or fired_at < cutoff:
                continue
            resolved_at = parse_iso(row.get("resolved_at", "")) 
            duration_min = (
                (resolved_at - fired_at).total_seconds() / 60 if resolved_at else None
            )
            alerts.append({
                **row,
                "fired_at": fired_at,
                "resolved_at": resolved_at,
                "duration_min": duration_min,
                "actionable": row.get("actionable", "false").lower() == "true",
            })

    total = len(alerts)
    actionable = [a for a in alerts if a["actionable"]]
    noise_ratio = (total - len(actionable)) / total if total else 0

    # On-call load: pages per engineer
    pages_by_eng: Counter[str] = Counter()
    for a in alerts:
        eng = a.get("paged_engineer", "")
        if eng:
            pages_by_eng[eng] += 1

    page_counts = list(pages_by_eng.values())
    on_call_load = {
        "engineers": len(pages_by_eng),
        "total_pages": sum(page_counts),
        "median_pages_per_eng": round(median(page_counts), 1) if page_counts else 0,
        "max_pages": max(page_counts) if page_counts else 0,
    }

    # Alert duration stats (proxy for TTD when explicit timestamp missing)
    durations = [a["duration_min"] for a in alerts if a["duration_min"] is not None]
    ttd_stats = {
        "median_min": round(median(durations), 1) if durations else None,
    }

    # Top noisy alert classes
    noisy = [a for a in alerts if not a["actionable"]]
    top_noisy = Counter(a["name"] for a in noisy).most_common(10)

    # Severity distribution
    sev_dist = dict(Counter(a.get("severity", "unknown") for a in alerts))

    return {
        "window_days": days,
        "total_alerts": total,
        "actionable_alerts": len(actionable),
        "noise_ratio": round(noise_ratio, 4),
        "noise_pct": round(noise_ratio * 100, 2),
        "on_call_load": on_call_load,
        "ttd_proxy_stats": ttd_stats,
        "top_noisy_alerts": [{"name": n, "count": c} for n, c in top_noisy],
        "severity_distribution": sev_dist,
        "quality_signal": "critical" if noise_ratio > 0.5 else "at_risk" if noise_ratio > 0.3 else "healthy",
    }


def main():
    parser = argparse.ArgumentParser(description="Alert quality and on-call load audit")
    parser.add_argument("--alerts", required=True, help="Alerts CSV file")
    parser.add_argument("--days", type=int, default=30, help="Look-back window in days")
    args = parser.parse_args()

    result = compute_alert_quality(Path(args.alerts), args.days)
    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
