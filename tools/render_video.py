"""Render a lesson's script.md into an MP4 video with subtitles.

Pipeline:
  1. Each scene becomes one HTML frame per narration beat (see
     ``script_format``): bullets appear one at a time, code lines light up.
  2. Screenshot every frame at 1920x1080 with headless Chrome.
  3. Synthesize each beat's narration (macOS ``say`` for now; swap ``synthesize``).
  4. Encode the frames and audio in one ffmpeg pass, each frame held for as
     long as its beat is spoken, and write an .srt subtitle file next to it.

Usage::

    python tools/render_video.py lessons/01-what-counts [--voice Samantha] [--scenes 1-3]

Output goes to ``build/<lesson>/<lesson>.mp4`` (and ``.srt``). Frames are
``sceneNN.png``, or ``sceneNN-K.png`` for beat K of a scene with several.
"""

from __future__ import annotations

import argparse
import fcntl
import html
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import script_format  # noqa: E402
from script_format import Scene  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
WIDTH, HEIGHT = 1920, 1080
PAD_SECONDS = 0.7  # silence after each scene's narration
BEAT_PAD_SECONDS = 0.25  # silence between beats inside a scene

CSS = """
* { box-sizing: border-box; margin: 0; }
body { width: 1920px; height: 1080px; overflow: hidden; font-family: -apple-system, "Helvetica Neue", sans-serif;
       background: radial-gradient(circle at 82% 8%, #1f3b63 0%, #0d1b2a 55%); color: #f4f1e8; }
.frame { position: absolute; inset: 120px 110px 110px; display: flex; flex-direction: column;
         justify-content: center; }
.kicker { position: absolute; top: 54px; left: 110px; font-size: 28px; letter-spacing: 3px; text-transform: uppercase;
          color: #ffd43b; font-weight: 600; }
.kicker .count { color: #8aa4c8; margin-right: 22px; font-variant-numeric: tabular-nums; }
.brand { position: absolute; bottom: 44px; right: 110px; font-size: 26px; color: #8aa4c8; }
.brand b { color: #ffd43b; }
.progress { position: absolute; bottom: 56px; left: 110px; width: 620px; display: flex; gap: 8px; }
.progress i { flex: 1; max-width: 44px; height: 8px; border-radius: 4px; background: #24395a; }
.progress i.done { background: #3776ab; }
.progress i.now { background: #ffd43b; }
h1 { font-size: 78px; line-height: 1.1; font-weight: 750; max-width: 1600px; letter-spacing: -1px; }
code { font-family: "SF Mono", Menlo, monospace; font-size: 0.88em; background: rgba(127, 180, 255, 0.14);
       color: #cfe2ff; padding: 0.08em 0.3em; border-radius: 0.25em; }

/* slide: bullets */
ul { margin-top: 56px; list-style: none; padding: 0; }
li { font-size: 46px; line-height: 1.3; margin: 22px 0; padding-left: 60px; position: relative; color: #f4f1e8; }
li::before { content: ""; position: absolute; left: 0; top: 20px; width: 22px; height: 22px; border-radius: 6px;
             background: #3776ab; box-shadow: 8px 8px 0 #ffd43b; }
li.done { color: #9fb2cc; }
li.todo, .card.todo { visibility: hidden; }

/* slide: title */
.badge { align-self: flex-start; font-size: 30px; font-weight: 700; letter-spacing: 4px; text-transform: uppercase;
         color: #0d1b2a; background: #ffd43b; border-radius: 999px; padding: 10px 30px; margin-bottom: 44px; }
.title h1 { font-size: 104px; max-width: 1500px; }
.title .sub { margin-top: 44px; font-size: 48px; line-height: 1.35; color: #b9c9df; }
.title .sub.todo { visibility: hidden; }

/* slide: steps */
.steps { display: flex; margin-top: 100px; }
.step { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 28px; position: relative; }
.step::before { content: ""; position: absolute; top: 45px; left: -50%; width: 100%; height: 6px;
                background: #24395a; }
.step:first-child::before { display: none; }
.step.done::before, .step.on::before { background: #3776ab; }
.num { width: 96px; height: 96px; border-radius: 50%; z-index: 1; display: flex; align-items: center;
       justify-content: center; font-size: 42px; font-weight: 700; background: #14263d; border: 4px solid #24395a;
       color: #6f87a8; }
.lbl { font-size: 40px; font-weight: 600; text-align: center; padding: 0 10px; color: #5f7696; line-height: 1.2; }
.steps.many .lbl { font-size: 30px; }
.step.done .num { background: #3776ab; border-color: #3776ab; color: #fff; }
.step.done .lbl { color: #b9c9df; }
.step.on .num { background: #ffd43b; border-color: #ffd43b; color: #0d1b2a;
                box-shadow: 0 0 0 12px rgba(255, 212, 59, 0.18); }
.step.on .lbl { color: #fff; }

/* slide: cards */
.cards h1 { font-size: 66px; }
.grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 28px; margin-top: 54px; }
.grid.two { grid-template-columns: repeat(2, 1fr); }
.card { background: rgba(255, 255, 255, 0.05); border: 3px solid #2a4466; border-radius: 22px;
        padding: 30px 36px 32px; display: flex; flex-direction: column; gap: 12px; }
.card.on { border-color: #ffd43b; background: rgba(255, 212, 59, 0.08); }
.ct { font-size: 44px; font-weight: 700; line-height: 1.2; }
.cd { font-size: 34px; line-height: 1.35; color: #b9c9df; }
.tag { align-self: flex-start; margin-top: 8px; font-size: 26px; font-weight: 700; letter-spacing: 1px;
       color: #5fd38d; border: 2px solid #2e6b4a; border-radius: 999px; padding: 4px 18px; }

/* code and terminal */
.win { border-radius: 22px; border: 2px solid #2a4466; background: #0a1220; overflow: hidden;
       box-shadow: 0 30px 80px rgba(0, 0, 0, 0.35); }
.winbar { background: #16233a; padding: 18px 26px; display: flex; align-items: center; gap: 12px; }
.winbar .dot { width: 18px; height: 18px; }
.wintitle { margin-left: 16px; font-family: "SF Mono", Menlo, monospace; font-size: 26px; color: #8aa4c8; }
pre { font-family: "SF Mono", Menlo, monospace; font-size: 50px; line-height: 1.6; padding: 40px 60px 44px 54px;
      color: #f2f5fa; white-space: pre; }
.ln { display: block; min-height: 1.6em; margin: 0 -18px; padding: 0 18px 0 12px; border-left: 6px solid transparent;
      border-radius: 6px; }
.ln.on { background: rgba(255, 212, 59, 0.11); border-left-color: #ffd43b; }
.ln.dim { opacity: 0.5; }
.ln.hide { visibility: hidden; }
.tok-str { color: #ffd43b; } .tok-op { color: #7fb4ff; } .tok-kw { color: #ff9e8a; } .tok-fn { color: #7fb4ff; }
.tok-com { color: #6f87a8; }
.prompt { color: #5fd38d; } .out { color: #a9b8cf; } .out-ok { color: #5fd38d; } .out-err { color: #ff8f8f; }
.out-plus { color: #5fd38d; } .out-hint { color: #ffd43b; }
.note { margin-top: 30px; min-height: 86px; font-size: 38px; line-height: 1.3; padding: 18px 30px;
        border-left: 8px solid #ffd43b; background: rgba(255, 212, 59, 0.08); border-radius: 0 14px 14px 0; }
.note.hide { visibility: hidden; }

/* browser */
.browser { border-radius: 22px; overflow: hidden; border: 2px solid #2a4466; background: #f6f8fa; }
.bar { background: #dfe3e8; padding: 22px 28px; display: flex; align-items: center; gap: 14px; }
.dot { width: 22px; height: 22px; border-radius: 50%; }
.url { margin-left: 24px; flex: 1; background: #fff; border-radius: 12px; padding: 14px 24px; font-size: 30px;
       color: #444; }
.page { height: 520px; display: flex; align-items: center; justify-content: center; color: #57606a; font-size: 38px; }
.caption { margin-top: 50px; font-size: 56px; font-weight: 700; color: #ffd43b; }
.capture { position: relative; overflow: hidden; line-height: 0; }
.capture img { display: block; }
.spot { position: absolute; border: 5px solid #ffd43b; border-radius: 12px;
        box-shadow: 0 0 0 4000px rgba(0, 0, 0, 0.45), 0 0 24px 6px rgba(255, 212, 59, 0.6); }
.shot-caption { margin-top: 20px; font-size: 38px; font-weight: 700; color: #ffd43b; text-align: center; }
.shot { align-self: center; }
.shot .bar { padding: 12px 20px; gap: 10px; }
.shot .dot { width: 16px; height: 16px; }
.shot .url { font-size: 20px; padding: 8px 18px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
"""


