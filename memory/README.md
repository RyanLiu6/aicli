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

## Current Memory Files

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
