# Lesson 00: What counts as a contribution

**Time:** 3 minute video · 5 minute exercise
**You'll need:** nothing yet

## Open source in one paragraph

Open source projects publish their code so anyone can read it, use it and
suggest changes. A small group of **maintainers** decide what gets in.
Everyone else who helps is a **contributor**. Most changes arrive as a
**pull request** (PR): "here is a change, please pull it into your project."
A maintainer reviews it, maybe asks for tweaks, and merges it.

Almost every Python library you've used works this way: `requests`,
`pytest`, `rich`, even the Python language itself (CPython).

## Contributions that count

You do not need to write clever code to contribute. All of these are real
contributions that maintainers are glad to get:

| Contribution | Example | Needs code? |
|---|---|---|
| Fix the docs | A typo, a broken link, an example that no longer runs | No |
| Report a bug well | Exact steps, Python version, the full error message | No |
| Reproduce someone else's bug | "I can reproduce this on Python 3.13 on macOS" | No |
| Add a missing test | A test for an edge case that nobody covered | A little |
| Fix a small bug | Usually labelled `good first issue` | Yes |
| Translate | Docs in your language | No |

A one-line docs fix that gets merged teaches you the same workflow as a big
feature: fork, branch, commit, pull request, review, merge. That workflow is
what this course teaches.

## Why Python is a good place to start

- **There's a lot of it.** Thousands of active Python projects label
  beginner-friendly issues.
- **The tools are shared.** Most projects use the same few things: a
  virtualenv, `pytest` for tests, a linter like `ruff`, and `pre-commit`.
  Learn them once and you can work on most Python projects.
- **Python is readable.** You can often understand a function in an
  unfamiliar codebase just by reading it.

## Three myths

1. **"I need to be an expert first."** Maintainers prefer small, careful
   changes from beginners over large, clever ones.
2. **"My change is too small to matter."** Small is the right size. Small
   PRs are easy to review, so they get merged.
3. **"Maintainers will be harsh."** Most are volunteers who are happy to see
   new people. Review comments are about the code, not about you.

## Where this course goes

1. **Part 1:** your first PR today, in the browser, no install.
2. **Part 2:** real tools: git, GitHub CLI, virtualenvs, pytest, ruff.
3. **Part 3:** a real Python project: finding an issue, passing CI,
   handling review.
4. **Part 4:** being a good contributor, including using AI tools honestly.

Next: [Lesson 01: your first PR, entirely in the browser](../01-first-pr-in-browser/).
