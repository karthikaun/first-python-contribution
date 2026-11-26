# Video script: What counts as a contribution

Target length: about 4 minutes.

## Scene 1: Start here
visual: slide
layout: title
title: You don't need to be an expert to contribute
bullets:
- You need one small, careful change.

> Maybe you think open source is for experts. People who write clever code
> all day. It isn't.

> To contribute, you need one small, careful change. In this video, you'll
> see what counts as a contribution. The list is longer than you think.

## Scene 2: Who is who
visual: slide
layout: cards
title: How open source works
bullets:
- Open source | The code is public. Anyone can read it, use it and suggest changes.
- Maintainers | A small group who decide what gets in.
- Contributors | Everyone else who helps. Soon, that's you.

> First, how does open source work? A project publishes its code. Anyone can
> read it, use it, and suggest changes.

> A small group of people decide what gets in. They are called maintainers.

> Everyone else who helps is a contributor. That is going to be you.

## Scene 3: The pull request
visual: slide
layout: steps
title: A pull request: "please pull my change in"
focus: 0 | 1 | 2 | 3 | 4 | all
bullets:
- You open a pull request
- A maintainer reviews it
- Maybe they ask for tweaks
- They merge it

> Most changes arrive as a pull request. P R for short. The name says what it
> is. Here is a change. Please pull it into your project.

> So, you open a pull request.

> A maintainer reviews it.

> Maybe they ask for a few tweaks. That is normal.

> And then they merge it. Your change is now part of the project.

> Almost every Python library you've used works this way. Requests. Pytest.
> Rich. Even the Python language itself.

## Scene 4: Contributions that count
visual: slide
layout: cards
title: All of these count
bullets:
- Fix the docs | A typo, a broken link, an example that no longer runs | No code
- Report a bug well | Exact steps, your Python version, the full error message | No code
- Reproduce a bug | "I can reproduce this on Python 3.13 on macOS" | No code
- Translate | Docs in your language | No code
- Add a missing test | For an edge case that nobody covered | A little code
- Fix a small bug | Usually labelled `good first issue` | Code

> Now the surprise. You do not need to write clever code. All of these are
> real contributions, and maintainers are glad to get them. Start with the
> docs. Fix a typo, a broken link, or an example that no longer runs.

> Report a bug well. That means the exact steps, your Python version, and the
> full error message.

> Or reproduce someone else's bug. Just say: I can reproduce this, on this
> Python version, on this system. That helps a lot.

> You can translate the docs into your language.

> So far, no code at all. Next, add a missing test, for an edge case that
> nobody covered. That needs a little code.

> And yes, you can fix a small bug. Look for the label, good first issue.

## Scene 5: Small teaches you everything
visual: slide
layout: steps
title: A one-line fix teaches the whole workflow
focus: 0 | 1-3 | 4-6 | all
bullets:
- Fork
- Branch
- Commit
- Pull request
- Review
- Merge

> Here is why small is fine. A one line docs fix that gets merged teaches you
> the same workflow as a big feature.

> Fork. Branch. Commit.

> Pull request. Review. Merge.

> Don't worry if these words are new. That workflow is what this course
> teaches, one step at a time.

## Scene 6: Why Python
visual: slide
title: Why Python is a good place to start
bullets:
- There's a lot of it: thousands of active projects label beginner-friendly issues
- The tools are shared: a virtualenv, `pytest`, `ruff`, `pre-commit`
- Python is readable, even in a codebase you've never seen

> Why start with Python? Three reasons. One. There is a lot of it. Thousands
> of active Python projects label issues that are friendly to beginners.

> Two. The tools are shared. Most projects use the same few things. A virtual
> environment. Pytest, for tests. A linter, like ruff. And pre-commit. Learn
> them once, and you can work on most Python projects.

> Three. Python is readable. You can often understand a function in an
> unfamiliar codebase just by reading it.

## Scene 7: Three myths
visual: slide
layout: cards
title: Three myths, and the truth
bullets:
- "I need to be an expert first" | Maintainers prefer small, careful changes from beginners over large, clever ones.
- "My change is too small to matter" | Small is the right size. Small PRs are easy to review, so they get merged.
- "Maintainers will be harsh" | Most are volunteers, happy to see new people. Review comments are about the code, not about you.

> Three myths might still be holding you back. Myth one. I need to be an
> expert first. No. Maintainers prefer small, careful changes from beginners
> over large, clever ones.

> Myth two. My change is too small to matter. Small is the right size. Small
> pull requests are easy to review, so they get merged.

> Myth three. Maintainers will be harsh. Most of them are volunteers, and
> they are happy to see new people. Review comments are about the code. They
> are not about you.

## Scene 8: By hand, on purpose
visual: slide
layout: cards
title: Why you type every command yourself
focus: 0 | 1 | 2 | 3 | 4 | all
bullets:
- You answer for it | Your name is on the pull request. You must be able to explain every line.
- You have to check it | Branches, commits and diffs show you what the agent really did.
- Things go wrong | A rejected push or a conflict only makes sense if you know the words.
- Open source is people | Choosing an issue, asking first, answering review. Maintainers want to hear from you.

> One more thing. In this course, you type every command yourself, in the
> terminal. No {AI|A I} agent does it for you. That is on purpose, even
> though tools like {Claude Code|Clawd Code} and Codex can open a pull
> request in minutes. Four reasons.

> One. You answer for it. Your name is on the pull request, so you must be
> able to explain every line.

> Two. You have to check it. Branches, commits and diffs show you what the
> agent really did.

> Three. Things go wrong. A rejected push, or a conflict, only makes sense
> if you know the words.

> Four. Open source is people. Choosing an issue, asking first, answering
> review. Maintainers want to hear from you.

> The steps are small, and you learn them once. After that, an agent is a
> faster pair of hands, and you still know what is going on.

## Scene 9: The road ahead
visual: slide
layout: cards
title: Where this course goes
bullets:
- Part 1 | Your first PR today, in the browser. No install.
- Part 2 | Real tools: git, GitHub CLI, virtualenvs, pytest, ruff.
- Part 3 | A real Python project: finding an issue, passing CI, handling review.
- Part 4 | Being a good contributor, including using AI tools honestly.

> Here is where the course goes. Part one. You open your first pull request
> today, in the browser, with nothing to install.

> Part two. You set up the real tools. Git, the GitHub command line,
> virtual environments, pytest and ruff.

> Part three. A real Python project. You find an issue, pass the automated
> checks, and handle review.

> Part four. Being a good contributor. That includes using A I tools honestly.

## Scene 10: Your task
visual: slide
title: Before the next lesson
bullets:
- Create a free GitHub account, with a username you'd show an employer
- Turn on two-factor authentication
- Write down the contribution you'd like to make first

> Before the next lesson, three small things. Create a free GitHub account, if
> you don't have one. Pick a username you'd be happy to show an employer. It
> appears on every contribution you make.

> Turn on two factor authentication. Many projects require it.

> And look at the list of contributions again. Write down the one you'd like
> to make first. Then open lesson two. Your first pull request is waiting.
