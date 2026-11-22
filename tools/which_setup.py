"""Work out how to set up and test a Python project you just cloned (Lesson 07).

Usage::

    python3 tools/which_setup.py PATH-TO-PROJECT

It looks for the files that reveal a project's tools (uv.lock, poetry.lock,
tox.ini, noxfile.py, .pre-commit-config.yaml, a Makefile, docs config...) and
prints the commands each one implies. It only reads files.

The project's own CONTRIBUTING file always wins: if it says something
different, do what it says.
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Windows learners use Git Bash (Lesson 03): `py` instead of `python3`, and the venv keeps its scripts in Scripts/.
if os.name == "nt":
    VENV_COMMANDS = ("py -m venv .venv", "source .venv/Scripts/activate")
else:
    VENV_COMMANDS = ("python3 -m venv .venv", "source .venv/bin/activate")

CONTRIBUTING_NAMES = ("CONTRIBUTING.md", "CONTRIBUTING.rst", "CONTRIBUTING.txt", "CONTRIBUTING")
CONTRIBUTING_DIRS = ("", ".github", "docs", "doc")
INTERESTING_MAKE_TARGETS = ("help", "install", "dev", "setup", "test", "tests", "lint", "check", "docs", "format")


@dataclass
class Finding:
    tool: str
    evidence: str
    commands: list[str] = field(default_factory=list)
    note: str = ""


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def find_contributing(root: Path) -> Path | None:
    for folder in CONTRIBUTING_DIRS:
        for name in CONTRIBUTING_NAMES:
            candidate = root / folder / name
            if candidate.is_file():
                return candidate
    return None


def _toml_section_keys(text: str, section: str) -> list[str]:
    """Keys in a TOML table like [project.optional-dependencies], without a TOML parser."""
    m = re.search(rf"^\[{re.escape(section)}\]\s*$(.*?)(?=^\[|\Z)", text, re.MULTILINE | re.DOTALL)
    if not m:
        return []
    return re.findall(r"^\s*([A-Za-z0-9_.-]+)\s*=", m.group(1), re.MULTILINE)


def make_targets(makefile: str) -> list[str]:
    targets = re.findall(r"^([A-Za-z][A-Za-z0-9_.-]*)\s*:(?!=)", makefile, re.MULTILINE)
    return [t for t in INTERESTING_MAKE_TARGETS if t in targets]


def detect(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    pyproject = _read(root / "pyproject.toml")

    # Environment managers: usually only one of these applies.
    if (root / "uv.lock").is_file():
        findings.append(Finding("uv", "uv.lock", ["uv sync", "uv run pytest"]))
    if (root / "poetry.lock").is_file() or "[tool.poetry" in pyproject:
        findings.append(
            Finding(
                "Poetry",
                "poetry.lock or [tool.poetry]",
                ["poetry install", "poetry run pytest"],
                "Install Poetry first: pipx install poetry",
            )
        )
    if (root / "pdm.lock").is_file() or "[tool.pdm" in pyproject:
        findings.append(Finding("PDM", "pdm.lock or [tool.pdm]", ["pdm install", "pdm run pytest"]))
    if "[tool.hatch.envs" in pyproject or (root / "hatch.toml").is_file():
        findings.append(
            Finding(
                "Hatch",
                "[tool.hatch.envs] or hatch.toml",
                ["hatch env show", "hatch test"],
                "Install Hatch first: pipx install hatch",
            )
        )

    # Test runners that create their own environments.
    if (root / "tox.ini").is_file() or (root / "tox.toml").is_file() or "[tool.tox" in pyproject:
        findings.append(
            Finding(
                "tox",
                "tox.ini, tox.toml or [tool.tox]",
                ["tox list", "tox run -e <env from the list>"],
                "Install tox first: pipx install tox",
            )
        )
    if (root / "noxfile.py").is_file():
        findings.append(
            Finding(
                "nox",
                "noxfile.py",
                ["nox --list", "nox -s <session from the list>"],
                "Install nox first: pipx install nox",
            )
        )

    if (root / ".pre-commit-config.yaml").is_file():
        findings.append(
            Finding(
                "pre-commit",
                ".pre-commit-config.yaml",
                ["pre-commit install", "pre-commit run --all-files"],
                "Runs the project's linters and formatters on every commit.",
            )
        )

    makefile = _read(root / "Makefile")
    if makefile:
        targets = make_targets(makefile)
        if targets:
            findings.append(
                Finding(
                    "Make",
                    "Makefile",
                    [f"make {t}" for t in targets],
                    "Read the Makefile to see what each target runs.",
                )
            )

    # Plain pip, when nothing above manages the environment.
    managed = {"uv", "Poetry", "PDM", "Hatch"}
    if not any(f.tool in managed for f in findings):
        commands = list(VENV_COMMANDS)
        groups = _toml_section_keys(pyproject, "dependency-groups")
        extras = _toml_section_keys(pyproject, "project.optional-dependencies")
        reqs = sorted(p.name for p in root.glob("requirements*.txt")) + sorted(
            f"requirements/{p.name}" for p in (root / "requirements").glob("*.txt")
        )
        dev_like = ("dev", "test", "tests", "testing")
        if any(g in dev_like for g in groups):
            group = next(g for g in dev_like if g in groups)
            commands.append(f"python -m pip install -e . --group {group}")
            evidence = f"[dependency-groups] {group}"
        elif any(e in dev_like for e in extras):
            extra = next(e for e in dev_like if e in extras)
            commands.append(f'python -m pip install -e ".[{extra}]"')
            evidence = f"[project.optional-dependencies] {extra}"
        elif reqs:
            commands.extend(f"python -m pip install -r {r}" for r in reqs)
            if pyproject or (root / "setup.py").is_file():
                commands.append("python -m pip install -e .")
            evidence = ", ".join(reqs)
        elif pyproject or (root / "setup.py").is_file():
            commands.append("python -m pip install -e .")
            evidence = "pyproject.toml or setup.py"
        else:
            evidence = ""
        if evidence:
            commands.append("python -m pytest")
            note = "--group needs pip 25.1 or newer." if any("--group" in c for c in commands) else ""
            findings.append(Finding("pip + venv", evidence, commands, note))

    if (root / "mkdocs.yml").is_file():
        findings.append(
            Finding("MkDocs (docs)", "mkdocs.yml", ["mkdocs serve"], "Preview the docs at http://127.0.0.1:8000")
        )
    for docs in ("docs", "doc"):
        if (root / docs / "conf.py").is_file():
            findings.append(
                Finding(
                    "Sphinx (docs)",
                    f"{docs}/conf.py",
                    [f"sphinx-build -b html {docs} {docs}/_build/html"],
                    "Many projects wrap this in `make html` or a tox/nox session.",
                )
            )
            break
    return findings


def report(root: Path) -> str:
    lines = [f"Project: {root.resolve().name}", ""]
    contributing = find_contributing(root)
    if contributing:
        lines.append(f"1. Read {contributing.relative_to(root)} first. If it disagrees with anything below, it wins.")
    else:
        lines.append("1. No CONTRIBUTING file found. Check the README and the project's docs for a developer guide.")
    findings = detect(root)
    if not findings:
        lines.append("2. No setup files found. This may not be a Python project, or its setup lives in the docs.")
        return "\n".join(lines)
    for n, f in enumerate(findings, start=2):
        lines.append(f"{n}. {f.tool}  (found {f.evidence})")
        lines.extend(f"     $ {c}" for c in f.commands)
        if f.note:
            lines.append(f"     {f.note}")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if len(argv) != 1 or not Path(argv[0]).is_dir():
        print("usage: python3 tools/which_setup.py PATH-TO-PROJECT", file=sys.stderr)
        return 2
    print(report(Path(argv[0])))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # ✔ and ✘ print on Windows too
    sys.exit(main(sys.argv[1:]))
