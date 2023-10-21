from enum import StrEnum

from holidays import HolidayBase

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
