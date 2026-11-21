# Video script: CI and code review

Target length: about 4 minutes.

## Scene 1: Start here
visual: slide
layout: title
title: Opening the PR isn't the end
bullets:
- What comes next is normal. None of it means you did something wrong.

> Opening the pull request isn't the end. Almost every pull request gets
> some back and forth.

> None of it means you did something wrong. It is the normal back and forth
> of every pull request.

## Scene 2: Four things
visual: slide
layout: cards
title: Almost every PR gets at least one of these
bullets:
- A red CI check | Something failed in the automated checks.
- Conflicts | "This branch has conflicts that must be resolved."
- Review comments | A reviewer asks for changes.
- A squash request | "Please squash into one commit."

> There are four things. A red {CI|C I} check.

> A message saying, this branch has conflicts that must be resolved.

> Review comments, asking for changes.

> And a request to squash your commits. This lesson covers all four.

## Scene 3: Red CI
visual: terminal
focus: 1 | 2 | all
notes:
- See which checks failed
- Print just the failing steps' output. Read the last 20 lines first.
- Push the fix to the same branch. Never open a new PR for it.
code:
```
$ gh pr checks
$ gh run view --log-failed
```

> When {CI|C I} is red, run {gh pr checks|g h, p r, checks}, to see what
> failed.

> Then {gh run view --log-failed|g h, run, view, dash dash log failed}. It
> prints just the failing steps' output. Read the last twenty lines first.
> That is where {pytest|pie test}, and ruff, say what went wrong.

> Fix it, and push to the same branch. Your pull request updates by itself.
> Never open a new pull request for the same change.

## Scene 4: What failed
visual: slide
layout: cards
title: What failed, and what to do
bullets:
- Lint or format | A style issue. Run the project's formatter and linter locally, commit, push.
- Fails on `main` too | A flaky or already-broken test, not you. Say so in a comment.
- "Waiting for approval" | First-time contributors' workflows need a maintainer's approval. Just wait.

> What failed? If it is lint or format, it is a style issue. Run the
> project's formatter and linter locally, commit, and push.

> If the same test fails on main too, or passes on a re-run, it is not you.
> Say so in a comment.

> And if it says, waiting for approval, do nothing. GitHub doesn't run first
> time contributors' workflows until a maintainer approves.

## Scene 5: The lab
visual: terminal
focus: 1-2 | 3-4 | 6 | 7 | 8
notes:
- A practice world on your computer: a fake project, a fake fork, your clone
- Your pull request is "open", and it has review comments
- While your PR waited, a maintainer changed the same line on `main`
- The reviewer wants a docstring
- And later, one tidy commit
code:
```
$ python3 tools/conflict_lab.py ../conflict-lab
$ cd ../conflict-lab/work
$ cat ../REVIEW.md
# Review comments on your pull request

1. **CI:** This branch has conflicts that must be resolved.
2. **Reviewer:** Could you add a docstring to `greeting()`?
3. **Reviewer (later):** Looks good! Please squash into one commit before we merge.
```

> You'll practise the rest in a safe lab on your computer. One command
> builds a fake project, a fake fork, and your clone, with a pull request
> open.

> Read the review comments.

> One. This branch has conflicts. While your pull request waited, a
> maintainer changed the same line on main.

> Two. The reviewer asks for a docstring.

> Three. Later, the reviewer asks you to squash into one commit. Let's
> handle all three.

## Scene 6: Rebase
visual: terminal
focus: 1-2 | 3-4
notes:
- Replay your commit on top of the latest `main`
- Git stops, and tells you where the conflict is
code:
```
$ git fetch upstream
$ git rebase upstream/main
CONFLICT (content): Merge conflict in app.py
error: could not apply 5cf76f3... Add an exclamation mark to the greeting
```

> First, the conflict. Fetch upstream, and rebase on its main. That replays
> your commit on top of the latest main.

> Git stops, and tells you. Merge conflict, in app {.py|dot p y}.

