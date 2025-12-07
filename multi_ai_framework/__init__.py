"""
Multi-AI Justice League Framework
Coordinated AI orchestration for complex multi-faceted missions
"""

from .missions.mission_orchestrator import MissionOrchestrator
from .core.ai_coordinator import AIJusticeLeague
from .config.config_manager import ConfigManager

__version__ = "1.0.0"

__all__ = [
    'MissionOrchestrator',
    'AIJusticeLeague',
    'ConfigManager'
]
