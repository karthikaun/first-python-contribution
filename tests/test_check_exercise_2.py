import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from check_exercise_2 import (  # noqa: E402
    check_changes,
    check_greeting,
    check_test,
    expected_paths,
    format_comment,
    module_name,
    validate,
)

ROOT = Path(__file__).resolve().parent.parent
GREETING = (ROOT / "practice/greetings/thejesh23.py").read_text()
TEST = (ROOT / "practice/tests/test_thejesh23.py").read_text()


@pytest.mark.parametrize(
    ("login", "expected"),
    [("ada", "ada"), ("Ada-Lovelace", "ada_lovelace"), ("42cats", "u_42cats"), ("class", "class_")],
)
def test_module_name(login, expected):
    assert module_name(login) == expected


def test_reference_solution_is_valid():
    assert check_greeting(GREETING).ok
    assert check_test(TEST, "thejesh23").ok


def test_changes_exact_pair():
    greet, test = expected_paths("Ada-L")
    assert greet == "practice/greetings/ada_l.py"
    assert check_changes([("A", greet), ("A", test)], "Ada-L").ok
    assert check_changes([("M", greet), ("A", test)], "Ada-L").ok


def test_changes_missing_and_extra():
    greet, _ = expected_paths("ada")
    errors = check_changes([("A", greet), ("M", "README.md")], "ada").errors
    assert any("other than" in e for e in errors)
    assert any("test_ada.py" in e for e in errors)


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("import os\n\ndef greet(name: str) -> str:\n    return name\n", "no imports"),
        ("def greet(name: str) -> str:\n    import os\n    return name\n", "no imports"),
        ("def greet(name):\n    return name\n", "type hint"),
        ("def greet(name: str):\n    return name\n", "return type"),
        ("def greet(a: str, b: str) -> str:\n    return a\n", "exactly one argument"),
        ("def hello(name: str) -> str:\n    return name\n", "define a function"),
        ("def greet(name: str) -> str:\n    return eval(name)\n", "`eval` isn't allowed"),
        ("def greet(name: str) -> str:\n    return name.__class__.__name__\n", "double-underscore"),
        ("x = 1\n\ndef greet(name: str) -> str:\n    return name\n", "only functions"),
        ('def greet(name: str) -> str:\n    return f"Hi {name}\n', "isn't valid Python"),
    ],
)
def test_bad_greetings(source, expected):
    errors = check_greeting(source).errors
    assert any(expected in e for e in errors), errors


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("from greetings.bob import greet\n\ndef test_x():\n    assert greet('a')\n", "import your function"),
        ("from greetings.ada import greet\n", "at least one function"),
        ("import os\nfrom greetings.ada import greet\n\ndef test_x():\n    pass\n", "only module you can import"),
        ("from greetings.ada import greet\n\ndef test_x():\n    open('f')\n", "`open` isn't allowed"),
    ],
)
def test_bad_tests(source, expected):
    errors = check_test(source, "ada").errors
    assert any(expected in e for e in errors), errors


def test_pytest_import_allowed():
    src = "import pytest\nfrom greetings.ada import greet\n\n\ndef test_x():\n    assert greet('a')\n"
    assert check_test(src, "ada").ok


def test_comment_success_and_failure():
    from check_first_commit import Result

    assert "Merging" in format_comment(Result(), "ada", "success", "u")
    failed = format_comment(Result(), "ada", "failure", "https://run")
    assert "https://run" in failed and "Merging" not in failed


def test_validate_against_real_git(tmp_path, monkeypatch):
    def git(*args):
        return subprocess.run(["git", *args], cwd=tmp_path, check=True, capture_output=True, text=True).stdout.strip()

    git("init", "-q", "-b", "main")
    git("config", "user.email", "t@example.com")
    git("config", "user.name", "t")
    (tmp_path / "practice/greetings").mkdir(parents=True)
    (tmp_path / "practice/tests").mkdir(parents=True)
    (tmp_path / "practice/README.md").write_text("hi\n")
    git("add", ".")
    git("commit", "-qm", "base")
    base = git("rev-parse", "HEAD")
    (tmp_path / "practice/greetings/ada.py").write_text(GREETING)
    (tmp_path / "practice/tests/test_ada.py").write_text(TEST.replace("thejesh23", "ada"))
    git("add", ".")
    git("commit", "-qm", "exercise")
    head = git("rev-parse", "HEAD")

    monkeypatch.chdir(tmp_path)
    assert validate("ada", base, head).ok
    assert not validate("bob", base, head).ok
