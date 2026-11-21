import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import capture_pages  # noqa: E402
import check_lessons  # noqa: E402
import render_video  # noqa: E402
import script_format  # noqa: E402

LESSON = Path(__file__).resolve().parent.parent / "lessons" / "01-first-pr-in-browser"


def test_png_size_of_real_capture():
    assert render_video.png_size(LESSON / "captures" / "repo.png") == (1440, 900)


def test_capture_layout_scales_highlight():
    scale, box = render_video.capture_layout((1440, 900), "100,200,40,20")
    assert scale == min(render_video.CAPTURE_MAX_W / 1440, render_video.CAPTURE_MAX_H / 900)
    assert box == tuple(round(v * scale) for v in (100, 200, 40, 20))
    assert render_video.capture_layout((300, 100), None) == (1.4, None)


def test_browser_scene_uses_capture():
    script = script_format.load(LESSON / "script.md")
    scene = next(s for s in script.scenes if s.fields.get("image") == "captures/repo.png")
    html = render_video.scene_html(scene, script.title, LESSON)
    assert "captures/repo.png" in html and 'class="spot"' in html


def test_browser_scene_without_capture_is_placeholder():
    scene = script_format.Scene(1, "x", {"visual": "browser", "url": "https://example.com", "caption": "c"})
    assert "screen capture goes here" in render_video.scene_html(scene, "t", LESSON)


def test_parse_box():
    assert capture_pages.parse_box("1,2,3,4") == (1, 2, 3, 4)


def test_highlight_outside_capture_is_reported(tmp_path):
    (tmp_path / "captures").mkdir()
    (tmp_path / "captures" / "repo.png").write_bytes((LESSON / "captures" / "repo.png").read_bytes())
    script = script_format.parse(
        "# Video script: X\n\n## Scene 1: S\nvisual: browser\nurl: u\ncaption: c\n"
        "image: captures/repo.png\nhighlight: 1400,880,100,100\n\n> Hi.\n"
        "\n## Scene 2: T\nvisual: browser\nurl: u\ncaption: c\nimage: captures/missing.png\n\n> Hi.\n"
    )
    problems = check_lessons.check_captures(tmp_path, script)
    assert any("outside" in p for p in problems)
    assert any("missing" in p for p in problems)
