# Video script: Your second PR, from the terminal

Target length: about 6 minutes.

## Scene 1: Start here
visual: slide
layout: title
title: Your second PR, from the terminal
bullets:
- A branch. A function. A test. Checked by CI before it's merged.

> Your first pull request was three lines, typed in the browser. This one is
> different.

> This time you'll work the way real Python projects work. On a branch. From
> the terminal. With a function, and a test for it. And automated checks have
> to pass before anything is merged.

## Scene 2: The plan
visual: slide
layout: steps
title: Ten small steps
focus: 1-3 | 4-6 | 7-10
bullets:
- Update main
- Make a venv
- Make a branch
- Write the test
- Write the function
- Format and lint
- Commit
- Push
- Pull request
- Watch CI

> Here is the plan. Ten small steps. First, you get ready. Update main, make
> a virtual environment, and make a branch.

> Then you write. The test first. Then the function. Then you format and
> lint.

> Then you ship it. Commit, push, open the pull request, and watch
> {CI|C I}. Let's go through them one by one.

## Scene 3: Your two files
visual: slide
title: Two files, named after you
bullets:
- `practice/greetings/ada_lovelace.py` holds your function
- `practice/tests/test_ada_lovelace.py` holds its test
- `Ada-Lovelace` becomes `ada_lovelace`: lowercase, and `-` becomes `_`

> You will add two files. The first one holds a function called greet. It
> returns a greeting.

> The second one holds a test that checks the function.

> Both are named after you. Our example learner is ada dash lovelace. Python
> can't import a module with a hyphen in its name. So write your username in
> lowercase, and replace each hyphen with an underscore.

## Scene 4: Start from the latest upstream
visual: terminal
focus: 1 | 2 | 3
notes:
- Go into your copy of the course repo
- Always start new work from `main`
- `upstream` is the original repo. This gets its newest commits.
code:
```
$ cd first-python-contribution
$ git switch main
$ git pull upstream main
```

> Step one. Open your terminal, and go into the course folder.

> Switch to main.

> Then pull from upstream. Now your main is up to date. Always start new work
> from an up to date main.

## Scene 5: Make a virtual environment
visual: terminal
focus: 1 | 2 | 3
notes:
- A venv is a private Python, just for this project
- Windows (Git Bash): `source .venv/Scripts/activate`
- `pytest` runs tests. `ruff` checks and formats code.
code:
```
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ python -m pip install pytest ruff
```

> Step two. Make a virtual environment. People call it a venv. It is a
> private Python, just for this project. Whatever you install in it can't
> clash with your other projects.

> Now activate it. On Windows, in Git Bash, the path says Scripts instead of
> bin.

> Look at the prompt. It now starts with {.venv|dot venv}. That means the
> venv is active. Now install two tools. {pytest|Pie test} runs tests. Ruff
> checks and formats your code. If you open a new terminal later, run the
> source line again.

## Scene 6: Make a branch
visual: terminal
focus: 1 | 1-2
notes:
- `-c` means create
- One branch per pull request. Never work on `main`.
code:
```
(.venv) $ git switch -c exercise-2
Switched to a new branch 'exercise-2'
```

> Step three. Make a branch. Git switch, dash c, {exercise-2|exercise two}.

> Never work on main directly. One branch per pull request.

## Scene 7: Write the test first
visual: code
file: practice/tests/test_ada_lovelace.py
focus: all | 1 | 4 | 5
notes:
- Create this file in your editor
- Import the function you are about to write
- A test is a function whose name starts with `test_`
- `assert` means: this must be true
code:
```
from greetings.ada_lovelace import greet


def test_greet_includes_name():
    assert "Sam" in greet("Sam")
```

> Step four. Write the test first. Yes, before the function. Create this
> file in your editor.

> Line one imports greet, the function you are about to write.

> A test is just a function whose name starts with test underscore.

> And assert says, this must be true. Here, the greeting for Sam must
> include the name Sam.

