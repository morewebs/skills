#!/usr/bin/env python3
"""
Sync / Link skills from this repository to AI agent runtime directories.
Supports Windows (directory junctions / copy) and Unix (symlinks / copy).

Usage:
    python tools/sync-skills.py --target [antigravity|claude|cursor|custom] [--dest <path>] [--copy]
"""

import argparse
import os
import shutil
import subprocess
import sys

PLATFORM = sys.platform


def get_default_target_dir(agent_name: str) -> str:
    home = os.path.expanduser("~")
    targets = {
        "antigravity": os.path.join(home, ".gemini", "config", "skills"),
        "gemini": os.path.join(home, ".gemini", "config", "skills"),
        "claude": os.path.join(home, ".claude", "skills"),
        "cursor": os.path.join(home, ".cursor", "skills"),
    }
    return targets.get(agent_name.lower())


def link_or_copy_dir(src: str, dest: str, force_copy: bool = False):
    os.makedirs(os.path.dirname(dest), exist_ok=True)

    if os.path.exists(dest):
        print(f"  [EXISTS] {dest} already exists. Skipping.")
        return

    if force_copy:
        print(f"  [COPY] Copying {os.path.basename(src)} -> {dest}")
        shutil.copytree(src, dest)
        return

    # Try symlink or Windows directory junction
    try:
        if PLATFORM == "win32":
            # On Windows without developer mode, symlinks require admin, but mklink /J (junctions) do not
            cmd = f'cmd /c mklink /J "{dest}" "{src}"'
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if res.returncode == 0:
                print(f"  [JUNCTION] Linked {os.path.basename(src)} -> {dest}")
                return
            else:
                # Fallback to copy
                print(f"  [FALLBACK-COPY] Junction failed, copying {os.path.basename(src)} -> {dest}")
                shutil.copytree(src, dest)
        else:
            os.symlink(src, dest, target_is_directory=True)
            print(f"  [SYMLINK] Linked {os.path.basename(src)} -> {dest}")
    except Exception as e:
        print(f"  [FALLBACK-COPY] Link failed ({e}), falling back to copy.")
        shutil.copytree(src, dest)


def sync_skills(target_agent: str, custom_dest: str = None, force_copy: bool = False):
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    skills_dir = os.path.join(repo_root, "skills")

    dest_dir = custom_dest if custom_dest else get_default_target_dir(target_agent)
    if not dest_dir:
        print(f"[ERROR] Unknown agent '{target_agent}'. Specify --dest <path> for custom targets.")
        return 1

    print(f"Syncing skills to target destination:")
    print(f"  Destination: {dest_dir}")
    print(f"  Mode: {'Copy' if force_copy else 'Symlink / Junction'}\n")

    os.makedirs(dest_dir, exist_ok=True)

    count = 0
    for entry in os.scandir(skills_dir):
        if entry.is_dir() and not entry.name.startswith("."):
            skill_name = entry.name
            skill_src = entry.path
            skill_dest = os.path.join(dest_dir, skill_name)
            link_or_copy_dir(skill_src, skill_dest, force_copy=force_copy)
            count += 1

    print(f"\nSynced {count} skill(s) successfully.")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Sync skills into agent runtime directories.")
    parser.add_argument(
        "--target",
        "-t",
        default="antigravity",
        choices=["antigravity", "gemini", "claude", "cursor", "custom"],
        help="Target agent runtime (default: 'antigravity')",
    )
    parser.add_argument(
        "--dest",
        "-d",
        default=None,
        help="Custom destination directory (overrides default agent paths)",
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Always copy files instead of creating directory links/junctions",
    )
    args = parser.parse_args()
    return sync_skills(args.target, args.dest, args.copy)


if __name__ == "__main__":
    sys.exit(main())
