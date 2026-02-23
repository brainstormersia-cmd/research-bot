from src.models import CompanyRecord


def dedupe_records(records: list[CompanyRecord]) -> list[CompanyRecord]:
    seen: set[tuple[str, str]] = set()
    out: list[CompanyRecord] = []
    for rec in records:
        key = (rec.numero_iscrizione, rec.ragione_sociale_norm)
        if key in seen:
            continue
        seen.add(key)
        out.append(rec)
    return out
