"""
Configuration Manager
Handles API keys, settings, and environment configuration
"""

from typing import Dict, Any, Optional
import os
import json
from pathlib import Path


class ConfigManager:
    """Manages configuration for multi-AI framework"""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._default_config_path()
        self.config: Dict[str, Any] = {}
        self.load()

    def _default_config_path(self) -> str:
        """Get default config path"""
        home = Path.home()
        config_dir = home / '.multi_ai_framework'
        config_dir.mkdir(parents=True, exist_ok=True)
        return str(config_dir / 'config.json')

    def load(self) -> Dict[str, Any]:
        """Load configuration from file and environment"""
        # Try to load from file
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {}

        # Override with environment variables if present
        self._load_from_environment()

        return self.config

    def _load_from_environment(self):
        """Load API keys from environment variables"""
        env_mappings = {
            'ANTHROPIC_API_KEY': 'anthropic_api_key',
            'GOOGLE_API_KEY': 'google_api_key',
            'DEEPSEEK_API_KEY': 'deepseek_api_key',
            'OPENAI_API_KEY': 'openai_api_key'
        }

        for env_var, config_key in env_mappings.items():
            if env_var in os.environ:
                self.config[config_key] = os.environ[env_var]

    def save(self) -> bool:
        """Save configuration to file"""
        try:
            # Don't save API keys to file for security
            save_config = {
                k: v for k, v in self.config.items()
                if not k.endswith('_api_key')
            }

            with open(self.config_path, 'w') as f:
                json.dump(save_config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        """Set configuration value"""
        self.config[key] = value

    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for service"""
        key_map = {
            'anthropic': 'anthropic_api_key',
            'claude': 'anthropic_api_key',
            'google': 'google_api_key',
            'gemini': 'google_api_key',
            'deepseek': 'deepseek_api_key',
            'openai': 'openai_api_key',
            'chatgpt': 'openai_api_key'
        }

        config_key = key_map.get(service.lower())
        if config_key:
            return self.config.get(config_key)
        return None

    def validate_api_keys(self) -> Dict[str, bool]:
        """Validate that API keys are configured"""
        required_keys = [
            'anthropic_api_key',
            'google_api_key',
            'deepseek_api_key',
            'openai_api_key'
        ]

        validation = {}
        for key in required_keys:
            validation[key] = key in self.config and bool(self.config[key])

        return validation

    def get_framework_config(self) -> Dict[str, Any]:
        """Get complete framework configuration"""
        return {
            'api_keys': {
                'anthropic_api_key': self.get('anthropic_api_key'),
                'google_api_key': self.get('google_api_key'),
                'deepseek_api_key': self.get('deepseek_api_key'),
                'openai_api_key': self.get('openai_api_key')
            },
            'max_workers': self.get('max_workers', 4),
            'claude_config': self.get('claude_config', {}),
            'gemini_config': self.get('gemini_config', {}),
            'deepseek_config': self.get('deepseek_config', {}),
            'chatgpt_config': self.get('chatgpt_config', {})
        }

    def create_example_config(self, output_path: Optional[str] = None):
        """Create example configuration file"""
        example = {
            "# Configuration for Multi-AI Framework": "DO NOT commit API keys to version control",
            "max_workers": 4,
            "claude_config": {
                "model": "claude-sonnet-4-5-20250929",
                "max_tokens": 8000
            },
            "gemini_config": {
                "model": "gemini-2.0-flash-exp"
            },
            "deepseek_config": {
                "model": "deepseek-chat"
            },
            "chatgpt_config": {
                "model": "gpt-4"
            },
            "# API Keys - Set these as environment variables": "",
            "# ANTHROPIC_API_KEY": "your-key-here",
            "# GOOGLE_API_KEY": "your-key-here",
            "# DEEPSEEK_API_KEY": "your-key-here",
            "# OPENAI_API_KEY": "your-key-here"
        }

        output_path = output_path or 'config.example.json'
        with open(output_path, 'w') as f:
            json.dump(example, f, indent=2)

        return output_path


def load_config(config_path: Optional[str] = None) -> ConfigManager:
    """Load configuration"""
    return ConfigManager(config_path)


def save_config(config_manager: ConfigManager) -> bool:
    """Save configuration"""
    return config_manager.save()
