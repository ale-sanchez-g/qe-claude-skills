#!/usr/bin/env python3
"""
compute_dora.py — Compute DORA metrics from git history and a deployments CSV.

Usage:
    python compute_dora.py --repo /path/to/repo --deployments deploys.csv --days 30

Deployments CSV schema:
    deploy_id, commit_sha, deployed_at, environment, status, incident_id
    (status: success | rollback | incident)
    (incident_id: optional; comma-separated for multiple incidents in same deploy)

Output: JSON to stdout with all four DORA metrics + percentile breakdowns.
"""

import argparse
import csv
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import median, quantiles


def git_commit_time(repo: Path, sha: str) -> datetime | None:
    """Return the authored UTC datetime for a commit SHA."""
    try:
        ts = subprocess.check_output(
            ["git", "-C", str(repo), "show", "-s", "--format=%aI", sha],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        return datetime.fromisoformat(ts).astimezone(timezone.utc)
    except subprocess.CalledProcessError:
        return None


def parse_iso(s: str) -> datetime:
    return datetime.fromisoformat(s).astimezone(timezone.utc)


def compute_dora(repo: Path, deployments_csv: Path, days: int) -> dict:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    deploys: list[dict] = []
    with deployments_csv.open() as fh:
        for row in csv.DictReader(fh):
            deployed_at = parse_iso(row["deployed_at"])
            if deployed_at < cutoff:
                continue
            deploys.append({**row, "deployed_at": deployed_at})

    prod_deploys = [d for d in deploys if d.get("environment", "").lower() in ("production", "prod")]

    # ── Deployment Frequency ────────────────────────────────────────────────
    successful = [d for d in prod_deploys if d["status"] == "success"]
    deploy_freq_per_day = len(successful) / days if days else 0

    # ── Lead Time for Changes ───────────────────────────────────────────────
    lead_times: list[float] = []
    for d in successful:
        commit_time = git_commit_time(repo, d["commit_sha"])
        if commit_time:
            lead_times.append((d["deployed_at"] - commit_time).total_seconds() / 3600)

    def percentile_report(values: list[float]) -> dict:
        if not values:
            return {"count": 0, "median_h": None, "p75_h": None, "p95_h": None}
        qs = quantiles(values, n=100)
        return {
            "count": len(values),
            "median_h": round(median(values), 2),
            "p75_h": round(qs[74], 2),
            "p95_h": round(qs[94], 2),
        }

    # ── Change Failure Rate ─────────────────────────────────────────────────
    failed = [d for d in prod_deploys if d["status"] in ("rollback", "incident")]
    cfr = len(failed) / len(prod_deploys) if prod_deploys else 0

    # ── MTTR ────────────────────────────────────────────────────────────────
    # Expects incident records keyed by incident_id in separate file; approximate
    # from deploy rollback window if incident timestamps not available.
    mttr_hours: list[float] = []
    for d in failed:
        # Look for the next successful deploy after this failed one as recovery proxy
        deploy_time = d["deployed_at"]
        recoveries = [
            s["deployed_at"]
            for s in successful
            if s["deployed_at"] > deploy_time
        ]
        if recoveries:
            mttr_hours.append((min(recoveries) - deploy_time).total_seconds() / 3600)

    result = {
        "window_days": days,
        "total_prod_deploys": len(prod_deploys),
        "deployment_frequency_per_day": round(deploy_freq_per_day, 3),
        "lead_time_for_changes": percentile_report(lead_times),
        "change_failure_rate": round(cfr, 4),
        "mttr": percentile_report(mttr_hours),
        "dora_band": _classify(deploy_freq_per_day, cfr, lead_times, mttr_hours),
    }
    return result


def _classify(freq: float, cfr: float, lead_times: list[float], mttr: list[float]) -> str:
    """Map metrics to DORA performance band (elite/high/medium/low)."""
    lt_med = median(lead_times) if lead_times else None
    mttr_med = median(mttr) if mttr else None

    if freq >= 1 and cfr <= 0.05 and (lt_med is not None and lt_med < 24) and (mttr_med is not None and mttr_med < 1):
        return "elite"
    if freq >= 1 / 7 and cfr <= 0.10 and (lt_med is not None and lt_med < 168):
        return "high"
    if freq >= 1 / 30 and cfr <= 0.15:
        return "medium"
    return "low"


def main():
    parser = argparse.ArgumentParser(description="Compute DORA metrics")
    parser.add_argument("--repo", default=".", help="Path to git repository")
    parser.add_argument("--deployments", required=True, help="Deployments CSV file")
    parser.add_argument("--days", type=int, default=30, help="Look-back window in days")
    args = parser.parse_args()

    result = compute_dora(Path(args.repo), Path(args.deployments), args.days)
    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
