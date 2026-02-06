# aicli

Unified configuration for AI CLI tools ([Claude Code](https://claude.com/claude-code), [Gemini CLI](https://github.com/google-gemini/gemini-cli), [OpenCode](https://opencode.ai/)).

## Setup

```bash
git clone git@github.com:RyanLiu6/aicli.git ~/aicli
cd ~/aicli
./scripts/bootstrap    # install dependencies and setup all tools
uv run setup claude    # setup specific tool only
```

## Structure

```
├── memory/                 # Shared rules (imported via @path in each tool's config)
├── skills/                 # Canonical skills (source of truth, markdown format)
├── templates/              # PR and review templates
├── modules/
│   ├── claude/             # Claude Code config (CLAUDE.md, settings.json)
│   │   └── hooks/          # Claude Code hooks (e.g., notify.sh)
│   ├── gemini/             # Gemini CLI config (GEMINI.md, settings.json)
│   └── opencode/           # OpenCode config (AGENTS.md, opencode.json)
├── scripts/
│   ├── bootstrap           # One-command setup (uv sync + setup)
│   ├── cli.py              # CLI entry point
│   └── setup.py            # Creates symlinks and generates skills
├── tests/                  # Pytest test suite
├── tasks.py                # Invoke tasks (test, lint, format, typecheck)
├── tools.json              # Tool definitions for setup script
└── .pre-commit-config.yaml # Pre-commit hooks (ruff format + check)
```

## How It Works

The `setup.py` script:
1. Symlinks config files from `modules/<tool>/` to each tool's config directory
2. For Claude/OpenCode: symlinks `skills/` directly (same markdown format)
3. For Gemini: generates TOML files from markdown skills on-the-fly

No manual syncing needed - just run `uv run setup` after adding or modifying skills.

## Development

### Tasks

Development tasks are managed via [Invoke](https://www.pyinvoke.org/):

```bash
inv test                # run tests
inv lint                # run ruff check
inv lint --fix          # run ruff check with auto-fix
inv format              # run ruff format
inv format --check      # check formatting without modifying
inv typecheck           # run pyright
```

### Pre-commit

```bash
uv run pre-commit install
```

Runs ruff format and ruff check on staged files before each commit.

### Bootstrap

`./scripts/bootstrap` runs `uv sync` followed by `uv run setup` in one step - useful for fresh clones or CI.

## CI

GitHub Actions runs lint, typecheck, and tests on pull requests (macOS and Ubuntu).

## Adding Shared Rules

Create a file in `memory/`:
```bash
echo "# My Rules" > memory/my-rules.md
```

Import in each tool's config file:
```markdown
@../../memory/my-rules.md
```

## Adding Skills

Add markdown files to `skills/`:
```markdown
---
description: Brief description for the skill
---

# Skill Name

Instructions here...
```

Run `uv run setup` to apply changes.

## Adding a New Tool

1. Add to `tools.json`:
    ```json
    "newtool": {
      "name": "New Tool",
      "config_dir": "~/.newtool",
      "tool_dir": "modules/newtool",
      "symlinks": [{"source": "CONFIG.md", "target": "CONFIG.md"}],
      "skills_symlink": {"source": "skills", "target": "skills"}
    }
    ```

2. Create `modules/newtool/` with config files

3. Run `uv run setup newtool`

## Known Issues

### Gemini CLI: Tool Permissions Don't Persist

The `tools.allowed` and `tools.exclude` settings in `settings.json` only work in non-interactive mode. In interactive mode, Gemini ignores these settings.

**Workaround:** The setup script adds an alias to `~/.zshrc`:
```bash
alias gemini='gemini --yolo'
```

Run `source ~/.zshrc` after setup to apply.
