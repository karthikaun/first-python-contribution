"""Build an upload-ready Udemy package from the rendered lesson videos.

Usage (after rendering every lesson with tools/render_video.py)::

    uv run python tools/udemy_package.py

Writes ``dist/udemy/``:

    lectures/NN - Title.mp4    stereo audio, loudness-normalised to -16 LUFS,
                               video copied unchanged (1080p H.264)
    captions/NN - Title.vtt    WebVTT captions from each lesson's .srt
    course-image.png           750x422 course image with no text (Udemy's standard)
    test-video.mp4             a 2.5 minute clip for Udemy's free Test Video review
    UPLOAD.md                  landing page copy, sections and lectures, step by step

The landing page copy comes from publishing/udemy-landing.md and is checked
against Udemy's limits first.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANDING = ROOT / "publishing" / "udemy-landing.md"
OUT = ROOT / "dist" / "udemy"
REPO_URL = "https://github.com/thejesh23/first-python-contribution"
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

TITLE_MAX, SUBTITLE_MAX, LECTURE_TITLE_MAX = 60, 120, 80
DESCRIPTION_MIN_WORDS, OBJECTIVES_MIN = 200, 4
LOUDNESS = "loudnorm=I=-16:TP=-1.5:LRA=11"
TEST_VIDEO_LESSON, TEST_VIDEO_SECONDS = "05-second-pr-from-terminal", 150
MAX_UPLOAD_BYTES = int(9.5 * 1024 * 1024)  # browser automation uploads at most 10 MB per file


@dataclass
class Lecture:
    number: int
    folder: str
    title: str

    @property
    def stem(self) -> str:
        safe = re.sub(r'[\\/*?"<>|]', "", self.title.replace(":", " -"))
        return f"{self.number:02d} - {safe}"


@dataclass
class Section:
    title: str
    lectures: list[Lecture]


def parse_landing(text: str) -> dict[str, str | list[str]]:
    """Split the landing file into its ## sections; list sections become lists."""
    parts = re.split(r"^## (.+)$", text, flags=re.M)[1:]
    out: dict[str, str | list[str]] = {}
    for name, body in zip(parts[::2], parts[1::2], strict=True):
        body = body.strip()
        bullets = [line[2:].strip() for line in body.splitlines() if line.startswith("- ")]
        out[name.strip()] = bullets if bullets and len(bullets) == len(body.splitlines()) else body
    return out


def landing_problems(landing: dict) -> list[str]:
    problems = []
    for key in ("Title", "Subtitle", "Description", "What you'll learn", "Requirements", "Who this course is for"):
        if key not in landing:
            problems.append(f"missing section: {key}")
    title, subtitle = str(landing.get("Title", "")), str(landing.get("Subtitle", ""))
    if len(title) > TITLE_MAX:
        problems.append(f"title is {len(title)} characters; Udemy allows {TITLE_MAX}")
    if "udemy" in title.lower():
        problems.append('the title must not contain "Udemy"')
    if len(subtitle) > SUBTITLE_MAX:
        problems.append(f"subtitle is {len(subtitle)} characters; Udemy allows {SUBTITLE_MAX}")
    words = len(str(landing.get("Description", "")).split())
    if words < DESCRIPTION_MIN_WORDS:
        problems.append(f"description is {words} words; Udemy needs at least {DESCRIPTION_MIN_WORDS}")
    objectives = landing.get("What you'll learn", [])
    if not isinstance(objectives, list) or len(objectives) < OBJECTIVES_MIN:
        problems.append(f"'What you'll learn' needs at least {OBJECTIVES_MIN} bullet points")
    return problems


def parse_sections(curriculum: str, lessons_dir: Path) -> list[Section]:
    """Sections are the curriculum's '## Part N: ...' headings; lectures are their lesson links."""
    sections: list[Section] = []
    number = 0
    for line in curriculum.splitlines():
        part = re.match(r"^## Part \d+: (.+)$", line)
        if part:
            sections.append(Section(part.group(1).strip(), []))
            continue
        link = re.search(r"\(lessons/([^/)]+)/\)", line)
        if sections and link and line.startswith("|"):
            folder = link.group(1)
            heading = (lessons_dir / folder / "README.md").read_text(encoding="utf-8").splitlines()[0]
            title = re.sub(r"^# (Lesson \w+: )?", "", heading).strip()
            number += 1
            sections[-1].lectures.append(Lecture(number, folder, title))
    return sections


