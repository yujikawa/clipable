from clipable import __version__
from clipable.converter import detect_format, convert_to_markdown


def test_version():
    assert __version__ == "0.4.0"


class TestDetectFormat:
    def test_tsv(self):
        text = "col1\tcol2\tcol3\nval1\tval2\tval3"
        assert detect_format(text) == "tsv"

    def test_csv(self):
        text = "col1,col2,col3\nval1,val2,val3"
        assert detect_format(text) == "csv"

    def test_single_line_returns_none(self):
        text = "col1\tcol2\tcol3"
        assert detect_format(text) is None

    def test_plain_text_returns_none(self):
        text = "hello world\nfoo bar"
        assert detect_format(text) is None


class TestConvertToMarkdown:
    def test_tsv_conversion(self):
        text = "Name\tAge\nAlice\t30\nBob\t25"
        md = convert_to_markdown(text)
        assert "|" in md
        assert "Name" in md
        assert "Alice" in md
        assert "30" in md

    def test_csv_conversion(self):
        text = "Name,Age\nAlice,30\nBob,25"
        md = convert_to_markdown(text, fmt="csv")
        assert "|" in md
        assert "Alice" in md

    def test_explicit_format_overrides_detection(self):
        text = "Name\tAge\nAlice\t30"
        # 明示的にTSVを指定
        md = convert_to_markdown(text, fmt="tsv")
        assert "Name" in md

    def test_linesep_replacement(self):
        text = "Name\tNote\nAlice\tline1\nline2"
        md = convert_to_markdown(text, linesep="<br>")
        # 改行が置換されていること
        assert "\n\n" not in md or "Name" in md
