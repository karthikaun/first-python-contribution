from greetings.karthikaun import greet


def test_greet_includes_name():
    assert "Sam" in greet("Sam")
