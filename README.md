# Claude Code Configuration

Personal configuration repository for [Claude Code](https://claude.com/claude-code), containing settings, core memory, and reusable skills.

## Structure

```
.
├── CLAUDE.md                  # Main global config (symlinked to ~/.claude/CLAUDE.md)
├── settings.json              # Claude Code settings and permissions
├── memory/                    # Core memory files (cross-project knowledge)
│   ├── base.md                # Base global rules (git workflow, etc.)
│   ├── project-notes-workflow.md
│   └── README.md
├── skills/                    # Reusable skills (currently empty)
└── scripts/                   # Setup and utility scripts
    └── setup.sh               # Symlink configuration setup
```

## Getting Started

### Initial Setup

```bash
# Clone this repository
git clone <your-repo-url> ~/claude
cd ~/claude

# Run the setup script
./scripts/setup.sh
```

The setup script creates symlinks from `~/.claude/` to this repo, so changes in either location stay synchronized.

### On New Machines

Simply clone the repo and run `./scripts/setup.sh` - all your Claude Code configuration will be instantly available.

## How It Works

```
Your git repo (~/claude)              Claude Code reads from
├── CLAUDE.md          ────symlink──→ ~/.claude/CLAUDE.md
├── memory/            (no symlink)
│   ├── base.md        ←──@import─── (imported by CLAUDE.md)
│   └── project-notes-workflow.md ← (imported by CLAUDE.md)
├── skills/            ────symlink──→ ~/.claude/skills/
└── settings.json      ────symlink──→ ~/.claude/settings.json
```

**Key insight**: Only CLAUDE.md, skills/, and settings.json are symlinked. The memory/ folder stays in the repo and is accessed via `@path` imports in CLAUDE.md.

## Components

### Global Configuration (`CLAUDE.md`)

The main global configuration file that gets symlinked to `~/.claude/CLAUDE.md`. This file:
- Uses `@path` syntax to import memory files from the repo
- Keeps all configuration version-controlled
- Enables portable setup across machines
- Currently imports:
  - `memory/base.md` - Core global rules (git workflow)
  - `memory/project-notes-workflow.md` - Notes organization guidelines

**Key benefit**: By symlinking CLAUDE.md (which imports memory files via `@path`), your entire configuration stays in this git repo without needing to symlink the memory folder itself.

### Settings (`settings.json`)

Configures Claude Code behavior and tool permissions:

- **Permissions**: Most tools allowed by default, with confirmation required for:
  - Git commits (`git commit`)
  - Git pushes (`git push`)
  - File deletions (`rm`)
- **Default Mode**: `acceptEdits` - automatically accept file edits
- **Always Thinking**: Enabled for better reasoning transparency
- **Co-authored-by**: Disabled - git commits won't include Claude Code co-author attribution

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

### Adding New Memory Files

1. Create a new memory file:
   ```bash
   echo "# My Custom Rules" > memory/my-rules.md
   ```

2. Import it in `CLAUDE.md`:
   ```markdown
   @memory/my-rules.md
   ```

3. Commit to git:
   ```bash
   git add memory/my-rules.md CLAUDE.md
   git commit -m "Add custom rules memory"
   ```

Changes take effect immediately - no need to restart Claude Code.

### Customizing Settings

Edit `settings.json` to adjust permissions, default modes, and other behavior. Changes are synced via symlink.

### Creating Skills

Add custom skills to `skills/` directory. See [skills/README.md](skills/README.md) for details.

## Philosophy

This setup follows a clear separation of concerns:
- **Project-specific knowledge** stays in project `_claude/` directories
- **Core memory** contains only curated, cross-project insights
- **Settings** balance automation with safety (auto-accept edits, but confirm destructive operations)
