# Lesson 07: Setting up any Python project

**Time:** 3 minute video · 45 minute exercise
**You'll need:** Lessons 03 and 05 done

In Lesson 05 you set up this course repo with `venv`, `pip` and `pytest`. Real
projects use many different tools to do the same job. You don't need to
master them all. You need to **recognise** which one a project uses, and run
two or three of its commands.

## The goal: the tests pass on your machine *before* you change anything

That's always step one. If the tests fail before you've touched anything,
the problem is your setup, not your change. Fix the setup first, or ask.

## Step 1: Read CONTRIBUTING (again)

The setup instructions are usually in CONTRIBUTING or a "development" page
in the docs. **If they exist, follow them exactly.** Everything below is for
understanding what they tell you, or for working it out when they don't.

## Step 2: Let the files tell you

Each tool leaves a file behind. Look at the project's top folder:

| If you see | The project uses | To set up and test |
|---|---|---|
| `uv.lock` | **uv** | `uv sync`, then `uv run pytest` |
| `poetry.lock` or `[tool.poetry]` in `pyproject.toml` | **Poetry** | `poetry install`, then `poetry run pytest` |
| `[tool.hatch.envs...]` in `pyproject.toml` | **Hatch** | `hatch env show` to see environments, `hatch test` to run tests |
| `tox.ini`, `tox.toml` or `[tool.tox]` | **tox** | `tox list`, then `tox run -e <one of them>` |
| `noxfile.py` | **nox** | `nox --list`, then `nox -s <one of them>` |
| `.pre-commit-config.yaml` | **pre-commit** | `pre-commit install` once, then it runs on every commit; `pre-commit run --all-files` to run it now |
| `Makefile` | **Make** | Read it; look for targets like `make test` and `make docs` |
| Only `pyproject.toml`, `setup.py` or `requirements*.txt` | **pip + venv** | Make a venv, then install (see below) and run `python -m pytest` |
| `docs/conf.py` | **Sphinx** docs | `sphinx-build -b html docs docs/_build/html` (often wrapped in `make html` or a tox/nox session) |
| `mkdocs.yml` | **MkDocs** docs | `mkdocs serve`, then open http://127.0.0.1:8000 |

Projects often use several at once. For example: uv for the environment,
pre-commit for linting and tox to test several Python versions.

### Installing with plain pip

After `python3 -m venv .venv` and `source .venv/bin/activate`, install the
project itself in **editable** mode (`-e`), so your changes to the code take
effect immediately, plus its development tools. Which command depends on
where the project lists those tools:

| Where the dev tools are listed | Install command |
|---|---|
| `[dependency-groups]` with a `test` or `dev` group in `pyproject.toml` | `python -m pip install -e . --group test` (needs pip 25.1+: run `python -m pip install --upgrade pip` first) |
| `[project.optional-dependencies]` with a `test` or `dev` extra | `python -m pip install -e ".[test]"` |
| `requirements-dev.txt` or similar | `python -m pip install -r requirements-dev.txt` and `python -m pip install -e .` |

### Tools that install tools

tox, nox, Hatch, Poetry and pre-commit are installed once for your whole
computer, not inside a project's venv. Use **pipx** or **uv tool** for that:

```bash norun
python3 -m pip install --user pipx
pipx install tox
```

or, if you have uv:

```bash norun
uv tool install tox
```

## Step 3: Let the course's detector help

`tools/which_setup.py` does Step 2 for you. Point it at any project you've
cloned:

```bash norun
python3 tools/which_setup.py ../requests
```

Here's what it says for [requests](https://github.com/psf/requests)
(November 2026):

```text
Project: requests

1. Read .github/CONTRIBUTING.md first. If it disagrees with anything below, it wins.
2. tox  (found tox.ini, tox.toml or [tool.tox])
     $ tox list
     $ tox run -e <env from the list>
     Install tox first: pipx install tox
3. pre-commit  (found .pre-commit-config.yaml)
     $ pre-commit install
     $ pre-commit run --all-files
     Runs the project's linters and formatters on every commit.
4. Make  (found Makefile)
     $ make test
     $ make docs
     Read the Makefile to see what each target runs.
5. pip + venv  (found [dependency-groups] test)
     $ python3 -m venv .venv
     $ source .venv/bin/activate
     $ python -m pip install -e . --group test
     $ python -m pytest
     --group needs pip 25.1 or newer.
6. Sphinx (docs)  (found docs/conf.py)
     $ sphinx-build -b html docs docs/_build/html
     Many projects wrap this in `make html` or a tox/nox session.
```

So for requests you can either use tox, which builds its own environments,
or a venv with the `test` group. Either way, `.github/CONTRIBUTING.md` comes
first.

And for [pip](https://github.com/pypa/pip) itself it finds nox:

```text
2. nox  (found noxfile.py)
     $ nox --list
     $ nox -s <session from the list>
```

`nox --list` shows sessions like `test-3.13` and `lint`. Run just the one
you need.

## Step 4: Run a small part of the tests first

Big projects have thousands of tests. While you're working, run only the
tests near your change:

```bash norun
python -m pytest tests/test_utils.py
python -m pytest tests/test_utils.py -k "unquote"
python -m pytest -x
```

- A file path runs only that file.
- `-k "unquote"` runs only tests whose names contain `unquote`.
- `-x` stops at the first failure.

Run the **whole** suite (or what CONTRIBUTING says) once before you push.

## When setup fails

- **Read the last lines of the error.** The useful part is almost always at
  the bottom.
- **Check the Python version.** `pyproject.toml` has `requires-python`; tox
  and nox sessions are often named after versions (`py313`, `test-3.13`).
- **A missing system library** (a C compiler, `libffi`, a database) is common
  in projects with C extensions. CONTRIBUTING usually lists them.
- **Search the project's issues** for your error message. Someone has
  probably hit it before.
- **Still stuck?** Ask in the project's chat or discussions, with the exact
  command and the full error. That's a normal, welcome question.

Next: [Lesson 08: finding an issue](../08-finding-an-issue/).
