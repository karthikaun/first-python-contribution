"""Small text helpers used by Exercise 3 (Lesson 10).

This file has a bug on purpose. See Lesson 10. Don't open a pull request to
fix it: the next learner needs it broken.
"""


def slugify(title: str) -> str:
    """Turn a title into a URL slug, e.g. "Hello World" -> "hello-world"."""
    return title.lower().replace(" ", "-")
