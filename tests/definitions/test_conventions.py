from decimal import Decimal

import pytest

from disquant.definitions.conventions import DayCount, year_fraction
from disquant.definitions.date import Date
from tests.definitions.test_conventions_data import ISDA_EXAMPLES


def test_init():
    day_count = DayCount("ACT/365F")

    assert day_count == DayCount.ACTUAL_365_FIXED


@pytest.mark.parametrize("start_date,end_date,day_count,expected", ISDA_EXAMPLES)
def test_year_fraction_isda(start_date: Date, end_date: Date, day_count: DayCount, expected: Decimal):
    assert year_fraction(start_date, end_date, day_count) == expected


def test_year_fraction_act_365_fixed():
    start_date = Date(2023, 9, 18)
    end_date = Date(2023, 10, 17)
    day_count = DayCount.ACTUAL_365_FIXED

    fraction = year_fraction(start_date, end_date, day_count)

    assert fraction == Decimal(29) / Decimal(365)


def test_year_fraction_actual_actual_isda():
    """
    Example taken from
    https://academybooks.nl/test/Diploma/Book-Interest%20calcs.pdf
    """
    start_date = Date(2007, 10, 1)
    end_date = Date(2008, 4, 1)
    day_count = DayCount.ACTUAL_ACTUAL_ISDA

    fraction = year_fraction(start_date, end_date, day_count)

    assert fraction == Decimal(92) / Decimal(365) + Decimal(91) / Decimal(366)


def test_year_fraction_deltaquants():
    """
    Examples taken from:
    http://www.deltaquants.com/day-count-conventions
    """
    # Example 1
    start = Date(2007, 12, 28)
    end = Date(2008, 2, 28)
    thirty_360 = year_fraction(start, end, DayCount.THIRTY_360)
    thirty_e_360 = year_fraction(start, end, DayCount.THIRTY_E_360)
    act_360 = year_fraction(start, end, DayCount.ACTUAL_360)
    act_365_fixed = year_fraction(start, end, DayCount.ACTUAL_365_FIXED)
    act_act_isda = year_fraction(start, end, DayCount.ACTUAL_ACTUAL_ISDA)

    assert thirty_360 == Decimal(60) / Decimal(360)
    assert thirty_e_360 == Decimal(60) / Decimal(360)
    assert act_act_isda == Decimal(4) / Decimal(365) + Decimal(58) / Decimal(366)
    assert act_365_fixed == Decimal(62) / Decimal(365)
    assert act_360 == Decimal(62) / Decimal(360)

    # Example 2
    start = Date(2007, 12, 28)
    end = Date(2008, 2, 29)
    thirty_360 = year_fraction(start, end, DayCount.THIRTY_360)
    thirty_e_360 = year_fraction(start, end, DayCount.THIRTY_E_360)
    act_360 = year_fraction(start, end, DayCount.ACTUAL_360)
    act_365_fixed = year_fraction(start, end, DayCount.ACTUAL_365_FIXED)
    act_act_isda = year_fraction(start, end, DayCount.ACTUAL_ACTUAL_ISDA)

    assert thirty_360 == Decimal(61) / Decimal(360)
    assert thirty_e_360 == Decimal(61) / Decimal(360)
    assert act_act_isda == Decimal(4) / Decimal(365) + Decimal(59) / Decimal(366)
    assert act_365_fixed == Decimal(63) / Decimal(365)
    assert act_360 == Decimal(63) / Decimal(360)

    # Example 3
    start = Date(2007, 10, 31)
    end = Date(2008, 11, 30)
    thirty_360 = year_fraction(start, end, DayCount.THIRTY_360)
    thirty_e_360 = year_fraction(start, end, DayCount.THIRTY_E_360)
    act_360 = year_fraction(start, end, DayCount.ACTUAL_360)
    act_365_fixed = year_fraction(start, end, DayCount.ACTUAL_365_FIXED)
    act_act_isda = year_fraction(start, end, DayCount.ACTUAL_ACTUAL_ISDA)

    assert thirty_360 == Decimal(390) / Decimal(360)
    assert thirty_e_360 == Decimal(390) / Decimal(360)
    assert act_act_isda == Decimal(62) / Decimal(365) + Decimal(334) / Decimal(366)
    assert act_365_fixed == Decimal(396) / Decimal(365)
    assert act_360 == Decimal(396) / Decimal(360)

    # Example 4
    start = Date(2008, 2, 1)
    end = Date(2009, 5, 31)
    thirty_360 = year_fraction(start, end, DayCount.THIRTY_360)
    thirty_e_360 = year_fraction(start, end, DayCount.THIRTY_E_360)
    act_360 = year_fraction(start, end, DayCount.ACTUAL_360)
    act_365_fixed = year_fraction(start, end, DayCount.ACTUAL_365_FIXED)
    act_act_isda = year_fraction(start, end, DayCount.ACTUAL_ACTUAL_ISDA)

    assert thirty_360 == Decimal(480) / Decimal(360)
    assert thirty_e_360 == Decimal(479) / Decimal(360)
    assert act_act_isda == Decimal(335) / Decimal(366) + Decimal(150) / Decimal(365)
    assert act_365_fixed == Decimal(485) / Decimal(365)
    assert act_360 == Decimal(485) / Decimal(360)
