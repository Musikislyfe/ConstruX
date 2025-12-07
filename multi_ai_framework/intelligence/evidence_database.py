"""
Evidence Database Management
Centralized storage and retrieval of case evidence
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import json
import sqlite3
from pathlib import Path


@dataclass
class Evidence:
    """Evidence item structure"""
    id: str
    case_id: str
    evidence_type: str  # document, testimony, physical, digital, etc.
    description: str
    source: str
    date_collected: str
    relevance_score: float  # 0-1 score
    metadata: Dict[str, Any]
    file_path: Optional[str] = None
    verified: bool = False
    tags: List[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class EvidenceDatabase:
    """Manages evidence collection and storage"""

    def __init__(self, db_path: str = "evidence.db"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS evidence (
                id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                evidence_type TEXT NOT NULL,
                description TEXT NOT NULL,
                source TEXT NOT NULL,
                date_collected TEXT NOT NULL,
                relevance_score REAL NOT NULL,
                metadata TEXT NOT NULL,
                file_path TEXT,
                verified INTEGER DEFAULT 0,
                tags TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_case_id ON evidence(case_id)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_evidence_type ON evidence(evidence_type)
        ''')

        conn.commit()
        conn.close()

    def add_evidence(self, evidence: Evidence) -> bool:
        """Add evidence to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO evidence (
                    id, case_id, evidence_type, description, source,
                    date_collected, relevance_score, metadata, file_path,
                    verified, tags
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                evidence.id,
                evidence.case_id,
                evidence.evidence_type,
                evidence.description,
                evidence.source,
                evidence.date_collected,
                evidence.relevance_score,
                json.dumps(evidence.metadata),
                evidence.file_path,
                1 if evidence.verified else 0,
                json.dumps(evidence.tags)
            ))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Error adding evidence: {e}")
            return False

    def get_evidence_by_case(self, case_id: str) -> List[Evidence]:
        """Get all evidence for a case"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM evidence WHERE case_id = ?
            ORDER BY relevance_score DESC, date_collected DESC
        ''', (case_id,))

        rows = cursor.fetchall()
        conn.close()

        return [self._row_to_evidence(row) for row in rows]

    def get_evidence_by_type(self, case_id: str, evidence_type: str) -> List[Evidence]:
        """Get evidence filtered by type"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM evidence WHERE case_id = ? AND evidence_type = ?
            ORDER BY relevance_score DESC
        ''', (case_id, evidence_type))

        rows = cursor.fetchall()
        conn.close()

        return [self._row_to_evidence(row) for row in rows]

    def search_evidence(self, case_id: str, search_term: str) -> List[Evidence]:
        """Search evidence by description or tags"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM evidence
            WHERE case_id = ? AND (
                description LIKE ? OR
                tags LIKE ?
            )
            ORDER BY relevance_score DESC
        ''', (case_id, f'%{search_term}%', f'%{search_term}%'))

        rows = cursor.fetchall()
        conn.close()

        return [self._row_to_evidence(row) for row in rows]

    def update_evidence_verification(self, evidence_id: str, verified: bool) -> bool:
        """Update evidence verification status"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                UPDATE evidence SET verified = ? WHERE id = ?
            ''', (1 if verified else 0, evidence_id))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Error updating verification: {e}")
            return False

    def get_evidence_summary(self, case_id: str) -> Dict[str, Any]:
        """Get summary statistics for case evidence"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN verified = 1 THEN 1 ELSE 0 END) as verified,
                AVG(relevance_score) as avg_relevance,
                evidence_type,
                COUNT(*) as type_count
            FROM evidence
            WHERE case_id = ?
            GROUP BY evidence_type
        ''', (case_id,))

        rows = cursor.fetchall()

        # Get total counts
        cursor.execute('''
            SELECT COUNT(*), SUM(verified), AVG(relevance_score)
            FROM evidence WHERE case_id = ?
        ''', (case_id,))

        total_row = cursor.fetchone()
        conn.close()

        return {
            'total_evidence': total_row[0] or 0,
            'verified_evidence': total_row[1] or 0,
            'average_relevance': total_row[2] or 0,
            'evidence_by_type': {
                row[3]: {'count': row[4]}
                for row in rows
            }
        }

    def _row_to_evidence(self, row) -> Evidence:
        """Convert database row to Evidence object"""
        return Evidence(
            id=row[0],
            case_id=row[1],
            evidence_type=row[2],
            description=row[3],
            source=row[4],
            date_collected=row[5],
            relevance_score=row[6],
            metadata=json.loads(row[7]),
            file_path=row[8],
            verified=bool(row[9]),
            tags=json.loads(row[10]) if row[10] else []
        )

    def export_case_evidence(self, case_id: str, output_path: str):
        """Export all case evidence to JSON file"""
        evidence_list = self.get_evidence_by_case(case_id)

        output = {
            'case_id': case_id,
            'export_date': datetime.now().isoformat(),
            'summary': self.get_evidence_summary(case_id),
            'evidence': [e.to_dict() for e in evidence_list]
        }

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)
