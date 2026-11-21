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

Target length: a 2–4 minute video (narration runs about 150 words a
minute), then the exercise. `tools/check_lessons.py` checks that each
lesson's stated length matches its script.
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
| 06 | [Setting up any Python project](lessons/06-set-up-any-project/): reading `pyproject.toml`, and the common setups (pip + venv, uv, Poetry, Hatch, tox, nox, pre-commit, Make). Plus docs builds (Sphinx, MkDocs). `tools/which_setup.py` detects them | Clone 2 real projects and get their test suites passing locally | Drafted |
| 07 | [Finding an issue](lessons/07-finding-an-issue/): `good first issue`, checking it's unclaimed, **searching for existing PRs first**, asking to be assigned. `tools/find_issues.py` lists fresh, unclaimed issues in welcoming Python projects | Shortlist 3 issues and comment on one | Drafted |
| 08 | [Making the change](lessons/08-making-the-change/): reproduce first, a failing test, the fix, docs, changelog/news fragments, commit messages. Docs-only PRs and good bug reports count too | Exercise 3 (local): fix a planted bug with a test; `tools/check_exercise_3.py` checks it | Drafted |
| 09 | [CI and review](lessons/09-ci-and-review/): reading red checks, "changes requested", applying suggestions, syncing with upstream, rebasing, merge conflicts, squashing on request | `tools/conflict_lab.py`: rebase, resolve a conflict, answer review, squash | Drafted |

## Part 4: Being a good contributor

| # | Lesson | Hands-on | Status |
|---|---|---|---|
| 10 | [Using AI tools well](lessons/10-using-ai-well/): where they help and hurt, verifying output, disclosure formats (`--trailer`), writing in your own words | Verify an AI explanation; rewrite an AI-style PR description | Drafted |
| 11 | [After the PR, and beyond GitHub](lessons/11-after-the-pr/): waiting, nudging once, rejection, stale bots, becoming a regular. GitLab, Codeberg, Gerrit and mailing-list patches | Write a nudge and a graceful close; test someone's PR | Drafted |

## Part 5: Capstone

| # | Lesson | Hands-on | Status |
|---|---|---|---|
| 12 | **[Your first external contribution](lessons/12-capstone/)**: a stage-by-stage checklist for a real PR | Get a PR merged in a real project you don't own, then add `graduates/YOUR-USERNAME.py`. The **Validate graduate** bot checks on GitHub that the PR is merged, yours, merged by a maintainer and in a real project, then you join the [graduates wall](graduates/) | Drafted |
| A | [Troubleshooting](lessons/A-troubleshooting/): login problems, pushing to the wrong repo, committed to `main`, push rejected, detached HEAD, fixing your last commit, fork out of date, pip and venv errors, PRs in the wrong place | A sandbox to break and fix each problem | Drafted |

## Principles

1. **A win in the first 15 minutes.** Lesson 01 needs no install, only a
   GitHub account.
2. **Teach what real Python projects actually check.** Later lessons are
   built around the checks a maintainer will run (pytest, ruff, pre-commit,
   news fragments), not toy steps.
3. **Commands are tested.** Every command that can run without your own
   account is run in CI (`tools/test_commands.py`), so the course can't go
   out of date without us noticing. The rest are marked and explained.
4. **Honest about AI.** The course is AI-generated and human-reviewed, and
   says so. Lessons 05 and 10 ask learners to be just as honest.
5. **Real projects, not just practice.** The sandbox teaches the moves.
   The capstone is only complete with a merged PR somewhere else.