def inline(text: str) -> str:
    """Escape text for HTML; `backticks` become <code> and **stars** become <b>."""
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", html.escape(text))
    return re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", out)


PY_TOKEN_RE = re.compile(
    r'(?P<str>[fFrRbB]?(?:"""[^"]*(?:"""|$)|"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'))'
    r"|(?P<com>#.*$)"
    r"|(?P<fn>(?<=\bdef )\w+)"
    r"|(?P<kw>\b(?:from|import|def|return|assert|if|elif|else|for|in|while|class|with|as|not|and|or|try|except"
    r"|raise|pass|None|True|False)\b)"
    r"|(?P<op>->|==|!=|=)"
)


def _highlight_python(line: str) -> str:
    out, pos = [], 0
    for m in PY_TOKEN_RE.finditer(line):
        out.append(html.escape(line[pos : m.start()]))
        out.append(f'<span class="tok-{m.lastgroup}">{html.escape(m.group())}</span>')
        pos = m.end()
    out.append(html.escape(line[pos:]))
    return "".join(out)


def _highlight_python_lines(lines: list[str]) -> list[str]:
    """Highlight a block of Python; the inside of a multi-line docstring is all string."""
    out, in_docstring = [], False
    for line in lines:
        odd = line.count('"""') % 2 == 1
        if in_docstring or (odd and not line.rstrip().endswith('"""')) or (odd and line.strip() == '"""'):
            out.append(f'<span class="tok-str">{html.escape(line)}</span>')
        else:
            out.append(_highlight_python(line))
        in_docstring ^= odd
    return out


