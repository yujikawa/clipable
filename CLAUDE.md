# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Clipable は、スプレッドシート（Excel / Google Sheets）からコピーしたデータをMarkdownテーブルに変換するCLIツール。
- **one-shot**: `clipable` — クリップボードを即変換してMarkdownで上書き
- **watch**: `clipable watch` — クリップボードを監視し、スプレッドシートデータを検知したら自動変換

## Commands

```bash
# 依存インストール
uv sync

# テスト実行
uv run pytest

# 単一テスト
uv run pytest tests/test_clipable.py::TestDetectFormat::test_tsv

# CLIを直接実行（開発中）
uv run clipable
uv run clipable watch

# ロックファイル更新
uv lock
```

## Architecture

```
clipable/
  __init__.py   # __version__
  cli.py        # typer app。コマンド定義（main / watch）
  converter.py  # フォーマット自動検出 + Markdown変換ロジック
  watcher.py    # クリップボードポーリング監視デーモン
tests/
  test_clipable.py
```

**データフロー（one-shot）:**
1. `pyperclip.paste()` でクリップボード取得
2. `detect_format()` でTSV/CSV/Noneを判定（タブ・カンマの行間一貫性でヒューリスティック判定）
3. `pandas.read_csv()` でDataFrame化（sep引数でフォーマット対応）
4. セル内改行を `linesep` 文字列に置換、NaNを空文字に
5. `pytablewriter.MarkdownTableWriter` でMarkdown生成
6. `pyperclip.copy()` でクリップボードに書き戻し

**watch モード:**
- 0.5秒ポーリングでクリップボードを監視
- 自分が書き込んだMarkdownは `converted_outputs` セットで追跡し再変換を防止
- `rich.Panel` で変換結果を表示

**依存関係:** `pandas` (CSV/TSV読み込み)、`pytablewriter` (Markdown生成)、`pyperclip` (クリップボードI/O)、`typer` + `rich` (CLI/UI)
