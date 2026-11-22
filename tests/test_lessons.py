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
    """The example files in Lesson 05 must be exactly what the bot accepts."""
    import re

    from check_exercise_2 import check_greeting, check_test

    text = (ROOT / "lessons/05-second-pr-from-terminal/README.md").read_text()
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


BEATS = (
    "# Video script: Demo\n\n"
    "## Scene 1: Slide\nvisual: slide\ntitle: T\nbullets:\n- one\n- two `code`\n\n"
    "> Intro.\n\n> First {gh|g h}.\n\n> Second,\n> still second.\n\n"
    "## Scene 2: Term\nvisual: terminal\nfocus: 1 | 2-3 | all\nnotes:\n- run it\n-\n- done\n"
    "code:\n```\n$ pytest\nE   boom\n1 passed in 0.01s\n```\n\n"
    "> Run.\n\n> Read.\n\n> Done.\n"
)


def test_blank_line_between_blockquotes_starts_a_new_beat():
    slide, term = script_format.parse(BEATS).scenes
    assert slide.beats == ["Intro.", "First {gh|g h}.", "Second, still second."]
    assert slide.narration == "Intro. First g h. Second, still second."
    assert script_format.shown(slide.beats[1]) == "First gh."
    assert slide.focus() == [set(), {1}, {2}]  # title alone, then one bullet per beat
    assert term.focus() == [{1}, {2, 3}, None]
    assert term.notes == ["run it", "-", "done"]
    assert script_format.problems(script_format.parse(BEATS)) == []


def test_one_beat_script_is_unchanged():
    script = script_format.parse("# Video script: X\n\n## Scene 1: S\nvisual: slide\ntitle: T\n\n> One.\n> Two.\n")
    assert script.scenes[0].beats == ["One. Two."]
    assert script.scenes[0].focus() == [None]


def test_beat_problems_reported():
    bad = BEATS.replace("focus: 1 | 2-3 | all", "focus: 1 | 9").replace("- done\n", "")
    found = script_format.problems(script_format.parse(bad))
    assert any("focus: has 2 entries but the narration has 3 beats" in p for p in found)
    assert any("points past the last of 3" in p for p in found)
    assert any("notes: has 2 items" in p for p in found)
    wrong = script_format.parse(BEATS.replace("title: T", "title: T\nlayout: spiral").replace("1 | 2-3", "x | 2-3"))
    found = script_format.problems(wrong)
    assert any("layout must be one of" in p for p in found)
    assert any("can't read focus" in p for p in found)


def test_frames_reveal_bullets_and_terminal_lines():
    import render_video

    slide, term = script_format.parse(BEATS).scenes
    frames = render_video.scene_frames(slide, "Demo", total=2)
    assert len(frames) == 3
    assert frames[0].count('<li class="todo">') == 2
    assert '<li class="on">one</li>' in frames[1] and '<li class="todo">two' in frames[1]
    assert '<li class="done">one</li>' in frames[2] and "<code>code</code>" in frames[2]
    assert '<span class="count">01 / 02</span>' in frames[0]
    assert frames[0].count('<i class="now">') == 1 and frames[0].count('<i class="">') == 1
    assert render_video.scene_html(slide, "Demo") == render_video.scene_frames(slide, "Demo")[-1]

    first, second, last = render_video.scene_frames(term, "Demo")
    assert first.count('class="ln on"') == 1 and first.count('class="ln hide"') == 2
    assert second.count('class="ln on"') == 2 and second.count('class="ln dim"') == 1
    assert 'class="ln hide"' not in last and 'class="ln dim"' not in last
    assert '<div class="note">run it</div>' in first and '<div class="note hide">' in second
    assert 'class="out-err">E   boom' in last and 'class="out-ok">1 passed' in last


def test_slide_layouts():
    import render_video

    def frame(layout, bullets, focus="all"):
        scene = script_format.Scene(1, "S", {"visual": "slide", "title": "T", "layout": layout, "focus": focus})
        scene.bullets, scene.beats = bullets, ["Hi."]
        return render_video.scene_html(scene, "Demo", ROOT / "lessons" / "05-second-pr-from-terminal")

    assert '<div class="badge">Lesson 05</div>' in frame("title", ["sub"])
    assert "Click <b>Commit</b> in <code>a.py</code>" in frame("bullets", ["Click **Commit** in `a.py`"])
    steps = frame("steps", ["a", "b", "c"], "2")
    assert [c in steps for c in ('"step done"', '"step on"', '"step todo"')] == [True] * 3
    cards = frame("cards", ["Docs | Fix a typo | No code", "Bug"])
    assert '<div class="cd">Fix a typo</div><div class="tag">No code</div>' in cards
    assert '<div class="grid two">' in cards and cards.count('class="cd"') == 1


