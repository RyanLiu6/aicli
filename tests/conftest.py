from pathlib import Path

import pytest


@pytest.fixture
def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


@pytest.fixture
def skills_dir(repo_root: Path) -> Path:
    return repo_root / "skills"


@pytest.fixture
def memory_dir(repo_root: Path) -> Path:
    return repo_root / "memory"


@pytest.fixture
def modules_dir(repo_root: Path) -> Path:
    return repo_root / "modules"
