# Video script: Opening a good issue

Target length: about 4 minutes.

## Scene 1: Start here
visual: slide
layout: title
title: Opening a good issue
bullets:
- When there's no issue yet, you write it.

> Sometimes there is no issue to pick up. You found a bug yourself. Or a
> docs page that's wrong. Or you want a feature.

> Then you open the issue. A good one gets fixed, sometimes by you. A vague
> one gets, can't reproduce, and is closed.

## Scene 2: Issue first
visual: slide
title: Many projects want the issue first
bullets:
- Agree on **what** to change, before anyone works on **how**
- CPython: the PR title names the issue, `gh-12345: Fix ...`
- Django: a ticket for everything except trivial changes
- CONTRIBUTING says which

> Before a pull request, many projects want an issue. So maintainers can
> agree on what to change, before anyone spends time on how.

> {CPython|C Python} is one. A pull request names its issue in the title.
> Found something new? Open the issue first. Only trivial changes, like a
> typo, can skip it.

> Django is another. Every change needs a ticket, unless it's trivial.

> Your project's contributing file says which rules apply. When it doesn't,
> an issue first is never wrong.

## Scene 3: Before you open one
visual: slide
layout: steps
title: Before you open one
bullets:
- Search open **and** closed issues
- Try the latest version
- Questions go to the forum or Discussions
- Security bugs: never a public issue

> Before you open one, search. Open and closed issues, with words from the
> error message. Already reported? Add what's new to that issue, or a thumbs
> up. Not a plus one comment.

> Try the latest version. It may be fixed already.

> Questions aren't issues. How do I, goes to the project's forum or
> discussions.

> And a security bug is never a public issue. Read the project's security
> file, or use Report a vulnerability. A public issue tells attackers before
> there's a fix.

## Scene 4: What a good report contains
visual: slide
layout: cards
title: What a good bug report contains
bullets:
- Title | What goes wrong, and when
- Steps to reproduce | The exact command someone can paste
- Expected | What should happen, and why
- Actual | The output as text, the whole traceback
- Versions | The package, Python, your OS

> A good bug report has five parts. A title that says what goes wrong, and
> when. Not, bug. Not, help.

> Steps to reproduce. The exact command or code someone can paste and run.

> Expected. What should happen, and why. Quote the docs if they say so.

> Actual. What happens instead. Paste the output as text, and the whole
> traceback. Never a screenshot of text.

> And versions. The package, Python, and your operating system. Most
> projects have an issue form that asks for exactly these.

## Scene 5: Keep it minimal
visual: code
lang: text
file: Steps to reproduce
focus: 1-2 | 4-5 | 7-10
notes:
- The smallest command that still shows the bug
- Expected, with the line from the docs
- Actual, pasted as text
code:
```
Steps to reproduce:
    python bug-hunt/splitbill.py 10 --people 3

Expected: shares of $3.34, $3.33 and $3.33, which add up to $10.00.
README.md says "the shares always add up to the total, to the cent".

Actual:
    Person 1: $3.33
    Person 2: $3.33
    Person 3: $3.33
```

> The steps matter most. A maintainer must see the bug before they can fix
> it. So make the example minimal. Cut everything that isn't needed, and
> check after each cut that the bug is still there.

> Then say what you expected, and why. Here, the docs promise the shares add
> up to the total.

> And paste what really happened. Three shares of three dollars thirty three
> make nine ninety nine. A cent went missing.

## Scene 6: The bug hunt
visual: terminal
focus: 1 | 2-5 | 7-10
notes:
- splitbill splits a bill between friends. It has bugs on purpose.
- Its README says what it should do
- This one is right. Others aren't.
code:
```
$ python bug-hunt/splitbill.py 120 --people 4 --tip 15
Bill:  $120.00
Tax:   $0.00
Tip:   $18.00 (15%)
Total: $138.00

Person 1: $34.50
Person 2: $34.50
Person 3: $34.50
Person 4: $34.50
```

> Now your turn. This course has a small program with bugs on purpose.
> Split bill splits a restaurant bill between friends.

> Its readme says what it should do. Try different bills, people, tips and
> tax, and compare.

> This one is right. Others aren't. There are five bugs to find.

## Scene 7: Report it
visual: slide
layout: steps
title: Report it with the Bug hunt form
bullets:
- **Issues → New issue → Bug hunt**
- Fill in every field
- A bot runs your command and checks your report
- Fix any ✘, then a maintainer reviews it

> Found one? Open issues, new issue, and pick the bug hunt form. Fill in
> every field.

> Within a minute, a bot checks your report. It even runs your command, and
> compares the result with a correct split bill. So it knows if your steps
> really show the bug.

> Fix anything it marks, by editing your issue. Then a maintainer reviews
> it. Please don't fix the bug in a pull request. The next learner needs it.

## Scene 8: Done
visual: slide
title: A report anyone can reproduce
bullets:
- Search first
- Minimal steps, expected and actual
- One bug per issue, in your own words

> That's a good issue. Search first. Give minimal steps, expected and actual.
> One bug per issue, in your own words.

> Next lesson, making the change.
