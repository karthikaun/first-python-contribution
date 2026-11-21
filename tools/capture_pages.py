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


def capture(url: str, out: Path, height: int = 900) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as profile:
        subprocess.run(
            [
                str(CHROME),
                "--headless=new",
                "--disable-gpu",
                "--hide-scrollbars",
                f"--user-data-dir={profile}",
                f"--virtual-time-budget={LOAD_BUDGET_MS}",
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
        capture(scene.fields["url"], out, int(scene.fields.get("height", 900)))
        if scene.fields.get("crop"):
            crop(out, parse_box(scene.fields["crop"]))
        done.add(image)
        print(f"captured {scene.fields['url']} -> {out.relative_to(lesson.parent.parent)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
