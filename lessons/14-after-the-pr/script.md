# Video script: After the PR, and beyond GitHub

Target length: about 3 minutes.

## Scene 1: Start here
visual: slide
layout: title
title: Your PR is open. Now what?
bullets:
- The human side: waiting, nudging, hearing no, and what comes after.

> Your pull request is open. The checks are green. And nothing happens.

> This lesson is about the human side. Waiting, nudging, rejection, and what
> comes after a merge. Then a quick tour beyond GitHub.

## Scene 2: Waiting
visual: slide
title: Silence is normal
bullets:
- Maintainers are often volunteers with jobs
- Days or weeks of silence is not a judgement of your work
- Keep CI green, and answer every review comment
- Start reading your next issue

> Maintainers are often volunteers with jobs.

> Days or weeks of silence is normal. It isn't a judgement of your work.

> While you wait, make sure {CI|C I} is green, and every review comment is
> answered.

> And start reading your next issue.

## Scene 3: Nudge once
visual: code
lang: text
file: Your comment on the PR
notes:
- After about two weeks, one polite comment is fine. Then wait again.
code:
```
Hi! Gentle ping on this one when someone has a moment. CI is green and
I'm happy to make any changes.
```

> If there has been no response after about two weeks, or whatever the
> contributing file says, one polite comment is fine. Like this one. Then
> wait again. Don't ping daily. Don't mention many maintainers. And don't
> message people privately about it.

## Scene 4: When the answer is no
visual: slide
title: When the answer is no
bullets:
- It happens to experienced contributors too
- Say thanks
- Ask once, if it's unclear. Then accept the answer.
- Don't argue in circles, or reopen it

> Sometimes the answer is no. Pull requests get closed without merging all
> the time. The maintainers decided on a different approach. Or someone
> else's fix landed first. It happens to experienced contributors too.

> Say thanks. It leaves a good impression for next time.

> If it's unclear, ask once. Would a smaller change be welcome? Then accept
> the answer.

> And don't argue in circles, or reopen it.

## Scene 5: Two more endings
visual: slide
layout: cards
title: Two more endings you'll meet
bullets:
- A bot marks it "stale" | After inactivity, a bot closes the PR. Still interested? Comment before it closes.
- A maintainer finishes it | They push to your branch, or re-do it. You usually still get credit. That's a success.

> There are two more endings. A bot marks the pull request stale, and
> closes it after inactivity. If you're still interested, comment before it
> closes.

> Or a maintainer finishes it for you. You usually still get credit, often
> as a co-authored by line. That is a success, not a failure.

## Scene 6: After the merge
visual: terminal
focus: 1-2 | 3 | 4
notes:
- Sync your `main` with upstream
- Delete the branch on your computer
- And delete it on your fork
code:
```
$ git switch main
$ git pull upstream main
$ git branch -d my-fix
$ git push origin --delete my-fix
```

> And when it is merged? Celebrate. You are a contributor to that project,
> permanently. Then clean up. Switch to the main branch, and pull from upstream.

> Delete your branch.

> And delete it on your fork too. Then look for your change in the next
> release notes.

## Scene 7: Become a regular
visual: slide
title: Become a regular
bullets:
- Reproduce bug reports
- Answer questions
- Improve the docs
- Review other people's PRs

> The most valuable contributors aren't the ones who write the most code.
> They are the ones who reproduce bug reports.

> Answer questions.

> Improve the docs.

> And review other people's pull requests. Even a comment like, this works
> for me on macOS, is real help.

## Scene 8: Beyond GitHub
visual: slide
layout: cards
title: Beyond GitHub: what you've learned carries over
bullets:
- GitLab | Pull requests are called merge requests. The CLI is `glab`.
- Codeberg | Runs Forgejo. Very close to GitHub.
- Gerrit | Each commit is reviewed on its own. You amend it instead of adding new ones.
- Mailing lists | You send your commits as emails: patches. No web UI.

> Everything you've learned carries over to other platforms. The buttons,
> and some commands, change. On GitLab, pull requests are called merge
> requests.

> Codeberg is very close to GitHub.

> On Gerrit, each commit is reviewed on its own. You amend your commit,
> instead of adding new ones.

> And some projects use mailing lists. The Linux kernel, and git itself. You
> send your commits as emails, called patches.

## Scene 9: A patch
visual: terminal
focus: 1-2 | 3-7
notes:
- `git format-patch` turns a commit into a patch file
- The patch is an email: from, date, subject, and then your change
code:
```
$ git format-patch -1
0001-Add-hello.py.patch
$ head -5 0001-Add-hello.py.patch
From 3f1c... Mon Sep 17 00:00:00 2001
From: Ada Lovelace <12345678+ada@users.noreply.github.com>
Date: ...
Subject: [PATCH] Add hello.py
```

> Here is what a patch looks like. Git format patch turns your commit into
> a patch file.

> Look at the top of it. It is an email, with a from line, a date, and a
> subject. Those projects send it with git send email, and review happens by
> reply. Each project documents its own process. Read it fully before
> sending anything. Mailing lists are public, and permanent.

## Scene 10: Done
visual: slide
title: The human side of open source
bullets:
- Be patient, and nudge once
- Be gracious when the answer is no
- Clean up, then become a regular

> So. Be patient, and nudge once.

> Be gracious when the answer is no.

> Clean up after the merge, and become a regular. Next is the capstone.
> Your first contribution to a project in the real world.
