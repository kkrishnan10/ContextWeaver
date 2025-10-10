from __future__ import annotations
import fnmatch
from typing import List

DEFAULT_EXCLUDES = {".git", "__pycache__", "node_modules", ".venv", ".idea"}

def should_exclude_dir(dirname: str) -> bool:
    """Return True if directory should be excluded."""
    return dirname in DEFAULT_EXCLUDES

def should_include(path: str, patterns: List[str]) -> bool:
    """Return True if path matches any pattern; include all if patterns empty."""
    if not patterns:
        return True
    return any(fnmatch.fnmatch(path, pat) for pat in patterns)
