# Exercise 02: A green doctor

- [ ] Install git, gh and Python 3.10+ (Lesson 02, step 1)
- [ ] Turn on **Keep my email addresses private** on GitHub and copy your noreply address
- [ ] Set `user.name`, `user.email` and `init.defaultBranch` with `git config --global`
- [ ] `gh auth login`
- [ ] `gh repo clone YOUR-USERNAME/first-python-contribution` and `cd` into it
- [ ] `git pull upstream main`
- [ ] `python3 tools/doctor.py` shows only green ✔

**Stuck on a red ✘?** The message says what to fix. If it still fails,
[open an issue](https://github.com/thejesh23/first-python-contribution/issues/new)
with the full doctor output pasted in. Remove anything you don't want public
first.

**Stretch:** run `git log --oneline -5`. The top lines are other learners'
first commits that you just pulled in from upstream.
