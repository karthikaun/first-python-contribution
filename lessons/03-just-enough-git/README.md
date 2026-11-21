# Lesson 03: Just enough git

**Time:** 3 minute video · 15 minute exercise
**You'll need:** git set up (Lesson 02)

You don't need to know all of git to contribute. You need six ideas. We'll
try each one in a throwaway **sandbox** folder, so nothing can go wrong.

| Idea | In one sentence |
|---|---|
| **Repository** | A project folder plus its whole history, kept in a hidden `.git` folder. |
| **Commit** | A snapshot of your files, with a message, an author and a link to the snapshot before it. |
| **Staging** | `git add` picks which changes go into the next commit. |
| **Branch** | A name that points at a commit and moves forward when you commit. |
| **Merge** | Bringing one branch's commits into another. |
| **Remote** | Another copy of the repository, usually on GitHub. |

## 1. A repository

Make a sandbox folder anywhere *outside* the course repo, and turn it into a
repository:

```bash
mkdir git-sandbox
cd git-sandbox
git init -b main
git status
```

`git init` creates the hidden `.git` folder, and `-b main` names the first
branch `main`. That folder *is* the
repository: delete it and the history is gone, but your files stay.
`git status` is the command you'll run most. It tells you where you are and
what's changed.

## 2. Your first local commit

```bash
echo 'print("Hello")' > hello.py
python3 hello.py
git status
git add hello.py
git status
git commit -m "Add hello.py"
git log --oneline
```

Watch `git status` change:

1. After creating the file, `hello.py` is **untracked**: git sees it but isn't saving it.
2. After `git add`, it's **staged**: "Changes to be committed".
3. After `git commit`, the change is saved in history and status is clean.

Why the extra `add` step? Because you often change several files but only
want some of them in a commit. Staging lets you choose.

## 3. See what changed

```bash
echo 'print("Hello, open source!")' > hello.py
git diff
git commit -am "Greet open source"
git log --oneline
```

`git diff` shows changes you haven't committed yet: `-` lines are removed,
`+` lines are added. `git commit -am` stages every already-tracked file
that changed and commits in one go. (It skips brand-new files: those still
need `git add`.)

## 4. Branches

A branch lets you try something without touching `main`:

```bash
git switch -c shout
echo 'print("HELLO, OPEN SOURCE!")' > hello.py
git commit -am "Shout the greeting"
python3 hello.py
git switch main
python3 hello.py
```

The same file prints different things depending on which branch you're on.
Switching branches changes the files in your folder to match that branch.

Here's what your history looks like now:

```text
main:   A ── B
               \
shout:          C
```

`main` points at commit B. `shout` points at commit C, which builds on B.
`git switch -c shout` means "create a branch called shout and switch to it".
(Older guides use `git checkout -b shout`, which does the same thing.)

## 5. Merge

Happy with `shout`? Bring it into `main`:

```bash
git merge shout
python3 hello.py
git log --oneline --graph --all
```

Because `main` hadn't changed since `shout` branched off, git just moves
`main` forward to C. That's called a **fast-forward**.

In real projects you rarely merge into `main` yourself. You push a branch and
open a pull request, and the **maintainer** merges it. That's exactly what
happened to your first commit in Lesson 01.

## 6. Remotes

Your sandbox has no remotes:

```bash
git remote -v
```

It prints nothing. Your clone of the course repo has two (from Lesson 02):

```text
          upstream (thejesh23/first-python-contribution)     ← you pull from here
               │
               │  fork
               ▼
          origin (YOUR-USERNAME/first-python-contribution)   ← you push here
               │
               │  clone
               ▼
          your computer
```

The four commands that move commits between them:

| Command | What it does |
|---|---|
| `git pull upstream main` | Get new commits from the original repo into your current branch. |
| `git push origin my-branch` | Send your branch to your fork on GitHub. |
| `git fetch upstream` | Download new commits from upstream without changing your files. |
| *Pull request* | Ask upstream to take the commits from a branch on your fork. Done on GitHub, not with git. |

## Clean up

The sandbox was just for practice. Delete it whenever you like:

```bash
cd ..
rm -rf git-sandbox
```

Next: [Lesson 04: your second PR, from the terminal](../04-second-pr-from-terminal/).
