import re
from typing import Optional

from pydantic import BaseModel


class ParsedCategory(BaseModel):
    cat: str
    classe: Optional[str] = None


_CLASS_RE = re.compile(r"^(?P<cat>[A-Za-z0-9.\-]+)\s+(?P<classe>[A-F])$", re.IGNORECASE)


def _normalize_token(token: str) -> str:
    token = token.strip()
    token = re.sub(r"\s+", " ", token)
    return token


def parse_categorie(raw: str) -> list[ParsedCategory]:
    """Parse category text like '2-bis , R.Met F, 4 F, 5 C' into typed objects."""
    if not raw:
        return []

    categories: list[ParsedCategory] = []
    for token in raw.split(","):
        normalized = _normalize_token(token)
        if not normalized:
            continue

        match = _CLASS_RE.match(normalized)
        if match:
            categories.append(
                ParsedCategory(
                    cat=match.group("cat"),
                    classe=match.group("classe").upper(),
                )
            )
            continue

        categories.append(ParsedCategory(cat=normalized, classe=None))

    return categories


def extract_detail_id_from_onclick(onclick_value: str) -> Optional[str]:
    """Extract detail id from JS onclick string like ExecImpresaDettaglio('271815')."""
    if not onclick_value:
        return None
    match = re.search(r"ExecImpresaDettaglio\('([^']+)'\)", onclick_value)
    return match.group(1) if match else None
