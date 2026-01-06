"""
Configuration loader with caching and validation.
Loads persona configurations and validates system setup.
"""
import json
from functools import lru_cache
from typing import Dict, Any, Optional
from pathlib import Path

from .constants import CONFIG_DIR, PERSONA_MAPPING
from ..exceptions.errors import ConfigurationError


class ConfigLoader:
    """Handles loading and caching of configuration files."""

    _instance: Optional['ConfigLoader'] = None

    def __new__(cls):
        """Singleton pattern to ensure only one config loader exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the config loader."""
        if self._initialized:
            return
        self._config_dir = Path(CONFIG_DIR)
        self._validate_config_directory()
        self._initialized = True

    def _validate_config_directory(self) -> None:
        """Validate that the config directory exists and is readable."""
        if not self._config_dir.exists():
            raise ConfigurationError(
                f"Configuration directory not found: {self._config_dir}"
            )
        if not self._config_dir.is_dir():
            raise ConfigurationError(
                f"Configuration path is not a directory: {self._config_dir}"
            )

    @lru_cache(maxsize=10)
    def load_persona(self, role: str) -> Dict[str, Any]:
        """
        Load a persona configuration file with caching.

        Args:
            role: The role name (Architect, Planner, Developer, QA)

        Returns:
            Dictionary containing persona configuration

        Raises:
            ConfigurationError: If the persona file cannot be loaded
        """
        # Handle special case: Developer role uses Steve.json
        if role == "Developer":
            filename = "Steve.json"
        else:
            filename = PERSONA_MAPPING.get(role, f"{role}.json")

        file_path = self._config_dir / filename

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                persona_data = json.load(f)

            # Validate required fields
            self._validate_persona(persona_data, role)
            return persona_data

        except FileNotFoundError:
            raise ConfigurationError(
                f"Persona configuration not found: {file_path}"
            )
        except json.JSONDecodeError as e:
            raise ConfigurationError(
                f"Invalid JSON in persona file {file_path}: {e}"
            )
        except Exception as e:
            raise ConfigurationError(
                f"Failed to load persona {role}: {e}"
            )

    def _validate_persona(self, persona_data: Dict[str, Any], role: str) -> None:
        """
        Validate that a persona has required fields.

        Args:
            persona_data: The loaded persona dictionary
            role: The role name for error messages

        Raises:
            ConfigurationError: If validation fails
        """
        required_fields = ['name', 'role', 'instructions']
        missing_fields = [f for f in required_fields if f not in persona_data]

        if missing_fields:
            raise ConfigurationError(
                f"Persona '{role}' missing required fields: {missing_fields}"
            )

    def reload_persona(self, role: str) -> Dict[str, Any]:
        """
        Force reload a persona configuration, bypassing cache.

        Args:
            role: The role name to reload

        Returns:
            Updated persona configuration
        """
        # Clear the cache for this specific role
        self.load_persona.cache_clear()
        return self.load_persona(role)

    def get_all_personas(self) -> Dict[str, Dict[str, Any]]:
        """
        Load all available persona configurations.

        Returns:
            Dictionary mapping role names to persona data
        """
        personas = {}
        for role in PERSONA_MAPPING.keys():
            try:
                personas[role] = self.load_persona(role)
            except ConfigurationError as e:
                # Log warning but continue
                print(f"Warning: Could not load persona {role}: {e}")
        return personas


# Global instance for easy access
config_loader = ConfigLoader()
