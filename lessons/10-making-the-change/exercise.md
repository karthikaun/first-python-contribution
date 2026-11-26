# Exercise 10: Fix the planted bug (local only)

Exercise 3 happens on your machine. **Don't open a pull request**: the bug
has to stay for the next learner.

- [ ] `git fetch upstream`, then `git switch -c fix-slugify upstream/main`
- [ ] Reproduce the bug from the lesson's bug report
- [ ] Add a parametrized test to `practice/tests/test_textkit.py` and watch it fail
- [ ] Fix `slugify` in `practice/textkit.py`, and update its docstring
- [ ] `python -m pytest practice`, `ruff format practice`, `ruff check practice`
- [ ] Add `practice/news/slugify-separators.bugfix.md`
- [ ] Commit with a subject line and a body (`git commit`, no `-m`)
- [ ] `python tools/check_exercise_3.py` is all ✔

When you're done, go back to `main` with `git switch main`. Your fix stays
safe on the `fix-slugify` branch.

**Stretch 1:** what should `slugify("Café au lait")` return? Write a test
for what you think is right, and see what your fix does. In a real project
this is a question to ask in the issue before you decide.

**Next:** in Lesson 11 you write the pull request title and description
for this fix.
