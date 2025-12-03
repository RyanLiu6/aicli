#!/usr/bin/env python3
"""CLI help command."""

from rich.console import Console
from rich.table import Table

COMMANDS = {
    "setup": "Create symlinks for AI CLI tools (~/.claude, ~/.gemini)",
    "claude-to-gemini": "Sync Claude skills → Gemini commands",
    "gemini-to-claude": "Sync Gemini commands → Claude skills",
    "help": "Show this help message",
}


def main() -> None:
    """Show available commands."""
    console = Console()

    table = Table(title="Available Commands", show_header=True, header_style="bold")
    table.add_column("Command")
    table.add_column("Description")

    for cmd, desc in COMMANDS.items():
        table.add_row(f"uv run {cmd}", desc)

    console.print(table)


if __name__ == "__main__":
    main()
