-- Add creation_date to scrap_rawdata (date only, default = current date).
-- Use this for transferring data to another table (e.g. filter by creation_date).
-- Run this in Supabase: SQL Editor → New query → paste → Run.

ALTER TABLE public.scrap_rawdata
ADD COLUMN IF NOT EXISTS creation_date date NULL DEFAULT (CURRENT_DATE);

COMMENT ON COLUMN public.scrap_rawdata.creation_date IS 'Date the row was first inserted; used for data transfer.';
