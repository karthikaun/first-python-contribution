# Curriculum

**Goal:** someone who has never opened a pull request finishes able to
contribute to **any** open source project, not just this course's practice
repo. The course ends with a real, merged pull request in a project the
learner chose themselves (Lesson 12).

## What you can do when you finish

Every item is taught in a lesson and practised in an exercise:

- [ ] Fork, clone, branch, commit, push and open a PR, in the browser or the terminal (01–04)
- [ ] Keep your fork and branch up to date with upstream (02, 09)
- [ ] Read a project's house rules: CONTRIBUTING, CLA or DCO, AI policy, code of conduct (05)
- [ ] Set up an unfamiliar Python project and run its tests and linters, whatever tools it uses: pip, uv, Poetry, Hatch, tox, nox, pre-commit, Make (06)
- [ ] Find an issue that's open, unclaimed and has no existing PR, and claim it properly (07)
- [ ] Make a change the way the project wants: tests, docs, style, changelog entry, commit message (08)
- [ ] Fix a failing CI check, respond to review, apply suggestions, rebase, resolve conflicts, squash on request (09)
- [ ] Use AI tools within a project's policy, and write your own words (05, 10)
- [ ] Handle silence, rejection and "won't fix" gracefully, and know what's different off GitHub (11)
- [ ] Land a merged PR in an external project (12)

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
| 02 | [Set up your machine: git, `gh`, Python, a private email](lessons/02-set-up-your-machine/) | Run `tools/doctor.py` until it's all green | Drafted |
| 03 | [Just enough git: commits, branches, merges, remotes](lessons/03-just-enough-git/) | A local sandbox repo | Drafted |
| 04 | [Your second PR, from the terminal: a Python function and its test](lessons/04-second-pr-from-terminal/) | Exercise 2 in `practice/`: pytest + ruff must pass in CI | Drafted |

## Part 3: Real projects

| # | Lesson | Hands-on | Status |
|---|---|---|---|
| 05 | [House rules: CONTRIBUTING, CLAs, DCO sign-offs, AI policies, code of conduct](lessons/05-house-rules/) | Fill the pre-flight checklist for 3 projects | Drafted |
| 06 | Setting up any Python project: reading `pyproject.toml`, and the common setups (pip + venv, uv, Poetry, Hatch, tox, nox, pre-commit, Make). Plus docs builds (Sphinx, MkDocs) | Clone 2 real projects and get their test suites passing locally | Planned |
| 07 | Finding an issue: `good first issue`, checking it's unclaimed, **searching for existing PRs first**, asking to be assigned. `tools/find_issues.py` lists fresh, unclaimed issues in welcoming Python projects | Shortlist 3 issues and comment on one | Planned |
| 08 | Making the change: reproduce first, a failing test, the fix, docs, changelog/news fragments, commit messages. Docs-only PRs and good bug reports count too | Exercise 3 in this repo: fix a planted bug with a test | Planned |
| 09 | CI and review: reading red checks, "changes requested", applying suggestions, syncing with upstream, rebasing, merge conflicts, squashing on request | Bot-staged review in this repo: a failing check, a review comment, a conflict | Planned |

## Part 4: Being a good contributor

| # | Lesson | Hands-on | Status |
|---|---|---|---|
| 10 | Using AI tools well: where they help, verifying output, disclosure formats, writing in your own words | Rewrite an AI-drafted PR description in your own words | Planned |
| 11 | After the PR, and beyond GitHub: waiting, nudging once, rejection, "won't fix", becoming a regular. What's different on GitLab, Codeberg, Gerrit and mailing-list projects | Write a polite follow-up and a graceful close | Planned |

## Part 5: Capstone

| # | Lesson | Hands-on | Status |
|---|---|---|---|
| 12 | **Your first external contribution**: a start-to-finish walkthrough of a real PR, with a checklist for each stage | Get a PR merged in a real project you don't own, then add `graduates/YOUR-USERNAME.py` with its link. A bot checks on GitHub that the PR is merged and is yours, then adds you to the graduates wall | Planned |
| A | Troubleshooting: auth errors, committed to `main`, detached HEAD, wrong fork, push rejected, "this branch has conflicts" | Reference page | Planned |

## Principles

1. **A win in the first 15 minutes.** Lesson 01 needs no install, only a
   GitHub account.
2. **Teach what real Python projects actually check.** Later lessons are
   built around the checks a maintainer will run (pytest, ruff, pre-commit,
   news fragments), not toy steps.
3. **Every command is tested.** Commands in lessons are run in CI so the
   course can't go out of date without us noticing.
4. **Honest about AI.** The course is AI-generated and human-reviewed, and
   says so. Lessons 05 and 10 ask learners to be just as honest.
5. **Real projects, not just practice.** The sandbox teaches the moves.
   The capstone is only complete with a merged PR somewhere else.
