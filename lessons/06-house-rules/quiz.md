# Quiz 06

**1. You open a PR to a new project and a bot asks you to sign a CLA. What
should you check before signing?**

<details><summary>Answer</summary>

Read the agreement. If you have a job, check whether your employer owns code
you write; you may need a corporate CLA. Make sure your commits use the
email you sign with.
</details>

**2. A project's CONTRIBUTING says "all commits must be signed off". What do
you do?**

<details><summary>Answer</summary>

Commit with `git commit -s`. For commits you already made, use
`git commit --amend -s --no-edit` (last commit) or `git rebase --signoff main`
(all of them), then `git push --force-with-lease`.
</details>

**3. A project allows AI-assisted code. Can you use AI to write your PR
description and review replies?**

<details><summary>Answer</summary>

Check the policy: some projects (nixpkgs, for example) don't allow LLM output
in descriptions or comments even when they allow AI code. Either way, writing
them yourself is the safe choice.
</details>

**4. An AI tool tells you it found a security bug in a library. What now?**

<details><summary>Answer</summary>

Reproduce it yourself first. If it's real, follow the project's
`SECURITY.md` and report it privately, saying you used AI if the policy asks
(curl, for example, requires it).
</details>

**5. Where do big projects like CPython keep their contributing rules?**

<details><summary>Answer</summary>

On a developer guide website. For CPython it's the Python Developer's Guide
at devguide.python.org.
</details>
