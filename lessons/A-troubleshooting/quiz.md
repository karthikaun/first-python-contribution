# Quiz A

**1. git says your local changes would be overwritten by checkout. Name two
ways forward.**

<details><summary>Answer</summary>

Commit the changes, or `git stash` them, switch, and `git stash pop` later.
</details>

**2. You committed on `main` by mistake and haven't pushed. What's the
safe order of commands?**

<details><summary>Answer</summary>

`git branch my-fix` first (to keep the commit), then
`git reset --hard origin/main` (or `upstream/main`), then `git switch my-fix`.
</details>

**3. Push rejected with "(fetch first)". What happened?**

<details><summary>Answer</summary>

GitHub has commits on that branch that you don't (for example a maintainer
pushed). `git pull --rebase`, then `git push`.
</details>

**4. You pushed to `OWNER/REPO` and got a 403. Why, and what fixes it?**

<details><summary>Answer</summary>

You cloned the original instead of your fork. `gh repo fork --remote` makes
your fork `origin` and the original `upstream`; then push again.
</details>

**5. `pip install` says `externally-managed-environment`. What now?**

<details><summary>Answer</summary>

Make and activate a virtual environment (`python3 -m venv .venv`,
`source .venv/bin/activate`) and install there.
</details>
