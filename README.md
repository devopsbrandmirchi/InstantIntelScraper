# InstantIntelScraper

Scrapy-based web scrapers that collect dealership vehicle inventory and write rows into **Supabase** (`public.scrap_rawdata`). Active production spiders are in **`Rocmob/spiders/`**.

## Features

- **Scrapy** spiders for multiple dealerships (RV, automotive, etc.)
- **Supabase (PostgreSQL)** storage via `supabase-py` upserts
- **Daily snapshots**: each vehicle can have one row per calendar day (UTC) using `creation_date` + composite primary key `(sk, creation_date)`
- **GitHub Actions**: parallel matrix jobs, scheduled twice daily in **UTC** (off the hour to reduce queue delays; manual `workflow_dispatch` also supported)

## Requirements

- Python **3.10+** (matches CI)
- Dependencies: see [`requirements.txt`](requirements.txt) (`scrapy`, `requests`, `supabase`, `psycopg2-binary`, `python-dotenv`)

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

[`Rocmob/rocmob_cfg.py`](Rocmob/rocmob_cfg.py) builds the client from environment variables (and optionally a repo-root `.env` loaded via `python-dotenv`).

- **Local:** copy [`.env.example`](.env.example) to `.env`, set `SUPABASE_URL` and `SUPABASE_KEY` (service role key, not anon). `.env` is gitignored.
- **GitHub Actions:** add repository secret `SUPABASE_URL` and either `SUPABASE_KEY` or `SUPABASE_SERVICE_ROLE_KEY` for the service role key. The workflow injects these into each job.

You may use `SUPABASE_SERVICE_ROLE_KEY` instead of `SUPABASE_KEY` anywhere (local `.env` or GitHub).

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

Workflow: [`.github/workflows/scrapy.yml`](.github/workflows/scrapy.yml) (shown in GitHub as **InstantIntel - Daily Scrapy to Supabase**).

- **Schedule**: `cron: "25 2 * * *"` and `cron: "35 7 * * *"` (UTC). GitHub may still start jobs **late**; times are not guaranteed.  
- **Triggers**: `schedule`, `workflow_dispatch`  
- **Matrix**: one job per spider (parallel runs)  
- Uses `actions/checkout@v6` and `actions/setup-python@v6`
- Sets `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true` so those actions run on **Node.js 24** (GitHub is deprecating Node 20 for Actions; Node 24 becomes the default around June 2026 — see [GitHub changelog](https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/)).

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
