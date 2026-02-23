from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl

from src.utils.category_parser import ParsedCategory


class PriorityTarget(str, Enum):
    ALTA = "alta"
    MEDIA = "media"
    BASSA = "bassa"


class OutreachStatus(str, Enum):
    DA_CONTATTARE = "da_contattare"
    CONTATTATO = "contattato"
    NON_INTERESSATO = "non_interessato"


class CompanyRecord(BaseModel):
    numero_iscrizione: str
    ragione_sociale: str
    ragione_sociale_norm: str
    indirizzo: Optional[str] = None
    cap: Optional[str] = None
    comune: Optional[str] = None
    provincia: Optional[str] = None

    categorie_raw: str = ""
    categorie_parsed_json: list[ParsedCategory] = Field(default_factory=list)
    has_categoria_5: bool = False
    classe_cat5: Optional[str] = None
    ha_anche_cat4: bool = False

    piva: Optional[str] = None
    codice_fiscale: Optional[str] = None
    rea: Optional[str] = None

    pec: Optional[str] = None
    email_generica: Optional[str] = None
    telefono: Optional[str] = None
    sito_web: Optional[HttpUrl] = None

    fatturato: Optional[float] = None
    anno_fatturato: Optional[int] = None
    dipendenti: Optional[int] = None
    anno_dipendenti: Optional[int] = None

    fonte_arricchimento: Optional[str] = None
    url_fonte: Optional[str] = None
    score_match: Optional[float] = None
    regola_match: Optional[str] = None

    quality_score: int = 0
    priority_score: int = 0
    priorita_target: PriorityTarget = PriorityTarget.BASSA
    canale_preferito: Optional[str] = None

    outreach_status: OutreachStatus = OutreachStatus.DA_CONTATTARE
    note_outreach: Optional[str] = None
    persona_referente: Optional[str] = None
    data_primo_contatto: Optional[date] = None

    data_estrazione: datetime = Field(default_factory=datetime.utcnow)
    note_parser: Optional[str] = None


class ExtractParams(BaseModel):
    sezione: str
    provincia: str
    categoria: str = "5"
    max_pagine: int = 20


class RunResult(BaseModel):
    records: list[CompanyRecord]
    warnings: list[str] = Field(default_factory=list)
