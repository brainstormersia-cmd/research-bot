from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd
import typer

from src.logging_config import configure_logging
from src.models import CompanyRecord, ExtractParams
from src.pipelines.enrich_companies import run_enrichment
from src.pipelines.export_dataset import run_export
from src.pipelines.extract_albo import run_extract_albo
from src.pipelines.generate_report import generate_report
from src.pipelines.score_leads import run_score
from src.validators.quality_checks import compute_quality_score

app = typer.Typer(help="Albo Rifiuti Cat.5 Lead Research Bot")


def _load_records(input_path: Path) -> list[CompanyRecord]:
    df = pd.read_csv(input_path)
    return [CompanyRecord.model_validate(row) for row in df.to_dict(orient="records")]


@app.command("extract-albo")
def extract_albo(
    sezione: str = typer.Option(...),
    provincia: str = typer.Option(...),
    categoria: str = typer.Option("5"),
    max_pagine: int = typer.Option(20),
):
    configure_logging()
    params = ExtractParams(sezione=sezione, provincia=provincia, categoria=categoria, max_pagine=max_pagine)
    records = run_extract_albo(params)
    out = Path("output/processed") / f"albo_cat5_{sezione.lower()}_{provincia.lower()}"
    run_export(records, out, ["csv"])


@app.command("enrich")
def enrich(input: Path = typer.Option(...)):
    records = _load_records(input)
    enriched = run_enrichment(records)
    run_export(enriched, input.with_name(input.stem + "_enriched"), ["csv"])


@app.command("score")
def score(input: Path = typer.Option(...), priority_province: Optional[str] = typer.Option(None)):
    records = _load_records(input)
    scored = run_score(records, priority_provinces=(priority_province or "").split(",") if priority_province else [])
    for rec in scored:
        rec.quality_score = compute_quality_score(rec)
    run_export(scored, input.with_name(input.stem + "_scored"), ["csv"])


@app.command("export")
def export(input: Path = typer.Option(...), format: str = typer.Option("xlsx,csv,jsonl")):
    records = _load_records(input)
    run_export(records, input.with_suffix(""), format.split(","))


@app.command("report")
def report(input: Path = typer.Option(...)):
    records = _load_records(input)
    generate_report(records, Path("output/reports"))


@app.command("run-full")
def run_full(
    sezione: str = typer.Option(...),
    provincia: str = typer.Option(...),
    categoria: str = typer.Option("5"),
    max_pagine: int = typer.Option(20),
    format: str = typer.Option("xlsx,csv,jsonl"),
    priority_province: str = typer.Option(""),
):
    configure_logging()
    extracted = run_extract_albo(ExtractParams(sezione=sezione, provincia=provincia, categoria=categoria, max_pagine=max_pagine))
    enriched = run_enrichment(extracted)
    scored = run_score(enriched, priority_provinces=[p for p in priority_province.split(",") if p])
    for rec in scored:
        rec.quality_score = compute_quality_score(rec)

    base = Path("output/processed") / f"companies_cat5_{sezione.lower()}_{provincia.lower()}"
    run_export(scored, base, format.split(","))
    generate_report(scored, Path("output/reports"))


if __name__ == "__main__":
    app()