## Scene 8: Watch it fail
visual: terminal
focus: 1 | 2 | 3
notes:
- Run the tests in the `practice` folder
- It can't find your function. You haven't written it yet.
- A test that fails first is a test that really tests something
code:
```
(.venv) $ python -m pytest practice
E   ModuleNotFoundError: No module named 'greetings.ada_lovelace'
ERROR practice/tests/test_ada_lovelace.py
```

> Now run the tests. Python, dash m, {pytest|pie test}, practice.

> It fails. Module not found. No module named greetings dot ada lovelace.

> And that's the point. The test can't find your function, because you
> haven't written it yet. Seeing a test fail first proves that it actually
> tests something.

## Scene 9: Write the function
visual: code
file: practice/greetings/ada_lovelace.py
focus: all | 1,5 | 4 | 6
notes:
- Create this second file
- Triple quotes make a docstring: what this is for
- Type hints: `name` is a string, and so is the result
- An f-string: `{name}` is replaced by the value of `name`
code:
```
"""Greeting for ada-lovelace."""


def greet(name: str) -> str:
    """Return a friendly greeting for name."""
    return f"Hello, {name}! Welcome to open source."
```

> Step five. Write the function. Create the second file.

> The text in triple quotes is a docstring. It says what the module, or the
> function, is for.

> {name: str|Name, colon, s t r}, and the arrow, are type hints. They say
> that name is a string, and so is the result.

> The last line is an f string. The name in curly brackets is replaced by
> the real name. Change the message if you like. It must include the name,
> and fit on one line.

## Scene 10: Watch it pass
visual: terminal
focus: 1 | 2 | 3-5 | 7
notes:
- Same command as before
- Each `.` is one passing test. This file is yours.
- The course's own tests. One checks every learner's `greet`, yours too.
- All green
code:
```
(.venv) $ python -m pytest practice
practice/tests/test_ada_lovelace.py .                                    [ 14%]
practice/tests/test_all_greetings.py ...                                 [ 57%]
practice/tests/test_textkit.py .                                         [ 71%]
practice/tests/test_thejesh23.py ..                                      [100%]

============================== 7 passed in 0.01s ===============================
```

> Run the same command again.

> This time, your test file has a dot next to it. Each dot is one passing
> test.

> The other files were already in the course. One of them, test all
> greetings, checks that every learner's greeting follows the rules. Yours
> too.

> And at the bottom, everything passed. Your number may be higher, because
> every learner adds a test.

## Scene 11: Format and lint
visual: terminal
focus: 1-2 | 3-4 | all
notes:
- `ruff format` rewrites your files to the project's style
- `ruff check` looks for mistakes, like unused imports
- CI runs these same three commands: format, check, pytest
code:
```
(.venv) $ ruff format practice
10 files left unchanged
(.venv) $ ruff check practice
All checks passed!
```

> Step six. Two more commands. Ruff format rewrites your files to match the
> project's style. Spacing, quotes, blank lines.

> Ruff check looks for mistakes, like unused imports. You want to see, all
> checks passed.

> Here is why this matters. {CI|C I} runs exactly these three commands.
> Format, check, and {pytest|pie test}. If they pass on your computer, they
> will pass in {CI|C I}.

## Scene 12: Check what changed
visual: terminal
focus: 1 | 2-5
notes:
- Always look before you commit
- Only your two new files. Nothing else.
code:
```
(.venv) $ git status
On branch exercise-2
Untracked files:
        practice/greetings/ada_lovelace.py
        practice/tests/test_ada_lovelace.py
```

> Step seven. Commit. But first, look. Run git status.

> You should see only your two new files. If you also see the
> {.venv|dot venv} folder, your git ignore file is missing. Pull from
> upstream again.

## Scene 13: Commit
visual: terminal
focus: 1-2 | 3 | 4-5
notes:
- Add exactly your two files
- A clear message: what does this commit do?
- Two files changed. Your work is saved.
code:
```
(.venv) $ git add practice/greetings/ada_lovelace.py
(.venv) $ git add practice/tests/test_ada_lovelace.py
(.venv) $ git commit -m "Add exercise 2 greeting for ada-lovelace"
[exercise-2 1fbbb3a] Add exercise 2 greeting for ada-lovelace
 2 files changed, 11 insertions(+)
```

