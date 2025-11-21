# Skills

Reusable skills that can be invoked across different projects in Claude Code.

## Purpose

Skills are specialized capabilities that can be called by name to perform specific tasks. They provide domain expertise and can be reused across all your projects.

## Current Skills

### create-pr.md
Create pull requests with concise, well-formatted descriptions. This skill:
- Ensures you're on a feature branch (not main/master)
- Reviews commits and changes
- Asks for user confirmation before pushing (respects git workflow rules)
- Creates PR with concise bullet-point summary
- Follows consistent formatting conventions

## What Are Skills?

Skills in Claude Code are specialized prompts or capabilities that:
- Provide domain-specific expertise (e.g., "pdf", "xlsx")
- Can be invoked by name during conversations
- Work across all projects
- Encapsulate common workflows or patterns

## Creating Skills

Skills can be defined to handle specific task types:
- Document processing (PDFs, spreadsheets)
- Code analysis patterns
- Testing workflows
- Deployment procedures
- Custom domain-specific tasks

## Usage

Once skills are defined, they can be invoked in conversations:
```
/skill-name [arguments]
```

Claude Code will load the skill's prompt and execute the specialized capability.

## Getting Started

To add your first skill:
1. Identify a repetitive task or specialized domain
2. Define the skill's scope and capabilities
3. Create the skill definition in this directory
4. Test it across different projects
5. Refine based on real-world usage

## Best Practices

- **Single responsibility**: Each skill should do one thing well
- **Clear naming**: Use descriptive names that indicate the skill's purpose
- **Documentation**: Include usage examples in skill definitions
- **Reusability**: Design skills to work across different project contexts
