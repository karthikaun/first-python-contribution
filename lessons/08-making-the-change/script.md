# Video script: Making the change

Target length: about 3 minutes.

## Scene 1: Start here
visual: slide
layout: title
title: Small, tested, documented, easy to review
bullets:
- Make the change the way maintainers want it.

> You've found an issue, and claimed it. Now make the change the way
> maintainers want it. Small, tested, documented, and easy to review.

> You'll practise on a bug planted in the course repo, in a function called
> slugify.

## Scene 2: The plan
visual: slide
layout: steps
title: Six steps to a change they can merge
bullets:
- Reproduce the bug
- Write a failing test
- Make the smallest fix
- Run everything
- Changelog entry
- Commit message

> Here is the plan. Reproduce the bug.

> Write a test that fails.

> Make the smallest fix that works.

> Run the tests, then everything.

> Add a changelog entry.

> And write a good commit message.

## Scene 3: Reproduce
visual: terminal
focus: 1 | 2-3 | 4
notes:
- A new branch for the fix
- Call the function yourself
- Two hyphens. The bug is real.
code:
```
$ git switch -c fix-slugify
$ cd practice
$ python -c "from textkit import slugify; print(repr(slugify('Hello  World')))"
'hello--world'
```

> The bug report says, slugify of Hello, two spaces, World, returns hello,
> two hyphens, world. First, make a branch.

> Then call the function yourself.

> There it is. Two hyphens. Always see the bug with your own eyes before
> fixing it. If you can't reproduce it, say so in the issue, instead of
> guessing.

## Scene 4: A failing test
visual: code
file: practice/tests/test_textkit.py
focus: all | 1-9 | 4-7 | 10-11
notes:
- A test that reproduces a bug is a regression test
- `parametrize` runs the same test once per pair
- One pair for every case in the bug report
- Each title must give its slug
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

> Next, write a test that fails. A test that reproduces a bug is called a
> regression test. It stops the bug ever coming back.

> Parametrize runs the same test once per pair.

> So one test covers every case in the bug report.

> For each pair, the slug of the title must equal the expected slug.

## Scene 5: Red
visual: terminal
focus: 1 | 2
notes:
- Run only this test file
- Four failures, one per case. Your test catches the bug.
code:
```
$ python -m pytest practice/tests/test_textkit.py
4 failed, 1 passed in 0.01s
```

> Run it.

> Four failures. One per case. Good. Your test catches the bug.

## Scene 6: The smallest fix
visual: code
file: practice/textkit.py
focus: 7 | 2-5 | all
notes:
- Every run of other characters becomes one hyphen. Then strip the ends.
- The docstring changed too. It describes the real behaviour.
- Change only what the issue needs. No tidying up nearby code.
code:
```
def slugify(title: str) -> str:
    """Turn a title into a URL slug, e.g. "Hello, World!" -> "hello-world".

    Letters and digits are kept; every run of other characters becomes a
    single hyphen, and hyphens at the start and end are removed.
    """
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
```

> Now the smallest fix that works. Letters and digits are kept. Every run of
> other characters becomes a single hyphen. And hyphens at the start and end
> are removed.

> Notice that the docstring changed too. It now describes the real
> behaviour.

> Change only what the issue needs. Don't rename things, or tidy up nearby
> code, in the same pull request. That makes your change harder to review.

## Scene 7: Run everything
visual: terminal
focus: 1 | 2 | 3-4
notes:
- Narrow first: it is fast
- Then the whole suite
- Then the linters, exactly as CI will
code:
```
$ python -m pytest practice/tests/test_textkit.py
$ python -m pytest practice
$ ruff format practice
$ ruff check practice
```

> Now run the tests. Narrow first, because it's fast.

> Then the whole suite.

> Then the linters. Exactly as {CI|C I} will.

## Scene 8: Changelog
visual: slide
layout: cards
title: A changelog entry, if the project wants one
bullets:
- News fragments | A small file per change, like `changelog.d/1234.bugfix.md` | Many larger projects
- blurb | A file under `Misc/NEWS.d/`, made with the `blurb` tool | CPython
- CHANGELOG.md | A line under an "Unreleased" heading | Many smaller projects
- Nothing | Maintainers write the release notes themselves | Also common

> Many projects want every user visible change described, for the release
> notes. How depends on the project. The contributing file will say. Some
> use news fragments. A small file per change.

> CPython uses a tool called blurb.

> Many smaller projects have a changelog file. You add a line under
> Unreleased.

> And some want nothing. This repo uses news fragments. Write yours for
> users. What was wrong, and what happens now.

## Scene 9: Commit message
visual: code
lang: text
file: Commit message
focus: 1 | 3-5 | all
notes:
- Subject: what the commit does. "Fix", not "Fixed". 72 characters or fewer.
- A blank line, then a body saying why
- Run `git commit` without `-m`, and git opens your editor
code:
```
Fix slugify for repeated spaces and punctuation

slugify("Hello  World") returned "hello--world", and punctuation was kept
in the slug. Replace every run of non-alphanumeric characters with one
hyphen and strip hyphens from the ends.
```

> Then a good commit message. The subject line says what the commit does,
> like an instruction. Fix, not fixed. Keep it to seventy two characters or
> fewer, with no full stop.

> Then a blank line, and a body saying why.

> To write a full message like this, run git commit without dash m. Git
> opens your editor.

## Scene 10: The checker
visual: terminal
focus: 1 | 2 | 3 | all
code:
```
$ python tools/check_exercise_3.py
✔ slugify handles every case in the bug report
✔ your test fails on the original buggy code, so it catches the bug
✔ your test passes on your fix
✔ all practice tests pass
✔ news fragment: practice/news/slugify-separators.bugfix.md
✔ commit message: "Fix slugify for repeated spaces and punctuation"

All done. Great fix!
```

> The course has a checker for this exercise.

> It checks that slugify handles every case in the bug report.

> The next line matters most. The checker runs your test against the
> original buggy code. A test that passes on broken code doesn't test
> anything.

> It also checks your news fragment, and your commit message. One more
> thing. This exercise is local only. Don't open a pull request for it,
> because the next learner needs the bug.

## Scene 11: Not just code
visual: slide
layout: cards
title: Not every contribution is code
bullets:
- A docs fix | A wrong example, a broken link, a step that didn't work for you.
- A good bug report | What happened, what you expected, a minimal example, and your versions.

> And remember, not every contribution is code. A docs fix counts. A wrong
> example, a broken link, a step that didn't work for you.

> So does a good bug report. The minimal example is the most valuable part.
> The smallest code that shows the problem, which a maintainer can paste and
> run.

## Scene 12: Done
visual: slide
title: A change maintainers can merge
bullets:
- Reproduce, failing test, smallest fix
- Docs, changelog, commit message
- In a real PR: `Fixes #1234` closes the issue on merge

> Reproduce. Failing test. Smallest fix.

> Docs, changelog, and a good commit message.

> And when you open a real pull request, write Fixes, hash, and the issue
> number in the description. GitHub closes the issue when it's merged. Next
> lesson, {CI|C I} and code review.
