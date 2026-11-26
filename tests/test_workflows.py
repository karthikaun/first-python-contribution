"""Guards for the GitHub Actions workflows."""

import re
from pathlib import Path

WORKFLOWS = Path(__file__).resolve().parent.parent / ".github" / "workflows"
BOTS = ["exercise-2-merge.yml", "graduate.yml"]


def test_only_the_first_commit_bot_merges():
    """A first pull request that passes is merged by the bot, so nobody waits for a maintainer.

    It must merge only the commit it checked, with a merge commit (a squash
    would leave the learner's main out of step), and never run the PR's code.
    """
    text = (WORKFLOWS / "first-commit.yml").read_text(encoding="utf-8")
    merges = re.findall(r"gh pr merge .*", text)
    assert len(merges) == 1
    assert "--merge" in merges[0] and '--match-head-commit "$HEAD"' in merges[0]
    assert "--squash" not in text and "--rebase" not in text and "--admin" not in text
    assert "steps.check.outputs.status == '0'" in text
    assert "persist-credentials: false" in text
    assert "git checkout" not in text and "ref: ${{" not in text, "the PR's code must never be checked out"


def test_the_other_bots_only_check_and_comment():
    """Exercise 2 and graduate pull requests are merged by a maintainer."""
    for name in BOTS:
        text = (WORKFLOWS / name).read_text(encoding="utf-8")
        assert "gh pr merge" not in text, f"{name} must not merge"
        assert "contents: read" in text and "contents: write" not in text, f"{name} needs no write access to code"
        assert "gh pr comment" in text


def test_lessons_say_who_merges():
    """The bot merges the first pull request (Lesson 02). A maintainer merges Exercise 2 and graduates."""
    root = WORKFLOWS.parent.parent

    def words(path: str) -> str:
        return " ".join((root / path).read_text(encoding="utf-8").replace(">", " ").split())

    bot_merges = re.compile(r"bots? (?:check(?:s)? (?:it )?,? ?and )?merges?\b|it comments,? (?:and )?merges", re.I)
    for page in (
        "lessons/05-second-pr-from-terminal/README.md",
        "lessons/05-second-pr-from-terminal/script.md",
        "lessons/15-capstone/README.md",
        "lessons/15-capstone/script.md",
        "practice/README.md",
    ):
        assert not bot_merges.search(words(page)), f"{page} says a bot merges; a maintainer does"
    maintainer_merges = re.compile(r"maintainer (?:reviews (?:it )?and )?merges", re.I)
    for page in (
        "lessons/02-first-pr-in-browser/README.md",
        "lessons/02-first-pr-in-browser/script.md",
        "lessons/02-first-pr-in-browser/exercise.md",
        "first-commits/README.md",
        "publishing/promo/script.md",
    ):
        assert not maintainer_merges.search(words(page)), f"{page} says a maintainer merges the first PR; the bot does"


def test_every_action_is_pinned_to_a_commit():
    for path in WORKFLOWS.glob("*.yml"):
        for ref in re.findall(r"uses: \S+@(\S+)", path.read_text(encoding="utf-8")):
            assert re.fullmatch(r"[0-9a-f]{40}", ref), f"{path.name}: pin {ref} to a commit SHA"


def test_bug_report_bot_only_comments():
    text = (WORKFLOWS / "bug-report.yml").read_text(encoding="utf-8")
    assert "contents: read" in text and "contents: write" not in text
    assert "gh issue close" not in text and "gh issue edit" not in text
    # The issue text reaches the checker only through env: never ${{ }} inside run:
    for block in re.findall(r"run: \|\n((?:\s{10}.*\n?)+)", text):
        assert "${{" not in block
