# Skills

Reusable skills that can be invoked across different projects in Claude Code.

## Directory Structure

Each skill must be in its own subdirectory with a `SKILL.md` file:

```
skills/
├── clean-docs/
│   └── SKILL.md
├── create-pr/
│   └── SKILL.md
├── make-commits/
│   └── SKILL.md
├── update-pr/
│   └── SKILL.md
└── README.md
```

## Current Skills

### /clean-docs
Evaluate and clean stale documentation from `~/dev/docs/`:
- Scans project note files for staleness
- Uses sub-agents to assess relevance
- Removes or flags outdated docs

### /make-commits
Analyze the working tree and create logical commits from staged/unstaged changes:
- Breaks changes into logical groups (features, bug fixes, components)
- Runs lints and type-checks before committing
- Creates commits with descriptive messages following repo style
- Uses TodoWrite to track commit progress
- Never commits to main/master directly
- Does NOT push - only creates local commits

### /create-pr
Create pull requests with concise, well-formatted descriptions:
- Ensures you're on a feature branch (not main/master)
- Reviews commits and changes
- Asks for user confirmation before pushing (respects git workflow rules)
- Creates PR with concise bullet-point summary
- Follows consistent formatting conventions

### /update-pr
Update existing pull requests with new commits and refreshed descriptions:
- Verifies you're on a branch with an existing PR
- Shows ALL commits in the branch (not just unpushed)
- Asks for user confirmation before pushing (respects git workflow rules)
- Recomputes PR description from scratch based on all commits
- Updates title only if needed
- Handles already-pushed commits gracefully

## Creating New Skills

Each skill needs:

1. **Directory**: `skills/<skill-name>/`
2. **SKILL.md file** with YAML frontmatter:

```yaml
---
name: skill-name
description: Brief description of what this skill does
---

# Skill Title

Instructions and content here...
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | No | Display name (defaults to directory name) |
| `description` | Recommended | What the skill does and when to use it |
| `disable-model-invocation` | No | Set `true` to prevent auto-loading |
| `user-invocable` | No | Set `false` to hide from `/` menu |
| `argument-hint` | No | Hint for autocomplete (e.g., `[issue-number]`) |

## Usage

Invoke skills with slash commands:
```
/skill-name [arguments]
```

Claude Code will load the skill's prompt and execute the specialized capability.