PROMPT_RE = re.compile(r"^((?:\(\.venv\) )?\$ )(.*)$")
CODE_WIDTH_PX = 1560  # inside the frame and the <pre> padding
CODE_HEIGHT_PX = 680
NOTE_HEIGHT_PX = 120


def code_font_px(lines: list[str], height: int = CODE_HEIGHT_PX) -> int:
    """Largest font size (max 50px) that fits every line without wrapping."""
    longest = max((len(line) for line in lines), default=1) or 1
    by_width = CODE_WIDTH_PX / (0.61 * longest)
    by_height = height / (1.6 * max(len(lines), 1))
    return int(max(22, min(50, by_width, by_height)))


def _output_class(line: str) -> str:
    """Colour for a line of terminal output."""
    if re.match(r"^E\s+\+ ", line):
        return "out-plus"
    if re.match(r"^E\s+\? ", line):
        return "out-hint"
    if re.match(r"^(E\s|ERROR\b|FAILED\b|CONFLICT\b|error:|fatal:)", line) or re.search(r"\d (failed|errors?)\b", line):
        return "out-err"
    if line.startswith("✓") or "All checks passed" in line or re.search(r"\bpassed in \d", line):
        return "out-ok"
    return "out"


def _terminal_line(line: str) -> str:
    m = PROMPT_RE.match(line)
    if m:
        return f'<span class="prompt">{html.escape(m.group(1))}</span>{html.escape(m.group(2))}'
    return f'<span class="{_output_class(line)}">{html.escape(line)}</span>'


