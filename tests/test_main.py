import subprocess
import sys
from pathlib import Path


def test_main_generates_output_and_respects_default_ignores(tmp_path):
    """
    Integration test:
    - create a fake repo with one normal file and one in node_modules/
    - run main.py on it
    - ensure output file contains only the kept file
    """
    root = Path(__file__).resolve().parents[1]
    main_py = root / "src" / "main.py"

   
    repo = tmp_path / "repo"
    repo.mkdir()

    keep_file = repo / "keep.py"
    keep_file.write_text("print('keep me')\n", encoding="utf8")

    node_modules_dir = repo / "node_modules"
    node_modules_dir.mkdir()
    ignored_file = node_modules_dir / "ignored.js"
    ignored_file.write_text("console.log('ignore me');\n", encoding="utf8")

    
    result = subprocess.run(
        [sys.executable, str(main_py), str(repo)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
    )

    
    stdout = result.stdout
    assert "Total kept files" in stdout
    assert "Total skipped files" in stdout
    assert "File list saved to" in stdout

    
    out_file = tmp_path / "contextweaver_output.txt"
    assert out_file.exists()

    lines = {line.strip() for line in out_file.read_text(encoding="utf8").splitlines()}

    
    assert "keep.py" in lines
    
    assert "node_modules/ignored.js" not in lines


def test_main_respects_extra_ignore_patterns(tmp_path):
    """
    Use the --ignore flag to exclude a specific pattern, and
    verify that matching files are skipped.
    """
    root = Path(__file__).resolve().parents[1]
    main_py = root / "src" / "main.py"

    repo = tmp_path / "repo2"
    repo.mkdir()

    kept = repo / "keep.txt"
    kept.write_text("ok\n", encoding="utf8")

    extra_ignored = repo / "notes.tmp"
    extra_ignored.write_text("ignore me\n", encoding="utf8")

   
    result = subprocess.run(
        [
            sys.executable,
            str(main_py),
            str(repo),
            "--ignore",
            "*.tmp",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
    )

    out_file = tmp_path / "contextweaver_output.txt"
    assert out_file.exists()

    lines = {line.strip() for line in out_file.read_text(encoding="utf8").splitlines()}

    assert "keep.txt" in lines
    assert "notes.tmp" not in lines
