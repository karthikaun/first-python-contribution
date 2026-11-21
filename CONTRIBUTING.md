# Contributing

Thanks for helping! There are two kinds of contribution here.

## 1. Learners: the exercises

- **Lesson 02:** add `first-commits/YOUR-USERNAME.py`. See
  [the lesson](lessons/02-first-pr-in-browser/).
- **Lesson 05:** add `practice/greetings/YOUR_NAME.py` and its test. See
  [the lesson](lessons/05-second-pr-from-terminal/).

Bots check and merge these PRs. Change only your own files.

## 2. Improving the course

Found a mistake, a broken link, or a command that doesn't work? Please
[open an issue](https://github.com/thejesh23/first-python-contribution/issues/new)
first, so we can agree on the fix. Then open a PR that links to it
(`Fixes #123`).

**Setup and checks:**

```bash norun
uv run ruff format .
uv run ruff check .
uv run python tools/check_lessons.py
uv run pytest
uv run python tools/test_commands.py
```

**Lesson format:** each lesson is a folder `lessons/NN-slug/` with
`README.md`, `script.md`, `exercise.md` and `quiz.md`. `tools/check_lessons.py`
checks the structure. Shell commands in ```` ```bash ```` blocks are run in
CI; mark ones that need a real account with ```` ```bash norun ````.

**Legal:** no CLA and no sign-off needed. By contributing you agree your
contribution is shared under this repo's licenses (MIT for code, CC BY 4.0
for lesson text and videos).

**AI policy:** this course is drafted with AI and reviewed by a human, and
we hold contributions to the same standard:

- AI-assisted changes are welcome if **you have read, run and understood
  every line**.
- Say so in your PR description (one sentence is enough, e.g.
  "Drafted with Claude, reviewed and tested by me").
- **Write issue comments, PR descriptions and review replies yourself.**
- Facts in lessons (versions, commands, policies) must be checked against
  the original source, with a link in the PR.

**Code of conduct:** be kind and patient. Everyone here is learning,
including the maintainer. If someone isn't, tell the maintainer
(thejesh23) in an issue. You don't need to include details there; just ask
for a private way to talk.
