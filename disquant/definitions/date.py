from __future__ import annotations

import datetime as dt
from enum import Enum
from functools import total_ordering
from typing import Self

# TODO remove dependency on relativedelta
from dateutil.relativedelta import relativedelta

from disquant.definitions.period import Period, Unit

# Constants are defined here
# Used by the `Date` class but not visible in instantiated `Date` objects
ENDS_OF_MONTHS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
ENDS_OF_MONTHS_LEAP_YEAR = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
MIN_YEAR = 1901
MAX_YEAR = 2199
MIN_EXCEL = 367
MAX_EXCEL = 109574


class Weekday(str, Enum):
    MON = "MON"
    TUE = "TUE"
    WED = "WED"
    THU = "THU"
    FRI = "FRI"
    SAT = "SAT"
    SUN = "SUN"


@total_ordering
class Date:
    """
    Custom date implementation.
    Allows dates from January 1st 1901 to December 31st 2199 as per QuantLib
    implementation.
    """

    def __init__(self, year: int, month: int, day: int):
        # Base error message
        error = f"Date({year}, {month}, {day}) is invalid: "

        # Ensure the year is within defined boundaries
        if not MIN_YEAR <= year <= MAX_YEAR:
            error += f"year should be in [{MIN_YEAR}, {MAX_YEAR}]"
            raise ValueError(error)
        self._year = year

        # Ensure the month is valid
        if not 1 <= month <= 12:
            error += "month should be in [1, 12]"
            raise ValueError(error)
        self._month = month

        # Ensure the day is valid
        ends_of_months = ENDS_OF_MONTHS_LEAP_YEAR if self.is_leap else ENDS_OF_MONTHS
        if not 1 <= day <= ends_of_months[month - 1]:
            error += f"day should be in [1, {ends_of_months[month - 1]}]"
            raise ValueError(error)
        self._day = day

    def __repr__(self) -> str:
        return f"Date({self._year:02d}, {self._month:02d}, {self.day:02d})"

    def __str__(self) -> str:
        return f"{self._year:02d}-{self._month:02d}-{self.day:02d}"

    @classmethod
    def today(cls) -> Self:
        """
        Instantiate a Date for today's date.
        """
        date = dt.date.today()
        return Date(date.year, date.month, date.day)

    @classmethod
    def from_date(cls, date: dt.date) -> Self:
        """
        Instantiate a Date from a datetime.date.
        """
        return Date(date.year, date.month, date.day)

    @classmethod
    def from_excel(cls, serial: int) -> Self:
        """
        Instantiate a Date from an Excel serial date number.
        """
        if not MIN_EXCEL <= serial <= MAX_EXCEL:
            raise ValueError(f"Invalid Excel serial date number: must be in [{MIN_EXCEL}, {MAX_EXCEL}]")

        min_date = Date(1901, 1, 1)
        return min_date + Period(serial - 367, Unit.DAY)

    @classmethod
    def from_string(cls, string: str) -> Self:
        """
        Instantiate a Date from a string.
        Expected string format is "YYYY-MM-DD".
        """
        if (
                len(string) != 10
                or not string[0:4].isnumeric()
                or not string[5:7].isnumeric()
                or not string[8:10].isnumeric()
        ):
            raise ValueError(f"{string} is not a valid string: expecting YYYY-MM-DD")

        year = int(string[0:4])
        month = int(string[5:7])
        day = int(string[8:10])

        return Date(year, month, day)

    @classmethod
    def imm(cls, year: int, month: int) -> Self:
        """
        IMM = International Monetary Market
        Instantiate a Date corresponding to the IMM date for a given year and month.
        The IMM date is the third Wednesday of the month .
        """
        date = Date(year, month, 15)
        while date.weekday != "WED":
            date += Period(1, Unit.DAY)
        return date

    @classmethod
    def third_friday(cls, year: int, month: int) -> Self:
        """
        Instantiate a Date corresponding to the third Friday for a given year and month.
        The third Friday of the month is when most European index futures expire.
        """
        date = Date(year, month, 15)
        while date.weekday != "FRI":
            date += Period(1, Unit.DAY)
        return date

    def to_date(self) -> dt.date:
        """
        Convert the date to a python datetime.date object.
        """
        return dt.date(self._year, self._month, self.day)

    def to_excel(self) -> int:
        """
        Convert the date into an Excel serial number.
        Allowed dates start on January 1st 1901, i.e. after the "Excel bug" of year 1900.
        """
        period = self - Date(1901, 1, 1)
        return 367 + period

    @property
    def year(self) -> int:
        return self._year

    @property
    def month(self) -> int:
        return self._month

    @property
    def day(self) -> int:
        return self._day

    @property
    def weekday(self) -> Weekday:
        date = self.to_date()
        weekday = date.strftime("%a")
        return Weekday(weekday.upper())

    @property
    def is_weekend(self) -> bool:
        return self.weekday in [Weekday.SAT, Weekday.SUN]

    @property
    def is_weekday(self) -> bool:
        return not self.is_weekend

    @property
    def is_leap(self) -> bool:
        return self._year % 4 == 0 and (self._year % 100 != 0 or self._year % 400 == 0)

    @property
    def is_eom(self) -> bool:
        """
        Check whether the current Date is an end of month.
        """
        ends_of_months = ENDS_OF_MONTHS_LEAP_YEAR if self.is_leap else ENDS_OF_MONTHS
        return self.day == ends_of_months[self._month - 1]

    def get_eom(self) -> Date:
        """
        Return a new Date corresponding to the last day of the current month.
        """
        ends_of_months = ENDS_OF_MONTHS_LEAP_YEAR if self.is_leap else ENDS_OF_MONTHS
        last_day = ends_of_months[self._month - 1]
        return Date(self._year, self._month, last_day)

    def __add__(self, other: Period) -> Date:
        """
        Adding a Period to a Date returns a new Date.
        """
        if not isinstance(other, Period):
            raise TypeError("Only a Period can be added to a Date")

        date = dt.date(self._year, self._month, self.day)
        return self._add_delta(date, other)

    def __sub__(self, other: Date | Period) -> Date | int:
        """
        Subtracting a Date from another Date returns the number of calendar days in between as an integer.
        Subtracting a Period from a Date returns a new Date.
        """
        date = dt.date(self._year, self._month, self.day)

        if isinstance(other, Date):
            other = dt.date(other._year, other._month, other.day)
            return (date - other).days

        elif isinstance(other, Period):
            period = Period(-other.quantity, other.unit)
            return self._add_delta(date, period)

        else:
            raise TypeError(f"Only a Date or a Period can be subtracted from a Date")

    def __hash__(self):
        """
        Required in order to use a Date as a dictionary key for instance.
        """
        return hash((self._year, self._month, self.day))

    @staticmethod
    def _add_delta(date: dt.date, period: Period):
        days = period.quantity if period.unit == "D" else 0
        weeks = period.quantity if period.unit == "W" else 0
        months = period.quantity if period.unit == "M" else 0
        years = period.quantity if period.unit == "Y" else 0

        new_date = date + relativedelta(days=days, weeks=weeks, months=months, years=years)
        return Date(new_date.year, new_date.month, new_date.day)

    def __eq__(self, other: Date) -> bool:
        return self._year == other._year and self._month == other._month and self.day == other.day

    def __lt__(self, other: Date) -> bool:
        if self._year != other._year:
            return self._year < other._year

        elif self._month != other._month:
            return self._month < other._month

        elif self.day != other.day:
            return self.day < other.day

        return False


class DateRange:
    def __init__(self, start: Date, end: Date):
        self.start = start
        self.end = end

    def __contains__(self, item: Date) -> bool:
        return self.start <= item < self.end

    def __iter__(self) -> list[Date]:
        date = self.start
        while date < self.end:
            yield date
            date += Period(1, Unit.DAY)
