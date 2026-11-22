import ast
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import doctor  # noqa: E402
import test_commands  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def fake(responses):
    def runner(cmd):
        return responses.get(" ".join(cmd))

    return runner


def test_doctor_runs_on_old_python():
    # Learners may start with an old Python; doctor must still run to tell them.
    ast.parse((ROOT / "tools/doctor.py").read_text(), feature_version=(3, 8))


def test_python_version():
    assert doctor.check_python((3, 13, 1))[0] == doctor.OK
    assert doctor.check_python((3, 9, 6))[0] == doctor.FAIL


def test_git_missing_and_old():
    assert doctor.check_git(fake({}))[0] == doctor.FAIL
    assert doctor.check_git(fake({"git --version": (0, "git version 2.20.1")}))[0] == doctor.FAIL
    assert doctor.check_git(fake({"git --version": (0, "git version 2.47.1 (Apple Git-1)")}))[0] == doctor.OK


def test_email_noreply_ok_other_warns():
    key = "git config --global user.email"
    assert doctor.check_git_email(fake({key: (0, "1+ada@users.noreply.github.com")}))[0] == doctor.OK
    assert doctor.check_git_email(fake({key: (0, "ada@example.com")}))[0] == doctor.WARN
    assert doctor.check_git_email(fake({key: (1, "")}))[0] == doctor.FAIL


def test_gh_auth():
    ok = fake({"gh auth status": (0, "✓ Logged in to github.com account ada (keyring)")})
    status, msg = doctor.check_gh_auth(ok)
    assert status == doctor.OK and "ada" in msg
    assert doctor.check_gh_auth(fake({"gh auth status": (1, "not logged in")}))[0] == doctor.FAIL


def test_upstream():
    fork = {"git remote get-url origin": (0, "https://github.com/ada/first-python-contribution.git")}
    assert doctor.check_upstream(fake(fork))[0] == doctor.FAIL
    fork["git remote get-url upstream"] = (0, "https://github.com/thejesh23/first-python-contribution.git")
    assert doctor.check_upstream(fake(fork))[0] == doctor.OK
    course = {"git remote get-url origin": (0, "https://github.com/thejesh23/first-python-contribution.git")}
    assert doctor.check_upstream(fake(course))[0] == doctor.WARN
    assert doctor.check_upstream(fake({})) is None


def test_command_blocks_skip_norun_and_dedent():
    md = "x\n```bash\necho hi\n```\n```bash norun\ngh auth login\n```\n   ```bash\n   echo indented\n   ```\n"
    assert test_commands.blocks(md) == ["echo hi", "echo indented"]


def test_command_block_after_blank_line_keeps_first_letter():
    assert test_commands.blocks("Text.\n\n```bash\ngit --version\n```\n") == ["git --version"]


def test_expect_fail_block_wrapped(tmp_path):
    import subprocess

    (script,) = test_commands.blocks("```bash expect-fail\ntrue\nfalse\n```\n")
    assert subprocess.run([test_commands.BASH, "-e", "-c", script]).returncode == 0
    (script,) = test_commands.blocks("```bash expect-fail\ntrue\n```\n")
    assert subprocess.run([test_commands.BASH, "-e", "-c", script], capture_output=True).returncode == 1


def test_windows_learners_type_py_for_python3():
    script = "python3 tools/doctor.py\npython3 -m venv .venv\npython -m pytest\n"
    assert test_commands.as_typed_on_windows(script) == "py tools/doctor.py\npy -m venv .venv\npython -m pytest\n"


@pytest.mark.parametrize("tool", ["check_exercise_3.py", "doctor.py", "which_setup.py"])
def test_tools_print_on_a_windows_code_page(tool):
    """Git Bash on Windows gives Python a cp1252 pipe; ✔ and ✘ must not crash the tools."""
    import os
    import subprocess

    tools = Path(__file__).resolve().parent.parent / "tools"
    env = {**os.environ, "PYTHONIOENCODING": "cp1252"}
    args = [sys.executable, str(tools / tool)] + (["."] if tool == "which_setup.py" else [])
    proc = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", env=env, cwd=tools.parent)
    assert "UnicodeEncodeError" not in proc.stderr, proc.stderr