def _line_states(count: int, focus: set[int] | None, reveal_to: int | None) -> list[str]:
    """CSS state per line: "on" (focused), "dim", "hide" (not typed yet) or ""."""
    states = []
    for n in range(1, count + 1):
        if reveal_to is not None and n > reveal_to:
            states.append("hide")
        elif focus is None:
            states.append("")
        else:
            states.append("on" if n in focus else "dim")
    return states


def _window(scene: Scene, focus: set[int] | None, reveal_to: int | None, note: str | None) -> str:
    """A code or terminal window, with focused lines lit and an optional note underneath."""
    terminal = scene.visual == "terminal"
    plain = scene.fields.get("lang") == "text"  # prose or a search query: no Python colours
    render = _terminal_line if terminal else html.escape if plain else _highlight_python
    height = CODE_HEIGHT_PX - (NOTE_HEIGHT_PX if scene.notes else 0)
    states = _line_states(len(scene.code), focus, reveal_to)
    rendered = _highlight_python_lines(scene.code) if render is _highlight_python else map(render, scene.code)
    lines = "".join(f'<span class="ln {state}">{line}</span>' for line, state in zip(rendered, states, strict=True))
    title = scene.fields.get("file") or ("Terminal" if terminal else "Text" if plain else "Python")
    out = (
        '<div class="win"><div class="winbar">'
        '<span class="dot" style="background:#ff5f57"></span>'
        '<span class="dot" style="background:#febc2e"></span>'
        '<span class="dot" style="background:#28c840"></span>'
        f'<span class="wintitle">{html.escape(title)}</span></div>'
        f'<pre style="font-size: {code_font_px(scene.code, height)}px">{lines}</pre></div>'
    )
    if scene.notes:
        hidden = note in (None, "-")
        out += f'<div class="note{" hide" if hidden else ""}">{"&nbsp;" if hidden else inline(note)}</div>'
    return out


def _item_states(count: int, focus: set[int] | None) -> list[str]:
    """CSS state per bullet: "on" (current), "done" (already shown), "todo" (not yet) or ""."""
    if focus is None:
        return [""] * count
    latest = max(focus, default=0)
    return ["on" if n in focus else "done" if n < latest else "todo" for n in range(1, count + 1)]


def _slide(scene: Scene, focus: set[int] | None, lesson_label: str) -> str:
    title = f"<h1>{inline(scene.fields['title'])}</h1>"
    states = _item_states(len(scene.bullets), focus)
    pairs = list(zip(scene.bullets, states, strict=True))
    if scene.layout == "title":
        subs = "".join(f'<div class="sub {s}">{inline(b)}</div>' for b, s in pairs)
        badge = f'<div class="badge">{html.escape(lesson_label)}</div>' if lesson_label else ""
        return f'{badge}<div class="title">{title}{subs}</div>'
    if scene.layout == "steps":
        steps = "".join(
            f'<div class="step {s or "done"}"><span class="num">{n}</span><span class="lbl">{inline(b)}</span></div>'
            for n, (b, s) in enumerate(pairs, start=1)
        )
        many = " many" if len(pairs) > 6 else ""
        return f'{title}<div class="steps{many}">{steps}</div>'
    if scene.layout == "cards":
        cards = ""
        for bullet, state in pairs:
            head, detail, tag = ([part.strip() for part in bullet.split("|")] + ["", ""])[:3]
            cards += (
                f'<div class="card {state}"><div class="ct">{inline(head)}</div>'
                + (f'<div class="cd">{inline(detail)}</div>' if detail else "")
                + (f'<div class="tag">{inline(tag)}</div>' if tag else "")
                + "</div>"
            )
        two = " two" if len(pairs) in (2, 4) else ""
        return f'<div class="cards">{title}<div class="grid{two}">{cards}</div></div>'
    items = "".join(f'<li class="{s}">{inline(b)}</li>' for b, s in pairs)
    return f"{title}<ul>{items}</ul>"


