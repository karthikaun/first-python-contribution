# Exercise 04: The sandbox

Do every block in the [lesson](README.md) in your own `git-sandbox` folder.
Then, without looking:

- [ ] Create a branch called `whisper`
- [ ] Change `hello.py` to print the greeting in lowercase, and commit it
- [ ] Switch back to `main` and check `hello.py` hasn't changed
- [ ] Merge `whisper` into `main`
- [ ] Run `git log --oneline --graph --all` and find your three branches' names

**Stretch:** on `main`, change `hello.py` and commit *before* merging
`whisper`. The merge can't be a fast-forward now. Git either creates a
**merge commit** or, if both branches changed the same line, reports a
**merge conflict**. If you get a conflict, open `hello.py`, keep the line
you want, delete the `<<<<<<<`, `=======` and `>>>>>>>` markers, then run
`git add hello.py` and `git commit`. You'll meet conflicts again in Lesson 12.
