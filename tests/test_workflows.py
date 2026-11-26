"""Guards for the GitHub Actions workflows."""

import re
from pathlib import Path

WORKFLOWS = Path(__file__).resolve().parent.parent / ".github" / "workflows"
BOTS = ["first-commit.yml", "exercise-2-merge.yml", "graduate.yml"]


def test_bots_only_check_and_comment():
    """The bots never merge: a maintainer reviews and merges every learner PR."""
    for name in BOTS:
        text = (WORKFLOWS / name).read_text(encoding="utf-8")
        assert "gh pr merge" not in text, f"{name} must not merge"
        assert "contents: read" in text and "contents: write" not in text, f"{name} needs no write access to code"
        assert "gh pr comment" in text


def test_no_lesson_says_a_bot_merges():
    """The lessons and videos must say what the bots do: check and comment."""
    root = WORKFLOWS.parent.parent
    pages = [*root.glob("*.md"), *root.glob("lessons/*/*.md"), *root.glob("publishing/**/*.md")]
    pages += [*root.glob("first-commits/README.md"), *root.glob("practice/README.md")]
    claim = re.compile(r"bots? (?:check(?:s)? and )?merges?\b|it comments,? (?:and )?merges", re.IGNORECASE)
    for page in pages:
        text = " ".join(page.read_text(encoding="utf-8").replace(">", " ").split())
        assert not claim.search(text), f"{page.relative_to(root)} says a bot merges; a maintainer does"


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
