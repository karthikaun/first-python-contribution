# Quiz 10

**1. Why should your test fail before you write the fix?**

<details><summary>Answer</summary>

It proves the test actually detects the bug. A test that passes on the
broken code can't protect against the bug coming back.
</details>

**2. While fixing `slugify`, you notice another function with messy
formatting. Do you tidy it in the same PR?**

<details><summary>Answer</summary>

No. Keep the PR to what the issue needs. Unrelated changes slow review.
Mention it, or send a separate PR if the project wants it.
</details>

**3. Which commit subject is better: "Fixed the bug." or "Fix slugify for
repeated spaces and punctuation"?**

<details><summary>Answer</summary>

The second: imperative mood, says what changed, no full stop.
</details>

**4. What does `Fixes #1234` in a PR description do?**

<details><summary>Answer</summary>

GitHub links the PR to issue 1234 and closes the issue when the PR is merged.
</details>

**5. You found a bug but can't fix it. What makes a bug report useful?**

<details><summary>Answer</summary>

What happened, what you expected, a minimal example someone can paste and
run, and your versions (package, Python, OS).
</details>
