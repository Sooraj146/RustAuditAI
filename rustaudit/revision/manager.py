"""
Intra-Procedural Revision Database Manager (SRS §4.6.7).
Maintains persistent revision tracking, historical code snapshots,
timestamps, quality metrics, and rollback capabilities.
"""

import sqlite3
import json
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional


@dataclass
class CodeRevision:
    revision_id: str
    function_name: str
    revision_number: int
    timestamp: str
    timestamp_display: str
    source_code: str
    rqi_score: float
    grade: str
    vector_scores: Dict[str, float]
    change_type: str  # "INITIAL", "PATCH_APPLIED", "ROLLBACK"
    patch_summary: str
    is_active: bool = True

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        return d


class RevisionManager:
    """SQLite-backed intra-procedural revision database complying with SRS §4.6.7."""

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            project_root = Path(__file__).parent.parent.parent
            data_dir = project_root / "data"
            data_dir.mkdir(parents=True, exist_ok=True)
            self.db_path = str(data_dir / "rustaudit_revisions.db")
        else:
            self.db_path = db_path

        if self.db_path == ":memory:":
            self._persistent_conn = sqlite3.connect(":memory:", check_same_thread=False)
            self._persistent_conn.row_factory = sqlite3.Row
        else:
            self._persistent_conn = None

        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        if self._persistent_conn is not None:
            return self._persistent_conn
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS intra_revisions (
                    id TEXT PRIMARY KEY,
                    function_name TEXT NOT NULL,
                    revision_number INTEGER NOT NULL,
                    timestamp TEXT NOT NULL,
                    timestamp_display TEXT NOT NULL,
                    source_code TEXT NOT NULL,
                    rqi_score REAL NOT NULL,
                    grade TEXT NOT NULL,
                    vector_scores TEXT NOT NULL,
                    change_type TEXT NOT NULL,
                    patch_summary TEXT NOT NULL,
                    is_active INTEGER NOT NULL DEFAULT 1
                )
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_rev_fn ON intra_revisions(function_name, revision_number)
            """)
            conn.commit()

    def record_revision(
        self,
        function_name: str,
        source_code: str,
        rqi_score: float,
        grade: str,
        vector_scores: Dict[str, float],
        change_type: str = "INITIAL",
        patch_summary: str = "",
    ) -> CodeRevision:
        """
        Records a new approved modification layer in the intra-procedural database.
        Sets prior revisions for this function to inactive.
        """
        now = datetime.now()
        iso_timestamp = now.isoformat()
        display_timestamp = now.strftime("%I:%M:%S %p (%b %d)")
        rev_id = str(uuid.uuid4())

        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Determine next sequential revision number for this function
            cursor.execute(
                "SELECT COALESCE(MAX(revision_number), 0) + 1 FROM intra_revisions WHERE function_name = ?",
                (function_name,)
            )
            next_rev_num = cursor.fetchone()[0]

            # Mark earlier revisions as not currently active
            cursor.execute(
                "UPDATE intra_revisions SET is_active = 0 WHERE function_name = ?",
                (function_name,)
            )

            # Insert new revision
            cursor.execute(
                """
                INSERT INTO intra_revisions (
                    id, function_name, revision_number, timestamp, timestamp_display,
                    source_code, rqi_score, grade, vector_scores, change_type, patch_summary, is_active
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                """,
                (
                    rev_id,
                    function_name,
                    next_rev_num,
                    iso_timestamp,
                    display_timestamp,
                    source_code,
                    float(rqi_score),
                    grade,
                    json.dumps(vector_scores),
                    change_type,
                    patch_summary or f"Revision #{next_rev_num} ({change_type})",
                )
            )
            conn.commit()

        return CodeRevision(
            revision_id=rev_id,
            function_name=function_name,
            revision_number=next_rev_num,
            timestamp=iso_timestamp,
            timestamp_display=display_timestamp,
            source_code=source_code,
            rqi_score=float(rqi_score),
            grade=grade,
            vector_scores=vector_scores,
            change_type=change_type,
            patch_summary=patch_summary or f"Revision #{next_rev_num} ({change_type})",
            is_active=True,
        )

    def get_revisions(self, function_name: Optional[str] = None) -> List[CodeRevision]:
        """Fetches chronological revision entries."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if function_name:
                cursor.execute(
                    "SELECT * FROM intra_revisions WHERE function_name = ? ORDER BY revision_number ASC",
                    (function_name,)
                )
            else:
                cursor.execute(
                    "SELECT * FROM intra_revisions ORDER BY timestamp ASC"
                )
            rows = cursor.fetchall()

        revisions = []
        for r in rows:
            revisions.append(
                CodeRevision(
                    revision_id=r["id"],
                    function_name=r["function_name"],
                    revision_number=r["revision_number"],
                    timestamp=r["timestamp"],
                    timestamp_display=r["timestamp_display"],
                    source_code=r["source_code"],
                    rqi_score=float(r["rqi_score"]),
                    grade=r["grade"],
                    vector_scores=json.loads(r["vector_scores"]) if r["vector_scores"] else {},
                    change_type=r["change_type"],
                    patch_summary=r["patch_summary"],
                    is_active=bool(r["is_active"]),
                )
            )
        return revisions

    def get_revision(self, revision_id: str) -> Optional[CodeRevision]:
        """Fetches a specific revision by UUID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM intra_revisions WHERE id = ?", (revision_id,))
            r = cursor.fetchone()

        if not r:
            return None

        return CodeRevision(
            revision_id=r["id"],
            function_name=r["function_name"],
            revision_number=r["revision_number"],
            timestamp=r["timestamp"],
            timestamp_display=r["timestamp_display"],
            source_code=r["source_code"],
            rqi_score=float(r["rqi_score"]),
            grade=r["grade"],
            vector_scores=json.loads(r["vector_scores"]) if r["vector_scores"] else {},
            change_type=r["change_type"],
            patch_summary=r["patch_summary"],
            is_active=bool(r["is_active"]),
        )

    def rollback_to_revision(self, revision_id: str) -> Optional[CodeRevision]:
        """
        Restores function code back to any earlier version state (SRS §4.6.7).
        Commits a new rollback entry into the revision database to maintain audit history.
        """
        target = self.get_revision(revision_id)
        if not target:
            return None

        summary = f"Rolled back to Revision #{target.revision_number} state ({target.change_type})"
        return self.record_revision(
            function_name=target.function_name,
            source_code=target.source_code,
            rqi_score=target.rqi_score,
            grade=target.grade,
            vector_scores=target.vector_scores,
            change_type="ROLLBACK",
            patch_summary=summary,
        )

    def clear_revisions(self, function_name: Optional[str] = None):
        """Clears revision records for a specific function or all functions."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if function_name:
                cursor.execute("DELETE FROM intra_revisions WHERE function_name = ?", (function_name,))
            else:
                cursor.execute("DELETE FROM intra_revisions")
            conn.commit()


_global_manager: Optional[RevisionManager] = None


def get_revision_manager(db_path: Optional[str] = None) -> RevisionManager:
    """Returns the singleton revision manager instance."""
    global _global_manager
    if _global_manager is None or db_path is not None:
        _global_manager = RevisionManager(db_path=db_path)
    return _global_manager
