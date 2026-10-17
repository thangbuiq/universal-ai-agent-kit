"""uak - sync one base kit into Claude Code, OpenCode, Codex and GitHub Copilot CLI."""

from __future__ import annotations

import sys
from enum import Enum
from pathlib import Path
from typing import Annotated

import typer
from loguru import logger
from rich.console import Console
from rich.table import Table

from . import __version__
from .kit import DEFAULT_KIT, Kit
from .targets import SyncError, Writer, build_targets

BANNER = r"""
  _   _  _     _  __
 | | | |/ \   | |/ /
 | | | / _ \  | ' /
 | |_| / ___ \ | . \
  \___/_/   \_\|_|\_\   universal-ai-agent-kit v{v}
"""

console = Console(stderr=True)
app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="Sync skills, commands, MCP servers and instructions into every coding CLI.",
)


class Target(str, Enum):
    claude = "claude"
    opencode = "opencode"
    codex = "codex"
    copilot = "copilot"


class Scope(str, Enum):
    user = "user"
    project = "project"


class Kind(str, Enum):
    skills = "skills"
    commands = "commands"
    mcp = "mcp"
    instructions = "instructions"


def _setup_logging(verbose: bool) -> None:
    logger.remove()
    logger.add(
        sys.stderr,
        level="DEBUG" if verbose else "INFO",
        colorize=True,
        format="<green>{time:HH:mm:ss}</green> <level>{level: <7}</level> {message}",
    )


def _banner() -> None:
    console.print(f"[bold cyan]{BANNER.format(v=__version__)}[/]")


@app.callback()
def main(
    ctx: typer.Context,
    kit: Annotated[
        Path | None, typer.Option(envvar="UAK_KIT", help="Custom kit directory.", exists=True, file_okay=False)
    ] = None,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Debug logging.")] = False,
    version: Annotated[bool, typer.Option("--version", help="Show version and exit.")] = False,
) -> None:
    if version:
        typer.echo(f"uak {__version__}")
        raise typer.Exit()
    _setup_logging(verbose)
    ctx.obj = Kit((kit or DEFAULT_KIT).resolve())
    logger.debug("kit: {}", ctx.obj.root)


@app.command("list")
def list_kit(ctx: typer.Context) -> None:
    """Show what the kit contains and which CLIs it can sync to."""
    kit: Kit = ctx.obj
    t = Table(title=f"kit: {kit.root}", title_justify="left", header_style="bold cyan")
    t.add_column("type"), t.add_column("name"), t.add_column("description", overflow="fold")
    for s in kit.skills:
        t.add_row("skill", s.name, Kit.describe(s))
    for c in kit.commands:
        t.add_row("command", f"/{c.stem}", "")
    for n, s in kit.mcp.items():
        t.add_row(f"mcp/{s['transport']}", n, s.get("description", ""))
    Console().print(t)
    Console().print("targets: " + ", ".join(build_targets(Path.cwd())))


@app.command()
def sync(
    ctx: typer.Context,
    target: Annotated[list[Target] | None, typer.Option("--target", "-t", help="Repeatable. Default: all.")] = None,
    scope: Annotated[Scope, typer.Option("--scope", "-s", help="user = global, project = this repo.")] = Scope.user,
    only: Annotated[list[Kind] | None, typer.Option("--only", help="Repeatable. Default: everything.")] = None,
    project_dir: Annotated[Path, typer.Option(help="Project root for --scope project.")] = Path("."),
    dry_run: Annotated[bool, typer.Option("--dry-run", "-n", help="Show changes without writing.")] = False,
    overwrite: Annotated[
        bool,
        typer.Option(
            "--overwrite", help="Replace existing skills, commands, MCP servers and instructions without asking."
        ),
    ] = False,
) -> None:
    """Install the kit into the selected coding CLIs (idempotent)."""
    _banner()
    kit: Kit = ctx.obj
    targets = build_targets(project_dir.resolve())
    names = [t.value for t in target] if target else list(targets)
    kinds = {k.value for k in only} if only else {k.value for k in Kind}
    ask = (lambda msg: typer.confirm(msg, default=False, err=True)) if sys.stdin.isatty() else None
    w = Writer(dry_run, overwrite, ask)
    failed = 0
    for n in names:
        t = targets[n]
        with logger.contextualize(target=n):
            logger.opt(colors=True).info(
                "<bold>{}</bold> ({} scope){}", t.label, scope.value, " [dry-run]" if dry_run else ""
            )
            try:
                t.sync(kit, scope.value, kinds, w)
            except SyncError as e:
                failed += 1
                logger.error("{}: {}", t.label, e)
    if failed:
        logger.error("{} target(s) failed", failed)
        raise typer.Exit(1)
    logger.success("dry run complete, nothing written" if dry_run else "synced {} target(s)", len(names))


if __name__ == "__main__":
    app()