def srt_to_vtt(srt: str) -> str:
    body = re.sub(r"(\d{2}:\d{2}:\d{2}),(\d{3})", r"\1.\2", srt.replace("\r\n", "\n"))
    return "WEBVTT\n\n" + body.strip() + "\n"


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, capture_output=True)


def encode_lecture(src: Path, dst: Path) -> None:
    """Stereo, loudness-normalised audio; video copied, or re-encoded if the file is too big."""
    audio = ["-af", LOUDNESS, "-ac", "2", "-ar", "48000", "-c:a", "aac", "-b:a", "128k"]
    run(["ffmpeg", "-y", "-i", str(src), "-c:v", "copy", *audio, "-movflags", "+faststart", str(dst)])
    if dst.stat().st_size > MAX_UPLOAD_BYTES:
        seconds = float(
            subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)],
                check=True,
                capture_output=True,
                text=True,
            ).stdout
        )
        # Two passes, so the opening title slide isn't starved while a one-pass
        # rate control settles (that made the first seconds blocky). 96k audio
        # is plenty for narration and leaves more of the budget for the picture.
        audio[audio.index("128k")] = "96k"
        kbps = int(MAX_UPLOAD_BYTES * 8 * 0.95 / seconds / 1000) - 96  # leave room for audio and the container
        video = ["-c:v", "libx264", "-preset", "slow", "-pix_fmt", "yuv420p", "-b:v", f"{kbps}k"]
        with tempfile.TemporaryDirectory() as tmp:
            log = ["-passlogfile", str(Path(tmp) / "x264")]
            run(["ffmpeg", "-y", "-i", str(src), *video, "-pass", "1", *log, "-an", "-f", "mp4", os.devnull])
            run(["ffmpeg", "-y", "-i", str(src), *video, "-pass", "2", *log, *audio,
                 "-movflags", "+faststart", str(dst)])  # fmt: skip


