
from pathlib import Path
import argparse
from ignore import merge_patterns, should_skip  

def main():
    parser = argparse.ArgumentParser(description="ContextWeaver with Git-Aware Ignore Support")
    parser.add_argument("path", nargs="?", default=".", help="Path to the repository root")
    parser.add_argument("--use-gitignore", action="store_true", default=True, help="Respect .gitignore and .git/info/exclude (default: on)")
    parser.add_argument("--no-default-ignores", action="store_true", help="Disable built-in default ignore patterns")
    parser.add_argument("--ignore", type=str, default="", help='Comma-separated extra ignore patterns (e.g., "**/*.map,coverage/**")')
    parser.add_argument("--verbose", action="store_true", help="Print SKIP/ADD decisions while scanning")
    args = parser.parse_args()

    repo_root = Path(args.path).resolve()
    extra_ignores = [s.strip() for s in args.ignore.split(",") if s.strip()]
    patterns = merge_patterns(
        use_defaults=not args.no_default_ignores,
        use_gitignore=args.use_gitignore,
        extra_ignores=extra_ignores,
        repo_root=repo_root,
    )

    if args.verbose:
        print(f"Scanning repository: {repo_root}")
        print(f"Total ignore patterns: {len(patterns)}")
        for pat in patterns: print("  -", pat)
        print("-" * 60)

    kept_files, skipped = [], 0
    for p in repo_root.rglob("*"):
        if p.is_dir(): continue
        rel = str(p.relative_to(repo_root))
        if should_skip(rel, patterns):
            skipped += 1
            if args.verbose: print(f"SKIP {rel}")
            continue
        if args.verbose: print(f"ADD  {rel}")
        kept_files.append(p)

    print("\n" + "=" * 60)
    print(f"Total kept files   : {len(kept_files)}")
    print(f"Total skipped files: {skipped}")
    print("=" * 60)

    out = Path("contextweaver_output.txt")
    with out.open("w", encoding="utf8") as f:
        for p in kept_files: f.write(f"{p.relative_to(repo_root)}\n")
    print(f"File list saved to: {out}")

if __name__ == "__main__":
    main()
