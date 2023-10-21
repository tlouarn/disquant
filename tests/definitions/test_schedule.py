from holidays import financial_holidays

from disquant.definitions.business_day import Adjustment
from disquant.definitions.date import Date
from disquant.definitions.period import Period, Unit
from disquant.definitions.schedule import Roll, Stub, generate_schedule


def test_generate_schedule():
    schedule = generate_schedule(
        start=Date(2023, 2, 28),
        end=Date(2023, 8, 28),
        step=Period(1, Unit.MONTH),
        holidays=financial_holidays("ECB"),
        adjustment=Adjustment.MODIFIED_FOLLOWING,
        stub=Stub.FRONT,
        roll=Roll.DOM,
    )

    assert schedule == [
        Date(2023, 3, 28),
        Date(2023, 4, 28),
        Date(2023, 5, 29),
        Date(2023, 6, 28),
        Date(2023, 7, 28),
        Date(2023, 8, 28),
    ]


def test_generate_schedule_eom():
    """
    When the schedule starts on the last day of the month
    and the roll convention is "EndOfMonth" and the step is
    equal to or larger than a month, each schedule date will
    also be a month-end.
    """
    schedule = generate_schedule(
        start=Date(2023, 2, 28),
        end=Date(2023, 8, 28),
        step=Period(1, Unit.MONTH),
        holidays=financial_holidays("ECB"),
        adjustment=Adjustment.MODIFIED_FOLLOWING,
        stub=Stub.FRONT,
        roll=Roll.EOM,
    )

    assert schedule == [
        Date(2023, 3, 31),
        Date(2023, 4, 28),
        Date(2023, 5, 31),
        Date(2023, 6, 30),
        Date(2023, 7, 31),
        Date(2023, 8, 28),
    ]
