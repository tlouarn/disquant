from decimal import Decimal
from enum import StrEnum
from typing import Self

from disquant.definitions.conventions import DayCount
from disquant.definitions.date import Date, DateRange
from disquant.definitions.period import Period, Unit
from disquant.definitions.rate import InterestRate, discount
from disquant.utils.interpolation import linear_interpolation


class Method(StrEnum):
    """
    List of available interpolation methods in order to compute
    discount factors from the discount curve.
    """

    LINEAR_ZERO_RATE = "LinearZeroRate"
    LINEAR_DISCOUNT_FACTOR = "LinearDiscountFactor"
    LOG_LINEAR_DISCOUNT_FACTOR = "LogLinearDiscountFactor"


class DiscountCurve:

    def __init__(self, start: Date, dates: list[Date], factors: list[Decimal]) -> None:
        """
        Construct a discount curve from a list of discount factors.

        :param start: start date of the curve
        :param dates: list of dates for each discount factor
        :param factors: list of Decimal for each discount factor
        """
        # Check that each provided date is different
        if len(set(dates)) != len(dates):
            raise ValueError("Some dates are duplicated")

        # Check that there are as many dates as there are factors
        if len(dates) != len(factors):
            raise ValueError("There needs to be as many dates as factors")

        # Check that the start date is the smallest date
        if not start < min(dates):
            raise ValueError("Some dates are smaller or equal to the start date")

        # Check that the dates are ordered by increasing order
        if not sorted(dates) == dates:
            raise ValueError("End dates need to be sorted in ascending order")

        self._start = start
        self._dates = dates
        self._factors = factors

    @property
    def start(self) -> Date:
        return self._start

    @property
    def end(self) -> Date:
        return self._dates[-1]

    @property
    def dates(self) -> list[Date]:
        return self._dates

    @property
    def factors(self) -> list[Decimal]:
        return self._factors

    def spot(self, date: Date, method: Method) -> Decimal:
        """
        Spot discount rate to the given date.

        :param date: end date
        :param method: interpolation method
        :return: zero discount factor
        """

        # If the requested date is the start date,
        # return 1
        if date == self._start:
            return Decimal(1)

        # If the requested date is one of the inputs,
        # return it
        if date in self._dates:
            i = self._dates.index(date)
            return self._factors[i]

        # If the requested date is outside the allowed range,
        # raise an Exception
        if not self._start < date <= self.end:
            raise ValueError(f"The date needs to be in ]{self.start},  {self.end}]")

        # Find the neighbouring data points
        i = 1
        while self._dates[i] <= date:
            i += 1

        df1 = self.factors[i - 1]
        df2 = self.factors[i]

        x1 = Decimal(self._dates[i - 1] - self.start)
        x2 = Decimal(self._dates[i] - self.start)
        x = Decimal(date - self.start)

        # Interpolate
        match method:
            case method.LINEAR_ZERO_RATE:
                """
                Linear interpolation of the zero rates.
                Zero rates are the continuously compounded spot rates inferred from
                the discount curve.
                """
                y1 = -Decimal.ln(df1) / x1
                y2 = -Decimal.ln(df2) / x2
                interp = linear_interpolation(x1, y1, x2, y2, x)
                y = Decimal.exp(-interp * x)

            case method.LINEAR_DISCOUNT_FACTOR:
                """
                Linear interpolation of the discount factors.
                """
                y1 = df1
                y2 = df2
                y = linear_interpolation(x1, y1, x2, y2, x)

            case method.LOG_LINEAR_DISCOUNT_FACTOR:
                """
                Linear interpolation of the natural logarithm of the discount factors.
                # TODO check also named "FLAT_FORWARD"
                """
                y1 = Decimal.ln(df1)
                y2 = Decimal.ln(df2)
                interp = linear_interpolation(x1, y1, x2, y2, x)
                y = Decimal.exp(interp)

            case _:
                raise NotImplementedError

        return y

    def forward(self, start: Date, end: Date, method: Method) -> Decimal:
        """
        Forward starting discount factor between two dates.

        :param start: start date
        :param end: end date
        :param method: interpolation method
        :return: forward discount factor
        """

        return self.spot(end, method) / self.spot(start, method)

    @classmethod
    def flat_forward(cls, start: Date, end: Date, rate: InterestRate, day_count: DayCount) -> Self:
        """
        In a "flat forward" discount curve, all spot rates and all forward rates are equal.
        For instance, in a flat forward 1% curve, the 1Y rate, the 2Y rate and the 1Y1Y rates
        are all worth 1%.

        In this basic implentation, we compute all discount factors at instantiation.
        TODO: use a generator to give the requested discount factors on demand.

        :param start: start date
        :param end: end date
        :param rate: interest rate with associated compounding frequency
        :param day_count: day count convention
        :return: an instance of DiscountCurve with precomputed discount factors
        """
        dates = []
        factors = []
        for date in DateRange(start + Period(1, Unit.DAY), end):
            factor = discount(rate=rate, start=start, end=date, day_count=day_count)
            dates.append(date)
            factors.append(factor)

        return cls(start=start, dates=dates, factors=factors)
