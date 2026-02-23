from __future__ import annotations

from pathlib import Path

from src.models import CompanyRecord
from src.utils.io_helpers import save_records


def run_export(records: list[CompanyRecord], output_base: Path, formats: list[str]) -> list[Path]:
    return save_records(records, output_base=output_base, formats=formats)
