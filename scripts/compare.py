"""Compare two Trivy JSON reports: python compare.py before.json after.json"""
import json
import sys
from collections import Counter

SEVERITIES = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "UNKNOWN"]


def summarize(path):
    with open(path, encoding="utf-8-sig") as f:
        data = json.load(f)
    vulns, secrets = [], 0
    for result in data.get("Results", []):
        vulns += result.get("Vulnerabilities") or []
        secrets += len(result.get("Secrets") or [])
    return {
        "total": len(vulns),
        "unique_cves": len({v["VulnerabilityID"] for v in vulns}),
        "severity": Counter(v["Severity"] for v in vulns),
        "no_fix": sum(1 for v in vulns if not v.get("FixedVersion")),
        "secrets": secrets,
    }


before, after = summarize(sys.argv[1]), summarize(sys.argv[2])
print(f"{'':<14}{'BEFORE':>8}{'AFTER':>8}")
for key in ["total", "unique_cves", "no_fix", "secrets"]:
    print(f"{key:<14}{before[key]:>8}{after[key]:>8}")
for sev in SEVERITIES:
    print(f"{sev:<14}{before['severity'][sev]:>8}{after['severity'][sev]:>8}")