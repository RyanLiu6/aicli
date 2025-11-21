# Project Notes & Memory Workflow

## Overview
A system for organizing project-specific notes and promoting them to core memory.

## Project-Specific Notes (`_claude/` directory)

### Location
- Each project should have a `_claude/` directory at its root
- Notes go in `_claude/notes/<descriptive-name>.md`

### When to Create Notes
When user asks clarifying questions like:
- "How does X work?"
- "What's the call chain of this API?"
- "Where is feature Y implemented?"
- Any explanatory/architectural questions

### What to Include
- The original question
- Detailed answer with code references
- File paths and line numbers where relevant
- Architecture or flow diagrams if helpful

### Process
1. Document question and answer in markdown
2. Save to `_claude/notes/<descriptive-name>.md` in that project
3. Keep as project-specific reference material

## Core Memory (`~/claude/memory`)

### When to Promote
**Only when explicitly requested** by user:
- "Add this as a memory"
- "Convert this note to core memory"
- "Save this to core memory"

### What Gets Promoted
- Important patterns or workflows (like this document)
- Cross-project knowledge
- Reusable architectural insights
- General development practices

### Location
- `~/claude/memory/<descriptive-name>.md`
- Use clear, searchable filenames

## Playground Rule

### The `_claude/` Directory
- Serves as sandbox/playground for that specific project
- Can include:
  - Notes
  - Temporary analysis files
  - Project-specific documentation
  - Working documents

### Export Restrictions
**Never automatically export to:**
- `~/claude/memory/` (core memories)
- `~/claude/skills/` (reusable skills)

**Only export when user explicitly requests it**

## Benefits
- Keeps project knowledge isolated and organized
- Prevents core memory clutter
- User curates what becomes persistent knowledge
- Easy to reference project-specific context
