from textkit import slugify


def test_slugify_two_words():
    assert slugify("Hello World") == "hello-world"
