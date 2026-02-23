from __future__ import annotations

import re

from bs4 import BeautifulSoup


def parse_albo_detail_page(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text("\n", strip=True)

    def find_by_label(label: str) -> str | None:
        el = soup.find(string=re.compile(label, re.IGNORECASE))
        if not el:
            return None
        parent_text = el.parent.get_text(" ", strip=True)
        return re.sub(fr"{label}\s*:?", "", parent_text, flags=re.IGNORECASE).strip() or None

    return {
        "indirizzo": find_by_label("Indirizzo"),
        "cap": find_by_label("CAP"),
        "comune": find_by_label("Comune"),
        "provincia": find_by_label("Provincia"),
        "pec": find_by_label("PEC") or _extract_email(text, pec_only=True),
        "email_generica": find_by_label("Email") or _extract_email(text),
        "telefono": find_by_label("Telefono"),
    }


def _extract_email(text: str, pec_only: bool = False) -> str | None:
    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    emails = re.findall(pattern, text)
    if pec_only:
        emails = [email for email in emails if "pec" in email.lower()]
    return emails[0] if emails else None
