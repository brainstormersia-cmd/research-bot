from __future__ import annotations

from bs4 import BeautifulSoup


def parse_ufficiocamerale_page(html: str) -> dict:
    """Best-effort parser for public company profile pages.

    If structure is unavailable or blocked, caller should log and skip.
    """

    soup = BeautifulSoup(html, "lxml")

    def first_text(selectors: list[str]) -> str | None:
        for selector in selectors:
            node = soup.select_one(selector)
            if node:
                value = node.get_text(" ", strip=True)
                if value:
                    return value
        return None

    return {
        "piva": first_text(["[data-field='piva']", ".piva", "#piva"]),
        "codice_fiscale": first_text(["[data-field='codice-fiscale']", ".codice-fiscale", "#codice-fiscale"]),
        "rea": first_text(["[data-field='rea']", ".rea", "#rea"]),
        "fatturato": first_text(["[data-field='fatturato']", ".fatturato", "#fatturato"]),
        "dipendenti": first_text(["[data-field='dipendenti']", ".dipendenti", "#dipendenti"]),
        "sito_web": first_text(["a.website", "[data-field='sito']", "a[href^='http']"]),
    }
