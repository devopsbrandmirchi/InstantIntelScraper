# rocmob_cfg.py
import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if value is None or not str(value).strip():
        raise RuntimeError(
            f"Missing required environment variable {name}. "
            "For local runs, copy .env.example to .env and fill in values. "
            "For GitHub Actions, add repository secrets SUPABASE_URL and SUPABASE_KEY "
            "(or set SUPABASE_SERVICE_ROLE_KEY instead of SUPABASE_KEY)."
        )
    return str(value).strip()


def _supabase_key() -> str:
    for name in ("SUPABASE_SERVICE_ROLE_KEY", "SUPABASE_KEY"):
        value = os.environ.get(name)
        if value is not None and str(value).strip():
            return str(value).strip()
    raise RuntimeError(
        "Missing SUPABASE_KEY or SUPABASE_SERVICE_ROLE_KEY. "
        "Use the Supabase service_role key (not the anon key) for server-side upserts."
    )


SUPABASE_URL = _require_env("SUPABASE_URL")
SUPABASE_KEY = _supabase_key()

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
