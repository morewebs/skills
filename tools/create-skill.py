#!/usr/bin/env python3
"""
Create a new agent skill adhering to the Agent Skills Standard.
Usage:
    python tools/create-skill.py <skill-name> [--description "Description here"]
"""

import argparse
import os
import re
import shutil
import sys

KEBAB_CASE_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def validate_skill_name(name: str) -> bool:
    return bool(KEBAB_CASE_PATTERN.match(name))


def create_skill(name: str, description: str = "") -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    template_dir = os.path.join(repo_root, "template")
    target_dir = os.path.join(repo_root, "skills", name)

    if not validate_skill_name(name):
        print(f"[ERROR] Invalid skill name: '{name}'.")
        print("Skill names must be lowercase kebab-case (e.g. 'frontend-design', 'summarize-docs').")
        return 1

    if os.path.exists(target_dir):
        print(f"[ERROR] Skill directory already exists: '{target_dir}'.")
        return 1

    if not os.path.isdir(template_dir):
        print(f"[ERROR] Template directory not found at: '{template_dir}'.")
        return 1

    print(f"Creating new skill '{name}' from template...")
    shutil.copytree(template_dir, target_dir)

    # Customize SKILL.md
    skill_md_path = os.path.join(target_dir, "SKILL.md")
    if os.path.isfile(skill_md_path):
        with open(skill_md_path, "r", encoding="utf-8") as f:
            content = f.read()

        title_case = " ".join(word.capitalize() for word in name.split("-"))
        desc_text = description if description else f"Operational instructions and workflows for {name}."

        content = content.replace("name: template-skill", f"name: {name}")
        content = content.replace(
            "description: Brief one-sentence summary of what this skill does and when the agent should activate it.",
            f"description: {desc_text}",
        )
        content = content.replace("# Template Skill Name", f"# {title_case}")

        with open(skill_md_path, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"[SUCCESS] Skill created at: {target_dir}")
    print("\nNext steps:")
    print(f"  1. Edit {os.path.relpath(skill_md_path, repo_root)} to define your instructions.")
    print(f"  2. Add helper scripts to skills/{name}/scripts/ if needed.")
    print(f"  3. Add templates/configs to skills/{name}/assets/ if needed.")
    print(f"  4. Test your skill using: python tools/validate-skills.py skills/{name}")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Scaffold a new agent skill.")
    parser.add_argument("name", help="Name of the skill in kebab-case (e.g. 'my-awesome-skill')")
    parser.add_argument(
        "--description",
        "-d",
        default="",
        help="Brief description of the skill for the YAML frontmatter",
    )
    args = parser.parse_args()
    return create_skill(args.name, args.description)


if __name__ == "__main__":
    sys.exit(main())
