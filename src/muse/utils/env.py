"""
Muse has several environment variables that can be set to configure its behavior. These are:
- MUSE_PLUGINS: The directory where Muse will look for plugins.
- MUSE_DATA: The directory where Muse will look for data files.
- MUSE_MODELS: The directory where Muse will look for models.
- MUSE_CACHE: The directory where Muse will store cached data.
"""

import os
from pathlib import Path

__all__ = ["get_plugins_dir", "get_data_dir", "get_models_dir", "get_cache_dir"]


def _get_env_var(name: str) -> str | None:
    return os.environ.get(name)


def _get_muse_var(name: str) -> str | None:
    return (
        _get_env_var(f"MUSE_{name.upper()}")
        or str(Path(_get_env_var("HOME"), ".muse", name.lower()))
        if _get_env_var("HOME")
        else None
    )


def get_plugins_dir() -> str | None:
    return _get_muse_var("PLUGINS")


def get_data_dir() -> str | None:
    return _get_muse_var("DATA")


def get_models_dir() -> str | None:
    return _get_muse_var("MODELS")


def get_cache_dir() -> str | None:
    return _get_muse_var("CACHE")
