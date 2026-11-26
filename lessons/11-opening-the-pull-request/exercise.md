# Exercise 11: Write the pull request

You fixed `slugify` in Lesson 10. Now write the pull request you would
open for it. **Don't open it**: the bug has to stay for the next learner.

- [ ] `git switch fix-slugify`
- [ ] Read your own diff, as a reviewer would: `git diff main`
- [ ] Create a file called `pr-description.md` in the course folder
- [ ] Line 1: the title. Say what the PR does, in the imperative, in 72 characters or fewer
- [ ] Leave line 2 blank
- [ ] Then the description: `Fixes #1234`, what changed and why, and how you tested it
- [ ] Check it, and fix anything marked ✘:

  ```bash norun
  python tools/check_pr_description.py pr-description.md
  ```

- [ ] `git switch main` when you're done. Don't commit `pr-description.md`

**Stretch 1:** open the pull request for one of your merged course PRs on
GitHub (Lesson 02 or 05) and read its title and description as a
maintainer would. What would you change? You can still edit them.

**Stretch 2:** find a merged pull request in a project you use, and one
that was closed without merging. Compare their titles and descriptions.
