# Project Notes & Memory Workflow

## Project-Specific Notes (`_claude/`)

- Location: `_claude/notes/<descriptive-name>.md` in each project
- When to create: Answers to questions like "How does X work?", "Where is Y implemented?"
- Include: Question, answer, code references, file paths

## Shared Memory (`~/aicli/shared/memory`)

**Only promote when user explicitly asks** ("Add this as a memory", "Save to core memory")

Candidates: Cross-project patterns, reusable workflows, general development practices

## Export Restrictions

The `_claude/` directory is a sandbox. **Never auto-export** to shared memory or skills - only when explicitly requested.
