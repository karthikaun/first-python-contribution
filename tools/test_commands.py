"""Run the shell commands shown in lessons, so lessons can't silently go stale.

Every fenced ```bash block in a lesson's README.md and exercise.md is run, in
lesson order, inside a throwaway HOME and working directory. Mark a block
```bash norun when it can't run in CI (installers, logins, your own fork) and
say why in the text around it. Mark a block ```bash expect-fail when its last
command is *supposed* to fail (like a rebase that stops on a conflict): the
run fails if that block succeeds.

Usage::

    python tools/test_commands.py [lesson-folder ...]
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LESSONS = ROOT / "lessons"
FENCE_RE = re.compile(r"^([ \t]*)```bash(?P<info>[^\n]*)\n(?P<body>.*?)^\1```", re.MULTILINE | re.DOTALL)
FILES = ("README.md", "exercise.md")


def blocks(text: str) -> list[str]:
    """Return the runnable bash blocks in a Markdown document."""
    out = []
    for m in FENCE_RE.finditer(text):
        info = m.group("info").split()
        if "norun" in info:
            continue
        indent = len(m.group(1))
        body = "\n".join(line[indent:] for line in m.group("body").splitlines())
        if "expect-fail" in info:
            body = f'if {{\n{body}\n}}; then echo "this block was expected to fail" >&2; exit 1; fi'
        out.append(body)
    return out


def lesson_script(folder: Path) -> str:
    parts = []
    for name in FILES:
        path = folder / name
        if path.is_file():
            parts.extend(blocks(path.read_text(encoding="utf-8")))
    return "\n".join(parts)


def run_lesson(folder: Path, home: Path) -> bool:
    script = lesson_script(folder)
    if not script.strip():
        print(f"skip {folder.name} (no runnable commands)")
        return True
    work = home / "work" / folder.name
    work.mkdir(parents=True)
    (work / "tools").symlink_to(ROOT / "tools")  # lessons run course tools as tools/...
    (work / "bug-hunt").symlink_to(ROOT / "bug-hunt")  # and the bug hunt (Lesson 09)
    env = {
        "HOME": str(home),
        "PATH": os.environ["PATH"],
        "GIT_CONFIG_NOSYSTEM": "1",
        "LANG": "C.UTF-8",
        "TERM": "dumb",
        "GIT_EDITOR": "true",  # accept default messages where a learner would save and close the editor
    }
    print(f"run  {folder.name}")
    proc = subprocess.run(
        ["bash", "-euxo", "pipefail", "-c", script], cwd=work, env=env, capture_output=True, text=True, timeout=300
    )
    if proc.returncode != 0:
        print(proc.stdout)
        print(proc.stderr)
        print(f"FAIL {folder.name} (exit {proc.returncode})")
        return False
    return True


def main(argv: list[str]) -> int:
    folders = [Path(a).resolve() for a in argv] or sorted(
        p for p in LESSONS.iterdir() if p.is_dir() and not p.name.startswith("_")
    )
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        if not any(f.name.startswith("03-") for f in folders):
            # Lesson 03 normally sets the identity; stand in for it when it isn't run.
            (home / ".gitconfig").write_text("[user]\n\tname = Course CI\n\temail = ci@example.com\n")
        ok = all([run_lesson(folder, home) for folder in folders])
    return 0 if ok else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # ✔ and ✘ print on Windows too
    sys.exit(main(sys.argv[1:]))
