from dataclasses import dataclass
from enum import StrEnum
from typing import Self

from disquant.definitions.business_day import Calendar
from disquant.definitions.curve import DiscountCurve, Method
from disquant.definitions.date import Date
from disquant.definitions.day_count import DayCount
from disquant.definitions.frequency import Frequency
from disquant.definitions.money import Currency, Money
from disquant.definitions.period import Period
from disquant.definitions.rate import InterestRate, compound
from disquant.definitions.schedule import Stub, generate_schedule


class Way(StrEnum):
    PAYER = "Payer"
    RECEIVER = "Receiver"


@dataclass(frozen=True)
class FixedCoupon:
    start: Date
    end: Date
    payment: Date
    amount: Money


class FixedLeg:
    def __init__(self, way: Way, coupons: list[FixedCoupon]) -> None:
        self._way = way
        self._coupons = coupons

    @classmethod
    def generate(
        cls,
        way: Way,
        start: Date,
        end: Date,
        notional: Money,
        coupon_rate: InterestRate,
        day_count: DayCount,
        payment_frequency: Frequency,
        payment_offset: Period,
        calendar: Calendar,
    ) -> Self:
        # Get the period equivalent to the payment frequency
        step = payment_frequency.to_period()

        # Generate schedule
        schedule = generate_schedule(start=start, end=end, step=step, calendar=calendar, stub=Stub.FRONT)

        # Generate coupons
        coupons = []
        start_dates = [start] + [date for date in schedule[:-1]]
        end_dates = [date for date in schedule]
        for dates in zip(start_dates, end_dates):
            compound_factor = compound(coupon_rate, dates[0], dates[1], day_count)
            amount = notional * (compound_factor - 1)
            payment = calendar.add(dates[1], payment_offset.quantity)
            coupon = FixedCoupon(start=dates[0], end=dates[1], amount=amount, payment=payment)
            coupons.append(coupon)

        return FixedLeg(way=way, coupons=coupons)

    def compute_npv(self, discount_curve: DiscountCurve) -> Money:
        npv = Money(0, Currency.USD)

        method = Method.LOG_LINEAR_DISCOUNT_FACTOR
        for coupon in self._coupons:
            discount_factor = discount_curve.spot(coupon.payment, method)
            npv += coupon.amount * discount_factor

        sign = -1 if self._way == Way.PAYER else 1

        return sign * npv
