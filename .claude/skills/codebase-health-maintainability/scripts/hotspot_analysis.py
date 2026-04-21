#!/usr/bin/env python3
"""
hotspot_analysis.py — Identify codebase hotspots by combining git churn with
static complexity proxies (line count as weight when real analysis unavailable).

Usage:
    python hotspot_analysis.py --repo /path/to/repo --days 90 [--top 20]

Output: JSON hotspot table + technical debt summary.
"""

import argparse
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


def git_churn(repo: Path, days: int) -> dict[str, int]:
    """Count net file-level changes over look-back period."""
    log = subprocess.check_output(
        [
            "git", "-C", str(repo), "log",
            f"--since={days} days ago",
            "--name-only",
            "--format=",
        ],
        text=True,
        stderr=subprocess.DEVNULL,
    )
    counts: dict[str, int] = defaultdict(int)
    for line in log.splitlines():
        line = line.strip()
        if line:
            counts[line] += 1
    return dict(counts)


def line_count(path: Path) -> int:
    try:
        return sum(1 for _ in path.open("rb"))
    except OSError:
        return 0


def complexity_proxy(file_path: Path) -> int:
    """
    Rough structural complexity proxy via keyword density.
    Replace with radon/lizard output for production use.
    """
    keywords = {b"if ", b"elif ", b"else:", b"for ", b"while ", b"except ", b"match "}
    try:
        content = file_path.read_bytes()
        return sum(content.count(kw) for kw in keywords)
    except OSError:
        return 0


def score_file(churn: int, loc: int, complexity: int, max_churn: int, max_loc: int, max_cc: int) -> float:
    """Normalised hotspot score in [0, 1]. Higher = more risk."""
    norm_c = churn / max_churn if max_churn else 0
    norm_l = loc / max_loc if max_loc else 0
    norm_cc = complexity / max_cc if max_cc else 0
    return round((norm_c * 0.5) + (norm_cc * 0.35) + (norm_l * 0.15), 4)


def compute_hotspots(repo: Path, days: int, top_n: int) -> dict:
    churn = git_churn(repo, days)
    if not churn:
        return {"error": "No churn data found – check --repo path and --days window"}

    # Gather metrics for every churned file
    files = []
    for rel_path, ch in churn.items():
        abs_path = repo / rel_path
        loc = line_count(abs_path)
        cc = complexity_proxy(abs_path)
        files.append({"path": rel_path, "churn": ch, "loc": loc, "complexity_proxy": cc})

    max_churn = max(f["churn"] for f in files) or 1
    max_loc = max(f["loc"] for f in files) or 1
    max_cc = max(f["complexity_proxy"] for f in files) or 1

    for f in files:
        f["hotspot_score"] = score_file(f["churn"], f["loc"], f["complexity_proxy"], max_churn, max_loc, max_cc)

    hotspots = sorted(files, key=lambda x: x["hotspot_score"], reverse=True)[:top_n]

    total_files = len(files)
    high_risk = [f for f in files if f["hotspot_score"] > 0.65]

    return {
        "window_days": days,
        "files_analysed": total_files,
        "high_risk_file_count": len(high_risk),
        "high_risk_pct": round(len(high_risk) / total_files * 100, 2) if total_files else 0,
        "hotspots": hotspots,
        "debt_signal": "critical" if len(high_risk) / total_files > 0.10 else "moderate" if len(high_risk) / total_files > 0.05 else "low",
    }


def main():
    parser = argparse.ArgumentParser(description="Codebase hotspot analysis")
    parser.add_argument("--repo", default=".", help="Path to git repository")
    parser.add_argument("--days", type=int, default=90, help="Churn look-back window in days")
    parser.add_argument("--top", type=int, default=20, help="Number of top hotspots to return")
    args = parser.parse_args()

    result = compute_hotspots(Path(args.repo), args.days, args.top)
    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
