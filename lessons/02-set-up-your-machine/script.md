# Video script: Set up your machine

Target length: about 3 minutes.

## Scene 1: Start here
visual: slide
layout: title
title: From the browser to your own computer
bullets:
- Three tools. Installed once.

> In the last lesson, you made a commit without installing anything. But
> real projects need you to run their code and tests on your own computer.

> So today you install three tools. You only do this once.

## Scene 2: The three tools
visual: slide
layout: cards
title: The three tools every Python contributor uses
bullets:
- git | Tracks changes and makes commits on your computer.
- GitHub CLI: `gh` | Talks to GitHub from the terminal: logs you in, clones, opens pull requests.
- Python | Runs the project's code and tests. You need 3.10 or newer.

> First, git. It tracks changes, and makes commits on your computer.

> Second, the GitHub command line tool, called {gh|g h}. It talks to GitHub
> from the terminal. It logs you in, clones repositories, and opens pull
> requests.

> Third, Python. It runs the project's code and its tests. You need version
> three point ten, or newer.

## Scene 3: Windows tip
visual: slide
title: On Windows? Use Git Bash
bullets:
- Install Git for Windows first
- Use the Git Bash app for every command in this course
- Type `py` wherever you see `python3`

> Are you on Windows? Then install Git for Windows first.

> It adds an app called Git Bash. Use it for every command in this course.
> Then the commands are the same as on a Mac, or on Linux.

> One difference. Wherever you see python three, type {py|p y} instead.

## Scene 4: Check the versions
visual: terminal
focus: 1-2 | 3-4 | 5-6
notes:
- You want git 2.28 or newer
- You want Python 3.10 or newer
- "not found"? Reopen the terminal, or run the installer again.
code:
```
$ git --version
git version 2.47.1
$ python3 --version
Python 3.13.1
$ gh --version
gh version 2.63.0
```

> The install links for your system are in the written lesson. When the
> installers finish, close and reopen your terminal. Then check each tool.
> Git should be two point twenty eight, or newer.

> Python should be three point ten, or newer.

> And {gh|g h} should answer with a version too. If a command says not
> found, the install didn't finish, or the terminal needs reopening.

## Scene 5: Your private email
visual: slide
title: Keep your email private
bullets:
- Every commit records a name and an email. Anyone can read them once you push.
- On GitHub: **Settings → Emails**
- Tick **Keep my email addresses private**
- Copy your **noreply** address

> Here is something many beginners miss. Every commit records a name and an
> email. Anyone can read them once you push.

> So use the private address that GitHub gives you. On GitHub, open
> Settings, then Emails.

> Tick, keep my email addresses private. Also tick, block command line
> pushes that expose my email.

> Then copy the noreply address shown there.

## Scene 6: Tell git who you are
visual: terminal
focus: 1 | 2 | 3
notes:
- Your name, in quotes
- Your noreply address, not your real email
- New repositories start on a branch called `main`
code:
```
$ git config --global user.name "Ada Lovelace"
$ git config --global user.email "12345678+ada@users.noreply.github.com"
$ git config --global init.defaultBranch main
```

> Now tell git who you are. Git config, dash dash global, user dot name, and
> your name in quotes.

> Then user dot email, with that noreply address.

> The third line makes new repositories start on a branch called main.
> Global means, for every repository on this computer. So you only do this
> once.

## Scene 7: Log in
visual: terminal
focus: 1 | 2-5 | all
notes:
- Log in to GitHub from the terminal
- Four questions. Pick these answers.
- Paste the one-time code in your browser. Check with `gh auth status`.
code:
```
$ gh auth login
? Where do you use GitHub? GitHub.com
? What is your preferred protocol for Git operations? HTTPS
? Authenticate Git with your GitHub credentials? Yes
? How would you like to authenticate GitHub CLI? Login with a web browser
```

> Next, log in. Run {gh auth login|g h, auth, login}.

> It asks four questions. Answer GitHub dot com. {HTTPS|H T T P S}. Yes. And,
> login with a web browser.

> Then {gh|g h} shows a one time code, and opens your browser. Paste the
> code, approve, and come back. To check it worked, run {gh auth status|g h,
> auth, status}.

## Scene 8: Clone your fork
visual: terminal
focus: 1-2 | 3 | 4-5 | 6-7
notes:
- Download your fork, then go into the folder
- List the remotes: the places this copy is connected to
- `origin` is your fork. You push your work here.
- `upstream` is the original course repo. `gh` added it for you.
code:
```
$ gh repo clone ada/first-python-contribution
$ cd first-python-contribution
$ git remote -v
origin    https://github.com/ada/first-python-contribution.git (fetch)
origin    https://github.com/ada/first-python-contribution.git (push)
upstream  https://github.com/thejesh23/first-python-contribution.git (fetch)
upstream  https://github.com/thejesh23/first-python-contribution.git (push)
```

> Remember the fork you made in the last lesson? Download it. {gh repo
> clone|G h, repo, clone}, your username, slash, first python contribution.
> Then go into the folder.

> Now run git remote, dash v. It shows two remotes. Two places this copy is
> connected to.

> Origin is your fork. You push your work here.

> Upstream is the original course repo. You get other people's changes from
> here. {gh|G h} added it for you, because it knows your repo is a fork.

## Scene 9: Run the doctor
visual: terminal
focus: 1 | 2 | 3-10 | 12
code:
```
$ git pull upstream main
$ python3 tools/doctor.py
✔ Python 3.13.1
✔ venv module available
✔ git 2.47.1
✔ git user.name is 'Ada Lovelace'
✔ git user.email is your private noreply address (12345678+ada@users.noreply.github.com)
✔ gh 2.63.0
✔ gh is logged in as ada
✔ origin is your fork, upstream is the course repo

All set. You're ready for Lesson 03.
```

> Last step. Other learners' commits have landed since you forked. So pull
> from upstream, to bring your copy up to date.

> Then run the course's checker. Python three, tools, slash, doctor
> {.py|dot p y}.

> It checks everything you just did. Each line should be a green tick. A red
> cross tells you what to fix. Fix the first one, and run it again.

> When it says all set, you are ready.

## Scene 10: Done
visual: slide
title: Your machine is ready
bullets:
- git, `gh` and Python are installed
- Your commits carry a private email
- Your fork is cloned, with `origin` and `upstream`

> That's it. Git, {gh|g h} and Python are installed.

> Your commits carry a private email.

> And your fork is on your computer, connected to origin and upstream. Next
> lesson, just enough git to never feel lost.
