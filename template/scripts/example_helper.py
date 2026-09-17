#!/usr/bin/env python3
"""
Example helper script for the template skill.
Agents can invoke helper scripts in scripts/ during execution.
"""

import argparse
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        description="Template helper script demonstrating automation capabilities."
    )
    parser.add_argument(
        "--input",
        type=str,
        help="Path to an input file or parameter string",
        default="",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run without side-effects",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    print(f"[helper] Running template script with input: '{args.input}'")
    if args.dry_run:
        print("[helper] Dry run enabled. No modifications made.")
        return 0

    # Perform intended task here
    print("[helper] Task completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
