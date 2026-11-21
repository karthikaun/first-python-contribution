# Exercise 2: a Python function and its test

This is the hands-on part of [Lesson 04](../lessons/04-second-pr-from-terminal/).
You add two files, named after your GitHub username (lowercase, with `-`
replaced by `_`, because Python module names can't contain hyphens):

```
practice/greetings/YOUR_NAME.py        # your greet() function
practice/tests/test_YOUR_NAME.py       # your test for it
```

Your function must look like this (the message is up to you):

```python
"""Greeting for YOUR-USERNAME."""


def greet(name: str) -> str:
    """Return a friendly greeting for name."""
    return f"Hello, {name}! Welcome to open source."
```

Before you push, run the same checks CI will run:

```bash norun
python -m pytest practice
ruff format practice
ruff check practice
```

When your pull request's tests pass, a bot merges it.

**Rules for your greeting** (checked by `tests/test_all_greetings.py` and the bot):

- `greet(name)` returns one line of text, at most 120 characters, that includes `name`.
- Your files contain functions only: no `import` in the greeting, and nothing
  that reads files, runs programs or calls `eval`.

# Exercise 3: fix a planted bug (local only)

`practice/textkit.py` has a bug on purpose. [Lesson 08](../lessons/08-making-the-change/)
walks you through fixing it on a branch, and `python tools/check_exercise_3.py`
checks your work. **Don't open a pull request for it**: the next learner
needs the bug.
