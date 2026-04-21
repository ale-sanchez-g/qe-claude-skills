#!/usr/bin/env python3
"""
pr_analytics.py — Measure PR cycle time, review latency, rework rate, and WIP
from a pull-requests CSV export.

Usage:
    python pr_analytics.py --prs prs.csv --days 30

Pull Requests CSV schema:
    pr_id, title, repo, author, opened_at, first_review_at, approved_at,
    merged_at, lines_added, lines_deleted, iteration_count, status, reopened
    (status: merged | closed | open)
    (reopened: true | false)

Output: JSON with cycle time, review latency, PR size distribution, rework rate,
        and current WIP count.
"""

import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import median, quantiles


def parse_iso(s: str) -> datetime | None:
    try:
        return datetime.fromisoformat(s).astimezone(timezone.utc)
    except (ValueError, AttributeError):
        return None


def hours_between(start: datetime | None, end: datetime | None) -> float | None:
    if start and end and end > start:
        return (end - start).total_seconds() / 3600
    return None


def size_bucket(lines: int) -> str:
    if lines < 50:
        return "xs"
    if lines < 200:
        return "small"
    if lines < 500:
        return "medium"
    if lines < 1000:
        return "large"
    return "xl"


def pct_report(values: list[float]) -> dict:
    if not values:
        return {"count": 0, "median_h": None, "p75_h": None, "p95_h": None}
    qs = quantiles(values, n=100)
    return {
        "count": len(values),
        "median_h": round(median(values), 2),
        "p75_h": round(qs[74], 2),
        "p95_h": round(qs[94], 2),
    }


def compute_pr_analytics(prs_csv: Path, days: int) -> dict:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    prs: list[dict] = []
    with prs_csv.open() as fh:
        for row in csv.DictReader(fh):
            opened = parse_iso(row.get("opened_at", ""))
            if not opened or opened < cutoff:
                continue
            merged = parse_iso(row.get("merged_at", ""))
            first_review = parse_iso(row.get("first_review_at", ""))
            approved = parse_iso(row.get("approved_at", ""))
            try:
                lines = int(row.get("lines_added", 0)) + int(row.get("lines_deleted", 0))
            except ValueError:
                lines = 0
            prs.append({
                **row,
                "opened_at": opened,
                "merged_at": merged,
                "first_review_at": first_review,
                "approved_at": approved,
                "lines_changed": lines,
            })

    merged = [p for p in prs if p["status"] == "merged"]
    open_prs = [p for p in prs if p["status"] == "open"]

    # Cycle time
    cycle_times = [hours_between(p["opened_at"], p["merged_at"]) for p in merged]
    cycle_times = [c for c in cycle_times if c is not None]

    # First review latency
    review_latencies = [hours_between(p["opened_at"], p["first_review_at"]) for p in merged]
    review_latencies = [r for r in review_latencies if r is not None]

    # PR size distribution
    size_dist: dict[str, int] = defaultdict(int)
    for p in prs:
        size_dist[size_bucket(p["lines_changed"])] += 1

    # Rework signal: iteration_count > 2 or reopened
    rework_prs = [p for p in merged if int(p.get("iteration_count", 1) or 1) > 2 or p.get("reopened", "").lower() == "true"]
    rework_rate = len(rework_prs) / len(merged) if merged else 0

    # WIP
    wip = len(open_prs)

    # By author (for skew detection)
    authors: dict[str, list[float]] = defaultdict(list)
    for p in merged:
        ct = hours_between(p["opened_at"], p["merged_at"])
        if ct:
            authors[p.get("author", "unknown")].append(ct)
    top_slow = sorted(
        [(a, round(median(ts), 2)) for a, ts in authors.items() if ts],
        key=lambda x: x[1],
        reverse=True,
    )[:5]

    return {
        "window_days": days,
        "total_prs": len(prs),
        "merged_prs": len(merged),
        "open_prs_wip": wip,
        "cycle_time": pct_report(cycle_times),
        "first_review_latency": pct_report(review_latencies),
        "pr_size_distribution": dict(size_dist),
        "rework_rate": round(rework_rate, 4),
        "rework_pct": round(rework_rate * 100, 2),
        "top5_authors_by_cycle_time": [{"author": a, "median_cycle_h": t} for a, t in top_slow],
        "flow_signal": "critical" if wip > 30 or rework_rate > 0.3 else "at_risk" if wip > 15 or rework_rate > 0.15 else "healthy",
    }


def main():
    parser = argparse.ArgumentParser(description="PR analytics and workflow efficiency")
    parser.add_argument("--prs", required=True, help="Pull requests CSV file")
    parser.add_argument("--days", type=int, default=30, help="Look-back window in days")
    args = parser.parse_args()

    result = compute_pr_analytics(Path(args.prs), args.days)
    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
