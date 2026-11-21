# Video script: The five problems everyone hits

Target length: about 4 minutes.

## Scene 1: Hook
visual: slide
title: Don't delete the folder
bullets:
- Almost everything in git can be undone
- Read the message: it usually says what to do
- Five problems everyone hits, and their fixes

> Something went wrong, and you're about to delete the whole folder and
> start again. Don't. Almost everything in git can be undone, and the error
> message usually tells you what to do. Here are the five problems everyone
> hits, and how to fix each one.

## Scene 2: Can't switch branches
visual: terminal
code:
```
$ git switch experiment
error: Your local changes to the following files would be overwritten by checkout:
	app.py
$ git stash
$ git switch experiment
$ git switch main
$ git stash pop
```

> One. Git won't switch branches because you have unsaved changes. It's
> protecting your work. Either commit it, or stash it: git stash puts it
> aside, you switch, and git stash pop brings it back.

## Scene 3: Committed to main
visual: terminal
code:
```
$ git branch greet-world
$ git reset --hard origin/main
$ git switch greet-world
```

> Two. You committed on main by mistake. If you haven't pushed, make a
> branch right now: it keeps your commit. Then reset main back to where it
> was, and switch to your new branch. Only reset once your work is safe on
> the branch, because dash dash hard throws away uncommitted changes.

## Scene 4: Push rejected
visual: terminal
code:
```
 ! [rejected]        main -> main (fetch first)
$ git pull --rebase
$ git push

hint: ... behind its remote counterpart.
$ git push --force-with-lease
```

> Three. Your push was rejected. If it says fetch first, someone pushed to
> your branch, maybe a maintainer: pull with rebase, then push. If it says
> you're behind after you rebased or squashed, that's expected: push with
> force with lease.

## Scene 5: Detached HEAD
visual: terminal
code:
```
You are in 'detached HEAD' state.
$ git switch -c keep-my-work
$ git switch main
```

> Four. Detached head sounds scary, but it just means you're looking at a
> commit instead of a branch. Made commits you want to keep? Create a branch
> right there. Otherwise, switch back to main.

## Scene 6: Fix your last commit
visual: terminal
code:
```
$ git reset --soft HEAD~1
$ git restore --staged notes.txt
$ git commit -m "Greet open source"
```

> Five. Your last commit has the wrong files, or a vague message. Git reset
> dash dash soft undoes the commit but keeps the changes. Git restore dash
> dash staged takes a file back out. Then commit again. And to just fix the
> message, use git commit dash dash amend.

## Scene 7: Still stuck?
visual: slide
title: Still stuck?
bullets:
- The troubleshooting page has 12 fixes with the exact messages
- Practise them in its sandbox
- Ask with the exact command and the full output

> The troubleshooting page has twelve fixes, each with the exact message
> you'll see, and a sandbox to practise them safely. Still stuck? Open an
> issue with the exact command you ran and the full output. Someone will
> help.
