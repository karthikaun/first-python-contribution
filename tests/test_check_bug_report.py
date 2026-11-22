import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import check_bug_report as cbr  # noqa: E402


def body(**overrides):
    fields = {
        "searched": "- [X] I searched this repository's issues for my bug",
        "what": "When the bill doesn't divide evenly, the shares don't add up to the total.",
        "steps": "```shell\npython bug-hunt/splitbill.py 10 --people 3\n```",
        "expected": "Shares of $3.34, $3.33 and $3.33, which add up to $10.00 (README.md says so).",
        "actual": "```text\nPerson 1: $3.33\nPerson 2: $3.33\nPerson 3: $3.33\n```",
        "version": "splitbill 1.2.0",
        "python": "Python 3.13.1",
        "os": "macOS 15.1",
    }
    fields.update(overrides)
    return "\n\n".join(f"### {cbr.FIELDS[key]}\n\n{value}" for key, value in fields.items())


GOOD_TITLE = "splitbill: shares don't add up to the total for 3 people"


def marks(report):
    return [mark for mark, _ in report.lines]


def test_a_good_report_passes_and_shows_what_the_bot_saw():
    report = cbr.check(GOOD_TITLE, body())
    assert report.ok, report.lines
    assert "Person 1: $3.34" in report.run
    text = cbr.comment(report, "octocat")
    assert text.startswith(cbr.MARKER)
    assert "A maintainer will review your report" in text


def test_other_issues_are_ignored():
    assert cbr.check("Typo in lesson 4", "The word 'comit' is misspelled.") is None


@pytest.mark.parametrize(
    "steps",
    [
        "python bug-hunt/splitbill.py 50 --tip 15%",
        "$ python3 splitbill.py 50 --people 0",
        "python bug-hunt/splitbill.py 100 --tax 10 --tip 20",
        "`python bug-hunt/splitbill.py 1234.5`",
        "1. cd bug-hunt\n2. py splitbill.py 100 --people=3",
    ],
)
def test_every_planted_bug_can_be_reproduced(steps):
    report = cbr.check(GOOD_TITLE, body(steps=steps))
    assert any("Steps reproduce a bug" in text for _, text in report.lines), report.lines


def test_a_command_that_works_fine_is_not_a_bug():
    report = cbr.check(GOOD_TITLE, body(steps="python bug-hunt/splitbill.py 120 --people 4 --tip 15"))
    assert not report.ok
    assert any("did exactly what README.md says" in text for _, text in report.lines)


def test_steps_need_a_command():
    report = cbr.check(GOOD_TITLE, body(steps="Run it with some numbers"))
    assert any("give the exact command" in text for _, text in report.lines)


def test_huge_numbers_are_not_run():
    report = cbr.check(GOOD_TITLE, body(steps="python bug-hunt/splitbill.py 10 --people 99999999"))
    assert any("bigger than it needs to be" in text for _, text in report.lines)


def test_nothing_from_the_issue_reaches_a_shell(tmp_path):
    marker = tmp_path / "pwned"
    report = cbr.check(GOOD_TITLE, body(steps=f"python bug-hunt/splitbill.py 10; touch {marker} $(touch {marker})"))
    assert not marker.exists()
    assert report is not None


@pytest.mark.parametrize("title", ["splitbill: ", "splitbill: bug", "splitbill: it is not working", "Error"])
def test_vague_titles_fail(title):
    report = cbr.check(title, body())
    assert any("Title" in text and mark == cbr.FAIL for mark, text in report.lines)


def test_unticked_search_box_fails():
    report = cbr.check(GOOD_TITLE, body(searched="- [ ] I searched this repository's issues for my bug"))
    assert not report.ok


def test_screenshots_and_cut_tracebacks_fail():
    shot = cbr.check(GOOD_TITLE, body(actual="![screenshot](https://example.com/a.png)"))
    assert any("not a screenshot" in text for _, text in shot.lines)
    cut = cbr.check(GOOD_TITLE, body(actual="Traceback (most recent call last):\n  File ..."))
    assert any("paste all of it" in text for _, text in cut.lines)


def test_same_expected_and_actual_fails():
    report = cbr.check(GOOD_TITLE, body(expected="It crashes", actual="it crashes"))
    assert not report.ok


def test_missing_versions_fail_and_old_version_warns():
    report = cbr.check(GOOD_TITLE, body(version="latest", python="_No response_", os=""))
    assert marks(report).count(cbr.FAIL) == 3
    old = cbr.check(GOOD_TITLE, body(version="splitbill 1.1.0"))
    assert old.ok and cbr.WARN in marks(old)


def test_needs_work_comment_says_how_to_edit():
    text = cbr.comment(cbr.check("splitbill: bug", body()), "octocat")
    assert "**Edit**" in text and "maintainer" not in text


@pytest.mark.parametrize("people", ["--people 5000", "--people=5000", "--peo 5000", "--p=5000", "--people 0005000"])
def test_every_spelling_of_a_huge_people_count_is_refused(people):
    report = cbr.check(GOOD_TITLE, body(steps=f"python bug-hunt/splitbill.py 10 {people}"))
    assert any("bigger than it needs to be" in text for _, text in report.lines), report.lines


def test_long_arguments_are_refused_and_never_fill_the_comment():
    report = cbr.check(GOOD_TITLE, body(steps="python bug-hunt/splitbill.py 10 --tax " + "1" * 50_000))
    assert any("bigger than it needs to be" in text for _, text in report.lines)
    assert len(cbr.comment(report, "octocat")) < 2_000


def test_the_comment_stays_small_at_the_people_limit():
    report = cbr.check(GOOD_TITLE, body(steps=f"python bug-hunt/splitbill.py 10 --people {cbr.MAX_PEOPLE}"))
    assert len(cbr.comment(report, "octocat")) < 10_000  # GitHub's limit is 65,536


@pytest.mark.parametrize("args", [["-h"], ["--version"], ["--peop"], ["abc"], ["10", "--t", "5"]])
def test_help_version_and_bad_commands_print_nothing_into_the_comment(args, capsys):
    assert not cbr.too_big(args)
    cbr.reference(args)
    assert capsys.readouterr().out == ""


def test_a_shell_comment_after_the_command_is_ignored():
    report = cbr.check(GOOD_TITLE, body(steps="python bug-hunt/splitbill.py 10 --people 3  # important: 3 people"))
    assert any("Steps reproduce a bug" in text for _, text in report.lines), report.lines


def test_python_code_steps_are_not_run_as_a_command():
    assert cbr.command_args("import splitbill\nsplitbill.split(10, 3)") is None


def test_a_short_specific_title_passes():
    report = cbr.check("splitbill: --tip 15% crashes", body())
    assert ("✔", "**Title** says what goes wrong.") in report.lines
