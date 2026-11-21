import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import conflict_lab  # noqa: E402

IDENTITY = {
    "GIT_AUTHOR_NAME": "t",
    "GIT_AUTHOR_EMAIL": "t@example.com",
    "GIT_COMMITTER_NAME": "t",
    "GIT_COMMITTER_EMAIL": "t@example.com",
}


def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, env={**os.environ, **IDENTITY})


def test_lab_has_open_pr_and_a_real_conflict(tmp_path):
    work = conflict_lab.create(tmp_path / "lab")
    assert (tmp_path / "lab" / "REVIEW.md").is_file()
    assert git(work, "branch", "--show-current").stdout.strip() == "fix-greeting"
    assert "upstream" in git(work, "remote").stdout
    # Your branch is already pushed to your fork.
    assert git(work, "rev-parse", "origin/fix-greeting").stdout == git(work, "rev-parse", "HEAD").stdout
    git(work, "fetch", "-q", "upstream")
    rebase = git(work, "rebase", "upstream/main")
    assert rebase.returncode != 0
    assert "CONFLICT" in rebase.stdout + rebase.stderr
    assert "<<<<<<<" in (work / "app.py").read_text()


def test_lab_refuses_to_overwrite(tmp_path):
    conflict_lab.create(tmp_path / "lab")
    with pytest.raises(SystemExit):
        conflict_lab.create(tmp_path / "lab")
