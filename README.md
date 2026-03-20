# clipable

[![Downloads](https://pepy.tech/badge/clipable)](https://pepy.tech/project/clipable)

Convert spreadsheet clipboard data (Excel, Google Sheets, CSV, TSV) to a Markdown table instantly.

## Install

```
pip install clipable
```

Or with uv:

```
uv tool install clipable
```

## Usage

### Watch mode (recommended)

Start the watcher once and forget about it. Every time you copy cells from a spreadsheet, the clipboard is automatically converted to Markdown — just paste.

```
clipable watch
```

### One-shot conversion

Copy cells from a spreadsheet, then run:

```
clipable
```

The clipboard is replaced with a Markdown table. Paste it wherever you need.

#### Format options

| Flag | Description |
|------|-------------|
| `-f tsv` | Force TSV parsing |
| `-f csv` | Force CSV parsing |
| `-l <sep>` | In-cell line break replacement (default: `<br>`) |

Format is auto-detected if `-f` is omitted.

## License

MIT
