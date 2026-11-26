"""Check a pull request title and description you wrote (Lesson 11).

Write them in a text file: the title on the first line, a blank line, then
the description. Then run, from the course folder::

    python tools/check_pr_description.py pr-description.md

It checks what a reviewer looks for:

1. a title that says what the PR does: specific, imperative, 72 characters or fewer
2. a link to the issue, with a keyword that closes it (``Fixes #1234``)
3. what changed and why, in a few sentences
4. how you tested it
5. no leftover template text, and not longer than the change deserves

Exits 0 when the description is ready, 1 when something needs fixing.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

OK, WARN, FAIL = "✔", "!", "✘"

TITLE_MAX = 72
MIN_WORDS = 15  # what changed and why
LONG_WORDS = 150  # more than this is long for a small change
PAST_TENSE = {"fixed", "added", "changed", "updated", "removed", "made", "fixes", "adds", "changes", "updates"}
VAGUE_WORDS = {
    "a", "an", "the", "my", "some", "this", "it", "fix", "fixed", "fixes", "bug", "bugs", "issue", "issues",
    "update", "updated", "updates", "change", "changes", "changed", "code", "stuff", "things", "pr", "pull",
    "request", "patch", "first", "new", "small", "minor", "improvements", "improvement", "wip",
}  # fmt: skip
PREFIX_RE = re.compile(r"^(?:gh-\d+|[a-z]+(?:\([^)]*\))?!?)\s*:\s*", re.IGNORECASE)  # "gh-123: " or "fix(docs): "
CLOSES_RE = re.compile(r"\b(?:fix(?:e[sd])?|close[sd]?|resolve[sd]?)\s*:?\s+(?:[\w.-]+/[\w.-]+)?#\d+", re.IGNORECASE)
ISSUE_RE = re.compile(r"(?:^|[\s(])(?:[\w.-]+/[\w.-]+)?#\d+\b|\bgh-\d+\b", re.IGNORECASE)
TESTED_RE = re.compile(r"\btest(?:ed|s|ing)?\b|\bpytest\b|\bruff\b|\btox\b|\bnox\b|\bverified\b|\bran\b", re.IGNORECASE)
PLACEHOLDER_RE = re.compile(r"<!--|\bTODO\b|describe your changes", re.IGNORECASE)
HEADING_RE = re.compile(r"^#{1,6}\s+\S", re.MULTILINE)


@dataclass
class Report:
    lines: list[tuple[str, str]] = field(default_factory=list)

    def add(self, mark: str, text: str) -> None:
        self.lines.append((mark, text))

    @property
    def ok(self) -> bool:
        return all(mark != FAIL for mark, _ in self.lines)


def split(text: str) -> tuple[str, str]:
    """The title (first non-empty line) and the description (everything after it)."""
    lines = text.replace("\r\n", "\n").strip().split("\n")
    return lines[0].strip(), "\n".join(lines[1:]).strip()


def check_title(title: str, report: Report) -> None:
    subject = PREFIX_RE.sub("", title)
    words = re.findall(r"[\w'`.-]+", subject)
    specific = [w for w in words if w.lower().strip("`.") not in VAGUE_WORDS]
    first = words[0].lower() if words else ""
    problems = []
    if len(words) < 3 or len(specific) < 2:
        problems.append('say what the PR does, like "Fix slugify for repeated spaces and punctuation"')
    if len(title) > TITLE_MAX:
        problems.append(f"it's {len(title)} characters; keep it to {TITLE_MAX} or fewer")
    if title.endswith("."):
        problems.append("drop the full stop at the end")
    if first in PAST_TENSE:
        problems.append(f'use the imperative mood: "Fix ...", not "{first.capitalize()} ..."')
    if problems:
        report.add(FAIL, f'**Title** "{title}": ' + "; ".join(problems) + ".")
    else:
        report.add(OK, f'**Title** says what the PR does: "{title}"')


def prose(body: str) -> str:
    """The description without the issue link line, so "Fixes #12" alone doesn't count as an explanation."""
    kept = [
        line for line in body.split("\n") if not re.fullmatch(r"\W*" + CLOSES_RE.pattern + r"\W*", line.strip(), re.I)
    ]
    return "\n".join(kept)


def check_body(body: str, report: Report) -> None:
    if CLOSES_RE.search(body):
        report.add(OK, "**Issue** is linked, and will close when the PR is merged.")
    elif ISSUE_RE.search(body):
        report.add(
            WARN,
            "**Issue** is mentioned, but nothing will close it. Write `Fixes #1234` if this PR fixes it "
            "(or keep `Refs #1234` if it's only part of the fix).",
        )
    else:
        report.add(FAIL, "**Issue:** link the issue this PR fixes, like `Fixes #1234`.")

    words = len(re.findall(r"[\w'`-]+", prose(body)))
    if words < MIN_WORDS:
        report.add(FAIL, "**What and why:** say what changed and why, in two or three sentences. The diff shows how.")
    else:
        report.add(OK, "**What and why** are explained.")

    if TESTED_RE.search(body):
        report.add(OK, "**Testing** is described.")
    else:
        report.add(FAIL, "**Testing:** say how you tested it: the tests you added, the commands you ran.")

    if PLACEHOLDER_RE.search(body):
        report.add(FAIL, "**Template text** is still there: fill in or remove the comments and TODOs.")
    if HEADING_RE.search(body) and words <= LONG_WORDS:
        report.add(
            WARN, "**Headings** in a short description read like a template. Plain sentences are easier to review."
        )
    if words > LONG_WORDS:
        report.add(
            WARN, f"**Length:** {words} words is long for a small change. Reviewers read short descriptions first."
        )


def check(text: str) -> Report:
    report = Report()
    if not text.strip():
        report.add(FAIL, "The file is empty. Put the title on the first line, a blank line, then the description.")
        return report
    title, body = split(text)
    check_title(title, report)
    check_body(body, report)
    return report


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("usage: python tools/check_pr_description.py FILE", file=sys.stderr)
        return 2
    path = Path(argv[0])
    if not path.is_file():
        print(f"{path} not found. Write your title and description there first.", file=sys.stderr)
        return 2
    report = check(path.read_text(encoding="utf-8"))
    for mark, text in report.lines:
        print(f"{mark} {text.replace('**', '')}")
    print()
    print("Ready to open. Nice description!" if report.ok else "Fix the ✘ lines, then run this again.")
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # ✔ and ✘ print on Windows too
    sys.exit(main(sys.argv[1:]))
