"""Checks every learner's greeting follows the rules. Maintained by the course."""

import importlib
import inspect
import pkgutil

import pytest

import greetings

MODULES = sorted(m.name for m in pkgutil.iter_modules(greetings.__path__))


@pytest.mark.parametrize("module_name", MODULES)
def test_greeting_follows_the_rules(module_name):
    module = importlib.import_module(f"greetings.{module_name}")
    assert hasattr(module, "greet"), "define a function called greet"
    greet = module.greet
    params = list(inspect.signature(greet).parameters.values())
    assert len(params) == 1, "greet should take exactly one argument: name"
    assert params[0].annotation is str or params[0].annotation == "str", "annotate it: name: str"
    for name in ("Ada", "Sam", "Grace Hopper"):
        result = greet(name)
        assert isinstance(result, str), "greet should return a string"
        assert name in result, "the greeting should include the name"
        assert "\n" not in result, "keep the greeting on one line"
        assert len(result) <= 120, "keep the greeting to 120 characters or fewer"


def test_there_is_at_least_one_greeting():
    assert MODULES
