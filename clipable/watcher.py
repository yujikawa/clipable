from __future__ import annotations

import time

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from . import clipboard
from .converter import convert_to_markdown, detect_format

console = Console()


def watch(linesep: str = "<br>", interval: float = 0.5) -> None:
    """Watch the clipboard and auto-convert spreadsheet data to Markdown.

    Args:
        linesep: Replacement string for in-cell line breaks.
        interval: Polling interval in seconds.
    """
    console.print(
        Panel(
            Text.assemble(
                ("clipable watch", "bold cyan"),
                " — watching clipboard\n",
                ("Copy cells from a spreadsheet and they will be auto-converted to Markdown.\n", "dim"),
                ("Ctrl+C", "bold yellow"),
                (" to stop", "dim"),
            ),
            border_style="cyan",
        )
    )

    last_text = clipboard.paste()
    # Track our own Markdown output to avoid re-converting it
    converted_outputs: set[str] = set()

    try:
        while True:
            current = clipboard.paste()

            if current != last_text and current not in converted_outputs:
                fmt = detect_format(current)
                if fmt is not None:
                    try:
                        md = convert_to_markdown(current, fmt=fmt, linesep=linesep)
                        clipboard.copy(md)
                        converted_outputs.add(md)

                        console.print(
                            f"\n[bold green]✓[/bold green] Detected [green]{fmt.upper()}[/green] — converted to Markdown and updated clipboard"
                        )
                        console.print(Panel(md, border_style="green", title="Markdown"))
                    except Exception as e:
                        console.print(
                            f"[bold red]✗[/bold red] Conversion failed: [red]{e}[/red]"
                        )

            last_text = current
            time.sleep(interval)

    except KeyboardInterrupt:
        console.print("\n[yellow]Stopped watching.[/yellow]")
