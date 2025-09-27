import argparse, sys, os, subprocess
from pygments.lexers import guess_lexer_for_filename
from pygments.util import ClassNotFound

TOOL_VERSION = "0.1.0"
MAX_BYTES = 16 * 1024  

EXCLUDED_DIRS = {".git", ".venv", "venv", "__pycache__"}

def get_all_files(paths):
    files = []
    for p in paths:
        ap = os.path.abspath(p)
        if os.path.isfile(ap):
            if not os.path.basename(ap).startswith("."):
                files.append(ap)
        elif os.path.isdir(ap):
            for root, dirs, fs in os.walk(ap):
                # skip hidden and excluded dirs
                dirs[:] = [d for d in dirs if not d.startswith(".") and d not in EXCLUDED_DIRS]
                for f in fs:
                    if f.startswith("."):
                        continue
                    files.append(os.path.join(root, f))
    return files

def get_git_info(base):
    try:
        run = lambda *cmd: subprocess.check_output(cmd, cwd=base, text=True, stderr=subprocess.PIPE).strip()
        commit = run("git", "rev-parse", "HEAD")
        branch = run("git", "rev-parse", "--abbrev-ref", "HEAD")
        author = run("git", "log", "-1", "--pretty=format:%an <%ae>")
        date   = run("git", "log", "-1", "--pretty=format:%ad")
        return f"- Commit: {commit}\n- Branch: {branch}\n- Author: {author}\n- Date: {date}"
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
        lines = []
        items = sorted(d.items())
        for i, (name, val) in enumerate(items):
            last = (i == len(items) - 1)
            prefix = "└── " if last else "├── "
            lines.append(f"{indent}{prefix}{name}")
            if isinstance(val, dict):
                lines.extend(walk(val, indent + ("    " if last else "│   ")))
        return lines

    return "\n".join(walk(tree))

def read_files(files, base, line_numbers=False):
    blocks, total_lines, total_chars = [], 0, 0
    for fp in sorted(files):
        try:
            size = os.path.getsize(fp)
            with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                rel = os.path.relpath(fp, base)
                content = f.read()
                if size > MAX_BYTES:
                    content = content[:MAX_BYTES] + f"\n... (file truncated > {MAX_BYTES//1024}KB)"
                lang = ""
                try:
                    lexer = guess_lexer_for_filename(fp, content)
                    lang = lexer.aliases[0] if lexer.aliases else ""
                except ClassNotFound:
                    pass

                out_text = with_line_numbers(content) if line_numbers else content
                blocks.append(f"### File: {rel}\n```{lang}\n{content}\n```")
                total_lines += content.count("\n") + 1
                total_chars += len(out_text)
        except Exception as e:
            print(f"Error reading {fp}: {e}", file=sys.stderr)
    return "\n\n".join(blocks), total_lines, total_chars

def main():
    parser = argparse.ArgumentParser(description="ContextWeaver - Repository Context Packager")
    parser.add_argument("-v","--version", action="version", version=f"%(prog)s {TOOL_VERSION}")
    parser.add_argument("paths", nargs="+", help="Paths to files or directories")
    parser.add_argument("-o","--output", help="Write output to file (default: stdout)")
    parser.add_argument("--tokens", action="store_true", help="Estimate token count (~chars/4) to stderr")
    parser.add_argument("--line-numbers", "-l", action="store_true", help="Prefix each output line with its 1-based line number")
    args = parser.parse_args()

    first_abs = os.path.abspath(args.paths[0])
    base = os.path.dirname(first_abs) if os.path.isfile(first_abs) else first_abs

    files = get_all_files(args.paths)
    if not files:
        print("Error: No files found in the specified paths.", file=sys.stderr)
        sys.exit(1)

    git = get_git_info(base)
    tree = structure_tree(files, base)
    contents, total_lines, total_chars = read_files(files, base, line_numbers=args.line_numbers)
    summary = f"- Total files: {len(files)}\n- Total lines: {total_lines}"

    output = f"""# Repository Context

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
                f.write(output + "\n")
            print(f"Context written to {args.output}", file=sys.stderr)
        except Exception as e:
            print(f"Error writing to file {args.output}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(output)

if __name__ == "__main__":
    main()