def course_image(landing: dict, dst: Path) -> None:
    """A 750x422 course image with no text (Udemy's image standards forbid text).

    It shows the contribution workflow as a git graph: a main line, a branch
    that curves off for your change, and the merge back.
    """
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="750" height="422" viewBox="0 0 750 422">
    <defs>
      <radialGradient id="bg" cx="78%" cy="18%" r="85%">
        <stop offset="0" stop-color="#1f3b63"/><stop offset="1" stop-color="#0d1b2a"/>
      </radialGradient>
      <filter id="glow"><feGaussianBlur stdDeviation="6" result="b"/>
        <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    </defs>
    <rect width="750" height="422" fill="url(#bg)"/>
    <g opacity="0.08" stroke="#c9d6e8" stroke-width="1">
      <path d="M0 70 H750 M0 140 H750 M0 210 H750 M0 280 H750 M0 350 H750"/>
      <path d="M75 0 V422 M150 0 V422 M225 0 V422 M300 0 V422 M375 0 V422"/>
      <path d="M450 0 V422 M525 0 V422 M600 0 V422 M675 0 V422"/>
    </g>
    <path d="M60 280 H690" stroke="#3776ab" stroke-width="14" stroke-linecap="round"/>
    <path d="M210 280 C 270 280, 270 140, 330 140 H 450 C 510 140, 510 280, 570 280"
          fill="none" stroke="#ffd43b" stroke-width="14" stroke-linecap="round" filter="url(#glow)"/>
    <g fill="#0d1b2a" stroke="#3776ab" stroke-width="10">
      <circle cx="90" cy="280" r="22"/><circle cx="210" cy="280" r="22"/><circle cx="390" cy="280" r="22"/>
      <circle cx="660" cy="280" r="22"/>
    </g>
    <g fill="#0d1b2a" stroke="#ffd43b" stroke-width="10" filter="url(#glow)">
      <circle cx="330" cy="140" r="24"/><circle cx="450" cy="140" r="24"/>
    </g>
    <circle cx="570" cy="280" r="34" fill="#ffd43b" filter="url(#glow)"/>
    <path d="M553 281 l12 12 l23 -25" fill="none" stroke="#0d1b2a" stroke-width="9"
          stroke-linecap="round" stroke-linejoin="round"/>
    </svg>"""
    html = f"<!doctype html><html><body style='margin:0'>{svg}</body></html>"
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "image.html"
        page.write_text(html, encoding="utf-8")
        run(
            [str(CHROME), "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
             f"--user-data-dir={tmp}/profile", "--window-size=750,422", f"--screenshot={dst}", page.as_uri()]
        )  # fmt: skip


def upload_guide(landing: dict, sections: list[Section]) -> str:
    def bullets(items):
        return "\n".join(f"- {item}" for item in items)

    lines = [
        "# Udemy upload guide",
        "",
        "Generated by `tools/udemy_package.py`. Files are next to this guide.",
        "",
        "## 0. Test Video first (recommended)",
        "",
        "Udemy reviews audio quality, and its guidance on text-to-speech narration has changed over time.",
        "Before uploading everything, send `test-video.mp4` to Udemy's free **Test Video** review",
        "(Instructor dashboard → Tools → Test Video) and ask whether the narration meets their standards.",
        "",
        "## 1. Course landing page",
        "",
        f"**Title** ({len(landing['Title'])}/60): {landing['Title']}",
        "",
        f"**Subtitle** ({len(landing['Subtitle'])}/120): {landing['Subtitle']}",
        "",
        "**Description:**",
        "",
        str(landing["Description"]),
        "",
        "**Language:** English · **Level:** Beginner · **Category:** Development",
        "",
        "**Course image:** `course-image.png` (750x422, no text, per Udemy's image standards)",
        "",
        "## 2. Intended learners",
        "",
        "**What you'll learn:**",
        "",
        bullets(landing["What you'll learn"]),
        "",
        "**Requirements:**",
        "",
        bullets(landing["Requirements"]),
        "",
        "**Who this course is for:**",
        "",
        bullets(landing["Who this course is for"]),
        "",
        "## 3. Curriculum",
        "",
        "Create one section per heading below, then one lecture per row. Upload the video, add its",
        "captions (English) and add the written lesson as an external resource link. Put the same",
        'link in the lecture\'s description too: "Written lesson, exercise and quiz: LINK".',
        "",
        "Udemy allows no links on the landing page itself (only in the instructor bio), so the",
        "description names the repository without a link.",
        "",
    ]
    for n, section in enumerate(sections, start=1):
        lines += [f"### Section {n}: {section.title}", "", "| # | Lecture title | Video | Captions | Resource link |"]
        lines += ["|---|---|---|---|---|"]
        for lec in section.lectures:
            lines.append(
                f"| {lec.number} | {lec.title} | `lectures/{lec.stem}.mp4` | `captions/{lec.stem}.vtt` "
                f"| {REPO_URL}/tree/main/lessons/{lec.folder} |"
            )
        lines.append("")
    lines += [
        "## 4. Before you submit",
        "",
        "- [ ] Test Video feedback received and acted on",
        "- [ ] Price set (free courses can have at most 2 hours of video; this one is under 1 hour)",
        "- [ ] Every lecture has its video, captions and resource link",
        "- [ ] Course image and landing page filled in",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    landing = parse_landing(LANDING.read_text(encoding="utf-8"))
    problems = landing_problems(landing)
    sections = parse_sections((ROOT / "CURRICULUM.md").read_text(encoding="utf-8"), ROOT / "lessons")
    for lec in (lec for s in sections for lec in s.lectures):
        if len(lec.title) > LECTURE_TITLE_MAX:
            problems.append(f"lecture title over {LECTURE_TITLE_MAX} characters: {lec.title}")
        if not (ROOT / "build" / lec.folder / f"{lec.folder}.mp4").is_file():
            problems.append(f"missing video: build/{lec.folder}/{lec.folder}.mp4 (run tools/render_video.py)")
    if problems:
        print("Fix these first:\n" + "\n".join(f"- {p}" for p in problems), file=sys.stderr)
        return 1

    (OUT / "lectures").mkdir(parents=True, exist_ok=True)
    (OUT / "captions").mkdir(parents=True, exist_ok=True)
    for lec in (lec for s in sections for lec in s.lectures):
        build = ROOT / "build" / lec.folder
        encode_lecture(build / f"{lec.folder}.mp4", OUT / "lectures" / f"{lec.stem}.mp4")
        srt = (build / f"{lec.folder}.srt").read_text(encoding="utf-8")
        (OUT / "captions" / f"{lec.stem}.vtt").write_text(srt_to_vtt(srt), encoding="utf-8")
        print(f"lecture {lec.stem}")
        if lec.folder == TEST_VIDEO_LESSON:
            run(["ffmpeg", "-y", "-i", str(OUT / "lectures" / f"{lec.stem}.mp4"), "-t", str(TEST_VIDEO_SECONDS),
                 "-c", "copy", str(OUT / "test-video.mp4")])  # fmt: skip
    course_image(landing, OUT / "course-image.png")
    (OUT / "UPLOAD.md").write_text(upload_guide(landing, sections), encoding="utf-8")
    print(f"\nDone: {OUT.relative_to(ROOT)}/ (start with UPLOAD.md)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
