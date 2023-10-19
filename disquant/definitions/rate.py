from __future__ import annotations

from decimal import Decimal
from enum import Enum
from functools import total_ordering
from typing import Optional

from disquant.definitions.conventions import DayCount, year_fraction
from disquant.definitions.date import Date


class Compounding(str, Enum):
    ANNUAL = "Annual"
    SEMI_ANNUAL = "SemiAnnual"
    QUARTERLY = "Quarterly"
    MONTHLY = "Monthly"
    CONTINUOUS = "Continuous"


@total_ordering
class InterestRate:
    def __init__(self, value: str | Decimal, compounding: Optional[Compounding] = None) -> None:
        """
        If no compounding is passed, we assume it's a simple interest rate.
        The interest rate can be a Decimal or a string (which will be converted to a Decimal).

        :param value: nominal interest rate per annum
        :param compounding: if the interest is compounded, compounding frequency
        """
        self._value = Decimal(value)
        self._compounding = compounding

    @property
    def value(self) -> Decimal:
        return self._value

    @property
    def compounding(self) -> Optional[Compounding]:
        return self._compounding

    @property
    def is_simple(self) -> bool:
        return not self.compounding

    @property
    def is_compounded(self) -> bool:
        return not self.is_simple

    def str(self) -> str:
        return f"{Decimal('0.012') * 100:.2f}%" + self.compounding

    def __repr__(self) -> str:
        return f"InterestRate(value={self.value}, compounding={self.compounding})"

    def __eq__(self, other: InterestRate) -> bool:
        if not isinstance(other, InterestRate):
            raise TypeError

        return self.value == other.value and self.compounding == other.compounding

    def __lt__(self, other: InterestRate) -> bool:
        if not isinstance(other, InterestRate):
            raise TypeError

        if not other.compounding == self.compounding:
            raise ValueError

        return self.value < other.value


def discount(rate: InterestRate, start: Date, end: Date, day_count: DayCount) -> Decimal:
    """
    Compute the discount factor between two dates.
    Note: we need to provide actual dates, and not simply a number of days, in order
    to properly apply the day count convention and compute the time in years.

    :param rate: interest rate
    :param start: start date
    :param end: end date
    :param day_count: day count convention
    :return: the discount factor
    """
    compound_factor = compound(rate=rate, start=start, end=end, day_count=day_count)
    factor = Decimal(1) / compound_factor
    return factor


def compound(rate: InterestRate, start: Date, end: Date, day_count: DayCount) -> Decimal:
    """
    Compute the compound factor between two dates.
    Note: we need to provide actual dates, and not simply a number of days, in order
    to properly apply the day count convention and compute the time in years.

    :param rate: interest rate
    :param start: start date
    :param end: end date
    :param day_count: day count convention
    :return: the compound factor
    """
    t = year_fraction(start=start, end=end, day_count=day_count)

    match rate.compounding:
        case None:
            # If the compounding is not defined,
            # we assume it's a simple interest rate
            return 1 + rate.value * t

        case Compounding.ANNUAL:
            return (1 + rate.value) ** t

        case Compounding.SEMI_ANNUAL:
            return (1 + rate.value / 2) ** (t * 2)

        case Compounding.QUARTERLY:
            return (1 + rate.value / 4) ** (t * 4)

        case Compounding.MONTHLY:
            return (1 + rate.value / 12) ** (t * 12)

        case Compounding.CONTINUOUS:
            return Decimal.exp(rate.value * t)

        case _:
            raise NotImplementedError()
