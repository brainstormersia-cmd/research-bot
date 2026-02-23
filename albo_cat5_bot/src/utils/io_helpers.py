from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src.models import CompanyRecord


def records_to_dataframe(records: list[CompanyRecord]) -> pd.DataFrame:
    rows = [r.model_dump(mode="json") for r in records]
    return pd.DataFrame(rows)


def save_records(records: list[CompanyRecord], output_base: Path, formats: list[str]) -> list[Path]:
    output_base.parent.mkdir(parents=True, exist_ok=True)
    df = records_to_dataframe(records)
    created: list[Path] = []

    if "csv" in formats:
        path = output_base.with_suffix(".csv")
        df.to_csv(path, index=False)
        created.append(path)
    if "xlsx" in formats:
        path = output_base.with_suffix(".xlsx")
        df.to_excel(path, index=False)
        created.append(path)
    if "jsonl" in formats:
        path = output_base.with_suffix(".jsonl")
        with path.open("w", encoding="utf-8") as f:
            for row in df.to_dict(orient="records"):
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
        created.append(path)

    return created
