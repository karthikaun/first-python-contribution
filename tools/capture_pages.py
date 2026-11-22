"""Capture the real web pages shown in a lesson's browser scenes.

Usage::

    python tools/capture_pages.py lessons/02-first-pr-in-browser

For every ``visual: browser`` scene with an ``image:`` field, it opens the
scene's ``url`` in headless Chrome and saves a screenshot to that path inside
the lesson folder. Optional fields:

    height: 2400          capture a taller page (default 900)
    crop: x,y,w,h         keep only this region of the capture

Chrome runs with a fresh, empty profile, so pages are captured logged out:
no account, cookies or notifications of whoever runs this end up in a video.
Re-run it whenever GitHub's pages change.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import script_format  # noqa: E402

CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
WIDTH = 1440
LOAD_BUDGET_MS = 10_000  # let the page's JavaScript finish before the screenshot


def parse_box(text: str) -> tuple[int, int, int, int]:
    x, y, w, h = (int(part) for part in text.split(","))
    return x, y, w, h


def capture(url: str, out: Path, height: int = 900, budget_ms: int = LOAD_BUDGET_MS) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as profile:
        subprocess.run(
            [
                str(CHROME),
                "--headless=new",
                "--disable-gpu",
                "--hide-scrollbars",
                f"--user-data-dir={profile}",
                f"--virtual-time-budget={budget_ms}",
                f"--window-size={WIDTH},{height}",
                f"--screenshot={out}",
                url,
            ],
            check=True,
            capture_output=True,
        )


def crop(path: Path, box: tuple[int, int, int, int]) -> None:
    x, y, w, h = box
    tmp = path.with_suffix(".crop.png")
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(path), "-vf", f"crop={w}:{h}:{x}:{y}", str(tmp)],
        check=True,
    )
    tmp.replace(path)


def looks_blank(path: Path) -> bool:
    """True if the image is (nearly) one flat colour: the page hadn't drawn yet."""
    gray = subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-i", str(path), "-vf", "scale=96:-1,format=gray", "-f", "rawvideo", "-"],
        check=True,
        capture_output=True,
    ).stdout
    return max(gray) - min(gray) < 16


def capture_scene(scene: script_format.Scene, out: Path) -> None:
    """Capture a scene's page, retrying with more load time when it comes out blank (a busy machine)."""
    for attempt in range(3):
        capture(scene.fields["url"], out, int(scene.fields.get("height", 900)), LOAD_BUDGET_MS * (attempt + 1))
        if scene.fields.get("crop"):
            crop(out, parse_box(scene.fields["crop"]))
        if not looks_blank(out):
            return
    raise RuntimeError(f"{out.name} is still blank after 3 tries: is {scene.fields['url']} up?")


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("usage: python tools/capture_pages.py LESSON-FOLDER", file=sys.stderr)
        return 2
    lesson = Path(argv[0]).resolve()
    script = script_format.load(lesson / "script.md")
    done: set[str] = set()
    for scene in script.scenes:
        image = scene.fields.get("image")
        if scene.visual != "browser" or not image or image in done:
            continue
        out = lesson / image
        capture_scene(scene, out)
        done.add(image)
        print(f"captured {scene.fields['url']} -> {out.relative_to(lesson.parent.parent)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
