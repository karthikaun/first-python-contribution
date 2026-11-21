"""Parse lesson video scripts (``lessons/NN-slug/script.md``).

A script is a Markdown file made of scenes::

    ## Scene 3: Star
    visual: browser
    url: https://github.com/...
    caption: Click Star, top right

    > Narration, written as a blockquote.
    > It can span several lines.

Fields before the narration are ``key: value`` lines. ``bullets:`` takes the
``- item`` lines that follow it. ``code:`` takes a fenced block (three
backticks on their own line before and after), so code can contain blank
lines and lines starting with ``>``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

VISUALS = {"slide", "browser", "terminal", "code"}
REQUIRED_FIELDS = {
    "slide": {"title"},
    "browser": {"url", "caption"},
    "terminal": {"code"},
    "code": {"code"},
}
SCENE_RE = re.compile(r"^## Scene (\d+): (.+)$")
FIELD_RE = re.compile(r"^([a-z]+):\s?(.*)$")
WORDS_PER_MINUTE = 150


@dataclass
class Scene:
    number: int
    heading: str
    fields: dict[str, str] = field(default_factory=dict)
    bullets: list[str] = field(default_factory=list)
    code: list[str] = field(default_factory=list)
    narration: str = ""

    @property
    def visual(self) -> str:
        return self.fields.get("visual", "")


@dataclass
class Script:
    title: str
    scenes: list[Scene]

    @property
    def words(self) -> int:
        return sum(len(s.narration.split()) for s in self.scenes)

    @property
    def minutes(self) -> float:
        return self.words / WORDS_PER_MINUTE


def parse(text: str) -> Script:
    title = ""
    scenes: list[Scene] = []
    current: Scene | None = None
    collecting: str | None = None  # "bullets", "code" (waiting for fence) or "fence"
    narration: list[str] = []

    def finish() -> None:
        if current is not None:
            current.narration = " ".join(narration).strip()
            scenes.append(current)

    for line in text.splitlines():
        if line.startswith("# ") and not title:
            title = line[2:].removeprefix("Video script:").strip()
            continue
        m = SCENE_RE.match(line)
        if m:
            finish()
            current = Scene(int(m.group(1)), m.group(2).strip())
            collecting, narration = None, []
            continue
        if current is None:
            continue
        if collecting == "fence":
            if line.strip() == "```":
                collecting = None
            else:
                current.code.append(line)
            continue
        if collecting == "code" and line.strip().startswith("```"):
            collecting = "fence"
            continue
        if line.startswith(">"):
            collecting = None
            narration.append(line[1:].strip())
            continue
        if not line.strip():
            collecting = None
            continue
        if collecting == "bullets" and line.startswith("- "):
            current.bullets.append(line[2:].strip())
            continue
        fm = FIELD_RE.match(line)
        if fm and not narration:
            key, value = fm.group(1), fm.group(2).strip()
            if key in ("bullets", "code") and not value:
                collecting = key
                current.fields[key] = ""
            else:
                current.fields[key] = value
    finish()
    return Script(title, scenes)


def problems(script: Script) -> list[str]:
    """Return a list of human-readable problems with a parsed script."""
    out: list[str] = []
    if not script.title:
        out.append("missing '# Video script: <title>' heading")
    if not script.scenes:
        out.append("no '## Scene N: <name>' sections")
    for i, scene in enumerate(script.scenes, start=1):
        where = f"scene {scene.number} ({scene.heading})"
        if scene.number != i:
            out.append(f"{where}: expected scene number {i}")
        if scene.visual not in VISUALS:
            out.append(f"{where}: visual must be one of {sorted(VISUALS)}, got {scene.visual!r}")
            continue
        for key in REQUIRED_FIELDS[scene.visual]:
            if key == "code" and not scene.code:
                out.append(f"{where}: needs a 'code:' block")
            elif key != "code" and not scene.fields.get(key):
                out.append(f"{where}: needs '{key}:'")
        if not scene.narration:
            out.append(f"{where}: no narration (write it as a '> ' blockquote)")
    return out


def load(path: Path) -> Script:
    return parse(path.read_text(encoding="utf-8"))
