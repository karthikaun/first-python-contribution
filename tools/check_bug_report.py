"""Check a learner's bug-hunt issue (Lesson 09).

The issue comes from the **Bug hunt** issue form, so its body has one
``### Heading`` per form field. The checker looks at what a maintainer needs
from a bug report: a specific title, steps someone can run, expected and
actual results, and versions. Then it runs the learner's command against
``bug-hunt/splitbill.py`` and against a correct version of splitbill, to see
whether the steps really show a bug.

Nothing from the issue is ever executed as code or passed to a shell: the
command line is split with :mod:`shlex` and only its arguments are given to
splitbill, which just parses numbers.

Usage (in CI, with the issue in environment variables)::

    TITLE=... BODY=... LOGIN=... python tools/check_bug_report.py

Prints a Markdown comment and exits 0 if the report is ready for a
maintainer, 1 if it needs work. Exits 3, printing nothing, when the issue
isn't a bug-hunt report.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import os
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPLITBILL = ROOT / "bug-hunt" / "splitbill.py"
MARKER = "<!-- bug-hunt-check -->"
NOT_A_BUG_HUNT_ISSUE = 3
CURRENT_VERSION = "1.2.0"
MAX_PEOPLE = 1000
MAX_ARGS = 12
MAX_ARG_LEN = 40
MAX_SHOWN_LINES = 40

OK, WARN, FAIL = "✔", "!", "✘"
NO_RESPONSE = "_No response_"
VAGUE_WORDS = {
    "a", "an", "the", "it", "is", "bug", "bugs", "error", "errors", "issue", "problem", "broken", "wrong",
    "not", "working", "doesn't", "does", "work", "help", "please", "fix", "found", "in", "splitbill", "i",
}  # fmt: skip

FIELDS = {
    "searched": "Did you search first?",
    "what": "What went wrong?",
    "steps": "Steps to reproduce",
    "expected": "What did you expect?",
    "actual": "What happened instead?",
    "version": "splitbill version",
    "python": "Python version",
    "os": "Operating system",
}


def parse_form(body: str) -> dict[str, str]:
    """Split an issue-form body into {field key: text}. Code fences are removed."""
    sections: dict[str, str] = {}
    parts = re.split(r"^### (.+?)\s*$", body.replace("\r\n", "\n"), flags=re.M)
    for heading, text in zip(parts[1::2], parts[2::2], strict=True):
        for key, label in FIELDS.items():
            if heading.strip() == label:
                text = text.strip()
                fenced = re.fullmatch(r"```[\w-]*\n(.*?)\n?```", text, flags=re.S)
                if fenced:
                    text = fenced.group(1).strip()
                sections[key] = "" if text == NO_RESPONSE else text
    return sections


def is_bug_hunt(form: dict[str, str]) -> bool:
    return "steps" in form and "actual" in form


@dataclass
class Report:
    lines: list[tuple[str, str]] = field(default_factory=list)
    run: str = ""

    def add(self, mark: str, text: str) -> None:
        self.lines.append((mark, text))

    @property
    def ok(self) -> bool:
        return all(mark != FAIL for mark, _ in self.lines)


def check_title(title: str, report: Report) -> None:
    rest = re.sub(r"^splitbill\s*:?\s*", "", title.strip(), flags=re.I)
    words = re.findall(r"[\w'%$.-]+", rest)
    specific = [w for w in words if w.lower() not in VAGUE_WORDS]
    if not rest:
        report.add(FAIL, "**Title:** add what goes wrong after `splitbill: `.")
    elif len(words) < 3 or len(specific) < 2:
        report.add(
            FAIL,
            f'**Title:** "{rest}" is too vague. Say what goes wrong and when, like '
            "`splitbill: total is wrong when there are 7 people`.",
        )
    else:
        report.add(OK, "**Title** says what goes wrong.")


def check_text_fields(form: dict[str, str], report: Report) -> None:
    what = form.get("what", "")
    if len(what.split()) < 6:
        report.add(FAIL, "**What went wrong:** one or two full sentences, so a maintainer gets it at a glance.")
    else:
        report.add(OK, "**What went wrong** is explained.")

    expected, actual = form.get("expected", ""), form.get("actual", "")
    if not expected or not actual:
        report.add(FAIL, "**Expected and actual:** fill in both. The difference between them *is* the bug.")
    elif normalise(expected) == normalise(actual):
        report.add(FAIL, "**Expected and actual** say the same thing. What should happen, and what happens instead?")
    else:
        report.add(OK, "**Expected** and **actual** results are both there.")

    if re.search(r"!\[[^\]]*\]\(|<img\b", actual):
        report.add(FAIL, "**Actual output:** paste the text, not a screenshot. Text can be searched and copied.")
    elif "Traceback" in actual and not re.search(r"^\w*(Error|Exception)\b.*$", actual, flags=re.M):
        report.add(FAIL, "**Traceback:** paste all of it. The last line, the error itself, is the most important.")


def check_versions(form: dict[str, str], report: Report) -> None:
    version, python, system = form.get("version", ""), form.get("python", ""), form.get("os", "")
    found = re.search(r"\d+\.\d+\.\d+", version)
    if not found:
        report.add(FAIL, "**splitbill version:** paste the output of `python bug-hunt/splitbill.py --version`.")
    elif found.group(0) != CURRENT_VERSION:
        report.add(
            WARN,
            f"**splitbill version** {found.group(0)} isn't the latest ({CURRENT_VERSION}). "
            "In a real project, check the bug still happens on the latest version first.",
        )
    if not re.search(r"\b3\.\d+", python):
        report.add(FAIL, "**Python version:** paste the output of `python --version`, like `Python 3.13.1`.")
    if not system.strip():
        report.add(FAIL, "**Operating system:** say which one, like `macOS 15.1` or `Windows 11`.")
    if found and re.search(r"\b3\.\d+", python) and system.strip():
        report.add(OK, "**Versions** are there.")


def normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


# --- Running the learner's command ---------------------------------------------------------


def command_args(steps: str) -> list[str] | None:
    """The arguments after ``splitbill.py`` in the first command line of the steps, if any."""
    for line in steps.splitlines():
        line = re.sub(r"^\s*(?:\$|>|%|PS [^>]*>)\s*", "", line.strip().strip("`"))
        if "splitbill" not in line or re.search(r"\bimport\b", line):
            continue
        try:
            tokens = shlex.split(line, comments=True)
        except ValueError:
            return None
        for i, token in enumerate(tokens):
            if token.endswith("splitbill.py") or token == "splitbill":
                return tokens[i + 1 :]
    return None


@dataclass
class Outcome:
    stdout: str
    error: str
    code: int

    def same_as(self, other: Outcome) -> bool:
        return self.stdout == other.stdout and (self.code == 0) == (other.code == 0) and self.error == other.error

    def show(self) -> str:
        text = self.stdout
        if self.code:
            text += self.error + "\n"
        lines = text.rstrip().splitlines()
        if len(lines) > MAX_SHOWN_LINES:  # keep the comment well under GitHub's size limit
            lines = [*lines[:MAX_SHOWN_LINES], f"... ({len(lines) - MAX_SHOWN_LINES} more lines)"]
        return "\n".join(lines) or "(no output)"


def last_line(text: str) -> str:
    lines = [line for line in text.strip().splitlines() if line.strip()]
    return lines[-1] if lines else ""


def run_splitbill(args: list[str]) -> Outcome:
    """Run the real (buggy) splitbill with the learner's arguments: no shell, a timeout."""
    proc = subprocess.run(
        [sys.executable, "-I", str(SPLITBILL), *args],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=SPLITBILL.parent,
        env={"PATH": os.environ.get("PATH", ""), "PYTHONIOENCODING": "utf-8"},
    )
    return Outcome(proc.stdout, last_line(proc.stderr) if proc.returncode else "", proc.returncode)


