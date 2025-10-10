from __future__ import annotations
from typing import Optional, List
import sys

def estimate_tokens(text: str) -> int:
    """Rough token estimate (~chars/4)."""
    return len(text) // 4

def to_stderr(msg: str) -> None:
    """Write message to stderr."""
    sys.stderr.write(msg + "\n")

def normalize_patterns(patterns: Optional[str]) -> List[str]:
    """Split comma-separated patterns into a clean list."""
    if not patterns:
        return []
    return [p.strip() for p in patterns.split(",") if p.strip()]
