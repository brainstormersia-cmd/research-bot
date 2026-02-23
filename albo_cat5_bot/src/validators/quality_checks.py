from src.models import CompanyRecord


def compute_quality_score(record: CompanyRecord) -> int:
    score = 0
    if record.ragione_sociale and record.numero_iscrizione:
        score += 30
    if record.indirizzo and record.comune and record.provincia:
        score += 25
    if record.pec or record.email_generica or record.telefono:
        score += 25
    if record.piva or record.codice_fiscale:
        score += 20
    return min(score, 100)
