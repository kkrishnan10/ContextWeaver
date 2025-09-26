
import argparse
import sys
import os
import subprocess
from pygments.lexers import guess_lexer_for_filename
from pygments.util import ClassNotFound

TOOL_VERSION = "0.1.0"

def get_all_files(paths, verbose=False):
    all_files = []
    excluded_dirs = {'venv'}

    for path in paths:
        abs_path = os.path.abspath(path)

        if os.path.isfile(abs_path):
            if not os.path.basename(abs_path).startswith('.'):
                all_files.append(abs_path)
                if verbose:
                    print(f"Reading file: {abs_path}", file=sys.stderr)

        elif os.path.isdir(abs_path):
            if verbose:
                print(f"Processing directory: {abs_path}", file=sys.stderr)
            for root, dirs, files in os.walk(abs_path):
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in excluded_dirs]
                for file in files:
                    if not file.startswith('.'):
                        file_path = os.path.join(root, file)
                        all_files.append(file_path)
                        if verbose:
                            print(f"Reading file: {file_path}", file=sys.stderr)
    return all_files

def get_git_info(repo_path):
    try:
        commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo_path, text=True, stderr=subprocess.PIPE).strip()
        branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=repo_path, text=True, stderr=subprocess.PIPE).strip()
        author = subprocess.check_output(['git', 'log', '-1', '--pretty=format:%an <%ae>'], cwd=repo_path, text=True, stderr=subprocess.PIPE).strip()
        date = subprocess.check_output(['git', 'log', '-1', '--pretty=format:%ad'], cwd=repo_path, text=True, stderr=subprocess.PIPE).strip()
        return f"- Commit: {commit}\n- Branch: {branch}\n- Author: {author}\n- Date: {date}"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "Not a git repository"

def main():
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
        help="Path to the output file. If not specified, prints to standard output."
    )

    parser.add_argument(
        "--tokens",
        action="store_true",
        help="Estimate and display the token count for the context."
    )

    parser.add_argument(
        "--verbose", "-V",
        action="store_true",
        help="Print progress messages to stderr as files/directories are processed."
    )

    args = parser.parse_args()

    file_list = get_all_files(args.paths, verbose=args.verbose)

    if not file_list:
        print("Error: No files found in the specified paths.", file=sys.stderr)
        sys.exit(1)

    # Just a placeholder for now
    print("Context packaging complete!")

if __name__ == "__main__":
    main()