CAPTURE_MAX_W, CAPTURE_MAX_H = 1560, 640


def png_size(path: Path) -> tuple[int, int]:
    """Width and height of a PNG, read from its header."""
    data = path.read_bytes()[16:24]
    return struct.unpack(">II", data)


def capture_layout(size: tuple[int, int], highlight: str | None) -> tuple[float, tuple[int, ...] | None]:
    """Scale a capture to fit the frame, and scale its highlight box with it."""
    w, h = size
    scale = min(CAPTURE_MAX_W / w, CAPTURE_MAX_H / h, 1.4)
    box = tuple(round(int(v) * scale) for v in highlight.split(",")) if highlight else None
    return scale, box


def _browser_bar(url: str) -> str:
    return (
        '<div class="bar">'
        '<span class="dot" style="background:#ff5f57"></span>'
        '<span class="dot" style="background:#febc2e"></span>'
        '<span class="dot" style="background:#28c840"></span>'
        f'<span class="url">{html.escape(url)}</span></div>'
    )


def _browser_capture(scene: Scene, lesson_dir: Path) -> str:
    image = lesson_dir / scene.fields["image"]
    size = png_size(image)
    scale, box = capture_layout(size, scene.fields.get("highlight"))
    w, h = round(size[0] * scale), round(size[1] * scale)
    spot = (
        f'<div class="spot" style="left:{box[0]}px;top:{box[1]}px;width:{box[2]}px;height:{box[3]}px"></div>'
        if box
        else ""
    )
    return (
        f'<div class="shot"><div class="browser" style="width:{w + 4}px">{_browser_bar(scene.fields["url"])}'
        f'<div class="capture"><img src="{image.as_uri()}" width="{w}" height="{h}">{spot}</div></div>'
        f'<div class="shot-caption">{html.escape(scene.fields["caption"])}</div></div>'
    )


def lesson_label(lesson_dir: Path | None) -> str:
    """``lessons/05-second-pr`` gives "Lesson 05"; an appendix like ``A-...`` gives "Appendix A"."""
    prefix = lesson_dir.name.split("-")[0] if lesson_dir else ""
    if prefix.isdigit():
        return f"Lesson {prefix}"
    return f"Appendix {prefix}" if len(prefix) == 1 and prefix.isalpha() else ""


def _body(scene: Scene, beat: int, lesson_dir: Path | None) -> str:
    focus_by_beat = scene.focus()
    focus = focus_by_beat[min(beat, len(focus_by_beat) - 1)]
    if scene.visual == "slide":
        return _slide(scene, focus, lesson_label(lesson_dir))
    if scene.visual in ("code", "terminal"):
        reveal_to = None
        if scene.visual == "terminal" and focus is not None:
            # Lines appear as they are talked about, and stay once shown.
            # An earlier "all" beat showed everything, so nothing hides again.
            seen = focus_by_beat[: beat + 1]
            reveal_to = None if None in seen else max((n for f in seen for n in f), default=0)
        note = None
        if scene.notes:
            note = scene.notes[0] if len(scene.notes) == 1 else scene.notes[min(beat, len(scene.notes) - 1)]
        return _window(scene, focus, reveal_to, note)
    if scene.visual == "browser" and scene.fields.get("image") and lesson_dir is not None:
        return _browser_capture(scene, lesson_dir)
    if scene.visual == "browser":
        # No capture yet: a placeholder frame. Add image: and run tools/capture_pages.py.
        return (
            f'<div class="browser">{_browser_bar(scene.fields["url"])}'
            '<div class="page">[ screen capture goes here ]</div></div>'
            f'<div class="caption">{html.escape(scene.fields["caption"])}</div>'
        )
    raise ValueError(f"unknown visual {scene.visual!r}")


