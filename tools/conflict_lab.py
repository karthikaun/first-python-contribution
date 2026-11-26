"""Create a safe practice world for Lesson 12: rebasing, conflicts, review, squashing.

Usage (from the course folder)::

    python3 tools/conflict_lab.py ../conflict-lab

It creates, entirely on your computer:

    ../conflict-lab/upstream.git   the "project" (a bare repository)
    ../conflict-lab/fork.git       "your fork" (a bare repository)
    ../conflict-lab/work           your clone: origin = fork, upstream = project

In ``work`` you're on branch ``fix-greeting`` with one commit that you've
already pushed to your fork (as if your PR were open). Meanwhile a maintainer
has changed the same line on upstream's ``main``. Nothing touches GitHub.
"""

from __future__ import annotations

import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

MAINTAINER = ["-c", "user.name=Project Maintainer", "-c", "user.email=maintainer@example.com"]
YOU = ["-c", "user.name=You (lab)", "-c", "user.email=you@example.com"]

BASE = """def greeting(name):
    return "Hello " + name
"""
YOURS = """def greeting(name):
    return "Hello " + name + "!"
"""
THEIRS = """def greeting(name):
    return f"Hello, {name}"
"""


def git(cwd: Path, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed:\n{proc.stderr}")
    return proc.stdout.strip()


def commit(repo: Path, who: list[str], message: str, files: dict[str, str]) -> None:
    for name, text in files.items():
        (repo / name).write_text(text, encoding="utf-8")
    git(repo, "add", *files)
    git(repo, *who, "commit", "-q", "-m", message)


def create(lab: Path) -> Path:
    if lab.exists():
        raise SystemExit(f"{lab} already exists. Delete it first (rm -rf {lab}) to start over.")
    lab.mkdir(parents=True)
    upstream, fork, work, seed = lab / "upstream.git", lab / "fork.git", lab / "work", lab / "seed"

    # The project starts with one commit.
    git(lab, "init", "-q", "--bare", "--initial-branch=main", str(upstream))
    git(lab, "init", "-q", "--initial-branch=main", str(seed))
    commit(seed, MAINTAINER, "Add greeting", {"app.py": BASE})
    git(seed, "push", "-q", str(upstream), "main")

    # You fork it and clone your fork.
    git(lab, "clone", "-q", "--bare", str(upstream), str(fork))
    git(lab, "clone", "-q", str(fork), str(work))
    git(work, "remote", "add", "upstream", str(upstream))

    # You make your change on a branch and push it: your PR is open.
    git(work, "switch", "-q", "-c", "fix-greeting")
    commit(work, YOU, "Add an exclamation mark to the greeting", {"app.py": YOURS})
    git(work, "push", "-q", "-u", "origin", "fix-greeting")

    # Meanwhile, a maintainer changes the same line on upstream main.
    git(seed, "pull", "-q", str(upstream), "main")
    commit(seed, MAINTAINER, "Use an f-string and a comma in the greeting", {"app.py": THEIRS})
    git(seed, "push", "-q", str(upstream), "main")
    remove_tree(seed)

    (lab / "REVIEW.md").write_text(
        "# Review comments on your pull request\n\n"
        "1. **CI:** This branch has conflicts that must be resolved.\n"
        "2. **Reviewer:** Could you add a docstring to `greeting()`?\n"
        "3. **Reviewer (later):** Looks good! Please squash into one commit before we merge.\n",
        encoding="utf-8",
    )
    return work


def remove_tree(path: Path) -> None:
    """shutil.rmtree, but also on Windows, where git's read-only object files can't be deleted as they are."""
    for p in path.rglob("*"):
        if p.is_file():
            os.chmod(p, stat.S_IWRITE | stat.S_IREAD)
    shutil.rmtree(path)


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("usage: python3 tools/conflict_lab.py PATH  (for example ../conflict-lab)", file=sys.stderr)
        return 2
    work = create(Path(argv[0]).resolve())
    print(f"Lab ready. Your clone is {work}")
    print("Read REVIEW.md in the lab folder, then follow Lesson 12.")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # ✔ and ✘ print on Windows too
    sys.exit(main(sys.argv[1:]))
