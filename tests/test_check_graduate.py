import re
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import check_graduate as g  # noqa: E402
import graduates_wall as wall  # noqa: E402

GOOD = (
    'name = "Ada Lovelace"\n'
    'github = "ada"\n'
    'pr = "https://github.com/psf/requests/pull/123"\n'
    'message = "Fixed a docs example."\n'
)


def pr_data(**overrides):
    data = {
        "merged": True,
        "user": {"login": "ada"},
        "merged_by": {"login": "maintainer"},
        "base": {"repo": {"full_name": "psf/requests", "owner": {"login": "psf"}, "fork": False}},
    }
    data.update(overrides)
    return data


def test_good_file_and_pr():
    result, values = g.parse_source(GOOD)
    assert result.ok and values["pr"].endswith("/pull/123")
    assert g.check_values(values, "ada").ok
    assert g.check_pr_data(pr_data(), "ada").ok


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        (GOOD.replace('message = "Fixed a docs example."\n', ""), "`message` is missing"),
        (GOOD + "import os\n", "use only four lines"),
        (GOOD.replace("Ada Lovelace", ""), "`name` is empty"),
        ('name = "x\n', "isn't valid Python"),
    ],
)
def test_bad_sources(source, expected):
    result, _ = g.parse_source(source)
    assert any(expected in e for e in result.errors), result.errors


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ({"github": "bob", "pr": "https://github.com/a/b/pull/1"}, "opened by `ada`"),
        ({"github": "ada", "pr": "https://gitlab.com/a/b/-/merge_requests/1"}, "GitHub pull request link"),
        ({"github": "ada", "pr": "https://github.com/a/b/issues/1"}, "GitHub pull request link"),
    ],
)
def test_bad_values(values, expected):
    assert any(expected in e for e in g.check_values(values, "ada").errors)


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        (pr_data(merged=False), "isn't merged yet"),
        (pr_data(user={"login": "bob"}), "opened by `bob`"),
        (pr_data(merged_by={"login": "ada"}), "merged that pull request yourself"),
        (
            pr_data(base={"repo": {"full_name": "ada/tool", "owner": {"login": "ada"}, "fork": False}}),
            "your own repository",
        ),
        (pr_data(base={"repo": {"full_name": "bob/requests", "owner": {"login": "bob"}, "fork": True}}), "is a fork"),
        (
            pr_data(
                base={
                    "repo": {
                        "full_name": "firstcontributions/first-contributions",
                        "owner": {"login": "firstcontributions"},
                        "fork": False,
                    }
                }
            ),
            "practice repository",
        ),
    ],
)
def test_bad_prs(data, expected):
    assert any(expected in e for e in g.check_pr_data(data, "ada").errors)


def test_merged_by_missing_is_accepted():
    assert g.check_pr_data(pr_data(merged_by=None), "ada").ok


@pytest.mark.parametrize(
    ("paths", "expected"),
    [(["graduates/ada.py"], True), (["graduates/README.md"], False), (["first-commits/ada.py"], False)],
)
def test_is_learner_pr(paths, expected):
    assert g.is_learner_pr(paths) is expected


def test_validate_with_fake_github(tmp_path, monkeypatch):
    def git(*args):
        return subprocess.run(["git", *args], cwd=tmp_path, check=True, capture_output=True, text=True).stdout.strip()

    git("init", "-q", "-b", "main")
    git("config", "user.email", "t@example.com")
    git("config", "user.name", "t")
    (tmp_path / "graduates").mkdir()
    (tmp_path / "graduates/README.md").write_text("wall\n")
    git("add", ".")
    git("commit", "-qm", "base")
    base = git("rev-parse", "HEAD")
    (tmp_path / "graduates/ada.py").write_text(GOOD)
    git("add", ".")
    git("commit", "-qm", "graduate")
    monkeypatch.chdir(tmp_path)
    assert g.validate("ada", base, "HEAD", fetch=lambda url: pr_data()).ok
    assert not g.validate("ada", base, "HEAD", fetch=lambda url: None).ok
    assert not g.validate("ada", base, "HEAD", fetch=lambda url: pr_data(merged=False)).ok


def test_wall_escapes_and_lists(tmp_path):
    (tmp_path / "ada.py").write_text(GOOD.replace("Fixed a docs example.", "<img src=x> [click](https://evil) | *hi*"))
    (tmp_path / "broken.py").write_text("name = 'x")
    text = wall.render(tmp_path)
    assert "**1 graduate**" in text
    assert "[psf/requests#123](https://github.com/psf/requests/pull/123)" in text
    assert re.search(r"(?<!\\)<img", text) is None and "\\<img" in text
    assert "](https://evil)" not in text
    assert "\\|" in text


def test_wall_empty(tmp_path):
    assert "No graduates yet" in wall.render(tmp_path)
