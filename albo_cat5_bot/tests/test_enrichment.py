from pathlib import Path

from src.sources.enrichment.ufficiocamerale.parser import parse_ufficiocamerale_page


def test_parse_ufficiocamerale_page_fixture():
    html = Path("tests/fixtures/ufficiocamerale_page.html").read_text(encoding="utf-8")
    out = parse_ufficiocamerale_page(html)
    assert out["piva"] == "01234567890"
    assert out["rea"] == "NA-123456"
