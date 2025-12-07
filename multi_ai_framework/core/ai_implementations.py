"""
Concrete AI Model Implementations
Integration with Claude, Gemini, DeepSeek, and ChatGPT APIs
"""

from typing import Dict, Any, Optional
import os
from .base_ai import BaseAI, AICapability, AIResponse


class ClaudeAI(BaseAI):
    """Claude AI - Strategic Command & Narrative Development"""

    def __init__(self, api_key: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        super().__init__(api_key, config)
        self.model_name = "claude"
        self.capabilities = [
            AICapability.STRATEGIC_REASONING,
            AICapability.NARRATIVE_DEVELOPMENT,
            AICapability.LEGAL_ANALYSIS,
            AICapability.CODE_GENERATION,
            AICapability.DATA_SYNTHESIS
        ]
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')

    def execute_task(self, task: Dict[str, Any]) -> AIResponse:
        """Execute task using Claude API"""
        try:
            # Import here to avoid dependency issues if not installed
            from anthropic import Anthropic

            client = Anthropic(api_key=self.api_key)

            prompt = task.get('prompt', '')
            model = task.get('model', 'claude-sonnet-4-5-20250929')
            max_tokens = task.get('max_tokens', 8000)

            response = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            content = response.content[0].text
            metadata = {
                'model': model,
                'usage': response.usage.model_dump() if hasattr(response, 'usage') else {},
                'stop_reason': response.stop_reason
            }

            return self._create_response(
                task_id=task.get('id', 'unknown'),
                content=content,
                metadata=metadata,
                success=True
            )

        except Exception as e:
            return self._create_response(
                task_id=task.get('id', 'unknown'),
                content="",
                metadata={},
                success=False,
                error=str(e)
            )

    def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if Claude can handle this task"""
        required_fields = ['prompt']
        return all(field in task for field in required_fields)


class GeminiAI(BaseAI):
    """Gemini AI - Real-time Research & Data Gathering"""

    def __init__(self, api_key: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        super().__init__(api_key, config)
        self.model_name = "gemini"
        self.capabilities = [
            AICapability.REAL_TIME_RESEARCH,
            AICapability.DATA_SYNTHESIS,
            AICapability.CODE_GENERATION
        ]
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')

    def execute_task(self, task: Dict[str, Any]) -> AIResponse:
        """Execute task using Gemini API"""
        try:
            # Import here to avoid dependency issues
            import google.generativeai as genai

            genai.configure(api_key=self.api_key)

            model_name = task.get('model', 'gemini-2.0-flash-exp')
            model = genai.GenerativeModel(model_name)

            prompt = task.get('prompt', '')
            response = model.generate_content(prompt)

            content = response.text
            metadata = {
                'model': model_name,
                'candidates': len(response.candidates) if hasattr(response, 'candidates') else 0
            }

            return self._create_response(
                task_id=task.get('id', 'unknown'),
                content=content,
                metadata=metadata,
                success=True
            )

        except Exception as e:
            return self._create_response(
                task_id=task.get('id', 'unknown'),
                content="",
                metadata={},
                success=False,
                error=str(e)
            )

    def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if Gemini can handle this task"""
        required_fields = ['prompt']
        return all(field in task for field in required_fields)


class DeepSeekAI(BaseAI):
    """DeepSeek AI - Advanced Reasoning & Modeling"""

    def __init__(self, api_key: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        super().__init__(api_key, config)
        self.model_name = "deepseek"
        self.capabilities = [
            AICapability.ADVANCED_MODELING,
            AICapability.STRATEGIC_REASONING,
            AICapability.CODE_GENERATION,
            AICapability.LEGAL_ANALYSIS
        ]
        self.api_key = api_key or os.getenv('DEEPSEEK_API_KEY')

    def execute_task(self, task: Dict[str, Any]) -> AIResponse:
        """Execute task using DeepSeek API"""
        try:
            # DeepSeek uses OpenAI-compatible API
            from openai import OpenAI

            client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.deepseek.com"
            )

            model = task.get('model', 'deepseek-chat')
            prompt = task.get('prompt', '')

            response = client.chat.completions.create(
                model=model,
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                max_tokens=task.get('max_tokens', 4000)
            )

            content = response.choices[0].message.content
            metadata = {
                'model': model,
                'usage': response.usage.model_dump() if hasattr(response, 'usage') else {},
                'finish_reason': response.choices[0].finish_reason
            }

            return self._create_response(
                task_id=task.get('id', 'unknown'),
                content=content,
                metadata=metadata,
                success=True
            )

        except Exception as e:
            return self._create_response(
                task_id=task.get('id', 'unknown'),
                content="",
                metadata={},
                success=False,
                error=str(e)
            )

    def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if DeepSeek can handle this task"""
        required_fields = ['prompt']
        return all(field in task for field in required_fields)


class ChatGPTAI(BaseAI):
    """ChatGPT AI - Communication & Optimization"""

    def __init__(self, api_key: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        super().__init__(api_key, config)
        self.model_name = "chatgpt"
        self.capabilities = [
            AICapability.COMMUNICATION_OPTIMIZATION,
            AICapability.DATA_SYNTHESIS,
            AICapability.CODE_GENERATION
        ]
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')

    def execute_task(self, task: Dict[str, Any]) -> AIResponse:
        """Execute task using ChatGPT API"""
        try:
            from openai import OpenAI

            client = OpenAI(api_key=self.api_key)

            model = task.get('model', 'gpt-4')
            prompt = task.get('prompt', '')

            response = client.chat.completions.create(
                model=model,
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                max_tokens=task.get('max_tokens', 4000)
            )

            content = response.choices[0].message.content
            metadata = {
                'model': model,
                'usage': response.usage.model_dump() if hasattr(response, 'usage') else {},
                'finish_reason': response.choices[0].finish_reason
            }

            return self._create_response(
                task_id=task.get('id', 'unknown'),
                content=content,
                metadata=metadata,
                success=True
            )

        except Exception as e:
            return self._create_response(
                task_id=task.get('id', 'unknown'),
                content="",
                metadata={},
                success=False,
                error=str(e)
            )

    def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if ChatGPT can handle this task"""
        required_fields = ['prompt']
        return all(field in task for field in required_fields)
