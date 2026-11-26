# Lesson 10: Making the change

**Time:** 3 minute video · 40 minute exercise
**You'll need:** this repo set up with your venv (Lesson 05)

You've found an issue and claimed it. Now make the change the way
maintainers want it: **small, tested, documented, and easy to review.**

You'll practise on a bug planted in this repo, `slugify` in
`practice/textkit.py`. Exercise 3 is **local only**: don't open a pull
request for it, because the next learner needs the bug.

## The bug report

> **slugify leaves doubled and stray hyphens**
>
> `slugify("Hello  World")` returns `"hello--world"`, and
> `slugify("Hello, World!")` returns `"hello,-world!"`. Expected
> `"hello-world"` for both. Leading/trailing spaces also give leading/trailing
> hyphens.

## Step 1: Branch, then reproduce

```bash norun
git switch main
git pull upstream main
git switch -c fix-slugify
cd practice
python -c "from textkit import slugify; print(repr(slugify('Hello  World')))"
cd ..
```

```text
'hello--world'
```

**Always see the bug with your own eyes before fixing it.** If you can't
reproduce it, say so in the issue (with your versions) instead of guessing.

## Step 2: Write a test that fails

A test that reproduces a bug is called a **regression test**: it stops the
bug ever coming back. Add to `practice/tests/test_textkit.py`:

```python
import pytest

from textkit import slugify


def test_slugify_two_words():
    assert slugify("Hello World") == "hello-world"


@pytest.mark.parametrize(
    ("title", "slug"),
    [
        ("Hello  World", "hello-world"),
        ("  Hello World ", "hello-world"),
        ("Hello, World!", "hello-world"),
        ("Python 3.13 is out", "python-3-13-is-out"),
    ],
)
def test_slugify_collapses_separators(title, slug):
    assert slugify(title) == slug
```

`@pytest.mark.parametrize` runs the same test once per pair, so one test
covers every case in the bug report. Run it:

```bash norun
python -m pytest practice/tests/test_textkit.py
```

```text
FAILED practice/tests/test_textkit.py::test_slugify_collapses_separators[Hello  World-hello-world]
FAILED practice/tests/test_textkit.py::test_slugify_collapses_separators[  Hello World -hello-world]
FAILED practice/tests/test_textkit.py::test_slugify_collapses_separators[Hello, World!-hello-world]
FAILED practice/tests/test_textkit.py::test_slugify_collapses_separators[Python 3.13 is out-python-3-13-is-out]
4 failed, 1 passed in 0.01s
```

Four failures, one per case. Good: your test catches the bug.

## Step 3: The smallest fix that works

Change only what the issue needs. Don't rename things, reformat other
functions or "tidy up" nearby code in the same PR: it makes your change
harder to review, and that's the fastest way to get a PR stuck.

```python
"""Small text helpers used by Exercise 3 (Lesson 10)."""

import re


def slugify(title: str) -> str:
    """Turn a title into a URL slug, e.g. "Hello, World!" -> "hello-world".

    Letters and digits are kept; every run of other characters becomes a
    single hyphen, and hyphens at the start and end are removed.
    """
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
```

Notice the **docstring changed too**: it now describes the real behaviour.
If a project has user docs for this function, update them in the same PR.

## Step 4: Run the tests, then everything

```bash norun
python -m pytest practice/tests/test_textkit.py
python -m pytest practice
ruff format practice
ruff check practice
```

```text
9 passed in 0.01s
```

Narrow first (fast), then the whole suite and the linters, exactly as CI
will.

## Step 5: A changelog entry

Many projects want every user-visible change described for the release
notes. **How depends on the project. CONTRIBUTING will say.** The common
styles:

| Style | What you add | Seen in |
|---|---|---|
| **News fragments** (towncrier and similar) | A small file per change, e.g. `changelog.d/1234.bugfix.md` | Many larger Python projects |
| **blurb** | A file under `Misc/NEWS.d/` made with the `blurb` tool | CPython |
| **CHANGELOG.md** | A line under an "Unreleased" heading | Many smaller projects |
| **Nothing** | Maintainers write release notes themselves | Also common |

This repo uses news fragments. Add `practice/news/slugify-separators.bugfix.md`:

```text
Fixed `slugify` producing doubled or stray hyphens for titles with repeated
spaces, leading or trailing spaces, or punctuation.
```

Write it for **users**: what was wrong, and what happens now.

## Step 6: A good commit message

```bash norun
git add practice/textkit.py practice/tests/test_textkit.py practice/news/slugify-separators.bugfix.md
git commit
```

Without `-m`, git opens your editor so you can write a full message:

```text
Fix slugify for repeated spaces and punctuation

slugify("Hello  World") returned "hello--world", and punctuation was kept
in the slug. Replace every run of non-alphanumeric characters with one
hyphen and strip hyphens from the ends.
```

- **Subject line:** what the commit does, in the imperative ("Fix", not
  "Fixed"), 72 characters or fewer, no full stop.
- **Blank line**, then a **body** saying *why*, wrapped at about 72 characters.
- Some projects want a format like `fix: ...` (Conventional Commits) or a
  sign-off (`git commit -s`, Lesson 06). CONTRIBUTING will say.

## Step 7: Check it

```bash norun
python tools/check_exercise_3.py
```

```text
✔ slugify handles every case in the bug report
✔ your test fails on the original buggy code, so it catches the bug
✔ your test passes on your fix
✔ all practice tests pass
✔ news fragment: practice/news/slugify-separators.bugfix.md
✔ commit message: "Fix slugify for repeated spaces and punctuation"

All done. Great fix!
```

The second line matters most: the checker runs **your test against the
original buggy code**. A test that passes on broken code doesn't test
anything.

## In a real project: open the pull request

Your fix is committed. In a real project the next step is the pull request,
and its title and description are your pitch to the reviewer.
[Lesson 11](../11-opening-the-pull-request/) is about writing them well.

## Not every contribution is code

Two contributions every project values, and that need no fix at all:

**A docs fix.** A wrong example, a broken link, a step that didn't work for
you in Lesson 07. Same workflow: branch, edit, build the docs if you can,
PR.

**A good bug report.** If you find a bug you can't fix, a clear report is a
real contribution. [Lesson 09](../09-opening-an-issue/) shows what goes in one.

Next: [Lesson 11: opening the pull request](../11-opening-the-pull-request/).
