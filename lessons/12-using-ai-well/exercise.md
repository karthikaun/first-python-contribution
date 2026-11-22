# Exercise 10: Verify, then rewrite

## Part 1: Check what an AI tells you

If you use an AI tool, ask it to explain this line from your Exercise 3 fix:

```python
return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
```

Then **verify every claim it makes** by running examples in Python. For
example, if it says "digits are kept", check `slugify("Python 3")`. Write
down anything it got wrong or left out. (Hint: what happens to `"Café"`?)

No AI tool? Explain the line yourself, then check *your* claims the same way.

## Part 2: Rewrite an AI-style PR description

Rewrite this in **five lines or fewer**, in your own words, for the
Exercise 3 fix:

```text
## Summary
This PR introduces a comprehensive and robust enhancement to the slugify
utility, significantly improving its handling of various edge cases and
ensuring consistent, reliable output across a wide range of inputs.

## Key Changes
- Implemented advanced regex-based normalization of separators
- Added extensive test coverage for numerous scenarios
- Improved overall code quality and maintainability

## Benefits
- Enhanced reliability and user experience
- Future-proofed the implementation for upcoming requirements
```

Checklist for your version:

- [ ] Links the issue (`Fixes #...`)
- [ ] Says what was wrong and what happens now, specifically
- [ ] Says how you tested it
- [ ] No claims you didn't check ("future-proofed", "significantly")
- [ ] No headings or bullet lists needed for a change this small

## Part 3: Find two real policies

Find the AI section of two projects you might contribute to (use your
Lesson 06 notes). Write down each project's disclosure format, if it has one.
