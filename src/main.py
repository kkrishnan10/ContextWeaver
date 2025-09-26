
import argparse
import sys
import os
import subprocess
from typing import List, Iterable, Tuple

TOOL_VERSION = "0.1.0"
EXCLUDED_DIRS = {"venv"}

def eprint(msg: str) -> None:
    print(msg, file=sys.stderr)

def iter_files(paths: Iterable[str], verbose: bool = False) -> List[str]:
    """Yield absolute file paths under the given paths, skipping hidden files/dirs and EXCLUDED_DIRS."""
    results: List[str] = []
    for p in paths:
        ap = os.path.abspath(p)
        if os.path.isfile(ap):
            if not os.path.basename(ap).startswith('.'):
                results.append(ap)
                if verbose:
                    eprint(f"Reading file: {ap}")
        elif os.path.isdir(ap):
            if verbose:
                eprint(f"Processing directory: {ap}")
            for root, dirs, files in os.walk(ap):
                
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in EXCLUDED_DIRS]
                for fname in files:
                    if fname.startswith('.'):
                        continue
                    fpath = os.path.join(root, fname)
                    results.append(fpath)
                    if verbose:
                        eprint(f"Reading file: {fpath}")
        else:
            if verbose:
                eprint(f"Skipping non-existent path: {ap}")
    return results

def read_text(path: str) -> Tuple[str, str]:
    """Return (content, error). error is '' on success."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read(), ""
    except Exception as ex:
        return "", f"{type(ex).__name__}: {ex}"

def header_for(path: str) -> str:
    rel = os.path.relpath(path, start=os.getcwd())
    return f"### File: {rel}"

def main() -> None:
    parser = argparse.ArgumentParser(description="ContextWeaver: print repository files as a single context.")
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {TOOL_VERSION}")

    parser.add_argument("paths", nargs="+", help="Files or directories to include")

    
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Print progress to stderr while scanning/reading files")

    
    parser.add_argument("-o", "--output", help="Write output to this file instead of stdout")

    args = parser.parse_args()

    files = iter_files(args.paths, verbose=args.verbose)
    if not files:
        eprint("Error: no files found under the provided paths.")
        sys.exit(1)

    out = open(args.output, "w", encoding="utf-8") if args.output else sys.stdout
    try:
        for f in files:
            content, err = read_text(f)
            print(header_for(f), file=out)
            print("```", file=out)
            if err:
                print(f"[ERROR] {err}", file=out)
            else:
                print(content, end="" if content.endswith("\n") else "\n", file=out)
            print("```", file=out)
    finally:
        if args.output:
            out.close()

if __name__ == "__main__":
    main()
