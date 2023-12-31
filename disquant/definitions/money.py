from __future__ import annotations

from enum import StrEnum
from functools import total_ordering
from typing import Optional

"""
Money object.
Inspired by https://pypi.org/project/money/

Using floats instead of Decimal for consistency
with the rest of the library.
"""


class Currency(StrEnum):
    EUR = "EUR"
    USD = "USD"


@total_ordering
class Money:
    def __init__(self, amount: float, currency: Currency) -> None:
        self._amount = amount
        self._currency = currency

    def __str__(self) -> str:
        return f"{self.currency} {self.amount}"

    def __repr__(self) -> str:
        return f"Money(amount={self.amount}, currency={self.currency})"

    @property
    def amount(self) -> float:
        return self._amount

    @property
    def currency(self) -> Currency:
        return self._currency

    def _check(self, other: Money) -> None:
        """
        Check that the other object is of type Money and has the
        same currency. Raise exceptions if not.
        """
        if not isinstance(other, Money):
            raise TypeError

        if not other.currency == self.currency:
            raise ValueError

    def __eq__(self, other: Money) -> bool:
        self._check(other)
        return other.amount == self.amount

    def __lt__(self, other: Money) -> bool:
        self._check(other)
        return self.amount < other.amount

    def __add__(self, other: Money) -> Money:
        self._check(other)
        return self.__class__(self.amount + other.amount, self.currency)

    def __sub__(self, other: Money) -> Money:
        self._check(other)
        return self.__class__(self.amount - other.amount, self.currency)

    def __hash__(self) -> int:
        return hash((self._amount, self._currency))

    def __round__(self, digits: Optional[int] = 0):
        return self.__class__(round(self._amount, digits), self._currency)

    def __mul__(self, other: float) -> Money:
        return self.__class__(self._amount * other, self._currency)

    def __rmul__(self, other: float) -> Money:
        return self.__mul__(other)

    def __neg__(self):
        return self.__class__(-self._amount, self._currency)

    def __pos__(self):
        return self.__class__(+self._amount, self._currency)

    def __abs__(self):
        return self.__class__(abs(self._amount), self._currency)

    def __int__(self):
        return int(self._amount)

    def __float__(self):
        return float(self._amount)
