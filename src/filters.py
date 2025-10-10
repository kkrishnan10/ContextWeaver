<<<<<<< HEAD
<<<<<<< HEAD
=======
cat <<'EOF' > src/filters.py
>>>>>>> 48a21fe (Create filters.py)
=======
>>>>>>> 41e3ea2 (Update filters.py)
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
<<<<<<< HEAD
<<<<<<< HEAD
=======
EOF
>>>>>>> 48a21fe (Create filters.py)
=======
>>>>>>> 41e3ea2 (Update filters.py)
