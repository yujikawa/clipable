from __future__ import annotations

from typing import Annotated, Optional

import pyperclip
import typer
from rich.console import Console
from rich.panel import Panel

from . import __version__

app = typer.Typer(
    name="clipable",
    help="Convert clipboard spreadsheet data to a Markdown table.",
    add_completion=False,
)
console = Console()


def _version_callback(value: bool) -> None:
    if value:
        console.print(f"clipable [bold cyan]{__version__}[/bold cyan]")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    fmt: Annotated[
        Optional[str],
        typer.Option("-f", "--format", help="Format override: csv, tsv (auto-detected if omitted)"),
    ] = None,
    linesep: Annotated[
        str,
        typer.Option("-l", "--linesep", help="Replacement string for in-cell line breaks"),
    ] = "<br>",
    version: Annotated[
        Optional[bool],
        typer.Option("--version", callback=_version_callback, is_eager=True, help="Show version and exit"),
    ] = None,
) -> None:
    """Convert clipboard spreadsheet data to a Markdown table and write it back to the clipboard."""
    if ctx.invoked_subcommand is not None:
        return

    from .converter import convert_to_markdown, detect_format  # noqa: PLC0415

    text = pyperclip.paste()

    if not text.strip():
        console.print("[bold red]✗[/bold red] Clipboard is empty.")
        raise typer.Exit(1)

    resolved_fmt = fmt or detect_format(text)
    if resolved_fmt is None and fmt is None:
        console.print(
            "[bold yellow]⚠[/bold yellow]  Could not detect table format. Falling back to whitespace-separated."
        )

    try:
        md = convert_to_markdown(text, fmt=fmt, linesep=linesep)
    except Exception as e:
        console.print(f"[bold red]✗[/bold red] Conversion failed: [red]{e}[/red]")
        raise typer.Exit(1)

    console.print(Panel(md, border_style="green", title="Markdown"))
    pyperclip.copy(md)
    console.print("[bold green]✓[/bold green] Clipboard updated. Ready to paste.")


@app.command()
def watch(
    linesep: Annotated[
        str,
        typer.Option("-l", "--linesep", help="Replacement string for in-cell line breaks"),
    ] = "<br>",
    interval: Annotated[
        float,
        typer.Option("-i", "--interval", help="Polling interval in seconds"),
    ] = 0.5,
) -> None:
    """Watch the clipboard and auto-convert spreadsheet data to Markdown.

    Once running, simply copy cells from a spreadsheet — the clipboard will
    be converted to Markdown automatically, ready to paste.
    """
    from .watcher import watch as _watch  # noqa: PLC0415

    _watch(linesep=linesep, interval=interval)
