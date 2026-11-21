# Video script: Set up your machine

Target length: about 7 minutes.

## Scene 1: Hook
visual: slide
title: From the browser to your own computer
bullets:
- Real projects run their tests on your machine
- Three tools, installed once
- About 20 minutes, mostly waiting for installers

> In the last lesson you made a commit without installing anything. That's
> great for small edits, but real Python projects want you to run their code
> and tests on your own computer before you open a pull request. So today we
> install three tools. You only do this once.

## Scene 2: The three tools
visual: slide
title: The three tools
bullets:
- git: makes commits on your computer
- gh, the GitHub CLI: talks to GitHub from the terminal
- Python 3.10 or newer: runs the code and the tests

> Git makes commits on your computer. G H, the GitHub command line tool,
> talks to GitHub for you: it logs you in, downloads repositories and opens
> pull requests. And Python runs the project's code and its tests. You need
> version three point ten or newer.

## Scene 3: Windows tip
visual: slide
title: On Windows? Use Git Bash
bullets:
- Install Git for Windows first
- Open the Git Bash app for every command in this course
- Type py wherever you see python3

> If you're on Windows, install Git for Windows first. It comes with an app
> called Git Bash. Use it for every command in this course, and the commands
> will be exactly the same as on a Mac or Linux. One difference: wherever you
> see python three, type p y instead.

## Scene 4: Check the versions
visual: terminal
code:
$ git --version
git version 2.47.1
$ python3 --version
Python 3.13.1
$ gh --version
gh version 2.63.0

> The install links for your system are in the written lesson. Once they're
> done, close and reopen your terminal, and check each tool. Git should be two
> point twenty eight or newer, and Python three point ten or newer. If one says
> not found, reopen the terminal, or run its installer again.

## Scene 5: Your private email
visual: slide
title: Keep your email private
bullets:
- Every commit records a name and an email
- Anyone can read them once you push
- GitHub → Settings → Emails → Keep my email addresses private
- Copy your noreply address

> Here's something most tutorials skip. Every commit records your name and an
> email address, and anyone can read them once you push. So use the private
> address GitHub gives you. On GitHub, open Settings, then Emails, and tick
> keep my email addresses private. Tick block command line pushes that expose
> my email, too. Then copy the noreply address it shows you.

## Scene 6: Tell git who you are
visual: terminal
code:
$ git config --global user.name "Ada Lovelace"
$ git config --global user.email "12345678+ada@users.noreply.github.com"
$ git config --global init.defaultBranch main

> Now tell git. Git config, dash dash global, user dot name, and your name in
> quotes. Then the same for user dot email, with that noreply address. The
> third line makes new repositories start on a branch called main. Global
> means every repository on this computer, so you only do this once.

## Scene 7: Log in
visual: terminal
code:
$ gh auth login
? Where do you use GitHub? GitHub.com
? What is your preferred protocol for Git operations? HTTPS
? Authenticate Git with your GitHub credentials? Yes
? How would you like to authenticate GitHub CLI? Login with a web browser

> Next, log in. Run g h auth login and answer four questions: GitHub dot com,
> H T T P S, yes, and login with a web browser. G H shows a one time code and
> opens your browser. Paste the code, approve it, and you're in.

## Scene 8: Clone your fork
visual: terminal
code:
$ gh repo clone ada/first-python-contribution
$ cd first-python-contribution
$ git remote -v
origin    https://github.com/ada/first-python-contribution.git
upstream  https://github.com/thejesh23/first-python-contribution.git

> Remember the fork you made last lesson? Download it with g h repo clone,
> your username, slash first python contribution. Go into the folder and run
> git remote dash v. You'll see two remotes. Origin is your fork, where you
> push your work. Upstream is the original course repository, where you get
> everyone else's changes. G H set that up for you.

## Scene 9: Run the doctor
visual: terminal
code:
$ git pull upstream main
$ python3 tools/doctor.py
✔ Python 3.13.1
✔ git 2.47.1
✔ git user.email is your private noreply address
✔ gh is logged in as ada
✔ origin is your fork, upstream is the course repo
All set. You're ready for Lesson 03.

> Last step. Git pull upstream main brings in everything that's changed since
> you forked. Then run python three tools slash doctor dot p y. It checks
> everything we just did. Every line should have a green tick. If you see a
> red cross, it tells you exactly how to fix it. Fix the first one and run it
> again.

## Scene 10: Done
visual: slide
title: Your machine is ready
bullets:
- git, gh and Python installed
- A private email on every commit
- Your fork cloned, with origin and upstream
- Next: just enough git

> That's it. Your machine is set up like a real contributor's, with a
> private email on every commit. In the next lesson, we look at what git is
> actually doing when you commit, branch and push. Just enough to never feel
> lost.
