# Video script: After the PR, and beyond GitHub

Target length: about 2 minutes.

## Scene 1: Hook
visual: slide
title: Your PR is open. Now what?
bullets:
- Waiting, and nudging once
- When the answer is no
- After the merge
- Contributing outside GitHub

> Your pull request is open, the checks are green, and nothing happens.
> This lesson is about the human side of open source. Waiting, nudging,
> hearing no, and what comes after a merge. And then a quick tour of how
> contributing works outside GitHub.

## Scene 2: Waiting
visual: slide
title: Silence is normal
bullets:
- Maintainers are often volunteers with jobs
- Days or weeks without a reply is normal
- Keep CI green and every comment answered
- Start reading your next issue

> Maintainers are often volunteers with jobs. Days or weeks of silence is
> completely normal, and it says nothing about your work. While you wait,
> keep your checks green, make sure every comment is answered, and start
> reading your next issue.

## Scene 3: Nudge once
visual: code
code:
```
Hi! Gentle ping on this one when someone has a moment. CI is green and
I'm happy to make any changes.
```

> After about two weeks, or whatever the contributing file says, one polite
> comment like this is fine. Then wait again. Don't ping every day, don't
> mention lots of maintainers, and don't message people privately about it.

## Scene 4: When the answer is no
visual: slide
title: When the answer is no
bullets:
- Say thanks
- Ask once, if it's unclear, what would be welcome
- Stale bots and maintainers finishing your PR
- It happens to everyone

> Sometimes the answer is no. A different approach was chosen, or someone
> else's fix landed first. It happens to experienced contributors all the
> time. Say thanks. If it's unclear, ask once what would be welcome. And if a
> maintainer finishes your pull request for you, that's a success: you'll
> usually still get credit.

## Scene 5: After the merge
visual: terminal
code:
```
$ git switch main
$ git pull upstream main
$ git branch -d my-fix
$ git push origin --delete my-fix
```

> And when it's merged, celebrate. You're a contributor to that project,
> permanently. Then tidy up: update main, and delete your branch locally and
> on your fork.

## Scene 6: Become a regular
visual: slide
title: Become a regular
bullets:
- Reproduce other people's bug reports
- Answer questions
- Improve the docs
- Review other people's PRs

> The most valuable contributors aren't the ones who write the most code.
> They're the ones who reproduce bug reports, answer questions, fix the docs,
> and review other people's pull requests. Even a comment saying this works
> for me on macOS is real help.

## Scene 7: Beyond GitHub
visual: slide
title: Beyond GitHub
bullets:
- GitLab: merge requests, the glab CLI
- Codeberg and Forgejo: very close to GitHub
- Gerrit: amend one commit, push to refs/for/main
- Mailing lists: patches by email

> Everything you've learned carries over to other platforms. GitLab calls
> pull requests merge requests. Codeberg feels almost like GitHub. Gerrit
> reviews each commit on its own, so you amend instead of adding commits.
> And some projects, like the Linux kernel, take patches by email.

## Scene 8: A patch
visual: terminal
code:
```
$ git format-patch -1
0001-Add-hello.py.patch
$ head -4 0001-Add-hello.py.patch
From 3f1c... Mon Sep 17 00:00:00 2001
From: Ada Lovelace <12345678+ada@users.noreply.github.com>
Subject: [PATCH] Add hello.py
```

> Here's what a patch looks like. Git format patch turns your commit into an
> email-ready file. Those projects send it with git send email, and review
> happens by replying. Each one documents its own process. Read it all
> before you send anything, because mailing lists are public and permanent.

## Scene 9: Done
visual: slide
title: The human side of open source
bullets:
- Patience, one polite nudge, gracious with no
- Clean up, then become a regular
- Next: the capstone

> Patience, one polite nudge, and grace when the answer is no. That's what
> makes maintainers glad to see you again. Next is the capstone: your first
> contribution to a project out in the real world.
