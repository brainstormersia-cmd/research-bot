import re
import unicodedata


def normalize_company_name(name: str) -> str:
    normalized = unicodedata.normalize("NFKD", name or "")
    normalized = normalized.encode("ascii", "ignore").decode("ascii")
    normalized = re.sub(r"[^A-Za-z0-9 ]+", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip().lower()
    return normalized
