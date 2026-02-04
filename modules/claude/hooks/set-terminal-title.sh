#!/bin/bash
# Sets terminal title to: repo_name | prompt_start
# Used by SessionStart and UserPromptSubmit hooks

INPUT=$(cat)

CWD=$(echo "$INPUT" | jq -r '.cwd // empty')
PROMPT=$(echo "$INPUT" | jq -r '.prompt // empty')

# Get repo/directory name
if [ -n "$CWD" ]; then
  REPO_NAME=$(basename "$CWD")
else
  REPO_NAME="Claude Code"
fi

# Build title
if [ -n "$PROMPT" ]; then
  # Truncate prompt to 40 chars, add ellipsis if longer
  PROMPT_SHORT=$(echo "$PROMPT" | head -c 40)
  if [ ${#PROMPT} -gt 40 ]; then
    PROMPT_SHORT="${PROMPT_SHORT}..."
  fi
  TITLE="${REPO_NAME} | ${PROMPT_SHORT}"
else
  TITLE="Claude Code | ${REPO_NAME}"
fi

# Set terminal title via escape sequence
printf "\033]0;%s\007" "$TITLE"

exit 0
