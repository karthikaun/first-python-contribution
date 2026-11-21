# Video script: Your second PR, from the terminal

Target length: about 8 minutes.

## Scene 1: Hook
visual: slide
title: Code, a test, and CI
bullets:
- A branch, not main
- A Python function and its test
- Checked by CI before it's merged

> Your first commit was three lines in the browser. This one is how real
> Python projects work: a branch, a function, a test for it, and automated
> checks that have to pass before anything is merged. About half an hour,
> start to finish.

## Scene 2: Your two files
visual: slide
title: Two files, named after you
bullets:
- practice/greetings/ada_lovelace.py: your greet function
- practice/tests/test_ada_lovelace.py: its test
- Username in lowercase, hyphens become underscores

> You'll add two files. Our example learner is ada dash lovelace. Python
> can't import a module with a hyphen in its name, so the files use ada
> underscore lovelace instead: your username in lowercase, with hyphens
> turned into underscores.

## Scene 3: Fresh start and a venv
visual: terminal
code:
```
$ git switch main
$ git pull upstream main
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ python -m pip install pytest ruff
```

> Start from an up to date main: switch to main and pull from upstream. Then
> make a virtual environment, a private Python just for this project, so
> nothing you install clashes with anything else. Activate it, and your
> prompt starts with dot venv. Then install pytest, which runs tests, and
> ruff, which checks your code's style.

## Scene 4: A branch
visual: terminal
code:
```
(.venv) $ git switch -c exercise-2
Switched to a new branch 'exercise-2'
```

> Never work on main. Make a branch called exercise two. One branch per
> pull request.

## Scene 5: Test first
visual: code
code:
```
from greetings.ada_lovelace import greet


def test_greet_includes_name():
    assert "Sam" in greet("Sam")
```

> Here's a habit good contributors have: write the test first. A test is a
> function whose name starts with test underscore. Assert means this must be
> true. Here: the greeting for Sam must include the name Sam.

## Scene 6: Red
visual: terminal
code:
```
(.venv) $ python -m pytest practice
E   ModuleNotFoundError: No module named 'greetings.ada_lovelace'
ERROR practice/tests/test_ada_lovelace.py
```

> Run python dash m pytest practice. It fails: no module named greetings dot
> ada lovelace. Of course. We haven't written it yet. Seeing your test fail
> first proves it's really testing something.

## Scene 7: The function
visual: code
code:
```
"""Greeting for ada-lovelace."""


def greet(name: str) -> str:
    """Return a friendly greeting for name."""
    return f"Hello, {name}! Welcome to open source."
```

> Now the function. The text in triple quotes is a docstring: it says what
> this is for. Name colon str, and arrow str, are type hints: the name is a
> string, and so is the result. And the f string puts the name into the
> greeting.

## Scene 8: Green, formatted, linted
visual: terminal
code:
```
(.venv) $ python -m pytest practice
============== 6 passed in 0.01s ==============
(.venv) $ ruff format practice
7 files left unchanged
(.venv) $ ruff check practice
All checks passed!
```

> Run pytest again. Six passed. Some of those are the course's own tests,
> checking every learner's greeting follows the rules, yours included. Then
> ruff format, which fixes your code's style, and ruff check, which looks for
> mistakes. CI runs these exact three commands, so if they pass here, they'll
> pass there.

## Scene 9: Commit, push, pull request
visual: terminal
code:
```
(.venv) $ git add practice/greetings/ada_lovelace.py practice/tests/test_ada_lovelace.py
(.venv) $ git commit -m "Add exercise 2 greeting for ada-lovelace"
(.venv) $ git push -u origin exercise-2
(.venv) $ gh repo set-default thejesh23/first-python-contribution
(.venv) $ gh pr create --fill
```

> Add your two files, and only those two. Commit with a clear message.
> Push the branch to origin, your fork. Then tell g h where pull requests
> should go, once, and run g h p r create dash dash fill. It uses your
> commit message as the title and prints a link to your pull request.

## Scene 10: Watch CI
visual: terminal
code:
```
(.venv) $ gh pr checks --watch
✓  Exercise 2 tests
✓  Exercise 2 review
(.venv) $ gh pr view --comments
```

> Run g h p r checks dash dash watch. First your tests run in CI. Then the
> review bot checks your file names and your code, comments, and if
> everything passed, merges your pull request. If something failed, the
> comment tells you where to look.

## Scene 11: When a test fails
visual: terminal
code:
```
>       assert greet("Sam") == "Hello, Sam! Welcome to open source."
E         - Hello, Sam! Welcome to open source.
E         ?  ^^^^
E         + Hi, Sam! Welcome to open source.
E         ?  ^
```

> And when a test fails, don't panic. Pytest shows you exactly what
> happened. Minus is what the test expected. Plus is what your code returned.
> The little arrows mark the difference. Fix it, run pytest, commit, push.
> Your pull request updates itself and CI runs again. Every contributor does
> this loop all the time.

## Scene 12: Done
visual: slide
title: You just did the real thing
bullets:
- Branch, test, code, format, lint
- Push, pull request, CI, merge
- Next: the house rules every project has

> That's the whole real world workflow: branch, test, code, format, lint,
> push, pull request, CI, merge. Next, before you touch someone else's
> project, we'll look at the house rules almost every project has, and the
> ones that catch beginners out.
