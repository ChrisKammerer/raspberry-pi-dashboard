import sqlite3
import json


DB_PATH = "src/dashboard.db"

def _get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    with _get_conn() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS dashboard_cache (
            key TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            updated_at DATETIME NOT NULL,
            expires_at DATETIME,
            status TEXT DEFAULT 'ok',
            error_message TEXT
            );
                           
        CREATE TABLE IF NOT EXISTS display_state (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            last_rendered_hash TEXT,
            last_rendered_at DATETIME,
            last_full_refresh_at DATETIME
            );
        """)


def upsert_cache(key, data, updated_at, expires_at=None):
    with _get_conn() as conn:
        conn.execute("""
        INSERT INTO dashboard_cache (key, data, updated_at, expires_at, status)
        VALUES (?, ?, ?, ?, 'ok')
        ON CONFLICT(key) DO UPDATE SET
            data=excluded.data,
            updated_at=excluded.updated_at,
            expires_at=excluded.expires_at,
            status='ok',
            error_message=NULL
        """, (key, json.dumps(data), updated_at, expires_at))

def get_cache(key):
    with _get_conn() as conn:
        cur = conn.execute("""
        SELECT data, updated_at, expires_at
        FROM dashboard_cache
        WHERE key = ?
        """, (key,))
        row = cur.fetchone()

        if not row:
            return None

        return {
            "data": json.loads(row[0]),
            "updated_at": row[1],
            "expires_at": row[2]
        }