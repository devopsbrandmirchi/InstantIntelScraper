-- One row per vehicle per calendar day (UTC): new insert each day when cron runs.
-- Run in Supabase SQL Editor after backing up if needed.

-- 1) Ensure every row has creation_date (use UTC date from created_at, or today)
UPDATE public.scrap_rawdata
SET creation_date = COALESCE(
  creation_date,
  (created_at AT TIME ZONE 'UTC')::date,
  CURRENT_DATE
)
WHERE creation_date IS NULL;

UPDATE public.scrap_rawdata
SET creation_date = CURRENT_DATE
WHERE creation_date IS NULL;

-- 2) Drop old primary key on sk only
ALTER TABLE public.scrap_rawdata
  DROP CONSTRAINT IF EXISTS scrap_rawdata_pkey;

-- 3) creation_date required for composite key
ALTER TABLE public.scrap_rawdata
  ALTER COLUMN creation_date SET NOT NULL;

-- 4) Composite PK: same sk can appear once per day; each new day = new row
ALTER TABLE public.scrap_rawdata
  ADD PRIMARY KEY (sk, creation_date);

COMMENT ON COLUMN public.scrap_rawdata.creation_date IS 'UTC calendar date of this scrape run (cron day); part of primary key with sk.';
