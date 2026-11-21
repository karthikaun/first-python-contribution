# Video script: CI and code review

Target length: about 8 minutes.

## Scene 1: Hook
visual: slide
title: Opening the PR isn't the end
bullets:
- A red CI check
- "This branch has conflicts"
- Review comments
- "Please squash"

> Opening the pull request isn't the end. Almost every pull request gets at
> least one of these: a red check, a merge conflict, review comments, or a
> request to squash your commits. None of them means you did something
> wrong. They're the normal back and forth of every pull request.

## Scene 2: Red CI
visual: terminal
code:
```
$ gh pr checks
X  tests (3.12)   https://github.com/...
✓  lint
$ gh run view --log-failed
```

> When CI goes red, run g h p r checks to see what failed, and g h run view
> dash dash log failed to see just the failing output. Read the last twenty
> lines first. That's where pytest or ruff tells you what went wrong. Fix it
> locally, commit, and push to the same branch. Your pull request updates
> itself.

## Scene 3: Not your fault
visual: slide
title: Sometimes it's not you
bullets:
- Fails on main too? Say so in a comment
- "Awaiting approval": a maintainer must approve first-time runs
- CLA or DCO check: see Lesson 05

> Sometimes it isn't your fault. If the same test fails on main too, say so
> in a comment. If the checks say awaiting approval, that's GitHub waiting
> for a maintainer to approve runs from first time contributors. Just wait.

## Scene 4: The lab
visual: terminal
code:
```
$ python3 tools/conflict_lab.py ../conflict-lab
$ cd ../conflict-lab/work
$ cat ../REVIEW.md
1. CI: This branch has conflicts that must be resolved.
2. Reviewer: Could you add a docstring to greeting()?
3. Reviewer (later): Please squash into one commit before we merge.
```

> To practise the rest safely, the course builds a little lab on your
> computer: a fake project, your fork, and your clone, with a pull request
> open. While it waited, a maintainer changed the same line you did. And
> your reviewer has three comments.

## Scene 5: Rebase and conflict
visual: terminal
code:
```
$ git fetch upstream
$ git rebase upstream/main
CONFLICT (content): Merge conflict in app.py
$ cat app.py
<<<<<<< HEAD
    return f"Hello, {name}"
=======
    return "Hello " + name + "!"
>>>>>>> (Add an exclamation mark to the greeting)
```

> Fetch upstream and rebase on its main. That replays your commit on top of
> the latest code. Git stops: conflict in app dot p y. The top half is what's
> on main now. The bottom half is yours.

## Scene 6: Resolve it
visual: terminal
code:
```
$ cat app.py
def greeting(name):
    return f"Hello, {name}!"
$ git add app.py
$ git rebase --continue
$ git push --force-with-lease
```

> Don't just pick a side. Keep what both changes meant: the maintainer's f
> string and comma, and your exclamation mark. Delete the markers, git add
> the file, and git rebase dash dash continue. You rewrote history, so push
> with dash dash force with lease. It refuses if anyone else pushed in the
> meantime. Never use plain force.

## Scene 7: Review comments
visual: slide
title: Handling review
bullets:
- Fix it in a new commit, push, reply with the commit
- Suggestions: click Commit suggestion
- Let the reviewer resolve their conversations
- Then click Re-request review

> Now the reviewer's comment. Make the change as a new commit and push
> normally, so the reviewer sees exactly what changed. Reply in one line,
> naming the commit. If they left a suggestion, you can apply it with one
> click. Let them resolve their own conversations, then click re-request
> review.

## Scene 8: Squash
visual: terminal
code:
```
$ git reset --soft upstream/main
$ git commit -m "Add an exclamation mark to the greeting"
$ git log --oneline
$ git push --force-with-lease
```

> Finally: please squash. Git reset dash dash soft upstream slash main
> undoes your commits but keeps all your changes staged. Commit once, with a
> message for the whole change, and force with lease again. Many projects
> squash for you when they merge, so only do this when you're asked.

## Scene 9: Done
visual: slide
title: You can handle any review
bullets:
- Red CI: read the last lines, fix, push
- Conflicts: rebase, resolve, force-with-lease
- Review: new commits, short replies, re-request
- Squash only when asked

> That's every part of review you'll meet. Red checks, conflicts, review
> comments, squashing. Next lesson, we talk about using AI tools well, when
> a project allows them.
