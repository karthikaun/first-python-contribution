"""The tests splitbill ships with. They pass, and splitbill still has bugs."""

import splitbill


def test_even_split_with_tip(capsys):
    assert splitbill.main(["120", "--people", "4", "--tip", "15"]) == 0
    out = capsys.readouterr().out
    assert "Total: $138.00" in out
    assert out.count("$34.50") == 4


def test_no_tip_by_default():
    assert splitbill.tip_amount(80, 0, 0) == 0


def test_split_between_two():
    assert splitbill.split(50, 2) == [25.0, 25.0]


def test_money_has_two_decimals():
    assert splitbill.money(7.5) == "$7.50"
