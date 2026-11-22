"""bug-hunt/splitbill.py must keep its planted bugs: learners report them (Lesson 09)."""

import pytest

import splitbill


def test_uneven_split_still_loses_a_cent():
    assert round(sum(splitbill.split(100, 3)), 2) != 100


def test_tip_still_includes_tax():
    assert splitbill.tip_amount(100, 10, 20) != 20


def test_percent_sign_still_crashes():
    with pytest.raises(ValueError):
        splitbill.parse_percent("15%")


def test_zero_people_still_crashes():
    with pytest.raises(ZeroDivisionError):
        splitbill.main(["50", "--people", "0"])


def test_money_still_has_no_thousands_separator():
    assert splitbill.money(1234.5) != "$1,234.50"


def test_the_documented_example_still_works(capsys):
    """The README's first example must stay correct, so learners can trust the rest of it."""
    splitbill.main(["120", "--people", "4", "--tip", "15"])
    assert capsys.readouterr().out.splitlines()[:4] == [
        "Bill:  $120.00",
        "Tax:   $0.00",
        "Tip:   $18.00 (15%)",
        "Total: $138.00",
    ]
