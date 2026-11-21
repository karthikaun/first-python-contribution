# Quiz 07

**1. What does `-linked:pr` mean in a GitHub issue search?**

<details><summary>Answer</summary>

Only issues that don't have a pull request linked to them.
</details>

**2. An issue has no assignee and no linked PR. Is it safe to start?**

<details><summary>Answer</summary>

Not yet. Read the whole thread (someone may have claimed it in a comment or
the maintainers may have decided against it), search PRs including closed
ones, check it's agreed (no `needs triage`) and reproduce it on `main`.
</details>

**3. Which comment is the better claim, and why?**
a) "can i work on this?"
b) "I'd like to work on this. I can reproduce it on main. My plan is to
return an empty list and add a test. Does that sound right?"

<details><summary>Answer</summary>

b). It shows you read the issue, checked it still happens, and have a plan
the maintainer can approve in one line.
</details>

**4. Someone claimed an issue two months ago and never opened a PR. What
do you do?**

<details><summary>Answer</summary>

Ask them politely if they're still working on it. If there's no answer after
about a week, ask a maintainer whether you can take over, and credit them in
your PR.
</details>

**5. Why might a popular project have almost no open `good first issue`s?**

<details><summary>Answer</summary>

They're taken quickly. Try other labels, projects you use, or problems you
hit yourself.
</details>
