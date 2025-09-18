
import argparse, sys, os, subprocess, fnmatch
from pygments.lexers import guess_lexer_for_filename
from pygments.util import ClassNotFound

TOOL_VERSION = "0.1.0"
MAX_BYTES = 16 * 1024
EXCLUDED_DIRS = {".git", ".venv", "venv", "__pycache__"}

def parse_include_patterns(include_arg):
    if not include_arg:
        return None
    
    parts = [p.strip() for p in include_arg.split(",") if p.strip()]
    return parts or None

def matches_includes(path, patterns):
    if not patterns:
        return True
    base = os.path.basename(path)
    return any(fnmatch.fnmatch(base, patt) for patt in patterns)

def get_all_files(paths, include_patterns=None):
    files = []
    for p in paths:
        ap = os.path.abspath(p)
        if os.path.isfile(ap):
            if not os.path.basename(ap).startswith(".") and matches_includes(ap, include_patterns):
                files.append(ap)
        elif os.path.isdir(ap):
            for root, dirs, fs in os.walk(ap):
                dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS and not d.startswith(".")]
                for f in fs:
                    if f.startswith("."):
                        continue
                    fp = os.path.join(root, f)
                    if matches_includes(fp, include_patterns):
                        files.append(fp)
    return files

def get_git_info(base):
    try:
        c = lambda *cmd: subprocess.check_output(cmd, cwd=base, text=True, stderr=subprocess.PIPE).strip()
        return "\n".join([
            f"- Commit: {c('git','rev-parse','HEAD')}",
            f"- Branch: {c('git','rev-parse','--abbrev-ref','HEAD')}",
            f"- Author: {c('git','log','-1','--pretty=format:%an <%ae>')}",
            f"- Date: {c('git','log','-1','--pretty=format:%ad')}",
        ])
    except Exception:
        return "Not a git repository"

def structure_tree(files, base):
    tree = {}
    for fp in files:
        rel = os.path.relpath(fp, base)
        parts = rel.split(os.sep)
        cur = tree
        for part in parts[:-1]:
            cur = cur.setdefault(part, {})
        cur[parts[-1]] = None

    def walk(d, indent=""):
        out = []
        items = sorted(d.items())
        for i,(name,val) in enumerate(items):
            last = (i == len(items) - 1)
            prefix = "└── " if last else "├── "
            out.append(f"{indent}{prefix}{name}")
            if isinstance(val, dict):
                out.extend(walk(val, indent + ("    " if last else "│   ")))
        return out

    return "\n".join(walk(tree))

def read_files(files, base):
    blocks, total_lines, total_chars = [], 0, 0
    for fp in sorted(files):
        try:
            sz = os.path.getsize(fp)
            with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                rel = os.path.relpath(fp, base)
                content = f.read()
                if sz > MAX_BYTES:
                    content = content[:MAX_BYTES] + f"\n... (file truncated > {MAX_BYTES//1024}KB)"
                lang = ""
                try:
                    lexer = guess_lexer_for_filename(fp, content)
                    lang = lexer.aliases[0] if lexer.aliases else ""
                except ClassNotFound:
                    pass
                blocks.append(f"### File: {rel}\n```{lang}\n{content}\n```")
                total_lines += content.count("\n") + 1
                total_chars += len(content)
        except Exception as e:
            print(f"Error reading {fp}: {e}", file=sys.stderr)
    return "\n\n".join(blocks), total_lines, total_chars

def main():
    p = argparse.ArgumentParser(description="ContextWeaver - Repository Context Packager")
    p.add_argument("-v","--version", action="version", version=f"%(prog)s {TOOL_VERSION}")
    p.add_argument("paths", nargs="+", help="Paths to files or directories")
    p.add_argument("-o","--output", help="Write output to file (default: stdout)")
    p.add_argument("--tokens", action="store_true", help="Estimate token count (~chars/4) to stderr")
    p.add_argument("--include", help="Comma-separated glob patterns (e.g. \"*.py,*.md\")")
    args = p.parse_args()

    include_patterns = parse_include_patterns(args.include)

    first_abs = os.path.abspath(args.paths[0])
    base = os.path.dirname(first_abs) if os.path.isfile(first_abs) else first_abs

    files = get_all_files(args.paths, include_patterns)
    if not files:
        print("Error: No files found in the specified paths.", file=sys.stderr)
        sys.exit(1)

    git = get_git_info(base)
    tree = structure_tree(files, base)
    contents, total_lines, total_chars = read_files(files, base)
    summary = f"- Total files: {len(files)}\n- Total lines: {total_lines}"

    out = f"""# Repository Context

## File System Location

{base}

## Git Info

{git}

## Structure

{tree}

## File Contents

{contents}

## Summary

{summary}
""".strip()

    if args.tokens:
        print(f"Estimated tokens: {total_chars//4}", file=sys.stderr)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(out + "\n")
            print(f"Context successfully written to {args.output}", file=sys.stderr)
        except Exception as e:
            print(f"Error writing to file {args.output}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(out)

if __name__ == "__main__":
    main()

