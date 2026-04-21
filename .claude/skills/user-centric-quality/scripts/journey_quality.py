#!/usr/bin/env python3
"""
journey_quality.py — Measure user journey success rates, failed completion rates,
and adoption signals from analytics event data.

Usage:
    python journey_quality.py --events events.csv --days 30 [--journeys "signup,checkout"]

Events CSV schema:
    event_id, user_id, journey, step, status, timestamp, segment, release_cohort
    (status: success | failure | abandoned)

Output: JSON with journey success rates, segment breakdowns, and quality signals.
"""

import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import median


def parse_iso(s: str) -> datetime | None:
    try:
        return datetime.fromisoformat(s).astimezone(timezone.utc)
    except (ValueError, AttributeError):
        return None


def compute_journey_quality(events_csv: Path, days: int, target_journeys: list[str]) -> dict:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    events: list[dict] = []
    with events_csv.open() as fh:
        for row in csv.DictReader(fh):
            ts = parse_iso(row.get("timestamp", ""))
            if not ts or ts < cutoff:
                continue
            journey = row.get("journey", "")
            if target_journeys and journey not in target_journeys:
                continue
            events.append({**row, "timestamp": ts})

    journeys: dict[str, dict] = defaultdict(
        lambda: {"total": 0, "success": 0, "failure": 0, "abandoned": 0, "by_segment": defaultdict(lambda: {"total": 0, "success": 0}), "by_cohort": defaultdict(lambda: {"total": 0, "success": 0})}
    )

    for e in events:
        j = e["journey"]
        status = e.get("status", "")
        segment = e.get("segment", "all")
        cohort = e.get("release_cohort", "unknown")

        journeys[j]["total"] += 1
        if status == "success":
            journeys[j]["success"] += 1
        elif status == "failure":
            journeys[j]["failure"] += 1
        elif status == "abandoned":
            journeys[j]["abandoned"] += 1

        journeys[j]["by_segment"][segment]["total"] += 1
        if status == "success":
            journeys[j]["by_segment"][segment]["success"] += 1

        journeys[j]["by_cohort"][cohort]["total"] += 1
        if status == "success":
            journeys[j]["by_cohort"][cohort]["success"] += 1

    result: dict = {"window_days": days, "journeys": {}}
    all_success_rates = []

    for jname, data in journeys.items():
        total = data["total"]
        success_rate = data["success"] / total if total else 0
        fail_rate = data["failure"] / total if total else 0
        abandon_rate = data["abandoned"] / total if total else 0
        all_success_rates.append(success_rate)

        segment_breakdown = {
            seg: {
                "total": sv["total"],
                "success_rate": round(sv["success"] / sv["total"], 4) if sv["total"] else 0,
            }
            for seg, sv in data["by_segment"].items()
        }

        cohort_breakdown = {
            cohort: {
                "total": cv["total"],
                "success_rate": round(cv["success"] / cv["total"], 4) if cv["total"] else 0,
            }
            for cohort, cv in data["by_cohort"].items()
        }

        result["journeys"][jname] = {
            "total_attempts": total,
            "success_rate": round(success_rate, 4),
            "failure_rate": round(fail_rate, 4),
            "abandonment_rate": round(abandon_rate, 4),
            "quality_signal": "healthy" if success_rate > 0.95 else "at_risk" if success_rate > 0.85 else "critical",
            "by_segment": segment_breakdown,
            "by_release_cohort": cohort_breakdown,
        }

    result["overall_avg_success_rate"] = round(sum(all_success_rates) / len(all_success_rates), 4) if all_success_rates else None
    return result


def main():
    parser = argparse.ArgumentParser(description="User journey quality analysis")
    parser.add_argument("--events", required=True, help="Analytics events CSV file")
    parser.add_argument("--days", type=int, default=30, help="Look-back window in days")
    parser.add_argument("--journeys", default="", help="Comma-separated journey names to include (all if empty)")
    args = parser.parse_args()

    target = [j.strip() for j in args.journeys.split(",") if j.strip()]
    result = compute_journey_quality(Path(args.events), args.days, target)
    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
