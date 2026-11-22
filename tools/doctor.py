"""Check that your machine is ready to contribute (Lesson 03).

Run it from your clone of the course repo::

    python3 tools/doctor.py        (macOS / Linux)
    py tools/doctor.py             (Windows)

Every line should be a green check. Each red cross says how to fix it.
Uses only the standard library and runs on old Pythons on purpose, so it can
tell you when your Python is too old.
"""

from __future__ import annotations

import importlib.util
import re
import shutil
import subprocess
import sys

COURSE_REPO = "thejesh23/first-python-contribution"
MIN_PYTHON = (3, 10)
MIN_GIT = (2, 28)

OK, WARN, FAIL = "ok", "warn", "fail"


def run(cmd: list[str]) -> tuple[int, str] | None:
    """Run a command; return (exit code, output), or None if it isn't installed."""
    if shutil.which(cmd[0]) is None:
        return None
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def parse_version(text: str) -> tuple[int, ...]:
    m = re.search(r"(\d+)\.(\d+)(?:\.(\d+))?", text)
    return tuple(int(g) for g in m.groups() if g is not None) if m else ()


def check_python(version: tuple[int, ...] = tuple(sys.version_info[:3])) -> tuple[str, str]:
    shown = ".".join(map(str, version))
    if version[:2] >= MIN_PYTHON:
        return OK, f"Python {shown}"
    return FAIL, f"Python {shown} is too old. Install the latest Python from https://www.python.org/downloads/"


def check_venv() -> tuple[str, str]:
    if importlib.util.find_spec("venv") and importlib.util.find_spec("ensurepip"):
        return OK, "venv module available"
    return FAIL, "venv isn't available. On Debian/Ubuntu: sudo apt install python3-venv"


def check_git(runner=run) -> tuple[str, str]:
    res = runner(["git", "--version"])
    if res is None:
        return FAIL, "git isn't installed. See Lesson 03, step 1."
    version = parse_version(res[1])
    if version[:2] < MIN_GIT:
        return FAIL, f"git {'.'.join(map(str, version))} is too old; install git 2.28 or newer."
    return OK, f"git {'.'.join(map(str, version))}"


def check_git_name(runner=run) -> tuple[str, str]:
    res = runner(["git", "config", "--global", "user.name"])
    if res and res[0] == 0 and res[1]:
        return OK, f"git user.name is {res[1]!r}"
    return FAIL, 'git doesn\'t know your name. Run: git config --global user.name "Your Name"'


def check_git_email(runner=run) -> tuple[str, str]:
    res = runner(["git", "config", "--global", "user.email"])
    if not (res and res[0] == 0 and res[1]):
        return FAIL, "git doesn't know your email. See Lesson 03, step 3 (use your GitHub noreply address)."
    email = res[1]
    if email.endswith("@users.noreply.github.com"):
        return OK, f"git user.email is your private noreply address ({email})"
    return WARN, (
        f"git user.email is {email}. Every commit you push makes it public. "
        "Consider your GitHub noreply address instead (Lesson 03, step 3)."
    )


def check_gh(runner=run) -> tuple[str, str]:
    res = runner(["gh", "--version"])
    if res is None:
        return FAIL, "GitHub CLI (gh) isn't installed. See Lesson 03, step 1."
    return OK, f"gh {'.'.join(map(str, parse_version(res[1])))}"


def check_gh_auth(runner=run) -> tuple[str, str]:
    res = runner(["gh", "auth", "status"])
    if res is None:
        return FAIL, "gh isn't installed, so it can't be logged in."
    if res[0] == 0:
        m = re.search(r"account (\S+)", res[1])
        return OK, f"gh is logged in{' as ' + m.group(1) if m else ''}"
    return FAIL, "gh isn't logged in. Run: gh auth login"


def check_upstream(runner=run) -> tuple[str, str] | None:
    """Only relevant inside a clone of the course repo."""
    origin = runner(["git", "remote", "get-url", "origin"])
    if not origin or origin[0] != 0 or "first-python-contribution" not in origin[1]:
        return None
    if COURSE_REPO in origin[1]:
        return (
            WARN,
            "You cloned the course repo itself, not your fork. Lesson 05 needs your fork: see Lesson 03, step 5.",
        )
    upstream = runner(["git", "remote", "get-url", "upstream"])
    if upstream and upstream[0] == 0 and COURSE_REPO in upstream[1]:
        return OK, "origin is your fork, upstream is the course repo"
    return FAIL, f"No 'upstream' remote. Run: git remote add upstream https://github.com/{COURSE_REPO}.git"


def symbols() -> dict[str, str]:
    fancy = {OK: "✔", WARN: "!", FAIL: "✘"}
    try:
        "".join(fancy.values()).encode(sys.stdout.encoding or "ascii")
    except (UnicodeEncodeError, LookupError):
        fancy = {OK: "[ok]", WARN: "[!!]", FAIL: "[xx]"}
    if sys.stdout.isatty():
        colors = {OK: "\033[32m", WARN: "\033[33m", FAIL: "\033[31m"}
        return {k: f"{colors[k]}{v}\033[0m" for k, v in fancy.items()}
    return fancy


def main() -> int:
    checks = [
        check_python(),
        check_venv(),
        check_git(),
        check_git_name(),
        check_git_email(),
        check_gh(),
        check_gh_auth(),
    ]
    upstream = check_upstream()
    if upstream:
        checks.append(upstream)
    sym = symbols()
    for status, message in checks:
        print(f"{sym[status]} {message}")
    failures = sum(status == FAIL for status, _ in checks)
    print()
    if failures:
        print(f"{failures} thing(s) to fix. Fix the first one, then run this again.")
        return 1
    print("All set. You're ready for Lesson 04.")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # ✔ and ✘ print on Windows too
    sys.exit(main())
