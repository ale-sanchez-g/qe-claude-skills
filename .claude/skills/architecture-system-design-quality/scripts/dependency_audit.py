#!/usr/bin/env python3
"""
dependency_audit.py — Audit service dependency density and blast radius from a
service topology JSON file.

Usage:
    python dependency_audit.py --topology topology.json [--critical-path "svc-a,svc-b"]

Topology JSON schema:
    {
      "services": [
        {
          "name": "payment-service",
          "depends_on": ["order-service", "user-service"],
          "resilience": {"timeout": true, "retry": true, "circuit_breaker": false}
        }
      ]
    }

Output: JSON with coupling metrics, blast radius estimates, and resilience gaps.
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path


def build_graphs(services: list[dict]) -> tuple[dict, dict]:
    """Return outgoing and incoming dependency dicts."""
    outgoing: dict[str, set] = defaultdict(set)
    incoming: dict[str, set] = defaultdict(set)
    for svc in services:
        name = svc["name"]
        for dep in svc.get("depends_on", []):
            outgoing[name].add(dep)
            incoming[dep].add(name)
    return dict(outgoing), dict(incoming)


def blast_radius(service: str, outgoing: dict, depth: int = 3) -> set:
    """BFS downstream impact (services that depend on `service`)."""
    visited: set[str] = set()
    # Build reverse map
    reverse: dict[str, set] = defaultdict(set)
    for src, targets in outgoing.items():
        for t in targets:
            reverse[t].add(src)

    queue = list(reverse.get(service, []))
    while queue and depth > 0:
        next_q = []
        for s in queue:
            if s not in visited:
                visited.add(s)
                next_q.extend(reverse.get(s, []))
        queue = next_q
        depth -= 1
    return visited


def compute_audit(topology_path: Path, critical_path: list[str]) -> dict:
    data = json.loads(topology_path.read_text())
    services = data["services"]
    names = [s["name"] for s in services]
    svc_index = {s["name"]: s for s in services}

    outgoing, incoming = build_graphs(services)

    total = len(names)
    coupling_stats: list[dict] = []

    resilience_gaps: list[dict] = []

    for name in names:
        out_deg = len(outgoing.get(name, set()))
        in_deg = len(incoming.get(name, set()))
        br = blast_radius(name, outgoing)
        svc_data = svc_index[name]
        res = svc_data.get("resilience", {})
        missing = [k for k in ("timeout", "retry", "circuit_breaker") if not res.get(k)]

        coupling_stats.append({
            "service": name,
            "outgoing_deps": out_deg,
            "incoming_deps": in_deg,
            "blast_radius": len(br),
            "blast_radius_services": sorted(br),
        })

        if missing:
            resilience_gaps.append({"service": name, "missing_patterns": missing})

    avg_out = sum(s["outgoing_deps"] for s in coupling_stats) / total if total else 0
    avg_in = sum(s["incoming_deps"] for s in coupling_stats) / total if total else 0
    avg_br = sum(s["blast_radius"] for s in coupling_stats) / total if total else 0

    high_coupling = [s for s in coupling_stats if s["outgoing_deps"] + s["incoming_deps"] > (avg_out + avg_in) * 1.5]
    high_blast = sorted(coupling_stats, key=lambda x: x["blast_radius"], reverse=True)[:5]

    critical_analysis = {}
    for svc in critical_path:
        if svc in svc_index:
            critical_analysis[svc] = {
                "blast_radius": blast_radius(svc, outgoing),
                "resilience_gaps": [g for g in resilience_gaps if g["service"] == svc],
            }

    return {
        "total_services": total,
        "avg_outgoing_deps": round(avg_out, 2),
        "avg_incoming_deps": round(avg_in, 2),
        "avg_blast_radius": round(avg_br, 2),
        "high_coupling_services": high_coupling,
        "highest_blast_radius_top5": high_blast,
        "resilience_gaps": resilience_gaps,
        "resilience_coverage_pct": round((total - len(resilience_gaps)) / total * 100, 2) if total else 0,
        "critical_path_analysis": critical_analysis,
    }


def main():
    parser = argparse.ArgumentParser(description="Service dependency and blast radius audit")
    parser.add_argument("--topology", required=True, help="Topology JSON file")
    parser.add_argument("--critical-path", default="", help="Comma-separated critical service names")
    args = parser.parse_args()

    critical = [s.strip() for s in args.critical_path.split(",") if s.strip()]
    result = compute_audit(Path(args.topology), critical)
    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
