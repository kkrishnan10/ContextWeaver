from ignore import should_skip

def test_should_skip_basic_pattern():
    patterns = ["*.py", "README.md"]

    assert should_skip("main.py", patterns)
    assert should_skip("README.md", patterns)
    assert not should_skip("docs/notes.txt", patterns)
