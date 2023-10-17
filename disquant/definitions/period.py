from __future__ import annotations

from enum import Enum
from functools import total_ordering


class Unit(str, Enum):
    DAY = "D"
    WEEK = "W"
    MONTH = "M"
    YEAR = "Y"


@total_ordering
class Period:
    """
    A Period is the difference between two dates expressed as a
    number of calendar day(s), week(s), month(s) or year(s).
    """

    def __init__(self, quantity: int, unit: Unit) -> None:
        self.quantity = quantity
        self.unit = unit

    def __str__(self) -> str:
        return f"{self.quantity}{self.unit}"

    def __repr__(self) -> str:
        return f"Period(quantity={self.quantity}, unit={self.unit}')"

    def __eq__(self, other: Period) -> bool:
        if not isinstance(other, Period):
            raise TypeError

        return self._days == other._days

    def __lt__(self, other: Period) -> bool:
        if not isinstance(other, Period):
            raise TypeError

        return self._days < other._days

    def __mul__(self, other: int) -> Period:
        if not isinstance(other, int):
            raise TypeError

        return Period(self.quantity * other, self.unit)

    def __rmul__(self, other: int) -> Period:
        if not isinstance(other, int):
            raise TypeError

        return Period(self.quantity * other, self.unit)

    def __add__(self, other: Period) -> Period:
        if not isinstance(other, Period):
            raise TypeError

        if not other.unit == self.unit:
            raise ValueError

        return Period(self.quantity + other.quantity, self.unit)

    @property
    def _days(self) -> int:
        """
        Private method to express the period in a
        standard number of days.
        Used to compare and sort periods.
        Examples: 1M < 3M, 12M = 1Y, etc.
        """
        match self.unit:
            case "D":
                return self.quantity
            case "W":
                return self.quantity * 7
            case "M":
                return self.quantity * 30
            case "Y":
                return self.quantity * 360
            case _:
                raise NotImplementedError
