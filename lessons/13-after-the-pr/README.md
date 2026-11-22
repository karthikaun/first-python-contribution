# Lesson 12: After the PR, and beyond GitHub

**Time:** 3 minute video · 20 minute exercise
**You'll need:** Lesson 10

Your PR is open, checks are green, and... nothing happens. This lesson is
about the human side: waiting, nudging, rejection, and what comes after a
merge. Then a quick tour of how contributing works on platforms that aren't
GitHub.

## Waiting

Maintainers are often volunteers with jobs. **Days or weeks of silence is
normal**, and it isn't a judgement of your work. Some projects say how
long to expect in CONTRIBUTING; big ones often have a triage rotation.

While you wait:

- make sure CI is green and every review comment is answered
- don't push lots of tiny "fix typo" commits (each one notifies people)
- start reading your next issue

## Nudging, once

If there's been no response after about **two weeks** (or whatever
CONTRIBUTING says), one polite comment on the PR is fine:

```text
Hi! Gentle ping on this one when someone has a moment. CI is green and
I'm happy to make any changes.
```

Then wait again. **Don't** ping daily, @-mention many maintainers, or DM
people about it. If a project has a chat or forum, asking there which
reviewer to ask is fine.

## When the answer is no

PRs get closed without merging all the time: the maintainers decided on a
different approach, the feature doesn't fit, or someone else's fix landed
first. It happens to experienced contributors too.

- **Say thanks.** Something like "Thanks for looking. Understood!" leaves a
  good impression for next time.
- **Ask once, if it's unclear**: "Would a smaller change that only fixes X
  be welcome?" Then accept the answer.
- **Don't argue in circles** or reopen it.

Two more endings you'll meet:

- **A bot marks the PR "stale" and closes it** after inactivity. If you're
  still interested, comment before it closes.
- **A maintainer finishes it for you**, pushing to your branch (that's what
  the **Allow edits by maintainers** checkbox allows) or re-doing it. You
  usually still get credit, often as a `Co-authored-by:` line. That's a
  success, not a failure.

## After the merge

1. **Celebrate.** You're a contributor to that project, permanently.
2. **Clean up**: delete your branch, sync your fork.

   ```bash norun
   git switch main
   git pull upstream main
   git branch -d my-fix
   git push origin --delete my-fix
   ```

3. **Look for your change in the next release notes.**
4. **Become a regular.** The most valuable contributors aren't the ones who
   write the most code. They're the ones who reproduce bug reports, answer
   questions, improve docs and review other people's PRs (a "this works for
   me on macOS" comment on someone's PR is real help).

## Beyond GitHub

Everything you've learned (fork, branch, small commits, tests, review)
carries over. The buttons and some commands change.

| Platform | Pull requests are called | What's different |
|---|---|---|
| **GitLab** (gitlab.com and self-hosted) | Merge requests (MRs) | Same fork-and-branch flow. The CLI is `glab` instead of `gh`. |
| **Codeberg** (runs Forgejo) and other Forgejo/Gitea sites | Pull requests | Very close to GitHub. You need an account on *that* site. |
| **Gerrit** (used by some large projects) | Changes | Each commit is reviewed on its own. You **amend** your commit instead of adding new ones, a `Change-Id:` trailer (added by a commit-msg hook) ties versions together, and you push with `git push origin HEAD:refs/for/main`. |
| **Mailing lists** (the Linux kernel, git itself, and others) | Patches | You send your commits as emails. No web UI. |

### What a patch looks like

Mailing-list projects turn commits into patch files with `git format-patch`.
Try it in a sandbox:

```bash
mkdir patch-demo
cd patch-demo
git init -q -b main
echo 'print("hello")' > hello.py
git add hello.py
git commit -q -m "Add hello.py"
git format-patch -1
head -5 0001-Add-hello.py.patch
```

```text
0001-Add-hello.py.patch
From 3f1c... Mon Sep 17 00:00:00 2001
From: Ada Lovelace <12345678+ada@users.noreply.github.com>
Date: ...
Subject: [PATCH] Add hello.py
```

Those projects then send the patch with `git send-email` to the right list
and maintainers (the Linux kernel has `scripts/get_maintainer.pl` to find
them), reply-all to review, and send an updated "v2" series instead of new
commits. Each project documents its own process; the kernel's is
*Submitting patches* in its docs. Read it fully before sending anything:
mailing lists are public and permanent.

Next: [Lesson 13: the capstone](../13-capstone/).
