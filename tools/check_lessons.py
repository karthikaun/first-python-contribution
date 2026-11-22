"""Check that every lesson folder has the required files and a valid script.

Usage::

    python tools/check_lessons.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import script_format  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
LESSONS = ROOT / "lessons"
REQUIRED_FILES = ("README.md", "script.md", "exercise.md", "quiz.md")
FOLDER_RE = re.compile(r"^(\d{2}|[A-Z])-[a-z0-9-]+$")
MAX_MINUTES = 10


def check_lesson(folder: Path) -> list[str]:
    out: list[str] = []
    if not FOLDER_RE.match(folder.name):
        out.append("folder name should look like '04-just-enough-git'")
    for name in REQUIRED_FILES:
        if not (folder / name).is_file():
            out.append(f"missing {name}")
    script_path = folder / "script.md"
    if script_path.is_file():
        script = script_format.load(script_path)
        out.extend(script_format.problems(script))
        out.extend(check_captures(folder, script))
        out.extend(check_stated_time(folder, script))
        if script.minutes > MAX_MINUTES:
            out.append(f"script is about {script.minutes:.0f} minutes; keep it under {MAX_MINUTES}")
    return out


TIME_RE = re.compile(r"\*\*Time:\*\* (\d+) minute video")


def check_stated_time(folder: Path, script: script_format.Script) -> list[str]:
    """The README's "**Time:** N minute video" must match the script's length."""
    readme = folder / "README.md"
    if not readme.is_file():
        return []
    m = TIME_RE.search(readme.read_text(encoding="utf-8"))
    if not m:
        return ['README.md needs a line like "**Time:** 3 minute video"']
    stated = int(m.group(1))
    if abs(stated - script.minutes) > 1:
        return [f"README says a {stated} minute video, but the script is about {script.minutes:.1f} minutes"]
    return []


def check_captures(folder: Path, script: script_format.Script) -> list[str]:
    """Browser scenes with image: must point at a capture, with the highlight inside it."""
    from render_video import png_size

    out = []
    for scene in script.scenes:
        image = scene.fields.get("image")
        if scene.visual != "browser" or not image:
            continue
        path = folder / image
        if not path.is_file():
            out.append(f"scene {scene.number}: {image} is missing (run tools/capture_pages.py)")
            continue
        if scene.fields.get("highlight"):
            w, h = png_size(path)
            x, y, bw, bh = (int(v) for v in scene.fields["highlight"].split(","))
            if x < 0 or y < 0 or x + bw > w or y + bh > h:
                out.append(f"scene {scene.number}: highlight {x},{y},{bw},{bh} is outside the {w}x{h} capture")
    return out


def lesson_folders() -> list[Path]:
    return sorted(p for p in LESSONS.iterdir() if p.is_dir() and not p.name.startswith("_"))


def main() -> int:
    failed = False
    for folder in lesson_folders():
        problems = check_lesson(folder)
        status = "ok" if not problems else "FAIL"
        print(f"{status:4} {folder.name}")
        for p in problems:
            print(f"     - {p}")
        failed |= bool(problems)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
