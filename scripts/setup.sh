#!/usr/bin/env bash

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Get the repo root (parent of scripts directory)
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Default Claude Code config directory
CLAUDE_CONFIG_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"

echo "========================================"
echo "Claude Code Configuration Setup"
echo "========================================"
echo ""
echo "Repo root: $REPO_ROOT"
echo "Target directory: $CLAUDE_CONFIG_DIR"
echo ""

# Function to backup existing file or directory
backup_if_exists() {
    local path=$1
    if [ -e "$path" ] && [ ! -L "$path" ]; then
        local backup_path="${path}.backup.$(date +%Y%m%d_%H%M%S)"
        echo -e "${YELLOW}Backing up existing $path to $backup_path${NC}"
        mv "$path" "$backup_path"
    elif [ -L "$path" ]; then
        echo -e "${YELLOW}Removing existing symlink: $path${NC}"
        rm "$path"
    fi
}

# Function to create symlink
create_symlink() {
    local source=$1
    local target=$2
    local name=$3

    if [ ! -e "$source" ]; then
        echo -e "${RED}Warning: Source $name not found at $source${NC}"
        return 1
    fi

    backup_if_exists "$target"

    echo -e "${GREEN}Creating symlink for $name${NC}"
    ln -s "$source" "$target"
    echo "  $target -> $source"
}

# Create Claude config directory if it doesn't exist
if [ ! -d "$CLAUDE_CONFIG_DIR" ]; then
    echo -e "${YELLOW}Creating Claude config directory: $CLAUDE_CONFIG_DIR${NC}"
    mkdir -p "$CLAUDE_CONFIG_DIR"
fi

echo ""
echo "Setting up symlinks..."
echo ""

# Symlink CLAUDE.md (main global config)
# Note: memory/ files are imported via @path in CLAUDE.md, so no symlink needed
create_symlink "$REPO_ROOT/CLAUDE.md" "$CLAUDE_CONFIG_DIR/CLAUDE.md" "CLAUDE.md"

# Symlink skills directory (Claude Code scans this directory)
create_symlink "$REPO_ROOT/skills" "$CLAUDE_CONFIG_DIR/skills" "skills"

# Symlink settings.json
create_symlink "$REPO_ROOT/settings.json" "$CLAUDE_CONFIG_DIR/settings.json" "settings.json"

echo ""
echo -e "${GREEN}========================================"
echo "Setup complete!"
echo "========================================${NC}"
echo ""
echo "Your Claude Code configuration is now symlinked to this repository."
echo "Any changes you make in either location will be reflected in both."
echo ""
echo "To verify the setup, run:"
echo "  ls -la $CLAUDE_CONFIG_DIR"
echo ""
