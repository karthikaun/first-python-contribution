# Quiz 10

**1. A reviewer asks why your AI-assisted fix works and you're not sure.
What should have happened before you opened the PR?**

<details><summary>Answer</summary>

You should have read and understood every line of the diff, and deleted or
rewritten anything you couldn't explain.
</details>

**2. An AI tool makes a failing test pass by changing the test's expected
value. Is that a fix?**

<details><summary>Answer</summary>

No. It hides the bug. Fix the code, not the test. CPython's guidelines
call this out as unacceptable.
</details>

**3. How do you add `Assisted-by: TOOL-NAME` to a commit with git?**

<details><summary>Answer</summary>

`git commit -m "..." --trailer "Assisted-by: TOOL-NAME"`, using the exact
format the project's policy shows.
</details>

**4. Your English isn't perfect. Should you use AI to polish your review
replies?**

<details><summary>Answer</summary>

Write them yourself in plain, simple sentences. Maintainers are used to
that, and many object to AI-written conversation. Some projects allow
translation tools, so check the policy.
</details>

**5. Name two things never to paste into an AI tool.**

<details><summary>Answer</summary>

Secrets (tokens, passwords, keys) and code you're not allowed to share.
</details>
