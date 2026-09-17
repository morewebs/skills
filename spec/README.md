# The Agent Skills Standard Specification

> Reference: [agentskills.io](https://agentskills.io) & open community conventions

The **Agent Skills Standard** is an open, file-system-based specification for packaging reusable capabilities, expert workflows, and operational runbooks for AI coding agents and autonomous assistants.

---

## 1. Core Principles

1. **Zero Registry Overhead**: Skills exist directly as directories on the local file system. No remote package registry, database, or API setup is required.
2. **File-System Native**: Agents discover skills by inspecting known paths (`skills/`, `.claude/skills/`, `.cursor/skills/`, `~/.gemini/config/skills/`) at startup.
3. **Progressive Disclosure**: Agents only parse metadata (`name`, `description`) during the initial indexing pass. Deep instructions and scripts are read into context **on-demand** when the skill is actually invoked.
4. **Agent Agnostic**: The standard is supported across leading agent frameworks including Antigravity, Claude Code, Cursor, Copilot Workspace, and custom LLM tool runners.

---

## 2. Directory Layout of a Single Skill

Every skill resides in a standalone, dedicated directory:

```
<skill-name>/
├── SKILL.md        # [REQUIRED] YAML frontmatter + markdown execution guidelines
├── scripts/        # [OPTIONAL] Executable scripts (.py, .sh, .js, .ps1)
├── assets/         # [OPTIONAL] Static templates, reference files, schemas
└── evals.json      # [OPTIONAL] Test scenarios and evaluation assertions
```

### 2.1 Directory Naming Rules
- **Format**: Lowercase, kebab-case (e.g. `frontend-design`, `docker-deploy`, `api-scaffolder`).
- **Characters**: `[a-z0-9-]`. No uppercase letters, spaces, or underscores.

---

## 3. Specification Details

### 3.1 `SKILL.md` (Required)
The entry point of any skill. It begins with a YAML frontmatter block enclosed by triple dashes (`---`), followed by markdown instructions.

#### Minimum Required Frontmatter
```yaml
---
name: skill-name
description: Clear, concise summary of what this skill does and when an agent should activate it.
---
```

#### Extended Frontmatter Fields
```yaml
---
name: skill-name
description: Comprehensive description for semantic skill matching.
version: 1.0.0
author: Your Name or Organization
compatibility:
  tools: ["run_command", "view_file", "replace_file_content"]
  os: ["linux", "windows", "darwin"]
tags: ["devops", "automation", "api"]
---
```

#### Markdown Body Structure
A standard `SKILL.md` body is organized into clear operational sections:
1. **Overview**: High-level explanation of the skill's purpose and scope.
2. **When to Activate**: Trigger words, file types, or user scenarios.
3. **Prerequisites & Dependencies**: Environment requirements (e.g., Python 3.10+, Docker, SSH keys).
4. **Step-by-Step Procedure**: Clear numbered instructions directing the agent on what actions to take.
5. **Helper Scripts (`scripts/`)**: Detailed documentation on what scripts exist, their arguments, and expected output.
6. **Reference Assets (`assets/`)**: Explanation of templates or configs available to the agent.
7. **Troubleshooting & Edge Cases**: Common failure modes and how the agent should handle them.

---

### 3.2 `scripts/` (Optional)
Contains deterministic automation scripts that the agent can execute using its command execution tools (e.g. `run_command`).
- **Language**: Python (`.py`), Bash (`.sh`), PowerShell (`.ps1`), or Node.js (`.js`/`.ts`).
- **Design Rule**: Scripts should be idempotent, produce human-and-agent-readable stdout/stderr, and return non-zero exit codes on failure.

---

### 3.3 `assets/` (Optional)
Houses static resources that the agent reads into memory or copies into project workspaces:
- Template files (e.g., `Dockerfile.template`, boilerplate components).
- Schemas (`schema.json`).
- Reference datasets, prompt guides, or API specifications.

---

### 3.4 `evals.json` (Optional)
Specifies evaluation scenarios to verify that the agent executes the skill accurately.

```json
[
  {
    "id": "eval-basic-run",
    "prompt": "User query that triggers the skill",
    "expected_behavior": "Description of expected agent behavior",
    "criteria": [
      "Agent activates the skill without extraneous prompting",
      "Agent executes the helper script with correct parameters",
      "Expected output file is generated in the workspace"
    ]
  }
]
```

---

## 4. Runtime Discovery Scopes

| Scope | Location Examples | Use Case |
| :--- | :--- | :--- |
| **Workspace (Project)** | `.agents/skills/`<br>`.cursor/skills/`<br>`.claude/skills/` | Project-specific runbooks shared with repository collaborators. |
| **Global (User)** | `~/.gemini/config/skills/`<br>`~/.claude/skills/`<br>`~/.cursor/skills/` | Personal skills library available across every project on your workstation. |
