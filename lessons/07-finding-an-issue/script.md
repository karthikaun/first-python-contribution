# Video script: Finding an issue

Target length: about 3 minutes.

## Scene 1: Start here
visual: slide
layout: title
title: Don't fix something that's already fixed
bullets:
- Find an issue that nobody else is working on.

> Here is the most common way beginners waste a weekend. They pick an issue.
> They work on it for days. They open a pull request. And they find that
> someone else fixed it last week.

> This lesson is about picking well. So that never happens to you.

## Scene 2: Be realistic
visual: slide
title: Good first issues get taken fast
bullets:
- In popular projects, often within days
- Try other labels: `help wanted`, `easy`, `beginner`, `documentation`
- Try projects you actually use
- Try problems you hit yourself

> Be realistic about the label, good first issue. In popular projects, those
> get taken fast, often within days. When we checked, in November 2026,
> {pytest|pie test} had just one open, and someone was already assigned to
> it.

> So widen your net. Try other labels. Help wanted, easy, beginner, or
> documentation. Every project names them differently.

> Try projects you actually use. You understand them, and you'll notice
> their rough edges.

> And try problems you hit yourself. A confusing error. A broken docs
> example. Nobody else is working on those.

## Scene 3: Search with filters
visual: slide
layout: cards
title: GitHub's issue search understands filters
bullets:
- `is:open` | Not closed
- `label:"good first issue"` | Has that label
- `no:assignee` | Nobody is assigned
- `-linked:pr` | No pull request is linked to it yet
- `language:python` | In a mostly-Python repository

> GitHub's issue search understands filters. Is open means not closed.

> Label means it has that label.

> No assignee means nobody is assigned.

> Minus linked {PR|P R} means no pull request is linked to it yet.

> And language Python means a mostly Python repository. The full search line
> is in the written lesson. Paste it into GitHub's search, and choose
> issues.

## Scene 4: The issue finder
visual: terminal
focus: 1 | 2-4 | 6
notes:
- It searches active Python projects with 500+ stars
- A candidate: the project, the title, the link, and its age
- Candidates, not guarantees. Your list will be different.
code:
```
$ python3 tools/find_issues.py
pipeshub-ai/pipeshub-ai (★4140)  Re-enable Greenhouse in the MCP server catalog
    https://github.com/pipeshub-ai/pipeshub-ai/issues/5044
    opened 23 days ago, 0 comments

26 of 62 issues look free. Read each thread fully before you claim one.
```

> That search returns a lot of tiny personal projects. The course's issue
> finder does better. It first finds active Python projects with five
> hundred stars or more. Then it searches those, with the same filters.

> It drops issues that an open pull request already mentions. And it flags
> issues where someone has commented, I'd like to work on this.

> Your list will be different. Issues are claimed and closed every day.
> These are candidates, not guarantees.

## Scene 5: The five checks
visual: slide
title: Before you claim: five checks
bullets:
- Read the whole thread, every comment
- Is someone already on it? Look at **Assignees** and the comments
- Is there a PR already? Look at **Development**, and search closed PRs too
- Is it agreed? `needs triage` means not decided yet
- Is it still a problem? Reproduce it on the latest `main`

> Before you claim a candidate, open it, and do five checks. One. Read the
> whole thread. Every comment. The answer is often in comment fourteen.

> Two. Is someone already on it? Look at the assignees, and at the comments.

> Three. Is there a pull request already? Look at Development in the
> sidebar. Then search the project's pull requests, including closed ones.
> A closed, unmerged one shows what the maintainers didn't want.

> Four. Is it agreed? Labels like needs triage, or needs decision, mean the
> maintainers haven't decided yet. Don't start coding.

> Five. Is it still a problem? Try to reproduce it on the latest main. Bugs
> get fixed without anyone closing the issue.

## Scene 6: Claim it well
visual: code
lang: text
file: Your comment on the issue
focus: all | 1-2 | 2-3
notes:
- In your own words, briefly, with your plan
- You read the issue, and checked it still happens
- You have a plan, so a maintainer can answer in one line
code:
```
Hi! I'd like to work on this. I can reproduce it on main: `parse("")`
raises IndexError. My plan is to return an empty list and add a test.
Does that sound right?
```

> Now claim it. Check the contributing file first. Some projects say, don't
> ask, just open a pull request. If it's not stated, comment in your own
> words, briefly, with your plan.

> This comment shows that you read the issue, and checked it still happens.

> And it shows you have a plan. So a maintainer can answer in one line. Then
> wait. Silence for a few days is normal.

## Scene 7: Don't
visual: slide
title: Three things not to do
bullets:
- Don't claim several issues at once
- Don't write "can I work on this?" with nothing else
- Don't use an AI tool to write the comment

> Three things not to do. Don't claim several issues at once, or one you
> can't start this week.

> Don't write, can I work on this, with nothing else.

> And don't use an {AI|A I} tool to write the comment.

## Scene 8: Old claims
visual: slide
layout: steps
title: When someone else claimed it first
bullets:
- Weeks old, no PR? Ask kindly
- Give it a week
- Ask a maintainer
- Mention them in your PR

> What if someone else claimed it first? If the claim is weeks old, with no
> pull request and no updates, ask kindly. Are you still working on this?

> Give it a week.

> If there is no answer, ask a maintainer whether you can take over.

> And if you do, mention the earlier person in your pull request. They may
> have useful notes.

## Scene 9: Done
visual: slide
title: You found your issue
bullets:
- Search wide
- Check carefully
- Claim with a plan, in your own words

> That is how you find an issue that is really yours. Search wide.

> Check carefully.

> And claim it with a plan, in your own words. Next lesson, making the
> change.
