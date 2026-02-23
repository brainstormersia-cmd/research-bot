from pathlib import Path

from src.sources.albo.parser_detail import parse_albo_detail_page
from src.sources.albo.parser_list import parse_albo_list_page


def test_parse_albo_list_page_fixture():
    html = Path("tests/fixtures/albo_list_page.html").read_text(encoding="utf-8")
    out = parse_albo_list_page(html)
    assert len(out) == 1
    assert out[0]["numero_iscrizione"] == "NA12345"
    assert out[0]["detail_id"] == "271815"


def test_parse_albo_detail_page_fixture():
    html = Path("tests/fixtures/albo_detail_page.html").read_text(encoding="utf-8")
    out = parse_albo_detail_page(html)
    assert out["pec"] == "info@pecazienda.it"
    assert out["telefono"] == "0811234567"
