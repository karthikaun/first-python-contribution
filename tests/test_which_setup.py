import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from which_setup import detect, find_contributing, make_targets, report  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def make(tmp_path, files):
    for name, text in files.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    return tmp_path


def tools(root):
    return [f.tool for f in detect(root)]


def test_uv_project(tmp_path):
    root = make(tmp_path, {"pyproject.toml": "[project]\nname='x'\n", "uv.lock": ""})
    assert tools(root) == ["uv"]


def test_poetry_and_tox_and_precommit(tmp_path):
    root = make(
        tmp_path,
        {"pyproject.toml": "[tool.poetry]\nname='x'\n", "tox.ini": "", ".pre-commit-config.yaml": ""},
    )
    assert tools(root) == ["Poetry", "tox", "pre-commit"]


def test_pip_with_dependency_group(tmp_path):
    root = make(tmp_path, {"pyproject.toml": "[project]\nname='x'\n\n[dependency-groups]\ntest = ['pytest']\n"})
    (finding,) = detect(root)
    assert finding.tool == "pip + venv"
    assert "python -m pip install -e . --group test" in finding.commands
    assert "25.1" in finding.note


def test_pip_with_extras(tmp_path):
    root = make(
        tmp_path, {"pyproject.toml": "[project]\nname='x'\n\n[project.optional-dependencies]\ndev = ['pytest']\n"}
    )
    assert 'python -m pip install -e ".[dev]"' in detect(root)[0].commands


def test_pip_with_requirements(tmp_path):
    root = make(tmp_path, {"setup.py": "", "requirements-dev.txt": "pytest\n"})
    commands = detect(root)[0].commands
    assert "python -m pip install -r requirements-dev.txt" in commands
    assert "python -m pip install -e ." in commands
    assert detect(root)[0].note == ""


def test_nox_make_and_docs(tmp_path):
    root = make(
        tmp_path,
        {
            "noxfile.py": "",
            "Makefile": "VAR := 1\ntest:\n\tpytest\nlint: test\n\truff check\nother:\n",
            "docs/conf.py": "",
            "mkdocs.yml": "",
        },
    )
    assert tools(root) == ["nox", "Make", "MkDocs (docs)", "Sphinx (docs)"]


def test_make_targets_ignores_variables():
    assert make_targets("CC := gcc\nhelp:\n\t@echo hi\ntest:\n") == ["help", "test"]


def test_contributing_locations(tmp_path):
    assert find_contributing(tmp_path) is None
    make(tmp_path, {".github/CONTRIBUTING.md": "x"})
    assert find_contributing(tmp_path) == tmp_path / ".github/CONTRIBUTING.md"


def test_report_on_this_repo():
    text = report(ROOT)
    assert "Read CONTRIBUTING.md first" in text
    assert "uv sync" in text


def test_report_on_empty_folder(tmp_path):
    assert "No setup files found" in report(tmp_path)
