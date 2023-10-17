import datetime as dt

import pytest

from disquant.definitions.date import Date, DateRange
from disquant.definitions.period import Period, Unit
from tests.definitions.test_date_data import YEARS


def test_constructor():
    date = Date(2023, 9, 18)

    assert date.year == 2023
    assert date.month == 9
    assert date.day == 18


def test_invalid_date_raises_value_error():
    # Test month outside [1, 12]
    with pytest.raises(ValueError):
        date = Date(2023, 15, 15)

    # Test negative day value
    with pytest.raises(ValueError):
        date = Date(2023, 2, -1)

    # Test day outside [1, 31]
    with pytest.raises(ValueError):
        date = Date(2023, 2, 32)

    # Test day does not exist
    with pytest.raises(ValueError):
        date = Date(2023, 9, 31)

    # 2023 is not a leap year
    with pytest.raises(ValueError):
        date = Date(2023, 2, 29)


def test_valid_string():
    date = Date.from_string("2023-09-18")

    assert date.year == 2023
    assert date.month == 9
    assert date.day == 18


def test_invalid_string_raises_value_error():
    with pytest.raises(ValueError):
        date = Date.from_string("20230918")

    with pytest.raises(ValueError):
        date = Date.from_string("YYYY 09 18")


def test_compare_eq():
    date_1 = Date(2023, 9, 18)
    date_2 = Date(2023, 9, 18)

    assert date_1 is not date_2
    assert date_1 == date_2


def test_compare_lt():
    date_1 = Date(2022, 9, 18)
    date_2 = Date(2023, 9, 18)
    date_3 = Date(2023, 9, 19)
    date_4 = Date(2023, 10, 18)

    assert date_1 < date_2 < date_3 < date_4


def test_add_period():
    date = Date(2023, 9, 18)
    period = Period(1, Unit.MONTH)
    maturity = date + period

    assert maturity == Date(2023, 10, 18)


def test_subtract_period():
    date = Date(2023, 9, 18)
    period = Period(1, Unit.WEEK)
    maturity = date - period

    assert maturity == Date(2023, 9, 11)


def test_subtract_date():
    date_1 = Date(2023, 9, 18)
    date_2 = Date(2023, 10, 18)

    assert date_2 - date_1 == 30


def test_imm_date_constructor():
    date = Date.imm(2023, 12)

    assert date == Date(2023, 12, 20)


def test_third_friday_constructor():
    date = Date.third_friday(2023, 12)

    assert date == Date(2023, 12, 15)


def test_today_constructor():
    date = Date.today()

    assert date.to_date() == dt.date.today()


def test_excel():
    """
    Test conversions between Excel serial numbers and Date objects.
    """
    assert Date.from_excel(367) == Date(1901, 1, 1)
    assert Date.from_excel(48000) == Date(2031, 6, 1)
    assert Date.from_excel(30000).to_excel() == 30000


def test_str():
    date = Date(2023, 9, 18)

    assert str(date) == "2023-09-18"


def test_weekday():
    assert Date(2023, 9, 18).weekday == "MON"
    assert Date(2023, 9, 19).weekday == "TUE"
    assert Date(2023, 9, 20).weekday == "WED"
    assert Date(2023, 9, 21).weekday == "THU"
    assert Date(2023, 9, 22).weekday == "FRI"
    assert Date(2023, 9, 23).weekday == "SAT"
    assert Date(2023, 9, 24).weekday == "SUN"


def test_is_weekend():
    assert not Date(2023, 9, 18).is_weekend
    assert not Date(2023, 9, 19).is_weekend
    assert not Date(2023, 9, 20).is_weekend
    assert not Date(2023, 9, 21).is_weekend
    assert not Date(2023, 9, 22).is_weekend
    assert Date(2023, 9, 23).is_weekend
    assert Date(2023, 9, 24).is_weekend


def test_is_leap_year():
    """
    Check that the function is correct for all years
    between 1901 and 2200
    All the test data is coming from QuantLib.
    https://github.com/lballabio/QuantLib/blob/master/ql/time/date.cpp
    """

    assert all(Date(1901 + i, 1, 1).is_leap == is_leap for i, is_leap in enumerate(YEARS))


def test_is_eom():
    assert Date(2024, 1, 31).is_eom
    assert Date(2024, 2, 29).is_eom
    assert Date(2023, 2, 28).is_eom

    assert not Date(2024, 2, 28).is_eom
    assert not Date(2023, 1, 30).is_eom

    # Test that there are 12 ends of months per year
    # in both leap and non-leap years
    assert sum(1 if date.is_eom else 0 for date in DateRange(Date(2023, 1, 1), Date(2024, 1, 1))) == 12
    assert sum(1 if date.is_eom else 0 for date in DateRange(Date(2024, 1, 1), Date(2025, 1, 1))) == 12


def test_get_eom():
    assert Date(2024, 1, 1).get_eom() == Date(2024, 1, 31)
    assert Date(2023, 12, 31).get_eom() == Date(2023, 12, 31)
