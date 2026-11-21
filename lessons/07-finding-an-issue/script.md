# Video script: Finding an issue

Target length: about 7 minutes.

## Scene 1: Hook
visual: slide
title: Don't fix something that's already fixed
bullets:
- Days of work on an issue
- Open the PR
- Someone fixed it last week

> Here's the most common way beginners lose a weekend. They pick an issue,
> work on it for days, open a pull request, and find out someone else fixed
> it last week. This lesson is about picking well, so that never happens to
> you.

## Scene 2: Be realistic
visual: slide
title: Good first issues go fast
bullets:
- Popular projects' easy issues are taken in days
- Try help wanted, easy, documentation labels
- Projects you use, problems you hit yourself

> Be realistic about good first issues. In popular projects they get taken
> within days. When we checked, pytest had just one, and someone was already
> on it. So widen your net. Try other labels, like help wanted, easy or
> documentation. Try projects you actually use. And remember the problems
> you hit yourself, like a setup step that failed in lesson six. Nobody else
> is working on those.

## Scene 3: Search with filters
visual: code
code:
```
is:issue is:open label:"good first issue" no:assignee -linked:pr language:python
```

> GitHub search understands filters. Is open. A label. No assignee, so
> nobody's been given it. Minus linked P R, so there's no pull request for it
> yet. And language python. Paste that into GitHub's search and choose
> issues.

## Scene 4: The issue finder
visual: terminal
code:
```
$ python3 tools/find_issues.py
pipeshub-ai/pipeshub-ai (★4140)  Re-enable Greenhouse in the MCP server catalog
    https://github.com/pipeshub-ai/pipeshub-ai/issues/5044
    opened 23 days ago, 0 comments

26 of 62 issues look free. Read each thread fully before you claim one.
```

> That search finds lots of tiny personal projects. The course's issue
> finder is pickier. It looks only in active Python projects with five
> hundred stars or more, uses the same filters, then drops issues that an
> open pull request mentions, and flags ones where someone has already said
> I'll take this. You can change the label, or search one repository.

## Scene 5: The five checks
visual: slide
title: Before you claim: five checks
bullets:
- Read the whole thread, every comment
- Assignees, and claims in the comments
- Development sidebar and PR search, including closed PRs
- Labels like needs triage: not agreed yet
- Reproduce it on the latest main

> Those are candidates, not guarantees. Before you claim one, do five
> checks. Read the whole thread: the answer is often in comment fourteen.
> Look for assignees and claims. Check the development sidebar and search the
> pull requests, including closed ones. Look for labels like needs triage,
> which mean nobody's agreed what to do yet. And reproduce it on the latest
> main, because bugs get fixed without anyone closing the issue.

## Scene 6: Claim it well
visual: code
code:
```
Hi! I'd like to work on this. I can reproduce it on main: `parse("")`
raises IndexError. My plan is to return an empty list and add a test.
Does that sound right?
```

> Check the contributing file: some projects say just open a pull request.
> Otherwise, comment in your own words, with a plan. This one shows you've
> read the issue, reproduced it, and know what you'll do, so a maintainer can
> say yes in one line. Then wait. A few days of silence is normal.

## Scene 7: Old claims
visual: slide
title: When someone claimed it first
bullets:
- Weeks old, no PR? Ask kindly if they're still on it
- Wait a week, then ask a maintainer
- Taking over? Mention them in your PR

> And if someone claimed it weeks ago with no pull request, ask them kindly
> if they're still working on it. Give it a week, then ask a maintainer. If
> you take over, mention them in your pull request. They might have useful
> notes.

## Scene 8: Done
visual: slide
title: You found your issue
bullets:
- Search wide, then check carefully
- Claim with a plan, in your own words
- Next: making the change

> That's how you find an issue that's really yours. Search wide, check
> carefully, and claim it with a plan. Next lesson: making the change the
> way maintainers want it.
