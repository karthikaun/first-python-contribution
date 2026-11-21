"""Render a lesson's script.md into an MP4 video with subtitles.

Pipeline, per scene:
  1. Build an HTML frame for the scene's visual (slide, code, terminal, browser).
  2. Screenshot it at 1920x1080 with headless Chrome.
  3. Synthesize the narration (macOS ``say`` for now; swap ``synthesize``).
  4. Combine image + audio into a clip with ffmpeg.
Then concatenate the clips and write an .srt subtitle file next to the video.

Usage::

    python tools/render_video.py lessons/00-what-counts [--voice Samantha] [--scenes 1-3]

Output goes to ``build/<lesson>/<lesson>.mp4`` (and ``.srt``).
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import script_format  # noqa: E402
from script_format import Scene  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
WIDTH, HEIGHT = 1920, 1080
PAD_SECONDS = 0.6  # silence after each scene's narration

CSS = """
* { box-sizing: border-box; margin: 0; }
body { width: 1920px; height: 1080px; overflow: hidden; font-family: -apple-system, "Helvetica Neue", sans-serif;
       background: radial-gradient(circle at 80% 10%, #1f3b63 0%, #0d1b2a 55%); color: #f4f1e8; }
.frame { position: absolute; inset: 0; padding: 120px 150px; display: flex; flex-direction: column;
         justify-content: center; }
.kicker { position: absolute; top: 60px; left: 150px; font-size: 28px; letter-spacing: 3px; text-transform: uppercase;
          color: #ffd43b; font-weight: 600; }
.brand { position: absolute; bottom: 55px; right: 150px; font-size: 26px; color: #8aa4c8; }
.brand b { color: #ffd43b; }
h1 { font-size: 84px; line-height: 1.1; font-weight: 750; max-width: 1550px; }
ul { margin-top: 60px; list-style: none; padding: 0; }
li { font-size: 46px; line-height: 1.35; margin: 18px 0; padding-left: 60px; position: relative; color: #dfe7f2; }
li::before { content: ""; position: absolute; left: 0; top: 24px; width: 22px; height: 22px; border-radius: 6px;
             background: #3776ab; box-shadow: 8px 8px 0 #ffd43b; }
pre { font-family: "SF Mono", Menlo, monospace; font-size: 50px; line-height: 1.6; background: #0a1220;
      border: 2px solid #2a4466; border-radius: 24px; padding: 60px 70px; color: #e8eef7; white-space: pre; }
.tok-str { color: #ffd43b; } .tok-op { color: #7fb4ff; } .prompt { color: #5fd38d; }
.browser { border-radius: 22px; overflow: hidden; border: 2px solid #2a4466; background: #f6f8fa; }
.bar { background: #dfe3e8; padding: 22px 28px; display: flex; align-items: center; gap: 14px; }
.dot { width: 22px; height: 22px; border-radius: 50%; }
.url { margin-left: 24px; flex: 1; background: #fff; border-radius: 12px; padding: 14px 24px; font-size: 30px;
       color: #444; }
.page { height: 520px; display: flex; align-items: center; justify-content: center; color: #57606a; font-size: 38px; }
.caption { margin-top: 50px; font-size: 56px; font-weight: 700; color: #ffd43b; }
"""


def _highlight_python(line: str) -> str:
    escaped = html.escape(line)
    escaped = re.sub(r"(&quot;.*?&quot;)", r'<span class="tok-str">\1</span>', escaped)
    return escaped.replace(" = ", ' <span class="tok-op">=</span> ')


PROMPT_RE = re.compile(r"^((?:\(\.venv\) )?\$ )(.*)$")
CODE_WIDTH_PX = 1480  # inside the frame and the <pre> padding
CODE_HEIGHT_PX = 760


def code_font_px(lines: list[str]) -> int:
    """Largest font size (max 50px) that fits every line without wrapping."""
    longest = max((len(line) for line in lines), default=1) or 1
    by_width = CODE_WIDTH_PX / (0.61 * longest)
    by_height = CODE_HEIGHT_PX / (1.6 * max(len(lines), 1))
    return int(max(22, min(50, by_width, by_height)))


def _terminal_line(line: str) -> str:
    m = PROMPT_RE.match(line)
    if m:
        return f'<span class="prompt">{html.escape(m.group(1))}</span>{html.escape(m.group(2))}'
    return html.escape(line)


def _pre(lines: list[str], rendered: list[str]) -> str:
    return f'<pre style="font-size: {code_font_px(lines)}px">' + "\n".join(rendered) + "</pre>"


def scene_html(scene: Scene, lesson_title: str) -> str:
    kicker = html.escape(scene.heading)
    if scene.visual == "slide":
        items = "".join(f"<li>{html.escape(b)}</li>" for b in scene.bullets)
        body = f"<h1>{html.escape(scene.fields['title'])}</h1><ul>{items}</ul>"
    elif scene.visual == "code":
        body = _pre(scene.code, [_highlight_python(line) for line in scene.code])
    elif scene.visual == "terminal":
        body = _pre(scene.code, [_terminal_line(line) for line in scene.code])
    elif scene.visual == "browser":
        # Placeholder frame until real page captures (Playwright) are wired in.
        body = (
            '<div class="browser"><div class="bar">'
            '<span class="dot" style="background:#ff5f57"></span>'
            '<span class="dot" style="background:#febc2e"></span>'
            '<span class="dot" style="background:#28c840"></span>'
            f'<span class="url">{html.escape(scene.fields["url"])}</span></div>'
            '<div class="page">[ screen capture goes here ]</div></div>'
            f'<div class="caption">{html.escape(scene.fields["caption"])}</div>'
        )
    else:
        raise ValueError(f"unknown visual {scene.visual!r}")
    brand = f"<b>First Python Contribution</b> · {html.escape(lesson_title)}"
    return (
        f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>"
        f"<div class='kicker'>{kicker}</div><div class='frame'>{body}</div><div class='brand'>{brand}</div>"
        "</body></html>"
    )


def screenshot(html_path: Path, png_path: Path) -> None:
    subprocess.run(
        [
            str(CHROME),
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            f"--window-size={WIDTH},{HEIGHT}",
            f"--screenshot={png_path}",
            html_path.as_uri(),
        ],
        check=True,
        capture_output=True,
    )


def synthesize(text: str, out: Path, voice: str, rate: int) -> None:
    """Text to speech. macOS ``say`` for the prototype; replace for production voices."""
    subprocess.run(["say", "-v", voice, "-r", str(rate), "-o", str(out), text], check=True)


def duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return float(out.strip())


def make_clip(png: Path, audio: Path, out: Path) -> None:
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-loop", "1", "-framerate", "30", "-i", str(png),
            "-i", str(audio),
            "-af", f"apad=pad_dur={PAD_SECONDS}",
            "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
            "-shortest", str(out),
        ],
        check=True,
    )  # fmt: skip


def concat(clips: list[Path], out: Path) -> None:
    listing = out.with_suffix(".txt")
    listing.write_text("".join(f"file '{c.name}'\n" for c in clips))
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(listing),
            "-c",
            "copy",
            str(out),
        ],
        check=True,
    )


def _srt_time(seconds: float) -> str:
    ms = round(seconds * 1000)
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def subtitles(scenes: list[Scene], durations: list[float]) -> str:
    """One cue per sentence, timed in proportion to its length within the scene."""
    cues, start, n = [], 0.0, 1
    for scene, dur in zip(scenes, durations, strict=True):
        speech = dur - PAD_SECONDS
        sentences = [s for s in re.split(r"(?<=[.!?])\s+", scene.narration) if s]
        total = sum(len(s) for s in sentences) or 1
        t = start
        for sentence in sentences:
            length = speech * len(sentence) / total
            cues.append(f"{n}\n{_srt_time(t)} --> {_srt_time(t + length)}\n{sentence}\n")
            t += length
            n += 1
        start += dur
    return "\n".join(cues)


def parse_range(spec: str | None, count: int) -> list[int]:
    if not spec:
        return list(range(1, count + 1))
    lo, _, hi = spec.partition("-")
    return list(range(int(lo), int(hi or lo) + 1))


def render(lesson: Path, voice: str, rate: int, scene_range: str | None) -> Path:
    for tool in ("ffmpeg", "ffprobe", "say"):
        if not shutil.which(tool):
            sys.exit(f"{tool} not found; install it first (brew install ffmpeg)")
    if not CHROME.exists():
        sys.exit(f"Google Chrome not found at {CHROME}")

    script = script_format.load(lesson / "script.md")
    problems = script_format.problems(script)
    if problems:
        sys.exit("script.md has problems:\n" + "\n".join(f"- {p}" for p in problems))

    wanted = set(parse_range(scene_range, len(script.scenes)))
    scenes = [s for s in script.scenes if s.number in wanted]
    build = ROOT / "build" / lesson.name
    build.mkdir(parents=True, exist_ok=True)

    clips, durations = [], []
    for scene in scenes:
        stem = build / f"scene{scene.number:02}"
        stem.with_suffix(".html").write_text(scene_html(scene, script.title), encoding="utf-8")
        screenshot(stem.with_suffix(".html"), stem.with_suffix(".png"))
        synthesize(scene.narration, stem.with_suffix(".aiff"), voice, rate)
        make_clip(stem.with_suffix(".png"), stem.with_suffix(".aiff"), stem.with_suffix(".mp4"))
        clips.append(stem.with_suffix(".mp4"))
        durations.append(duration(stem.with_suffix(".mp4")))
        print(f"scene {scene.number:2}: {durations[-1]:5.1f}s  {scene.heading}")

    video = build / f"{lesson.name}.mp4"
    concat(clips, video)
    video.with_suffix(".srt").write_text(subtitles(scenes, durations), encoding="utf-8")
    print(f"\n{video.relative_to(ROOT)}  ({sum(durations) / 60:.1f} min)")
    return video


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render a lesson video from its script.md")
    parser.add_argument("lesson", type=Path)
    parser.add_argument("--voice", default="Samantha")
    parser.add_argument("--rate", type=int, default=175, help="words per minute for say")
    parser.add_argument("--scenes", help="e.g. 1-3 to render only some scenes")
    args = parser.parse_args(argv)
    render(args.lesson.resolve(), args.voice, args.rate, args.scenes)
    return 0


if __name__ == "__main__":
    sys.exit(main())
