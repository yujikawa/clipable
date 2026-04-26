# Changelog

## [0.5.0] - 2026-04-26

### Changed
- Replaced `pyperclip` dependency with a built-in `clipboard` module using subprocess only (no `ctypes`)
- Supports macOS (`pbcopy`/`pbpaste`), Linux (`xclip`/`xsel`/`wl-clipboard`), Windows and WSL2 (`clip.exe`/`powershell.exe`)

## [0.4.0] - 2026-04-26

### Changed
- Removed `pandas` dependency: CSV/TSV parsing now uses the stdlib `csv` module, significantly reducing startup time
- Removed `pytablewriter` dependency: Markdown table generation is now done with a pure-Python implementation
- Lazy-load `converter` and `watcher` modules inside their respective command functions so that `--version` and `--help` no longer trigger heavy imports

## [0.3.0]

### Changed
- Migrated CLI from `argparse` to `typer`
- Split logic into `converter.py` and `watcher.py` modules
- Added `watch` subcommand for continuous clipboard monitoring

## [0.2.0]

### Changed
- Replaced `pd.read_clipboard()` with `pyperclip.paste()` to avoid redundant clipboard reads
- Added `rich` output with panel display and colored status messages
