from __future__ import annotations

from loguru import logger

from src.models import CompanyRecord


def run_enrichment(records: list[CompanyRecord]) -> list[CompanyRecord]:
    """Fallback-only enrichment placeholder.

    Real integrations may require licensed APIs or explicit scraping permission.
    """
    logger.warning("Enrichment sources not configured: returning input records unchanged")
    return records
