# Video script: Setting up any Python project

Target length: about 3 minutes.

## Scene 1: Hook
visual: slide
title: Every project sets up differently
bullets:
- uv, Poetry, Hatch, tox, nox, pre-commit, Make...
- You don't need to master them
- You need to recognise them

> In lesson four you set up a project with a virtual environment, pip and
> pytest. Real projects use lots of different tools to do the same job: uv,
> Poetry, Hatch, tox, nox, Make. You don't need to master any of them. You
> just need to recognise which one a project uses, and run two or three of
> its commands.

## Scene 2: The goal
visual: slide
title: Step zero: tests pass before you change anything
bullets:
- Clone, set up, run the tests
- Failing already? It's your setup, not your change
- Fix the setup first, or ask

> Here's the rule. Before you change a single line, get the project's tests
> passing on your machine. If they fail before you've touched anything, the
> problem is your setup, not your change. And it's much easier to fix now
> than later.

## Scene 3: The files tell you
visual: slide
title: The files tell you which tools
bullets:
- uv.lock → uv sync, uv run pytest
- poetry.lock → poetry install, poetry run pytest
- tox.ini → tox list, tox run -e ...
- noxfile.py → nox --list, nox -s ...
- .pre-commit-config.yaml → pre-commit install

> First, read the contributing file. If it has setup steps, follow them
> exactly. If not, the files in the project tell you. A file called uv dot
> lock means uv: run uv sync, then uv run pytest. Poetry dot lock means
> Poetry. Tox dot ini means tox. A noxfile means nox. And a pre-commit config
> means the project checks your code on every commit.

## Scene 4: Plain pip
visual: terminal
code:
```
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ python -m pip install -e . --group test
(.venv) $ python -m pytest
```

> No special tool? Then it's plain pip, like lesson four. Make a venv,
> activate it, and install the project in editable mode, dash e, so your
> changes take effect straight away. Add its test tools too: here with dash
> dash group test, because this project lists them as a dependency group.
> The written lesson shows the other two common ways.

## Scene 5: The detector
visual: terminal
code:
```
$ python3 tools/which_setup.py ../requests
1. Read .github/CONTRIBUTING.md first.
2. tox  (found tox.ini)
     $ tox list
3. pre-commit  (found .pre-commit-config.yaml)
5. pip + venv  (found [dependency-groups] test)
     $ python -m pip install -e . --group test
```

> The course has a helper that does this detective work for you. Point
> tools slash which setup dot p y at any project you've cloned. For the
> requests library, it finds the contributing file, tox, pre-commit, and a
> test dependency group. So you could use tox, or a venv with the test group.
> Either way, read the contributing file first.

## Scene 6: Run a small part
visual: terminal
code:
```
(.venv) $ python -m pytest tests/test_utils.py
(.venv) $ python -m pytest tests/test_utils.py -k "unquote"
(.venv) $ python -m pytest -x
```

> Big projects have thousands of tests. While you work, run just the tests
> near your change. Give pytest a file, or use dash k to pick tests by name,
> or dash x to stop at the first failure. Then run the whole suite once
> before you push.

## Scene 7: When setup fails
visual: slide
title: When setup fails
bullets:
- Read the last lines of the error
- Check requires-python in pyproject.toml
- Search the project's issues for the error
- Ask, with the exact command and full error

> And when setup fails, which it will sometimes: read the last lines of the
> error first. Check which Python versions the project supports. Search its
> issues for your error message. And if you're still stuck, ask, with the
> exact command and the full error. That's a normal, welcome question.

## Scene 8: Done
visual: slide
title: You can set up any Python project
bullets:
- Read CONTRIBUTING, then let the files tell you
- Tests pass before you change anything
- Next: finding an issue to work on

> That's it. Read the contributing file, let the project's files tell you
> the rest, and get the tests passing before you change anything. Next
> lesson, we find an issue to work on, and make sure nobody else is already
> on it.
