import json 
import sqlite3
from datetime import datetime, timezone
from app.core.config import get_settings

settings = get_settings()

# initialize the database if it doesn't exist
def init_db() -> None:
    con = sqlite3.connect(settings.audit_db_path)
    con.execute(
        """CREATE TABLE IF NOT EXISTS query_audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            question TEXT NOT NULL,
            source_used TEXT NOT NULL,
            trace_json TEXT NOT NULL
        )"""
    )
    con.commit()
    con.close()

def write_audit(question: str, source_used: str, trace: list[str]) -> None:
    con = sqlite3.connect(settings.audit_db_path)
    con.execute(
        "INSERT INTO query_audit_log(created_at, question, source_used, trace_json) VALUES (?, ?, ?, ?)",
        (datetime.now(timezone.utc).isoformat(), question, source_used, json.dumps(trace)),
    )
    con.commit()
    con.close()
