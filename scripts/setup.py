#!/usr/bin/env python3
"""
AI CLI Tools Setup Script

Sets up symlinks for multiple AI CLI tools (Claude Code, Gemini CLI, etc.)
by reading configuration from tools.json.

Usage:
    python setup.py              # Setup all tools
    python setup.py claude       # Setup only Claude Code
    python setup.py gemini       # Setup only Gemini CLI
    python setup.py --list       # List available tools
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


class Colors:
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    RED = "\033[0;31m"
    BLUE = "\033[0;34m"
    BOLD = "\033[1m"
    NC = "\033[0m"  # No Color


def print_colored(message: str, color: str = Colors.NC) -> None:
    print(f"{color}{message}{Colors.NC}")


def get_repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def load_tools_config(repo_root: Path) -> dict:
    config_path = repo_root / "tools.json"
    if not config_path.exists():
        print_colored(f"Error: tools.json not found at {config_path}", Colors.RED)
        sys.exit(1)

    with open(config_path) as f:
        return json.load(f)


SHELL_ALIASES = {
    "gemini": {
        "alias": "alias gemini='gemini --yolo'",
        "comment": "# Gemini CLI: run in yolo mode (auto-approve all tools)",
    },
}


def setup_shell_alias(tool_id: str) -> bool:
    """Add shell alias to ~/.zshrc if it doesn't exist."""
    if tool_id not in SHELL_ALIASES:
        return True

    alias_config = SHELL_ALIASES[tool_id]
    alias_line = alias_config["alias"]
    comment_line = alias_config["comment"]

    zshrc_path = Path.home() / ".zshrc"

    if not zshrc_path.exists():
        print_colored(f"  Warning: ~/.zshrc not found, skipping alias setup", Colors.YELLOW)
        return False

    with open(zshrc_path) as f:
        content = f.read()

    if alias_line in content:
        print_colored(f"  Alias already exists in ~/.zshrc", Colors.GREEN)
        return True

    print_colored(f"  Adding alias to ~/.zshrc", Colors.GREEN)
    with open(zshrc_path, "a") as f:
        f.write(f"\n{comment_line}\n{alias_line}\n")

    print(f"    Added: {alias_line}")
    print_colored(f"  Run 'source ~/.zshrc' or restart your shell to apply", Colors.YELLOW)
    return True


def backup_if_exists(path: Path) -> None:
    if path.exists() and not path.is_symlink():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f"{path.suffix}.backup.{timestamp}")
        print_colored(f"  Backing up existing {path.name} to {backup_path.name}", Colors.YELLOW)
        path.rename(backup_path)
    elif path.is_symlink():
        print_colored(f"  Removing existing symlink: {path}", Colors.YELLOW)
        path.unlink()


def create_symlink(source: Path, target: Path, name: str) -> bool:
    if not source.exists():
        print_colored(f"  Warning: Source {name} not found at {source}", Colors.RED)
        return False

    backup_if_exists(target)

    print_colored(f"  Creating symlink for {name}", Colors.GREEN)
    target.symlink_to(source)
    print(f"    {target} -> {source}")
    return True


def setup_tool(tool_id: str, tool_config: dict, repo_root: Path) -> bool:
    name = tool_config["name"]
    config_dir = Path(os.path.expanduser(tool_config["config_dir"]))
    tool_dir = repo_root / tool_config["tool_dir"]

    print_colored(f"\n{'=' * 50}", Colors.BLUE)
    print_colored(f"Setting up {name}", Colors.BOLD)
    print_colored(f"{'=' * 50}", Colors.BLUE)
    print(f"  Source directory: {tool_dir}")
    print(f"  Target directory: {config_dir}")

    # Check if tool directory exists in repo
    if not tool_dir.exists():
        print_colored(f"  Warning: Tool directory {tool_dir} not found, skipping", Colors.YELLOW)
        return False

    # Create config directory if it doesn't exist
    if not config_dir.exists():
        print_colored(f"  Creating config directory: {config_dir}", Colors.YELLOW)
        config_dir.mkdir(parents=True)

    # Create symlinks
    success = True
    for symlink in tool_config.get("symlinks", []):
        source = tool_dir / symlink["source"]
        target = config_dir / symlink["target"]

        if not create_symlink(source, target, symlink["source"]):
            success = False

    # Setup shell aliases if needed
    setup_shell_alias(tool_id)

    return success


def list_tools(config: dict) -> None:
    print_colored("\nAvailable tools:", Colors.BOLD)
    print_colored("-" * 40, Colors.BLUE)

    for tool_id, tool_config in config.get("tools", {}).items():
        name = tool_config.get("name", tool_id)
        config_dir = tool_config.get("config_dir", "unknown")
        print(f"  {Colors.GREEN}{tool_id}{Colors.NC}: {name}")
        print(f"    Config dir: {config_dir}")
        symlinks = tool_config.get("symlinks", [])
        print(f"    Symlinks: {', '.join(s['source'] for s in symlinks)}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Setup symlinks for AI CLI tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python setup.py              # Setup all tools
  python setup.py claude       # Setup only Claude Code
  python setup.py gemini       # Setup only Gemini CLI
  python setup.py claude gemini  # Setup specific tools
  python setup.py --list       # List available tools
        """,
    )
    parser.add_argument(
        "tools",
        nargs="*",
        help="Specific tools to setup (default: all)",
    )
    parser.add_argument(
        "--list",
        "-l",
        action="store_true",
        help="List available tools and exit",
    )

    args = parser.parse_args()

    repo_root = get_repo_root()
    config = load_tools_config(repo_root)

    print_colored("=" * 50, Colors.BLUE)
    print_colored("AI CLI Tools Setup", Colors.BOLD)
    print_colored("=" * 50, Colors.BLUE)
    print(f"Repository root: {repo_root}")

    if args.list:
        list_tools(config)
        return

    tools_config = config.get("tools", {})

    if not tools_config:
        print_colored("Error: No tools defined in tools.json", Colors.RED)
        sys.exit(1)

    # Determine which tools to setup
    if args.tools:
        tools_to_setup = {}
        for tool_id in args.tools:
            if tool_id in tools_config:
                tools_to_setup[tool_id] = tools_config[tool_id]
            else:
                print_colored(f"Warning: Unknown tool '{tool_id}', skipping", Colors.YELLOW)
    else:
        tools_to_setup = tools_config

    if not tools_to_setup:
        print_colored("No valid tools to setup", Colors.RED)
        sys.exit(1)

    # Setup each tool
    results = {}
    for tool_id, tool_config in tools_to_setup.items():
        results[tool_id] = setup_tool(tool_id, tool_config, repo_root)

    # Summary
    print_colored(f"\n{'=' * 50}", Colors.BLUE)
    print_colored("Setup Summary", Colors.BOLD)
    print_colored(f"{'=' * 50}", Colors.BLUE)

    for tool_id, success in results.items():
        name = tools_config[tool_id]["name"]
        status = f"{Colors.GREEN}OK{Colors.NC}" if success else f"{Colors.YELLOW}PARTIAL{Colors.NC}"
        print(f"  {name}: {status}")

    print_colored(f"\n{'=' * 50}", Colors.GREEN)
    print_colored("Setup complete!", Colors.GREEN)
    print_colored(f"{'=' * 50}", Colors.GREEN)


if __name__ == "__main__":
    main()
