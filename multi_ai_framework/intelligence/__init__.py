"""
Intelligence Gathering Module
Evidence collection, violation tracking, and research coordination
"""

from .evidence_database import EvidenceDatabase, Evidence
from .violation_tracker import ViolationTracker, Violation
from .research_coordinator import IntelligenceGathering

__all__ = [
    'EvidenceDatabase',
    'Evidence',
    'ViolationTracker',
    'Violation',
    'IntelligenceGathering'
]