def money(amount: float) -> str:
    return f"${amount:,.2f}"


def build_parser() -> argparse.ArgumentParser:
    """The same command line as bug-hunt/splitbill.py, abbreviations like --peo included."""
    parser = argparse.ArgumentParser(prog="splitbill", description="Split a restaurant bill between friends.")
    parser.add_argument("bill", type=float, help="the bill before tax and tip, e.g. 120 or 120.50")
    parser.add_argument("--people", type=int, default=1, help="how many people share the bill (default: 1)")
    parser.add_argument("--tip", default="0", help="tip percentage, e.g. 15 or 15%% (default: 0)")
    parser.add_argument("--tax", type=float, default=0.0, help="tax as an amount, e.g. 9.60 (default: 0)")
    parser.add_argument("--version", action="version", version=f"splitbill {CURRENT_VERSION}")
    return parser


def reference(args: list[str]) -> Outcome:
    """What README.md says splitbill should do."""
    parser = build_parser()
    out, err = io.StringIO(), io.StringIO()
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            ns = parser.parse_args(args)
            if ns.people < 1:
                parser.error("--people must be at least 1")
            tip_percent = float(ns.tip.removesuffix("%"))
            tip = ns.bill * tip_percent / 100
            total = ns.bill + ns.tax + tip
            print(f"Bill:  {money(ns.bill)}")
            print(f"Tax:   {money(ns.tax)}")
            print(f"Tip:   {money(tip)} ({tip_percent:g}%)")
            print(f"Total: {money(total)}")
            print()
            base, extra = divmod(round(total * 100), ns.people)
            for number in range(1, ns.people + 1):
                print(f"Person {number}: {money((base + (number <= extra)) / 100)}")
    except SystemExit as exit_:
        code = exit_.code if isinstance(exit_.code, int) else 1
        return Outcome(out.getvalue(), last_line(err.getvalue()) if code else "", code)
    except (ValueError, OverflowError) as exc:
        return Outcome(out.getvalue(), f"{type(exc).__name__}: {exc}", 1)
    return Outcome(out.getvalue(), "", 0)


