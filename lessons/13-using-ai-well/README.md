# Lesson 12: Using AI tools well

**Time:** 3 minute video · 30 minute exercise
**You'll need:** Lesson 06 (house rules) and Lesson 10

Lesson 06 was about *whether* a project allows AI tools. This lesson is
about using them **well** when it does: so they make you a better
contributor, not a source of work for maintainers.

> **This course is honest about its own AI use:** it was drafted with AI and
> reviewed by a human, and every command in it is tested.

## The one rule

**You are responsible for every line you submit, whoever or whatever wrote
it.** If a reviewer asks "why does this work?", you must be able to answer
without asking the AI again.

## Where AI tools help

| Task | How it helps | How to use it safely |
|---|---|---|
| **Understanding unfamiliar code** | "What does this function do? Where is X handled?" | Open the files it names and check it's right |
| **Reading a traceback** | Explains an error in plain words | Reproduce the error yourself first |
| **Finding where to change** | Points you at likely files | Confirm by reading the code, or with `grep` |
| **Drafting a test** | Suggests cases you forgot | Run it on the buggy code: it must fail (Lesson 10) |
| **Rubber-ducking** | Explaining your plan out loud finds gaps | Ideas only. Nothing is submitted |

## Where AI tools hurt

- **Plausible but wrong.** AI can invent functions, options and APIs that
  don't exist, with total confidence. If you didn't run it, it isn't verified.
- **Changing the test instead of the code.** Making tests pass by weakening
  them is the opposite of a fix. CPython's guidelines list it as an
  unacceptable use.
- **Huge diffs.** AI tends to "improve" things nobody asked about. Lesson 10's
  rule still holds: the smallest change the issue needs.
- **Unverified bug and security reports.** Never report something an AI
  "found" until you've reproduced it yourself. Maintainers spend real hours on
  fake reports.
- **Your words.** Comments, PR descriptions and replies are you talking to a
  person (see below).

## A workflow that keeps you in charge

1. **Understand the issue yourself first.** Reproduce it (Lesson 10).
2. **Use AI to explore**: explain code, suggest where to look, list edge cases.
3. **Write the change yourself, or treat AI output as a draft you rewrite.**
4. **Read every line of the diff** (`git diff`) as if a stranger wrote it.
   Delete anything you can't explain.
5. **Run it**: the tests, the linters, and the examples from the issue.
6. **Disclose**, the way the project asks.

## Disclosing AI use

Follow the project's own format exactly (Lesson 06). The three common ones:

**A commit trailer**, used by LLVM and nixpkgs. git can add it for you:

```bash
mkdir ai-trailer-demo
cd ai-trailer-demo
git init -q -b main
echo 'print("hi")' > demo.py
git add demo.py
git commit -q -m "Add demo" --trailer "Assisted-by: TOOL-NAME"
git log -1 --format=%B
```

```text
Add demo

Assisted-by: TOOL-NAME
```

Replace `TOOL-NAME` with what the project's policy asks for: usually the
tool's name, sometimes its version.

**A sentence in the PR description**, for example: "I used an AI assistant
to help write the tests; I reviewed and ran all of them."

**A checkbox in the PR template.** Tick it honestly.

No policy? A one-line disclosure in the PR description is the safe default.

## Write your own words

Many maintainers who accept AI-assisted *code* object to AI-written
*conversation*. Some projects (nixpkgs, for example) don't allow LLM output in
PR descriptions, comments or commit message bodies at all. The tell-tale
signs maintainers notice:

- long, over-formatted descriptions with headings and bullet lists for a
  three-line change
- praise and filler ("Great question!", "This comprehensive fix...")
- confident claims nobody checked ("This improves performance significantly")

Compare two PR descriptions for the same change:

```text
## Summary
This PR introduces a comprehensive and robust enhancement to the slugify
utility, significantly improving its handling of edge cases. ...
## Key Changes
- Implemented advanced regex-based normalization ...
## Benefits
- Enhanced reliability and maintainability ...
```

```text
Fixes #12

slugify kept punctuation and doubled hyphens for repeated spaces. It now
turns each run of non-alphanumeric characters into one hyphen and strips
hyphens from the ends. Added a regression test with the cases from the
issue.
```

The second is shorter, specific, and clearly written by someone who did the
work. **If English isn't your first language**, simple, plain sentences in
your own words are far better than polished AI prose. Maintainers are used
to both. (Some policies allow translation tools: check.)

## Privacy and licensing

- **Don't paste secrets** (tokens, passwords, private keys) or code you're
  not allowed to share into an AI tool.
- **Licensing matters.** Some projects (NetBSD, for example) treat
  AI-generated code as possibly copied from somewhere with an incompatible
  licence. That's why their policies are strict. Respect them.

Next: [Lesson 13: after the PR, and beyond GitHub](../13-after-the-pr/).
