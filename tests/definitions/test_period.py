from disquant.definitions.period import Period, Unit


def test_init():
    period = Period(1, Unit.MONTH)

    assert period.quantity == 1
    assert period.unit == Unit.MONTH


def test_compare():
    period_1d = Period(1, Unit.DAY)
    period_7d = Period(7, Unit.DAY)
    period_1w = Period(1, Unit.WEEK)
    period_1m = Period(1, Unit.MONTH)
    period_2m = Period(2, Unit.MONTH)
    period_12m = Period(12, Unit.MONTH)
    period_18m = Period(18, Unit.MONTH)
    period_24m = Period(24, Unit.MONTH)
    period_1y = Period(1, Unit.YEAR)
    period_2y = Period(2, Unit.YEAR)

    assert period_1d < period_1w < period_1m < period_1y
    assert period_1m < period_2m
    assert period_7d == period_1w
    assert period_12m == period_1y
    assert period_24m == period_2y
    assert period_24m == 2 * period_1y
    assert period_1y < period_18m < period_2y


def test_sort():
    # Create an ordered list of periods
    periods = [
        Period(1, Unit.DAY),
        Period(7, Unit.DAY),
        Period(1, Unit.WEEK),
        Period(2, Unit.WEEK),
        Period(30, Unit.DAY),
        Period(1, Unit.MONTH),
        Period(2, Unit.MONTH),
        Period(3, Unit.MONTH),
        Period(6, Unit.MONTH),
        Period(9, Unit.MONTH),
        Period(12, Unit.MONTH),
        Period(1, Unit.YEAR),
        Period(18, Unit.MONTH),
        Period(2, Unit.YEAR),
        Period(5, Unit.YEAR),
        Period(10, Unit.YEAR),
    ]

    # Create a copy of the list and sort it by string representation
    # e.g. 10Y, 1D, 1M, 1W etc.
    string_periods = sorted(periods.copy(), key=lambda x: str(x))

    # Check that sorting it back puts the periods back in order
    assert sorted(string_periods) == periods


def test_add():
    period_1w = Period(1, Unit.WEEK)
    period_3w = Period(3, Unit.WEEK)
    period_4w = Period(4, Unit.WEEK)

    assert period_1w + period_3w == period_4w


def test_mul():
    period_1d = Period(1, Unit.DAY)
    period_1w = Period(1, Unit.WEEK)

    assert 7 * period_1d == period_1w


def test_rmul():
    period_1d = Period(1, Unit.DAY)
    period_1w = Period(1, Unit.WEEK)

    assert period_1d * 7 == period_1w
