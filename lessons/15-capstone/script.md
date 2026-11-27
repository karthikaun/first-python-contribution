# Video script: Capstone: your first external contribution

Target length: about 2 minutes.

## Scene 1: Start here
visual: slide
layout: title
title: Now do it for real
bullets:
- A merged pull request, in an open source project you don't own.

> This is it. Time to do it for real.

> A merged pull request, in an open source project you don't own. When it's
> merged, you add yourself to the graduates wall. A bot checks your pull
> request on GitHub before letting you in.

## Scene 2: What counts
visual: slide
title: What counts
bullets:
- A **merged** PR, not just opened, on GitHub
- In a project you don't own, that isn't a fork
- Opened by you, merged by a maintainer
- Code, tests or docs: all count

> Here is what counts. A merged pull request. Not just opened.

> In a project you don't own, that isn't a fork. And not this course, or a
> practice repo.

> Opened by you, and merged by a maintainer.

> And code, tests or docs all count.

## Scene 3: What doesn't
visual: slide
title: Would they have wanted it anyway?
bullets:
- Not whitespace-only changes
- Not spelling "fixes" that aren't errors
- Not anything opened just to tick a box

> Some things don't count, even if they get merged. Whitespace only changes.

> Spelling fixes that aren't errors.

> Or anything opened just to tick a box. Maintainers can tell, and it costs
> them time. Here is the test. Would the maintainer have wanted this change,
> even if you weren't doing a course?

## Scene 4: Stage by stage
visual: slide
layout: steps
title: The capstone, stage by stage
bullets:
- Choose
- Read the house rules
- Set up
- Make the change
- Open the PR
- Review
- Wait, then graduate

> The written lesson has a checklist for every stage. Each one links to the
> lesson that covers it. Choose an issue, and do the five checks.

> Read the house rules, in full.

> Set up. The tests pass before you change anything.

> Make the change. On a branch, with the smallest fix.

> Open the pull request, in your own words.

> Handle review. Answer every comment.

> Then wait. One polite nudge, at most. And graduate.

## Scene 5: Start small
visual: slide
title: Start small
bullets:
- A docs fix or a small bug is a great capstone
- Expect 1 to 4 weeks, mostly waiting for review
- While you wait, it's fine to start a second candidate

> Prefer small. A docs fix, or a small bug, is a great capstone.

> Expect it to take one to four weeks. Mostly waiting for review.

> While you wait, it's fine to start on a second candidate, in another
> project. Just don't claim more than you can actively work on.

## Scene 6: Graduate
visual: code
file: graduates/ada.py
focus: all | 1-2 | 3 | 4
notes:
- In the course repo, on a new branch: `graduates/YOUR-USERNAME.py`
- Your name, and your GitHub username
- The link to your merged pull request
- One sentence: what you changed, or what you learned
code:
```
name = "Ada Lovelace"
github = "ada"
pr = "https://github.com/OWNER/REPO/pull/123"
message = "One sentence: what you changed, or what you learned"
```

> Once your pull request is merged, come back to this course repo. Sync
> main, make a branch, and create a file in the graduates folder, named
> after your username.

> It holds your name, and your GitHub username.

> The link to your merged pull request.

> And one sentence. What you changed, or what you learned. Then commit,
> push, and open a pull request, like in lesson five.

## Scene 7: The bot
visual: slide
title: The Validate graduate bot checks your PR
bullets:
- It is merged
- It is yours
- It was merged by someone else
- It is in a real project you don't own

> A bot looks up your pull request on GitHub. It checks that it is merged.

> That it is yours.

> That it was merged by someone else.

> And that it is in a real project you don't own. If everything checks out,
> the bot says so. A maintainer merges it, and you appear on the graduates
> wall. If not, its comment says exactly what's wrong.

## Scene 8: Now you can use AI agents
visual: slide
title: Now you can use AI agents
bullets:
- You know the basics. Claude Code, Codex or Cursor will speed you up.
- Read the project's AI policy first. Some accept no AI pull requests.
- You still answer for every line

> One last thing. You did this whole course by hand, so you know the basics.
> For your next contributions, go ahead and use agentic tools, like
> {Claude Code|Clawd Code}, Codex, or Cursor. They speed up the work, and now
> you can check what they did.

> But be careful. Read the project's {AI|A I} policy first. Some projects,
> including well known ones, don't accept {AI|A I} assisted pull requests at
> all. Others want you to say that you used one.

> And everywhere, you still answer for every line.

## Scene 9: Welcome
visual: slide
title: Welcome to open source
bullets:
- Go back to the same project
- Help the next beginner
- You can contribute to any open source project now

> And then, welcome to open source. Go back to the same project. Your second
> pull request there will be much easier, and maintainers remember helpful
> people.

> Help the next beginner.

> You can contribute to any open source project now. Thank you for taking
> the course.
