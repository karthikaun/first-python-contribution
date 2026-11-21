# Video script: House rules

Target length: about 4 minutes.

## Scene 1: Hook
visual: slide
title: Most closed PRs broke a rule, not the code
bullets:
- No issue first
- An unsigned CLA, a missing sign-off
- AI-written code where it isn't allowed

> Here's something nobody tells beginners. Most first pull requests that get
> closed aren't closed because the code was bad. They're closed because the
> contributor broke a house rule they never read. Every project writes its
> rules down. Today: where to find them, and the four that catch people out.

## Scene 2: Where the rules live
visual: slide
title: Where the rules live
bullets:
- CONTRIBUTING.md, or a developer guide: read all of it
- CODE_OF_CONDUCT.md
- The pull request template: fill every section
- SECURITY.md: report security bugs privately

> Start with the contributing file, or for big projects, a developer guide
> website. CPython's is called the Python Developer's Guide. Read all of it.
> There's also a code of conduct, a pull request template you should fill in
> completely, and a security file explaining how to report security bugs
> privately, never in a public issue.

## Scene 3: What to look for
visual: slide
title: Read CONTRIBUTING for these six things
bullets:
- Issue first? How do I claim one?
- Setup and test commands
- Style, commit messages, changelog
- CLA or DCO
- AI policy

> When you read it, look for six things. Do they want an issue before a pull
> request? How do you claim an issue? How do you set up and run the tests?
> What style, commit message and changelog rules are there? Is there a legal
> step, like a C L A or a D C O? And what's their policy on AI?

## Scene 4: CLAs
visual: slide
title: Rule 1: Contributor License Agreements
bullets:
- A legal agreement: you may contribute this, they may use it
- A bot comments on your first PR asking you to sign
- CPython: python-cla-bot checks every commit author's email
- Have a job? Check who owns code you write

> A C L A, a contributor license agreement, is a legal agreement. It says
> you have the right to contribute your code, and the project may use it.
> You'll meet one when a bot comments on your first pull request asking you
> to sign. CPython works like this: a bot checks the email on every commit,
> and you sign once per email address. So set up your noreply email first.
> And if you have a job, check your contract before signing. Many employers
> own code you write, even at weekends.

## Scene 5: DCO
visual: terminal
code:
```
$ git commit -s -m "Fix the typo in the install guide"
$ git log -1
    Fix the typo in the install guide

    Signed-off-by: Ada Lovelace <12345678+ada@users.noreply.github.com>
```

> Other projects use a D C O, a developer certificate of origin, instead.
> Nothing to sign on a website. Instead, every commit carries a signed off by
> line, saying you have the right to submit this code. Git adds it when you
> commit with dash s. The Linux kernel and QEMU require it. Forgot? Git commit
> dash dash amend dash s fixes your last commit. And some projects, like curl,
> don't use sign offs at all. Read the rules for this project.

## Scene 6: AI policies vary
visual: slide
title: Rule 3: AI policies vary a lot
bullets:
- Banned: Gentoo, NetBSD, QEMU
- Allowed with disclosure: LLVM, nixpkgs (Assisted-by trailer)
- Allowed, you're responsible: CPython, curl
- Policies change: always read the current one

> Now the rule that varies the most: AI. Some projects ban AI generated
> contributions. Gentoo, NetBSD and QEMU do. Some allow them if you disclose
> it and a human has reviewed every line, often with an Assisted by line in
> the commit message. LLVM and nixpkgs work like that. And some, like CPython
> and curl, accept AI assisted work but make you fully responsible for it.
> These policies change often, so always read the current one.

## Scene 7: Rules that work everywhere
visual: slide
title: AI rules that work everywhere
bullets:
- Find the AI section before you start
- Write your own comments and PR descriptions
- Understand every line you submit
- Reproduce any AI-found bug yourself before reporting it

> Some rules work everywhere. Find the AI section before you start, not after
> your pull request is closed. Write your comments and descriptions yourself.
> Maintainers want to talk to you, and plenty of projects ban AI written
> discussion even when they allow AI code. Understand every line you submit.
> And never report a bug an AI found until you've reproduced it yourself.

## Scene 8: Code of conduct
visual: slide
title: Rule 4: The code of conduct
bullets:
- Applies to issues, PRs, chat, everywhere
- Be kind, assume good intent
- It also says how to report problems: it protects you too

> Finally, the code of conduct. It applies everywhere the project meets:
> issues, pull requests, chat. Mostly it says be kind and assume good intent.
> It also says how to report someone who isn't, which protects you too.

## Scene 9: Your checklist
visual: slide
title: Pre-flight checklist, for every project
bullets:
- CONTRIBUTING read? Issue claimed?
- CLA or DCO?
- AI policy and disclosure format?
- Test, lint, commit and changelog rules?

> The written lesson has a checklist to copy for every new project. Use it
> every time, and you'll avoid the mistakes that close most first pull
> requests. Next lesson, we open up a real Python project and find our way
> around it.
