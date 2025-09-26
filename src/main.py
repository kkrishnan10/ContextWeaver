import os
import sys
import argparse
import subprocess
from datetime import datetime

def get_git_info(path):
    try:
        commit = subprocess.check_output(
            ["git", "-C", path, "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        branch = subprocess.check_output(
            ["git", "-C", path, "rev-parse", "--abbrev-ref", "HEAD"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        author = subprocess.check_output(
            ["git", "-C", path, "log", "-1", "--pretty=format:%an <%ae>"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        date = subprocess.check_output(
            ["git", "-C", path, "log", "-1", "--pretty=format:%cd"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        return commit, branch, author, date
    except subprocess.CalledProcessError:
        return None, None, None, None

def collect_files(paths, include_patterns=None, verbose=False):
    collected = []
    for path in paths:
        if os.path.isdir(path):
            if verbose:
                print(f"Processing directory: {path}", file=sys.stderr)
            for root, dirs, files in os.walk(path):
                for file in files:
                    filepath = os.path.join(root, file)
                    if include_patterns and not any(
                        filepath.endswith(p) for p in include_patterns
                    ):
                        continue
                    if verbose:
                        print(f"Reading file: {filepath}", file=sys.stderr)
                    collected.append(filepath)
        elif os.path.isfile(path):
            if include_patterns and not any(
                path.endswith(p) for p in include_patterns
            ):
                continue
            if verbose:
                print(f"Reading file: {path}", file=sys.stderr)
            collected.append(path)
        else:
            print(f"Skipping invalid path: {path}", file=sys.stderr)
    return collected

def main():
    parser = argparse.ArgumentParser(description="Repository Context Packager")

    parser.add_argument(
        "-v", "--version",
        action="version",
        version="ContextWeaver 0.1"
    )

    parser.add_argument(
        "paths",
        nargs="+",
        help="Paths to files or directories to include in the context."
    )

    parser.add_argument(
        "-o", "--output",
        help="Path to the output file. If not specified, prints to stdout."
    )

    parser.add_argument(
        "--tokens",
        action="store_true",
        help="Estimate and display the token count for the context."
    )

    parser.add_argument(
        "--include",
        help="Comma-separated list of file extensions/patterns to include."
    )

   
    parser.add_argument(
        "--verbose", "-V",
        action="store_true",
        help="Print progress messages to stderr as files/directories are processed."
    )

    args = parser.parse_args()

    include_patterns = None
    if args.include:
        include_patterns = [p.strip() for p in args.include.split(",")]

    files = collect_files(args.paths, include_patterns, verbose=args.verbose)

   
    output_lines = []
    output_lines.append("# Repository Context\n")

    repo_path = os.path.abspath(args.paths[0])
    output_lines.append("## File System Location\n")
    output_lines.append(repo_path + "\n")

    commit, branch, author, date = get_git_info(repo_path)
    output_lines.append("## Git Info\n")
    if commit:
        output_lines.append(f"- Commit: {commit}")
        output_lines.append(f"- Branch: {branch}")
        output_lines.append(f"- Author: {author}")
        output_lines.append(f"- Date: {date}\n")
    else:
        output_lines.append("Not a git repository\n")

    output_lines.append("## Structure\n")
    for f in files:
        rel_path = os.path.relpath(f, repo_path)
        output_lines.append(rel_path)
    output_lines.append("\n")

    output_lines.append("## File Contents\n")
    for f in files:
        try:
            with open(f, "r", encoding="utf-8") as file:
                content = file.read()
            output_lines.append(f"### File: {f}\n```")
            output_lines.append(content)
            output_lines.append("```\n")
        except Exception as e:
            print(f"Error reading {f}: {e}", file=sys.stderr)

    output_lines.append("## Summary\n")
    output_lines.append(f"- Total files: {len(files)}")
    total_lines = sum(len(open(f, "r", encoding="utf-8").readlines()) for f in files)
    output_lines.append(f"- Total lines: {total_lines}")

    final_output = "\n".join(output_lines)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as out_file:
            out_file.write(final_output)
    else:
        print(final_output)

if __name__ == "__main__":
    main()
