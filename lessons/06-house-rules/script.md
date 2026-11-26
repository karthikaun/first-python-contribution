# Video script: House rules

Target length: about 5 minutes.

## Scene 1: Start here
visual: slide
layout: title
title: Most closed PRs broke a rule, not the code
bullets:
- Every project writes its rules down. Read them first.

> Here is something nobody tells beginners. Most first pull requests that
> get closed aren't closed because the code is bad. They're closed because
> the contributor broke a house rule they never read.

> Every project writes its rules down. Today, you learn where to find them,
> and the four that catch beginners out most.

## Scene 2: Where the rules live
visual: slide
layout: cards
title: Where the rules live
bullets:
- `CONTRIBUTING.md` | How to set up, test and submit. The most important file. Read all of it.
- `CODE_OF_CONDUCT.md` | How people are expected to treat each other.
- PR template | The questions your PR description must answer. Fill in every section.
- `SECURITY.md` | How to report a security bug privately. Never in a public issue.

> Start with the contributing file. It tells you how to set up, test, and
> submit. It is the most important file. Read all of it. Big projects often
> keep it on a website instead. CPython's is called the Python Developer's
> Guide.

> The code of conduct says how people are expected to treat each other.

> The pull request template holds the questions your description must
> answer. Fill in every section.

> And the security file says how to report a security bug privately. Never
> in a public issue.

## Scene 3: What to look for
visual: slide
title: Read CONTRIBUTING for six things
bullets:
- Do they want an issue first?
- How do you claim an issue?
- How to set up and run the tests
- Style and commit messages
- Legal: a CLA or a DCO sign-off
- The AI policy

> When you read it, look for six things. One. Do they want an issue first?
> Many projects only accept pull requests for issues that a maintainer has
> agreed to. A surprise pull request is often closed unread.

> Two. How do you claim an issue? Some want a comment. Some assign issues.
> Some say, don't ask, just open a pull request.

> Three. How to set up, and run the tests.

> Four. Style and commit messages. Linters, a message format, a changelog
> entry.

> Five. A legal step. A {CLA|C L A}, or a {DCO|D C O} sign off.

> And six. The {AI|A I} policy. It varies the most, and it changes often.

## Scene 4: CLAs
visual: slide
title: Rule 1: Contributor License Agreements
bullets:
- A legal agreement between you and the project
- A bot comments on your first PR, asking you to sign
- CPython: you sign once per email address, so set your noreply email first
- Have a job? Check your employment contract before you sign

> Rule one. The {CLA|C L A}. A contributor license agreement. It is a legal
> agreement between you and the project. It confirms you have the right to
> contribute your code, and lets the project use it. You normally keep your
> copyright.

> How will you meet one? You open your first pull request, and a bot
> comments, asking you to sign. Your pull request can't be merged until you
> do.

> CPython works like this. The bot checks the email address of every
> commit's author, and you sign once per email address. So set up your
> {noreply|no reply} address before you sign.

> And read it before you sign. It is a legal document. If you have a job,
> check your employment contract. Many employers own code you write, even in
> your free time.

## Scene 5: DCO
visual: terminal
focus: 1 | 2-5 | all
notes:
- `-s` adds the sign-off line for you
- It certifies you wrote the code, or have the right to submit it
- Forgot? `git commit --amend -s --no-edit` fixes the last commit
code:
```
$ git commit -s -m "Fix the typo in the install guide"
$ git log -1
    Fix the typo in the install guide

    Signed-off-by: Ada Lovelace <12345678+ada@users.noreply.github.com>
```

> Rule two. Some projects use a {DCO|D C O} instead. A developer
> certificate of origin. There is nothing to sign on a website. Instead, you
> commit with dash s.

> Then every commit carries a signed off by line. In short, it certifies
> that you wrote the code, or have the right to submit it. The Linux kernel
> requires it on every patch. QEMU requires one too.

> Forgot it? Amend the last commit with dash s, then update your pull
> request. And some projects, like curl, say plainly that they don't use
> sign offs at all. That's the point. Read the rules for this project.

## Scene 6: AI policies vary
visual: slide
layout: cards
title: Rule 3: AI policies vary a lot
bullets:
- Some ban it | Gentoo, NetBSD, QEMU
- Some allow it, with disclosure | LLVM, nixpkgs: a human in the loop, and an `Assisted-by` trailer
- Some allow it, and you're responsible | CPython, curl

> Rule three. {AI|A I}. Projects take very different positions on code
> written with {AI|A I} tools. Some ban it. Gentoo, NetBSD and QEMU do.

> Some allow it, with disclosure, and a human responsible. In LLVM and
> nixpkgs, a human must stay in the loop, and you label tool use. The
> example label is an Assisted by line in the commit message.

> And some allow it, and you are responsible for the result. CPython and
> curl work like that. These policies change. Always read the current
> version.

## Scene 7: Rules that work everywhere
visual: slide
title: AI rules that work everywhere
bullets:
- Find the AI section before you start
- No policy written down? Ask, or disclose anyway
- Write your own comments and PR descriptions
- Understand every line you submit
- Reproduce any AI-found bug yourself before you report it
- Use the exact disclosure format the project shows

> Some rules work everywhere. Find the {AI|A I} section before you start.
> Not after your pull request is closed.

> No policy written down? Ask in the issue, or disclose anyway.

> Write your own comments and descriptions. Maintainers want to talk to you.

> Understand every line you submit. If a reviewer asks, why did you do this,
> then, the {AI|A I} did it, isn't an answer.

> Never submit a bug report that an {AI|A I} found, without reproducing it
> yourself.

> And use the exact disclosure format the project shows. Don't invent your
> own.

## Scene 8: Code of conduct
visual: slide
title: Rule 4: The code of conduct
bullets:
- It covers issues, PRs, chat, and anywhere else the project meets
- Be kind, assume good intent, no harassment
- It says how to report problems. That protects you too.

> Rule four. The code of conduct. It covers issues, pull requests, chat, and
> anywhere else the project meets.

> It usually comes down to this. Be kind. Assume good intent. No harassment.

> It also says how to report someone who breaks it. That protects you too.

## Scene 9: Your checklist
visual: slide
layout: cards
title: Pre-flight checklist, for every new project
bullets:
- Read | CONTRIBUTING, and the developer guide if there is one
- Issue | Issue first? Is mine free, and how do I claim it?
- Legal | A CLA to sign? A DCO sign-off, with `git commit -s`?
- AI policy | Banned, disclose, or allowed? Which disclosure format?
- Tools | Setup and test commands, linters, commit format, changelog
- People | PR template sections, and the code of conduct

> The written lesson has a checklist. Copy it into your notes for every new
> project. Read the contributing file.

> Check the issue rules.

> Check the legal step.

> Check the {AI|A I} policy.

> Note the setup, test and style rules.

> And the pull request template, and the code of conduct. Next lesson, we
> set up a real Python project.