def scene_frames(scene: Scene, lesson_title: str, lesson_dir: Path | None = None, total: int = 0) -> list[str]:
    """One HTML page per narration beat. ``total`` (scenes in the lesson) adds the progress bar."""
    kicker = html.escape(scene.heading)
    progress = ""
    if total:
        kicker = f'<span class="count">{scene.number:02} / {total:02}</span>{kicker}'
        marks = ("done" if n < scene.number else "now" if n == scene.number else "" for n in range(1, total + 1))
        progress = '<div class="progress">' + "".join(f'<i class="{m}"></i>' for m in marks) + "</div>"
    brand = f"<b>First Python Contribution</b> · {html.escape(lesson_title)}"
    return [
        f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>"
        f"<div class='kicker'>{kicker}</div><div class='frame'>{_body(scene, beat, lesson_dir)}</div>"
        f"{progress}<div class='brand'>{brand}</div></body></html>"
        for beat in range(max(len(scene.beats), 1))
    ]


def scene_html(scene: Scene, lesson_title: str, lesson_dir: Path | None = None, total: int = 0) -> str:
    """The scene's final frame: everything revealed."""
    return scene_frames(scene, lesson_title, lesson_dir, total)[-1]


def screenshot(html_path: Path, png_path: Path) -> None:
    with tempfile.TemporaryDirectory() as profile:  # never touch the user's Chrome profile
        subprocess.run(
            [
                str(CHROME),
                "--headless=new",
                "--disable-gpu",
                "--hide-scrollbars",
                "--force-device-scale-factor=1",
                "--allow-file-access-from-files",
                f"--user-data-dir={profile}",
                f"--window-size={WIDTH},{HEIGHT}",
                f"--screenshot={png_path}",
                html_path.as_uri(),
            ],
            check=True,
            capture_output=True,
        )


SAY_LOCK = Path(tempfile.gettempdir()) / "first-python-contribution-say.lock"
SAY_ATTEMPTS = 12


def synthesize(text: str, out: Path, voice: str, rate: int) -> None:
    """Text to speech. macOS ``say`` for the prototype; replace for production voices.

    ``say`` sometimes garbles a clip when other ``say`` processes or heavy work
    run at the same time, and it doesn't report it. Serial runs are
    byte-identical, so only one runs at a time (across processes), and a clip
    is kept only when two runs in a row agree.
    """
    check = out.with_name(out.stem + ".check" + out.suffix)
    cmd = ["say", "-v", voice, "-r", str(rate), "-o"]
    with SAY_LOCK.open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        subprocess.run([*cmd, str(out), text], check=True)
        for attempt in range(SAY_ATTEMPTS):
            subprocess.run([*cmd, str(check), text], check=True)
            if check.read_bytes() == out.read_bytes():
                check.unlink()
                return
            check.replace(out)
            time.sleep(min(attempt + 1, 5))  # give a busy machine a moment
    raise RuntimeError(f"say gave a different clip on every run: {text[:60]!r}")


def duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return float(out.strip())


def pad_audio(speech: Path, out: Path, pad: float) -> None:
    """Convert narration to 48 kHz WAV with ``pad`` seconds of silence after it."""
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(speech), "-af", f"apad=pad_dur={pad}",
         "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(out)],
        check=True,
    )  # fmt: skip


@dataclass
class Segment:
    """One beat: a still frame held while its narration plays."""

    scene: Scene
    text: str  # as the subtitles show it
    png: Path
    wav: Path
    pad: float
    seconds: float = 0.0


def plan_segments(scenes: list[Scene], build: Path) -> list[Segment]:
    """Name the frame and audio file for every beat of every scene."""
    out = []
    for scene in scenes:
        beats = scene.beats or [scene.narration]
        for k, beat in enumerate(beats, start=1):
            stem = build / (f"scene{scene.number:02}" + (f"-{k}" if len(beats) > 1 else ""))
            pad = PAD_SECONDS if k == len(beats) else BEAT_PAD_SECONDS
            out.append(Segment(scene, beat, stem.with_suffix(".png"), stem.with_suffix(".wav"), pad))
    return out


