from __future__ import annotations
from pathlib import Path
from typing import Iterator, List
import os, sys

# plain imports so script execution works
from filters import should_include, should_exclude_dir

def iter_files(targets: List[str], include_patterns: List[str], verbose: bool=False) -> Iterator[Path]:
    """Yield files from given targets (files or directories), honoring include patterns."""
    for t in targets:
        p = Path(t)
        if not p.exists():
            if verbose:
                sys.stderr.write(f"[skip] does not exist: {p}\n")
            continue
        if p.is_file():
            rel = p.as_posix()
           if should_include(rel, include_patterns):
    yield f
elif verbose:
    sys.stderr.write(f"[skip] not included by pattern: {rel}\n")

        else:
            for root, dirs, files in os.walk(p):
                # prune excluded dirs
                dirs[:] = [d for d in dirs if not should_exclude_dir(d)]
                for name in files:
                    f = Path(root) / name
                    rel = f.as_posix()
                    if should_include(rel, include_patterns):
                        yield f
                    elif verbose:
                        sys.stderr.write(f"[skip] not included by pattern: {rel}\n")
