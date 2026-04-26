from clipable import __version__
from clipable.converter import detect_format, convert_to_markdown


def test_version():
    assert __version__ == "0.5.0"


class TestDetectFormat:
    def test_tsv(self):
        assert detect_format("col1\tcol2\tcol3\nval1\tval2\tval3") == "tsv"

    def test_csv(self):
        assert detect_format("col1,col2,col3\nval1,val2,val3") == "csv"

    def test_single_line_returns_none(self):
        assert detect_format("col1\tcol2\tcol3") is None

    def test_plain_text_returns_none(self):
        assert detect_format("hello world\nfoo bar") is None

    def test_empty_returns_none(self):
        assert detect_format("") is None

    def test_whitespace_only_returns_none(self):
        assert detect_format("   \n  ") is None

    def test_inconsistent_tab_counts_returns_none(self):
        # タブ数の差が2以上の場合はTSVと判定しない
        assert detect_format("a\tb\tc\nd") is None

    def test_tsv_takes_priority_over_csv(self):
        # タブとカンマ両方あればTSV優先
        assert detect_format("a,b\tc\nd,e\tf") == "tsv"


class TestConvertToMarkdown:
    def test_tsv_output_structure(self):
        text = "Name\tAge\nAlice\t30\nBob\t25"
        md = convert_to_markdown(text)
        lines = md.splitlines()
        assert len(lines) == 4  # ヘッダー + 区切り + データ2行
        assert lines[0].startswith("|")
        assert "---" in lines[1]
        assert "Alice" in lines[2]
        assert "Bob" in lines[3]

    def test_tsv_values_correct(self):
        text = "Name\tAge\nAlice\t30"
        md = convert_to_markdown(text)
        assert "Name" in md
        assert "Age" in md
        assert "Alice" in md
        assert "30" in md

    def test_csv_conversion(self):
        text = "Name,Age\nAlice,30\nBob,25"
        md = convert_to_markdown(text, fmt="csv")
        lines = md.splitlines()
        assert len(lines) == 4
        assert "Alice" in md
        assert "30" in md

    def test_explicit_tsv_overrides_detection(self):
        text = "Name\tAge\nAlice\t30"
        md = convert_to_markdown(text, fmt="tsv")
        assert "Name" in md
        assert "Age" in md
        assert "Alice" in md

    def test_linesep_replacement(self):
        # CSVクォートでセル内改行を表現
        text = 'Name\tNote\nAlice\t"line1\nline2"'
        md = convert_to_markdown(text, linesep="<br>")
        assert "<br>" in md
        assert "line1" in md
        assert "line2" in md
        # 生の改行がセル内に残っていないこと
        assert "line1\nline2" not in md

    def test_custom_linesep(self):
        text = 'A\tB\n"x\ny"\tz'
        md = convert_to_markdown(text, linesep="[BR]")
        assert "[BR]" in md

    def test_empty_cells(self):
        text = "A\tB\tC\n1\t\t3\n4\t5\t"
        md = convert_to_markdown(text)
        lines = md.splitlines()
        assert len(lines) == 4
        assert "1" in md
        assert "3" in md

    def test_fallback_whitespace_separated(self):
        text = "col1 col2\nval1 val2"
        md = convert_to_markdown(text, fmt=None)
        assert "col1" in md
        assert "val1" in md

    def test_unknown_format_falls_back_to_whitespace(self):
        text = "A\tB\n1\t2"
        # 未知フォーマット指定 → whitespaceフォールバック
        md = convert_to_markdown(text, fmt="xml")
        assert "A" in md or "1" in md


class TestCLI:
    def setup_method(self):
        from typer.testing import CliRunner
        from clipable.cli import app
        self.runner = CliRunner()
        self.app = app

    def _mock_clipboard(self, mocker, paste_value: str = ""):
        mocker.patch("clipable.clipboard.paste", return_value=paste_value)
        mocker.patch("clipable.clipboard.copy")

    def test_version_flag(self):
        result = self.runner.invoke(self.app, ["--version"])
        assert result.exit_code == 0
        assert "0.5.0" in result.output

    def test_help_flag(self):
        result = self.runner.invoke(self.app, ["--help"])
        assert result.exit_code == 0
        assert "clipboard" in result.output.lower()

    def test_empty_clipboard_exits_with_error(self, mocker):
        self._mock_clipboard(mocker, paste_value="")
        result = self.runner.invoke(self.app, [])
        assert result.exit_code == 1

    def test_whitespace_only_clipboard_exits_with_error(self, mocker):
        self._mock_clipboard(mocker, paste_value="   \n  ")
        result = self.runner.invoke(self.app, [])
        assert result.exit_code == 1

    def test_tsv_converts_and_copies(self, mocker):
        tsv = "Name\tAge\nAlice\t30\nBob\t25"
        mocker.patch("clipable.clipboard.paste", return_value=tsv)
        copy_mock = mocker.patch("clipable.clipboard.copy")

        result = self.runner.invoke(self.app, [])

        assert result.exit_code == 0
        copy_mock.assert_called_once()
        md = copy_mock.call_args[0][0]
        assert "Name" in md
        assert "Alice" in md
        assert "30" in md

    def test_csv_format_flag(self, mocker):
        mocker.patch("clipable.clipboard.paste", return_value="Name,Age\nAlice,30")
        copy_mock = mocker.patch("clipable.clipboard.copy")

        result = self.runner.invoke(self.app, ["-f", "csv"])

        assert result.exit_code == 0
        md = copy_mock.call_args[0][0]
        assert "Name" in md
        assert "Alice" in md

    def test_custom_linesep_option(self, mocker):
        mocker.patch("clipable.clipboard.paste", return_value='Name\tNote\nAlice\t"a\nb"')
        copy_mock = mocker.patch("clipable.clipboard.copy")

        result = self.runner.invoke(self.app, ["-l", "BR"])

        assert result.exit_code == 0
        md = copy_mock.call_args[0][0]
        assert "BR" in md

    def test_output_contains_success_message(self, mocker):
        self._mock_clipboard(mocker, paste_value="A\tB\n1\t2")

        result = self.runner.invoke(self.app, [])

        assert result.exit_code == 0
        assert "Clipboard updated" in result.output
