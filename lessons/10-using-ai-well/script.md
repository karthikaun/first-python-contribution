# Video script: Using AI tools well

Target length: about 3 minutes.

## Scene 1: Start here
visual: slide
layout: title
title: You're responsible for every line
bullets:
- Whoever, or whatever, wrote it.

> Lesson five was about whether a project allows {AI|A I} tools. This lesson
> is about using them well, when it does.

> There is one rule. You are responsible for every line you submit. Whoever,
> or whatever, wrote it. If a reviewer asks, why does this work, you must be
> able to answer without asking the {AI|A I} again.

## Scene 2: Where it helps
visual: slide
layout: cards
title: Where AI tools help
bullets:
- Understanding unfamiliar code | Then open the files it names, and check it's right.
- Reading a traceback | Reproduce the error yourself first.
- Finding where to change | Confirm by reading the code, or with `grep`.
- Drafting a test | Run it on the buggy code. It must fail.

> {AI|A I} tools help with some tasks. Understanding unfamiliar code. Ask
> what a function does. Then open the files it names, and check it's right.

> Reading a traceback. It explains an error in plain words. But reproduce
> the error yourself first.

> Finding where to change. It points you at likely files. Confirm by reading
> the code.

> And drafting a test. It suggests cases you forgot. Run the test on the
> buggy code. It must fail.

## Scene 3: Where it hurts
visual: slide
title: Where AI tools hurt
bullets:
- Plausible but wrong: if you didn't run it, it isn't verified
- Changing the test instead of the code
- Huge diffs that "improve" things nobody asked about
- Bug and security reports nobody reproduced

> And they can hurt. They can be plausible, but wrong. {AI|A I} can invent
> functions and options that don't exist, with total confidence. If you
> didn't run it, it isn't verified.

> They change the test instead of the code. Making tests pass by weakening
> them is the opposite of a fix. CPython's guidelines list it as an
> unacceptable use.

> They make huge diffs, improving things nobody asked about. The rule still
> holds. The smallest change the issue needs.

> And unverified bug reports. Never report something an {AI|A I} found,
> until you've reproduced it yourself. Maintainers spend real hours on fake
> reports.

## Scene 4: A workflow
visual: slide
layout: steps
title: A workflow that keeps you in charge
bullets:
- Understand the issue yourself
- Use AI to explore
- Write it, or rewrite the draft
- Read every line of the diff
- Run it
- Disclose

> Here is a workflow that keeps you in charge. Understand the issue
> yourself first. Reproduce it.

> Use {AI|A I} to explore. Explain code, suggest where to look, list edge
> cases.

> Write the change yourself. Or treat {AI|A I} output as a draft that you
> rewrite.

> Read every line of the diff, as if a stranger wrote it. Delete anything
> you can't explain.

> Run it. The tests, the linters, and the examples from the issue.

> And disclose, the way the project asks.

## Scene 5: A disclosure trailer
visual: terminal
focus: 1 | 2-5
notes:
- `--trailer` adds a line at the end of the commit message
- LLVM and nixpkgs use this format. Follow the project's own, exactly.
code:
```
$ git commit -q -m "Add demo" --trailer "Assisted-by: TOOL-NAME"
$ git log -1 --format=%B
Add demo

Assisted-by: TOOL-NAME
```

> How do you disclose? There are three common formats. The first is a
> commit trailer. Git can add it for you, with dash dash trailer.

> It becomes a line at the end of the commit message. LLVM and nixpkgs use
> this. The other two formats are a sentence in the pull request
> description, or a checkbox in the template. No policy? A one line
> disclosure in the description is the safe default.

## Scene 6: Spot the AI prose
visual: code
lang: text
file: PR description A
notes:
- Headings and bullets for a three-line change. Filler. Unchecked claims.
code:
```
## Summary
This PR introduces a comprehensive and robust enhancement to the slugify
utility, significantly improving its handling of edge cases. ...
## Key Changes
- Implemented advanced regex-based normalization ...
## Benefits
- Enhanced reliability and maintainability ...
```

> Now the part about your words. Many maintainers who accept {AI|A I}
> assisted code object to {AI|A I} written conversation. They notice the
> signs. Long descriptions, with headings and bullet lists, for a three line
> change. Praise and filler. And confident claims nobody checked.

## Scene 7: Your own words
visual: code
lang: text
file: PR description B
notes:
- Shorter, specific, and clearly written by someone who did the work
code:
```
Fixes #12

slugify kept punctuation and doubled hyphens for repeated spaces. It now
turns each run of non-alphanumeric characters into one hyphen and strips
hyphens from the ends. Added a regression test with the cases from the
issue.
```

> Compare it with this one, for the same change. It is shorter. It is
> specific. And it is clearly written by someone who did the work.

## Scene 8: Plain English is fine
visual: slide
title: Is English not your first language?
bullets:
- Simple, plain sentences in your own words
- Far better than polished AI prose
- Maintainers are used to both

> If English isn't your first language, write simple, plain sentences, in
> your own words.

> They are far better than polished {AI|A I} prose.

> Maintainers are used to both.

## Scene 9: Privacy and licences
visual: slide
title: Privacy and licensing
bullets:
- Don't paste secrets into an AI tool: tokens, passwords, private keys
- Don't paste code you're not allowed to share
- Some projects treat AI code as possibly copied. Respect their rules.

> Two last things. Don't paste secrets into an {AI|A I} tool. No tokens,
> passwords, or private keys.

> And no code you're not allowed to share.

> Licensing matters too. Some projects treat {AI|A I} generated code as
> possibly copied from somewhere with an incompatible licence. That is why
> their policies are strict. Respect them.

## Scene 10: Done
visual: slide
title: Stay in charge
bullets:
- You're responsible for every line
- Verify everything, and keep the diff small
- Disclose, the way the project asks
- Your own words in every conversation

> So, stay in charge. You are responsible for every line.

> Verify everything, and keep the diff small.

> Disclose, the way the project asks.

> And use your own words in every conversation. Next lesson, what happens
> after the pull request.
