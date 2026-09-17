---
name: template-skill
description: Brief one-sentence summary of what this skill does and when the agent should activate it.
---

# Template Skill Name

Provide a concise overview of what this skill accomplishes, its primary use case, and what problem it solves.

---

## When to Activate

Specify the explicit conditions, prompts, or file contexts that should trigger this skill:
- When the user asks to perform `<specific task>`
- When working on files matching `<pattern>`
- When the user issues command `/<trigger-phrase>`

---

## Prerequisites & Dependencies

List any software, credentials, or environment requirements needed before running this skill:
- Python 3.9+ or Node.js runtime
- Required CLI tools or API credentials
- Expected files in the project workspace

---

## Operational Workflow

Provide unambiguous step-by-step instructions for the agent to follow.

### Step 1: Inspection & Pre-Checks
1. Check if prerequisites are satisfied.
2. View relevant target files using file inspection tools before making modifications.

### Step 2: Execution
1. If helper scripts are available, execute them via command line tools:
   ```bash
   python scripts/example_helper.py --input "target-file.ext"
   ```
2. Parse the script output and apply necessary edits.

### Step 3: Verification
1. Verify that changes match expected requirements.
2. Report the results to the user with actionable next steps.

---

## Bundled Resources

### Helper Scripts (`scripts/`)
- `example_helper.py`: Demonstrates an automated task or helper tool for this skill.

### Static Assets (`assets/`)
- `example_template.txt`: Boilerplate configuration or template file for reference.

---

## Troubleshooting & Edge Cases

| Issue / Error | Likely Cause | Recommended Agent Action |
| :--- | :--- | :--- |
| Prerequisite missing | Tool/dependency not installed | Inform the user with exact installation command |
| Script execution error | Invalid argument format | Check inputs and rerun script |
