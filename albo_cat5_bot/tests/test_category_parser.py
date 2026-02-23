from src.utils.category_parser import extract_detail_id_from_onclick, parse_categorie


def test_parse_categorie_mixed_tokens():
    parsed = parse_categorie("2-bis , R.Met F, 4 F")
    assert [p.model_dump() for p in parsed] == [
        {"cat": "2-bis", "classe": None},
        {"cat": "R.Met", "classe": "F"},
        {"cat": "4", "classe": "F"},
    ]


def test_parse_categorie_simple_cat5():
    parsed = parse_categorie("5 F")
    assert [p.model_dump() for p in parsed] == [{"cat": "5", "classe": "F"}]


def test_parse_categorie_multiple():
    parsed = parse_categorie("5 A, 4 F, 2-bis")
    assert [p.model_dump() for p in parsed] == [
        {"cat": "5", "classe": "A"},
        {"cat": "4", "classe": "F"},
        {"cat": "2-bis", "classe": None},
    ]


def test_extract_detail_id_from_onclick():
    assert extract_detail_id_from_onclick("ExecImpresaDettaglio('271815')") == "271815"
