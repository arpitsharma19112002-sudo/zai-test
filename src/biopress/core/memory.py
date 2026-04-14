"""Persistent Memory module for BioPress."""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


class Memory:
    """Lightweight pattern tracking for BioPress."""

    def __init__(self, enabled: bool = False, limit: int = 1000):
        self.enabled = enabled
        self.limit = limit
        self._db_path: Optional[Path] = None
        self._conn: Optional[sqlite3.Connection] = None

    def initialize(self, db_path: Optional[Path] = None) -> None:
        """Initialize the memory database."""
        if not self.enabled:
            return

        if db_path is None:
            db_path = Path.home() / ".config" / "biopress" / "memory.db"

        self._db_path = db_path
        self._db_path.parent.mkdir(parents=True, exist_ok=True)

        self._conn = sqlite3.connect(str(self._db_path))
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT NOT NULL,
                pattern_key TEXT NOT NULL,
                count INTEGER DEFAULT 1,
                last_seen TEXT NOT NULL,
                data TEXT,
                UNIQUE(pattern_type, pattern_key)
            )
        """)
        self._conn.commit()

    def track_question_pattern(
        self, topic: str, question_type: str, quality_score: float
    ) -> None:
        """Track question generation patterns."""
        if not self.enabled or not self._conn:
            return

        key = f"{topic}:{question_type}"
        self._upsert_pattern("question", key, {"quality_score": quality_score})

    def track_correction(
        self, original: str, corrected: str, correction_type: str
    ) -> None:
        """Track editor corrections to learn from feedback."""
        if not self.enabled or not self._conn:
            return

        self._upsert_pattern(
            "correction",
            correction_type,
            {"original": original, "corrected": corrected},
        )

    def get_question_stats(self, topic: str) -> dict:
        """Get question generation stats for a topic."""
        if not self.enabled or not self._conn:
            return {}

        # Escape wildcards to prevent logic injection
        escaped_topic = topic.replace("%", "\\%").replace("_", "\\_")
        cursor = self._conn.execute(
            """
            SELECT pattern_key, count, data FROM patterns
            WHERE pattern_type = 'question' AND pattern_key LIKE ? ESCAPE '\\'
            """,
            (f"{escaped_topic}:%",),
        )

        stats = {}
        for row in cursor:
            key_parts = row[0].split(":")
            if len(key_parts) >= 2:
                qtype = key_parts[1]
                stats[qtype] = {"count": row[1], "avg_quality": json.loads(row[2] or "{}").get("quality_score", 0)}

        return stats

    def get_correction_stats(self) -> dict:
        """Get correction statistics."""
        if not self.enabled or not self._conn:
            return {}

        cursor = self._conn.execute(
            "SELECT pattern_key, count FROM patterns WHERE pattern_type = 'correction'"
        )

        return {row[0]: row[1] for row in cursor}

    def _upsert_pattern(self, pattern_type: str, pattern_key: str, data: dict) -> None:
        """Insert or update a pattern."""
        now = datetime.now(timezone.utc).isoformat()
        data_json = json.dumps(data)

        self._conn.execute(
            """
            INSERT INTO patterns (pattern_type, pattern_key, count, last_seen, data)
            VALUES (?, ?, 1, ?, ?)
            ON CONFLICT(pattern_type, pattern_key) DO UPDATE SET
                count = count + 1,
                last_seen = ?,
                data = ?
            """,
            (pattern_type, pattern_key, now, data_json, now, data_json),
        )
        self._prune_old_records()
        self._conn.commit()

    def _prune_old_records(self) -> None:
        """Prune oldest records if over limit."""
        self._conn.execute(
            """
            DELETE FROM patterns WHERE id NOT IN (
                SELECT id FROM patterns ORDER BY last_seen DESC LIMIT ?
            )
            """,
            (self.limit,),
        )

    def clear(self) -> None:
        """Clear all memory data."""
        if not self.enabled or not self._conn:
            return

        self._conn.execute("DELETE FROM patterns")
        self._conn.commit()

    def close(self) -> None:
        """Close the database connection."""
        if self._conn:
            self._conn.close()
            self._conn = None


import threading

_memory_instance: Optional[Memory] = None
_lock = threading.Lock()


def get_memory() -> Memory:
    """Get the global memory instance with thread safety."""
    global _memory_instance
    if _memory_instance is None:
        with _lock:
            if _memory_instance is None:
                from biopress.core.config import get_config_manager
        
                config = get_config_manager()
                enabled = config.get("memory") == "enabled"
                limit = int(config.get("memory_limit") or "1000")
        
                _memory_instance = Memory(enabled=enabled, limit=limit)
                _memory_instance.initialize()

    return _memory_instance


def reset_memory() -> None:
    """Reset the global memory instance."""
    global _memory_instance
    if _memory_instance:
        _memory_instance.close()
    _memory_instance = None