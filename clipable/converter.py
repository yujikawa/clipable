from __future__ import annotations

import io
import re

import pandas as pd
import pytablewriter


def detect_format(text: str) -> str | None:
    """Detect the format of clipboard text.

    Returns:
        'tsv', 'csv', or None if not recognized as tabular data.
    """
    lines = [l for l in text.strip().splitlines() if l.strip()]
    if len(lines) < 2:
        return None

    # TSV: tabs appear consistently across lines
    tab_counts = [line.count("\t") for line in lines]
    if tab_counts[0] > 0 and max(tab_counts) - min(tab_counts) <= 1:
        return "tsv"

    # CSV: commas appear consistently across lines
    comma_counts = [line.count(",") for line in lines]
    if comma_counts[0] > 0 and max(comma_counts) - min(comma_counts) <= 1:
        return "csv"

    return None


def convert_to_markdown(
    text: str,
    fmt: str | None = None,
    linesep: str = "<br>",
) -> str:
    """Convert text to a Markdown table.

    Args:
        text: Input text to convert.
        fmt: Format hint ('tsv', 'csv', or None for auto-detection).
        linesep: Replacement string for in-cell line breaks.

    Returns:
        Markdown table string.
    """
    resolved_fmt = fmt or detect_format(text)

    if resolved_fmt == "tsv":
        df = pd.read_csv(io.StringIO(text), sep="\t")
    elif resolved_fmt == "csv":
        df = pd.read_csv(io.StringIO(text))
    else:
        # Fallback: whitespace-separated
        df = pd.read_csv(io.StringIO(text), sep=r"\s+", engine="python")

    # Replace in-cell line breaks
    df = df.replace(r"\n|\r\n|\r", linesep, regex=True)
    df = df.fillna("")

    writer = pytablewriter.MarkdownTableWriter()
    writer.from_dataframe(df)
    writer.margin = 1
    return writer.dumps()
