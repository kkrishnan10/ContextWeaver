
import argparse
import os
import sys
import subprocess
from typing import Iterable, List, Tuple

TOOL_VERSION = "0.1.0"
EXCLUDED_DIRS = {"venv"}



def eprint(msg: str) -> None:
    print(msg, file=sys.stderr)


def get_all_files(paths: Iterable[str], verbose: bool = False) -> List[str]:
    """
    Return a list of absolute file paths under the given paths.
    Skips hidden files/dirs (starting with '.') and EXCLUDED_DIRS.
    """
    files: List[str] = []
    for p in paths:
        ap = os.path.abspath(p)

        if os.path.isfile(ap):
            if not os.path.basename(ap).startswith("."):
                files.append(ap)
                if verbose:
                    eprint(f"Reading file: {ap}")
            else:
                if verbose:
                    eprint(f"Skipping hidden file: {ap}")

        elif os.path.isdir(ap):
            if verbose:
                eprint(f"Processing directory: {ap}")
            for root, dirs, fnames in os.walk(ap):
                
                dirs[:] = [
                    d for d in dirs
                    if not d.startswith(".") and d not in EXCLUDED_DIRS
                ]
                for fname in fnames:
                    if fname.startswith("."):
                        continue
                    fpath = os.path.join(root, fname)
                    files.append(fpath)
                    if verbose:
                        eprint(f"Reading file: {fpath}")
        else:
            if verbose:
                eprint(f"Skipping non-existent path: {ap}")

    return files


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


def estimate_tokens(s: str) -> int:
    """
    Very rough token estimate (OpenAI-like): ~4 chars/token heuristic.
    Good enough for quick counts without external deps.
    """
    
    return 0 if not s else max(1, (len(s) // 4))


def get_git_info(repo_path: str) -> str:
    """Best-effort git info; safe if repo or git is missing."""
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_path, text=True, stderr=subprocess.PIPE
        ).strip()
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_path, text=True, stderr=subprocess.PIPE
        ).strip()
        author = subprocess.check_output(
            ["git", "log", "-1", "--pretty=%ae"],
            cwd=repo_path, text=True, stderr=subprocess.PIPE
        ).strip()
        date = subprocess.check_output(
            ["git", "log", "-1", "--pretty=%ad"],
            cwd=repo_path, text=True, stderr=subprocess.PIPE
        ).strip()
        return f"- Commit: {commit}\n- Branch: {branch}\n- Author: {author}\n- Date: {date}"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "Not a git repository"



def main() -> None:
    parser = argparse.ArgumentParser(description="Repository Context Packager")

    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {TOOL_VERSION}"
    )


    parser.add_argument(
        "paths",
        nargs="+",
        help="Paths to files or directories to include in the context."
    )

    
    parser.add_argument(
        "-o", "--output",
        help="Write output to this file instead of stdout."
    )

   
    parser.add_argument(
        "--tokens",
        action="store_true",
        help="Estimate and display an approximate token count."
    )

    
    parser.add_argument(
        "--verbose", "-V",
        action="store_true",
        help="Print progress messages to stderr while scanning/reading files."
    )

   
    args = parser.parse_args()

   
    files = get_all_files(args.paths, verbose=args.verbose)
    if not files:
        eprint("Error: no files found under the provided paths.")
        sys.exit(1)

    
    out = open(args.output, "w", encoding="utf-8") if args.output else sys.stdout
    total_chars = 0
    try:
        
        root = os.path.abspath(args.paths[0])
        meta = get_git_info(root)
        print("## Repo", file=out)
        print(meta, file=out)
        print("", file=out)

        
        for f in files:
            content, err = read_text(f)

            print(header_for(f), file=out)
            print("```", file=out)
            if err:
                print(f"[ERROR] {err}", file=out)
            else:
                total_chars += len(content)
                print(content, end="" if content.endswith("\n") else "\n", file=out)

            print("```", file=out)
            print("", file=out)

        
        if args.tokens:
            approx_tokens = estimate_tokens("".join(files) + str(total_chars))
            print("## Summary", file=out)
            print(f"- Files: {len(files)}", file=out)
            print(f"- Approx chars printed: {total_chars}", file=out)
            print(f"- Approx tokens: {approx_tokens}", file=out)

    finally:
        if args.output:
            out.close()


if __name__ == "__main__":
    main()
