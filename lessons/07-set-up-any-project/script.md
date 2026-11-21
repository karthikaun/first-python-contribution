# Video script: Setting up any Python project

Target length: about 3 minutes.

## Scene 1: Start here
visual: slide
layout: title
title: Every project sets up differently
bullets:
- You don't need to master the tools. You need to recognise them.

> In lesson five, you set up the course repo with a venv, pip and
> {pytest|pie test}. Real projects use many different tools to do the same
> job.

> You don't need to master them all. You need to recognise which one a
> project uses, and run two or three of its commands.

## Scene 2: The goal
visual: slide
title: First: the tests pass before you change anything
bullets:
- That is always step one
- Failing already? The problem is your setup, not your change
- Fix the setup first, or ask

> Here is the goal. The tests pass on your machine, before you change
> anything. That is always step one.

> If the tests fail before you've touched anything, the problem is your
> setup. It is not your change.

> So fix the setup first. Or ask.

## Scene 3: The files tell you
visual: slide
layout: cards
title: Each tool leaves a file behind
bullets:
- uv | `uv.lock` → `uv sync`, then `uv run pytest`
- Poetry | `poetry.lock` → `poetry install`, then `poetry run pytest`
- tox | `tox.ini` → `tox list`, then `tox run -e` and one of them
- nox | `noxfile.py` → `nox --list`, then `nox -s` and one of them
- pre-commit | `.pre-commit-config.yaml` → `pre-commit install`, once
- Make | `Makefile` → read it, and look for `make test`

> First, read the contributing file again. If it has setup instructions,
> follow them exactly. If not, let the files tell you. Each tool leaves a
> file behind. Look at the project's top folder. A file called {uv.lock|u v
> dot lock} means {uv|u v}. Run {uv sync|u v sync}, then {uv run pytest|u v
> run pie test}.

> Poetry dot lock means Poetry.

> {tox.ini|Tox dot ini} means tox. List its environments, then run one of
> them.

> A nox file means nox. It works the same way.

> A pre-commit config means pre-commit. Install it once, and then it runs
> on every commit.

> And a Makefile means Make. Read it, and look for targets like make test.
> Projects often use several of these at once.

## Scene 4: Plain pip
visual: terminal
focus: 1-2 | 3 | 4
notes:
- No special tool? Make a venv, like in Lesson 05
- `-e` is editable mode: your changes to the code take effect immediately
- Then run the tests
code:
```
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ python -m pip install -e . --group test
(.venv) $ python -m pytest
```

> No special tool? Then it is plain pip. Make a venv and activate it, like
> in lesson five.

> Then install the project itself in editable mode. That is dash e. Your
> changes to the code take effect immediately. Add its development tools
> too. Here, with dash dash group test, because this project lists them as a
> dependency group. The written lesson shows the other two ways.

> Then run the tests.

## Scene 5: The detector
visual: terminal
focus: 1 | 4 | 5-7 | 8-9 | 10-13
code:
```
$ python3 tools/which_setup.py ../requests
Project: requests

1. Read .github/CONTRIBUTING.md first. If it disagrees with anything below, it wins.
2. tox  (found tox.ini, tox.toml or [tool.tox])
     $ tox list
     $ tox run -e <env from the list>
3. pre-commit  (found .pre-commit-config.yaml)
4. Make  (found Makefile)
5. pip + venv  (found [dependency-groups] test)
     $ python -m pip install -e . --group test
     $ python -m pytest
6. Sphinx (docs)  (found docs/conf.py)
```

> The course has a helper that does this detective work for you. Point
> which setup {.py|dot p y} at any project you've cloned. Here, the requests
> library.

> First, it tells you to read the contributing file. If that disagrees with
> anything below, it wins.

> Then it finds tox, and shows the commands to run.

> It finds pre-commit, and a Makefile.

> And it finds a test dependency group, for pip and a venv. So for requests,
> you can either use tox, or a venv with the test group. Either way, the
> contributing file comes first.

## Scene 6: Run a small part
visual: terminal
focus: 1 | 2 | 3
notes:
- A file path runs only that file
- `-k` runs only tests whose names contain `unquote`
- `-x` stops at the first failure
code:
```
(.venv) $ python -m pytest tests/test_utils.py
(.venv) $ python -m pytest tests/test_utils.py -k "unquote"
(.venv) $ python -m pytest -x
```

> Big projects have thousands of tests. While you're working, run only the
> tests near your change. A file path runs only that file.

> Dash k runs only tests whose names contain a word. Here, unquote.

> And dash x stops at the first failure. Then run the whole suite once,
> before you push.

## Scene 7: When setup fails
visual: slide
title: When setup fails
bullets:
- Read the last lines of the error
- Check the Python version: `requires-python` in `pyproject.toml`
- Search the project's issues for your error message
- Still stuck? Ask, with the exact command and the full error

> Sometimes setup fails. Read the last lines of the error. The useful part
> is almost always at the bottom.

> Check the Python version the project needs.

> Search the project's issues for your error message. Someone has probably
> hit it before.

> Still stuck? Ask, in the project's chat or discussions, with the exact
> command and the full error. That is a normal, welcome question.

## Scene 8: Done
visual: slide
layout: steps
title: You can set up any Python project
focus: all | all
bullets:
- Read CONTRIBUTING
- Let the files tell you
- Tests pass first
- Then change things

> So. Read the contributing file. Let the project's files tell you the
> rest. And get the tests passing before you change anything.

> Next lesson, we find an issue to work on.
