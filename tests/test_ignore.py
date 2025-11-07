from pathlib import Path

from ignore import (
    DEFAULT_IGNORES,
    load_gitignore,
    merge_patterns,
    should_skip,
)


def test_load_gitignore_reads_gitignore_and_info_exclude(tmp_path):
    """
    Ensure load_gitignore() reads both .gitignore and .git/info/exclude,
    ignores comments/blank lines, and returns all patterns.
    """
    repo_root = tmp_path

    
    (repo_root / ".gitignore").write_text(
        """
        # comment
        *.log
        build/
        """
        .strip()
        + "\n",
        encoding="utf8",
    )

   
    info_dir = repo_root / ".git" / "info"
    info_dir.mkdir(parents=True)
    (info_dir / "exclude").write_text(
        """
        # local exclude
        secret.txt
        """
        .strip()
        + "\n",
        encoding="utf8",
    )

    patterns = load_gitignore(repo_root)

    assert "*.log" in patterns
    assert "build/" in patterns
    assert "secret.txt" in patterns
   
    assert "# comment" not in patterns
    assert "# local exclude" not in patterns


def test_merge_patterns_defaults_only(tmp_path):
    """
    If we enable defaults and disable gitignore/extra patterns,
    the merged result should be a copy of DEFAULT_IGNORES.
    """
    repo_root = tmp_path  

    merged = merge_patterns(
        use_defaults=True,
        use_gitignore=False,
        extra_ignores=[],
        repo_root=repo_root,
    )

    
    assert merged == DEFAULT_IGNORES
    
    merged.append("extra/")
    assert "extra/" not in DEFAULT_IGNORES


def test_merge_patterns_combines_gitignore_and_extra_with_dedup(tmp_path):
    """
    merge_patterns() should combine defaults, gitignore patterns,
    and extra patterns without duplicates.
    """
    repo_root = tmp_path

    
    (repo_root / ".gitignore").write_text(
        "node_modules/\ncustom_ignore/\n", encoding="utf8"
    )

    merged = merge_patterns(
        use_defaults=True,
        use_gitignore=True,
        extra_ignores=["*.log", "custom_ignore/"],
        repo_root=repo_root,
    )

    
    for pat in DEFAULT_IGNORES:
        assert pat in merged

    
    assert "custom_ignore/" in merged

    
    assert "*.log" in merged

   
    assert merged.count("custom_ignore/") == 1


def test_should_skip_respects_directory_patterns():
    """
    Patterns ending with '/' should match any path starting with that prefix.
    """
    patterns = ["node_modules/"]

    assert should_skip("node_modules/react/index.js", patterns)
    assert should_skip("node_modules/package.json", patterns)
   
    assert not should_skip("src/node_modules_extra/file.js", patterns)


def test_should_skip_matches_simple_globs():
    patterns = ["*.py", "README.md"]

    
    assert should_skip("main.py", patterns)
    assert should_skip("README.md", patterns)

    
    assert not should_skip("src/main.py", patterns)


def test_should_skip_handles_windows_style_paths():
    """
    Backslashes should be normalized to forward slashes internally.
    """
    patterns = ["src/*.py"]

    assert should_skip("src/main.py", patterns)
    
    assert should_skip(r"src\\main.py", patterns)
