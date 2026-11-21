# Video script: Just enough git

Target length: about 7 minutes.

## Scene 1: Hook
visual: slide
title: Six ideas, and git stops being scary
bullets:
- Repository, commit, staging
- Branch, merge, remote
- Try them in a sandbox where nothing can break

> Git has hundreds of commands, but to contribute you need six ideas:
> repository, commit, staging, branch, merge and remote. We'll try every one
> in a throwaway sandbox folder, so nothing you do today can break anything.

## Scene 2: A repository
visual: terminal
code:
```
$ mkdir git-sandbox
$ cd git-sandbox
$ git init -b main
Initialized empty Git repository in /home/ada/git-sandbox/.git/
```

> Make a folder called git sandbox, go into it, and run git init dash b
> main. That creates a hidden folder called dot git. That hidden folder is
> the repository: your project's whole history lives in there. The dash b
> main part names the first branch main.

## Scene 3: Untracked, staged, committed
visual: terminal
code:
```
$ echo 'print("Hello")' > hello.py
$ git status
Untracked files:
	hello.py
$ git add hello.py
$ git status
Changes to be committed:
	new file:   hello.py
$ git commit -m "Add hello.py"
```

> Create a tiny Python file, then run git status, the command you'll use
> more than any other. Git sees hello dot p y but isn't saving it: it's
> untracked. Git add stages it, which means it'll go into the next commit.
> Git commit saves the snapshot, with a message saying what changed.

## Scene 4: Why staging exists
visual: slide
title: Why the extra git add step?
bullets:
- You often change several files at once
- Staging picks which changes go in this commit
- One commit, one idea

> Why the extra add step? Because you'll often change several files, but
> each commit should be about one idea. Staging lets you choose exactly what
> goes into this commit, and leave the rest for the next one.

## Scene 5: See what changed
visual: terminal
code:
```
$ echo 'print("Hello, open source!")' > hello.py
$ git diff
-print("Hello")
+print("Hello, open source!")
$ git commit -am "Greet open source"
```

> Change the file and run git diff. Lines starting with minus were removed,
> lines starting with plus were added. This is exactly what a maintainer
> sees when they review your pull request. Git commit dash a m stages every
> tracked file that changed, and commits, in one go.

## Scene 6: Branches
visual: terminal
code:
```
$ git switch -c shout
$ echo 'print("HELLO, OPEN SOURCE!")' > hello.py
$ git commit -am "Shout the greeting"
$ python3 hello.py
HELLO, OPEN SOURCE!
$ git switch main
$ python3 hello.py
Hello, open source!
```

> A branch lets you try something without touching main. Git switch dash c
> shout creates a branch called shout and moves you onto it. Change the file
> and commit. Now run it: it shouts. Switch back to main and run it again: it
> doesn't. Same file, different branch. Switching branches changes the files
> in your folder.

## Scene 7: Merge
visual: terminal
code:
```
$ git merge shout
Fast-forward
 hello.py | 2 +-
$ git log --oneline --graph --all
* 3c1d2e7 (HEAD -> main, shout) Shout the greeting
* 9b8a7f6 Greet open source
* 1a2b3c4 Add hello.py
```

> Happy with the shouting? Git merge shout brings it into main. Main hadn't
> changed, so git simply moves main forward. That's a fast forward. In real
> projects, you won't merge into main yourself. You open a pull request, and
> a maintainer merges it, like your first commit in lesson one.

## Scene 8: Remotes
visual: slide
title: Remotes: other copies of the repo
bullets:
- upstream: the original project, where you pull from
- origin: your fork on GitHub, where you push to
- git pull upstream main, git push origin my-branch
- A pull request asks upstream to take your branch

> Last idea: remotes. A remote is another copy of the repository, usually on
> GitHub. Your course clone has two. Upstream is the original project: you
> pull new commits from it. Origin is your fork: you push your branches to it.
> And a pull request asks upstream to take the commits from one of your
> branches.

## Scene 9: Done
visual: slide
title: You know just enough git
bullets:
- status, add, commit, diff
- switch -c, merge
- pull from upstream, push to origin
- Next: your second PR, from the terminal

> That's just enough git. Status, add, commit and diff for making changes.
> Switch and merge for branches. Pull from upstream and push to origin. Next
> lesson, you'll use all of them to open a real pull request with Python code
> and a test.
