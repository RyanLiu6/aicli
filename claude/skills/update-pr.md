---
description: Update existing pull request with new commits
---

# Update Pull Request

Push new commits to an existing PR and update its description.

## Workflow

1. Check branch and PR: `git branch --show-current` and `gh pr view --json number,title,url,baseRefName,body`
2. Review ALL commits: `git log <base-branch>..HEAD --oneline`
3. Check for unpushed: `git log origin/<branch>..HEAD --oneline`
4. **Ask user** before pushing unpushed commits
5. Push if confirmed: `git push`
6. Recompute PR description based on ALL commits (use previous description as style guide)
7. Update PR: `gh pr edit <number> --title "..." --body "..."`
8. Return the PR URL

## Key Principles

- Generate description from ALL commits, not just new ones
- Keep previous description's format/style
- Only update title if no longer accurate
- Always ask before pushing
