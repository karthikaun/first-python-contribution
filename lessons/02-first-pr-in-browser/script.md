# Video script: Star, fork, and your first commit

Target length: about 3 minutes.

## Scene 1: Start here
visual: slide
layout: title
title: Ten minutes from now, you're a contributor
bullets:
- No install. Just a browser and a GitHub account.

> In the next ten minutes, you'll make your first contribution to a public
> project on GitHub.

> No install. Nothing to set up. Just your browser, and a GitHub account.
> Let's go.

## Scene 2: Four words
visual: slide
layout: cards
title: Four words you'll use forever
bullets:
- Star | A bookmark. It changes nothing in the code.
- Fork | Your own copy of someone else's repo, under your account.
- Commit | A saved snapshot of a change, with a message saying what changed.
- Pull request | A request to the original repo: "please pull my commit in."

> Four words first. A star is a bookmark. It changes nothing in the code.

> A fork is your own copy of someone else's project. You can change your
> fork freely. The original is untouched.

> A commit is a saved snapshot of a change, with a message saying what
> changed.

> And a pull request asks the original project, please pull my commit in.

## Scene 3: Star
visual: browser
url: https://github.com/thejesh23/first-python-contribution
caption: Click Star, top right
image: captures/repo.png
highlight: 1236,184,96,36

> Open the course repository. The link is in the description. Near the top
> right, there's a Star button. Starring is optional. It bookmarks the
> course, so you can find it again, and it helps other beginners find it.

## Scene 4: Fork
visual: browser
url: https://github.com/thejesh23/first-python-contribution
caption: Fork → Create fork
image: captures/repo.png
highlight: 1138,184,98,36

> Next to Star is Fork. Click it, then click Create fork. After a few
> seconds, you're on a page with your username in the address. Look at the
> top left. It says, forked from {thejesh23/first-python-contribution|thejesh
> 23, slash, first python contribution}. That is your copy.

## Scene 5: Create your file
visual: browser
url: https://github.com/thejesh23/first-python-contribution/tree/main/first-commits
caption: In your fork: first-commits → Add file → Create new file
image: captures/first-commits.png
highlight: 337,417,1087,41

> In your fork, open the folder called first commits. Click Add file, then
> Create new file. Name the file after your GitHub username, followed by
> {.py|dot p y}. It must match your username exactly.

## Scene 6: Three lines of Python
visual: code
file: first-commits/octocat.py
focus: 1 | 2 | 3 | all
notes:
- Your name, in quotes
- Your GitHub username, in quotes
- One sentence: why you're learning Python
- Three variables holding strings. Each value needs `"` at both ends.
code:
```
name = "Your Name"
github = "your-github-username"
message = "Why you're learning Python"
```

> Now paste three lines of Python, and fill them in. Name equals your name,
> in quotes.

> GitHub equals your username, in quotes.

> And message equals one sentence. Why are you learning Python?

> That is real Python. Three variables, each holding a string. Watch the
> quotes. Every value needs one at the start, and one at the end.

## Scene 7: Commit
visual: slide
title: Commit your file
bullets:
- Click **Commit changes...**
- Write a message: `Add first commit for octocat`
- Keep "Commit directly to the main branch"
- Click **Commit changes**

> Now save it. Click Commit changes.

> Write a commit message. For example, add first commit for, and then your
> username.

> Keep, commit directly to the main branch, selected. This is your fork, so
> that's fine.

> Then click Commit changes. You just made a commit. Right now, it is in
> your fork. It is not in the original repo yet.

## Scene 8: Open the pull request
visual: browser
url: https://github.com/thejesh23/first-python-contribution/compare
caption: Contribute → Open pull request, then check base ← head
image: captures/compare.png
crop: 100,180,1240,250
highlight: 56,99,260,36

> Go to the main page of your fork. A banner says, this branch is one commit
> ahead. Click Contribute, then Open pull request. Check the arrow at the
> top. The base repository is the original. The head repository is your
> fork. Then click Create pull request.

## Scene 9: The bot
visual: browser
url: https://github.com/thejesh23/first-python-contribution/pull/52
caption: The bot explains what to fix. When your file is right, it merges.
image: captures/bot-review.png
height: 2600
crop: 100,515,900,552

> Now watch. Within a minute or two, a check called Validate first commit
> runs. It reads your file with Python's own parser, the same way Python
> reads your code before running it.

> If your file is right, the bot says so, and merges your pull request. If
> something is wrong, the bot tells you exactly what to fix. Fix it in your
> fork, and commit. Your pull request updates automatically, and the check
> runs again.

## Scene 10: You did the real thing
visual: slide
layout: steps
title: That's the real workflow
focus: 0 | all | all
bullets:
- Fork
- Commit
- Pull request
- Automated checks
- Merge

> When the bot merges it, you get the purple Merged badge. Your commit is
> now part of a public project.

> And that is the same workflow behind every open source contribution. Fork,
> commit, pull request, automated checks, merge.

> In real projects, the checks run first, then a human reviews and merges.
> Their checks also run real tests. You'll write some, and meet a human
> reviewer, later in this course. Next, we set up your own machine.
