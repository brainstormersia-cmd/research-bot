from __future__ import annotations

from collections import Counter
from datetime import datetime
from pathlib import Path

from src.models import CompanyRecord


def generate_report(records: list[CompanyRecord], output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    total = len(records)
    with_pec = sum(1 for r in records if r.pec)
    with_tel = sum(1 for r in records if r.telefono)
    with_piva = sum(1 for r in records if r.piva)
    by_province = Counter((r.provincia or "N/D") for r in records)

    top20 = sorted(records, key=lambda r: r.priority_score, reverse=True)[:20]
    incomplete = [r for r in records if not (r.pec or r.email_generica or r.telefono)]

    date_stamp = datetime.now().strftime("%Y%m%d")
    md_path = output_dir / f"report_{date_stamp}.md"
    html_path = output_dir / f"report_{date_stamp}.html"

    md = [
        "# Report Lead Cat.5",
        f"- Totale aziende Cat.5: **{total}**",
        f"- Con PEC: **{with_pec}**",
        f"- Con telefono: **{with_tel}**",
        f"- Con P.IVA: **{with_piva}**",
        "\n## Distribuzione per provincia",
    ]
    md.extend([f"- {k}: {v}" for k, v in by_province.items()])
    md.append("\n## Top 20 lead")
    md.extend([f"- {r.ragione_sociale} ({r.provincia}) - score {r.priority_score}" for r in top20])
    md.append("\n## Record incompleti")
    md.extend([f"- {r.ragione_sociale} ({r.numero_iscrizione})" for r in incomplete[:50]])
    md.append(
        '\n> Avvertenza compliance: "Dataset per outreach discovery mirato. Non usare per invio massivo automatico."'
    )

    md_text = "\n".join(md)
    md_path.write_text(md_text, encoding="utf-8")
    html_path.write_text(f"<html><body><pre>{md_text}</pre></body></html>", encoding="utf-8")
    return md_path, html_path
