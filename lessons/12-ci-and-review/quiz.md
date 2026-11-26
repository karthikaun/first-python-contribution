# Quiz 12

**1. CI failed on your PR. Where do you look first?**

<details><summary>Answer</summary>

The last lines of the failing step's log (`gh run view --log-failed`, or the
check's **Details** link). That's where the tool says what went wrong.
</details>

**2. In a conflict, what's between `<<<<<<< HEAD` and `=======` during a
rebase?**

<details><summary>Answer</summary>

What's on the branch you're rebasing onto (upstream's `main`). Your commit's
version is between `=======` and `>>>>>>>`.
</details>

**3. Why `git push --force-with-lease` instead of `git push --force`?**

<details><summary>Answer</summary>

It only overwrites your branch on GitHub if nobody else has pushed to it
since you last fetched, so you can't accidentally destroy someone's work.
</details>

**4. A reviewer asks for a change mid-review. New commit, or amend and
force-push?**

<details><summary>Answer</summary>

Usually a new commit, so the reviewer can see exactly what changed. Squash
at the end only if asked.
</details>

**5. Your checks say "awaiting approval". What do you do?**

<details><summary>Answer</summary>

Wait. GitHub needs a maintainer to approve workflow runs for first-time
contributors.
</details>
