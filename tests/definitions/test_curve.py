import math

from disquant.definitions.curve import DiscountCurve, Method
from disquant.definitions.date import Date, DateRange
from disquant.definitions.day_count import DayCount, year_fraction
from disquant.definitions.period import Period, Unit
from disquant.definitions.rate import Compounding, InterestRate, as_rate, discount

EPSILON = 0.00000001


def test_init():
    """
    Example taken from:
    http://www.derivativepricing.com/blogpage.asp?id=6
    """
    start = Date(2011, 11, 10)
    dates = [
        Date(2011, 11, 14),
        Date(2012, 5, 14),
        Date(2012, 11, 14),
        Date(2013, 5, 14),
        Date(2013, 11, 14),
        Date(2014, 5, 14),
        Date(2014, 11, 14),
        Date(2015, 5, 14),
        Date(2015, 11, 16),
        Date(2016, 5, 16),
        Date(2016, 11, 14),
    ]
    factors = [
        0.9999843,
        0.9966889,
        0.9942107,
        0.9911884,
        0.9880738,
        0.983649,
        0.9786276,
        0.9710461,
        0.9621778,
        0.9514315,
        0.9394919,
    ]

    # Build the discount curve
    discount_curve = DiscountCurve(start=start, dates=dates, factors=factors)
    assert isinstance(discount_curve, DiscountCurve)

    # Check that all the discount factors used to create the curve
    # are correctly recalculated
    method = Method.LOG_LINEAR_DISCOUNT_FACTOR
    assert all(discount_curve.spot(date=date, method=method) == factor for date, factor in zip(dates, factors))

    # Check that all input discount factors are correctly recalculated
    # as "forward-starting" discount factors with the same start date
    method = Method.LOG_LINEAR_DISCOUNT_FACTOR
    assert all(discount_curve.forward(start, date, method=method) == factor for date, factor in zip(dates, factors))


def test_flat_forward():
    # Parameters
    start = Date(2023, 10, 17)
    end = Date(2024, 10, 17)
    rate = InterestRate(0.01, Compounding.CONTINUOUS)
    day_count = DayCount.ACTUAL_360

    # Build discount curve
    discount_curve = DiscountCurve.flat_forward(start=start, end=end, rate=rate, day_count=day_count)

    # Compute all spot rates
    method = Method.LOG_LINEAR_DISCOUNT_FACTOR
    for date in DateRange(start + Period(1, Unit.DAY), end):
        spot_df = discount_curve.spot(date=date, method=method)
        time = year_fraction(start=start, end=date, day_count=day_count)
        spot_rate = -math.log(spot_df) / time
        assert spot_rate - rate.value < EPSILON

    # Compute all 1-day forward rates
    method = Method.LOG_LINEAR_DISCOUNT_FACTOR
    for date in DateRange(start + Period(1, Unit.DAY), end - Period(1, Unit.DAY)):
        spot_df = discount_curve.forward(start=date, end=date + Period(1, Unit.DAY), method=method)
        time = year_fraction(start=date, end=date + Period(1, Unit.DAY), day_count=day_count)
        spot_rate = -math.log(spot_df) / time
        assert spot_rate - rate.value < EPSILON


def test_linear_zero_rate_interpolation():
    """
    Example taken from
    https://www.isda.org/a/7KiDE/linear-interpolation-example-1-10.pdf
    """
    # LIBOR USD conventions
    compounding = Compounding.ANNUAL
    day_count = DayCount.ACTUAL_360

    # Build the discount curve from the provided quotes
    start = Date(2005, 12, 5)

    date_1m = Date(2006, 1, 9)
    libor_1m = InterestRate(0.043313, compounding)
    factor_1m = discount(libor_1m, start, date_1m, day_count)

    date_2m = Date(2006, 2, 7)
    libor_2m = InterestRate(0.043944, compounding)
    factor_2m = discount(libor_2m, start, date_2m, day_count)

    dates = [date_1m, date_2m]
    factors = [factor_1m, factor_2m]
    discount_curve = DiscountCurve(start=start, dates=dates, factors=factors)

    # Interpolate
    date = Date(2006, 1, 19)
    factor = discount_curve.spot(date, method=Method.LINEAR_ZERO_RATE)
    rate = as_rate(factor=factor, start=start, end=date, day_count=day_count, compounding=compounding)

    assert round(rate, 5) == InterestRate(0.04353, Compounding.ANNUAL)
