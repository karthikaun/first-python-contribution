# Video script: Using AI tools well

Target length: about 3 minutes.

## Scene 1: Hook
visual: slide
title: You're responsible for every line
bullets:
- Whoever, or whatever, wrote it
- Could you explain it without asking the AI again?

> Lesson five was about whether a project allows AI tools. This one is about
> using them well when it does. And there's one rule above all the others.
> You're responsible for every line you submit, whoever or whatever wrote it.
> If a reviewer asks why it works, you need to be able to answer without
> asking the AI again.

## Scene 2: Where it helps
visual: slide
title: Where AI tools help
bullets:
- Explaining unfamiliar code
- Reading a traceback in plain words
- Pointing at where to change
- Suggesting test cases you forgot

> AI tools are genuinely useful for some things. Explaining code you've
> never seen. Turning a scary traceback into plain words. Pointing you at the
> files where a change probably belongs. And suggesting test cases you forgot.
> In every case, check what it told you against the real code.

## Scene 3: Where it hurts
visual: slide
title: Where AI tools hurt
bullets:
- Confident, plausible, and wrong
- Changing the test instead of the code
- Huge diffs nobody asked for
- Bug reports nobody reproduced

> And they can hurt. They invent functions and options that don't exist,
> with total confidence. They'll make a test pass by weakening the test,
> which CPython lists as unacceptable. They "improve" things nobody asked
> about. And they report bugs nobody has reproduced, which costs maintainers
> real hours.

## Scene 4: A workflow
visual: slide
title: A workflow that keeps you in charge
bullets:
- Understand and reproduce the issue yourself
- Use AI to explore and draft
- Read every line of git diff; delete what you can't explain
- Run the tests and the examples, then disclose

> So here's a workflow that keeps you in charge. Understand and reproduce
> the issue yourself first. Use AI to explore, or to draft. Then read every
> line of your diff as if a stranger wrote it, and delete anything you can't
> explain. Run the tests and the examples from the issue. And disclose it,
> the way the project asks.

## Scene 5: A disclosure trailer
visual: terminal
code:
```
$ git commit -m "Add demo" --trailer "Assisted-by: TOOL-NAME"
$ git log -1 --format=%B
Add demo

Assisted-by: TOOL-NAME
```

> Some projects, like LLVM and nixpkgs, want a line at the end of the commit
> message, called a trailer. Git adds it for you with dash dash trailer.
> Others want a sentence in the pull request description, or a checkbox in
> the template. Use exactly the format the project shows.

## Scene 6: Your own words
visual: code
code:
```
Fixes #12

slugify kept punctuation and doubled hyphens for repeated spaces. It now
turns each run of non-alphanumeric characters into one hyphen and strips
hyphens from the ends. Added a regression test with the cases from the
issue.
```

> Now, the part people get wrong most. Write your comments and descriptions
> yourself. Maintainers can spot AI prose instantly: headings and bullet
> points for a three line change, words like comprehensive and robust, and
> claims nobody checked. This description is short, specific, and clearly
> written by the person who did the work.

## Scene 7: Plain English is fine
visual: slide
title: Plain, simple English is perfect
bullets:
- Not your first language? Short sentences in your own words
- Maintainers are used to it
- Polished AI prose is the thing they object to

> If English isn't your first language, that's completely fine. Short,
> simple sentences in your own words are far better than polished AI prose.
> Maintainers all over the world read plain English every day.

## Scene 8: Privacy and licences
visual: slide
title: Privacy and licences
bullets:
- Never paste secrets or private code into AI tools
- Some projects treat AI code as possibly copied
- That's why their rules are strict: respect them

> Two last things. Never paste secrets or private code into an AI tool. And
> some projects worry that AI generated code might be copied from somewhere
> with an incompatible licence. That's why their rules are strict. Respect
> them.

## Scene 9: Done
visual: slide
title: Use AI to learn faster, not to skip learning
bullets:
- You're responsible for every line
- Verify, keep diffs small, disclose
- Your words in every conversation

> Use AI to learn faster, not to skip the learning. You're responsible for
> every line, you verify everything, and every conversation is in your own
> words. Next lesson: what happens after you open the pull request, and how
> contributing works outside GitHub.
