from __future__ import annotations

from bs4 import BeautifulSoup

from src.utils.category_parser import extract_detail_id_from_onclick


def parse_albo_list_page(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    rows = soup.select("table tbody tr")
    companies: list[dict] = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 5:
            continue

        detail_button = row.select_one("a[onclick], button[onclick]")
        onclick = detail_button.get("onclick") if detail_button else ""

        companies.append(
            {
                "numero_iscrizione": cols[0].get_text(strip=True),
                "ragione_sociale": cols[1].get_text(" ", strip=True),
                "provincia": cols[2].get_text(strip=True),
                "stato_iscrizione": cols[3].get_text(strip=True),
                "categorie_raw": cols[4].get_text(" ", strip=True),
                "detail_id": extract_detail_id_from_onclick(onclick),
            }
        )
    return companies
