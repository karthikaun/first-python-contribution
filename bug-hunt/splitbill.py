"""splitbill: split a restaurant bill between friends.

This is the bug hunt for Lesson 09. The program has bugs **on purpose**.
Read README.md (it says how splitbill should behave), try it, and report a
bug you find as an issue. Don't open a pull request that fixes them: the
next learner needs the bugs.
"""

from __future__ import annotations

import argparse

__version__ = "1.2.0"


def parse_percent(text: str) -> float:
    """Read a tip percentage. Both "15" and "15%" mean 15 percent."""
    return float(text)


def tip_amount(bill: float, tax: float, tip_percent: float) -> float:
    """The tip, worked out on the bill before tax."""
    return (bill + tax) * tip_percent / 100


def split(total: float, people: int) -> list[float]:
    """Each person's share. The shares always add up to the total exactly."""
    share = round(total / people, 2)
    return [share] * people


def money(amount: float) -> str:
    """Format an amount like $1,234.50."""
    return f"${amount:.2f}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="splitbill", description="Split a restaurant bill between friends.")
    parser.add_argument("bill", type=float, help="the bill before tax and tip, e.g. 120 or 120.50")
    parser.add_argument("--people", type=int, default=1, help="how many people share the bill (default: 1)")
    parser.add_argument("--tip", default="0", help="tip percentage, e.g. 15 or 15%% (default: 0)")
    parser.add_argument("--tax", type=float, default=0.0, help="tax as an amount, e.g. 9.60 (default: 0)")
    parser.add_argument("--version", action="version", version=f"splitbill {__version__}")
    args = parser.parse_args(argv)

    tip_percent = parse_percent(args.tip)
    tip = tip_amount(args.bill, args.tax, tip_percent)
    total = args.bill + args.tax + tip

    print(f"Bill:  {money(args.bill)}")
    print(f"Tax:   {money(args.tax)}")
    print(f"Tip:   {money(tip)} ({tip_percent:g}%)")
    print(f"Total: {money(total)}")
    print()
    for number, share in enumerate(split(total, args.people), start=1):
        print(f"Person {number}: {money(share)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
