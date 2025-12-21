#!/usr/bin/env python3
"""
Sync skills/commands between Claude Code, Gemini CLI, and OpenCode.

Converts between:
- Claude Code skills (markdown with YAML frontmatter)
- Gemini CLI commands (TOML)
- OpenCode commands (markdown with YAML frontmatter)
"""

import re
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

console = Console()

TOOLS = {
    "claude": {
        "dir": "claude/skills",
        "ext": ".md",
        "name": "Claude Skills",
    },
    "gemini": {
        "dir": "gemini/commands",
        "ext": ".toml",
        "name": "Gemini Commands",
    },
    "opencode": {
        "dir": "opencode/command",
        "ext": ".md",
        "name": "OpenCode Commands",
    },
}


def get_repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from markdown content."""
    frontmatter = {}
    body = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            yaml_content = parts[1].strip()
            body = parts[2].strip()

            for line in yaml_content.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    frontmatter[key.strip()] = value.strip()

    return frontmatter, body


def parse_toml(content: str) -> dict:
    """Parse simple TOML content (description and prompt fields)."""
    result = {}

    desc_match = re.search(r'description\s*=\s*"([^"]*)"', content)
    if desc_match:
        result["description"] = desc_match.group(1)

    prompt_match = re.search(r'prompt\s*=\s*"""(.*?)"""', content, re.DOTALL)
    if prompt_match:
        result["prompt"] = prompt_match.group(1).strip()

    return result


def skill_to_command(skill_path: Path) -> tuple[str, str, str]:
    """Convert a Claude skill (md) to Gemini command (toml)."""
    content = skill_path.read_text()
    frontmatter, body = parse_frontmatter(content)

    name = skill_path.stem
    description = frontmatter.get("description", "")

    lines = []
    if description:
        lines.append(f'description = "{description}"')

    lines.append('prompt = """')
    lines.append(body)
    lines.append('"""')

    return name, description, "\n".join(lines)


def command_to_skill(command_path: Path) -> tuple[str, str, str]:
    """Convert a Gemini command (toml) to Claude/OpenCode skill (md)."""
    content = command_path.read_text()
    parsed = parse_toml(content)

    name = command_path.stem
    description = parsed.get("description", "")
    prompt = parsed.get("prompt", "")

    lines = []
    if description:
        lines.append("---")
        lines.append(f"description: {description}")
        lines.append("---")
        lines.append("")

    lines.append(prompt)

    return name, description, "\n".join(lines)


def copy_markdown(source_path: Path) -> tuple[str, str, str]:
    """Copy markdown between Claude and OpenCode (same format)."""
    content = source_path.read_text().rstrip()
    frontmatter, _ = parse_frontmatter(content)
    name = source_path.stem
    description = frontmatter.get("description", "")
    return name, description, content


CONVERTERS = {
    ("claude", "gemini"): skill_to_command,
    ("claude", "opencode"): copy_markdown,
    ("gemini", "claude"): command_to_skill,
    ("gemini", "opencode"): command_to_skill,
    ("opencode", "claude"): copy_markdown,
    ("opencode", "gemini"): skill_to_command,
}


@click.command()
@click.option(
    "--from",
    "source",
    type=click.Choice(list(TOOLS.keys())),
    default="claude",
    help="Source tool",
)
@click.option(
    "--to",
    "target",
    type=click.Choice(list(TOOLS.keys())),
    default="gemini",
    help="Target tool",
)
@click.option(
    "--dry-run",
    "-n",
    is_flag=True,
    help="Preview changes without writing files",
)
def main(source: str, target: str, dry_run: bool) -> None:
    """Sync skills/commands between Claude Code, Gemini CLI, and OpenCode."""
    repo_root = get_repo_root()

    if source == target:
        console.print("[red]Error:[/red] --from and --to cannot be the same")
        raise SystemExit(1)

    converter = CONVERTERS.get((source, target))
    if not converter:
        console.print(f"[red]Error:[/red] No converter for {source} → {target}")
        raise SystemExit(1)

    source_cfg = TOOLS[source]
    target_cfg = TOOLS[target]

    source_dir = repo_root / source_cfg["dir"]
    target_dir = repo_root / target_cfg["dir"]
    source_ext = f"*{source_cfg['ext']}"
    target_ext = target_cfg["ext"]

    console.rule(f"[bold]{source_cfg['name']} → {target_cfg['name']}[/bold]")

    if not source_dir.exists():
        console.print(f"[red]Error:[/red] Source directory not found: {source_dir}")
        raise SystemExit(1)

    if not dry_run and not target_dir.exists():
        console.print(f"[yellow]Creating:[/yellow] {target_dir}")
        target_dir.mkdir(parents=True)

    source_files = list(source_dir.glob(source_ext))

    if not source_files:
        console.print("[yellow]No files found to sync[/yellow]")
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("Source")
    table.add_column("Target")
    table.add_column("Description", style="dim")

    synced = 0
    for source_path in sorted(source_files):
        name, description, output_content = converter(source_path)
        target_path = target_dir / f"{name}{target_ext}"

        table.add_row(source_path.name, target_path.name, description or "-")

        if not dry_run:
            target_path.write_text(output_content + "\n")
            synced += 1

    console.print(table)
    console.print()

    if dry_run:
        console.print(f"[yellow]Dry run:[/yellow] {len(source_files)} file(s) would be synced")
    else:
        console.print(f"[green]Synced:[/green] {synced} file(s)")


def claude_to_gemini() -> None:
    """Sync Claude skills to Gemini commands."""
    main(["--from", "claude", "--to", "gemini"])


def claude_to_opencode() -> None:
    """Sync Claude skills to OpenCode commands."""
    main(["--from", "claude", "--to", "opencode"])


def gemini_to_claude() -> None:
    """Sync Gemini commands to Claude skills."""
    main(["--from", "gemini", "--to", "claude"])


def gemini_to_opencode() -> None:
    """Sync Gemini commands to OpenCode commands."""
    main(["--from", "gemini", "--to", "opencode"])


def opencode_to_claude() -> None:
    """Sync OpenCode commands to Claude skills."""
    main(["--from", "opencode", "--to", "claude"])


def opencode_to_gemini() -> None:
    """Sync OpenCode commands to Gemini commands."""
    main(["--from", "opencode", "--to", "gemini"])


if __name__ == "__main__":
    main()
