"""The maintainer congratulation messages the bot workflows post."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS = ["first-commit.yml", "exercise-2-merge.yml"]


def test_each_workflow_posts_an_existing_message_before_merging():
    for name in WORKFLOWS:
        text = (ROOT / ".github" / "workflows" / name).read_text(encoding="utf-8")
        files = re.findall(r"\.github/congrats/([\w-]+\.md)", text)
        assert files, f"{name} posts no congratulation"
        for file in files:
            message = (ROOT / ".github" / "congrats" / file).read_text(encoding="utf-8")
            assert "@{login}" in message, f"{file} should greet the learner"
        assert text.index("Congratulate from the maintainer") < text.index("- name: Merge")
        assert "secrets.MAINTAINER_TOKEN" in text
        token_step = text[text.index("Congratulate from the maintainer") : text.index("- name: Merge")]
        assert "python" not in token_step, "the token step must not run tools a previous step installed"


def test_every_action_is_pinned_to_a_commit():
    for path in (ROOT / ".github" / "workflows").glob("*.yml"):
        for ref in re.findall(r"uses: \S+@(\S+)", path.read_text(encoding="utf-8")):
            assert re.fullmatch(r"[0-9a-f]{40}", ref), f"{path.name}: pin {ref} to a commit SHA"
