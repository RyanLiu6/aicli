---
description: Create pull requests with concise descriptions
---

# Create Pull Request

Create a pull request with a concise, well-formatted description.

## Workflow

1. **Verify branch**: Ensure you're NOT on main/master branch
2. **Review changes**: Check git status and recent commits
3. **Check with user**: Confirm before pushing (per user's git workflow rules)
4. **Push to origin**: Push to `origin` from the current branch (if needed)
5. **Create PR**: Use `gh pr create` with description from template
6. **Return PR URL**

## PR Title Format

- If user provides a Linear ticket (e.g., `[DP-1234]`), use: `[DP-1234] - Brief title`
- Otherwise, just use: `Brief title`

## PR Description Format

Use the template at `templates/pr-description.md`:

```
### Why are you making these changes?

<!-- Explain the context, problem, and solution -->

### How has this been tested?

<!-- Describe testing approach -->
```

## Instructions

1. Check current branch: `git branch --show-current`
   - If on main/master, stop and ask user to create a feature branch

2. Review changes:
   - Run `git status` to see what's committed
   - Run `git log main..HEAD --oneline` (or `master..HEAD`) to see commits
   - Review recent conversation for context

3. Check remote status:
   - Run `git status` to see if branch is already tracking remote
   - If already pushed and up-to-date, skip push step

4. **ASK USER**: "Ready to push and create PR? Here's what will be pushed: [list commits]"
   - Wait for user confirmation
   - This respects the user's git workflow rules

5. Push changes (if user confirmed and needed):
   ```bash
   git push -u origin <current-branch>
   ```

6. Create PR:
   ```bash
   gh pr create --title "[DP-XXXX] - Brief title" --body "$(cat <<'EOF'
   ### Why are you making these changes?

   <context and explanation>

   ### How has this been tested?

   <testing approach>
   EOF
   )"
   ```

7. Return the PR URL to the user

## Notes

- If `gh pr create` fails because PR already exists, use `gh pr view --web` to open it
- Always respect user's git workflow rules (check before push, use feature branches)
- If branch is already pushed and up-to-date, can skip directly to PR creation