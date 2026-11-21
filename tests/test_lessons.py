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
        "```\n"
        'x = "y"\n'
        "\n"
        ">       assert x\n"
        "```\n\n"
        "> Narration.\n"
    )
    assert script.title == "Demo"
    first, second = script.scenes
    assert first.fields["title"] == "Hello"
    assert first.bullets == ["one", "two"]
    assert first.narration == "First line second line."
    assert second.code == ['x = "y"', "", ">       assert x"]
    assert second.narration == "Narration."
    assert script_format.problems(script) == []


def test_problems_reported():
    script = script_format.parse("# Video script: X\n\n## Scene 2: Bad\nvisual: slide\n")
    found = script_format.problems(script)
    assert any("expected scene number 1" in p for p in found)
    assert any("needs 'title:'" in p for p in found)
    assert any("no narration" in p for p in found)


def test_lesson_04_examples_pass_the_bot():
    """The example files in Lesson 04 must be exactly what the bot accepts."""
    import re

    from check_exercise_2 import check_greeting, check_test

    text = (ROOT / "lessons/04-second-pr-from-terminal/README.md").read_text()
    blocks = re.findall(r"```python\n(.*?)```", text, re.DOTALL)
    greeting = next(b for b in blocks if "def greet" in b)
    test = next(b for b in blocks if "from greetings" in b)
    assert check_greeting(greeting).ok
    assert check_test(test, "ada-lovelace").ok
    namespace: dict = {}
    exec(greeting, namespace)
    assert "Sam" in namespace["greet"]("Sam")


def test_code_font_fits_long_lines():
    import render_video

    assert render_video.code_font_px(['x = "y"']) == 50
    long = render_video.code_font_px(["(.venv) $ " + "x" * 90])
    assert long * 0.61 * 100 <= render_video.CODE_WIDTH_PX
    assert 'class="prompt">(.venv) $ </span>git' in render_video._terminal_line("(.venv) $ git status")


def test_stated_time_must_match_script(tmp_path):
    words = " ".join(["word"] * 450)  # about 3 minutes at 150 words a minute
    script = script_format.parse(f"# Video script: X\n\n## Scene 1: S\nvisual: slide\ntitle: T\n\n> {words}\n")
    (tmp_path / "README.md").write_text("# L\n\n**Time:** 3 minute video · 5 minute exercise\n")
    assert check_lessons.check_stated_time(tmp_path, script) == []
    (tmp_path / "README.md").write_text("# L\n\n**Time:** 8 minute video · 5 minute exercise\n")
    assert "8 minute video" in check_lessons.check_stated_time(tmp_path, script)[0]
    (tmp_path / "README.md").write_text("# L\n")
    assert "needs a line" in check_lessons.check_stated_time(tmp_path, script)[0]
