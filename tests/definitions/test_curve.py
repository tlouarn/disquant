from decimal import Decimal

from disquant.definitions.conventions import DayCount, year_fraction
from disquant.definitions.curve import DiscountCurve, Method
from disquant.definitions.date import Date, DateRange
from disquant.definitions.period import Period, Unit
from disquant.definitions.rate import Compounding, InterestRate


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
        Date(2016, 11, 14)
    ]
    factors = [
        Decimal("0.9999843"),
        Decimal("0.9966889"),
        Decimal("0.9942107"),
        Decimal("0.9911884"),
        Decimal("0.9880738"),
        Decimal("0.983649"),
        Decimal("0.9786276"),
        Decimal("0.9710461"),
        Decimal("0.9621778"),
        Decimal("0.9514315"),
        Decimal("0.9394919"),
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
    start = Date(2023, 10, 17)
    end = Date(2024, 10, 17)
    rate = InterestRate("0.01", Compounding.CONTINUOUS)
    day_count = DayCount.ACTUAL_360

    discount_curve = DiscountCurve.flat_forward(start=start, end=end, rate=rate, day_count=day_count)

    # Compute all spot rates
    method = Method.LOG_LINEAR_DISCOUNT_FACTOR
    for date in DateRange(start + Period(1, Unit.DAY), end):
        spot_df = discount_curve.spot(date=date, method=method)
        time = year_fraction(start=start, end=date, day_count=day_count)
        spot_rate = - Decimal.ln(spot_df) / Decimal(time)
        assert round(spot_rate, 8) == rate.value

    # Compute all 1-day forward rates
    method = Method.LOG_LINEAR_DISCOUNT_FACTOR
    for date in DateRange(start + Period(1, Unit.DAY), end - Period(1, Unit.DAY)):
        spot_df = discount_curve.forward(start=date, end=date + Period(1, Unit.DAY), method=method)
        time = year_fraction(start=date, end=date + Period(1, Unit.DAY), day_count=day_count)
        spot_rate = - Decimal.ln(spot_df) / Decimal(time)
        assert round(spot_rate, 8) == rate.value
