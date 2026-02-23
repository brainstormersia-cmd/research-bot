# Albo Rifiuti Cat.5 Lead Research Bot

Bot compliance-first per estrazione, arricchimento, scoring e reporting di aziende Categoria 5 dall'Albo Gestori Ambientali.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## CLI

```bash
python -m src.main run-full \
  --sezione NA \
  --provincia NA \
  --categoria 5 \
  --max-pagine 20 \
  --format xlsx,csv,jsonl \
  --priority-province NA,SA,CE
```

Comandi separati:

```bash
python -m src.main extract-albo --sezione NA --provincia NA --categoria 5
python -m src.main enrich --input output/processed/albo_cat5_na_na.csv
python -m src.main score --input output/processed/albo_cat5_na_na_enriched.csv --priority-province NA,SA,CE
python -m src.main export --input output/processed/albo_cat5_na_na_enriched_scored.csv --format xlsx
python -m src.main report --input output/processed/albo_cat5_na_na_enriched_scored.csv
```

## Compliance e limiti

- Rispetta `robots.txt` e termini d'uso delle fonti.
- User-Agent dichiarato, nessun bypass CAPTCHA/protezioni.
- Delay conservativo configurabile (default 2s).
- Retry con backoff esponenziale via Tenacity.
- Se una fonte non è legalmente/tecnicamente adatta allo scraping: log + skip + fallback.
- Il modulo `enrichment` è fallback-safe: ritorna i record senza bloccare la pipeline se le integrazioni non sono disponibili.

### Alternative legali consigliate

- API/servizi CCIAA con licenza esplicita.
- INI-PEC ufficiale per consultazioni conformi.
- Open data pubblici con termini compatibili.

## Estensione a Cat.4 / altre province

- Cambiare `--categoria` da `5` a `4` (o altro) in estrazione.
- Aggiornare `priority-province` e regole di scoring in `src/pipelines/score_leads.py`.
- Aggiungere parser dedicati in `src/sources/enrichment/*`.