> Add your two files, and only those two. You can add them one at a time,
> like this, or both in one command.

> Then commit, with a clear message.

> Git answers, two files changed. Your work is saved on your branch.

## Scene 14: Push and open the pull request
visual: terminal
focus: 1 | 2 | 3
notes:
- `origin` is your fork. `-u` remembers it, so next time: `git push`
- Tell `gh` where your pull requests go. You do this once.
- `--fill` uses your commit message as the title
code:
```
(.venv) $ git push -u origin exercise-2
(.venv) $ gh repo set-default thejesh23/first-python-contribution
(.venv) $ gh pr create --fill
```

> Step eight. Push your branch to origin. That is your fork. Dash u
> remembers where this branch goes. Next time, a plain git push is enough.

> Step nine. The pull request. First, tell {gh|g h} which repo your pull
> requests go to. You only do this once.

> Then, {gh pr create --fill|g h, p r, create, dash dash fill}. It uses your
> commit message as the title, and prints the link to your new pull request.

## Scene 15: Watch CI
visual: terminal
focus: 1 | 2 | 3
notes:
- Watch the check run, live
- The check runs `ruff format --check`, `ruff check` and `pytest`
- Then the review bot comments, and a maintainer merges
code:
```
(.venv) $ gh pr checks --watch
✓  test
(.venv) $ gh pr view --comments
```

> Step ten. Watch {CI|C I}. Run {gh pr checks --watch|g h, p r, checks, dash
> dash watch}.

> One check runs. It is called test. It runs ruff format, ruff check and
> {pytest|pie test} on your code. The same three commands you just ran.

> After it passes, a review bot looks at your file names and your code. About
> a minute later, it leaves a comment. If everything passed, a maintainer
> reviews and merges your pull request. Read the comment with {gh pr view --comments|g h, p r, view,
> dash dash comments}.

## Scene 16: When a test fails
visual: terminal
focus: all | 2 | 4 | 3,5 | all
notes:
- Don't panic. Read it from the bottom up.
- `-` is what the test expected
- `+` is what your function returned
- `^` marks the difference
- Expected "Hello", got "Hi"
code:
```
>       assert greet("Sam") == "Hello, Sam! Welcome to open source."
E         - Hello, Sam! Welcome to open source.
E         ?  ^^^^
E         + Hi, Sam! Welcome to open source.
E         ?  ^
```

> One more thing. Some day, a test will fail. Don't panic. {pytest|Pie test}
> shows you exactly what went wrong. Read it from the bottom up.

> The minus line is what the test expected.

> The plus line is what your function returned.

> And the little arrows mark the difference.

> So here, the test expected Hello, but the function said Hi.

## Scene 17: The fix loop
visual: slide
layout: steps
title: Fix, push, and CI runs again
bullets:
- Fix the code, or the test
- Run pytest again
- Commit
- `git push`
- CI runs again

> What do you do about it? Fix the code. Or fix the test, if the test was
> wrong.

> Run {pytest|pie test} again.

> Commit.

> And git push.

> Your pull request updates by itself, and {CI|C I} runs again. This loop is
> a normal part of every contribution.

## Scene 18: Tidy up after the merge
visual: terminal
focus: 1 | 2 | 3
notes:
- Back to `main`
- Your merged work arrives in `main`
- The branch has done its job
code:
```
(.venv) $ git switch main
(.venv) $ git pull upstream main
(.venv) $ git branch -d exercise-2
```

> After the merge, tidy up. Switch back to the main branch.

> Pull from upstream. Main now includes your merged work.

> So the branch can go. Git branch, dash d, deletes it.

## Scene 19: Done
visual: slide
layout: steps
title: You just did the real thing
focus: all | all
bullets:
- Branch
- Test
- Code
- Format
- Lint
- Push
- Pull request
- CI
- Merge

> That is the real workflow. Branch, test, code, format, lint, push, pull
> request, {CI|C I}, merge. Real Python contributors do this every day.

> Next is lesson six. The house rules that every project expects you to
> read first.
