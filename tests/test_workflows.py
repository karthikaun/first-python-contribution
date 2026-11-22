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


def test_every_action_is_pinned_to_a_commit():
    for path in WORKFLOWS.glob("*.yml"):
        for ref in re.findall(r"uses: \S+@(\S+)", path.read_text(encoding="utf-8")):
            assert re.fullmatch(r"[0-9a-f]{40}", ref), f"{path.name}: pin {ref} to a commit SHA"