def too_big(args: list[str]) -> bool:
    """True if running these arguments could print a huge amount.

    The arguments are parsed exactly as splitbill parses them, so every
    spelling of the option counts: ``--people 5000``, ``--people=5000``,
    ``--peo 5000``.
    """
    if len(args) > MAX_ARGS or any(len(a) > MAX_ARG_LEN for a in args):
        return True
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            people = build_parser().parse_args(args).people
    except SystemExit:  # a bad command, --help or --version: splitbill prints a little and stops
        return False
    return people > MAX_PEOPLE


def check_reproduces(form: dict[str, str], report: Report) -> None:
    args = command_args(form.get("steps", ""))
    if args is None:
        report.add(
            FAIL,
            "**Steps:** give the exact command, like `python bug-hunt/splitbill.py 10 --people 3`, "
            "so anyone can paste it and see the bug.",
        )
        return
    command = shlex.join(["python", "bug-hunt/splitbill.py", *args])
    if len(command) > 200:
        command = command[:200] + "..."
    if too_big(args):
        report.add(
            FAIL, f"**Steps:** `{command}` is bigger than it needs to be. Use the smallest numbers that show it."
        )
        return
    try:
        got = run_splitbill(args)
    except subprocess.TimeoutExpired:
        report.add(FAIL, f"**Steps:** `{command}` took too long. Use the smallest numbers that show the bug.")
        return
    want = reference(args)
    if got.same_as(want):
        report.add(
            FAIL,
            f"**Steps:** I ran `{command}` and splitbill did exactly what README.md says. "
            "Check README.md again, or find the command that shows the bug.",
        )
        return
    report.add(OK, f"**Steps reproduce a bug:** I ran `{command}` and it doesn't do what README.md says.")
    report.run = (
        "<details><summary>What I saw when I ran your command</summary>\n\n"
        f"splitbill printed:\n\n```text\n{got.show()}\n```\n\n"
        f"README.md says it should print:\n\n```text\n{want.show()}\n```\n\n</details>"
    )


def check(title: str, body: str) -> Report | None:
    form = parse_form(body)
    if not is_bug_hunt(form):
        return None
    report = Report()
    if "[x]" not in form.get("searched", "").lower():
        report.add(FAIL, "**Search first:** tick the box once you've searched the issues for your bug.")
    check_title(title, report)
    check_text_fields(form, report)
    check_reproduces(form, report)
    check_versions(form, report)
    return report


def comment(report: Report, login: str) -> str:
    who = f"@{login}" if login else "there"
    out = [MARKER, "### 🐞 Bug report check", ""]
    out += [f"{mark} {text}" for mark, text in report.lines]
    if report.run:
        out += ["", report.run]
    out.append("")
    if report.ok:
        out.append(
            f"🎉 Great report, {who}! Someone who has never seen this bug can reproduce it from what you wrote. "
            "**A maintainer will review your report.**\n\nPlease don't open a pull request that fixes it: "
            "the next learner needs the bug. Next up: Lesson 10, making the change."
        )
    else:
        out.append(
            f"Nearly there, {who}. Edit your issue to fix the ✘ items: click **···** at the top right of "
            "your report, then **Edit**. I'll check again when you save."
        )
    return "\n".join(out) + "\n"


def main() -> int:
    title, body, login = os.environ.get("TITLE", ""), os.environ.get("BODY", ""), os.environ.get("LOGIN", "")
    report = check(title, body)
    if report is None:
        return NOT_A_BUG_HUNT_ISSUE
    sys.stdout.write(comment(report, login))
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
