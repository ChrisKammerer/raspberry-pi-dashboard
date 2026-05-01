from db import get_cache, init_db, upsert_cache
from datetime import datetime, timezone, timedelta

init_db()

data = {
    "temp": 75,
    "wind": 4
}
key = "weather2"
updated_at = datetime.now(timezone.utc)
expires_at = updated_at + timedelta(minutes=30)
upsert_cache(key, data, updated_at, expires_at)

results = get_cache(key)

print(results)