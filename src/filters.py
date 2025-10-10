from __future__ import annotations
import fnmatch
from pathlib import Path

def should_include(path: Path, include_patterns: list[str] | None) -> bool:
    """Return True if file matches any include pattern (or all if None)."""
    if include_patterns is None:
        return True
    name = path.name
    for pat in include_patterns:
        if fnmatch.fnmatch(name, pat):
            return True
    return False

def should_exclude_dir(path: Path) -> bool:
    """Return True if directory should be skipped."""
    return any(name.startswith('.') for name in path.parts)
