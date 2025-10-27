from __future__ import annotations
import fnmatch
from pathlib import Path
from typing import Iterable, List

DEFAULT_IGNORES: List[str] = [
    "node_modules/","dist/","build/","*.log",".DS_Store",".env",".env.*",".venv/","__pycache__/",
]

def _read_patterns_file(p: Path) -> list[str]:
    patterns: list[str] = []
    if p.exists():
        for line in p.read_text(encoding="utf8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            patterns.append(line)
    return patterns

def load_gitignore(repo_root: Path) -> list[str]:
    patterns: list[str] = []
    patterns += _read_patterns_file(repo_root / ".gitignore")
    patterns += _read_patterns_file(repo_root / ".git" / "info" / "exclude")
    return patterns

def merge_patterns(use_defaults: bool, use_gitignore: bool, extra_ignores: Iterable[str], repo_root: Path) -> list[str]:
    merged: list[str] = []
    if use_defaults: merged.extend(DEFAULT_IGNORES)
    if use_gitignore: merged.extend(load_gitignore(repo_root))
    if extra_ignores: merged.extend([p for p in extra_ignores if p])
    seen, deduped = set(), []
    for pat in merged:
        if pat not in seen:
            deduped.append(pat); seen.add(pat)
    return deduped

def should_skip(rel_path: str, patterns: Iterable[str]) -> bool:
    path = rel_path.replace("\\", "/")
    for pat in patterns:
        p = pat.replace("\\", "/")
        if p.endswith("/"):
            if path == p[:-1] or path.startswith(p): return True
            if fnmatch.fnmatch(path, p + "**"): return True
        if fnmatch.fnmatch(path, p): return True
        if not p.endswith("/") and fnmatch.fnmatch(path, p + "/**"): return True
    return False