def encode(segments: list[Segment], out: Path) -> None:
    """One pass: every frame held for its beat's length, over the joined narration."""
    frames = out.with_name("frames.txt")
    audio = out.with_name("audio.txt")
    listing = "".join(f"file '{s.png.name}'\nduration {s.seconds:.6f}\n" for s in segments)
    frames.write_text(listing + f"file '{segments[-1].png.name}'\n")  # the concat demuxer needs the last one twice
    audio.write_text("".join(f"file '{s.wav.name}'\n" for s in segments))
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error",
         "-f", "concat", "-safe", "0", "-i", str(frames),
         "-f", "concat", "-safe", "0", "-i", str(audio),
         "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-tune", "stillimage",
         "-c:a", "aac", "-b:a", "160k", "-t", f"{sum(s.seconds for s in segments):.3f}",
         "-movflags", "+faststart", str(out)],
        check=True,
    )  # fmt: skip


def _srt_time(seconds: float) -> str:
    ms = round(seconds * 1000)
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def subtitles(parts: list[tuple[str, float, float]]) -> str:
    """One cue per sentence. ``parts`` is (text, seconds, trailing silence) for each beat, in order;
    a sentence's share of its beat is in proportion to its length."""
    cues, start, n = [], 0.0, 1
    for text, seconds, pad in parts:
        speech = seconds - pad
        sentences = [s for s in re.split(r"(?<=[.!?])\s+", script_format.shown(text)) if s]
        total = sum(len(s) for s in sentences) or 1
        t = start
        for sentence in sentences:
            length = speech * len(sentence) / total
            cues.append(f"{n}\n{_srt_time(t)} --> {_srt_time(t + length)}\n{sentence}\n")
            t += length
            n += 1
        start += seconds
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
    for stale in build.glob("scene*"):
        stale.unlink()

    segments = plan_segments(scenes, build)
    pages = [page for s in scenes for page in scene_frames(s, script.title, lesson, len(script.scenes))]
    for segment, page in zip(segments, pages, strict=True):
        segment.png.with_suffix(".html").write_text(page, encoding="utf-8")

    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(lambda s: screenshot(s.png.with_suffix(".html"), s.png), segments))
    # Narration last and one clip at a time: say garbles clips on a busy machine.
    for segment in segments:
        speech = segment.wav.with_suffix(".aiff")
        synthesize(script_format.spoken(segment.text), speech, voice, rate)
        pad_audio(speech, segment.wav, segment.pad)
        segment.seconds = duration(segment.wav)

    for scene in scenes:
        mine = [s for s in segments if s.scene is scene]
        print(f"scene {scene.number:2}: {sum(s.seconds for s in mine):5.1f}s  {len(mine)} frames  {scene.heading}")

    video = build / f"{lesson.name}.mp4"
    encode(segments, video)
    srt = subtitles([(s.text, s.seconds, s.pad) for s in segments])
    video.with_suffix(".srt").write_text(srt, encoding="utf-8")
    print(f"\n{video.relative_to(ROOT)}  ({sum(s.seconds for s in segments) / 60:.1f} min)")
    return video


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render a lesson video from its script.md")
    parser.add_argument("lesson", type=Path)
    parser.add_argument("--voice", default="Aman", help="macOS voice (Aman: Indian English, male)")
    parser.add_argument("--rate", type=int, default=170, help="words per minute for say")
    parser.add_argument("--scenes", help="e.g. 1-3 to render only some scenes")
    args = parser.parse_args(argv)
    render(args.lesson.resolve(), args.voice, args.rate, args.scenes)
    return 0


if __name__ == "__main__":
    sys.exit(main())
