# aicli

Unified configuration for AI CLI tools ([Claude Code](https://claude.com/claude-code), [Gemini CLI](https://github.com/google-gemini/gemini-cli)).

## Setup

```bash
git clone git@github.com:RyanLiu6/aicli.git ~/aicli
python scripts/setup.py        # all tools
python scripts/setup.py claude # specific tool
```

## Structure

```
├── shared/memory/       # Shared rules (imported via @path in each tool's config)
├── claude/              # Claude Code: CLAUDE.md, settings.json, skills/
├── gemini/              # Gemini CLI: GEMINI.md, settings.json, commands/
├── tools.json           # Tool definitions for setup script
└── scripts/setup.py     # Creates symlinks to ~/.claude, ~/.gemini, etc.
```

## Adding Shared Rules

```bash
echo "# My Rules" > shared/memory/my-rules.md
```

Then import in each tool's config:
```markdown
@../shared/memory/my-rules.md
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
3. Run `python scripts/setup.py newtool`
