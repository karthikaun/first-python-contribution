# Quiz 11

**1. Which title is better: "Update utils.py" or "Strip hyphens from the
ends of slugs"?**

<details><summary>Answer</summary>

The second. It says what the PR does. The first only names a file, which
the diff already shows.
</details>

**2. What four things belong in a pull request description?**

<details><summary>Answer</summary>

The issue it fixes (`Fixes #1234`), what changed and why, how you tested
it, and anything the reviewer should know.
</details>

**3. Your PR fixes half of issue 88. Do you write `Fixes #88`?**

<details><summary>Answer</summary>

No. `Fixes` closes the issue when the PR is merged. Write `Refs #88`, and
say what is still left to do.
</details>

**4. The project's template has a checkbox "I added tests". You didn't.
What do you do?**

<details><summary>Answer</summary>

Leave it unticked and say why, or add the tests. Never tick a box that
isn't true: the reviewer will check.
</details>

**5. Your change isn't finished, but you want CI to run on it. How do you
open the pull request?**

<details><summary>Answer</summary>

As a draft (`gh pr create --draft`, or the arrow next to **Create pull
request**). Mark it **Ready for review** when it's done.
</details>