def test_python_highlighting_and_code_focus():
    import render_video

    line = render_video._highlight_python('def greet(name: str) -> str:  # hi "x"')
    assert '<span class="tok-kw">def</span> <span class="tok-fn">greet</span>' in line
    assert '<span class="tok-op">-&gt;</span>' in line and '<span class="tok-com"># hi &quot;x&quot;</span>' in line
    assert '<span class="tok-str">f&quot;Hi {n}&quot;</span>' in render_video._highlight_python('x = f"Hi {n}"')
    scene = script_format.Scene(1, "C", {"visual": "code", "file": "a.py", "focus": "2"}, code=["a = 1", "b = 2"])
    page = render_video.scene_html(scene, "Demo")
    assert page.count('class="ln dim"') == 1 and page.count('class="ln on"') == 1  # code never hides lines
    assert '<span class="wintitle">a.py</span>' in page
    doc = render_video._highlight_python_lines(
        ['    """Turn a title', "    and digits", '    """', "    return x and y"]
    )
    assert doc[1] == '<span class="tok-str">    and digits</span>' and "tok-kw" not in doc[0] + doc[2]
    assert '<span class="tok-kw">and</span>' in doc[3]
    assert render_video._output_class("4 failed, 1 passed in 0.01s") == "out-err"
    assert render_video._output_class("7 passed in 0.01s") == "out-ok"
    scene.fields["lang"] = "text"
    assert 'class="tok-' not in render_video.scene_html(scene, "Demo")


def test_segments_and_subtitles(tmp_path):
    import render_video

    scenes = script_format.parse(BEATS).scenes
    segments = render_video.plan_segments(scenes, tmp_path)
    assert [s.png.name for s in segments[:4]] == ["scene01-1.png", "scene01-2.png", "scene01-3.png", "scene02-1.png"]
    pads = [s.pad for s in segments[:3]]
    assert pads == [render_video.BEAT_PAD_SECONDS, render_video.BEAT_PAD_SECONDS, render_video.PAD_SECONDS]
    single = script_format.parse("# Video script: X\n\n## Scene 1: S\nvisual: slide\ntitle: T\n\n> One. Two.\n")
    assert [s.png.name for s in render_video.plan_segments(single.scenes, tmp_path)] == ["scene01.png"]

    srt = render_video.subtitles([("Say {gh|g h}. Ok.", 4.5, 0.5), ("Next.", 2.0, 0.5)])
    assert "Say gh." in srt and "g h" not in srt
    assert "3\n00:00:04,500 --> 00:00:06,000\nNext." in srt


@pytest.mark.parametrize("folder", check_lessons.lesson_folders(), ids=lambda p: p.name)
def test_every_scene_of_every_lesson_builds_frames(folder):
    import render_video

    script = script_format.load(folder / "script.md")
    for scene in script.scenes:
        frames = render_video.scene_frames(scene, script.title, folder, len(script.scenes))
        assert len(frames) == max(len(scene.beats), 1)
        if scene.visual in ("code", "terminal"):
            height = render_video.CODE_HEIGHT_PX - (render_video.NOTE_HEIGHT_PX if scene.notes else 0)
            px = render_video.code_font_px(scene.code, height)
            longest = max(len(line) for line in scene.code)
            assert px * 0.61 * longest <= render_video.CODE_WIDTH_PX, f"scene {scene.number}: a line is too long"


def test_say_runs_one_at_a_time_and_retries_until_two_runs_agree(monkeypatch, tmp_path):
    """Concurrent or busy-machine `say` garbles some clips: hold a lock, keep a clip two runs agree on."""
    import fcntl

    import render_video

    monkeypatch.setattr(render_video, "SAY_LOCK", tmp_path / "say.lock")
    outputs = iter([b"garbled", b"good", b"good"])
    held = []

    def fake_run(cmd, check):
        with (tmp_path / "say.lock").open("w") as other:
            try:
                fcntl.flock(other, fcntl.LOCK_EX | fcntl.LOCK_NB)
                held.append(False)
            except BlockingIOError:
                held.append(True)
        Path(cmd[cmd.index("-o") + 1]).write_bytes(next(outputs))

    monkeypatch.setattr(render_video.subprocess, "run", fake_run)
    monkeypatch.setattr(render_video.time, "sleep", lambda s: None)
    out = tmp_path / "out.aiff"
    render_video.synthesize("Hello.", out, "Aman", 170)
    assert out.read_bytes() == b"good"
    assert held == [True, True, True]
    assert sorted(p.name for p in tmp_path.iterdir()) == ["out.aiff", "say.lock"]
