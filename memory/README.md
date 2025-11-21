# Core Memory

Cross-project knowledge and workflows that persist across Claude Code sessions.

## Purpose

Core memory files contain important patterns, insights, and workflows that are useful across multiple projects. Unlike project-specific notes (which live in each project's `_claude/` directory), these are curated pieces of knowledge that you want Claude to remember globally.

## When to Add Memory Files

Only promote content to core memory when:
- The knowledge applies across multiple projects
- It represents a reusable pattern or workflow
- You explicitly want this information available in all sessions
- It contains general development practices or architectural insights

**Note**: Don't automatically add things here. Core memory should be intentionally curated to avoid clutter.

## How Memory Files Are Loaded

Memory files are imported by the main `CLAUDE.md` file using the `@path` syntax:
```markdown
@memory/base.md
@memory/project-notes-workflow.md
```

When `~/claude/CLAUDE.md` is symlinked to `~/.claude/CLAUDE.md`, Claude Code automatically loads all imported memory files at startup.

**Important**: The memory/ folder itself is NOT symlinked. The `@path` imports in CLAUDE.md resolve relative to the actual file location (`~/claude/`), so memory files are accessed directly from your git repo. This means:
- Memory files stay in version control
- No need to symlink the memory/ directory
- Changes to memory files are immediately active

## Current Memory Files

### base.md
Core global rules and preferences that apply to all Claude Code sessions:
- Git workflow rules (commit/push behavior)
- Code style preferences
- Communication preferences
- Other fundamental rules that should always be active

**This is the foundation** - add universal rules here that should apply everywhere.

### project-notes-workflow.md
Guidelines for organizing project-specific notes vs. core memories:
- Project notes go in `_claude/` directories within each project
- Core memory is for cross-project, curated knowledge only
- Export to core memory only when explicitly requested
- Keeps project knowledge isolated while preserving important patterns

## File Naming

Use clear, descriptive filenames that make the content easily searchable:
- `project-notes-workflow.md` (good)
- `workflow.md` (too vague)
- `temp-notes.md` (temporary files don't belong in core memory)

## Best Practices

1. **Be selective**: Not everything deserves to be in core memory
2. **Stay organized**: Use clear file names and structure
3. **Keep it current**: Update or remove outdated information
4. **Add context**: Include enough detail for future sessions to understand
5. **Cross-reference**: Link to related memory files when relevant
