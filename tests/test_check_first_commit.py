import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from check_first_commit import check_changes, check_source, format_comment, validate  # noqa: E402

GOOD = 'name = "Ada Lovelace"\ngithub = "ada"\nmessage = "Learning Python!"\n'


def test_valid_file():
    assert check_source(GOOD, "ada").ok


def test_login_case_insensitive_in_value():
    assert check_source(GOOD, "Ada").ok


def test_comments_are_allowed():
    assert check_source("# my first commit\n" + GOOD, "ada").ok


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ('name = "Ada\ngithub = "ada"\nmessage = "hi"\n', "isn't valid Python"),
        ('name = "Ada"\ngithub = "ada"\n', "`message` is missing"),
        (GOOD + 'age = "30"\n', "unexpected variable `age`"),
        (GOOD + 'name = "Again"\n', "`name` is set twice"),
        (GOOD + "import os\n", "each line should look like"),
        ('name = "Ada"\ngithub = "ada"\nmessage = 42\n', "each line should look like"),
        ('name = ""\ngithub = "ada"\nmessage = "hi"\n', "`name` is empty"),
        ('name = "Your Name"\ngithub = "ada"\nmessage = "hi"\n', "still says"),
        ('name = "Ada"\ngithub = "someone-else"\nmessage = "hi"\n', "must match"),
        ('name = "Ada"\ngithub = "ada"\nmessage = "' + "x" * 300 + '"\n', "too long"),
        ("x" * 3000, "too long"),
    ],
)
def test_invalid_sources(source, expected):
    result = check_source(source, "ada")
    assert not result.ok
    assert any(expected in e for e in result.errors), result.errors


def test_only_own_file_is_fine():
    result, path = check_changes([("A", "first-commits/ada.py")], "ada")
    assert result.ok and path == "first-commits/ada.py"


def test_other_files_rejected():
    result, _ = check_changes([("A", "first-commits/ada.py"), ("M", "README.md")], "ada")
    assert any("other than" in e for e in result.errors)


def test_wrong_file_name_explained():
    result, path = check_changes([("A", "first-commits/Ada Lovelace.py")], "ada")
    assert path is None
    assert any("named after your GitHub username" in e for e in result.errors)


def test_wrong_case_file_name():
    result, path = check_changes([("A", "first-commits/ADA.py")], "ada")
    assert path == "first-commits/ADA.py"
    assert any("capital letters" in e for e in result.errors)


def test_deleting_own_file_rejected():
    result, path = check_changes([("D", "first-commits/ada.py")], "ada")
    assert path is None and not result.ok


def test_comment_mentions_user():
    assert "@ada" in format_comment(check_source(GOOD, "ada"), "ada")
    assert "fix" in format_comment(check_source("", "ada"), "ada")


def test_validate_against_real_git(tmp_path, monkeypatch):
    def git(*args):
        return subprocess.run(["git", *args], cwd=tmp_path, check=True, capture_output=True, text=True).stdout.strip()

    git("init", "-q", "-b", "main")
    git("config", "user.email", "t@example.com")
    git("config", "user.name", "t")
    (tmp_path / "first-commits").mkdir()
    (tmp_path / "first-commits" / "README.md").write_text("hi\n")
    git("add", ".")
    git("commit", "-qm", "base")
    base = git("rev-parse", "HEAD")
    (tmp_path / "first-commits" / "ada.py").write_text(GOOD)
    git("add", ".")
    git("commit", "-qm", "add ada")
    head = git("rev-parse", "HEAD")

    monkeypatch.chdir(tmp_path)
    assert validate("ada", base, head).ok
    assert not validate("bob", base, head).ok


@pytest.mark.parametrize(
    ("paths", "expected"),
    [
        (["first-commits/ada.py"], True),
        (["first-commits/ada.py", "README.md"], True),
        (["first-commits/README.md"], False),
        (["lessons/02-first-pr-in-browser/README.md"], False),
        (["first-commits/sub/ada.py"], False),
    ],
)
def test_is_learner_pr(paths, expected):
    from check_first_commit import is_learner_pr

    assert is_learner_pr(paths) is expected


def test_main_is_silent_on_an_exercise_2_pr_that_carries_the_first_commit(tmp_path, monkeypatch, capsys):
    """PR #47: the Exercise 2 bot reviews it, so this bot must not ask to undo the exercise files."""
    from check_first_commit import NOT_A_LEARNER_PR, main

    def git(*args):
        return subprocess.run(["git", *args], cwd=tmp_path, check=True, capture_output=True, text=True).stdout.strip()

    git("init", "-q", "-b", "main")
    git("config", "user.email", "t@example.com")
    git("config", "user.name", "t")
    (tmp_path / "README.md").write_text("hi\n")
    git("add", ".")
    git("commit", "-qm", "base")
    base = git("rev-parse", "HEAD")
    for folder in ("first-commits", "practice/greetings", "practice/tests"):
        (tmp_path / folder).mkdir(parents=True)
    (tmp_path / "first-commits/ada.py").write_text(GOOD)
    git("add", ".")
    git("commit", "-qm", "first commit")
    first = git("rev-parse", "HEAD")
    (tmp_path / "practice/greetings/ada.py").write_text("def greet(name: str) -> str:\n    return name\n")
    (tmp_path / "practice/tests/test_ada.py").write_text("from greetings.ada import greet\n")
    git("add", ".")
    git("commit", "-qm", "exercise 2")
    monkeypatch.chdir(tmp_path)

    assert main(["--login", "ada", "--base", base, "--head", first]) == 0  # the first PR itself is still checked
    capsys.readouterr()
    assert main(["--login", "ada", "--base", base, "--head", git("rev-parse", "HEAD")]) == NOT_A_LEARNER_PR
    assert capsys.readouterr().out == ""


def test_a_syntax_error_says_its_line_once():
    """Python adds "(detected at line 3)" to some messages; the bot used to add "(line 3)" after it."""
    errors = check_source('name = "Ada"\ngithub = "ada"\nmessage = "Hello\n', "ada").errors
    assert errors == [
        "Your file isn't valid Python: unterminated string literal (line 3). "
        'A missing quote `"` is the most common cause.'
    ]
