# InstantIntelScraper

Scrapy-based web scrapers that collect dealership vehicle inventory and write rows into **Supabase** (`public.scrap_rawdata`). Active production spiders are in **`Rocmob/spiders/`**.

## Features

- **Scrapy** spiders for multiple dealerships (RV, automotive, etc.)
- **Supabase (PostgreSQL)** storage via `supabase-py` upserts
- **Daily snapshots**: each vehicle can have one row per calendar day (UTC) using `creation_date` + composite primary key `(sk, creation_date)`
- **GitHub Actions**: parallel matrix jobs, scheduled daily at **02:00 UTC** (manual `workflow_dispatch` also supported)

## Requirements

- Python **3.10+** (matches CI)
- Dependencies: see [`requirements.txt`](requirements.txt) (`scrapy`, `requests`, `supabase`, `psycopg2-binary`)

## Project layout

| Path | Purpose |
|------|---------|
| `Rocmob/` | Scrapy project module (settings, middlewares, pipelines) |
| `Rocmob/spiders/` | **Active** spiders writing to Supabase |
| `Rocmob/rocmob_cfg.py` | Supabase client initialization |
| `.github/workflows/scrapy.yml` | Scheduled / manual spider runs |
| `supabase_add_creation_date.sql` | Adds `creation_date` column (if needed) |
| `supabase_scrap_rawdata_daily_pk.sql` | Migration: composite PK `(sk, creation_date)` for daily inserts |
| `spider_mysql_to_supabase_mapping.csv` | CSV mapping MySQL file → Supabase file → spider name → dealership |
| `spider_mysql_to_supabase_mapping.txt` | Same mapping in plain-text table form |
| `scrapy.cfg` | Scrapy project entry (`default = Rocmob.settings`) |

## Local setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install -r requirements.txt
```

### Supabase configuration

The client is created in [`Rocmob/rocmob_cfg.py`](Rocmob/rocmob_cfg.py). **Do not commit real API keys** to public repositories—prefer environment variables and local overrides (or GitHub **Secrets** for Actions).

Spiders upsert into `scrap_rawdata` with:

```python
supabase.table("scrap_rawdata").upsert(row, on_conflict="sk,creation_date").execute()
```

Ensure your table schema matches (including `creation_date` and the composite primary key if you use daily snapshots). Run the SQL scripts in the Supabase SQL Editor when migrating (back up first).

## Run a spider locally

From the repository root:

```bash
scrapy list
scrapy crawl <spider_name>
```

Example:

```bash
scrapy crawl skyriverrv
```

Spider names are the Scrapy `name` attribute (same strings as in the GitHub Actions matrix).

## GitHub Actions

Workflow: [`.github/workflows/scrapy.yml`](.github/workflows/scrapy.yml).

- **Schedule**: `cron: "0 2 * * *"` → daily at 02:00 UTC  
- **Triggers**: `schedule`, `workflow_dispatch`  
- **Matrix**: one job per spider (parallel runs)  
- Uses `actions/checkout@v4` and `actions/setup-python@v5`

If credentials are not injected via Secrets/env in CI, ensure your deployment approach matches how `rocmob_cfg.py` obtains the Supabase URL and key.

## Adding a new spider

1. Add a spider module under `Rocmob/spiders/` following existing patterns (`creation_date` in `__init__`, `row` dict aligned with `scrap_rawdata`, upsert `on_conflict="sk,creation_date"`).
2. Append the spider `name` to the `matrix.spider` list in `.github/workflows/scrapy.yml`.
3. Update `spider_mysql_to_supabase_mapping.csv` and `spider_mysql_to_supabase_mapping.txt` if it was migrated from a MySQL file.

## MySQL → Supabase reference

See **`spider_mysql_to_supabase_mapping.csv`** (machine-friendly) or **`spider_mysql_to_supabase_mapping.txt`** (readable table) for:

- MySQL source filename (`MySqlSpiders/`)
- Supabase spider filename (`Rocmob/spiders/`)
- Scrapy spider name
- Dealership display name

## License / disclaimer

Scraping is subject to each site’s terms of use and robots policy. Use responsibly and only where you have permission to collect data.
