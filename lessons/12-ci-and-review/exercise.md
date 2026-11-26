# Exercise 12: The conflict lab

Do the whole lab from the [lesson](README.md), then do it **again without
looking**:

```bash norun
rm -rf ../conflict-lab
python3 tools/conflict_lab.py ../conflict-lab
cd ../conflict-lab/work
```

- [ ] Rebase `fix-greeting` on `upstream/main`
- [ ] Resolve the conflict by keeping both changes, then `git rebase --continue`
- [ ] `git push --force-with-lease`
- [ ] Add the docstring as a new commit and `git push`
- [ ] Squash into one commit and `git push --force-with-lease`
- [ ] `git log --oneline upstream/main..` shows exactly one commit

**Stretch 1:** start the lab again and squash with `git rebase -i upstream/main`
instead of `git reset --soft`.

**Stretch 2:** start the lab again, and in the middle of the rebase run
`git rebase --abort`. Check with `git log --oneline` that nothing was lost.

**Stretch 3:** find a merged PR in a project you use that had several rounds
of review. Read how the contributor replied to each comment.
