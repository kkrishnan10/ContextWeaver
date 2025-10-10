from __future__ import annotations
import argparse, sys
from pathlib import Path

# Plain imports so `python src/main.py ...` works
from scanner import iter_files
from formatter import make_snapshot
from utils import estimate_tokens, normalize_patterns, to_stderr

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="ContextWeaver: generate a text snapshot of your repo/files")
    p.add_argument("targets", nargs="+", help="Files or directories to include in snapshot")
    p.add_argument("-o", "--output", help="Write snapshot to file instead of stdout")
    p.add_argument("--include", dest="include", metavar="PATTERNS", type=str, help="Comma-separated glob patterns, e.g. '*.py,*.md'")
    p.add_argument("--tokens", action="store_true", help="Print ~token count (~chars/4) to stderr")
    p.add_argument("-V", "--verbose", action="store_true", help="Verbose messages to stderr")
    p.add_argument("-l", "--line-numbers", action="store_true", help="Prefix each line with its 1-based number")
    return p

def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    patterns = normalize_patterns(args.include)

    if args.verbose:
        to_stderr(f"[info] include patterns: {patterns or 'ALL'}")
        to_stderr(f"[info] scanning targets: {args.targets}")

    files = list(iter_files(args.targets, patterns, verbose=args.verbose))
    if args.verbose:
        to_stderr(f"[info] files included: {len(files)}")

    snapshot = make_snapshot(files, add_line_numbers=args.line_numbers)
    if args.tokens:
        to_stderr(f"[tokens] ~{estimate_tokens(snapshot)}")

    if args.output:
        Path(args.output).write_text(snapshot, encoding="utf-8")
        if args.verbose:
            to_stderr(f"[info] wrote snapshot -> {args.output}")
    else:
        sys.stdout.write(snapshot)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
