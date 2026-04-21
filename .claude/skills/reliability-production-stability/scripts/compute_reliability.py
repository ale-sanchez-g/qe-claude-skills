#!/usr/bin/env python3
"""
compute_reliability.py — Compute reliability and SLO metrics from time-series data.

Usage:
    python compute_reliability.py --events events.csv --days 30

Events CSV schema:
    timestamp, service, event_type, duration_seconds, severity
    (event_type: outage | degradation | ok)
    (severity: sev1 | sev2 | sev3 | none)

Output: JSON to stdout with availability, MTBF, incident rate, and latency summary.
"""

import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import median, quantiles


def parse_iso(s: str) -> datetime:
    return datetime.fromisoformat(s).astimezone(timezone.utc)


def compute_reliability(events_csv: Path, days: int) -> dict:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    window_seconds = days * 86400

    events: list[dict] = []
    with events_csv.open() as fh:
        for row in csv.DictReader(fh):
            ts = parse_iso(row["timestamp"])
            if ts >= cutoff:
                events.append({**row, "timestamp": ts})

    services: dict[str, dict] = defaultdict(
        lambda: {"outage_seconds": 0.0, "incidents": [], "durations": []}
    )

    for e in events:
        svc = e["service"]
        etype = e["event_type"]
        dur = float(e.get("duration_seconds", 0) or 0)
        sev = e.get("severity", "none")

        if etype in ("outage", "degradation"):
            services[svc]["outage_seconds"] += dur
            services[svc]["incidents"].append({"severity": sev, "duration_s": dur})

    result: dict = {"window_days": days, "services": {}}
    sev_counts: dict[str, int] = defaultdict(int)

    for svc, data in services.items():
        uptime_s = window_seconds - data["outage_seconds"]
        availability = uptime_s / window_seconds if window_seconds else 0
        n_incidents = len(data["incidents"])
        mtbf_h = (uptime_s / 3600) / n_incidents if n_incidents else None
        durations_h = [i["duration_s"] / 3600 for i in data["incidents"]]

        for inc in data["incidents"]:
            sev_counts[inc["severity"]] += 1

        result["services"][svc] = {
            "availability_pct": round(availability * 100, 4),
            "downtime_minutes": round(data["outage_seconds"] / 60, 2),
            "incident_count": n_incidents,
            "mtbf_hours": round(mtbf_h, 2) if mtbf_h else None,
            "incident_duration": _duration_stats(durations_h),
            "slo_status": "at_risk" if availability < 0.999 else "healthy",
        }

    result["severity_distribution"] = dict(sev_counts)
    result["error_budget_remaining_pct"] = _error_budget(result["services"])
    return result


def _duration_stats(hours: list[float]) -> dict:
    if not hours:
        return {"count": 0, "median_h": None, "p90_h": None}
    qs = quantiles(hours, n=100)
    return {
        "count": len(hours),
        "median_h": round(median(hours), 2),
        "p90_h": round(qs[89], 2),
    }


def _error_budget(services: dict) -> float | None:
    """Return average remaining error budget across services using 99.9% SLO."""
    target = 99.9
    remaining = [
        max(0, (s["availability_pct"] - target) / (100 - target) * 100)
        for s in services.values()
    ]
    return round(sum(remaining) / len(remaining), 2) if remaining else None


def main():
    parser = argparse.ArgumentParser(description="Compute reliability metrics")
    parser.add_argument("--events", required=True, help="Events CSV file")
    parser.add_argument("--days", type=int, default=30, help="Look-back window in days")
    args = parser.parse_args()

    result = compute_reliability(Path(args.events), args.days)
    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
