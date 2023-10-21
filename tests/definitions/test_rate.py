import math

from disquant.definitions.date import Date
from disquant.definitions.day_count import DayCount
from disquant.definitions.rate import Compounding, InterestRate, compound, discount


def test_init():
    value = 0.03
    rate = InterestRate(value, Compounding.ANNUAL)

    assert rate.value == value
    assert rate.compounding == Compounding.ANNUAL


def test_init_simple_interest_rate():
    rate = InterestRate(0.03)

    assert rate.value == 0.03
    assert rate.compounding is None


def test_compound():
    """
    Example taken from
    https://www.deriscope.com/excel/blog/InterestRate.xlsx
    """
    rate = InterestRate(0.04)
    start = Date(2018, 9, 7)
    end = Date(2020, 3, 7)
    compound_factor = compound(rate, start, end, DayCount.ACTUAL_365_FIXED)

    assert math.isclose(compound_factor, 1.05994520547945)


def test_discount():
    """
    Example taken from
    https://www.deriscope.com/excel/blog/InterestRate.xlsx
    """
    rate = InterestRate(0.04)
    start = Date(2018, 9, 7)
    end = Date(2020, 3, 7)
    discount_factor = discount(rate, start, end, DayCount.ACTUAL_365_FIXED)

    assert math.isclose(discount_factor, 0.94344499586435)


def test_examples_from_option_pricing_formulas():
    """
    Testing the examples from "Option Pricing Formulas" (Haug, 2nd Edition, p. 491)
    Examples were given with only 4 decimals precision.
    """
    day_count = DayCount.ACTUAL_365_FIXED

    rate_1 = InterestRate(0.08, Compounding.QUARTERLY)
    rate_2 = InterestRate(0.0792, Compounding.CONTINUOUS)

    date_1 = Date(2023, 1, 1)
    date_2 = Date(2024, 1, 1)

    cf_1 = compound(rate_1, date_1, date_2, day_count)
    cf_2 = compound(rate_2, date_1, date_2, day_count)

    assert math.isclose(cf_1, cf_2, rel_tol=0.0001)
