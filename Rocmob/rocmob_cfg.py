# rocmob_cfg.py
import os
from supabase import create_client, Client

SUPABASE_URL = "https://paifqtwkewuqszvqcuam.supabase.co"   # from Supabase > Settings > API
SUPABASE_KEY = "sb_publishable_Zcdbg00wDsMxIioTqHfOwQ_yu6gudtp" # use service_role key (not anon)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
