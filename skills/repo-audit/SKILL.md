---
name: repo-audit
description: Inspects the repository for essential files (README, .gitignore, license), verifies clean git status, and generates a structured health report. Use when evaluating a new or existing repository's readiness and cleanliness.
---

# Repository Audit Skill

This skill provides a standardized workflow for auditing the health, cleanliness, and readiness of a software repository.

---

## When to Activate

Activate this skill when:
- The user asks for a "repository audit", "repo check", or "repository health check".
- Starting work on a new repository or preparing a repository for public release.
- Verifying whether essential repository files (.gitignore, README, license) exist.

---

## Workflow Procedure

### Step 1: Run the Audit Script
Execute the bundled audit helper script to scan the repository root:

```bash
python skills/repo-audit/scripts/audit_repo.py --target "."
```

The script will inspect:
1. Presence of `README.md`
2. Presence of `.gitignore`
3. Presence of `LICENSE` or `LICENSE.md`
4. Git repository status (untracked, modified, or unstaged files)

### Step 2: Format the Health Report
Using the template from `skills/repo-audit/assets/report_template.md`, compile the findings into a concise markdown summary for the user.

### Step 3: Propose Remediation
If any checks failed (e.g., missing `.gitignore` or uncommitted changes), recommend specific commands or files to create.

---

## Bundled Resources

- **`scripts/audit_repo.py`**: Python script that performs the automated checks and outputs JSON / text results.
- **`assets/report_template.md`**: Markdown template used to structure the final audit report presented to the user.
- **`evals.json`**: Evaluation test cases for validating this skill.
