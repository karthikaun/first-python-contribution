# Video script: The five problems everyone hits

Target length: about 2 minutes.

## Scene 1: Start here
visual: slide
layout: title
title: Don't delete the folder
bullets:
- Nearly everything in git can be undone.

> Something went wrong. And you are about to delete your folder and start
> again. Don't.

> Nearly everything in git can be undone. Here are five problems everyone
> hits, and the fix for each one.

## Scene 2: Five problems
visual: slide
layout: steps
title: Five problems everyone hits
focus: all
bullets:
- Can't switch branches
- Committed to `main`
- Push rejected
- Detached HEAD
- Wrong last commit

> You can't switch branches. You committed to main by mistake. Your push was
> rejected. You are in a detached head state. Or your last commit is wrong.
> Let's fix them, one by one.

## Scene 3: Can't switch branches
visual: terminal
focus: 1-5 | 6 | 7-8 | 9
notes:
- You have unsaved work. Git stopped to protect it.
- Stash it: put it aside
- Now you can switch, and switch back
- Bring your work back
code:
```
$ git switch experiment
error: Your local changes to the following files would be overwritten by checkout:
	app.py
Please commit your changes or stash them before you switch branches.
Aborting
$ git stash
$ git switch experiment
$ git switch main
$ git stash pop
```

> One. Git won't switch branches. You have unsaved work, and switching would
> overwrite it. Git stopped to protect it. The message says what to do.
> Commit your changes, or stash them.

> Git stash puts your work aside.

> Now you can switch, and switch back.

> And git stash pop brings your work back.

## Scene 4: Committed to main
visual: terminal
focus: 1 | 2 | 3
notes:
- Make the branch now. It keeps your commit.
- Put `main` back. `--hard` throws away uncommitted changes.
- Carry on, on your branch
code:
```
$ git branch greet-world
$ git reset --hard origin/main
$ git switch greet-world
```

> Two. You committed on main by mistake. As long as you haven't pushed, it's
> easy. Make the branch now. It keeps your commit.

> Then put main back where it was. Be careful. Dash dash hard throws away
> uncommitted changes. So only run it once your work is safely on the new
> branch.

> Then switch to your branch, and carry on.

## Scene 5: Push rejected, fetch first
visual: terminal
focus: 1-4 | 5 | 6
notes:
- GitHub has commits on your branch that you don't have
- Bring their commits in, under yours
- Then push
code:
```
$ git push
 ! [rejected]        main -> main (fetch first)
hint: Updates were rejected because the remote contains work that you do not
hint: have locally.
$ git pull --rebase
$ git push
```

> Three. Your push was rejected. If it says fetch first, GitHub has commits
> on your branch that you don't have. Maybe a maintainer pushed a fix.

> Bring their commits in under yours, with git pull, dash dash rebase.

> Then push.

## Scene 6: Push rejected, behind
visual: terminal
focus: 1-3 | 4
notes:
- After a rebase, amend or squash, this is expected
- You rewrote commits you had already pushed
code:
```
$ git push
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart.
$ git push --force-with-lease
```

> If it says your branch is behind, after you rebased, amended or squashed,
> that is expected. You rewrote commits you had already pushed.

> So push with dash dash force with lease.

## Scene 7: Detached HEAD
visual: terminal
focus: 1-2 | 3 | 4
notes:
- You checked out a commit instead of a branch. Nothing is broken.
- Made commits you want to keep? Create a branch right where you are.
- Otherwise, just switch back
code:
```
You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, ...
$ git switch -c keep-my-work
$ git switch main
```

> Four. Detached head. It sounds scary. But you just checked out a commit,
> instead of a branch. Nothing is broken.

> Did you make commits you want to keep? Create a branch right where you
> are, before switching away.

> Otherwise, just switch back to main.

## Scene 8: Fix your last commit
visual: terminal
focus: 1 | 2 | 3
notes:
- Undo the last commit, but keep its changes staged
- Take a file out of the next commit. Your edits stay.
- Commit again, with a better message
code:
```
$ git reset --soft HEAD~1
$ git restore --staged notes.txt
$ git commit -q -m "Greet open source"
```

> Five. Your last commit has the wrong files, or a vague message. Git reset,
> dash dash soft, undoes the last commit, but keeps its changes staged.

> Git restore, dash dash staged, takes a file out of the next commit. Your
> edits stay.

> Then commit again, with a better message. To change only the message, use
> git commit, dash dash amend.

## Scene 9: Still stuck?
visual: slide
title: Still stuck?
bullets:
- The troubleshooting page has 12 fixes, with the exact messages
- Its sandbox lets you practise them safely
- Or open an issue, with the exact command and the full output

> The troubleshooting page has twelve fixes, each with the exact message
> you'll see.

> It comes with a sandbox, so you can practise the fixes safely.

> Still stuck? Open an issue, with the exact command you ran, and the full
> output. Remove anything you don't want public first.
