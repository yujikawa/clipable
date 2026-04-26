from __future__ import annotations

import csv
import io
import re


def detect_format(text: str) -> str | None:
    """Detect the format of clipboard text.

    Returns:
        'tsv', 'csv', or None if not recognized as tabular data.
    """
    lines = [l for l in text.strip().splitlines() if l.strip()]
    if len(lines) < 2:
        return None

    tab_counts = [line.count("\t") for line in lines]
    if tab_counts[0] > 0 and max(tab_counts) - min(tab_counts) <= 1:
        return "tsv"

    comma_counts = [line.count(",") for line in lines]
    if comma_counts[0] > 0 and max(comma_counts) - min(comma_counts) <= 1:
        return "csv"

    return None


def _parse(text: str, delimiter: str) -> tuple[list[str], list[list[str]]]:
    reader = csv.reader(io.StringIO(text), delimiter=delimiter)
    rows = list(reader)
    if not rows:
        raise ValueError("No data found")
    return rows[0], rows[1:]


def _replace_linesep(value: str, linesep: str) -> str:
    return re.sub(r"\r\n|\r|\n", linesep, value)


def _to_markdown(headers: list[str], rows: list[list[str]], linesep: str) -> str:
    processed = [
        [_replace_linesep(cell, linesep) for cell in row]
        for row in rows
    ]
    col_widths = [
        max(len(h), max((len(r[i]) for r in processed if i < len(r)), default=0))
        for i, h in enumerate(headers)
    ]

    def fmt_row(cells: list[str]) -> str:
        padded = cells + [""] * (len(col_widths) - len(cells))
        return "| " + " | ".join(c.ljust(w) for c, w in zip(padded, col_widths)) + " |"

    sep = "| " + " | ".join("-" * w for w in col_widths) + " |"
    return "\n".join([fmt_row(headers), sep] + [fmt_row(r) for r in processed])


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
        headers, rows = _parse(text, "\t")
    elif resolved_fmt == "csv":
        headers, rows = _parse(text, ",")
    else:
        # Fallback: split on any whitespace run
        lines = [l for l in text.strip().splitlines() if l.strip()]
        headers = lines[0].split()
        rows = [l.split() for l in lines[1:]]

    return _to_markdown(headers, rows, linesep)
