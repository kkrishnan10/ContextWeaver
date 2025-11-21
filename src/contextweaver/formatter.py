from __future__ import annotations
from pathlib import Path
from typing import List

def read_text_safely(path: Path) -> str:
    """Read file as text, ignoring decode errors."""
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def with_line_numbers(text: str) -> str:
    """Add line numbers to text."""
    lines = text.splitlines()
    return "\n".join(f"{i+1:>6} | {line}" for i, line in enumerate(lines))

def make_snapshot(file_paths: List[Path], add_line_numbers: bool=False) -> str:
    """Combine files into one formatted snapshot string."""
    parts: List[str] = []
    for fp in file_paths:
        content = read_text_safely(fp)
        if add_line_numbers:
            content = with_line_numbers(content)
        header = f"===== FILE: {fp} ====="
        parts.append(header)
        parts.append(content)
    return "\n".join(parts) + ("\n" if parts else "")
