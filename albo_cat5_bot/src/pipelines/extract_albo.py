from __future__ import annotations

from loguru import logger

from src.models import CompanyRecord, ExtractParams
from src.sources.albo.client import AlboClient
from src.sources.albo.parser_detail import parse_albo_detail_page
from src.sources.albo.parser_list import parse_albo_list_page
from src.utils.category_parser import parse_categorie
from src.utils.text_normalization import normalize_company_name


def run_extract_albo(params: ExtractParams) -> list[CompanyRecord]:
    client = AlboClient()
    records: list[CompanyRecord] = []

    try:
        for page in range(1, params.max_pagine + 1):
            response = client.get(
                "/ricerca/iscritti",
                params={
                    "sezione": params.sezione,
                    "provincia": params.provincia,
                    "categoria": params.categoria,
                    "page": page,
                },
            )
            page_items = parse_albo_list_page(response.text)
            if not page_items:
                break

            for item in page_items:
                parsed = parse_categorie(item["categorie_raw"])
                has_cat5 = any(cat.cat == "5" for cat in parsed)
                if not has_cat5:
                    continue

                detail_data = {}
                if item.get("detail_id"):
                    detail_response = client.get(f"/dettaglio/{item['detail_id']}")
                    detail_data = parse_albo_detail_page(detail_response.text)

                record = CompanyRecord(
                    numero_iscrizione=item["numero_iscrizione"],
                    ragione_sociale=item["ragione_sociale"],
                    ragione_sociale_norm=normalize_company_name(item["ragione_sociale"]),
                    provincia=item.get("provincia") or params.provincia,
                    categorie_raw=item["categorie_raw"],
                    categorie_parsed_json=parsed,
                    has_categoria_5=has_cat5,
                    classe_cat5=next((cat.classe for cat in parsed if cat.cat == "5"), None),
                    ha_anche_cat4=any(cat.cat == "4" for cat in parsed),
                    indirizzo=detail_data.get("indirizzo"),
                    cap=detail_data.get("cap"),
                    comune=detail_data.get("comune"),
                    pec=detail_data.get("pec"),
                    email_generica=detail_data.get("email_generica"),
                    telefono=detail_data.get("telefono"),
                )
                records.append(record)

        logger.info(f"Extracted {len(records)} Cat.5 companies")
        return records
    finally:
        client.close()
