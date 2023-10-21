import pytest

from disquant.definitions.day_count import DayCount, year_fraction
from disquant.definitions.date import Date
from tests.definitions.test_conventions_data import ISDA_EXAMPLES


def test_init():
    day_count = DayCount("ACT/365F")

    assert day_count == DayCount.ACTUAL_365_FIXED


@pytest.mark.parametrize("start_date,end_date,day_count,expected", ISDA_EXAMPLES)
def test_year_fraction_isda(start_date: Date, end_date: Date, day_count: DayCount, expected: float):
    assert year_fraction(start_date, end_date, day_count) == expected


def test_year_fraction_act_365_fixed():
    start_date = Date(2023, 9, 18)
    end_date = Date(2023, 10, 17)
    day_count = DayCount.ACTUAL_365_FIXED

    fraction = year_fraction(start_date, end_date, day_count)

    assert fraction == 29 / 365


def test_year_fraction_actual_actual_isda():
    """
    Example taken from
    https://academybooks.nl/test/Diploma/Book-Interest%20calcs.pdf
    """
    start_date = Date(2007, 10, 1)
    end_date = Date(2008, 4, 1)
    day_count = DayCount.ACTUAL_ACTUAL_ISDA

    fraction = year_fraction(start_date, end_date, day_count)

    assert fraction == 92 / 365 + 91 / 366


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

    assert thirty_360 == 60 / 360
    assert thirty_e_360 == 60 / 360
    assert act_act_isda == 4 / 365 + 58 / 366
    assert act_365_fixed == 62 / 365
    assert act_360 == 62 / 360

    # Example 2
    start = Date(2007, 12, 28)
    end = Date(2008, 2, 29)
    thirty_360 = year_fraction(start, end, DayCount.THIRTY_360)
    thirty_e_360 = year_fraction(start, end, DayCount.THIRTY_E_360)
    act_360 = year_fraction(start, end, DayCount.ACTUAL_360)
    act_365_fixed = year_fraction(start, end, DayCount.ACTUAL_365_FIXED)
    act_act_isda = year_fraction(start, end, DayCount.ACTUAL_ACTUAL_ISDA)

    assert thirty_360 == 61 / 360
    assert thirty_e_360 == 61 / 360
    assert act_act_isda == 4 / 365 + 59 / 366
    assert act_365_fixed == 63 / 365
    assert act_360 == 63 / 360

    # Example 3
    start = Date(2007, 10, 31)
    end = Date(2008, 11, 30)
    thirty_360 = year_fraction(start, end, DayCount.THIRTY_360)
    thirty_e_360 = year_fraction(start, end, DayCount.THIRTY_E_360)
    act_360 = year_fraction(start, end, DayCount.ACTUAL_360)
    act_365_fixed = year_fraction(start, end, DayCount.ACTUAL_365_FIXED)
    act_act_isda = year_fraction(start, end, DayCount.ACTUAL_ACTUAL_ISDA)

    assert thirty_360 == 390 / 360
    assert thirty_e_360 == 390 / 360
    assert act_act_isda == 62 / 365 + 334 / 366
    assert act_365_fixed == 396 / 365
    assert act_360 == 396 / 360

    # Example 4
    start = Date(2008, 2, 1)
    end = Date(2009, 5, 31)
    thirty_360 = year_fraction(start, end, DayCount.THIRTY_360)
    thirty_e_360 = year_fraction(start, end, DayCount.THIRTY_E_360)
    act_360 = year_fraction(start, end, DayCount.ACTUAL_360)
    act_365_fixed = year_fraction(start, end, DayCount.ACTUAL_365_FIXED)
    act_act_isda = year_fraction(start, end, DayCount.ACTUAL_ACTUAL_ISDA)

    assert thirty_360 == 480 / 360
    assert thirty_e_360 == 479 / 360
    assert act_act_isda == 335 / 366 + 150 / 365
    assert act_365_fixed == 485 / 365
    assert act_360 == 485 / 360
