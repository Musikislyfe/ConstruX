"""
Base AI Interface for Multi-AI Coordination Framework
Defines common interface for all AI models
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import time


class AICapability(Enum):
    """AI Model Capabilities"""
    STRATEGIC_REASONING = "strategic_reasoning"
    REAL_TIME_RESEARCH = "real_time_research"
    ADVANCED_MODELING = "advanced_modeling"
    COMMUNICATION_OPTIMIZATION = "communication_optimization"
    NARRATIVE_DEVELOPMENT = "narrative_development"
    LEGAL_ANALYSIS = "legal_analysis"
    DATA_SYNTHESIS = "data_synthesis"
    CODE_GENERATION = "code_generation"


@dataclass
class AIResponse:
    """Standardized AI response format"""
    model_name: str
    task_id: str
    content: str
    metadata: Dict[str, Any]
    timestamp: float
    success: bool
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            'model_name': self.model_name,
            'task_id': self.task_id,
            'content': self.content,
            'metadata': self.metadata,
            'timestamp': self.timestamp,
            'success': self.success,
            'error': self.error
        }


class BaseAI(ABC):
    """Base class for all AI model integrations"""

    def __init__(self, api_key: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        self.api_key = api_key
        self.config = config or {}
        self.capabilities: List[AICapability] = []
        self.model_name = "base_ai"

    @abstractmethod
    def execute_task(self, task: Dict[str, Any]) -> AIResponse:
        """Execute a task and return standardized response"""
        pass

    @abstractmethod
    def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if this AI can handle the task"""
        pass

    def has_capability(self, capability: AICapability) -> bool:
        """Check if AI has specific capability"""
        return capability in self.capabilities

    def get_capabilities(self) -> List[AICapability]:
        """Get list of AI capabilities"""
        return self.capabilities

    def _create_response(self, task_id: str, content: str,
                        metadata: Dict[str, Any], success: bool = True,
                        error: Optional[str] = None) -> AIResponse:
        """Helper to create standardized response"""
        return AIResponse(
            model_name=self.model_name,
            task_id=task_id,
            content=content,
            metadata=metadata,
            timestamp=time.time(),
            success=success,
            error=error
        )
