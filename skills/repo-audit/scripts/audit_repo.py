#!/usr/bin/env python3
"""
Repository Health & Readiness Auditor
Usage: python audit_repo.py [--target <path>] [--json]
"""

import argparse
import json
import os
import subprocess
import sys


def parse_args():
    parser = argparse.ArgumentParser(description="Audit repository health and structure.")
    parser.add_argument(
        "--target",
        type=str,
        default=".",
        help="Path to the repository root to inspect (default: current directory)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output audit findings in JSON format",
    )
    return parser.parse_args()


def audit_repository(target_path: str) -> dict:
    target = os.path.abspath(target_path)
    report = {
        "repository_path": target,
        "checks": {},
        "overall_status": "PASS",
    }

    # 1. Check for README
    readme_candidates = ["README.md", "README.txt", "readme.md", "README"]
    has_readme = any(os.path.isfile(os.path.join(target, f)) for f in readme_candidates)
    report["checks"]["readme"] = {
        "passed": has_readme,
        "detail": "README file exists" if has_readme else "Missing README.md",
    }

    # 2. Check for .gitignore
    has_gitignore = os.path.isfile(os.path.join(target, ".gitignore"))
    report["checks"]["gitignore"] = {
        "passed": has_gitignore,
        "detail": ".gitignore exists" if has_gitignore else "Missing .gitignore",
    }

    # 3. Check for LICENSE
    license_candidates = ["LICENSE", "LICENSE.md", "LICENSE.txt", "license"]
    has_license = any(os.path.isfile(os.path.join(target, f)) for f in license_candidates)
    report["checks"]["license"] = {
        "passed": has_license,
        "detail": "LICENSE file exists" if has_license else "Missing LICENSE file",
    }

    # 4. Check Git status
    is_git_repo = os.path.isdir(os.path.join(target, ".git"))
    if is_git_repo:
        try:
            res = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=target,
                capture_output=True,
                text=True,
                check=False,
            )
            uncommitted = [line.strip() for line in res.stdout.strip().splitlines() if line.strip()]
            report["checks"]["git_clean"] = {
                "passed": len(uncommitted) == 0,
                "detail": f"{len(uncommitted)} uncommitted changes found" if uncommitted else "Working tree clean",
                "uncommitted_count": len(uncommitted),
            }
        except Exception as e:
            report["checks"]["git_clean"] = {"passed": False, "detail": f"Git command failed: {e}"}
    else:
        report["checks"]["git_clean"] = {"passed": False, "detail": "Not a git repository"}

    # Overall Status Calculation
    failed_checks = [k for k, v in report["checks"].items() if not v["passed"]]
    if failed_checks:
        report["overall_status"] = "WARN" if len(failed_checks) <= 2 else "FAIL"
        report["failed_checks"] = failed_checks
    else:
        report["overall_status"] = "PASS"
        report["failed_checks"] = []

    return report


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    args = parse_args()
    results = audit_repository(args.target)

    if args.json:
        print(json.dumps(results, indent=2))
        return 0

    print(f"=== Repository Audit: {results['repository_path']} ===")
    print(f"Overall Status: {results['overall_status']}\n")
    for check_name, check_data in results["checks"].items():
        status_tag = "OK" if check_data["passed"] else "MISSING"
        print(f"[{status_tag}] {check_name.upper()}: {check_data['detail']}")

    return 0 if results["overall_status"] != "FAIL" else 1


if __name__ == "__main__":
    sys.exit(main())
