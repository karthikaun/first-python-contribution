# Video script: Opening the pull request

Target length: about 3 minutes.

## Scene 1: Start here
visual: slide
layout: title
title: Opening the pull request
bullets:
- The title and description are your pitch to the reviewer.

> Your change is ready. Now you hand it to a reviewer, who has many other
> pull requests waiting.

> The title and the description decide how fast yours gets looked at, and
> how many questions come back.

## Scene 2: Before you open it
visual: slide
layout: steps
title: Before you open it
bullets:
- One change per PR
- Read your own diff
- Run what CI runs

> Before you open it, three checks. One change per pull request. A fix and a
> refactor are two pull requests. Small ones get reviewed first.

> Read your own diff once, as if you were the reviewer. Remove stray print
> calls, and changes to lines you didn't mean to touch.

> And run what {CI|C I} runs. The tests and the linters.

## Scene 3: The title
visual: slide
layout: cards
title: The title: say what the PR does
bullets:
- `Fix bug` | Which bug?
- `Update textkit.py` | Names a file, not a change
- `Fix slugify for repeated spaces and punctuation` | Says what it does

> The title is what maintainers see, in a list of a hundred pull requests.
> Fix bug. Which bug?

> Update text kit. That names a file, not a change.

> Fix slugify for repeated spaces and punctuation. That says what it does.
> Write it like a commit subject. Fix, not fixed. Short, and no full stop.

## Scene 4: Title formats
visual: slide
title: Some projects want a format
bullets:
- CPython: `gh-12345: Fix ...`
- Conventional Commits: `fix: ...`
- CONTRIBUTING says which

> Some projects want a format. {CPython|C Python} puts the issue number
> first.

> Others start with a word like fix, and a colon.

> The contributing file says which. And when a project squashes your
> commits, the title often becomes the commit message in its history.

## Scene 5: Four things
visual: slide
layout: cards
title: The description: four things
bullets:
- The issue | `Fixes #1234` closes it on merge
- What and why | Two or three sentences
- How you tested | Tests added, commands run
- Anything else | A choice you weren't sure about

> The description needs four things. The issue it fixes. Write fixes, hash,
> and the number, and GitHub closes the issue when your pull request is
> merged.

> What changed, and why, in two or three sentences. The diff shows how. It
> can't show why.

> How you tested it. The tests you added, and the commands you ran.

> And anything else the reviewer should know. A choice you weren't sure
> about, or something you left out on purpose.

## Scene 6: A whole description
visual: code
lang: text
file: pr-description.md
focus: 1 | 3 | 5-7 | 9-10
notes:
- The title, on the first line
- The issue it fixes
- What changed, and why
- How it was tested
code:
```
Fix slugify for repeated spaces and punctuation

Fixes #1234

`slugify` kept punctuation and produced doubled hyphens for repeated
spaces. It now turns every run of non-alphanumeric characters into a
single hyphen and strips hyphens from the ends.

Tested: added a parametrized regression test with the cases from the
issue; the full test suite and ruff pass locally.
```

> Here is a whole one. The title.

> The issue.

> What changed and why, in two sentences.

> And how it was tested. That's all. Under sixty words. Short is good. Long
> descriptions, with headings and bullet lists, are what maintainers have
> learned to skip.

## Scene 7: A real one
visual: browser
url: https://github.com/python/cpython/pull/162029
caption: A real description, merged into Python: what changed, how it was tested, the issue
image: captures/real-pr.png
height: 1100
crop: 100,170,1240,460

> Here is a real one, merged into Python itself. One sentence says what
> changed. Two lines say how it was tested. And the last line links the
> issue.

## Scene 8: Templates and drafts
visual: slide
title: Templates and drafts
bullets:
- A template? Fill in every section, tick only what's true
- Not finished? Open a **draft**
- Done? Click **Ready for review**

> If the project has a template, GitHub puts it in the box for you. Fill in
> every section, and tick only the boxes that are true.

> Not finished, but you want {CI|C I} to run? Open a draft. A draft can't be
> merged, and reviewers aren't asked to look yet.

> When it's done, click ready for review.

## Scene 9: Practise
visual: terminal
focus: 1 | 2-5 | 7
notes:
- Write your title and description in a file, then check it
- It checks what a reviewer looks for
- Don't open this one. The next learner needs the bug.
code:
```
$ python tools/check_pr_description.py pr-description.md
✔ Title says what the PR does: "Fix slugify for repeated spaces and punctuation"
✔ Issue is linked, and will close when the PR is merged.
✔ What and why are explained.
✔ Testing is described.

Ready to open. Nice description!
```

> Now your turn. Write the title and description for your slugify fix, in a
> file. Then run the checker.

> It checks what a reviewer looks for. The title, the issue, what and why,
> and how you tested.

> Don't open this pull request. The next learner needs the bug.

## Scene 10: Done
visual: slide
title: A pull request that's easy to review
bullets:
- A title that says what it does
- The issue, what and why, how you tested
- Short, and in your own words

> That's a pull request that's easy to review. A title that says what it
> does.

> The issue, what and why, and how you tested. Short, and in your own
> words. Next lesson, {CI|C I} and code review.
