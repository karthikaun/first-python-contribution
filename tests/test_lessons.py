import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import check_lessons  # noqa: E402
import script_format  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


@pytest.mark.parametrize("folder", check_lessons.lesson_folders(), ids=lambda p: p.name)
def test_lesson_is_complete(folder):
    assert check_lessons.check_lesson(folder) == []


def test_every_first_commit_file_is_valid():
    sys.path.insert(0, str(ROOT / "tools"))
    from check_first_commit import check_source

    for path in (ROOT / "first-commits").glob("*.py"):
        result = check_source(path.read_text(), path.stem)
        assert result.ok, (path.name, result.errors)


def test_parse_scene_fields():
    script = script_format.parse(
        "# Video script: Demo\n\n"
        "## Scene 1: Start\n"
        "visual: slide\n"
        "title: Hello\n"
        "bullets:\n- one\n- two\n\n"
        "> First line\n> second line.\n\n"
        "## Scene 2: Code\n"
        "visual: code\n"
        "code:\n"
        'x = "y"\n\n'
        "> Narration.\n"
    )
    assert script.title == "Demo"
    first, second = script.scenes
    assert first.fields["title"] == "Hello"
    assert first.bullets == ["one", "two"]
    assert first.narration == "First line second line."
    assert second.code == ['x = "y"']
    assert script_format.problems(script) == []


def test_problems_reported():
    script = script_format.parse("# Video script: X\n\n## Scene 2: Bad\nvisual: slide\n")
    found = script_format.problems(script)
    assert any("expected scene number 1" in p for p in found)
    assert any("needs 'title:'" in p for p in found)
    assert any("no narration" in p for p in found)
