# Lesson 01: What counts as a contribution

**Time:** 5 minute video · 5 minute exercise
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

## Why this course does everything by hand

In this course you type every command yourself, in a terminal. No AI agent
does a step for you. That's on purpose, even though tools like Claude Code
and Codex can fork a repo, write a change and open a pull request in
minutes. Four reasons:

1. **You answer for it, not the tool.** Your name is on the pull request.
   Projects hold the person who opened it responsible for every line, and
   many say so in an AI policy (Lesson 06). When a reviewer asks "why this
   change?", you have to answer.
2. **You can't check what you can't read.** What an agent produces is a
   branch, some commits and a diff. Knowing what those are is how you see
   what it really did, and how you notice that it changed a test instead of
   the code, or touched files nobody asked about.
3. **Things go wrong, and then it's you and git.** A rejected push, a
   conflict, a branch started from the wrong place: you need to know what
   the words mean to fix it, or even to tell the agent what to fix.
4. **Open source is people.** Choosing an issue nobody else is working on,
   asking before you start, answering review, waiting politely: no tool does
   that for you. Maintainers want to hear from you, in your own words
   (Lesson 13).

The steps are small and you learn them once: this course takes about a day.
So do the exercises by hand, even if you have an agent open in another
window. After that, an agent is a faster pair of hands, and you are still
the one who knows what is going on. Lesson 13 is about using these tools
well.

## Where this course goes

1. **Part 1:** your first PR today, in the browser, no install.
2. **Part 2:** real tools: git, GitHub CLI, virtualenvs, pytest, ruff.
3. **Part 3:** a real Python project: finding an issue, passing CI,
   handling review.
4. **Part 4:** being a good contributor, including using AI tools honestly.

Next: [Lesson 02: your first PR, entirely in the browser](../02-first-pr-in-browser/).