## Scene 7: Read the conflict
visual: code
lang: text
file: app.py
focus: 2-3 | 4-6 | all
notes:
- Between `<<<<<<<` and `=======`: what's on `main` now
- Between `=======` and `>>>>>>>`: your commit
- Don't just pick one side. Keep what both changes meant.
code:
```
def greeting(name):
<<<<<<< HEAD
    return f"Hello, {name}"
=======
    return "Hello " + name + "!"
>>>>>>> 5cf76f3 (Add an exclamation mark to the greeting)
```

> Open the file. Git has marked the conflict. The top part is what's on main
> now. The maintainer's change.

> The bottom part is your commit.

> Don't just pick one side. Keep what both changes meant. The maintainer's f
> string and comma. And your exclamation mark.

## Scene 8: Resolve it
visual: code
file: app.py
notes:
- No markers left. The f-string, the comma, and your `!`.
code:
```
def greeting(name):
    return f"Hello, {name}!"
```

> Edit the file so it reads exactly this, with no markers left.

## Scene 9: Continue and push
visual: terminal
focus: 1-2 | 3-4 | 5
notes:
- Check that it works
- Stage the file, then continue the rebase
- You rewrote history. Never use plain `--force`.
code:
```
$ python3 -c "from app import greeting; print(greeting('Ada'))"
Hello, Ada!
$ git add app.py
$ git rebase --continue
$ git push --force-with-lease
```

> Check that it works. Hello, Ada, with the comma and the exclamation mark.

> Then git add the file, and git rebase, dash dash continue. Your commit now
> sits on top of the maintainer's.

> Now update your pull request. You rewrote your branch's history, so a
> plain git push is refused. Use dash dash force with lease. It replaces the
> branch, but only if nobody else pushed to it. Never use plain force. And
> if a rebase goes wrong, git rebase, dash dash abort, puts everything back.

## Scene 10: Review comments
visual: terminal
focus: 1 | 2
notes:
- Make the change as a new commit
- Push normally. Then reply in one line, naming the commit.
code:
```
$ git commit -am "Add a docstring to greeting"
$ git push
```

> Next, the review comment. The reviewer asked for a docstring. Add it, and
> make the change as a new commit.

> Then push normally. New commits let reviewers see exactly what changed
> since they last looked. Then reply on the comment with one short line,
> naming the commit.

## Scene 11: Review etiquette
visual: slide
title: Review etiquette
bullets:
- New commits while review is going on
- Don't resolve the reviewer's conversations yourself
- Disagreeing is fine: explain once, politely
- Don't know how? Say so, and ask
- Changes requested? Fix, push, then **Re-request review**

> Some review etiquette. Push new commits while review is going on. Don't
> force push in the middle of a review, unless asked.

> Don't resolve the reviewer's conversations yourself. Let them do it, once
> they're happy.

> Disagreeing is fine. Explain your reasoning once, politely. Then go with
> the maintainer's decision. It's their project.

> Don't know how to do what they asked? Say so, and ask. That's normal.

> And if they requested changes, fix what's asked, push, and click
> Re-request review.

## Scene 12: Squash
visual: terminal
focus: 1 | 2 | 3-4
notes:
- Undo your commits, but keep all your changes staged
- One commit, with a message for the whole change
- Only squash when asked. Many projects squash for you when they merge.
code:
```
$ git reset --soft upstream/main
$ git commit -m "Add an exclamation mark to the greeting"
$ git log --oneline
$ git push --force-with-lease
```

> Finally, the squash. Git reset, dash dash soft, upstream slash main. It
> undoes your commits, but keeps all your changes staged.

> So the next commit contains everything. Write a message that describes
> the whole change.

> Check the log, and push with force with lease again. Many projects squash
> for you when they merge. Only do it yourself when asked.

## Scene 13: Done
visual: slide
title: You can handle any review
bullets:
- Red CI: read the last lines, fix, push to the same branch
- Conflicts: rebase, keep both meanings, `--force-with-lease`
- Review: new commits, short replies
- Squash: only when asked

> That's it. Red {CI|C I}. Read the last lines, fix, and push to the same
> branch.

> Conflicts. Rebase, keep both meanings, and force with lease.

> Review. New commits, and short replies.

> Squash. Only when asked. Next lesson, using {AI|A I} tools well.
