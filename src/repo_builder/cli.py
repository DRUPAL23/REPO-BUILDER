"""Typer command-line interface for repo-builder."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from repo_builder import __version__
from repo_builder.config import Settings
from repo_builder.parser import parse_project_spec

app = typer.Typer(
    name="repo-builder",
    help="Generate application repositories from natural-language project briefs.",
    no_args_is_help=True,
    add_completion=False,
)
console = Console()


@app.callback()
def main() -> None:
    """Universal AI-driven GitHub repository builder."""


@app.command()
def version() -> None:
    """Print the installed repo-builder version."""
    console.print(f"repo-builder {__version__}")


@app.command("config")
def show_config() -> None:
    """Show effective configuration without exposing credentials."""
    settings = Settings.load()
    table = Table(title="repo-builder configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value")
    table.add_row("LLM provider", settings.llm_provider)
    table.add_row("LLM model", settings.llm_model)
    table.add_row("LLM credentials", "configured" if settings.has_llm_credentials() else "not configured")
    table.add_row("GitHub owner", settings.github_owner or "not configured")
    table.add_row("GitHub token", "configured" if settings.github_token else "not configured")
    table.add_row("Private repositories", str(settings.github_private).lower())
    table.add_row("Validate Python", str(settings.validate_python).lower())
    table.add_row("Validate JavaScript", str(settings.validate_js).lower())
    console.print(table)


@app.command("parse")
def parse_brief(
    prompt: Annotated[str, typer.Argument(help="Natural-language description of the project.")],
    name: Annotated[str | None, typer.Option("--name", "-n", help="Override the inferred project name.")] = None,
    output: Annotated[Path | None, typer.Option("--output", "-o", help="Write the normalized spec to this JSON file.")] = None,
) -> None:
    """Parse a project brief into a validated, normalized specification."""
    try:
        spec = parse_project_spec(prompt, name=name)
    except Exception as exc:
        console.print(f"[red]Unable to parse project brief:[/red] {exc}")
        raise typer.Exit(code=2) from exc

    rendered = json.dumps(spec.model_dump(), indent=2, ensure_ascii=False)
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered + "\n", encoding="utf-8")
        console.print(f"[green]Project specification saved:[/green] {output}")
    else:
        console.print(rendered)
