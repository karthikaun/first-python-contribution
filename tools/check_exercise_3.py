"""Check your Exercise 3 fix locally (Lesson 10).

Run it from the course folder, with your venv active::

    python tools/check_exercise_3.py

It checks that:

1. ``slugify`` in practice/textkit.py now behaves as the bug report asks
2. your test in practice/tests/test_textkit.py *fails* on the original buggy
   code (so it really catches the bug) and passes on yours
3. the practice tests still pass
4. you added a news fragment in practice/news/
5. your last commit message is in good shape (if you've committed)

Exercise 3 is local only: don't open a pull request for it.
"""

from __future__ import annotations

import importlib.util
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRACTICE = ROOT / "practice"
TEXTKIT = PRACTICE / "textkit.py"
LEARNER_TEST = PRACTICE / "tests" / "test_textkit.py"
NEWS = PRACTICE / "news"

BUGGY_SOURCE = """
def slugify(title: str) -> str:
    return title.lower().replace(" ", "-")
"""

EXPECTED = {
    "Hello World": "hello-world",
    "Hello  World": "hello-world",
    "  Hello World ": "hello-world",
    "Hello, World!": "hello-world",
    "Python 3.13 is out": "python-3-13-is-out",
    "already-a-slug": "already-a-slug",
    "": "",
    "---": "",
}

PAST_TENSE = {"fixed", "added", "changed", "updated", "removed", "made", "fixes", "adds", "changes", "updates"}

OK, WARN, FAIL = "✔", "!", "✘"


def load_slugify(path: Path):
    spec = importlib.util.spec_from_file_location("learner_textkit", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module.slugify


def check_behaviour(slugify) -> list[str]:
    """Return the cases slugify still gets wrong."""
    wrong = []
    for title, expected in EXPECTED.items():
        try:
            got = slugify(title)
        except Exception as exc:  # noqa: BLE001 - report any crash to the learner
            got = f"raised {type(exc).__name__}"
        if got != expected:
            wrong.append(f"slugify({title!r}) returned {got!r}, expected {expected!r}")
    return wrong


def run_test_against(source: str, test_file: Path) -> int:
    """Run the learner's test file against a given textkit source; return pytest's exit code."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        (tmp_path / "textkit.py").write_text(source, encoding="utf-8")
        shutil.copy(test_file, tmp_path / "test_textkit.py")
        (tmp_path / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "test_textkit.py"],
            cwd=tmp_path,
            capture_output=True,
            text=True,
        )
        return proc.returncode


def check_commit_message(subject: str) -> list[str]:
    tips = []
    if len(subject) > 72:
        tips.append(f"subject is {len(subject)} characters; keep it to 72 or fewer")
    if subject.endswith("."):
        tips.append("drop the full stop at the end of the subject")
    first = subject.split(":")[-1].strip().split(" ")[0].lower() if subject.strip() else ""
    if first in PAST_TENSE:
        tips.append(f'use the imperative mood: "Fix ...", not "{first.capitalize()} ..."')
    if subject and subject[0].islower() and ":" not in subject:
        tips.append("start the subject with a capital letter")
    return tips


def news_fragments(news_dir: Path) -> list[Path]:
    return [p for p in news_dir.glob("*.md") if p.name != "README.md" and p.read_text(encoding="utf-8").strip()]


def main() -> int:
    results: list[tuple[str, str]] = []

    wrong = check_behaviour(load_slugify(TEXTKIT))
    if wrong:
        results.append((FAIL, "slugify still has the bug:\n       " + "\n       ".join(wrong[:4])))
    else:
        results.append((OK, "slugify handles every case in the bug report"))

    if run_test_against(BUGGY_SOURCE, LEARNER_TEST) == 1:
        results.append((OK, "your test fails on the original buggy code, so it catches the bug"))
    else:
        results.append((FAIL, "your test passes on the original buggy code: add a case from the bug report"))
    if run_test_against(TEXTKIT.read_text(encoding="utf-8"), LEARNER_TEST) == 0:
        results.append((OK, "your test passes on your fix"))
    else:
        results.append((FAIL, "your test fails on your fix: run python -m pytest practice/tests/test_textkit.py"))

    proc = subprocess.run([sys.executable, "-m", "pytest", "-q", "practice"], cwd=ROOT, capture_output=True, text=True)
    results.append((OK, "all practice tests pass") if proc.returncode == 0 else (FAIL, "some practice tests fail"))

    fragments = news_fragments(NEWS)
    if any(re.search(r"\.bugfix\.md$", p.name) for p in fragments):
        results.append((OK, f"news fragment: {fragments[0].relative_to(ROOT)}"))
    else:
        results.append((FAIL, "add a news fragment like practice/news/slugify-separators.bugfix.md"))

    log = subprocess.run(["git", "log", "-1", "--format=%s"], cwd=ROOT, capture_output=True, text=True)
    subject = log.stdout.strip()
    branch = subprocess.run(
        ["git", "branch", "--show-current"], cwd=ROOT, capture_output=True, text=True
    ).stdout.strip()
    if branch in ("", "main"):
        results.append((WARN, "you're on main: make a branch for your fix (git switch -c fix-slugify)"))
    elif subject:
        tips = check_commit_message(subject)
        results.append((WARN, "commit message: " + "; ".join(tips)) if tips else (OK, f'commit message: "{subject}"'))

    for status, message in results:
        print(f"{status} {message}")
    failed = sum(status == FAIL for status, _ in results)
    print("\nAll done. Great fix!" if not failed else f"\n{failed} thing(s) to fix.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # ✔ and ✘ print on Windows too
    sys.exit(main())
