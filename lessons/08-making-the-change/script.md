# Video script: Making the change

Target length: about 8 minutes.

## Scene 1: Hook
visual: slide
title: Small, tested, documented, easy to review
bullets:
- Reproduce the bug
- A test that fails
- The smallest fix
- A changelog entry and a good commit message

> You've found an issue and claimed it. Now let's make the change the way
> maintainers want it: small, tested, documented, and easy to review. We'll
> practise on a bug planted in the course repo, in a function called
> slugify.

## Scene 2: Reproduce
visual: terminal
code:
```
$ git switch -c fix-slugify
$ cd practice
$ python -c "from textkit import slugify; print(repr(slugify('Hello  World')))"
'hello--world'
```

> The bug report says slugify of Hello, two spaces, World gives a double
> hyphen. Make a branch, then see it for yourself. There it is: hello, dash
> dash, world. Always reproduce a bug before you fix it. If you can't,
> say so in the issue instead of guessing.

## Scene 3: A failing test
visual: code
code:
```
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

> Next, a test that fails. Parametrize runs the same test once for each
> pair, so one test covers every case in the bug report. A test like this
> is called a regression test, because it stops the bug from ever coming
> back.

## Scene 4: Red
visual: terminal
code:
```
$ python -m pytest practice/tests/test_textkit.py
FAILED ...[Hello  World-hello-world]
FAILED ...[  Hello World -hello-world]
FAILED ...[Hello, World!-hello-world]
FAILED ...[Python 3.13 is out-python-3-13-is-out]
4 failed, 1 passed in 0.01s
```

> Run it. Four failures, one for each case. Good. That proves your test
> catches the bug.

## Scene 5: The smallest fix
visual: code
code:
```
def slugify(title: str) -> str:
    """Turn a title into a URL slug, e.g. "Hello, World!" -> "hello-world".

    Letters and digits are kept; every run of other characters becomes a
    single hyphen, and hyphens at the start and end are removed.
    """
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
```

> Now the smallest fix that works. Every run of characters that aren't
> letters or digits becomes one hyphen, then we strip hyphens from the ends.
> Notice the docstring changed too, so it describes what the function really
> does. And don't tidy up anything else in the same pull request. Unrelated
> changes make reviews slow.

## Scene 6: Changelog
visual: slide
title: A changelog entry, if the project wants one
bullets:
- News fragments: changelog.d/1234.bugfix.md
- CPython: blurb, in Misc/NEWS.d
- CHANGELOG.md: a line under Unreleased
- CONTRIBUTING says which

> Many projects want every change described for the release notes. Some use
> small news fragment files, CPython uses a tool called blurb, others have a
> changelog file. The contributing file tells you which. Write it for users:
> what was wrong, and what happens now.

## Scene 7: Commit message
visual: code
code:
```
Fix slugify for repeated spaces and punctuation

slugify("Hello  World") returned "hello--world", and punctuation was kept
in the slug. Replace every run of non-alphanumeric characters with one
hyphen and strip hyphens from the ends.
```

> Then a good commit message. A short subject saying what the commit does,
> like an instruction: fix, not fixed. A blank line. Then a body saying why.
> Reviewers, and people reading the history years from now, will thank you.

## Scene 8: The checker
visual: terminal
code:
```
$ python tools/check_exercise_3.py
✔ slugify handles every case in the bug report
✔ your test fails on the original buggy code, so it catches the bug
✔ your test passes on your fix
✔ all practice tests pass
✔ news fragment: practice/news/slugify-separators.bugfix.md
✔ commit message: "Fix slugify for repeated spaces and punctuation"
```

> The course has a checker for this exercise. The most important line is
> the second one: it runs your test against the original buggy code. A test
> that passes on broken code doesn't test anything.

## Scene 9: Not just code
visual: slide
title: Not every contribution is code
bullets:
- A docs fix: wrong examples, broken links, missing steps
- A bug report with a minimal example and versions
- Fixes #1234 in your PR closes the issue on merge

> And remember, not every contribution is code. Fixing the docs counts. So
> does a clear bug report, with the smallest code that shows the problem,
> and your versions. When you do open a pull request, write fixes, hash, and
> the issue number in the description, and GitHub closes the issue when it's
> merged.

## Scene 10: Done
visual: slide
title: A change maintainers can merge
bullets:
- Reproduce, failing test, smallest fix
- Docs, changelog, commit message
- Next: CI and code review

> Reproduce, failing test, smallest fix, docs, changelog, a good commit
> message. That's a change maintainers can merge. Next lesson: what happens
> after you open the pull request, when CI goes red and the reviewer has
> questions.
