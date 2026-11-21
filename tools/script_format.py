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

Beats
-----
Blockquote paragraphs separated by a blank line are **beats**. Each beat gets
its own frame, so the picture changes while the narrator talks::

    > Three steps.

    > First, fork.

    > Then, branch.

On a slide, bullets appear one per beat (as many beats as bullets, or one
extra beat first for the title alone). ``focus:`` sets it by hand, one entry
per beat separated by ``|``: line or bullet numbers (``2``, ``1-3``, ``1,4``),
``0`` for nothing yet, or ``all``. In code scenes the focused lines are lit
and the rest dimmed; in terminal scenes later lines stay hidden until their
beat. ``notes:`` takes ``- item`` lines, one per beat (``-`` for none): a
short callout under the code.

Other optional fields: ``layout:`` on slides (``bullets``, ``title``,
``steps``, ``cards``; card bullets are ``Title | detail | tag``) and
``file:`` on code/terminal scenes (the window title). ``lang: text`` on a
code scene turns off Python colours, for prose or a search query.

``{gh|g h}`` in narration shows "gh" in the subtitles and says "g h".
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
LAYOUTS = {"bullets", "title", "steps", "cards"}
LIST_FIELDS = ("bullets", "notes")
SAY_RE = re.compile(r"\{([^{}|]+)\|([^{}|]+)\}")  # {shown|spoken}


def spoken(text: str) -> str:
    """Narration as the voice should say it."""
    return SAY_RE.sub(r"\2", text)


def shown(text: str) -> str:
    """Narration as the subtitles should show it."""
    return SAY_RE.sub(r"\1", text)


def parse_focus(spec: str) -> list[set[int] | None]:
    """``"0 | 1-2 | all"`` becomes ``[set(), {1, 2}, None]`` (None: everything, no emphasis)."""
    out: list[set[int] | None] = []
    for part in spec.split("|"):
        part = part.strip()
        if part in ("all", "-", ""):
            out.append(None)
            continue
        numbers: set[int] = set()
        for piece in part.split(","):
            lo, _, hi = piece.strip().partition("-")
            numbers.update(range(int(lo), int(hi or lo) + 1))
        numbers.discard(0)
        out.append(numbers)
    return out


@dataclass
class Scene:
    number: int
    heading: str
    fields: dict[str, str] = field(default_factory=dict)
    bullets: list[str] = field(default_factory=list)
    code: list[str] = field(default_factory=list)
    narration: str = ""  # every beat, as spoken
    notes: list[str] = field(default_factory=list)
    beats: list[str] = field(default_factory=list)  # narration paragraphs, markup intact

    @property
    def visual(self) -> str:
        return self.fields.get("visual", "")

    @property
    def layout(self) -> str:
        return self.fields.get("layout", "bullets")

    def focus(self) -> list[set[int] | None]:
        """What to emphasise on each beat's frame. Raises ValueError on a bad ``focus:``."""
        count = max(len(self.beats), 1)
        if self.fields.get("focus"):
            return parse_focus(self.fields["focus"])
        if self.visual == "slide" and count > 1:
            n = len(self.bullets)
            if count == n:
                return [{i} for i in range(1, n + 1)]
            if count == n + 1:
                return [set(), *({i} for i in range(1, n + 1))]
        return [None] * count


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
    collecting: str | None = None  # "bullets", "notes", "code" (waiting for fence) or "fence"
    narration: list[list[str]] = []
    new_beat = True

    def finish() -> None:
        if current is not None:
            current.beats = [" ".join(beat).strip() for beat in narration]
            current.narration = " ".join(spoken(beat) for beat in current.beats).strip()
            scenes.append(current)

    for line in text.splitlines():
        if line.startswith("# ") and not title:
            title = line[2:].removeprefix("Video script:").strip()
            continue
        m = SCENE_RE.match(line)
        if m:
            finish()
            current = Scene(int(m.group(1)), m.group(2).strip())
            collecting, narration, new_beat = None, [], True
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
            if new_beat:
                narration.append([])
                new_beat = False
            narration[-1].append(line[1:].strip())
            continue
        if not line.strip():
            collecting, new_beat = None, True
            continue
        if collecting in LIST_FIELDS and line.startswith("-"):
            getattr(current, collecting).append(line[1:].strip() or "-")
            continue
        fm = FIELD_RE.match(line)
        if fm and not narration:
            key, value = fm.group(1), fm.group(2).strip()
            if key in ("bullets", "notes", "code") and not value:
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
        out.extend(f"{where}: {p}" for p in _beat_problems(scene))
    return out


def _beat_problems(scene: Scene) -> list[str]:
    out: list[str] = []
    beats = max(len(scene.beats), 1)
    if scene.visual == "slide" and scene.layout not in LAYOUTS:
        out.append(f"layout must be one of {sorted(LAYOUTS)}, got {scene.layout!r}")
    try:
        focus = scene.focus()
    except ValueError:
        return [*out, f"can't read focus: {scene.fields['focus']!r} (use e.g. '0 | 1-2 | all')"]
    if len(focus) != beats:
        out.append(f"focus: has {len(focus)} entries but the narration has {beats} beats")
    items = len(scene.bullets) if scene.visual == "slide" else len(scene.code)
    if any(max(f, default=0) > items for f in focus if f):
        out.append(f"focus: points past the last of {items} lines/bullets")
    if scene.notes and len(scene.notes) not in (1, beats):
        out.append(f"notes: has {len(scene.notes)} items; use 1 or one per beat ({beats})")
    if scene.notes and scene.visual not in ("code", "terminal"):
        out.append("notes: only works on code and terminal scenes")
    return out


def load(path: Path) -> Script:
    return parse(path.read_text(encoding="utf-8"))
