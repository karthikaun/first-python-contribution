from greetings.divya0795 import greet


def test_greet_includes_name():
    assert "Sam" in greet("Sam")
