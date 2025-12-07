"""
Violation Tracking System
Tracks building violations, safety issues, and regulatory compliance
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import json
import sqlite3


@dataclass
class Violation:
    """Violation record structure"""
    id: str
    case_id: str
    violation_type: str  # building_safety, osha, ada, etc.
    severity: str  # critical, major, minor
    description: str
    location: str
    date_reported: str
    date_discovered: Optional[str] = None
    status: str = "open"  # open, in_progress, resolved, ignored
    responsible_party: Optional[str] = None
    citation_number: Optional[str] = None
    fine_amount: Optional[float] = None
    metadata: Dict[str, Any] = None
    evidence_ids: List[str] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.evidence_ids is None:
            self.evidence_ids = []

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ViolationTracker:
    """Tracks and manages violation records"""

    def __init__(self, db_path: str = "violations.db"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS violations (
                id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                violation_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                description TEXT NOT NULL,
                location TEXT NOT NULL,
                date_reported TEXT NOT NULL,
                date_discovered TEXT,
                status TEXT DEFAULT 'open',
                responsible_party TEXT,
                citation_number TEXT,
                fine_amount REAL,
                metadata TEXT,
                evidence_ids TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_violation_case ON violations(case_id)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_violation_type ON violations(violation_type)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_violation_status ON violations(status)
        ''')

        conn.commit()
        conn.close()

    def add_violation(self, violation: Violation) -> bool:
        """Add violation to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO violations (
                    id, case_id, violation_type, severity, description,
                    location, date_reported, date_discovered, status,
                    responsible_party, citation_number, fine_amount,
                    metadata, evidence_ids
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                violation.id,
                violation.case_id,
                violation.violation_type,
                violation.severity,
                violation.description,
                violation.location,
                violation.date_reported,
                violation.date_discovered,
                violation.status,
                violation.responsible_party,
                violation.citation_number,
                violation.fine_amount,
                json.dumps(violation.metadata),
                json.dumps(violation.evidence_ids)
            ))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Error adding violation: {e}")
            return False

    def get_violations_by_case(self, case_id: str) -> List[Violation]:
        """Get all violations for a case"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM violations WHERE case_id = ?
            ORDER BY severity DESC, date_reported DESC
        ''', (case_id,))

        rows = cursor.fetchall()
        conn.close()

        return [self._row_to_violation(row) for row in rows]

    def get_critical_violations(self, case_id: str) -> List[Violation]:
        """Get critical severity violations"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM violations
            WHERE case_id = ? AND severity = 'critical'
            ORDER BY date_reported DESC
        ''', (case_id,))

        rows = cursor.fetchall()
        conn.close()

        return [self._row_to_violation(row) for row in rows]

    def get_open_violations(self, case_id: str) -> List[Violation]:
        """Get unresolved violations"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM violations
            WHERE case_id = ? AND status = 'open'
            ORDER BY severity DESC, date_reported DESC
        ''', (case_id,))

        rows = cursor.fetchall()
        conn.close()

        return [self._row_to_violation(row) for row in rows]

    def update_violation_status(self, violation_id: str, status: str) -> bool:
        """Update violation status"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                UPDATE violations SET status = ? WHERE id = ?
            ''', (status, violation_id))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Error updating status: {e}")
            return False

    def get_violation_summary(self, case_id: str) -> Dict[str, Any]:
        """Get summary statistics for violations"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN severity = 'critical' THEN 1 ELSE 0 END) as critical,
                SUM(CASE WHEN severity = 'major' THEN 1 ELSE 0 END) as major,
                SUM(CASE WHEN severity = 'minor' THEN 1 ELSE 0 END) as minor,
                SUM(CASE WHEN status = 'open' THEN 1 ELSE 0 END) as open,
                SUM(COALESCE(fine_amount, 0)) as total_fines
            FROM violations WHERE case_id = ?
        ''', (case_id,))

        row = cursor.fetchone()
        conn.close()

        return {
            'total_violations': row[0] or 0,
            'critical_violations': row[1] or 0,
            'major_violations': row[2] or 0,
            'minor_violations': row[3] or 0,
            'open_violations': row[4] or 0,
            'total_fines': row[5] or 0
        }

    def calculate_leverage_score(self, case_id: str) -> float:
        """
        Calculate leverage score based on violations
        Higher score = more leverage
        """
        summary = self.get_violation_summary(case_id)

        score = 0.0
        score += summary['critical_violations'] * 10
        score += summary['major_violations'] * 5
        score += summary['minor_violations'] * 2
        score += summary['open_violations'] * 3
        score += (summary['total_fines'] / 1000) * 0.5  # $1000 = 0.5 points

        return min(score, 100.0)  # Cap at 100

    def _row_to_violation(self, row) -> Violation:
        """Convert database row to Violation object"""
        return Violation(
            id=row[0],
            case_id=row[1],
            violation_type=row[2],
            severity=row[3],
            description=row[4],
            location=row[5],
            date_reported=row[6],
            date_discovered=row[7],
            status=row[8],
            responsible_party=row[9],
            citation_number=row[10],
            fine_amount=row[11],
            metadata=json.loads(row[12]) if row[12] else {},
            evidence_ids=json.loads(row[13]) if row[13] else []
        )
