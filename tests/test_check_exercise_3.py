import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import check_exercise_3 as ex3  # noqa: E402

FIXED = """
import re


def slugify(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
"""

GOOD_TEST = """
import pytest
from textkit import slugify


@pytest.mark.parametrize(("title", "slug"), [("Hello  World", "hello-world"), ("Hello, World!", "hello-world")])
def test_slugify_separators(title, slug):
    assert slugify(title) == slug
"""

WEAK_TEST = """
from textkit import slugify


def test_slugify_two_words():
    assert slugify("Hello World") == "hello-world"
"""


def write(tmp_path, name, text):
    path = tmp_path / name
    path.write_text(text)
    return path


def test_planted_bug_is_still_planted():
    assert ex3.check_behaviour(ex3.load_slugify(ex3.TEXTKIT)), "practice/textkit.py must stay buggy for learners"


def test_reference_fix_passes(tmp_path):
    assert ex3.check_behaviour(ex3.load_slugify(write(tmp_path, "fixed.py", FIXED))) == []


def test_good_test_catches_bug_and_passes_on_fix(tmp_path):
    test_file = write(tmp_path, "test_good.py", GOOD_TEST)
    assert ex3.run_test_against(ex3.BUGGY_SOURCE, test_file) == 1
    assert ex3.run_test_against(FIXED, test_file) == 0


def test_weak_test_misses_bug(tmp_path):
    assert ex3.run_test_against(ex3.BUGGY_SOURCE, write(tmp_path, "test_weak.py", WEAK_TEST)) == 0


@pytest.mark.parametrize(
    ("subject", "tip"),
    [
        ("Fixed slugify", "imperative"),
        ("Fix slugify.", "full stop"),
        ("x" * 80, "72"),
        ("fix slugify separators", "capital"),
    ],
)
def test_commit_message_tips(subject, tip):
    assert any(tip in t for t in ex3.check_commit_message(subject))


@pytest.mark.parametrize("subject", ["Fix slugify for repeated separators", "fix: collapse separators in slugify"])
def test_good_commit_messages(subject):
    assert ex3.check_commit_message(subject) == []


def test_news_fragments(tmp_path):
    write(tmp_path, "README.md", "readme")
    write(tmp_path, "empty.bugfix.md", "")
    assert ex3.news_fragments(tmp_path) == []
    write(tmp_path, "slugify.bugfix.md", "Fixed it.")
    assert [p.name for p in ex3.news_fragments(tmp_path)] == ["slugify.bugfix.md"]
