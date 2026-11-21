# Exercise A: Break it, then fix it

Use the sandbox from the [troubleshooting page](README.md). For each
problem, cause it on purpose, read the message, and fix it **without looking
at the fix**:

- [ ] Get "would be overwritten by checkout" and fix it with `git stash`
- [ ] Commit on `main` by mistake, then move the commit to a new branch
- [ ] Get into "detached HEAD", make a commit there, and keep it on a branch
- [ ] Commit a file you didn't mean to, then take it out of the commit
- [ ] Amend a commit message

**Stretch:** clone the sandbox a second time (`git clone practice-remote.git
second-clone`), push a commit from the second clone, then try to push a
different commit from the first. Fix the "fetch first" rejection.
