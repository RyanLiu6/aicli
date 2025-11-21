# Claude Code Configuration

Personal configuration repository for [Claude Code](https://claude.com/claude-code), containing settings, core memory, and reusable skills.

## Structure

```
.
├── settings.json              # Claude Code settings and permissions
├── memory/                    # Core memory files (cross-project knowledge)
│   └── project-notes-workflow.md
└── skills/                    # Reusable skills (currently empty)
```

## Components

### Settings (`settings.json`)

Configures Claude Code behavior and tool permissions:

- **Permissions**: Most tools allowed by default, with confirmation required for:
  - Git commits (`git commit`)
  - Git pushes (`git push`)
  - File deletions (`rm`)
- **Default Mode**: `acceptEdits` - automatically accept file edits
- **Always Thinking**: Enabled for better reasoning transparency

### Memory (`memory/`)

Core memory files containing cross-project knowledge and workflows that persist across sessions. See [memory/README.md](memory/README.md) for details on:
- What belongs in core memory vs. project-specific notes
- Current memory files and their purposes
- Best practices for managing core memory

### Skills (`skills/`)

Directory for custom reusable skills that can be invoked across different projects. See [skills/README.md](skills/README.md) for:
- What skills are and how they work
- How to create custom skills
- Usage examples and best practices

## Usage

This configuration is automatically loaded by Claude Code when it's placed in the appropriate location. The settings define how Claude Code interacts with your system, while memory files provide persistent context across sessions.

## Philosophy

This setup follows a clear separation of concerns:
- **Project-specific knowledge** stays in project `_claude/` directories
- **Core memory** contains only curated, cross-project insights
- **Settings** balance automation with safety (auto-accept edits, but confirm destructive operations)

## Getting Started

1. Place this repository in your Claude Code configuration directory
2. Customize `settings.json` to match your workflow preferences
3. Add cross-project knowledge to `memory/` as needed
4. Create reusable skills in `skills/` for common tasks
