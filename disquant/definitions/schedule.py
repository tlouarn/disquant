from enum import StrEnum
from typing import Optional

from holidays import HolidayBase

from disquant.definitions.business_day import Adjustment, adjust_date
from disquant.definitions.date import Date
from disquant.definitions.period import Period, Unit


# Todo add long and short stub
class Stub(StrEnum):
    FRONT = "Front"
    BACK = "Back"


# TODO add DayOfWeek
class Roll(StrEnum):
    DOM = "DayOfMonth"
    EOM = "EndOfMonth"


def generate_schedule(
    start: Date,
    end: Date,
    step: Period,
    holidays: HolidayBase,
    adjustment: Adjustment,
    stub: Stub,
    roll: Optional[Roll] = Roll.DOM,
) -> list[Date]:
    """
    Generate a schedule.

    :param start: start date
    :param end: end date
    :param step: period used to compute the regular steps (e.g. "3M")
    :param holidays: list of holidays
    :param adjustment: business day adjustment convention
    :param stub: stub convention
    :param roll: roll convention (DayOfMonth or EndOfMonth)
    :return: an ordered list of dates

    """
    # Initialize schedule
    schedule = []

    # The "EndOfMonth" roll convention applies if
    # the start date is the last day of its month
    # and the step is at least a month
    start_eom = start == start.get_eom()
    freq_eom = step >= Period(1, Unit.MONTH)
    is_eom = start_eom and freq_eom and roll == roll.EOM

    # Adjust maturity
    end = adjust_date(end, holidays, adjustment)
    schedule.append(end)

    # Exit if the maturity is closer than a step
    if end < start + step:
        return schedule

    # If the stub is FRONT, compute unadjusted dates
    # starting from the end date
    if stub == Stub.FRONT:
        date = end - step
        date = date.get_eom() if is_eom else date
        while date > start:
            schedule.append(date)
            date = date - step
            date = date.get_eom() if is_eom else date

    # If the stub is BACK, compute unadjusted dates
    # starting from the start date
    elif stub == Stub.BACK:
        date = start + step
        date = date.get_eom() if is_eom else date
        while date < end:
            schedule.append(date)
            date = date + step
            date = date.get_eom() if is_eom else date

    # Adjust intermediary dates
    schedule = [adjust_date(date, holidays, adjustment) for date in schedule]

    # Sort the dates
    return sorted(schedule)
