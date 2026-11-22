"""Small text helpers used by Exercise 3 (Lesson 09).

This file has a bug on purpose. See Lesson 09. Don't open a pull request to
fix it: the next learner needs it broken.
"""


def slugify(title: str) -> str:
    """Turn a title into a URL slug, e.g. "Hello World" -> "hello-world"."""
    return title.lower().replace(" ", "-")
