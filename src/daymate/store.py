"""本地事件存储：SQLite，所有痕迹只留在用户自己的电脑上"""
import sqlite3
from datetime import datetime

from .config import DATA_DIR

DB_PATH = DATA_DIR / "daymate.db"


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            kind TEXT NOT NULL,          -- shell | file | window
            detail TEXT NOT NULL,
            meta TEXT DEFAULT ''
        )
        """
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_events_ts ON events(ts)")
    return conn


def add_event(kind: str, detail: str, meta: str = "") -> None:
    conn = get_conn()
    conn.execute(
        "INSERT INTO events (ts, kind, detail, meta) VALUES (?, ?, ?, ?)",
        (datetime.now().isoformat(timespec="seconds"), kind, detail, meta),
    )
    conn.commit()
    conn.close()


def add_events_batch(rows: list) -> None:
    """批量写入，rows: list of (ts, kind, detail, meta)"""
    if not rows:
        return
    conn = get_conn()
    conn.executemany(
        "INSERT INTO events (ts, kind, detail, meta) VALUES (?, ?, ?, ?)", rows
    )
    conn.commit()
    conn.close()


def events_by_date(date_str: str) -> list:
    """date_str 形如 2026-09-17"""
    conn = get_conn()
    rows = conn.execute(
        "SELECT ts, kind, detail, meta FROM events WHERE ts LIKE ? ORDER BY ts",
        (date_str + "%",),
    ).fetchall()
    conn.close()
    return rows


def clear_day(date_str: str) -> int:
    conn = get_conn()
    cur = conn.execute("DELETE FROM events WHERE ts LIKE ?", (date_str + "%",))
    conn.commit()
    affected = cur.rowcount
    conn.close()
    return affected
