#!/usr/bin/env python3
"""
Validate skills against the Agent Skills Standard.
Usage:
    python tools/validate-skills.py [optional_path_to_skill_or_dir]
"""

import argparse
import json
import os
import re
import sys

KEBAB_CASE_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


def parse_frontmatter(content: str) -> dict:
    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        return {}
    raw_yaml = match.group(1)
    metadata = {}
    current_key = None

    for line in raw_yaml.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            current_key = key.strip()
            val = val.strip().strip("'\"")
            if val == ">-" or val == ">" or val == "|":
                metadata[current_key] = ""
            else:
                metadata[current_key] = val
        elif current_key and line:
            if metadata[current_key]:
                metadata[current_key] += " " + line.strip()
            else:
                metadata[current_key] = line.strip()

    return metadata


def validate_skill_dir(skill_path: str) -> tuple[bool, list[str]]:
    errors = []
    skill_name = os.path.basename(os.path.normpath(skill_path))

    # 1. Folder naming rule: lowercase, kebab-case
    if not KEBAB_CASE_PATTERN.match(skill_name):
        errors.append(f"Directory '{skill_name}' violates kebab-case naming (must be lowercase alphanumeric + hyphens).")

    # 2. SKILL.md check
    skill_md = os.path.join(skill_path, "SKILL.md")
    if not os.path.isfile(skill_md):
        errors.append(f"Missing required entry point: SKILL.md")
    else:
        try:
            with open(skill_md, "r", encoding="utf-8") as f:
                content = f.read()

            if not content.startswith("---"):
                errors.append("SKILL.md must start with YAML frontmatter delimiter '---'.")
            else:
                metadata = parse_frontmatter(content)
                if not metadata.get("name"):
                    errors.append("SKILL.md frontmatter missing required 'name' field.")
                elif metadata.get("name") != skill_name:
                    errors.append(f"Frontmatter name '{metadata.get('name')}' does not match directory name '{skill_name}'.")

                if not metadata.get("description"):
                    errors.append("SKILL.md frontmatter missing required 'description' field.")
        except Exception as e:
            errors.append(f"Failed to read or parse SKILL.md: {e}")

    # 3. evals.json check (if present)
    evals_json = os.path.join(skill_path, "evals.json")
    if os.path.isfile(evals_json):
        try:
            with open(evals_json, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                errors.append("evals.json must be a JSON array of evaluation cases.")
        except Exception as e:
            errors.append(f"Invalid JSON in evals.json: {e}")

    is_valid = len(errors) == 0
    return is_valid, errors


def main():
    parser = argparse.ArgumentParser(description="Validate skills against Agent Skills Standard.")
    parser.add_argument(
        "target",
        nargs="?",
        default="skills",
        help="Path to a specific skill folder or the skills root directory (default: 'skills')",
    )
    args = parser.parse_args()

    target_path = os.path.abspath(args.target)
    if not os.path.exists(target_path):
        print(f"[ERROR] Path does not exist: {target_path}")
        return 1

    # Determine if validating a single skill or multiple
    skills_to_validate = []
    if os.path.isfile(os.path.join(target_path, "SKILL.md")):
        skills_to_validate.append(target_path)
    else:
        for entry in os.scandir(target_path):
            if entry.is_dir() and not entry.name.startswith("."):
                skills_to_validate.append(entry.path)

    if not skills_to_validate:
        print(f"No skills found in {target_path} to validate.")
        return 0

    print(f"Validating {len(skills_to_validate)} skill(s) against Agent Skills Standard...\n")
    all_passed = True

    for skill in skills_to_validate:
        name = os.path.basename(skill)
        is_valid, errors = validate_skill_dir(skill)
        if is_valid:
            print(f"  [PASS] {name}")
        else:
            all_passed = False
            print(f"  [FAIL] {name}")
            for err in errors:
                print(f"         - {err}")

    print("\n" + ("=" * 40))
    if all_passed:
        print("ALL SKILLS VALIDATED SUCCESSFULLY.")
        return 0
    else:
        print("VALIDATION FAILED WITH ERRORS.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
