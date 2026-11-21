# Video script: Star, fork, and your first commit

Target length: about 8 minutes.

## Scene 1: Hook
visual: slide
title: Ten minutes from now, you're a contributor
bullets:
- No install
- Just a browser and a GitHub account

> In the next ten minutes, you'll make your first contribution to a public
> project on GitHub. No install, nothing to set up. Just your browser and a
> GitHub account. Let's go.

## Scene 2: Four words
visual: slide
title: Four words you'll use forever
bullets:
- Star: a bookmark
- Fork: your own copy of a repo
- Commit: a saved snapshot of a change
- Pull request: "please pull my commit in"

> Four words first. A star is a bookmark. A fork is your own copy of someone
> else's project, where you can change anything without touching the
> original. A commit is a saved snapshot of a change, with a message saying
> what changed. And a pull request asks the original project to pull your
> commit in.

## Scene 3: Star
visual: browser
url: https://github.com/thejesh23/first-python-contribution
caption: Click Star, top right

> Open the course repository. The link is in the description. Top right,
> there's a Star button. Starring saves the repo to your list of stars, so you
> can find it again, and it helps other beginners find it. It's optional, and
> it doesn't change any code.

## Scene 4: Fork
visual: browser
url: https://github.com/thejesh23/first-python-contribution/fork
caption: Fork → Create fork

> Next to Star is Fork. Click it, then click Create fork. After a few
> seconds you're on a page with your username in the address. Look under the
> name: it says forked from thejesh23 slash first python contribution. This
> is your copy.

## Scene 5: Create your file
visual: browser
url: https://github.com/thejesh23/first-python-contribution/tree/main/first-commits
caption: first-commits → Add file → Create new file

> In your fork, open the folder called first commits. Click Add file, then
> Create new file. Name the file after your GitHub username, followed by dot
> p y. It has to match your username exactly, including capital letters.

## Scene 6: Three lines of Python
visual: code
code:
name = "Your Name"
github = "your-github-username"
message = "Why you're learning Python"

> Now type three lines of Python. Name equals your name, in quotes. GitHub
> equals your username, in quotes. And message equals one sentence about
> you, or why you're learning Python. These are three variables, each holding a string. Watch the quotes:
> every value needs one at the start and one at the end.

## Scene 7: Commit
visual: browser
url: https://github.com/thejesh23/first-python-contribution
caption: Commit changes... → write a message → Commit changes

> Click Commit changes. Write a short message, like: add first commit for,
> and your username. Keep commit directly to the main branch selected. That's
> fine here, because this is your fork. Click Commit changes. Congratulations,
> that's your first commit. Right now it only lives in your fork.

## Scene 8: Open the pull request
visual: browser
url: https://github.com/thejesh23/first-python-contribution/compare
caption: Contribute → Open pull request

> Go back to the main page of your fork. There's a banner saying your branch
> is one commit ahead. Click Contribute, then Open pull request. Check the
> arrow at the top: your fork on the right, pointing into the original repo
> on the left. Click Create pull request.

## Scene 9: The bot
visual: slide
title: What happens next
bullets:
- A check reads your file with Python's own parser
- All good: the bot comments and merges your PR
- Something wrong: it tells you exactly what to fix

> Now watch. A check called validate first commit starts running. It reads
> your file with Python's own parser, the same one Python uses before it runs
> your code. If everything's right, the bot leaves a comment and merges your
> pull request. If something's off, it tells you exactly what to fix. Fix it
> in your fork, commit again, and your pull request updates by itself.

## Scene 10: You did the real thing
visual: slide
title: That's the real workflow
bullets:
- Fork → commit → pull request → checks → merge
- Real projects add a human review
- Next: git on your own machine

> See that purple Merged badge? Your commit is now part of a public project.
> That's the same workflow behind every open source contribution: fork,
> commit, pull request, checks, merge. Real projects add a human reviewer and
> run real tests, and you'll do both later in this course. Next lesson, we set
> up git on your own machine.
