from pathlib import Path

from scanner import iter_files


def test_iter_files_from_directory_respects_patterns_and_excludes(tmp_path):
    
    root = tmp_path

    src_dir = root / "src"
    src_dir.mkdir()
    keep_py = src_dir / "keep.py"
    keep_py.write_text("# keep\n", encoding="utf8")

    skip_txt = src_dir / "skip.txt"
    skip_txt.write_text("skip me\n", encoding="utf8")

    hidden_dir = src_dir / ".hidden"
    hidden_dir.mkdir()
    secret_py = hidden_dir / "secret.py"
    secret_py.write_text("# secret\n", encoding="utf8")

    node_modules = root / "node_modules"
    node_modules.mkdir()
    lib_js = node_modules / "lib.js"
    lib_js.write_text("console.log('hi');\n", encoding="utf8")

    files = list(iter_files([str(root)], include_patterns=["*.py"]))

    rel_paths = {f.relative_to(root).as_posix() for f in files}

    assert "src/keep.py" in rel_paths

    assert "src/skip.txt" not in rel_paths
    assert "src/.hidden/secret.py" not in rel_paths
    assert "node_modules/lib.js" not in rel_paths


def test_iter_files_from_single_file_target_respects_patterns(tmp_path):
  
    keep_md = tmp_path / "keep.md"
    keep_md.write_text("# title\n", encoding="utf8")

    other_txt = tmp_path / "other.txt"
    other_txt.write_text("hello\n", encoding="utf8")

    files_md = list(iter_files([str(keep_md)], include_patterns=["*.md"]))
    files_txt = list(iter_files([str(other_txt)], include_patterns=["*.md"]))

    assert [f.name for f in files_md] == ["keep.md"]
    assert files_txt == []


def test_iter_files_includes_all_when_patterns_empty(tmp_path):
   
    root = tmp_path
    (root / "a.txt").write_text("a\n", encoding="utf8")
    (root / "b.py").write_text("b\n", encoding="utf8")

    node_modules = root / "node_modules"
    node_modules.mkdir()
    (node_modules / "ignored.js").write_text("ignored\n", encoding="utf8")

    files = list(iter_files([str(root)], include_patterns=[]))
    rel_paths = {f.relative_to(root).as_posix() for f in files}

   
    assert "a.txt" in rel_paths
    assert "b.py" in rel_paths

    assert "node_modules/ignored.js" not in rel_paths
