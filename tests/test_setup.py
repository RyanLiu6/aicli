from pathlib import Path
from textwrap import dedent

from scripts.setup import convert_md_to_toml, find_skill_files, parse_frontmatter


def test_parse_frontmatter() -> None:
    content = dedent("""\
        ---
        name: test-skill
        description: A test skill
        ---

        # Body content
    """)
    frontmatter, body = parse_frontmatter(content)

    assert frontmatter["name"] == "test-skill"
    assert frontmatter["description"] == "A test skill"
    assert "# Body content" in body


def test_parse_frontmatter_no_frontmatter() -> None:
    content = "# Just a heading\n\nSome content."
    frontmatter, body = parse_frontmatter(content)

    assert frontmatter == {}
    assert body == content


def test_parse_frontmatter_empty_values() -> None:
    content = dedent("""\
        ---
        name: my-skill
        description:
        ---

        Body here.
    """)
    frontmatter, body = parse_frontmatter(content)

    assert frontmatter["name"] == "my-skill"
    assert frontmatter["description"] == ""
    assert "Body here." in body


def test_convert_md_to_toml(tmp_path: Path) -> None:
    skill_file = tmp_path / "SKILL.md"
    skill_file.write_text(
        dedent("""\
        ---
        name: test-skill
        description: A test skill for conversion
        ---

        # Test Skill

        Do the thing.
    """)
    )

    result = convert_md_to_toml(skill_file)

    assert 'description = "A test skill for conversion"' in result
    assert 'prompt = """' in result
    assert "# Test Skill" in result
    assert "Do the thing." in result
    assert result.rstrip().endswith('"""')


def test_convert_md_to_toml_no_frontmatter(tmp_path: Path) -> None:
    skill_file = tmp_path / "SKILL.md"
    skill_file.write_text("# Just content\n\nNo frontmatter here.")

    result = convert_md_to_toml(skill_file)

    assert 'description = "' not in result
    assert 'prompt = """' in result
    assert "# Just content" in result


def test_find_skill_files(tmp_path: Path) -> None:
    skill_a = tmp_path / "skill-a"
    skill_a.mkdir()
    (skill_a / "SKILL.md").write_text("---\nname: skill-a\n---\n# A")

    skill_b = tmp_path / "skill-b"
    skill_b.mkdir()
    (skill_b / "SKILL.md").write_text("---\nname: skill-b\n---\n# B")

    (tmp_path / "not-a-skill").mkdir()

    skills = find_skill_files(tmp_path)
    names = sorted([name for name, _ in skills])

    assert names == ["skill-a", "skill-b"]


def test_find_skill_files_ignores_readme(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# Skills readme")
    skill = tmp_path / "my-skill"
    skill.mkdir()
    (skill / "SKILL.md").write_text("---\nname: my-skill\n---\n# Skill")

    skills = find_skill_files(tmp_path)
    names = [name for name, _ in skills]

    assert "README" not in names
    assert "my-skill" in names
