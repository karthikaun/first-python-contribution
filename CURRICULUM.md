# Curriculum

**Goal:** someone who has never opened a pull request lands a real,
merged contribution to a Python project, and knows how to keep going.

Every lesson has the same four parts:

| File | What it is |
|---|---|
| `README.md` | The written lesson. Readable on its own, without the video. |
| `script.md` | The video script: scenes, on-screen visuals, narration. Rendered by `tools/render_video.py`. |
| `exercise.md` | The hands-on task. Most of them happen in this repo, starting with [`first-commits/`](first-commits/). |
| `quiz.md` | 3–5 questions with hidden answers. |

Target length: 5–8 minute video, 10–20 minutes including the exercise.
Each long video also gets one 60-second clip for Shorts/Reels.

## Part 1: Your first PR, today

| # | Lesson | Hands-on | Status |
|---|---|---|---|
| 00 | [What counts as a contribution](lessons/00-what-counts/) | Pick the kind of contribution you'll make first | Drafted |
| 01 | [Star, fork, and your first commit, in the browser](lessons/01-first-pr-in-browser/) | Add `first-commits/YOU.py` to this repo; the bot merges it | Drafted |

## Part 2: Real tools

| # | Lesson | Hands-on | Status |
|---|---|---|---|
| 02 | Set up your machine: git, `gh`, Python, a noreply email | Run `tools/doctor.py` until it's all green | Planned |
| 03 | Just enough git: commits, branches, remotes, as pictures | Local sandbox repo | Planned |
| 04 | Your second PR, from the terminal: a Python function and its test | Exercise 2 in this repo: pytest + ruff must pass in CI | Planned |

## Part 3: Real projects

| # | Lesson | Hands-on | Status |
|---|---|---|---|
| 05 | Reading a Python project: `pyproject.toml`, CONTRIBUTING, tests, tox/nox, pre-commit | Annotate a real repo | Planned |
| 06 | Finding an issue: `good first issue`, checking who's on it, **searching for existing PRs first** | Shortlist 3 issues | Planned |
| 07 | A quality change: virtualenv, run the tests, ruff, type hints, docstrings, news fragments | Exercise 3 in this repo | Planned |
| 08 | CI and review: reading red checks, replying, syncing your fork, merge conflicts | Bot-staged failing check + review comment | Planned |

## Part 4: Being a good contributor

| # | Lesson | Hands-on | Status |
|---|---|---|---|
| 09 | Using AI responsibly: project AI policies, disclosure, understanding every line, writing in your own words | Policy quiz on 3 real CONTRIBUTING files | Planned |
| 10 | After the PR: waiting, nudging once, what to do when you're ignored, becoming a regular | Pick your real issue | Planned |
| A | Troubleshooting: auth errors, committed to `main`, detached HEAD, wrong fork | Reference page | Planned |

## Principles

1. **A win in the first 15 minutes.** Lesson 01 needs no install, only a
   GitHub account.
2. **Teach what real Python projects actually check.** Later lessons are
   built around the checks a maintainer will run (pytest, ruff, pre-commit,
   news fragments), not toy steps.
3. **Every command is tested.** Commands in lessons are run in CI so the
   course can't go out of date without us noticing.
4. **Honest about AI.** The course is AI-generated and human-reviewed, and
   says so. Lesson 09 asks learners to be just as honest.
