# clipable

[![PyPI version](https://img.shields.io/pypi/v/clipable?color=blue)](https://pypi.org/project/clipable/)
[![Python](https://img.shields.io/pypi/pyversions/clipable)](https://pypi.org/project/clipable/)
[![Downloads](https://pepy.tech/badge/clipable)](https://pepy.tech/project/clipable)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/yujikawa/clipable/publish.yml?label=release)](https://github.com/yujikawa/clipable/actions/workflows/publish.yml)

**clipable** converts spreadsheet data from your clipboard into a Markdown table — instantly.

Copy cells from Excel, Google Sheets, or any CSV/TSV source, run `clipable`, and the Markdown table is already in your clipboard, ready to paste into any document or wiki.

## Why clipable?

Manually converting spreadsheet data to Markdown tables is tedious. clipable eliminates that entirely.

With **watch mode**, you don't even run a command — just copy cells from a spreadsheet and the clipboard is automatically converted. The flow becomes simply: **copy → paste**.

## Install

```
pip install clipable
```

With uv:

```
uv tool install clipable
```

## Usage

### Watch mode (recommended)

Start the watcher once in a terminal. After that, every time you copy cells from a spreadsheet the clipboard is silently converted to Markdown in the background.

```
clipable watch
```

```
╭─────────────────────────────────────────────────────╮
│ clipable watch — watching clipboard                 │
│ Copy cells from a spreadsheet and they will be      │
│ auto-converted to Markdown.                         │
│ Ctrl+C to stop                                      │
╰─────────────────────────────────────────────────────╯

✓ Detected TSV — converted to Markdown and updated clipboard
╭─ Markdown ──────────────────────────────────────────╮
│ | Name  | Age | Department  |                       │
│ | ----- | --- | ----------- |                       │
│ | Alice | 30  | Engineering |                       │
│ | Bob   | 25  | Design      |                       │
╰─────────────────────────────────────────────────────╯
```

### One-shot conversion

Copy cells from a spreadsheet, then run:

```
clipable
```

The clipboard is replaced with the Markdown table and printed to the terminal for confirmation.

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `-f`, `--format` | auto | Force format: `tsv` or `csv` |
| `-l`, `--linesep` | `<br>` | Replacement string for in-cell line breaks |
| `--version` | | Show version and exit |

For `clipable watch`:

| Option | Default | Description |
|--------|---------|-------------|
| `-l`, `--linesep` | `<br>` | Replacement string for in-cell line breaks |
| `-i`, `--interval` | `0.5` | Clipboard polling interval in seconds |

### Format auto-detection

clipable automatically detects whether your clipboard contains TSV (tab-separated) or CSV (comma-separated) data. Use `-f` to override when needed.

### Example output

Input (copied from Google Sheets):

```
Name	Age	Department
Alice	30	Engineering
Bob	25	Design
```

Output (Markdown, written back to clipboard):

```markdown
| Name  | Age | Department  |
| ----- | --- | ----------- |
| Alice | 30  | Engineering |
| Bob   | 25  | Design      |
```

## License

MIT
