import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import check_pr_description as cpd  # noqa: E402

GOOD = """Fix slugify for repeated spaces and punctuation

Fixes #1234

`slugify` kept punctuation and produced doubled hyphens for repeated
spaces. It now turns every run of non-alphanumeric characters into a
single hyphen and strips hyphens from the ends.

Tested: added a parametrized regression test with the cases from the
issue; the full test suite and ruff pass locally.
"""


def marks(report):
    return [mark for mark, _ in report.lines]


def problems(report):
    return " ".join(text for mark, text in report.lines if mark != cpd.OK)


def with_title(title):
    return title + "\n" + GOOD.split("\n", 1)[1]


def with_body(body):
    return "Fix slugify for repeated spaces and punctuation\n\n" + body


def test_the_lessons_example_passes():
    report = cpd.check(GOOD)
    assert report.ok and marks(report) == [cpd.OK] * 4, report.lines


@pytest.mark.parametrize(
    "title",
    [
        "gh-1234: Fix slugify for repeated spaces",
        "fix: collapse repeated separators in slugify",
        "fix(textkit): collapse repeated separators",
        "Add --version to splitbill",
    ],
)
def test_project_title_formats_pass(title):
    assert cpd.check(with_title(title)).ok


@pytest.mark.parametrize(
    ("title", "why"),
    [
        ("Fix bug", "say what the PR does"),
        ("Update code", "say what the PR does"),
        ("My first PR", "say what the PR does"),
        ("Fixed slugify for repeated spaces", "imperative"),
        ("Fix slugify for repeated spaces.", "full stop"),
        ("Fix slugify so that it handles repeated spaces, leading spaces, trailing spaces and punctuation", "72"),
    ],
)
def test_weak_titles_fail_with_a_reason(title, why):
    report = cpd.check(with_title(title))
    assert not report.ok and why in problems(report)


def test_a_missing_issue_link_fails_and_a_bare_mention_warns():
    body = GOOD.split("\n", 2)[2]
    assert "link the issue" in problems(cpd.check(with_body(body.replace("Fixes #1234\n", ""))))
    mentioned = cpd.check(with_body(body.replace("Fixes #1234", "See #1234")))
    assert mentioned.ok and cpd.WARN in marks(mentioned)
    assert cpd.check(with_body(body.replace("Fixes #1234", "Closes python/cpython#1234"))).ok


def test_only_a_link_is_not_an_explanation():
    report = cpd.check(with_body("Fixes #1234\n\nTested locally."))
    assert "What and why" in problems(report)


def test_testing_must_be_described():
    body = (
        "Fixes #1234\n\n" + "slugify now turns every run of other characters into one hyphen and strips the ends. " * 2
    )
    assert "Testing" in problems(cpd.check(with_body(body)))


def test_template_leftovers_fail():
    report = cpd.check(GOOD + "\n<!-- Describe your changes here -->\n")
    assert "Template text" in problems(report)


def test_headings_and_length_only_warn():
    headed = cpd.check(GOOD.replace("Fixes #1234", "## Summary\n\nFixes #1234"))
    assert headed.ok and "Headings" in problems(headed)
    long = cpd.check(GOOD + "\n" + "This sentence adds detail nobody needs to review the change. " * 20)
    assert long.ok and "Length" in problems(long)


def test_an_issue_number_is_not_a_heading():
    assert "Headings" not in problems(cpd.check(GOOD.replace("Fixes #1234", "#1234 is fixed by this.\nFixes #1234")))


def test_empty_file_and_cli(tmp_path, capsys):
    assert not cpd.check("  \n").ok
    path = tmp_path / "pr.md"
    path.write_text(GOOD, encoding="utf-8")
    assert cpd.main([str(path)]) == 0
    assert "Ready to open" in capsys.readouterr().out
    path.write_text("Fix bug\n\nfixed it", encoding="utf-8")
    assert cpd.main([str(path)]) == 1
    assert cpd.main([str(tmp_path / "missing.md")]) == 2
    assert cpd.main([]) == 2
