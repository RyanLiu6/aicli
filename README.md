# aicli

Unified configuration for AI CLI tools ([Claude Code](https://claude.com/claude-code), [Gemini CLI](https://github.com/google-gemini/gemini-cli)).

## Setup

```bash
git clone git@github.com:RyanLiu6/aicli.git ~/aicli
cd ~/aicli
uv sync              # install dependencies
uv run setup         # symlink all tools
uv run setup claude  # symlink specific tool
uv run help          # show available commands
```

## Structure

```
├── shared/memory/          # Shared rules (imported via @path in each tool's config)
├── claude/                 # Claude Code: CLAUDE.md, settings.json, skills/
├── gemini/                 # Gemini CLI: GEMINI.md, settings.json, commands/
├── tools.json              # Tool definitions for setup script
├── pyproject.toml          # Python dependencies (click, rich)
└── scripts/
    ├── setup.py            # Creates symlinks to ~/.claude, ~/.gemini, etc.
    └── sync_skills.py      # Syncs Claude skills ↔ Gemini commands
```

## Adding Shared Rules

```bash
echo "# My Rules" > shared/memory/my-rules.md
```

Then import in each tool's config:
```markdown
@../shared/memory/my-rules.md
```

## Syncing Skills/Commands

Claude Code uses "skills" (markdown) while Gemini CLI uses "commands" (TOML). Sync between them:

```bash
uv run claude-to-gemini  # Claude → Gemini
uv run gemini-to-claude  # Gemini → Claude
```

## Adding Tools

1. Add to `tools.json`:
   ```json
   {
     "newtool": {
       "name": "New Tool",
       "config_dir": "~/.newtool",
       "tool_dir": "newtool",
       "symlinks": [{"source": "CONFIG.md", "target": "CONFIG.md"}]
     }
   }
   ```

2. Create directory and config file with shared imports
3. Run `uv run setup newtool`

## Known Issues

### Gemini CLI: Tool Permissions Don't Persist (as of Dec 2024)

The `tools.allowed` and `tools.exclude` settings in `settings.json` **only work in non-interactive mode** (e.g., `gemini -p "prompt"`). In interactive mode, Gemini CLI ignores these settings and prompts for every command.

**Related GitHub Issues:**
- [#4340](https://github.com/google-gemini/gemini-cli/issues/4340) - "Always Approve" not persisting across sessions
- [#13737](https://github.com/google-gemini/gemini-cli/issues/13737) - Feature request to save permissions to settings

**Workaround:** The setup script automatically adds an alias to `~/.zshrc`:

```bash
alias gemini='gemini --yolo'
```

This bypasses all confirmation prompts. Run `source ~/.zshrc` after setup to apply.

**Status:** Check the issues above to see if this has been fixed. Once fixed, remove the alias from `~/.zshrc`.
