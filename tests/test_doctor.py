import ast
import sys
from pathlib import Path

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
