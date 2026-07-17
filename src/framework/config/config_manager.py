"""Centralized, layered configuration management.

Resolution order (highest precedence first):

1. Explicit keyword overrides passed at call time.
2. Environment variables (e.g. ``BROWSER``, ``ENV``, ``HEADLESS``).
3. Environment-specific YAML file (``config-<env>.yaml``).
4. Base ``config.yaml`` defaults.
"""

from __future__ import annotations

import os
import threading
from pathlib import Path
from typing import Any

import yaml

from framework.exceptions.framework_exceptions import FrameworkException

_CONFIG_DIR = Path(__file__).resolve().parents[3] / "config"


class ConfigManager:
    """Thread-safe lazy singleton exposing merged configuration values."""

    _instance: "ConfigManager | None" = None
    _lock = threading.Lock()

    def __init__(self) -> None:
        env = os.getenv("ENV", "qa").lower()
        self._values: dict[str, Any] = self._load_layered_config(env)

    @classmethod
    def get_instance(cls) -> "ConfigManager":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    @staticmethod
    def _load_yaml(path: Path) -> dict[str, Any]:
        if not path.exists():
            return {}
        with path.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle) or {}

    def _load_layered_config(self, env: str) -> dict[str, Any]:
        base = self._load_yaml(_CONFIG_DIR / "config.yaml")
        overlay = self._load_yaml(_CONFIG_DIR / f"config-{env}.yaml")
        if not base and not overlay:
            raise FrameworkException(
                f"No configuration files found in {_CONFIG_DIR} for environment '{env}'"
            )
        merged = {**base, **overlay}
        merged["env"] = env
        return merged

    def get(self, key: str, default: Any = None) -> Any:
        """Return a config value, preferring an env-var override of the same name."""
        env_override = os.getenv(key.upper())
        if env_override is not None:
            return env_override
        return self._values.get(key, default)

    def get_bool(self, key: str, default: bool = False) -> bool:
        value = self.get(key, default)
        if isinstance(value, bool):
            return value
        return str(value).strip().lower() in {"true", "1", "yes"}

    def get_int(self, key: str, default: int = 0) -> int:
        value = self.get(key, default)
        try:
            return int(value)
        except (TypeError, ValueError) as exc:
            raise FrameworkException(f"Config value for '{key}' is not an integer: {value}") from exc
