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
        return f"{self._value * 100:.2f}%" + self.compounding

    def __repr__(self) -> str:
        return f"InterestRate(value={self._value}, compounding={self._compounding})"

    def __eq__(self, other: InterestRate) -> bool:
        if not isinstance(other, InterestRate):
            raise TypeError

        return self._value == other.value and self._compounding == other.compounding

    def __lt__(self, other: InterestRate) -> bool:
        if not isinstance(other, InterestRate):
            raise TypeError

        if not other._compounding == self._compounding:
            raise ValueError

        return self._value < other._value

    def __round__(self, digits: Optional[int] = 0):
        return self.__class__(round(self._value, digits), self._compounding)


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
    factor = 1 / compound_factor
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


def as_rate(
    factor: Decimal,
    start: Date,
    end: Date,
    day_count: DayCount,
    compounding: Optional[Compounding] = None,
) -> InterestRate:
    """
    Express a discount factor as an interest rate
    taking into account the day count and compounding conventions.

    :param factor: discount factor
    :param start: start date
    :param end: end date
    :param day_count: day count convention
    :param compounding: compounding convention
    :return: the corresponding interest rate
    """
    t = year_fraction(start=start, end=end, day_count=day_count)

    match compounding:
        case None:
            # If the compounding is not defined,
            # we assume it's a simple interest rate
            rate = (1 / factor - 1) / t
            return InterestRate(rate, compounding)

        case Compounding.ANNUAL:
            rate = Decimal.exp(Decimal.ln(1 / factor) / t) - 1
            return InterestRate(rate, compounding)

        case Compounding.SEMI_ANNUAL:
            rate = 2 * (Decimal.exp(Decimal.ln(1 / factor) / (2 * t)) - 1)
            return InterestRate(rate, compounding)

        case Compounding.QUARTERLY:
            rate = 4 * (Decimal.exp(Decimal.ln(1 / factor) / (4 * t)) - 1)
            return InterestRate(rate, compounding)

        case Compounding.MONTHLY:
            rate = 12 * (Decimal.exp(Decimal.ln(1 / factor) / (12 * t)) - 1)
            return InterestRate(rate, compounding)

        case Compounding.CONTINUOUS:
            rate = Decimal.ln(1 / factor) / t
            return InterestRate(rate, compounding)

        case _:
            raise NotImplementedError()
