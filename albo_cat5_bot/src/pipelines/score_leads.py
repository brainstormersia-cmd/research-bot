from __future__ import annotations

from src.models import CompanyRecord, PriorityTarget


def compute_priority_score(record: CompanyRecord, priority_provinces: list[str] | None = None) -> CompanyRecord:
    score = 0
    priority_provinces = [p.upper() for p in (priority_provinces or [])]

    if record.has_categoria_5:
        score += 10
    if record.pec:
        score += 20
    if record.telefono or record.email_generica:
        score += 15
    if record.ha_anche_cat4:
        score += 15
    if record.piva:
        score += 10

    coherence_fields = [record.ragione_sociale, record.indirizzo, record.comune, record.provincia]
    if all(coherence_fields):
        score += 10

    if record.provincia and record.provincia.upper() in priority_provinces:
        score += 10
    if record.fatturato or record.dipendenti:
        score += 10
    if record.sito_web:
        score += 10

    record.priority_score = min(score, 100)
    if record.priority_score >= 70:
        record.priorita_target = PriorityTarget.ALTA
    elif record.priority_score >= 45:
        record.priorita_target = PriorityTarget.MEDIA
    else:
        record.priorita_target = PriorityTarget.BASSA

    if record.pec:
        record.canale_preferito = "PEC"
    elif record.email_generica:
        record.canale_preferito = "email"
    elif record.telefono:
        record.canale_preferito = "telefono"

    return record


def run_score(records: list[CompanyRecord], priority_provinces: list[str] | None = None) -> list[CompanyRecord]:
    return [compute_priority_score(rec, priority_provinces=priority_provinces) for rec in records]
