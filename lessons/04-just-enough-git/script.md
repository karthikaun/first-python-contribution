# Video script: Just enough git

Target length: about 3 minutes.

## Scene 1: Start here
visual: slide
layout: title
title: Six ideas, and git stops being scary
bullets:
- Try each one in a sandbox, where nothing can go wrong.

> Git has a lot of commands. But you don't need to know all of git to
> contribute. You need six ideas.

> We'll try each one in a throwaway sandbox folder. So nothing can go wrong.

## Scene 2: Six ideas
visual: slide
layout: cards
title: The six ideas
bullets:
- Repository | A project folder plus its whole history.
- Commit | A snapshot of your files, with a message.
- Staging | `git add` picks what goes into the next commit.
- Branch | A name that points at a commit.
- Merge | Bringing one branch's commits into another.
- Remote | Another copy of the repository, usually on GitHub.

> Here they are. A repository is a project folder, plus its whole history.

> A commit is a snapshot of your files, with a message.

> Staging picks which changes go into the next commit.

> A branch is a name that points at a commit.

> A merge brings one branch's commits into another.

> And a remote is another copy of the repository, usually on GitHub. Now
> let's try them.

## Scene 3: A repository
visual: terminal
focus: 1-2 | 3-4
notes:
- Make the sandbox outside the course repo
- The hidden `.git` folder is the repository. `-b main` names the first branch.
code:
```
$ mkdir git-sandbox
$ cd git-sandbox
$ git init -b main
Initialized empty Git repository in /home/ada/git-sandbox/.git/
```

> Make a folder called git sandbox, anywhere outside the course repo. And go
> into it.

> Now run git init, dash b main. It creates a hidden folder, called dot git.
> That folder is the repository. Your whole history lives in there. And dash
> b main names the first branch, main.

## Scene 4: Untracked, staged, committed
visual: terminal
focus: 1 | 2-4 | 5-8 | 9
notes:
- Create a tiny Python file
- Untracked: git sees the file, but isn't saving it
- Staged: it will go into the next commit
- Committed: the change is saved in history
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

> Create a tiny Python file.

> Then run git status. It is the command you'll run most. It tells you where
> you are, and what has changed. Right now, hello {.py|dot p y} is
> untracked. Git sees it, but isn't saving it.

> Git add stages the file. Run status again. Now it says, changes to be
> committed.

> And git commit saves the change in history, with a message.

## Scene 5: Why staging exists
visual: slide
title: Why the extra `git add` step?
bullets:
- You often change several files
- But you only want some of them in a commit
- Staging lets you choose

> Why the extra add step? Because you often change several files.

> But you only want some of them in this commit.

> Staging lets you choose.

## Scene 6: See what changed
visual: terminal
focus: 1 | 2-4 | 5
notes:
- Change the file
- `-` lines are removed. `+` lines are added.
- `-am` stages every tracked file that changed, and commits
code:
```
$ echo 'print("Hello, open source!")' > hello.py
$ git diff
-print("Hello")
+print("Hello, open source!")
$ git commit -am "Greet open source"
```

> Now change the file.

> And run git diff. It shows changes you haven't committed yet. Minus lines
> are removed. Plus lines are added.

> Then, git commit, dash a m. It stages every tracked file that changed, and
> commits, in one go. It skips brand new files. Those still need git add.

## Scene 7: Branches
visual: terminal
focus: 1 | 2-3 | 4-5 | 6-8
notes:
- Create a branch called `shout`, and switch to it
- Change the file and commit, on the branch
- On `shout`, it shouts
- On `main`, it doesn't. Same file, different branch.
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

> A branch lets you try something without touching main. Git switch, dash c,
> shout. That means, create a branch called shout, and switch to it.

> Change the file, and commit.

> Run it. It shouts.

> Now switch back to the main branch, and run it again. It doesn't shout. The same file
> prints different things, depending on which branch you're on. Switching
> branches changes the files in your folder.

## Scene 8: Merge
visual: terminal
focus: 1-3 | 4-7 | all
notes:
- `main` hadn't changed, so git just moves it forward: a fast-forward
- `main` and `shout` now point at the same commit
- In real projects, the maintainer merges your pull request
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

> Happy with shout? Bring it into main, with git merge shout. Main hadn't
> changed since shout branched off. So git just moves main forward. That is
> called a fast forward.

> Look at the log. Main and shout now point at the same commit.

> In real projects, you rarely merge into main yourself. You push a branch,
> and open a pull request. The maintainer merges it. That is exactly what
> happened to your first commit, in lesson two.

## Scene 9: Remotes
visual: slide
layout: cards
title: Remotes: other copies of the repo
bullets:
- upstream | The original repo. You pull from here. | `git pull upstream main`
- origin | Your fork on GitHub. You push here. | `git push origin my-branch`
- Pull request | Asks upstream to take the commits from a branch on your fork. | Done on GitHub

> The last idea is remotes. Your sandbox has none. But your clone of the
> course repo has two. Upstream is the original repo. You pull new commits
> from there.

> Origin is your fork. You push your branches there.

> And a pull request asks upstream to take the commits from a branch on your
> fork. You do that on GitHub, not with git.

## Scene 10: Done
visual: slide
title: You know just enough git
bullets:
- `status`, `add`, `commit` and `diff` to make changes
- `switch -c` and `merge` for branches
- Pull from `upstream`, push to `origin`

> That is just enough git. Status, add, commit and diff, to make changes.

> Switch and merge, for branches.

> Pull from upstream, and push to origin. Next lesson, you use all of them
> to open a real pull request, with Python code and a test.
