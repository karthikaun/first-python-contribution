# Quiz 03

**1. You created `notes.py`. `git status` lists it under "Untracked files".
What do you run before committing it?**

<details><summary>Answer</summary>

`git add notes.py`. It stages the file so the next commit includes it.
</details>

**2. What does `git diff` show?**

<details><summary>Answer</summary>

Changes you haven't committed yet: `-` lines removed, `+` lines added.
</details>

**3. You're on branch `fix-typo`. You run `git switch main`. What happens to
the files in your folder?**

<details><summary>Answer</summary>

They change to match `main`. Your `fix-typo` commits are still safe on that
branch.
</details>

**4. Which remote do you push your branch to, and which do you pull other
people's changes from?**

<details><summary>Answer</summary>

Push to `origin` (your fork). Pull from `upstream` (the original project).
</details>

**5. Does `git commit -am "..."` include a brand-new file you never added?**

<details><summary>Answer</summary>

No. `-a` only stages files git already tracks. New files need `git add` first.
</details>
