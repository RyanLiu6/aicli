from invoke.context import Context
from invoke.tasks import task


@task
def test(ctx: Context, verbose: bool = False) -> None:
    cmd = "uv run pytest"
    if verbose:
        cmd += " -v"
    ctx.run(cmd, pty=True)


@task
def format(ctx: Context, check: bool = False) -> None:  # noqa: A001
    cmd = "uv run ruff format"
    if check:
        cmd += " --check"
    ctx.run(cmd, pty=True)


@task
def lint(ctx: Context, fix: bool = False) -> None:
    cmd = "uv run ruff check"
    if fix:
        cmd += " --fix"
    ctx.run(cmd, pty=True)


@task
def typecheck(ctx: Context) -> None:
    ctx.run("uv run mypy scripts/ tasks.py tests/", pty=True)
