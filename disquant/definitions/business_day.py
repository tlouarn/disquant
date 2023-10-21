from enum import StrEnum
from typing import Optional

from holidays import HolidayBase, country_holidays, financial_holidays

from disquant.definitions.date import Date
from disquant.definitions.period import Period, Unit


class Adjustment(StrEnum):
    UNADJUSTED = "Unadjusted"
    PREVIOUS = "Previous"
    MODIFIED_PREVIOUS = "ModifiedPrevious"
    FOLLOWING = "Following"
    MODIFIED_FOLLOWING = "ModifiedFollowing"


def previous(date: Date, holidays: HolidayBase) -> Date:
    """
    Previous business day adjustment.
    """
    adjusted_date = date
    while adjusted_date.is_weekend or adjusted_date.to_date() in holidays:
        adjusted_date = adjusted_date - Period(1, Unit.DAY)
    return adjusted_date


def modified_previous(date: Date, holidays: HolidayBase) -> Date:
    """
    ModifiedPrevious business day adjustment.
    """
    adjusted_date = previous(date, holidays)
    if adjusted_date.month == date.month:
        return adjusted_date
    return following(date, holidays)


def following(date: Date, holidays: HolidayBase) -> Date:
    """
    Following business day adjustment.
    """
    adjusted_date = date
    while adjusted_date.is_weekend or adjusted_date.to_date() in holidays:
        adjusted_date = adjusted_date + Period(1, Unit.DAY)
    return adjusted_date


def modified_following(date: Date, holidays: HolidayBase) -> Date:
    """
    ModifiedFollowing business day adjustment.
    """
    adjusted_date = following(date, holidays)
    if adjusted_date.month == date.month:
        return adjusted_date
    return previous(date, holidays)


def adjust_date(date: Date, holidays: HolidayBase, convention: Adjustment) -> Date:
    """
    Base method to adjust a date based on given holidays and a business day convention.
    """
    match convention:
        case Adjustment.UNADJUSTED:
            return date
        case Adjustment.PREVIOUS:
            return previous(date, holidays)
        case Adjustment.MODIFIED_PREVIOUS:
            return modified_previous(date, holidays)
        case Adjustment.FOLLOWING:
            return following(date, holidays)
        case Adjustment.MODIFIED_FOLLOWING:
            return modified_following(date, holidays)
        case _:
            raise NotImplementedError(f"{convention}")


MAPPING = {"TARGET": financial_holidays("ECB"), "USA": country_holidays("US")}


class Calendar:
    def __init__(self, identifier: Optional[str] = None, adjustment: Optional[Adjustment] = None) -> None:
        self._identifier = identifier
        self._adjustment = adjustment or Adjustment.UNADJUSTED

        # Map the identifier to holidays
        self._holidays = MAPPING[identifier] if identifier else []

    def is_closed(self, date: Date) -> bool:
        return date.is_weekend or date in self._holidays

    def is_open(self, date: Date) -> bool:
        return not self.is_closed(date)

    def add(self, date: Date, business_days: int) -> Date:
        """
        Add a number of good business days to a date with respect to
        holidays and good business day adjustment convention specified
        in the calendar. Works with a positive or negative number of days.

        :param date: original date
        :param business_days: positive or negative number of business days
        :return: new date
        """
        remaining_days = abs(business_days)
        factor = 1 if business_days >= 0 else -1
        while remaining_days > 0:
            date = self.adjust(date + factor * Period(1, Unit.DAY))
            remaining_days -= 1
        return date

    def add_period(self, date: Date, period: Period) -> Date:
        """
        Add a period to a date and adjust with respect to holidays and
        good business day adjustment convention specified in the calendar.
        Works with positive or negative periods.

        :param date: original date
        :param period: period to add
        :return: new date
        """
        return self.adjust(date + period)

    def adjust(self, date: Date) -> Date:
        match self._adjustment:
            case Adjustment.UNADJUSTED:
                return date

            case Adjustment.PREVIOUS:
                return previous(date, self._holidays)

            case Adjustment.MODIFIED_PREVIOUS:
                return modified_previous(date, self._holidays)

            case Adjustment.FOLLOWING:
                return following(date, self._holidays)

            case Adjustment.MODIFIED_FOLLOWING:
                return modified_following(date, self._holidays)

            case _:
                raise NotImplementedError
