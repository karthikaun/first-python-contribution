from greetings.thejesh23 import greet


def test_greet_includes_name():
    assert "Sam" in greet("Sam")


def test_greet_is_friendly():
    assert greet("Sam").startswith("Hello")
