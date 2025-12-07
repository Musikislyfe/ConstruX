"""
Execution Coordination Module
Multi-front campaign execution: complaints, media, settlement negotiations
"""

from .complaint_generator import ComplaintGenerator, ComplaintPackage
from .media_coordinator import MediaCoordinator, MediaPackage
from .settlement_negotiator import SettlementNegotiator, NegotiationFramework
from .execution_coordinator import ExecutionCoordination

__all__ = [
    'ComplaintGenerator',
    'ComplaintPackage',
    'MediaCoordinator',
    'MediaPackage',
    'SettlementNegotiator',
    'NegotiationFramework',
    'ExecutionCoordination'
]
