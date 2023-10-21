from disquant.definitions.business_day import Adjustment, Calendar
from disquant.definitions.date import Date
from disquant.definitions.period import Period, Unit
from disquant.definitions.schedule import Roll, Stub, generate_schedule


def test_generate_schedule():
    schedule = generate_schedule(
        start=Date(2023, 2, 28),
        end=Date(2023, 8, 28),
        step=Period(1, Unit.MONTH),
        calendar=Calendar("TARGET", Adjustment.MODIFIED_FOLLOWING),
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
        calendar=Calendar("TARGET", Adjustment.MODIFIED_FOLLOWING),
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


def test_generate_schedule_tenor_6m():
    """
    Example taken from
    http://gouthamanbalaraman.com/blog/interest-rate-swap-quantlib-python.html
    """

    calendar = Calendar("USA", Adjustment.MODIFIED_FOLLOWING)

    calculation_date = Date(2015, 10, 20)
    settlement_date = calendar.add(date=calculation_date, business_days=5)
    maturity_date = calendar.add_period(date=settlement_date, period=Period(10, Unit.YEAR))

    schedule = generate_schedule(
        start=settlement_date,
        end=maturity_date,
        step=Period(6, Unit.MONTH),
        calendar=calendar,
        stub=Stub.FRONT,
        roll=Roll.DOM,
    )

    assert schedule == [
        Date(2016, 4, 27),
        Date(2016, 10, 27),
        Date(2017, 4, 27),
        Date(2017, 10, 27),
        Date(2018, 4, 27),
        Date(2018, 10, 29),
        Date(2019, 4, 29),
        Date(2019, 10, 28),
        Date(2020, 4, 27),
        Date(2020, 10, 27),
        Date(2021, 4, 27),
        Date(2021, 10, 27),
        Date(2022, 4, 27),
        Date(2022, 10, 27),
        Date(2023, 4, 27),
        Date(2023, 10, 27),
        Date(2024, 4, 29),
        Date(2024, 10, 28),
        Date(2025, 4, 28),
        Date(2025, 10, 27),
    ]


def test_generate_schedule_tenor_3m():
    """
    Example taken from
    http://gouthamanbalaraman.com/blog/interest-rate-swap-quantlib-python.html
    """

    calendar = Calendar("USA", Adjustment.MODIFIED_FOLLOWING)

    calculation_date = Date(2015, 10, 20)
    settlement_date = calendar.add(date=calculation_date, business_days=5)
    maturity_date = calendar.add_period(date=settlement_date, period=Period(10, Unit.YEAR))

    schedule = generate_schedule(
        start=settlement_date,
        end=maturity_date,
        step=Period(3, Unit.MONTH),
        calendar=calendar,
        stub=Stub.FRONT,
        roll=Roll.DOM,
    )

    assert schedule == [
        Date(2016, 1, 27),
        Date(2016, 4, 27),
        Date(2016, 7, 27),
        Date(2016, 10, 27),
        Date(2017, 1, 27),
        Date(2017, 4, 27),
        Date(2017, 7, 27),
        Date(2017, 10, 27),
        Date(2018, 1, 29),
        Date(2018, 4, 27),
        Date(2018, 7, 27),
        Date(2018, 10, 29),
        Date(2019, 1, 28),
        Date(2019, 4, 29),
        Date(2019, 7, 29),
        Date(2019, 10, 28),
        Date(2020, 1, 27),
        Date(2020, 4, 27),
        Date(2020, 7, 27),
        Date(2020, 10, 27),
        Date(2021, 1, 27),
        Date(2021, 4, 27),
        Date(2021, 7, 27),
        Date(2021, 10, 27),
        Date(2022, 1, 27),
        Date(2022, 4, 27),
        Date(2022, 7, 27),
        Date(2022, 10, 27),
        Date(2023, 1, 27),
        Date(2023, 4, 27),
        Date(2023, 7, 27),
        Date(2023, 10, 27),
        Date(2024, 1, 29),
        Date(2024, 4, 29),
        Date(2024, 7, 29),
        Date(2024, 10, 28),
        Date(2025, 1, 27),
        Date(2025, 4, 28),
        Date(2025, 7, 28),
        Date(2025, 10, 27),
    ]
