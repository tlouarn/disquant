import math

from disquant.definitions.business_day import Adjustment, Calendar
from disquant.definitions.curve import DiscountCurve
from disquant.definitions.date import Date
from disquant.definitions.day_count import DayCount
from disquant.definitions.frequency import Frequency
from disquant.definitions.money import Currency, Money
from disquant.definitions.period import Period, Unit
from disquant.definitions.rate import Compounding, InterestRate
from disquant.instruments.irs import FixedLeg, Way


def test_compute_fixed_leg_npv():
    """
    Example taken from
    http://gouthamanbalaraman.com/blog/interest-rate-swap-quantlib-python.html
    """

    calendar = Calendar("USA", Adjustment.MODIFIED_FOLLOWING)

    calculation_date = Date(2015, 10, 20)
    settlement_date = calendar.add(date=calculation_date, business_days=5)
    maturity_date = calendar.add_period(date=settlement_date, period=Period(10, Unit.YEAR))

    # Generate fixed leg
    fixed_leg = FixedLeg.generate(
        way=Way.PAYER,
        start=settlement_date,
        end=maturity_date,
        notional=Money(10_000_000, Currency.USD),
        coupon_rate=InterestRate(0.025, Compounding.ANNUAL),
        day_count=DayCount("ACT/360"),
        payment_frequency=Frequency("SemiAnnual"),
        payment_offset=Period(0, Unit.DAY),
        calendar=calendar,
    )

    # Compute fixed leg npv
    risk_free_rate = InterestRate(0.01, Compounding.CONTINUOUS)
    discount_curve = DiscountCurve.flat_forward(
        start=calculation_date, end=maturity_date, rate=risk_free_rate, day_count=DayCount("ACT/365F")
    )
    npv = fixed_leg.compute_npv(discount_curve)

    assert math.isclose(npv, -2407495.2348627294)
